"""Every State, UT and city, every year: the datasets behind the trends dashboard.

The single-place series in series.py follow one row (Chennai, Tamil Nadu)
through a table across the years. This module reads every row of the same
tables, works out which State, UT or city each row is, and returns one tidy
record per place, year, category, sex and age group:

    year, place, ptype, group, cat, sex, age, value, check, source

``ptype`` is state, ut, city or total (All India, Total (States) ...).
``source`` is ncrb (a table NCRB published) or ogd (the "Suicides in India
2001-2012" dataset NCRB contributed to data.gov.in, which adds 2001-2003 and an
age breakdown for every suicide table up to 2012).

Only records that pass their checks are returned: a category's sexes add up to
its printed total, a traffic row's slots add up to its printed total, a rate
matches suicides / population. Records with nothing printed to check against
are kept for text-layer tables, which are copied digit for digit.
"""

from __future__ import annotations

import difflib
import re
from functools import lru_cache

import pandas as pd

from .harmonise import CAUSES, EDUCATION, MEANS, PROFESSION, age_band, standard
from .lib import LISTING_RANK, ROOT, SCANNED, find_tables, q
from .series import (
    CITY_NAMES, MONTHS, SLOTS, _traffic_groups, best_reading, categories, month_slot, read_blocks, sex_of,
    suicide_rates, time_slot,
)
from .topics import TOPICS, tables_for

SEXES = ["Male", "Female", "Transgender"]
OK = {"ok", "ok (vs grand total)", "derived (sum of sexes)", "derived"}
OGD_FILE = ROOT / "data" / "ogd" / "suicides-in-india-2001-2012.csv.gz"  # data.gov.in, via github.com/elseasama/Indian-cities-births-and-deaths
# Reclaim Chennai's own compilations from the ADSI reports, github.com/elseasama/OpenDataChennai
ODC_RATES = ROOT / "data" / "ogd" / "opendatachennai-suicide-rate-state-city-1998-2020.csv"
ODC_CITY_AGE = ROOT / "data" / "ogd" / "opendatachennai-suicides-major-cities-sex-age-2019.csv"

# --------------------------------------------------------------------------- places


@lru_cache(maxsize=1)
def known_cities() -> tuple[str, ...]:
    """City names printed in at least three text-layer years: the reference that scanned and odd spellings snap to."""
    from ncrb.entities import standardise

    t = q("SELECT DISTINCT t.year, c.name, c.section FROM cells c JOIN tables t USING (table_id) WHERE t.publication = 'adsi' "
          "AND t.year >= 2001 AND t.method IN ('pdf_text', 'excel') AND regexp_matches(lower(t.title), 'city|cities') "
          "AND regexp_matches(lower(t.title), 'time of occurrence|rate of suicides|incidence and rate|month')")
    years: dict[str, set] = {}
    for y, n, sec in zip(t.year, t.name, t.section):
        c = clean_city(n)
        if not c or len(c) < 3 or re.search(r"total|india|\d", c, re.I):
            continue
        if standardise(str(n))[1] in ("state", "ut", "total") and c not in CITY_NAMES.values():
            continue
        years.setdefault(c, set()).add(y)
    keep: list[str] = []
    for c, ys in sorted(years.items(), key=lambda kv: -len(kv[1])):
        # the most-printed spelling wins; truncations and labels run together with a neighbour are dropped
        if len(ys) >= 3 and not re.match(r"states?\b|m\s", c, re.I) and not difflib.get_close_matches(c, keep, n=1, cutoff=0.85):
            if not any(k in c and k != c for k in keep):
                keep.append(c)
    return tuple(sorted(set(keep) | set(CITY_NAMES.values())))


def clean_city(name: str) -> str:
    n = re.sub(r"^[\W\d]+[.,]?\s*", "", str(name))
    n = re.sub(r"\s*\(.*?\)\s*|\bcity\b|[*#@!$+]|\s\d+\s", " ", n, flags=re.I)
    n = re.sub(r"\s+", " ", n).strip().title()
    return CITY_NAMES.get(n, n)


def resolve(name: str, section: str, scanned: bool, year: int | None = None) -> tuple[str, str] | None:
    """(standard name, type) for a printed row label, or None for rows that are not places. ``year`` (the table's)
    tells Bombay State (to 1959) or Hyderabad State (to 1956) from the city."""
    from ncrb.entities import standardise

    raw = re.sub(r"^[\W\d]+[.,]?\s*", "", str(name or "")).strip()
    raw = re.sub(r"\s*\[line \d+\]\s*$", "", raw, flags=re.I)
    if not raw or len(raw) < 2:
        return None
    std, kind = standardise(raw, None if re.search(r"cit", str(section or ""), re.I) else year)
    in_city = bool(re.search(r"cit", str(section or ""), re.I)) or bool(re.search(r"\bcity\b", raw, re.I))
    c = clean_city(raw)
    if kind == "total":
        low = std.lower()
        if "cit" in low or "crs" in low:
            return "Total (Cities)", "total"
        if re.search(r"\bstates?\b", low):
            return "Total (States)", "total"
        if re.search(r"\buts?\b|union", low):
            return "Total (UTs)", "total"
        return "All India", "total"
    # 'Madras' is both the old Tamil Nadu and Chennai; Delhi and Chandigarh are UTs and cities
    if in_city and (kind not in ("state", "ut") or c in CITY_NAMES or raw.title() in CITY_NAMES):
        hit = difflib.get_close_matches(c, known_cities(), n=1, cutoff=0.86 if scanned else 0.9)
        if hit:
            return hit[0], "city"
        return (c, "city") if not scanned and c else None
    if kind in ("state", "ut"):
        return std, kind
    if not in_city:
        # city-only tables (2014+ 'City wise') carry no section heading
        hit = difflib.get_close_matches(c, known_cities(), n=1, cutoff=0.9)
        if hit:
            return hit[0], "city"
    return None


# --------------------------------------------------------------------------- reading every row


def _siblings(t) -> list[str]:
    """A workbook split into one sheet per sex (2014-15) is read as one table."""
    m = re.match(r"(.+_t)\d+$", t.table_id)
    if t.method != "excel" or not m:
        return [t.table_id]
    return q("SELECT table_id FROM tables WHERE table_id LIKE ?", [m.group(1) + "%"]).table_id.tolist()


def vlm_rows(table_id: str) -> list[tuple[str, str, pd.DataFrame]]:
    """Every row of a scanned table as read by the AI OCR model: (label, section, cells)."""
    try:
        from ncrb.assemble import assemble
        from ncrb.crawl import ROOT as RAW
        from ncrb.pdftable import col_label, parse_number
        from ncrb.vlm import DEFAULT_MODEL
        from ncrb.vlm_tables import cache_path, file_sha, page_segments
    except ImportError:
        return []
    t = q("SELECT source_file, pages, year FROM tables WHERE table_id = ?", [table_id])
    if t.empty:
        return []
    path = RAW / t.source_file[0]
    a, b = (int(x) for x in str(t.pages[0]).split("-")) if "-" in str(t.pages[0]) else (1, 1)
    sha = file_sha(path)
    segs = []
    for p in range(a, b + 1):
        cp = cache_path(DEFAULT_MODEL, sha, p)
        if cp.exists():
            segs += page_segments(cp.read_text(encoding="utf-8"), p)
    out = []
    for tab in assemble(segs) if segs else []:
        for r in tab.rows:
            cells = []
            for cid, raw in r.cells.items():
                hdr = tab.columns.get(cid, [])
                cells.append({
                    "col_no": col_label(cid), "column": " | ".join(hdr), **{f"h{i + 1}": (hdr[i] if i < len(hdr) else "") for i in range(5)},
                    "value": parse_number(raw), "raw": raw, "source": "ai_ocr",
                })
            if cells:
                out.append((r.label, r.section or "", pd.DataFrame(cells)))
    return out


def all_readings(topic: str) -> tuple[pd.DataFrame, dict[int, dict[tuple[str, str], list[pd.DataFrame]]]]:
    """For each year, every place in the chosen table with its readings (text/Tesseract first, AI OCR second)."""
    from .lib import col_order

    picked = tables_for(topic)
    out: dict[int, dict] = {}
    for t in picked.itertuples():
        scanned = t.method in SCANNED
        ids = _siblings(t)
        marks = ",".join("?" for _ in ids)
        cells = q(f'SELECT table_id, "row", section, name, col_no, "column", h1, h2, h3, h4, h5, value, raw FROM cells WHERE table_id IN ({marks})', ids)
        cells["_o"] = cells.col_no.map(col_order)
        places: dict[tuple[str, str], list[pd.DataFrame]] = {}
        seen: dict[tuple[str, str, str], int] = {}
        for (tid, row), g in cells.groupby(["table_id", "row"], sort=False):
            key = resolve(g.name.iloc[0], g.section.iloc[0], scanned)
            if not key:
                continue
            # a place printed twice in one sheet (a facing page) keeps its first row
            if seen.setdefault((key[0], key[1], tid), row) != row:
                continue
            g = g.sort_values("_o").drop(columns="_o").assign(source="ocr" if scanned else "text")
            places.setdefault(key, [])
            if places[key] and ids != [t.table_id]:
                places[key][0] = pd.concat([places[key][0], g], ignore_index=True)   # sibling sheet
            elif not places[key]:
                places[key].append(g)
        if scanned:
            for label, section, g in vlm_rows(t.table_id):
                key = resolve(label, section, True)
                if key:
                    places.setdefault(key, [])
                    if len(places[key]) < 2:
                        places[key].append(g)
        out[int(t.year)] = places
    # scanned years where no extracted table had the reference place: try the AI reading of each candidate
    tp = TOPICS[topic]
    allc = find_tables(tp["pub"], tp["title"], exclude=tp.get("exclude"))
    extra = []
    for y, g in allc[allc.method.isin(SCANNED) & ~allc.year.isin(out.keys())].groupby("year"):
        for c in g.sort_values("listing", key=lambda s: s.map(LISTING_RANK).fillna(9)).itertuples():
            places = {}
            for label, section, cells in vlm_rows(c.table_id):
                key = resolve(label, section, True)
                if key and key not in places:
                    places[key] = [cells]
            if len(places) >= 5:
                out[int(y)] = places
                extra.append(c)
                break
    if extra:
        picked = pd.concat([picked, pd.DataFrame(extra).drop(columns="Index", errors="ignore")], ignore_index=True)
    PROV[topic] = picked[["year", "title", "source_url", "method"]].copy()
    return picked, out


# the table read for each topic and year, for the credit line under every chart
PROV: dict[str, pd.DataFrame] = {}


# --------------------------------------------------------------------------- readers


def read_traffic(topic: str, n: int, slot_fn, labels: list[str]) -> pd.DataFrame:
    picked, by_year = all_readings(topic)
    recs = []
    for year, places in sorted(by_year.items()):
        for (place, ptype), readings in places.items():
            def reader(r):
                r = r.reset_index(drop=True)
                return read_blocks(r, n, slot_fn, _traffic_groups(r, n + 1), positional=r["source"].iloc[0] == "text")

            df, src = best_reading(readings, reader)
            if df.empty:
                continue
            for x in df.itertuples():
                recs.append((year, place, ptype, x.group, labels[x.k], "", "", x.value, x.check, src))
    return frame(recs)


def read_persons(topic: str, labels_rx: list[tuple[str, str]]) -> pd.DataFrame:
    """Persons died in traffic accidents (2021+ state tables): heading = slot | accident type | Injured/Died."""
    picked, by_year = all_readings(topic)
    recs = []
    for year, places in sorted(by_year.items()):
        for (place, ptype), readings in places.items():
            rows = []
            for c in readings[0].itertuples():
                parts = [x.strip() for x in str(c.column).split("|")]
                if len(parts) < 3 or not re.search(r"died|killed", parts[2], re.I):
                    continue
                cat = next((nm for nm, rx in labels_rx if re.search(rx, parts[0], re.I)), None)
                kind = ("Road" if re.search(r"^road", parts[1], re.I) else "Railway crossing" if re.search(r"crossing", parts[1], re.I)
                        else "Railway" if re.search(r"rail", parts[1], re.I) else "Total traffic")
                if cat:
                    rows.append((kind, cat, c.value))
            d = pd.DataFrame(rows, columns=["group", "cat", "value"])
            for g, x in d.groupby("group"):
                tot = x[x.cat == "Total"].value
                parts = x[x.cat != "Total"].value.sum()
                ok = "ok" if len(tot) and abs(parts - tot.iloc[0]) <= 1 else ("no total" if not len(tot) else "mismatch")
                for r in x[x.cat != "Total"].itertuples():
                    recs.append((year, place, ptype, g, r.cat, "", "", r.value, ok, "text"))
    return frame(recs)


def read_categories(topics: list[str], table: list | None) -> pd.DataFrame:
    """Category x sex (x age) tables. ``table`` harmonises the category names; None keeps them (age groups)."""
    recs = []
    done: set[tuple[int, str, str]] = set()
    for topic in topics:
        picked, by_year = all_readings(topic)
        for year, places in sorted(by_year.items()):
            for (place, ptype), readings in places.items():
                if (year, place, ptype) in done:
                    continue
                df, src = best_reading(readings, categories)
                if df.empty:
                    continue
                done.add((year, place, ptype))
                df = df.assign(year=year, place=place, ptype=ptype, source=src)
                recs.append(df)
    if not recs:
        return frame([])
    d = pd.concat(recs, ignore_index=True)
    d["printed"] = d["category"]
    d["cat"] = d["category"].map(lambda c: standard(c, table)) if table else d["category"]
    return d


def tidy_categories(d: pd.DataFrame, place_totals: dict | None = None) -> pd.DataFrame:
    """Harmonised categories summed; checks carried; scanned years checked against the place's total."""
    if d.empty:
        return frame([])
    d = d.copy()
    d["age"] = d["age"].map(lambda a: "all ages" if a in ("", "Total") else age_band(a))
    grand = d[d["category"].str.match(r"^\W*(grand\s+)?total\W*$|^\W*grand\b", case=False, na=False)]
    gmax = grand.groupby(["year", "place", "ptype"]).value.max().to_dict()
    d = d[d["cat"].notna() & d["sex"].isin(SEXES + ["Total"])]
    # scanned: per-category checks can pass by chance, so the year must also add up for the place
    bad = set()
    for (y, pl, pt), g in d[d.source != "text"].groupby(["year", "place", "ptype"]):
        parts = g[g.sex.isin(SEXES) & (g.age == "all ages")].value.sum()
        targets = [x for x in (gmax.get((y, pl, pt)), (place_totals or {}).get((y, pl))) if x == x and x]
        if not any(abs(parts - t) <= 0.02 * t for t in targets):
            bad.add((y, pl, pt))
    d = d[[(k not in bad) for k in zip(d.year, d.place, d.ptype)]]
    d = d[d["check"].isin(OK) | ((d["check"] == "no total") & (d.source == "text"))]
    out = (d.groupby(["year", "place", "ptype", "cat", "sex", "age", "source"], as_index=False)
           .agg(value=("value", "sum"), check=("check", "first")))
    out["group"] = ""
    out["source"] = "ncrb"
    return out[COLS]


def add_both_sexes(d: pd.DataFrame) -> pd.DataFrame:
    """Where a table prints no both-sexes figure (2014-15 sheets, 2021+ age tables), add the sexes up."""
    keys = ["year", "place", "ptype", "group", "cat", "age"]
    has = d[d.sex == "Total"][keys].drop_duplicates()
    s = d[d.sex.isin(SEXES)].groupby(keys, as_index=False).agg(value=("value", "sum"), source=("source", "first"))
    s = s.merge(has, on=keys, how="left", indicator=True)
    s = s[s["_merge"] == "left_only"].drop(columns="_merge").assign(sex="Total", check="derived")
    return pd.concat([d, s[COLS]], ignore_index=True)


# --------------------------------------------------------------------------- data.gov.in, 2001-2012


@lru_cache(maxsize=1)
def ogd() -> pd.DataFrame:
    """'Suicides in India 2001-2012', State x Year x Type x Gender x Age group, as NCRB gave it to data.gov.in."""
    if not OGD_FILE.exists():
        return pd.DataFrame()
    from ncrb.entities import standardise

    d = pd.read_csv(OGD_FILE)
    names = {n: standardise(n) for n in d.State.unique()}
    d["place"] = d.State.map(lambda n: names[n][0])
    d["ptype"] = d.State.map(lambda n: names[n][1])
    d.loc[d.State.str.contains("All India"), ["place", "ptype"]] = ["All India", "total"]
    d.loc[d.State.str.contains(r"Total \(States\)"), ["place", "ptype"]] = ["Total (States)", "total"]
    d.loc[d.State.str.contains(r"Total \(Uts\)", case=False), ["place", "ptype"]] = ["Total (UTs)", "total"]
    d["age"] = d.Age_group.replace({"0-100+": "all ages"})   # 0-14, 15-29, 30-44, 45-59, 60+ as in NCRB's 2001-2013 tables
    return d


def ogd_dataset(type_code: str, table: list | None) -> pd.DataFrame:
    d = ogd()
    if d.empty:
        return frame([])
    d = d[d.Type_code == type_code].copy()
    d["cat"] = d.Type.map(lambda c: standard(c, table)) if table else d.Type
    d = d[d.cat.notna()]
    by_age = d.groupby(["Year", "place", "ptype", "cat", "Gender", "age"], as_index=False).Total.sum()
    all_ages = by_age.groupby(["Year", "place", "ptype", "cat", "Gender"], as_index=False).Total.sum().assign(age="all ages")
    x = pd.concat([by_age[by_age.age != "all ages"], all_ages], ignore_index=True)
    x = x.rename(columns={"Year": "year", "Gender": "sex", "Total": "value"})
    both = x.groupby(["year", "place", "ptype", "cat", "age"], as_index=False).value.sum().assign(sex="Total")
    x = pd.concat([x, both], ignore_index=True)
    x["group"] = ""
    x["check"] = "ok"
    x["source"] = "ogd"
    return x[COLS]


def merge_sources(ncrb: pd.DataFrame, gov: pd.DataFrame) -> pd.DataFrame:
    """NCRB's printed tables first. data.gov.in fills (place, year) pairs they lack, and every age breakdown up to 2012."""
    if gov.empty:
        return ncrb
    have = set(zip(ncrb.year, ncrb.place, ncrb.ptype))
    have_age = set(zip(ncrb[ncrb.age != "all ages"].year, ncrb[ncrb.age != "all ages"].place))
    keep = [((y, p, t) not in have) or (a != "all ages" and (y, p) not in have_age)
            for y, p, t, a in zip(gov.year, gov.place, gov.ptype, gov.age)]
    return pd.concat([ncrb, gov[keep]], ignore_index=True)


# --------------------------------------------------------------------------- the datasets

COLS = ["year", "place", "ptype", "group", "cat", "sex", "age", "value", "check", "source"]


def frame(recs) -> pd.DataFrame:
    return pd.DataFrame(recs, columns=COLS)


def traffic_time() -> pd.DataFrame:
    """The time and month tables count the same accidents, so a scanned year whose two totals disagree is dropped."""
    t = read_traffic("traffic_time_chennai", 8, time_slot, SLOTS)
    m = traffic_month()
    mt = m[(m.group == "Road") & (m.check == "ok")].groupby(["year", "place", "ptype"]).value.sum()
    tt = t[(t.group == "Road") & (t.check == "ok") & (t.source != "text")].groupby(["year", "place", "ptype"]).value.sum()
    both = pd.concat([tt, mt], axis=1, keys=["t", "m"]).dropna()
    bad = set(both[(both.t - both.m).abs() > 0.02 * both.m].index)
    hit = [(k in bad) for k in zip(t.year, t.place, t.ptype)]
    t.loc[hit, "check"] = "disagrees with month table"
    return t


@lru_cache(maxsize=1)
def traffic_month() -> pd.DataFrame:
    return read_traffic("traffic_month_chennai", 12, month_slot, MONTHS)


SLOT_RX = [(lab, rf"^{lab[:2]}\s*:?\s*00\s*hrs?\.?\s*to\s*{lab[3:]}") for lab in SLOTS] + [("Total", r"total")]
MONTH_RX = [(m, rf"^{m}") for m in MONTHS] + [("Total", r"total")]


def road_deaths_time() -> pd.DataFrame:
    return read_persons("traffic_time_deaths_tn", SLOT_RX)


def road_deaths_month() -> pd.DataFrame:
    return read_persons("traffic_month_deaths_tn", MONTH_RX)


@lru_cache(maxsize=1)
def rates() -> pd.DataFrame:
    r, _ = suicide_rates()
    r = r[r.rate_check == "ok"]
    recs = []
    for x in r.itertuples():
        for cat, v in (("Rate", x.rate), ("Suicides", x.suicides), ("Population (lakh)", x.population_lakh)):
            if v == v and v is not None:
                recs.append((x.year, x.name_std, x.entity_type, "", cat, "Total", "all ages", v, "ok", "ncrb"))
    d = frame(recs)
    # OpenDataChennai's compilation of the ADSI State/UT/city rate tables: 1998-2003, which NCRB's site lacks
    if ODC_RATES.exists():
        from ncrb.entities import standardise

        o = pd.read_csv(ODC_RATES, dtype=str)
        num = lambda v: pd.to_numeric(str(v).replace(" ", "."), errors="coerce")
        have = set(zip(d.year, d.place))
        add = []
        for r in o.itertuples():
            y = int(r.Year)
            if y > 2003:
                continue      # NCRB's own tables from 2004 (the compilation matches them there)
            if r.Category == "City":
                hit = difflib.get_close_matches(clean_city(r[2]), known_cities(), n=1, cutoff=0.8)
                if not hit:
                    continue
                place, ptype = hit[0], "city"
            else:
                place, ptype = standardise(r[2])
                if ptype not in ("state", "ut"):
                    continue
            if (y, place) in have:
                continue
            n, pop, rate = num(r[3]), num(r[5]), num(r[6])
            if not (n == n and pop == pop and rate == rate and pop > 0 and abs(n / pop - rate) <= 0.15 + 0.02 * rate):
                continue
            add += [(y, place, ptype, "", "Rate", "Total", "all ages", rate, "ok", "odc"),
                    (y, place, ptype, "", "Suicides", "Total", "all ages", n, "ok", "odc"),
                    (y, place, ptype, "", "Population (lakh)", "Total", "all ages", pop, "ok", "odc")]
        a = frame(add)
        # a row whose rate is far from the place's own 2004-2010 level was mis-copied (e.g. Chennai 1998: 1.8)
        ref = d[(d.cat == "Rate") & d.year.between(2004, 2010)].groupby("place").value.median()
        rr = a[a.cat == "Rate"].set_index(["year", "place"]).value
        bad = {k for k, v in rr.items() if k[1] in ref and not (ref[k[1]] / 3 <= v <= ref[k[1]] * 3)}
        a = a[[(y, p) not in bad for y, p in zip(a.year, a.place)]]
        d = pd.concat([d, a], ignore_index=True)
    # data.gov.in counts fill the suicide totals for 2001-2003 (no population or rate is published with them)
    o = ogd()
    if not o.empty:
        tot = o[o.Type_code == "Causes"].groupby(["Year", "place", "ptype"], as_index=False).Total.sum()
        have = set(zip(d.year, d.place))
        add = [(y, p, t, "", "Suicides", "Total", "all ages", v, "ok", "ogd") for y, p, t, v in zip(tot.Year, tot.place, tot.ptype, tot.Total) if (y, p) not in have]
        d = pd.concat([d, frame(add)], ignore_index=True)
    return d


def place_totals() -> dict:
    r = rates()
    s = r[r.cat == "Suicides"]
    return {(y, p): v for y, p, v in zip(s.year, s.place, s.value)}


def suicide_dataset(topics: list[str], age_topics: list[str], table: list, ogd_code: str | None) -> pd.DataFrame:
    d = tidy_categories(read_categories(topics, table), place_totals())
    if age_topics:
        a = tidy_categories(read_categories(age_topics, table), place_totals())
        a = a[a.age != "all ages"]
        d = pd.concat([d, a], ignore_index=True)
    if ogd_code:
        d = merge_sources(d, ogd_dataset(ogd_code, table))
    return add_both_sexes(d)


def suicide_means() -> pd.DataFrame:
    return suicide_dataset(["suicide_means_tn", "suicide_means_city"], ["suicide_means_age_tn"], MEANS, "Means_adopted")


def suicide_profession() -> pd.DataFrame:
    return suicide_dataset(["suicide_profession_tn", "suicide_profession_city"], ["suicide_profession_age_tn"], PROFESSION, "Professional_Profile")


def suicide_causes() -> pd.DataFrame:
    return suicide_dataset(["suicide_causes_tn", "suicide_causes_city"], [], CAUSES, "Causes")


def suicide_education() -> pd.DataFrame:
    return suicide_dataset(["suicide_education_tn", "suicide_education_city"], [], EDUCATION, "Education_Status")


def suicide_sex_age() -> pd.DataFrame:
    """Suicides by age group and sex: NCRB's sex x age tables, data.gov.in for 2001-2012, the age tables' totals from 2021."""
    raw = read_categories(["suicide_sex_age_tn", "suicide_sex_age_chennai"], None)
    recs = []
    for r in raw.itertuples():
        if r.category in SEXES:                      # 2014-15 sheets: one per sex, age in the heading
            sex, age = r.category, r.age or "Total"
        elif re.match(r"grand", r.category, re.I):
            sex, age = "Total", "Total"
        else:
            sex, age = r.sex, r.category
        if not sex:
            continue
        band = age_band(age)
        recs.append((r.year, r.place, r.ptype, "", band, sex, "all ages", r.value, r.check, "ncrb" if r.source == "text" else "ncrb"))
    d = frame(recs)
    d = d[d.cat.isin(["0-14", "0-17", "14-17", "15-29", "18-29", "30-44", "45-59", "60+", "all ages"])]
    d = d[d.check.isin(OK) | (d.check == "no total")]
    d = d.drop_duplicates(["year", "place", "ptype", "cat", "sex"])
    # a year must have its age groups: a garbled heading row is not an age table
    d = d[d.groupby(["year", "place", "ptype"]).cat.transform("nunique") >= 4]
    # 2021 onwards: the total row of the means x sex x age table
    a = tidy_categories(read_categories(["suicide_means_age_tn"], MEANS))
    if not a.empty:
        t = read_categories(["suicide_means_age_tn"], None)
        t = t[t.category.str.match(r"^\W*(grand\s+)?total\W*$", case=False) & t.sex.isin(SEXES)]
        t = t.assign(cat=t.age.map(lambda x: "all ages" if x in ("", "Total") else age_band(x)), age="all ages", group="", check="ok", source="ncrb")
        t = t[["year", "place", "ptype", "group", "cat", "sex", "age", "value", "check", "source"]]
        have = set(zip(d.year, d.place))
        d = pd.concat([d, t[[(y, p) not in have for y, p in zip(t.year, t.place)]]], ignore_index=True)
    # data.gov.in 2001-2012: every suicide is in the Causes table, so its sex x age sums are the totals
    o = ogd()
    if not o.empty:
        x = o[(o.Type_code == "Causes") & (o.age != "all ages")]
        g = x.groupby(["Year", "place", "ptype", "Gender", "age"], as_index=False).Total.sum()
        g = g.rename(columns={"Year": "year", "Gender": "sex", "age": "cat", "Total": "value"})
        alla = g.groupby(["year", "place", "ptype", "sex"], as_index=False).value.sum().assign(cat="all ages")
        g = pd.concat([g, alla], ignore_index=True).assign(group="", age="all ages", check="ok", source="ogd")
        have = set(zip(d.year, d.place, d.ptype))
        d = pd.concat([d, g[[(y, p, t) not in have for y, p, t in zip(g.year, g.place, g.ptype)]][COLS]], ignore_index=True)
    # 2019, the big cities: the city table by sex and age that OpenDataChennai copied from ADSI 2019
    if ODC_CITY_AGE.exists():
        raw = pd.read_csv(ODC_CITY_AGE, header=[0, 1])
        add = []
        for _, row in raw.iterrows():
            name = str(row.iloc[0])
            hit = difflib.get_close_matches(clean_city(name), known_cities(), n=1, cutoff=0.8)
            if not hit:
                continue
            for (sex, age), v in row.iloc[2:].items():
                sex = re.sub(r"\..*$", "", str(sex)).strip()
                if sex in SEXES and str(v).strip() not in ("", "nan"):
                    add.append((2019, hit[0], "city", "", age_band(str(age)), sex, "all ages", float(v), "ok", "odc"))
        a = frame(add)
        if not a.empty:
            alla = a.groupby(["year", "place", "ptype", "sex"], as_index=False).value.sum().assign(group="", cat="all ages", age="all ages", check="ok", source="odc")
            a = pd.concat([a, alla[COLS]], ignore_index=True)
            have = set(zip(d.year, d.place, d.ptype))
            d = pd.concat([d, a[[(y, p, t) not in have for y, p, t in zip(a.year, a.place, a.ptype)]]], ignore_index=True)
    d = d.drop_duplicates(["year", "place", "ptype", "cat", "sex"])
    keys = ["year", "place", "ptype", "group", "cat", "age"]
    have = d[d.sex == "Total"][keys].drop_duplicates()
    s = d[d.sex.isin(SEXES)].groupby(keys, as_index=False).agg(value=("value", "sum"), source=("source", "first"))
    s = s.merge(have, on=keys, how="left", indicator=True)
    s = s[s["_merge"] == "left_only"].drop(columns="_merge").assign(sex="Total", check="derived")
    return pd.concat([d, s[COLS]], ignore_index=True)


DATASETS = {
    "traffic_time": dict(build=traffic_time, topics=["traffic_time_chennai"], title="Traffic crashes by time of day", unit="crashes", cats=SLOTS,
                         groups=["Road", "Railway crossing", "Railway", "Total traffic"]),
    "traffic_month": dict(build=traffic_month, topics=["traffic_month_chennai"], title="Traffic crashes by month", unit="crashes", cats=MONTHS,
                          groups=["Road", "Railway crossing", "Railway", "Total traffic"]),
    "road_deaths_time": dict(build=road_deaths_time, topics=["traffic_time_deaths_tn"], title="Persons killed in traffic crashes by time of day", unit="deaths", cats=SLOTS,
                             groups=["Road", "Railway crossing", "Railway", "Total traffic"]),
    "road_deaths_month": dict(build=road_deaths_month, topics=["traffic_month_deaths_tn"], title="Persons killed in traffic crashes by month", unit="deaths", cats=MONTHS,
                              groups=["Road", "Railway crossing", "Railway", "Total traffic"]),
    "suicide_means": dict(build=suicide_means, topics=["suicide_means_tn", "suicide_means_city", "suicide_means_age_tn"], title="Suicides by means adopted", unit="suicides"),
    "suicide_profession": dict(build=suicide_profession, topics=["suicide_profession_tn", "suicide_profession_city", "suicide_profession_age_tn"], title="Suicides by profession", unit="suicides"),
    "suicide_causes": dict(build=suicide_causes, topics=["suicide_causes_tn", "suicide_causes_city"], title="Suicides by cause", unit="suicides"),
    "suicide_education": dict(build=suicide_education, topics=["suicide_education_tn", "suicide_education_city"], title="Suicides by educational status", unit="suicides"),
    "suicide_sex_age": dict(build=suicide_sex_age, topics=["suicide_sex_age_tn", "suicide_sex_age_chennai", "suicide_means_age_tn"], title="Suicides by age group and sex", unit="suicides",
                            cats=["0-14", "0-17", "14-17", "15-29", "18-29", "30-44", "45-59", "60+"]),
    "suicide_rate": dict(build=rates, topics=["suicide_rate"], title="Suicides, population and rate", unit="per lakh people", cats=["Rate", "Suicides", "Population (lakh)"]),
}
