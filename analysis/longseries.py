"""Long series: every State, UT and big city, each main crime head, 1953-2024.

Crime in India printed the same core figures in every edition, the cases
registered under each IPC crime head in each State and city, but in tables of
a different shape each time: one table per crime head in the 1950s-60s, a
"crime under different heads" table later, rates and incidence side by side
from the 1990s, and separate violent / property crime tables from 2014. The
Explore families follow one table shape and so start in the 1990s or 2000s.

This module instead collects, for every year, every printed figure that is a
count of cases under a crime head for a place, from whichever table holds it,
including the previous-year columns that comparative tables reprint, and keeps
the reading that is best supported:

- a figure from a text-layer table (copied digit for digit) wins;
- otherwise a figure printed alike in two or more tables (an edition and the
  next edition's comparison column, a State table and an all-heads table);
- a lone figure from an OCR'd scan is kept only if its table's totals mostly
  check out and it is in line with the neighbouring years (within a factor of
  2.5 of their median), since a misread digit or a figure from the wrong
  column is the usual error.

Output: Explore families (same JSON as analysis.families) under topic
"Long series since 1953", plus a provenance file naming the table behind every
figure. Run after analysis.families:

    uv run --extra analysis --extra vlm python -m analysis.longseries
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from statistics import median

import pandas as pd

from .engine import resolve
from .families import OUT, col_order, slug
from .lib import SCANNED, q

TOPIC = "Long series since 1953"

# canonical crime heads: (key, label, matches, unless)
IPC_HEADS = [
    ("total", "Total cognizable crimes (IPC)", r"total\s*(cog|i\.?\s?p\.?\s?c|crimes? \(?ipc)|total cognizable", r"sll|special|local|women|children|cyber|scheduled|juvenil|economic|violent|property"),
    ("murder", "Murder", r"\bmurd", r"attempt|culpable|c\.?\s?h\.?\b|not amount|motive|victim|fire.?arm|abetment|dowry|kidnap|abduct|rape|life convict|by group|dacoit"),
    ("attempt_murder", "Attempt to commit murder", r"attempt.{0,20}murd", r""),
    ("chna", "Culpable homicide not amounting to murder", r"culpable|c\.?\s?h\.?\s*not", r"attempt"),
    ("rape", "Rape", r"\brape", r"attempt|victim|incest|minor|^(?!.*(total rape|custodial\s*\+)).*(custod|gang)"),
    ("kidnapping", "Kidnapping & abduction", r"kidnap|abduct", r"women|girls|ransom|marriage|children|minor|murder"),
    ("dacoity", "Dacoity", r"dacoit", r"prep|assembl|murder"),
    ("robbery", "Robbery", r"robber", r"dacoit|prep"),
    ("burglary", "Burglary / house-breaking", r"burglar|house.?break", r""),
    ("theft", "Theft", r"theft", r"cattle|cycle|auto|motor|vehicle|railway|electric|other|ordinary"),
    ("riots", "Riots", r"\briot", r""),
    ("cbt", "Criminal breach of trust", r"breach of trust", r""),
    # from 2017 NCRB prints 'Forgery, Cheating & Fraud' with Cheating (Sec. 420) as one of its parts: the part is the
    # head that matches the earlier years, not the combined total or the frauds
    ("cheating", "Cheating", r"cheat", r"(forgery|fraud)(?!.*\|\s*(b\)\s*)?cheating\b)|impersonation|personation"),
    ("counterfeiting", "Counterfeiting", r"counterfeit", r""),
    ("arson", "Arson", r"\barson", r""),
    ("hurt", "Hurt", r"\bhurt\b", r"acid|rash|negligen|driving|endanger|deter|weapon|attempt|(simple|grievous)\s+hurt\s*\(total|"
                               r"(simple|grievous) hurt (simple|grievous) hurt|^(?!.*(hurt\s*\(total|simple\s*\+\s*grievous)).*(grievous|simple)"),
    ("dowry_deaths", "Dowry deaths", r"dowry death", r""),
    ("molestation", "Assault on women with intent to outrage modesty", r"modesty|molest", r""),
    ("cruelty", "Cruelty by husband or relatives", r"cruelty by husband", r""),
]
# a table that counts something other than cases registered
NOT_CASES_TABLE = re.compile(
    r"motive|arrest|juvenil|disposal|person|victim(?!s?\s*\(\s*v\s*\))|value|property|fire.?arm|pending|convict|charge|by sex|"
    # crimes against a group (SCs, STs, children, senior citizens, foreigners) are a subset of all cases under a head
    r"scheduled|atrocit|\bs\.?\s?[ct]s?\b|child|senior|elderly|foreigner|tourist|"
    # cyber crimes: IPC heads committed through communication devices, a small subset
    r"cyber|communication device|\bit act|"
    # cases of one agency or kind of offender: railway police (GRP), insurgents, extremists
    r"insurgen|extremist|naxal|terroris|left.?wing|\bgrp\b|railway|"
    r"age.?group|recidiv|police (station|personnel|strength)|court|accused|apprehend|custod|casualt|district|"
    r"trial|prosecut|withdrawn|compound|investigat|stolen|recover|offender|dead|death of|injured|"
    # tables of shares only; a 'comparative incidence ... and percentage variation' table keeps its count columns
    r"^\W*(table\W*[\w.-]*\W*)?(percentage|share|rank)",
    re.I)
# the all-heads IPC table, whose total column is just 'Total | I' (2002) or 'Total'
IPC_TABLE = re.compile(r"cognizable crimes\s*\(ipc\)|\bipc crimes\b|crime under different (crime )?heads", re.I)
BARE_TOTAL = re.compile(r"^\s*total\s*(\|\s*(i|incidence|cases?|c\.?\s?r\.?)\s*)?$", re.I)
NOT_CASES_COL = re.compile(
    r"rate|%|percent|variation|share|rank|person|victim|female|male|arrest|population|lakh|average|ratio|"
    # 2024: each head in two halves, IPC (to 30 June) and BNS (from 1 July), then their total
    r"\|\s*(ipc|bns)\s*$|"
    r"convict|charge|pending|disposal|withdrawn|compound|trial|acquit|investig|communication device|cyber|\bit act|"
    r"\b(r|v|p)\b\s*(\(\s*\d+\s*\)|\d+[a-z]?)?\s*$|^\s*\(?(r|v)\)?\s*$",
    re.I)
CASES_COL = re.compile(r"\bi\b|incidence|cases|c\.?\s?r\.?\b|reported|registered|number|during the year", re.I)
YEAR = re.compile(r"(?<!\d)(19[5-9]\d|20[0-2]\d)(?!\d)")
# cities that were never a State's name: a row after one of these, in a table with no section headings, is a city
CITY_ONLY = re.compile(r"^[\W\d]*(calcutta|kolkata|ahmedabad|kanpur|bangalore|bengaluru|poona|pune|nagpur|lucknow|jaipur|indore|"
                       r"coimbatore|madurai|surat|varanasi|patna|agra|allahabad|jabalpur|amritsar|ludhiana|vadodara|baroda)\b", re.I)
WEIGHT = {"pdf_text": 3.0, "excel": 3.0, "pdf_vlm": 1.5, "pdf_mixed": 1.0, "pdf_ocr": 1.0}


def head_of(text: str, heads) -> str | None:
    hits = [k for k, _, inc, exc, *_ in heads if re.search(inc, text, re.I) and not (exc and re.search(exc, text, re.I))]
    return hits[0] if len(hits) == 1 else None


# counts of people (deaths, prisoners) are what ADSI and Prison Statistics measure: only rates, shares and splits go
NOT_COUNT_COL = re.compile(r"rate|%|percent|variation|share|rank|female|male|women|(mid.?year|projected|census)\s*population|lakh|average|ratio|occupancy|"
                           r"\b(r)\b\s*$|^\s*\(?r\)?\s*$", re.I)


def candidates(pub: str, heads, years=(1953, 2024), not_table=NOT_CASES_TABLE, need_table=None, not_col=NOT_CASES_COL) -> pd.DataFrame:
    """Every printed figure that is a count under one head for one place, with its year and source."""
    t = q("SELECT table_id, year, title, method, listing, checks_total, checks_passed, source_url FROM tables "
          "WHERE publication = ? AND n_cells > 0 AND year BETWEEN ? AND ?", [pub, *years])
    # which tables: the rules, with Jev's labels where it is sure (analysis.classify)
    from .classify import table_policy
    pol = table_policy(pub, t.title, not_table)
    t = t.assign(policy=t.title.map(pol).fillna("keep"))
    t = t[t.policy != "drop"]
    if need_table is not None:
        # a scanned continuation page's title can be just its page number ('22'): its file says what it is
        t = t[t.title.fillna("").str.contains(need_table) | t.table_id.str.contains(need_table)]
    out = []
    for chunk in range(0, len(t), 400):
        ids = t.table_id.iloc[chunk:chunk + 400].tolist()
        c = q(f'SELECT table_id, "row", section, name, col_no, "column", value FROM cells WHERE table_id IN ({",".join("?" * len(ids))}) '
              'AND value IS NOT NULL', ids)
        out.append(c)
    c = pd.concat(out).merge(t, on="table_id")
    c["column"] = c["column"].fillna("")
    c = c[(c.value >= 0) & (c.value == c.value.round())]      # counts of cases: whole and not negative (decimals are rates)
    c = c[~c["column"].str.contains(not_col)]
    # which head: from the column, else from the title (one table per head, 1950s-60s)
    heads_col = {x: head_of(x, heads) for x in c["column"].unique()}
    heads_title = {x: head_of(re.sub(r"\d{4}", "", str(x)), heads) for x in c.title.unique()}
    # a head taken from the title needs a column that counts it: cases/incidence by default, or the head's own
    # column pattern (road deaths: 'Died', 'Persons killed')
    colneed = {h[0]: re.compile(h[4], re.I) for h in heads if len(h) > 4 and h[4]}
    def from_title(col, ti):
        k = heads_title[ti]
        if not k:
            return None
        if k in colneed:
            return k if colneed[k].search(col) and not re.search(r"male|female|injur|cases", col, re.I) else None
        return k if (CASES_COL.search(col) or YEAR.search(col) or not col.strip() or re.fullmatch(r"\s*col_\d+\s*", col)
                     or re.fullmatch(r"\W*cogni[sz]able\s+crimes\W*", col, re.I)) else None
    c["head"] = [heads_col[col] or from_title(col, ti) for col, ti in zip(c["column"], c.title)]
    # headings Jev is sure name another head, or hold rates or victims (analysis.classify)
    from .classify import column_veto
    veto = column_veto(pub, c["column"].unique(), heads_col)
    c.loc[c["column"].isin(veto), "head"] = None
    # heads that may only come from certain tables (prisons: the State-wise distribution tables, not annexures)
    tneed = {h[0]: re.compile(h[5], re.I) for h in heads if len(h) > 5 and h[5]}
    if tneed:
        c["head"] = [None if (k in tneed and not tneed[k].search(str(ti))) else k for k, ti in zip(c["head"], c.title)]
    bare = c["head"].isna() & c["column"].str.match(BARE_TOTAL) & c.title.fillna("").str.contains(IPC_TABLE) \
        & ~c.title.fillna("").str.contains(r"sll|special|local|women|children|scheduled|cyber|juvenil", case=False)
    c.loc[bare, "head"] = "total"
    c = c[c["head"].notna()]
    # the year a figure belongs to: a single year named in its column, else the edition's year
    def fig_year(col, ed, ti):
        ys = set(YEAR.findall(col))
        if len(ys) == 1:
            y = int(ys.pop())
            return y if ed - 6 <= y <= ed else None
        if ys:
            return None
        # a table filed under a later edition whose title names its own year ('... during 2012' in the 2015 files)
        ts = {int(y) for y in YEAR.findall(str(ti))}
        if len(ts) == 1 and ed - 6 <= min(ts) < ed:
            return ts.pop()
        return ed
    c["fy"] = [fig_year(col, ed, ti) for col, ed, ti in zip(c["column"], c.year, c.title)]
    # comparative tables whose year row was not read ("MURDER (6)", "MURDER (7)" for 1968 and 1969): the same
    # head in two or three columns, with no year of its own, is consecutive years ending with the edition's year
    c["_o"] = c.col_no.map(col_order)
    # 'Inmate Population M F Tr. Total (7)..(10)': one flattened heading over the Male, Female, Transgender and
    # Total columns, not years; the Total (the largest of them) is the figure
    sexsplit = c["column"].str.contains(r"\bM\b.{0,6}\bF\b|male.{0,12}female", case=False, regex=True)
    if sexsplit.any():
        top = c[sexsplit].groupby(["table_id", "row", "head"]).value.transform("max")
        c = c[~sexsplit | (c.value == top.reindex(c.index).fillna(-1))]
        sexsplit = sexsplit.reindex(c.index)
    base = c["column"].str.replace(r"\(\s*\d+\s*\)|\s+", " ", regex=True).str.strip().str.lower()
    from_col = c["column"].map(lambda x: heads_col.get(x) is not None) & ~c["column"].str.contains(YEAR) & ~sexsplit
    reyear = {}
    for (tid, b), g in c[from_col].assign(_b=base[from_col]).groupby(["table_id", "_b"]):
        cols = sorted(g.drop_duplicates("col_no")[["col_no", "_o"]].itertuples(index=False), key=lambda x: x[1])
        # a column whose figures are far smaller than its neighbours' is a change or a share, not a year
        sums = g.groupby("col_no").value.sum()
        top = sums.max() if len(sums) else 0
        cols = [x for x in cols if top and sums.get(x[0], 0) >= 0.3 * top]
        if 2 <= len(cols) <= 3:
            ed = int(g.year.iloc[0])
            for i, (cn, _) in enumerate(cols):
                reyear[(tid, cn)] = ed - (len(cols) - 1 - i)
    if reyear:
        c["fy"] = [reyear.get((t, cn), y) for t, cn, y in zip(c.table_id, c.col_no, c.fy)]
    c = c[c.fy.notna()]
    # places; in tables without section headings, rows after the first city-only name are cities
    first_city = {}
    for tid, g in c.groupby("table_id"):
        m = g[g.name.fillna("").str.match(CITY_ONLY)]
        first_city[tid] = m["row"].min() if len(m) else None
    places = []
    for tid, row, sec, name, meth, ed in zip(c.table_id, c["row"], c.section, c.name, c.method, c.year):
        fc = first_city.get(tid)
        sec2 = sec if (sec and re.search(r"cit|state|u\.?\s?t", str(sec), re.I)) else ("Cities" if fc is not None and row >= fc else (sec or ""))
        nm = re.sub(r"\s+police\b.*$", "", str(name or ""), flags=re.I)        # 'Madras City Police'
        places.append(resolve(nm, str(sec2 or ""), meth in SCANNED, int(ed)))
    c["place"] = places
    c = c[c.place.notna()]
    # a district-and-city table: only the rows named as a city (district names repeat city and State names)
    c = c[(c.policy != "cities") | ((c.place.map(lambda p: p[1]) == "city") & c.name.fillna("").str.contains(r"\bcity\b", case=False))]
    # a table of crimes against women: only the heads that are crimes against women
    c = c[(c.policy != "women") | c["head"].isin(["rape", "dowry_deaths", "molestation", "cruelty"])]
    c["pname"] = c.place.map(lambda p: p[0])
    c["ptype"] = c.place.map(lambda p: p[1])
    # a city must be one NCRB lists in its city tables (text-layer headings otherwise slip in as 'cities')
    from .engine import known_cities
    cities = set(known_cities())
    c = c[(c.ptype != "city") | c.pname.isin(cities)]
    c["w"] = c.method.map(WEIGHT).fillna(1.0)
    ok = c.checks_total.fillna(0) > 0
    c.loc[ok, "w"] *= 0.5 + c.loc[ok, "checks_passed"] / c.loc[ok, "checks_total"]
    c["own"] = (c.fy == c.year)
    # where one table row gives several figures for the same head and year (garbled headings), the first column
    # is usually the cases registered; the rest are persons, rates or later stages
    c["crank"] = c.groupby(["table_id", "row", "head", "fy"])._o.rank(method="dense") - 1
    return c[["pname", "ptype", "head", "fy", "value", "w", "own", "crank", "method", "table_id", "title", "column", "year", "source_url"]]


def options(g: pd.DataFrame) -> list[dict]:
    """The distinct readings of one place, head and year, with how well each is supported."""
    groups = defaultdict(list)
    for r in g.itertuples(index=False):
        v = float(r.value)
        key = next((k for k in groups if abs(k - v) <= max(0.5, 0.002 * abs(k))), v)
        groups[key].append(r)
    out = []
    for v, rs in groups.items():
        src = sorted(rs, key=lambda x: (not x.own, x.crank, -x.w))[0]
        # independent printings: the same table reprinted in a year-wise volume is one source, not two
        indep = {(int(x.year), re.sub(r"[^a-z]+", "", str(x.title).lower())[:50]) for x in rs}
        out.append({"value": v, "support": sum(x.w for x in rs), "n": len(indep),
                    "text": any(x.method in ("pdf_text", "excel") for x in rs), "crank": min(x.crank for x in rs), "src": src})
    out.sort(key=lambda o: -o["support"])
    for o in out:
        rival = max((x["support"] for x in out if x is not o), default=0)
        o["firm"] = o["text"] or (o["n"] >= 2 and o["support"] > rival)
    return out


# the first full year after a State lost or gained a large area: figures on either side are not compared (Madras
# lost Andhra in Oct 1953 and Malabar in Nov 1956, so 1953 is far above 1954 and 1956 above 1957)
BREAKS = {
    "Tamil Nadu": (1954, 1957), "Kerala": (1957,), "Karnataka": (1954, 1957), "Andhra Pradesh": (1957, 2015),
    "Madhya Pradesh": (1957, 2001), "Rajasthan": (1957,), "Punjab": (1957, 1967), "Himachal Pradesh": (1967,),
    "Bihar": (2001,), "Uttar Pradesh": (2001,), "Assam": (1964, 1972), "Jammu & Kashmir": (2020,),
}


def segment(place: str, year: int) -> int:
    return sum(year >= b for b in BREAKS.get(place, ()))


SKIP = 1.0      # cost of leaving a year empty
JUMP = 2.0      # cost per unit of |log change| between consecutive kept years (scaled by sqrt of the gap)


def path(years: list[int], opts: dict[int, list[dict]], place: str = "") -> dict[int, dict]:
    """The readings that make the most consistent series: firm figures are fixed, and for the other years the
    reading is chosen (or the year left empty) to minimise jumps against the neighbours, favouring readings
    with more support and from a table's first column."""
    import math

    def emit(o):
        if o["firm"]:
            # several printed figures for a year (an edition, a later revision): the one more tables agree on
            return -6.0 - 2.0 * min(o["n"], 3)
        return 1.2 - math.log1p(o["support"]) + 0.6 * o["crank"]

    def jump(a, b, gap, y):
        cut = 0.25 if segment(place, y - gap) != segment(place, y) else 1.0      # the State itself changed
        return cut * JUMP * abs(math.log((a + 1) / (b + 1))) / math.sqrt(gap)

    # a year with several printed figures, one of them exactly the year before's: that one is last year's table
    # filed under this year (NCRB's '... City-wise - 2019' file holds the 2018 figures)
    for i, y in enumerate(years[1:], 1):
        before = [o for o in opts[years[i - 1]] if o["firm"]] if years[i - 1] == y - 1 else []
        if not before:
            continue
        last = max(before, key=lambda o: o["support"])["value"]        # the year before's best-supported figure
        firm = [o for o in opts[y] if o["firm"]]
        rep = [o for o in firm if o["value"] >= 50 and o["value"] == last]
        rivals = [o for o in firm if o not in rep and 0.5 * last <= o["value"] <= 2 * last
                  and o["support"] >= max((r["support"] for r in rep), default=0)]
        if rep and rivals:
            opts[y] = [o for o in opts[y] if o not in rep]
    # dp over (year index, option index); a state may skip up to 4 years back
    best: dict[tuple[int, int], tuple[float, tuple[int, int] | None]] = {}
    for i, y in enumerate(years):
        for k, o in enumerate(opts[y]):
            if any(x["firm"] for x in opts[y]) and not o["firm"]:
                continue
            cost0 = SKIP * i + emit(o)                       # first kept year
            choice = (cost0, None)
            for j in range(max(0, i - 5), i):
                for m, _ in enumerate(opts[years[j]]):
                    prev = best.get((j, m))
                    if prev is None:
                        continue
                    c = prev[0] + SKIP * (i - j - 1) + jump(opts[years[j]][m]["value"], o["value"], y - years[j], y) + emit(o)
                    if c < choice[0]:
                        choice = (c, (j, m))
            best[(i, k)] = choice
    if not best:
        return {}
    n = len(years)
    end = min(best, key=lambda s: best[s][0] + SKIP * (n - 1 - s[0]))
    out, s = {}, end
    while s is not None:
        out[years[s[0]]] = opts[years[s[0]]][s[1]]
        s = best[s][1]
    return out


def pick(c: pd.DataFrame) -> pd.DataFrame:
    """One figure per place, head and year: firm readings, and the most consistent of the rest."""
    rows = []
    for (p, pt, h), g in c.groupby(["pname", "ptype", "head"]):
        opts = {int(y): options(gy) for y, gy in g.groupby("fy")}
        years = sorted(opts)
        chosen = path(years, opts, p)
        # a scanned reading must be within a factor of 2 of the median of at least two kept neighbours (within 5
        # years); repeated until nothing more drops, so a reading never vouches for another that is itself dropped
        kept = dict(chosen)
        while True:
            drop = []
            for y, o in kept.items():
                if o["firm"]:
                    continue
                near = [kept[x]["value"] for x in kept if x != y and abs(x - y) <= 5 and segment(p, x) == segment(p, y)]
                wide = len(near) < 2        # alone in its territory (Madras 1953): any neighbours, a wider band
                if wide:
                    near = [kept[x]["value"] for x in kept if x != y and abs(x - y) <= 5]
                m = median(near) if len(near) >= 2 else None
                # counts in the hundreds and up rarely move more than ~30% in a year; small ones can double
                lo, hi = (0.4, 2.5) if wide else (0.7, 1.43) if m and m >= 200 and len(near) >= 3 else (0.5, 2.0)
                if m is None or not (m > 0 and lo <= o["value"] / m <= hi or (m == 0 and o["value"] <= 5)):
                    drop.append(y)
            if not drop:
                break
            for y in drop:
                kept.pop(y)
        for y, o in sorted(kept.items()):
            src = o["src"]
            status = "text" if o["text"] else "agreed" if o["firm"] else "consistent"
            rows.append({"place": p, "ptype": pt, "head": h, "year": y, "value": o["value"], "status": status, "n": o["n"], "method": src.method,
                         "table_id": src.table_id, "title": src.title, "column": getattr(src, "column", ""), "edition": int(src.year), "url": src.source_url})
    return pd.DataFrame(rows)


def family(pub: str, ptypes: tuple[str, ...], geo: str, heads, d: pd.DataFrame, title: str) -> dict | None:
    d = d[d.ptype.isin(ptypes)]
    if d.empty:
        return None
    hk = [k for k, *_ in heads if k in set(d["head"])]
    hk = [k for k in hk if k != "total"] + (["total"] if "total" in hk else [])
    label = {k: lab for k, lab, *_ in heads}
    tord = {"total": 0, "state": 1, "ut": 2, "city": 3}
    places = sorted({(p, t) for p, t in zip(d.place, d.ptype)}, key=lambda x: (tord.get(x[1], 9), x[0]))
    pi = {k: i for i, k in enumerate(places)}
    hi = {k: i for i, k in enumerate(hk)}
    data = defaultdict(list)
    for r in d.sort_values("year").itertuples(index=False):
        v = r.value
        data[f"{pi[(r.place, r.ptype)]}.{hi[r.head]}.0"] += [r.year, int(v) if float(v).is_integer() else round(v, 2)]
    srcs = defaultdict(list)
    # sources by the year a figure is for (the chart asks whether that year was read from a scan)
    for r in d.drop_duplicates(["year", "title"]).itertuples(index=False):
        lst = srcs[str(r.year)]
        if len(lst) < 8 and not any(x["title"] == r.title for x in lst):
            lst.append({"title": re.sub(r"\s+", " ", str(r.title)).strip()[:160], "url": r.url, "method": r.method})
    years = sorted(int(y) for y in d.year.unique())
    return {"id": slug(f"long-{geo}-{title}"), "pub": pub, "topic": TOPIC, "title": title, "geo": geo, "mode": "places",
            "also": [], "years": years,
            "cats": [{"name": label[k], **({"total": 1} if k == "total" else {})} for k in hk], "brks": [""],
            "rows": [{"name": p, "type": t} for p, t in places], "d": data, "sources": dict(srcs)}


# ADSI: the State/UT/city totals of suicides and accidental deaths (not the breakdowns by cause, means, age ...)
ADSI_HEADS = [
    ("suicides", "Suicides", r"suicid", r"rate|attempt|farm|agricult|student|police|capf|armed"),
    ("accidental", "Accidental deaths (all causes)", r"accidental deaths?|accidents?\s*\(?total|total accident|un.?natural and natural|all causes",
     r"rate|road|traffic|rail|fire|nature|natural cause|un.?natural cause|other cause|drown|poison|electrocut"),
    # deaths in road crashes: a road/traffic accident table's deaths column ('Total | Died', 'Persons killed')
    ("road", "Deaths in road crashes", r"(road|traffic) accident.*(died|deaths?|killed)|(died|deaths?|killed).*(road|traffic) accident",
     r"rate|injur|rail|unmanned|crossing", r"(died|deaths?|killed)"),
]
ADSI_NOT_TABLE = re.compile(r"cause.?wise|by causes|causes? of|means|profession|occupation|education|age.?group|sex.?wise|month|time of|"
                            r"mode of|vehicle|place of|social status|marital|economic|district|^\W*(table\W*[\w.-]*\W*)?(percentage|share|rank)|"
                            r"farm|student|rail|crossing|weather|road classification|junction|traffic control", re.I)
ADSI_NEED_TABLE = re.compile(r"suicid|accident", re.I)
# Prison Statistics: capacity and the people held, by State/UT
PSI_HEADS = [   # (key, label, matches, unless, column must match, table title must match)
    ("capacity", "Capacity of prisons", r"capacity", r"rate|occupancy|%", None,
     r"capacity"),
    ("inmates", "Prison population (inmates)", r"inmate|prison population|population of (prisoners|inmates)|total prisoners",
     r"capacity|rate|occupancy|female|women|foreign|death|released|admitted|escape|convict|under.?trial|detenu", None,
     r"capacity|inmate population|prison population|occupancy|types? of (prison )?(inmates|prisoners)"),
    ("undertrials", "Undertrial prisoners", r"under.?trial", r"rate|%|female|women|foreign|released|death|period|age|education|caste|religion|domicile", None,
     r"distribution of under.?trials|under.?trials in jails|types? of (prison |indian prison )?(inmates|prisoners)|inmates? (population )?by type"),
    ("convicts", "Convicted prisoners", r"convict", r"rate|%|female|women|foreign|released|death|period|age|education|caste|religion|domicile|sentence|re.?convict", None,
     r"distribution of convicts|convicts in jails|types? of (prison |indian prison )?(inmates|prisoners)|inmates? (population )?by type"),
]
PSI_NOT_TABLE = re.compile(r"annex|foreign|(central|district|sub|women|open|special|other|borstal)\s+(jails?|schools?)|borstal|budget|expenditure|staff|vacanc|training|vehicle|wage|vocational|percentage|share|age.?group|"
                           r"education|caste|religion|domicile|sentence|period of|offence|crime head|death|escape|jail break|released|parole", re.I)


def suicide_datasets() -> pd.DataFrame:
    """Total suicides by State/UT (and city) from two transcriptions of NCRB's own tables, as extra candidates:
    'Suicides in India 2001-2012', the State-wise dataset NCRB gave data.gov.in (causes add up to the total; it
    is the only State-wise source for 2001-2003), and Reclaim Chennai's OpenDataChennai copies of ADSI's
    'incidence and rate of suicides' tables, 1998-2020 (States, UTs and cities)."""
    from .engine import ODC_RATES, OGD_FILE

    rows = []
    if OGD_FILE.exists():
        o = pd.read_csv(OGD_FILE)
        o = o[o.Type_code == "Causes"].groupby(["State", "Year"]).Total.sum().reset_index()
        for st, y, v in zip(o.State, o.Year, o.Total):
            p = resolve(str(st), "", False, int(y))
            if p and v > 0:
                rows.append({"pname": p[0], "ptype": p[1], "head": "suicides", "fy": int(y), "value": float(v), "w": 3.0, "own": True,
                             "crank": 0, "method": "excel", "table_id": "ogd/suicides-in-india-2001-2012", "year": int(y),
                             "title": "Suicides in India 2001-2012 (NCRB, data.gov.in): causes, total", "source_url": "https://data.gov.in"})
    if ODC_RATES.exists():
        r = pd.read_csv(ODC_RATES)
        for cat, nm, n, y in zip(r.Category, r["State or City"], r["Number of Suicides"], r.Year):
            try:
                v = float(str(n).replace(",", ""))
            except ValueError:
                continue
            p = resolve(str(nm), "Cities" if str(cat).lower().startswith("cit") else "", False, int(y))
            # its 1998-99 city rows are scrambled (Chennai 222 with a population of 125.9 lakh): left out
            if p and v > 0 and not (p[1] == "city" and int(y) < 2000):
                rows.append({"pname": p[0], "ptype": p[1], "head": "suicides", "fy": int(y), "value": v, "w": 2.5, "own": True,
                             "crank": 0, "method": "excel", "table_id": "odc/suicide-rate-state-city-1998-2020", "year": int(y),
                             "title": "Incidence and rate of suicides (ADSI), as copied in OpenDataChennai",
                             "source_url": "https://github.com/elseasama/OpenDataChennai"})
    return pd.DataFrame(rows)


def run_pub(pub, heads, title, cats_city, not_table, need_table, years):
    c = candidates(pub, heads, years=years, not_table=not_table, need_table=need_table, not_col=NOT_COUNT_COL)
    if pub == "adsi":
        c = pd.concat([c, suicide_datasets()], ignore_index=True)
    c = c[c.value > 0]          # a State's suicides, deaths or prisoners are never nil; a 0 is another column's
    d = pick(c) if len(c) else pd.DataFrame()
    if d.empty:
        return [], d
    # one family per head: suicides, accidental deaths and road deaths are different counts with their own sources
    fams = []
    for k, lab, *_ in heads:
        dk = d[d["head"] == k]
        if dk.empty:
            continue
        fams += [f for f in (
            family(pub, ("state", "ut", "total"), "state", heads, dk, f"{lab}, by State"),
            family(pub, ("city",), "city", heads, dk, f"{lab}, by city") if cats_city else None,
        ) if f]
    return fams, d


def main() -> None:
    c = candidates("cii", IPC_HEADS)
    d = pick(c)
    fams = [f for f in (
        family("cii", ("state", "ut", "total"), "state", IPC_HEADS, d, "Cases registered under main IPC crime heads, by State"),
        family("cii", ("city",), "city", IPC_HEADS, d, "Cases registered under main IPC crime heads, by city"),
    ) if f]
    fa, da = run_pub("adsi", ADSI_HEADS, "Suicides and accidental deaths", True, ADSI_NOT_TABLE, ADSI_NEED_TABLE, (1967, 2024))
    # Prison Statistics is left to its own Explore tables: its State totals sit among many look-alike columns (per
    # jail type, per sex, foreign inmates, annexures) and an automatic pick was not reliable before 2002
    fp, dp = [], pd.DataFrame()
    fams += fa + fp
    idx_path = OUT / "index.json"
    index = json.loads(idx_path.read_text())
    index["families"] = [f for f in index["families"] if f["topic"] != TOPIC]
    for x, dd in (("adsi", da), ("psi", dp)):
        if len(dd):
            dd[["place", "ptype", "head", "year", "value", "status", "n", "table_id", "edition"]].to_csv(OUT / x / "long-series-provenance.csv", index=False)
            for place in ("Tamil Nadu", "Chennai"):
                g = dd[dd.place == place]
                for k in sorted(set(g["head"])):
                    ys = sorted(g[g["head"] == k].year)
                    print(f"  {x} {place} {k:12} {len(ys):>3} years  {ys[0] if ys else ''}-{ys[-1] if ys else ''}  {g[g['head'] == k].status.value_counts().to_dict()}")
    for f in fams:
        (OUT / f["pub"] / f"{f['id']}.json").write_text(json.dumps(f, separators=(",", ":")), encoding="utf-8")
        index["families"].insert(0, {k: f[k] for k in ("id", "pub", "topic", "title", "geo", "mode")} | {
            "y0": f["years"][0], "y1": f["years"][-1], "n": len(f["years"]), "rows": len(f["rows"]), "cats": len(f["cats"]), "also": []})
    idx_path.write_text(json.dumps(index, separators=(",", ":")), encoding="utf-8")
    prov = d[["place", "ptype", "head", "year", "value", "status", "n", "table_id", "column", "edition"]]
    prov.to_csv(OUT / "cii" / "long-series-provenance.csv", index=False)
    # coverage for Tamil Nadu and Chennai
    for place in ("Tamil Nadu", "Chennai"):
        g = d[d.place == place]
        print(f"\n{place}:")
        for k, lab, *_ in IPC_HEADS:
            ys = sorted(g[g["head"] == k].year)
            miss = [y for y in range(1953, 2025) if y not in ys]
            st = g[g["head"] == k].status.value_counts().to_dict()
            print(f"  {lab[:34]:34} {len(ys):>3} years {st}  missing: {compact(miss)}")
    print(f"\n{len(d)} figures for {d.place.nunique()} places; statuses {d.status.value_counts().to_dict()}")


def compact(ys):
    out, s = [], None
    for y in ys + [None]:
        if s is None:
            s = p = y
        elif y == p + 1:
            p = y
        else:
            out.append(f"{s}" if s == p else f"{s}-{p}")
            s = p = y
    return ", ".join(out)


if __name__ == "__main__":
    sys.exit(main())
