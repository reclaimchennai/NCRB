"""The population NCRB used, by place and year, so any count can be shown per lakh people.

NCRB prints an estimated or projected mid-year population (in lakhs, thousands or millions) beside its rates in
Crime in India and ADSI. Every such printed figure is collected, converted to lakhs, and one figure is chosen per
place and year: text-layer figures first, then the value most printings agree on, and a scanned figure only when it
sits within a fifth of the years around it. Populations of groups (women, children, senior citizens, SCs, STs) are
left out. Cities keep the population NCRB printed for them (often a census figure, used for several years).

    uv run --extra vlm --extra analysis python -m analysis.population   -> web/data/explore/population.json
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from statistics import median

from .engine import known_cities, resolve
from .lib import ROOT, SCANNED, q

OUT = ROOT / "web" / "data" / "explore" / "population.json"
POP = re.compile(r"population", re.I)
GROUP = re.compile(r"female|male|women|girl|child|juvenil|senior|elder|s\.?\s?c\b|s\.?\s?t\b|scheduled|caste|tribe|urban|rural|"
                   r"rate|per\s*(lakh|100|1,?00,?000|one)|percent|%|share|volume|incidence|variation|growth|density|census\s+20\d\d\s*\(|"
                   r"inmate|prison|police|jail|vehicle|literacy|area", re.I)
UNIT = [(re.compile(r"million", re.I), 10.0), (re.compile(r"thousand|'?000'?|\(000\)", re.I), 0.01), (re.compile(r"lakh", re.I), 1.0)]


def unit_of(col: str) -> float | None:
    for rx, f in UNIT:
        if rx.search(col):
            return f
    return None


def main() -> None:
    t = q("SELECT table_id, publication, year, method FROM tables WHERE n_cells > 0")
    c = q('SELECT c.table_id, c.section, c.name, c."column", c.value FROM cells c WHERE c."column" ILIKE \'%population%\' '
          'AND c.value IS NOT NULL AND c.value > 0')
    c = c.merge(t, on="table_id")
    c = c[c["column"].map(lambda s: bool(POP.search(s)) and not GROUP.search(s))]
    c["unit"] = c["column"].map(unit_of)
    c = c[c.unit.notna()]
    cities = set(known_cities())
    cand = defaultdict(list)        # (place, type, year) -> [(lakhs, text?)]
    for r in c.itertuples(index=False):
        ys = re.findall(r"(?<!\d)(19[5-9]\d|20[0-2]\d)(?!\d)", r.column)
        y = int(ys[0]) if len(set(ys)) == 1 else int(r.year)
        if not (int(r.year) - 1 <= y <= int(r.year)):
            continue
        p = resolve(str(r.name or ""), str(r.section or ""), r.method in SCANNED, int(r.year))
        if not p or (p[1] == "city" and p[0] not in cities):
            continue
        v = float(r.value) * r.unit
        if not (0.05 <= v <= 20000):             # Lakshadweep ~0.7 lakh .. India ~14,500 lakh
            continue
        cand[(p[0], p[1], y)].append((round(v, 2), r.method not in SCANNED))
    # one figure per place and year
    chosen = defaultdict(dict)
    for (pl, ty, y), vs in cand.items():
        groups = defaultdict(list)
        for v, txt in vs:
            k = next((g for g in groups if abs(g - v) <= max(0.05, 0.01 * g)), v)
            groups[k].append(txt)
        best = max(groups, key=lambda g: (any(groups[g]), len(groups[g])))
        chosen[(pl, ty)][y] = (best, any(groups[best]))
    # scanned figures must sit within a fifth of the median of their neighbours (and the neighbours' own scale)
    out, n_drop = {}, 0
    for (pl, ty), ys in chosen.items():
        keep = {}
        for y, (v, txt) in ys.items():
            near = [ys[x][0] for x in ys if x != y and abs(x - y) <= 4]
            if not txt and (len(near) < 2 or not 0.8 <= v / median(near) <= 1.25):
                n_drop += 1
                continue
            keep[str(y)] = v
        if keep:
            out[f"{pl}|{ty}"] = dict(sorted(keep.items()))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"unit": "lakh", "note": "NCRB's estimated or projected mid-year population, as printed beside its rates",
                               "places": out}, separators=(",", ":")), encoding="utf-8")
    n = sum(len(v) for v in out.values())
    print(f"population: {n} place-years for {len(out)} places ({n_drop} scanned figures left out)")
    for k in ("Tamil Nadu|state", "Chennai|city", "All India|total"):
        v = out.get(k, {})
        print(f"  {k}: {len(v)} years, {min(v) if v else ''}-{max(v) if v else ''}; " + ", ".join(f"{y}: {v[y]}" for y in list(v)[::8]))


if __name__ == "__main__":
    main()
