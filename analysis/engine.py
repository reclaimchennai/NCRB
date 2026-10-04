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

import collections
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
    # dot leaders of scanned tables: 'Madras . . . . 663' or 'Bangalore .'
    raw = re.sub(r"(\s*\.){1,}(\s.*)?$", "", raw) if re.search(r"\s\.(\s|$)", raw) else raw
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


# the AI OCR readings in the page cache, best first (analysis reads the strongest one a file has)
VLM_MODELS = ["OvisOCR2-2048", "OvisOCR2", "PaddleOCR-VL-1.6-2048", "mlx-community/GLM-OCR-bf16"]


def _vlm_model(sha: str) -> str | None:
    from ncrb.vlm_tables import CACHE, model_slug

    return next((m for m in VLM_MODELS if (CACHE / model_slug(m) / sha[:16]).is_dir()), None)


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
    model = _vlm_model(sha) or DEFAULT_MODEL
    segs = []
    for p in range(a, b + 1):
        cp = cache_path(model, sha, p)
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


def _file_vlm_tables(table_id: str) -> list[dict]:
    """Every table the AI OCR model read anywhere in the file of ``table_id``, each as {place key: cells}."""
    try:
        from ncrb.assemble import assemble
        from ncrb.crawl import ROOT as RAW
        from ncrb.pdftable import col_label, parse_number
        from ncrb.vlm import DEFAULT_MODEL
        from ncrb.vlm_tables import cache_path, file_sha, page_segments
    except ImportError:
        return []
    t = q("SELECT source_file FROM tables WHERE table_id = ?", [table_id])
    if t.empty:
        return []
    sha = file_sha(RAW / t.source_file[0])
    model = _vlm_model(sha) or DEFAULT_MODEL
    segs = []
    for pno in range(1, 60):
        cp = cache_path(model, sha, pno)
        if not cp.exists():
            if pno > 1:
                break
            continue
        segs += page_segments(cp.read_text(encoding="utf-8"), pno)
    out = []
    for tab in assemble(segs) if segs else []:
        m = {}
        for r in tab.rows:
            key = resolve(r.label, r.section or "", True)
            if not key or key in m:
                continue
            cells = []
            for cid, raw in r.cells.items():
                hdr = tab.columns.get(cid, [])
                cells.append({"col_no": col_label(cid), "column": " | ".join(hdr), **{f"h{i + 1}": (hdr[i] if i < len(hdr) else "") for i in range(5)},
                              "value": parse_number(raw), "raw": raw, "source": "ai_ocr"})
            if cells:
                m[key] = pd.DataFrame(cells)
        if m:
            out.append(m)
    return out


def _join_column_halves(t, places: dict) -> None:
    """A wide scanned table printed in two column halves on successive pages (1970s-80s appendices: Railways ...
    Drowning on the first pages, Hanging ... Grand Total on the next) is read as two tables, or only its first half is
    extracted at all. Each place's cells from the other half are added when the other table comes from the same file,
    lists the same places, and either continues the first half's column numbers or carries different headings (each
    half often numbers its columns from 3)."""
    from .lib import col_order

    if not places:
        return
    def heads(g):
        return {re.sub(r"[^a-z]+", "", str(c).lower()) for c in g["column"] if re.search(r"[a-z]{3}", str(c), re.I)}
    def nums(g):
        return {col_order(c) for c in g.col_no if col_order(c) < 1000}
    halves = []
    for tid in q("SELECT table_id FROM tables WHERE source_file = (SELECT source_file FROM tables WHERE table_id = ?) AND table_id <> ?",
                 [t.table_id, t.table_id]).table_id:
        cells = q('SELECT table_id, "row", section, name, col_no, "column", h1, h2, h3, h4, h5, value, raw FROM cells WHERE table_id = ?', [tid])
        m = {}
        for _, g in cells.groupby("row", sort=False):
            key = resolve(g.name.iloc[0], g.section.iloc[0], True)
            if key and key not in m:
                m[key] = g.assign(source="ocr")
        if m:
            halves.append(m)
    halves += _file_vlm_tables(t.table_id)
    for half in halves:
        shared = [k for k in places if k in half]
        if len(shared) < 5:                       # not the same list of places
            continue
        joined = False
        for k in shared:
            second = half[k]
            for i, first in enumerate(places[k]):
                if second["source"].iloc[0] != first["source"].iloc[0]:
                    continue
                a, b = nums(first), nums(second)
                ha, hb = heads(first), heads(second)
                cont = a and b and min(b) > max(a)
                other = ha and hb and len(ha & hb) <= 0.2 * min(len(ha), len(hb)) and not (hb <= ha)
                if not (cont or other):
                    continue
                if not cont:                      # renumber the second half after the first
                    off = (max(a) if a else 0) + 100
                    second = second.assign(col_no=[str(col_order(c) + off) if col_order(c) < 1000 else c for c in second.col_no])
                places[k][i] = pd.concat([first, second.reindex(columns=first.columns)], ignore_index=True)
                joined = True
        if joined:
            return


# --------------------------------------------------------------------------- the 1967-1988 appendices, by position
#
# ADSI printed suicides by means and by causes for every State, UT and city as appendices too wide for one page: the
# columns run on over two to four page groups (Railways ... Fire on the first pages, Drowning ... Grand Total on the
# next), and some editions print a group's figures on a facing page without the place names. The extracted tables
# lose the later groups or carry the first group's headings over them. Here every page of the file is read again
# from each AI OCR reading in the cache: a place's figures are its rows in page order, the categories are the
# edition's column headings in page order (M and F under each, then Total M, Total F and Grand Total; to 1970 one
# figure per category and a Total), and a place-year is kept only if its figures add up exactly: the categories'
# males to Total M, females to Total F, the two to the Grand Total, and the Grand Total within 1% of the long
# series' count of suicides for the place and year (required where a table prints no sexes, and for All India).
# Readings that pass but disagree are dropped. Used only for place-years the normal reading leaves out.

POS_CHECK = "ok (positional, adds up)"
POS_LAYOUTS: dict[tuple[int, str], list[str]] = {}   # each edition's categories, where its own headings settle them
POS_YEARS = range(1967, 1989)
POS_APPENDIX = {"means": (6, 4), "causes": (5, 3)}   # the appendix number up to 1972, and from 1973
POS_CATS = {
    "means": [("By Railways", r"rail"), ("By Machine", r"machin"), ("By Fire-arms", r"fire\W*arm"), ("By Weapons", r"weapon"),
              ("By Poison", r"poison"), ("On Roads", r"\broads?\b"), ("By Fire", r"\bfire\b(?!\W*arm)"), ("By Drowning", r"drown"),
              ("By Hanging", r"\bhang"), ("By Jumping", r"jump"), ("By Electrocution", r"electr"), ("By Sleeping pills", r"sleep|pills"),
              ("By Other means", r"\bother")],
    "causes": [("Failure in examination", r"examin|failure"), ("Quarrel with parents-in-law", r"parent|in.?laws?\b"),
               ("Quarrel with spouse", r"spouse|married|partner"), ("Poverty", r"povert"), ("Frustration", r"frustrat"),
               ("Love affairs", r"\blove"), ("Insanity", r"insan"), ("Dispute over property", r"propert"), ("Dreadful disease", r"disease"),
               ("Unemployment", r"employ"), ("Bankruptcy or sudden change in economic position", r"bankrupt|economic"),
               ("Death of dear persons", r"death|dear\s*person"), ("Fall in social reputation", r"reputation"), ("Dowry dispute", r"dowry"),
               ("Illegitimate pregnancy", r"illegitim|pregnan"), ("Causes not known", r"not\s*known"), ("Other causes", r"\bother")],
}
_POS_MARK = [(r"^\W*states?\W*$", "state"), (r"^\W*(u\W*t\W*s?|union\s*territor\w*)\W*$", "ut"), (r"^\W*cit(y|ies)\W*$", "city")]


def _pos_token(cell: str):
    """A figure, 0 for a dash or '..' (nil), 'NA' for N.A., None for filler (dot leaders, empty), 'BAD' for text."""
    s = re.sub(r"\s+", "", str(cell or ""))
    if s in ("", ".", "·", ":", ";", "'", ",", "*", "|"):
        return None
    if re.fullmatch(r"[-–—~_]+|\.{2,}|…+|nil", s, re.I):
        return 0
    if re.fullmatch(r"n\.?a\.?", s, re.I):
        return "NA"
    if re.fullmatch(r"\.?\d[\d,.·]*", s):         # (a percentage row's 16·90 too: such rows are only counted, not read)
        return int(re.sub(r"\D", "", s))
    return "BAD"


def _pos_file(year: int, kind: str):
    """The edition's appendix file for ``kind``, or None."""
    from ncrb.crawl import ROOT as RAW

    n = POS_APPENDIX[kind][0 if year <= 1972 else 1]
    hits = [p for p in sorted((RAW / "raw" / "adsi" / str(year) / "table_content").glob("*.pdf"))
            if re.search(rf"appendix-{n}(\d|\.pdf$)", p.name)]
    return hits[0] if len(hits) == 1 else None


def _pos_reading(texts: dict[int, str], year: int, kind: str) -> dict:
    """One model's reading of a file: places {key: {page: [figures or None]}}, heads {page: categories in heading
    order}, totals (pages with a Total heading), ncols (the figure columns the printed column numbers count), titled
    (a page title names the kind)."""
    from ncrb.vlm import parse_output

    cats = POS_CATS[kind]
    places: dict[tuple[str, str], dict[int, list]] = {}
    heads: dict[int, list[str]] = {}
    totals: set[int] = set()
    firsts, maxes = [], []
    kw: set[str] = set()                         # the page titles name suicides and the kind somewhere in the file
    section = "state"
    prev: list[tuple] = []                       # the previous page's figure rows, for a facing page without names
    for pno in sorted(texts):
        lines, grids = parse_output(texts[pno])
        kw |= {w for w, rx in (("kind", "means" if kind == "means" else "cause"), ("suicid", "suicid")) if any(re.search(rx, ln, re.I) for ln in lines)}
        rows: list[tuple] = []                   # (key or None, figures or None) for every row with figures, in order
        named = 0
        for g in grids:
            data = False
            first_cat = None                     # the cell index of the first category heading in this grid
            for r in g.rows:
                li = next((i for i, c in enumerate(r) if re.search(r"[A-Za-z]{2,}", c) and _pos_token(c) == "BAD"), None)
                label = re.sub(r"[\s.:,]+$", "", r[li]).strip() if li is not None else ""
                toks = [t for t in (_pos_token(c) for c in (r[li + 1:] if li is not None else r)) if t is not None]
                nums = [t for t in toks if isinstance(t, int)]
                vals = None if "BAD" in toks else toks
                if label and not nums:
                    m = next((s for rx, s in _POS_MARK if re.match(rx, label, re.I)), None)
                    if m:
                        section = m
                    elif not data:               # heading text: the categories in printed order
                        if any(re.search(r"\btotal\b", c, re.I) for c in r) and \
                                any(re.search(rx, c, re.I) for c in r for _, rx in cats + [("", r"grand")]):
                            totals.add(pno)
                        heads.setdefault(pno, [])
                        for i, c in enumerate(r):
                            hits = sorted((mm.start(), name) for name, rx in cats for mm in [re.search(rx, c, re.I)] if mm)
                            if hits and first_cat is None:
                                first_cat = i
                            for _, name in hits:
                                if name not in heads[pno]:
                                    heads[pno].append(name)
                    continue
                if not label:
                    ints = [t for t in toks if isinstance(t, int)]
                    if len(ints) >= 3 and len(ints) == len(toks) and ints == sorted(set(ints)) and ints[-1] <= 60 and not data:
                        maxes.append(ints[-1])   # the column-number row
                        if first_cat is not None and isinstance(_pos_token(r[first_cat]), int):
                            firsts.append(_pos_token(r[first_cat]))
                        continue
                    if len(nums) >= 2:
                        rows.append((None, vals))
                        data = True
                    continue
                k0, kc = resolve(label, "", True, year), resolve(label, "Cities", True, year)
                if k0 == kc and k0:
                    key = k0
                    if k0[1] in ("state", "ut", "city"):
                        section = k0[1]
                elif kc and kc[1] == "city" and section == "city":
                    key = kc
                else:
                    key = k0
                if key == ("All India", "total") and not re.search(r"grand|india", label, re.I):
                    key = None                   # a States, UTs or (misread) Cities total
                data = True
                if key and key[1] != "total":
                    named += 1
                rows.append((key, vals))
        if not named:
            # a facing page without the place names: its figure rows are the page before's, in the same order
            rows = [(k, v) for (k, _), (_, v) in zip(prev, rows)] if len(rows) >= 3 and len(rows) == len(prev) else []
        for key, vals in rows:
            if key:
                places.setdefault(key, {}).setdefault(pno, []).append(vals)
        prev = rows if named else []
    first = collections.Counter(firsts).most_common(1)[0][0] if firsts else None
    return {"places": places, "heads": {p: h for p, h in heads.items() if h}, "totals": totals, "titled": kw == {"kind", "suicid"},
            "ncols": max(maxes) - first + 1 if first is not None and maxes and max(maxes) > first else None}


def _pos_layout(readings: list[dict], year: int, kind: str, log: list | None, reference: list[str] | None = None):
    """The edition's categories in printed order, and each page's (categories, has totals); a page without headings
    takes the page before's. A page's headings are the longest reading that the others fit inside (a heading a model
    missed); where readings contradict each other, the one that repeats another page's settled headings (the pages
    of one column group share them), else, when every reading fits inside the categories of a neighbouring edition
    (``reference``), the headings they found in that edition's order, else the one most readings agree on. A page
    none of these settles is left out, with the pages that follow it; a page whose headings fit inside another
    page's longer list takes that list (the figures on the page must still fit it)."""
    def within(a, b):
        it = iter(b)
        return all(x in it for x in a)

    def widest(lists):
        top = max(lists, key=len)
        return top if all(within(x, top) for x in lists) else None

    allp = sorted({p for r in readings for pl in r["places"].values() for p in pl} | {p for r in readings for p in r["heads"]})
    lists = {p: [tuple(r["heads"][p]) for r in readings if p in r["heads"]] for p in allp}
    settled = {p: widest(ls) for p, ls in lists.items() if ls and widest(ls)}
    for p, ls in lists.items():
        if not ls or p in settled:
            continue
        same = {x for x in ls if x in settled.values()}
        votes = collections.Counter(ls).most_common()
        if len(same) == 1:
            settled[p] = same.pop()
        elif reference and all(within(x, reference) for x in ls):
            found = {c for x in ls for c in x}   # the headings the readings found, in the neighbouring edition's order
            settled[p] = tuple(c for c in reference if c in found)
        elif votes[0][1] >= 2 and (len(votes) == 1 or votes[1][1] < votes[0][1]):
            settled[p] = votes[0][0]
        elif log is not None:
            log.append((year, kind, f"page {p} headings disagree", ls))
    # a page whose headings fit inside another page's longer list (one column group, a heading missed) takes it
    tops = {x for x in settled.values() if not any(x != y and within(x, y) for y in settled.values())}
    for p, x in list(settled.items()):
        sup = [y for y in tops if within(x, y)]
        if len(sup) == 1:
            settled[p] = sup[0]
    order: list[str] = []
    pages: dict[int, tuple[list[str], bool]] = {}
    last = None
    for p in allp:
        if lists[p]:
            last = (list(settled[p]), any(p in r["totals"] for r in readings)) if p in settled else None
            if last:
                order += [c for c in last[0] if c not in order]
        if last:
            pages[p] = last
    return order or None, pages


@lru_cache(maxsize=1)
def _long_series_suicides() -> dict:
    """{(place, ptype, year): suicides} from the long series (analysis/longseries.py)."""
    f = ROOT / "web" / "data" / "explore" / "adsi" / "long-series-provenance.csv"
    if not f.exists():
        return {}
    ls = pd.read_csv(f)
    ls = ls[ls["head"] == "suicides"]
    return {(r.place, r.ptype, int(r.year)): float(r.value) for r in ls.itertuples()}


def _pos_check(vals: list, ncat: int, split: bool, target: float | None, ptype: str) -> bool:
    """A place's figures add up exactly (an N.A. category counts as nothing), and the Grand Total is within 1% of
    the long series' count; without that count only a table with sexes (three equations) is trusted, and never for
    a total row (a misread 'Total (Cities)' must not pass for All India)."""
    if split:
        tm, tf, gt = vals[-3:]
        if any(not isinstance(x, int) for x in (tm, tf, gt)):
            return False
        ms = sum(x for x in vals[0:2 * ncat:2] if isinstance(x, int))
        fs = sum(x for x in vals[1:2 * ncat:2] if isinstance(x, int))
        # one sex's printed total a digit out (1981 Tamil Nadu means: Total F 1,825, its females adding up to 1,826,
        # 3,010 + 1,826 = the Grand Total 4,836 = the long series) is taken as that total misread, if the long series
        # confirms the Grand Total; the categories, which are what is kept, then add up exactly
        one_off = target is not None and ms + fs == gt and sorted([abs(ms - tm), abs(fs - tf)]) == [0, 1]
        if not ((ms == tm and fs == tf and tm + tf == gt) or one_off):
            return False
    else:
        gt = vals[-1]
        if not isinstance(gt, int) or sum(x for x in vals[:ncat] if isinstance(x, int)) != gt:
            return False
    if gt <= 0:
        return False
    if target is None:
        return split and ptype != "total"
    return abs(gt - target) <= 0.01 * target


def positional_edition(year: int, kind: str, log: list | None = None, reference: list[str] | None = None) -> pd.DataFrame:
    """Every place's categories x sex from one edition's appendix, read by position (see above); COLS records with
    the printed category in ``cat``."""
    from itertools import combinations, product

    from ncrb.vlm_tables import CACHE, file_sha, model_slug

    path = _pos_file(year, kind)
    if path is None:
        return frame([])
    sha = file_sha(path)
    readings = []
    for m in VLM_MODELS:
        d = CACHE / model_slug(m) / sha[:16]
        if not d.is_dir():
            continue
        texts = {int(p.stem): p.read_text(encoding="utf-8") for p in d.glob("*.txt") if p.stem.isdigit()}
        if texts:
            readings.append(_pos_reading(texts, year, kind))
    if not readings or not any(r["titled"] for r in readings):
        return frame([])
    lay, page_heads = _pos_layout(readings, year, kind, log, reference)
    if not lay:
        return frame([])
    if reference is None:
        POS_LAYOUTS[(year, kind)] = lay
    # a table without sexes has one equation per place, so it is read only where the printed column numbers (two
    # readings agreeing) count exactly its categories and Total
    ncols = collections.Counter(r["ncols"] for r in readings if r["ncols"]).most_common()
    ncols = ncols[0][0] if ncols and ncols[0][1] >= 2 and (len(ncols) == 1 or ncols[1][1] < ncols[0][1]) else None
    target = _long_series_suicides()
    recs = []
    keys = {k for r in readings for k in r["places"]}
    for key in keys:
        # the place's rows on each page, from every reading that found it on the same pages
        sets: dict[tuple, dict[int, set]] = {}
        for p in (r["places"] for r in readings):
            if key not in p:
                continue
            pages = tuple(sorted(p[key]))
            for pno, vs in p[key].items():
                for v in vs:
                    if v is not None:
                        sets.setdefault(pages, {}).setdefault(pno, set()).add(tuple(v))
        passed = {}
        for found, cand in sets.items():
            if set(cand) != set(found) or len(found) > 10:
                continue
            for pages in (sub for n in range(1, len(found) + 1) for sub in combinations(found, n)):
                # each page must carry the figures its own headings promise, the pages together every category once
                # (a stray row on another page, say a misread name, is left out)
                if any(p not in page_heads for p in pages) or [c for p in pages for c in page_heads[p][0]] != lay \
                        or [page_heads[p][1] for p in pages] != [False] * (len(pages) - 1) + [True]:
                    continue
                combos = list(product(*[sorted(cand[pno], key=str) for pno in pages]))
                if len(combos) > 512:
                    continue
                for combo in combos:
                    for split in (True, False):
                        if not split and ncols != len(lay) + 1:
                            continue
                        want = [(2 if split else 1) * len(page_heads[p][0]) + ((3 if split else 1) if page_heads[p][1] else 0) for p in pages]
                        if [len(part) for part in combo] != want:
                            continue
                        vals = [x for part in combo for x in part]
                        if _pos_check(vals, len(lay), split, target.get((key[0], key[1], year)), key[1]):
                            passed[(split, tuple(vals))] = True
        if len(passed) != 1:
            if log is not None and len(passed) > 1:
                log.append((year, kind, "readings disagree", key))
            continue
        split, vals = next(iter(passed))
        for i, name in enumerate(lay):
            if split:
                for sex, v in (("Male", vals[2 * i]), ("Female", vals[2 * i + 1])):
                    if isinstance(v, int):
                        recs.append((year, key[0], key[1], "", name, sex, "all ages", v, POS_CHECK, "ncrb"))
            elif isinstance(vals[i], int):
                recs.append((year, key[0], key[1], "", name, "Total", "all ages", vals[i], POS_CHECK, "ncrb"))
        if log is not None:
            log.append((year, kind, "ok", key, vals[-1]))
    return frame(recs)


def positional(kind: str, table: list, log: list | None = None) -> pd.DataFrame:
    """All the 1967-1988 editions read by position, categories harmonised with ``table``. An edition is read again
    with the categories of the year before (or after) deciding between readings whose headings contradict each
    other, and that reading kept where it lets more places add up."""
    out = []
    first = {y: positional_edition(y, kind, log) for y in POS_YEARS}
    for y in POS_YEARS:
        d = first[y]
        # an edition's categories come only from its own pages: a neighbouring edition's order would make the figures
        # add up without proving the labels (NCRB reordered columns between editions), so it is not used
        ref = None
        if ref:
            # the neighbour's categories decide only where they let more places add up (a heading the models missed)
            d2 = positional_edition(y, kind, None, ref)
            if d2[["place", "ptype"]].drop_duplicates().shape[0] > d[["place", "ptype"]].drop_duplicates().shape[0]:
                d = d2
                if log is not None:
                    log.append((y, kind, "read with the neighbouring edition's categories", sorted(set(zip(d.place, d.ptype)))))
        if d.empty:
            continue
        d["cat"] = d["cat"].map(lambda c: standard(c, table))
        d = d[d["cat"].notna()]
        out.append(d.groupby(["year", "place", "ptype", "group", "cat", "sex", "age", "check", "source"], as_index=False).value.sum()[COLS])
    return pd.concat(out, ignore_index=True) if out else frame([])


def positional_credit(year: int, kind: str, topics: list[str]) -> None:
    """Add the edition's appendix to the credit line of ``topics`` for ``year``."""
    path = _pos_file(year, kind)
    url = q("SELECT source_url FROM tables WHERE source_file = ? LIMIT 1", [str(path.relative_to(ROOT))]).source_url
    url = url.iloc[0] if len(url) else (f"https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/{path.name}"
                                        if re.match(r"\d", path.name) else None)
    if not url:
        return
    title = f"State wise distribution of Suicides by {'Means Adopted' if kind == 'means' else 'Causes'} during {year}"
    for t in topics:
        pv = PROV.get(t)
        if pv is None or not ((pv.year == year) & (pv.source_url == url)).any():
            row = pd.DataFrame([{"year": year, "title": title, "source_url": url, "method": "pdf_vlm"}])
            PROV[t] = row if pv is None else pd.concat([pv, row], ignore_index=True)


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
    # a table printing only male and female figures has no per-category total to check against; a scanned one is kept
    # here only because its year added up to the place's grand total above (1971, 1972, 1988 means tables)
    scanned_ok = (d["check"] == "no total") & (d.source != "text")
    d.loc[scanned_ok, "check"] = "ok (adds up to the grand total)"
    d = d[d["check"].isin(OK | {"ok (adds up to the grand total)", POS_CHECK}) | ((d["check"] == "no total") & (d.source == "text"))]
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
    # years with no printed rate: the long series' count of suicides over the population NCRB printed for that place
    # and year (analysis/population.py), marked 'computed' so the charts can tell them from NCRB's own rates
    import json

    prov = ROOT / "web" / "data" / "explore" / "adsi" / "long-series-provenance.csv"
    popf = ROOT / "web" / "data" / "explore" / "population.json"
    if prov.exists() and popf.exists():
        ls = pd.read_csv(prov)
        ls = ls[ls["head"] == "suicides"]
        pop = json.loads(popf.read_text())["places"]
        have = set(zip(d.year[d.cat == "Rate"], d.place[d.cat == "Rate"]))
        add = []
        for r in ls.itertuples():
            pp = pop.get(f"{r.place}|{r.ptype}", {}).get(str(int(r.year)))
            if (int(r.year), r.place) in have or not pp:
                continue
            add.append((int(r.year), r.place, r.ptype, "", "Rate", "Total", "all ages", round(r.value / pp, 2), "computed", "computed"))
        d = pd.concat([d, frame(add)], ignore_index=True)
    return d


def place_totals() -> dict:
    r = rates()
    s = r[r.cat == "Suicides"]
    return {(y, p): v for y, p, v in zip(s.year, s.place, s.value)}


def suicide_dataset(topics: list[str], age_topics: list[str], table: list, ogd_code: str | None, by_position: str | None = None) -> pd.DataFrame:
    d = tidy_categories(read_categories(topics, table), place_totals())
    if by_position:
        # the 1967-1988 appendices read by position (positional()), for the place-years the tables above leave out
        pos = positional(by_position, table)
        have = set(zip(d.year, d.place, d.ptype))
        pos = pos[[k not in have for k in zip(pos.year, pos.place, pos.ptype)]]
        for y in sorted(set(pos.year)):
            positional_credit(int(y), by_position, topics[:1])
        d = pd.concat([d, pos], ignore_index=True)
    if age_topics:
        a = tidy_categories(read_categories(age_topics, table), place_totals())
        a = a[a.age != "all ages"]
        d = pd.concat([d, a], ignore_index=True)
    if ogd_code:
        d = merge_sources(d, ogd_dataset(ogd_code, table))
    return add_both_sexes(d)


def suicide_means() -> pd.DataFrame:
    return suicide_dataset(["suicide_means_tn", "suicide_means_city"], ["suicide_means_age_tn"], MEANS, "Means_adopted", "means")


def suicide_profession() -> pd.DataFrame:
    return suicide_dataset(["suicide_profession_tn", "suicide_profession_city"], ["suicide_profession_age_tn"], PROFESSION, "Professional_Profile")


def suicide_causes() -> pd.DataFrame:
    return suicide_dataset(["suicide_causes_tn", "suicide_causes_city"], [], CAUSES, "Causes", "causes")


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
