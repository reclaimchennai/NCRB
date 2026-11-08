"""Dowry: every figure NCRB printed on dowry deaths (Sec. 304B IPC, Sec. 80 BNS from July 2024) and the Dowry
Prohibition Act, 1961, joined across editions into one series per place and measure, for the dowry dashboard.

Measures, by State, UT and city unless noted:
- dowry deaths: cases registered (the long series, analysis/longseries.py), victims (printed from 2014), and the rate
  per lakh women (cases over the female population: NCRB's own from 2012, before that the Census of India's, a
  straight line between the 1991, 2001 and 2011 counts - labelled as such);
- Dowry Prohibition Act cases (1988-), the same Act throughout;
- police and courts: the charge-sheeting and conviction rates NCRB printed State-wise for 2000-2013, and for All India
  every year (cases charge-sheeted, convicted, acquitted, pending trial, and the two rates);
- suicides over dowry disputes (ADSI, 'Dowry dispute', from 2014 'Marriage related issues: dowry related').

Each figure is chosen as the long series chooses (analysis.longseries.pick): text-layer readings first, then the
value most printings agree on; a scanned reading far from its neighbours is left out.

    uv run --extra vlm --extra analysis python -m analysis.dowry      -> web/data/dowry/dowry.json
"""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict

import pandas as pd

from .engine import known_cities, resolve
from .lib import ROOT, SCANNED, q
from .longseries import WEIGHT, YEAR, pick

OUT = ROOT / "web" / "data" / "dowry" / "dowry.json"
CENSUS = ROOT / "data" / "external" / "census_female_population.csv"

# tables whose dowry columns are not cases registered in the place: persons, juveniles, motives of murder, districts,
# railway police, shares, metropolitan aggregates
NOT_TABLE = re.compile(r"juvenil|arrest|apprehend|motive|district|\bgrp\b|railway|percentage disposal|persons|"
                       r"metropolitan|excerpt|share|variation over|crime head-?wise in metro", re.I)
CODE = re.compile(r"^\s*\(?([IVRP])\)?\s*$", re.I)


def measure_of(col: str, title: str) -> tuple[str, str] | None:
    """(kind, measure) of a State/UT/city column: kind 'death' or 'dpa'; measure cases, victims, cs_rate, conv_rate."""
    segs = [s.strip() for s in str(col).split("|")]
    code = None
    if len(segs) > 1 and CODE.match(segs[-1]):
        code = CODE.match(segs[-1]).group(1).upper()
        segs = segs[:-1]
    if YEAR.search(segs[-1]) and not re.search(r"dowry", segs[-1], re.I):
        segs = segs[:-1]
    if not segs or not re.search(r"dowry", segs[-1], re.I):
        return None            # the column belongs to the head printed after the dowry one ('Dowry Prohibition Act | Child Marriage ...')
    s = segs[-1]
    kind = "death" if re.search(r"dowry\s*death", s, re.I) else "dpa" if re.search(r"dowry\s*proh", s, re.I) else None
    if not kind:
        return None
    t = str(title)
    if re.search(r"charge\W{0,3}sheeting rate", t, re.I):
        return kind, "cs_rate"
    if re.search(r"conviction rate", t, re.I):
        return kind, "conv_rate"
    if re.search(r"disposal", t, re.I):
        return None
    if code in ("R", "P"):
        return None
    if code == "V":
        return kind, "victims"
    return kind, "cases"


def fig_year(col: str, ed: int, title: str) -> int | None:
    col = re.sub(r"act,?\s*19[56]\d", "act", str(col), flags=re.I)          # 'Dowry Prohibition Act, 1961' names the Act, not the year
    ys = set(YEAR.findall(col))
    if len(ys) == 1:
        y = int(ys.pop())
        return y if ed - 6 <= y <= ed else None
    if ys:
        return None
    ts = {int(y) for y in YEAR.findall(str(title))}
    if len(ts) == 1 and min(ts) < ed:
        return ts.pop() if ed - 6 <= min(ts) else None
    return ed


def place_of(name, section, method, ed):
    nm = re.sub(r"\s+police\b.*$", "", str(name or ""), flags=re.I)
    return resolve(nm, str(section or ""), method in SCANNED, int(ed))


def cand_rows(c: pd.DataFrame, head: str, cities: set) -> list[dict]:
    rows = []
    for r in c.itertuples(index=False):
        pl = place_of(r.name, r.section, r.method, r.year)
        if not pl or (pl[1] == "city" and pl[0] not in cities):
            continue
        fy = fig_year(r.column, int(r.year), r.title)
        if fy is None:
            continue
        rows.append({"pname": pl[0], "ptype": pl[1], "head": head, "fy": fy, "value": float(r.value), "w": WEIGHT.get(r.method, 1.0),
                     "own": fy == int(r.year), "crank": 0, "method": r.method, "table_id": r.table_id, "title": r.title,
                     "column": r.column, "year": int(r.year), "source_url": r.source_url})
    return rows


def places_measures(cities: set) -> pd.DataFrame:
    """Victims, Dowry Prohibition Act cases and the State-wise police and court rates, chosen per place and year."""
    c = q('SELECT c.table_id, c.section, c.name, c."column", c.value, t.year, t.title, t.method, t.source_url FROM cells c '
          'JOIN tables t USING (table_id) WHERE t.publication = \'cii\' AND c.value IS NOT NULL AND c.value >= 0 AND c."column" ILIKE \'%dowry%\'')
    c = c[~c.title.fillna("").str.contains(NOT_TABLE)]
    c["m"] = [measure_of(col, ti) for col, ti in zip(c["column"], c.title)]
    c = c[c.m.notna()]
    rows = []
    for (kind, meas), g in c.groupby("m"):
        if meas in ("cases", "victims"):
            g = g[g.value == g.value.round()]
        if meas in ("cs_rate", "conv_rate"):
            g = g[g.value <= 100]
        rows += cand_rows(g, f"{kind}_{meas}", cities)
    # tables read from the page images where no scan reading was usable (data/handread, kind 'dowry')
    from pathlib import Path
    from .engine import handread_tables

    for m in handread_tables("dowry"):
        for sec, rws in m.ROWS.items():
            for name, v in rws.items():
                if name.upper().startswith(("TOTAL", "GRAND")) or v[0] is None:
                    continue
                pl = resolve(name, "Cities" if sec == "Cities" else sec, True, m.YEAR)
                if pl and pl[1] != "total" and (pl[1] != "city" or pl[0] in cities):
                    rows.append({"pname": pl[0], "ptype": pl[1], "head": "dpa_cases", "fy": m.YEAR, "value": float(v[0]), "w": 2.0, "own": True,
                                 "crank": 0, "method": "handread", "table_id": f"handread/{Path(m.SOURCE).stem}", "title": f"{m.TITLE} (read from the page image)",
                                 "column": m.CATS[0], "year": m.YEAR, "source_url": ""})
            g = rws.get("GRAND TOTAL")
            if g and g[0] is not None:
                rows.append({"pname": "All India", "ptype": "total", "head": "dpa_cases", "fy": m.YEAR, "value": float(g[0]), "w": 2.0, "own": True,
                             "crank": 0, "method": "handread", "table_id": f"handread/{Path(m.SOURCE).stem}", "title": f"{m.TITLE} (read from the page image)",
                             "column": m.CATS[0], "year": m.YEAR, "source_url": ""})
    d = pick(pd.DataFrame(rows)) if rows else pd.DataFrame()
    return d


STATEMENT = [  # 2004-2012 workbooks, one sheet per crime head: 'STATEMENT OF CASES ... UNDER DOWRY DEATHS ... DURING 2009 | <measure>'
    ("chargesheeted", r"chargesheets were laid|charge.?sheets were laid"),
    ("final_reports", r"final report submitted"),
    ("trials_completed", r"trials were completed"),
    ("convicted", r"^cases convicted"),
    ("acquitted", r"acquitted"),
    ("pending_trial", r"pending trial at the end"),
]


def statements(cities: set) -> pd.DataFrame:
    """State-wise police and court disposal of dowry deaths and Dowry Prohibition Act cases, 2003-2012 (the workbooks)."""
    c = q('SELECT c.table_id, c.section, c.name, c."column", c.value, t.year, t.title, t.method, t.source_url FROM cells c '
          'JOIN tables t USING (table_id) WHERE t.publication = \'cii\' AND c.value IS NOT NULL AND c.value >= 0 '
          'AND (c."column" ILIKE \'statement of cases%dowry%\' OR t.title ILIKE \'statement of cases%dowry%\')')
    rows = []
    for r in c.itertuples(index=False):
        if re.match(r"\s*statement of cases", str(r.column), re.I):
            head, _, lab = str(r.column).partition("|")
        else:                     # the statement is the sheet's title, the column the measure
            head, lab = str(r.title), str(r.column).split("|")[-1]
        kind = "death" if re.search(r"dowry\s*death", head, re.I) else "dpa" if re.search(r"dowry\s*proh", head, re.I) else None
        y = re.search(r"during\s+((?:19|20)\d\d)", head, re.I)
        meas = next((m for m, rx in STATEMENT if re.search(rx, lab.strip(), re.I)), None)
        if not (kind and y and meas) or r.value != round(r.value):
            continue
        pl = place_of(r.name, r.section, r.method, r.year)
        if not pl or (pl[1] == "city" and pl[0] not in cities):
            continue
        fy = int(y.group(1))
        rows.append({"pname": pl[0], "ptype": pl[1], "head": f"{kind}_st_{meas}", "fy": fy, "value": float(r.value), "w": WEIGHT.get(r.method, 1.0),
                     "own": fy == int(r.year), "crank": 0, "method": r.method, "table_id": r.table_id, "title": r.title, "column": r.column,
                     "year": int(r.year), "source_url": r.source_url})
    return pick(pd.DataFrame(rows)) if rows else pd.DataFrame()


def female_population(cities: set) -> dict:
    """NCRB's female population (lakh) by place and year, from its crimes-against-women tables (2012-)."""
    c = q('SELECT c.table_id, c.section, c.name, c."column", c.value, t.year, t.title, t.method, t.source_url FROM cells c '
          'JOIN tables t USING (table_id) WHERE t.publication = \'cii\' AND c.value > 0 AND c."column" ILIKE \'%population%\'')
    # from 2020 the crimes-against-women table heads it just 'Mid-Year Projected Population': still women (Tamil Nadu 2022: 384 lakh)
    women = c.title.fillna("").str.contains(r"against women", case=False)
    c = c[c["column"].str.contains(r"lakh", case=False) & (c["column"].str.contains(r"female", case=False) | women)
          & ~c["column"].str.contains(r"child|senior|male\b(?<!female)", case=False)]
    rows = cand_rows(c, "female_pop", cities)
    if not rows:
        return {}
    d = pick(pd.DataFrame(rows))
    out = defaultdict(dict)
    for r in d.itertuples(index=False):
        out[(r.place, r.ptype)][int(r.year)] = float(r.value)
    return out


def census_female() -> dict:
    """Census of India female population (lakh) for 1991, 2001, 2011 by State (data/external, see its source column)."""
    out = defaultdict(dict)
    if not CENSUS.exists():
        return out
    from ncrb.entities import standardise

    for r in csv.DictReader(CENSUS.open(encoding="utf-8")):
        try:
            v = float(str(r["female_population"]).replace(",", ""))
        except ValueError:
            continue
        name = r["state"].strip()
        if re.search(r"^india$|all.?india", name, re.I):
            key = ("All India", "total")
        else:
            p = standardise(name)
            if p[1] not in ("state", "ut"):
                continue
            key = (p[0], p[1])
        out[key][int(r["census_year"])] = v / 1e5
    return out


# All India, by crime head: (measure, test on the heading's letters only - NCRB's headings break words across
# lines: 'Chargesh eeting Rate', 'Charge- Sheets')
def disposal_measure(col: str) -> str | None:
    k = re.sub(r"[^a-z]", "", col.lower())
    if "persons" in k:
        return None
    if "chargesheetingrate" in k:
        return "ai_cs_rate"
    if "convictionrate" in k:
        return "ai_conv_rate"
    if "percentage" in k or "previous" in k or "prv" in k or "outof" in k:
        return None
    if re.search(r"chargeshe(et|ets)(were|submitted|laid|ed)", k) and "rate" not in k and "total" not in k.split("chargeshe")[0][-12:]:
        return "ai_chargesheeted"
    if "pendinginv" in k and ("end" in k or k.endswith("pendinginvestigation")):
        return "ai_pending_investigation"
    if "acquitted" in k:
        return "ai_acquitted"
    if "convicted" in k and "rate" not in k:
        return "ai_convicted"
    if "pendingtrial" in k and ("end" in k or k.endswith("pendingtrial")):
        return "ai_pending_trial"
    return None


def all_india_disposal() -> pd.DataFrame:
    """Police and court disposal of dowry-death and Dowry Prohibition Act cases, All India, every edition."""
    c = q('SELECT c.table_id, c.name, c."column", c.value, t.year, t.title, t.method, t.source_url FROM cells c JOIN tables t USING (table_id) '
          'WHERE t.publication = \'cii\' AND c.value IS NOT NULL AND c.value >= 0 AND c.name ILIKE \'%dowry%\' '
          'AND (t.title ILIKE \'%disposal%\') AND t.title NOT ILIKE \'%persons%\' AND t.title NOT ILIKE \'%metropolitan%\' AND t.title NOT ILIKE \'%percentage%\'')
    rows = []
    for r in c.itertuples(index=False):
        kind = "death" if re.search(r"dowry\s*death", r.name, re.I) else "dpa" if re.search(r"dowry\s*proh", r.name, re.I) else None
        if not kind:
            continue
        meas = disposal_measure(str(r.column))
        if not meas:
            continue
        if "rate" not in meas and r.value != round(r.value):
            continue
        fy = fig_year(r.column, int(r.year), r.title)
        if fy is None:
            continue
        rows.append({"pname": "All India", "ptype": "total", "head": f"{kind}_{meas}", "fy": fy, "value": float(r.value),
                     "w": WEIGHT.get(r.method, 1.0), "own": fy == int(r.year), "crank": 0, "method": r.method, "table_id": r.table_id,
                     "title": r.title, "column": r.column, "year": int(r.year), "source_url": r.source_url})
    return pick(pd.DataFrame(rows)) if rows else pd.DataFrame()


def main() -> None:
    cities = set(known_cities())
    series = defaultdict(lambda: defaultdict(dict))       # measure -> (place, type) -> {year: value}
    status = defaultdict(lambda: defaultdict(dict))
    srcs = defaultdict(set)
    # dowry deaths, cases: the long series
    ls = pd.read_csv(ROOT / "web" / "data" / "explore" / "cii" / "long-series-provenance.csv")
    for r in ls[ls["head"] == "dowry_deaths"].itertuples(index=False):
        series["death_cases"][(r.place, r.ptype)][int(r.year)] = float(r.value)
        status["death_cases"][(r.place, r.ptype)][int(r.year)] = r.status
    for d in (places_measures(cities), all_india_disposal(), statements(cities)):
        for r in d.itertuples(index=False):
            if r.head == "death_cases":
                continue
            series[r.head][(r.place, r.ptype)][int(r.year)] = float(r.value)
            status[r.head][(r.place, r.ptype)][int(r.year)] = r.status
            srcs[(r.head, int(r.year))].add((re.sub(r"\s+", " ", str(r.title)).strip()[:160], r.url or "", r.method))
    # charge-sheeting and conviction rates NCRB did not print State-wise, worked out from its own counts with its own
    # definitions: charge-sheets over charge-sheets and final reports; convictions over trials completed
    worked = set()
    for kind in ("death", "dpa"):
        cs, fr = series[f"{kind}_st_chargesheeted"], series[f"{kind}_st_final_reports"]
        cv, tc = series[f"{kind}_st_convicted"], series[f"{kind}_st_trials_completed"]
        for key in set(cs) | set(cv):
            for y in cs.get(key, {}):
                if y not in series[f"{kind}_cs_rate"].get(key, {}) and y in fr.get(key, {}) and cs[key][y] + fr[key][y] > 0:
                    series[f"{kind}_cs_rate"][key][y] = round(100 * cs[key][y] / (cs[key][y] + fr[key][y]), 1)
                    worked.add(f"{kind}_cs_rate|{key[0]}|{key[1]}|{y}")
            for y in cv.get(key, {}):
                if y not in series[f"{kind}_conv_rate"].get(key, {}) and tc.get(key, {}).get(y):
                    series[f"{kind}_conv_rate"][key][y] = round(100 * cv[key][y] / tc[key][y], 1)
                    worked.add(f"{kind}_conv_rate|{key[0]}|{key[1]}|{y}")
    # rate per lakh women: NCRB's female population (2012-), else the Census line between 1991, 2001 and 2011
    fem = female_population(cities)
    cen = census_female()
    rate_src = {}
    for key, ys in series["death_cases"].items():
        for y, v in ys.items():
            pop, how = fem.get(key, {}).get(y), "ncrb"
            if pop is None and key in cen:
                cy = cen[key]
                lo = max((c for c in cy if c <= y), default=None)
                hi = min((c for c in cy if c >= y), default=None)
                if lo is not None and hi is not None:
                    pop = cy[lo] if lo == hi else cy[lo] + (cy[hi] - cy[lo]) * (y - lo) / (hi - lo)
                    how = "census"
                elif lo is not None and y - lo <= 1:
                    pop, how = cy[lo], "census"
                elif hi is not None and hi - y <= 1:            # 1990: the 1991 census, a year on
                    pop, how = cy[hi], "census"
            if pop and pop > 0:
                series["death_rate_women"][key][y] = round(v / pop, 2)
                rate_src[(key, y)] = how
    for key, ys in fem.items():
        for y, v in ys.items():
            series["female_pop"][key][y] = v
    # suicides over dowry disputes: the suicide causes dataset (both sexes, all ages)
    sc = ROOT / "web" / "data" / "trends" / "suicide_causes" / "index.json"
    if sc.exists():
        meta = json.loads(sc.read_text())
        ci = meta["cats"].index("Dowry related") if "Dowry related" in meta["cats"] else None
        if ci is not None:
            for p in meta["places"]:
                h = p["head"].get(str(ci)) or {}
                for y, v in h.items():
                    if v is not None:
                        series["suicides_dowry"][(p["name"], p["type"])][int(y)] = float(v)
    # All India suicides over dowry where NCRB printed no All-India figure (2001-2003, data.gov.in): States and UTs added up
    summed = []
    sd = series["suicides_dowry"]
    years_st = defaultdict(list)
    for (pl, ty), ys in sd.items():
        if ty in ("state", "ut"):
            for y, v in ys.items():
                years_st[y].append(v)
    for y, vs in years_st.items():
        if y not in sd.get(("All India", "total"), {}) and len(vs) >= 28:
            sd[("All India", "total")][y] = float(sum(vs))
            summed.append(y)
    # the output: places, measures, and {measure: {place index: [year, value, ...]}}
    places = sorted({k for m in series.values() for k in m}, key=lambda k: ({"total": 0, "state": 1, "ut": 2, "city": 3}.get(k[1], 9), k[0]))
    pi = {k: i for i, k in enumerate(places)}
    data = {}
    for m, by in series.items():
        data[m] = {str(pi[k]): [x for y in sorted(ys) for x in (y, ys[y])] for k, ys in by.items() if ys}
    computed = sorted({f"{pi[k]}.{y}" for (k, y), how in rate_src.items() if how == "census"})
    sources = defaultdict(list)
    for (m, y), ss in srcs.items():
        for t, u, me in sorted(ss)[:4]:
            sources[f"{m}.{y}"].append({"title": t, "url": u, "method": me})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"places": [{"name": k[0], "type": k[1]} for k in places], "data": data,
                               "rate_census": computed, "worked": sorted(worked), "suicides_india_summed": sorted(summed), "sources": sources}, separators=(",", ":")), encoding="utf-8")
    print(f"dowry: {len(places)} places -> {OUT.relative_to(ROOT)}")
    for m in sorted(series):
        ys = sorted({y for v in series[m].values() for y in v})
        n = sum(len(v) for v in series[m].values())
        tn = sorted(series[m].get(("Tamil Nadu", "state"), {}))
        ai = sorted(series[m].get(("All India", "total"), {}))
        print(f"  {m:26} {n:6} figures, {len(series[m]):3} places, {ys[0] if ys else ''}-{ys[-1] if ys else ''}; "
              f"Tamil Nadu {tn[0] if tn else '-'}-{tn[-1] if tn else '-'} ({len(tn)}), All India {ai[0] if ai else '-'}-{ai[-1] if ai else '-'} ({len(ai)})")


if __name__ == "__main__":
    main()
