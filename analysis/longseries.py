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
    ("murder", "Murder", r"\bmurd", r"attempt|culpable|c\.?\s?h\.?\b|not amount|motive|victim|fire.?arm|abetment|dowry"),
    ("attempt_murder", "Attempt to commit murder", r"attempt.{0,20}murd", r""),
    ("chna", "Culpable homicide not amounting to murder", r"culpable|c\.?\s?h\.?\s*not", r""),
    ("rape", "Rape", r"\brape", r"attempt|custod|gang|victim|incest|minor"),
    ("kidnapping", "Kidnapping & abduction", r"kidnap|abduct", r"women|girls|ransom|marriage|children|minor|murder"),
    ("dacoity", "Dacoity", r"dacoit", r"prep|assembl|murder"),
    ("robbery", "Robbery", r"robber", r"dacoit|prep"),
    ("burglary", "Burglary / house-breaking", r"burglar|house.?break", r""),
    ("theft", "Theft", r"theft", r"cattle|cycle|auto|motor|vehicle|railway|electric|other|ordinary"),
    ("riots", "Riots", r"\briot", r""),
    ("cbt", "Criminal breach of trust", r"breach of trust", r""),
    ("cheating", "Cheating", r"cheat", r""),
    ("counterfeiting", "Counterfeiting", r"counterfeit", r""),
    ("arson", "Arson", r"\barson", r""),
    ("hurt", "Hurt", r"\bhurt\b", r"grievous|acid|simple"),
    ("dowry_deaths", "Dowry deaths", r"dowry death", r""),
    ("molestation", "Assault on women with intent to outrage modesty", r"modesty|molest", r""),
    ("cruelty", "Cruelty by husband or relatives", r"cruelty by husband", r""),
]
# a table that counts something other than cases registered
NOT_CASES_TABLE = re.compile(
    r"motive|arrest|juvenil|disposal|person|victim|percentage|value|property|fire.?arm|pending|convict|charge|by sex|"
    r"age.?group|recidiv|police (station|personnel|strength)|court|accused|apprehend|custod|casualt|district|"
    r"trial|prosecut|withdrawn|compound|rank|share|investigat|stolen|recover|offender|dead|death of|injured",
    re.I)
NOT_CASES_COL = re.compile(
    r"rate|%|percent|variation|share|rank|person|victim|female|male|arrest|population|lakh|average|ratio|"
    r"convict|charge|pending|disposal|withdrawn|compound|trial|acquit|investig|\b(r|v|p)\b\s*$|^\s*\(?(r|v)\)?\s*$",
    re.I)
CASES_COL = re.compile(r"\bi\b|incidence|cases|c\.?\s?r\.?\b|reported|registered|number|during the year", re.I)
YEAR = re.compile(r"(?<!\d)(19[5-9]\d|20[0-2]\d)(?!\d)")
# cities that were never a State's name: a row after one of these, in a table with no section headings, is a city
CITY_ONLY = re.compile(r"^[\W\d]*(calcutta|kolkata|ahmedabad|kanpur|bangalore|bengaluru|poona|pune|nagpur|lucknow|jaipur|indore|"
                       r"coimbatore|madurai|surat|varanasi|patna|agra|allahabad|jabalpur|amritsar|ludhiana|vadodara|baroda)\b", re.I)
WEIGHT = {"pdf_text": 3.0, "excel": 3.0, "pdf_vlm": 1.5, "pdf_mixed": 1.0, "pdf_ocr": 1.0}


def head_of(text: str, heads) -> str | None:
    hits = [k for k, _, inc, exc in heads if re.search(inc, text, re.I) and not (exc and re.search(exc, text, re.I))]
    return hits[0] if len(hits) == 1 else None


def candidates(pub: str, heads, years=(1953, 2024)) -> pd.DataFrame:
    """Every printed figure that is cases under one crime head for one place, with its year and source."""
    t = q("SELECT table_id, year, title, method, listing, checks_total, checks_passed, source_url FROM tables "
          "WHERE publication = ? AND n_cells > 0 AND year BETWEEN ? AND ?", [pub, *years])
    t = t[~t.title.fillna("").str.contains(NOT_CASES_TABLE)]
    out = []
    for chunk in range(0, len(t), 400):
        ids = t.table_id.iloc[chunk:chunk + 400].tolist()
        c = q(f'SELECT table_id, "row", section, name, col_no, "column", value FROM cells WHERE table_id IN ({",".join("?" * len(ids))}) '
              'AND value IS NOT NULL', ids)
        out.append(c)
    c = pd.concat(out).merge(t, on="table_id")
    c["column"] = c["column"].fillna("")
    c = c[(c.value >= 0) & (c.value == c.value.round())]      # counts of cases: whole and not negative (decimals are rates)
    c = c[~c["column"].str.contains(NOT_CASES_COL)]
    # which head: from the column, else from the title (one table per head, 1950s-60s)
    heads_col = {x: head_of(x, heads) for x in c["column"].unique()}
    heads_title = {x: head_of(re.sub(r"\d{4}", "", str(x)), heads) for x in c.title.unique()}
    c["head"] = [heads_col[col] or (heads_title[ti] if not heads_col[col] and (CASES_COL.search(col) or YEAR.search(col) or not col.strip()) else None)
                 for col, ti in zip(c["column"], c.title)]
    c = c[c["head"].notna()]
    # the year a figure belongs to: a single year named in its column, else the edition's year
    def fig_year(col, ed):
        ys = set(YEAR.findall(col))
        if len(ys) == 1:
            y = int(ys.pop())
            return y if ed - 6 <= y <= ed else None
        return ed if not ys else None
    c["fy"] = [fig_year(col, ed) for col, ed in zip(c["column"], c.year)]
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
        places.append(resolve(str(name or ""), str(sec2 or ""), meth in SCANNED, int(ed)))
    c["place"] = places
    c = c[c.place.notna()]
    c["pname"] = c.place.map(lambda p: p[0])
    c["ptype"] = c.place.map(lambda p: p[1])
    c["w"] = c.method.map(WEIGHT).fillna(1.0)
    ok = c.checks_total.fillna(0) > 0
    c.loc[ok, "w"] *= 0.5 + c.loc[ok, "checks_passed"] / c.loc[ok, "checks_total"]
    c["own"] = (c.fy == c.year)
    # where one table row gives several figures for the same head and year (garbled headings), the first column
    # is usually the cases registered; the rest are persons, rates or later stages
    c["_o"] = c.col_no.map(col_order)
    c["crank"] = c.groupby(["table_id", "row", "head", "fy"])._o.rank(method="dense") - 1
    return c[["pname", "ptype", "head", "fy", "value", "w", "own", "crank", "method", "table_id", "title", "year", "source_url"]]


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
        out.append({"value": v, "support": sum(x.w for x in rs), "n": len({x.table_id for x in rs}),
                    "text": any(x.method in ("pdf_text", "excel") for x in rs), "crank": min(x.crank for x in rs), "src": src})
    out.sort(key=lambda o: -o["support"])
    for o in out:
        rival = max((x["support"] for x in out if x is not o), default=0)
        o["firm"] = o["text"] or (o["n"] >= 2 and o["support"] > rival)
    return out


SKIP = 1.0      # cost of leaving a year empty
JUMP = 2.0      # cost per unit of |log change| between consecutive kept years (scaled by sqrt of the gap)


def path(years: list[int], opts: dict[int, list[dict]]) -> dict[int, dict]:
    """The readings that make the most consistent series: firm figures are fixed, and for the other years the
    reading is chosen (or the year left empty) to minimise jumps against the neighbours, favouring readings
    with more support and from a table's first column."""
    import math

    def emit(o):
        if o["firm"]:
            return -6.0
        return 1.2 - math.log1p(o["support"]) + 0.6 * o["crank"]

    def jump(a, b, gap):
        return JUMP * abs(math.log((a + 1) / (b + 1))) / math.sqrt(gap)

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
                    c = prev[0] + SKIP * (i - j - 1) + jump(opts[years[j]][m]["value"], o["value"], y - years[j]) + emit(o)
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
        chosen = path(years, opts)
        # a scanned reading must be within a factor of 2 of the median of at least two kept neighbours (within 5
        # years); repeated until nothing more drops, so a reading never vouches for another that is itself dropped
        kept = dict(chosen)
        while True:
            drop = []
            for y, o in kept.items():
                if o["firm"]:
                    continue
                near = [kept[x]["value"] for x in kept if x != y and abs(x - y) <= 5]
                m = median(near) if len(near) >= 2 else None
                if m is None or not (m > 0 and 0.5 <= o["value"] / m <= 2.0 or (m == 0 and o["value"] <= 5)):
                    drop.append(y)
            if not drop:
                break
            for y in drop:
                kept.pop(y)
        for y, o in sorted(kept.items()):
            src = o["src"]
            status = "text" if o["text"] else "agreed" if o["firm"] else "consistent"
            rows.append({"place": p, "ptype": pt, "head": h, "year": y, "value": o["value"], "status": status, "n": o["n"],
                         "table_id": src.table_id, "title": src.title, "edition": int(src.year), "url": src.source_url})
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
    for r in d.drop_duplicates(["edition", "title"]).itertuples(index=False):
        lst = srcs[str(r.edition)]
        if len(lst) < 8 and not any(x["title"] == r.title for x in lst):
            lst.append({"title": re.sub(r"\s+", " ", str(r.title)).strip()[:160], "url": r.url, "method": ""})
    years = sorted(int(y) for y in d.year.unique())
    return {"id": slug(f"long-{geo}-{title}"), "pub": pub, "topic": TOPIC, "title": title, "geo": geo, "mode": "places",
            "also": [], "years": years,
            "cats": [{"name": label[k], **({"total": 1} if k == "total" else {})} for k in hk], "brks": [""],
            "rows": [{"name": p, "type": t} for p, t in places], "d": data, "sources": dict(srcs)}


def main() -> None:
    c = candidates("cii", IPC_HEADS)
    d = pick(c)
    fams = [f for f in (
        family("cii", ("state", "ut", "total"), "state", IPC_HEADS, d, "Cases registered under main IPC crime heads, by State"),
        family("cii", ("city",), "city", IPC_HEADS, d, "Cases registered under main IPC crime heads, by city"),
    ) if f]
    idx_path = OUT / "index.json"
    index = json.loads(idx_path.read_text())
    index["families"] = [f for f in index["families"] if f["topic"] != TOPIC]
    for f in fams:
        (OUT / f["pub"] / f"{f['id']}.json").write_text(json.dumps(f, separators=(",", ":")), encoding="utf-8")
        index["families"].insert(0, {k: f[k] for k in ("id", "pub", "topic", "title", "geo", "mode")} | {
            "y0": f["years"][0], "y1": f["years"][-1], "n": len(f["years"]), "rows": len(f["rows"]), "cats": len(f["cats"]), "also": []})
    idx_path.write_text(json.dumps(index, separators=(",", ":")), encoding="utf-8")
    prov = d[["place", "ptype", "head", "year", "value", "status", "n", "table_id", "edition"]]
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
