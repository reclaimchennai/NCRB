"""Turn the per-year tables of each topic into one tidy time series.

For every topic the right table is taken for each year (see topics.py), the
row for the place is read, and its columns are mapped to fixed categories
(time slot, month, means, profession, age group, sex) by their printed
headings, falling back to their position where the scan garbled a heading.
Each year is checked against its own printed total where one exists, and the
check result travels with the data (``check`` column), so a chart can leave
out or mark the years that do not add up.

Scanned years (before about 2000) are read twice when the AI OCR has seen the
page: the Tesseract reading and the GLM-OCR reading. The one whose figures add
up to the printed total wins.
"""

from __future__ import annotations

import re

import pandas as pd

from .lib import PLACES, SCANNED, q, rows_for
from .topics import tables_for

SLOTS = ["00-03", "03-06", "06-09", "09-12", "12-15", "15-18", "18-21", "21-24"]
SLOT_START = {"0000": 0, "0300": 1, "0600": 2, "0900": 3, "1200": 4, "1500": 5, "1800": 6, "2100": 7}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTH_RX = {m: re.compile(rf"\b{m[:3]}", re.I) for m in MONTHS}


# --------------------------------------------------------------------------- AI OCR alternative


def vlm_cells(table_id: str, place: str) -> pd.DataFrame:
    """Cells of a scanned table as read by the AI OCR (from the page cache), for one place."""
    try:
        import pymupdf

        from ncrb.assemble import assemble
        from ncrb.crawl import ROOT
        from ncrb.pdftable import TOTAL_RE, col_label, parse_number
        from ncrb.vlm import DEFAULT_MODEL
        from ncrb.vlm_tables import cache_path, file_sha, page_segments
    except ImportError:
        return pd.DataFrame()
    t = q("SELECT source_file, pages, year FROM tables WHERE table_id = ?", [table_id])
    if t.empty:
        return pd.DataFrame()
    path = ROOT / t.source_file[0]
    a, b = (int(x) for x in str(t.pages[0]).split("-")) if "-" in str(t.pages[0]) else (1, 1)
    sha = file_sha(path)
    segs = []
    for p in range(a, b + 1):
        cp = cache_path(DEFAULT_MODEL, sha, p)
        if cp.exists():
            segs += page_segments(cp.read_text(encoding="utf-8"), p)
    if not segs:
        return pd.DataFrame()
    rx = re.compile(PLACES.get(place, place), re.I)
    out = []
    for tab in assemble(segs):
        for r in tab.rows:
            if not rx.search(r.label):
                continue
            for cid, raw in r.cells.items():
                hdr = tab.columns.get(cid, [])
                out.append({
                    "table_id": table_id, "year": int(t.year[0]), "row": 0, "section": r.section, "name": r.label,
                    "col_no": col_label(cid), "column": " | ".join(hdr), **{f"h{i + 1}": (hdr[i] if i < len(hdr) else "") for i in range(5)},
                    "value": parse_number(raw), "raw": raw, "source": "ai_ocr",
                })
            break  # first matching row only
    return pd.DataFrame(out)


def candidates(topic: str) -> tuple[pd.DataFrame, dict[int, list[pd.DataFrame]]]:
    """Picked tables, and for each year the readings of the place's row (Tesseract/text first, AI OCR second)."""
    picked = tables_for(topic)
    from .topics import TOPICS

    place = TOPICS[topic]["place"]
    cells = rows_for(picked.table_id.tolist(), place)
    cells["source"] = "text"
    # a workbook split into one sheet per sex (2014-15): read the sibling sheets as one table
    for t in picked.itertuples():
        m = re.match(r"(.+_t)\d+$", t.table_id)
        if t.method != "excel" or not m:
            continue
        alt = q("SELECT table_id FROM tables WHERE table_id LIKE ? AND table_id <> ?", [m.group(1) + "%", t.table_id])
        more = rows_for(alt.table_id.tolist(), place)
        if more.empty:
            continue
        more = more[more["row"] == more.groupby("table_id")["row"].transform("min")]
        own_rows = cells.loc[cells.table_id == t.table_id, "row"]
        more = more.assign(table_id=t.table_id, row=int(own_rows.min()) if len(own_rows) else 0)
        cells = pd.concat([cells, more], ignore_index=True)
    out: dict[int, list[pd.DataFrame]] = {}
    for t in picked.itertuples():
        own = cells[cells.table_id == t.table_id]
        # one row per table: tables printing the place twice (a facing page) keep the first
        if not own.empty:
            own = own[own["row"] == own["row"].min()]
            if t.method in SCANNED:
                own = own.assign(source="ocr")
        readings = [own] if not own.empty else []
        if t.method in SCANNED:
            v = vlm_cells(t.table_id, place)
            if not v.empty:
                readings.append(v)
        out[int(t.year)] = readings
    return picked, out


# --------------------------------------------------------------------------- grouped columns


def groups(cells: pd.DataFrame, group_rx: str | None = None) -> list[tuple[str, pd.DataFrame]]:
    """Split a row's columns into consecutive groups by their outermost heading."""
    out: list[tuple[str, list]] = []
    cur = None
    for _, c in cells.iterrows():
        g = c["h1"] if (c["h2"] or "") else ""
        if group_rx and not re.search(group_rx, g or "", re.I):
            g = cur if cur is not None else g
        if cur is None or g != cur:
            out.append((g, []))
            cur = g
        out[-1][1].append(c)
    return [(g, pd.DataFrame(rows)) for g, rows in out]


def slots_of(cells: pd.DataFrame, n: int, label_rx) -> list[tuple[int | None, float]]:
    """(category index or None for 'total', value) per column, by heading or position."""
    vals = list(cells["value"])
    heads = [str(x) for x in cells["column"]]
    out = []
    for i, (h, v) in enumerate(zip(heads, vals)):
        k = label_rx(h)
        if k is None:
            k = i if i < n else None  # position: n categories then the total
        out.append((k, v))
    return out


def time_slot(h: str) -> int | None:
    leaf = h.split("|")[-1]
    # only a full 'start ... to end' pair identifies the slot; a lone time is often the end of the previous one
    m = re.search(r"\b(0000|0300|0600|0900|1200|1500|1800|2100)\s*(?:hrs?\.?|hours)?\s*(?:to|-)\s*(0300|0600|0900|1200|1500|1800|2100|2400)\b", leaf, re.I)
    if m and (SLOT_START[m.group(1)] + 1) % 8 == SLOT_START.get(m.group(2), 0) % 8:
        return SLOT_START[m.group(1)]
    if re.search(r"total", leaf, re.I):
        return None
    return -1  # unreadable heading: fall back to position


def month_slot(h: str) -> int | None:
    leaf = h.split("|")[-1]
    if re.search(r"total", leaf, re.I):
        return None
    for i, m in enumerate(MONTHS):
        if MONTH_RX[m].search(leaf):
            return i
    return -1


def read_blocks(cells: pd.DataFrame, n: int, slot_fn, group_names: list[str], positional: bool = False) -> pd.DataFrame:
    """A row laid out as blocks of n categories + a total (traffic tables), as long rows with a check."""
    vals = list(cells["value"])
    heads = [str(x) for x in cells["column"]]
    size = n + 1
    rows = []
    nblocks = len(vals) // size
    for b in range(max(1, nblocks)):
        block_vals = vals[b * size:(b + 1) * size]
        block_heads = heads[b * size:(b + 1) * size]
        if len(block_vals) < n:
            continue
        cats: dict[int, float] = {}
        total = None
        for i, (h, v) in enumerate(zip(block_heads, block_vals)):
            # text-layer tables keep NCRB's fixed column order; position is exact there and headings are not
            k = (i if i < n else None) if positional else slot_fn(h)
            if k == -1 or k is None and i < n:
                k = i if i < n else None
            if k is None:
                total = v
            elif k not in cats:
                cats[k] = v
        name = group_names[b] if b < len(group_names) else f"group {b + 1}"
        s = sum(v for v in cats.values() if v == v and v is not None)
        ok = total is not None and total == total and len(cats) == n and abs(s - total) <= max(1, 0.005 * total)
        for k, v in sorted(cats.items()):
            rows.append({"group": name, "k": k, "value": v, "printed_total": total, "check": "ok" if ok else ("no total" if total is None else "mismatch")})
    return pd.DataFrame(rows)


def best_reading(readings: list[pd.DataFrame], reader) -> tuple[pd.DataFrame, str]:
    """Parse each reading; keep the one whose blocks add up (text first, then AI OCR, then Tesseract)."""
    best, best_src, best_score = pd.DataFrame(), "", -1
    for r in readings:
        if r.empty:
            continue
        out = reader(r)
        if out.empty:
            continue
        score = (out["check"] == "ok").mean() + (0.01 if r["source"].iloc[0] in ("text", "ai_ocr") else 0)
        if score > best_score:
            best, best_src, best_score = out, r["source"].iloc[0], score
    return best, best_src


# --------------------------------------------------------------------------- traffic


def _traffic_groups(cells: pd.DataFrame, size: int) -> list[str]:
    names = []
    for b in range(len(cells) // size or 1):
        h = " ".join(str(x) for x in cells["column"].iloc[b * size:(b + 1) * size])
        if re.search(r"rail\s*-?\s*road|crossing", h, re.I):
            names.append("Railway crossing")
        elif re.search(r"other rail|railway acc", h, re.I):
            names.append("Railway")
        elif re.search(r"total traffic", h, re.I) and b > 0:
            names.append("Total traffic")
        elif re.search(r"road acc", h, re.I):
            names.append("Road")
        else:
            names.append(["Road", "Railway crossing", "Railway", "Total traffic"][b] if b < 4 else f"group {b + 1}")
    return names


def traffic(topic: str, n: int, slot_fn, labels: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    picked, by_year = candidates(topic)
    out = []
    for year, readings in sorted(by_year.items()):
        def reader(r):
            r = r.reset_index(drop=True)
            return read_blocks(r, n, slot_fn, _traffic_groups(r, n + 1), positional=r["source"].iloc[0] == "text")

        df, src = best_reading(readings, reader)
        if df.empty:
            continue
        df["year"] = year
        df["source"] = src
        df["category"] = df["k"].map(lambda k: labels[k])
        out.append(df.drop(columns="k"))
    data = pd.concat(out, ignore_index=True) if out else pd.DataFrame()
    return data, picked


def traffic_persons(topic: str, labels_rx: list[tuple[str, str]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """State tables of persons injured and died (2021 onwards): heading = slot | accident type | Injured/Died."""
    picked, by_year = candidates(topic)
    out = []
    for year, readings in sorted(by_year.items()):
        if not readings:
            continue
        for _, c in readings[0].iterrows():
            parts = [x.strip() for x in str(c["column"]).split("|")]
            if len(parts) < 3:
                continue
            slot = next((name for name, rx in labels_rx if re.search(rx, parts[0], re.I)), None)
            kind = "Road" if re.search(r"^road", parts[1], re.I) else "Railway crossing" if re.search(r"crossing", parts[1], re.I) else \
                "Railway" if re.search(r"rail", parts[1], re.I) else "Total traffic" if re.search(r"total", parts[1], re.I) else parts[1]
            what = "Died" if re.search(r"died|killed", parts[2], re.I) else "Injured" if re.search(r"injur", parts[2], re.I) else parts[2]
            out.append({"year": year, "category": slot or parts[0], "group": kind, "measure": what, "value": c["value"]})
    d = pd.DataFrame(out)
    # check: the slots of each year, type and measure add up to the printed total
    d["check"] = ""
    for (y, g, m), x in d.groupby(["year", "group", "measure"]):
        tot = x[x.category == "Total"].value
        parts = x[x.category != "Total"].value.sum()
        d.loc[x.index, "check"] = "ok" if len(tot) and abs(parts - tot.iloc[0]) <= 1 else ("no total" if not len(tot) else "mismatch")
    return d, picked


# --------------------------------------------------------------------------- category tables (means, profession, age)


SEX_RX = [("Male", r"\bmale\b|^m$"), ("Female", r"female|^f$"), ("Transgender", r"trans"), ("Total", r"total|^t$")]


def sex_of(leaf: str) -> str | None:
    leaf = leaf.strip().lower()
    for name, rx in SEX_RX:
        if re.search(rx, leaf):
            if name == "Male" and "female" in leaf:
                continue
            return name
    return None


def _split_groups(gs: list[tuple[str, pd.DataFrame]]) -> list[tuple[str, pd.DataFrame]]:
    """Repair groups where a spanning heading was printed only over its last column.

    In some editions 'Others' heads only its Total column, so its Male and
    Female columns land under the previous category (which then shows Male,
    Female, Total, share, Male, Female). Columns after a category's own total
    are carried over to the next, unnamed group, which is named from its text.
    """
    out, carry = [], []
    for name, g in gs:
        g = g.reset_index(drop=True)
        if not name:  # named from its own headings, before any carried columns join it
            text = " ".join(str(x) for x in g["column"] if not re.search(r"share|%", str(x), re.I))
            name = re.sub(r"\b(total|male|female|transgender)\b|\(\d+\)|\|", " ", text, flags=re.I)
            name = re.sub(r"\s+", " ", name).strip()
        if carry:
            g = pd.concat([pd.DataFrame(carry), g], ignore_index=True)
            carry = []
        if not name or len(g) == 0:
            continue
        keep, seen_total = [], False
        for _, c in g.iterrows():
            s = sex_of(str(c["h2"] or c["column"]).split("|")[-1])
            if seen_total and s == "Male":
                carry = [r for _, r in g.iloc[len(keep):].iterrows()]
                break
            if s == "Total":
                seen_total = True
            keep.append(c)
        out.append((name, pd.DataFrame(keep)))
    return out


def categories(cells: pd.DataFrame) -> pd.DataFrame:
    """Columns grouped as category -> sex (and age when present), with a check that male + female (+TG) = total."""
    rows = []
    has_tg = cells["column"].str.contains("transgender", case=False, na=False).any()
    template = ["Male", "Female", "Transgender", "Total"] if has_tg else ["Male", "Female", "Total", "share"]
    for name, g in _split_groups(groups(cells.reset_index(drop=True))):
        for i, (_, c) in enumerate(g.iterrows()):
            levels = [c[f"h{k}"] for k in range(2, 6) if c[f"h{k}"]]
            # workbooks with one sheet per sex head each sheet with the sex itself
            sex = sex_of(name) if re.fullmatch(r"\s*(male|female|transgender)\s*", name, re.I) else None
            age = ""
            for lv in levels:
                s = sex_of(lv)
                if s and not (sex and s == "Total"):
                    sex = s
                elif s == "Total":
                    age = "Total"  # 'Male | Total': all ages of one sex
                elif re.search(r"\d|year|age|above|below|upto", lv, re.I):
                    age = lv
            if sex is None and not age and i < len(template):
                sex = template[i]
            if re.search(r"share|%", " ".join(levels), re.I) or sex == "share":
                continue
            rows.append({"category": name, "sex": sex or "", "age": age, "value": c["value"], "raw": c["raw"]})
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    def verdict(parts, tot):
        if not len(tot):
            return "no total"
        return "ok" if abs(parts - tot.iloc[0]) <= max(1, 0.005 * (tot.iloc[0] or 0)) else "mismatch"

    if (df.age != "").any():
        # age-wise tables: the age groups of each category and sex add up to that sex's total
        check = []
        for (cat, sex), g in df.groupby(["category", "sex"], sort=False):
            check += [(cat, sex, verdict(g[g.age != "Total"].value.fillna(0).sum(), g[g.age == "Total"].value))]
        ck = pd.DataFrame(check, columns=["category", "sex", "check"])
        return df.merge(ck, on=["category", "sex"], how="left")
    check = []
    for (cat, age), g in df.groupby(["category", "age"], sort=False):
        check += [(cat, age, verdict(g[g.sex.isin(["Male", "Female", "Transgender"])].value.fillna(0).sum(), g[g.sex == "Total"].value))]
    ck = pd.DataFrame(check, columns=["category", "age", "check"])
    return df.merge(ck, on=["category", "age"], how="left")


def category_series(topic: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    picked, by_year = candidates(topic)
    out = []
    for year, readings in sorted(by_year.items()):
        df, src = best_reading(readings, categories)
        if df.empty:
            continue
        df["year"] = year
        df["source"] = src
        out.append(df)
    return (pd.concat(out, ignore_index=True) if out else pd.DataFrame()), picked


# --------------------------------------------------------------------------- rates (all States, UTs, cities)


CITY_NAMES = {"Madras": "Chennai", "Bombay": "Mumbai", "Greater Mumbai": "Mumbai", "Calcutta": "Kolkata", "Bangalore": "Bengaluru",
              "Poona": "Pune", "Baroda": "Vadodara", "Trivandrum": "Thiruvananthapuram", "Cochin": "Kochi", "Delhi City": "Delhi",
              "Benares": "Varanasi", "Calicut": "Kozhikode", "Cawnpore": "Kanpur", "Kanpur Nagar": "Kanpur",
              "Delhi": "Delhi", "Chandigarh": "Chandigarh"}  # also UTs: in the cities block they are the city


def _rate_columns(cols: list[tuple[str, str]]) -> dict[str, str]:
    """col_no for suicides, share, population and rate, read from the lowest heading level."""
    found: dict[str, str] = {}
    for no, col in cols:
        leaf = str(col).split("|")[-1].lower()
        if re.search(r"rank", leaf):
            continue
        if re.search(r"rate|volume|per (one )?lakh|col\.?\s*3\s*/", leaf):
            key = "rate"
        elif re.search(r"population|lakh|mid.?year|\(000\)", leaf):
            key = "population"
        elif re.search(r"share|percent|%", leaf):
            key = "share_pct"
        elif re.search(r"number|incidence|suicid", leaf):
            key = "suicides"
        else:
            continue
        found.setdefault(key, no)
    return found


def suicide_rates() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Number, population and rate of suicides for every State, UT and city, every year available.

    Columns are found by heading; when the figures of a row do not agree
    (rate = suicides / population in lakh) NCRB's fixed order is tried
    (number, % share, population, rate). Implausible rates are blanked.
    """
    from ncrb.entities import standardise

    from .lib import col_order

    picked = tables_for("suicide_rate")
    marks = ",".join("?" for _ in picked.table_id)
    cells = q(
        f'SELECT table_id, year, "row", section, name, col_no, "column", value FROM cells WHERE table_id IN ({marks})',
        picked.table_id.tolist(),
    )
    out = []
    for tid, tab in cells.groupby("table_id"):
        cols = tab.drop_duplicates("col_no")[["col_no", "column"]]
        cols = sorted(cols.itertuples(index=False), key=lambda c: col_order(c[0]))
        by_head = _rate_columns(cols)
        thousands = any(re.search(r"\(000\)|thousand", str(c[1]), re.I) for c in cols)
        numeric = [c[0] for c in cols if col_order(c[0]) < 1000]
        by_pos = dict(zip(["suicides", "share_pct", "population", "rate"], numeric[:4])) if len(numeric) >= 4 else {}
        for row, g in tab.groupby("row"):
            v = dict(zip(g.col_no, g.value))

            def read(m):
                r = {k: v.get(c) for k, c in m.items()}
                if thousands and r.get("population") is not None:
                    r["population"] = r["population"] / 100
                return r

            def agrees(r):
                n, p, rt = r.get("suicides"), r.get("population"), r.get("rate")
                return all(x is not None and x == x for x in (n, p, rt)) and p > 0 and abs(n / p - rt) <= 0.15 + 0.02 * rt

            r = read(by_head)
            if not agrees(r) and by_pos and agrees(read(by_pos)):
                r = read(by_pos)
            rec = {"table_id": tid, "year": int(g.year.iloc[0]), "name": g.name.iloc[0], "section": g.section.iloc[0],
                   "suicides": r.get("suicides"), "share_pct": r.get("share_pct"), "population_lakh": r.get("population"), "rate": r.get("rate"),
                   "rate_check": "ok" if agrees(r) else "no population" if r.get("population") is None else "mismatch"}
            out.append(rec)
    df = pd.DataFrame(out)
    df["name"] = df["name"].str.replace(r"^[\W\d]+[.,]?\s*", "", regex=True)  # serial numbers left on scanned rows
    std = df["name"].map(lambda n: standardise(n))
    df["name_std"] = std.map(lambda x: x[0])
    df["entity_type"] = std.map(lambda x: x[1])
    in_city_section = df["section"].fillna("").str.contains("cit", case=False) | df["name"].str.contains(r"\bcity\b", case=False)
    clean = df["name"].str.replace(r"\s*\(.*?\)\s*|\bcity\b|[*#@!]", " ", regex=True).str.strip().str.title().str.replace(r"\s+", " ", regex=True)
    # 'Madras' is both the old name of Tamil Nadu and of Chennai: in the cities block it is the city
    city = in_city_section & (~df["entity_type"].isin(["state", "ut", "total"]) | clean.isin(CITY_NAMES.keys()))
    df.loc[city, "entity_type"] = "city"
    df.loc[city, "name_std"] = clean[city].replace(CITY_NAMES)
    # scanned years: snap OCR'd city names to the cities printed in the text years, drop what does not match
    import difflib

    known = sorted(set(df.loc[city & (df.year >= 2004), "name_std"]) | set(CITY_NAMES))
    def snap(n):
        m = difflib.get_close_matches(n, known, n=1, cutoff=0.8)
        return CITY_NAMES.get(m[0], m[0]) if m else None
    old = city & (df.year < 2004)
    df.loc[old, "name_std"] = df.loc[old, "name_std"].map(snap)
    df = df[~(old & df["name_std"].isna())]
    tot = df.entity_type == "total"
    low = df["name_std"].str.lower()
    df.loc[tot, "name_std"] = "All India"
    df.loc[tot & low.str.contains(r"\bstates?\b"), "name_std"] = "Total (States)"
    df.loc[tot & low.str.contains(r"\buts?\b|union"), "name_std"] = "Total (UTs)"
    df.loc[tot & low.str.contains(r"cit|crs"), "name_std"] = "Total (Cities)"
    # a rate outside 0-100 per lakh is a misread figure
    bad = ~df["rate"].between(0, 100)
    df.loc[bad & df["rate"].notna(), "rate_check"] = "implausible rate (blanked)"
    df.loc[bad, "rate"] = None
    df = df[df.entity_type.isin(["state", "ut", "city", "total"])]
    df = df.sort_values(["year", "entity_type", "name_std", "rate_check"]).drop_duplicates(["year", "entity_type", "name_std"])
    return df.reset_index(drop=True), picked
