"""Every missing year on the site: for each trend dataset and long series, each place's years with no figure between
its first and last year. Writes analysis/output/gaps.csv and prints a summary (Tamil Nadu and Chennai first).

    python3 scripts/gap_report.py [--all]
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRENDS = ROOT / "web" / "data" / "trends"
LONG = ROOT / "web" / "data" / "explore" / "adsi" / "long-series-provenance.csv"
LONG_CII = ROOT / "web" / "data" / "explore" / "cii" / "long-series-provenance.csv"
OUT = ROOT / "analysis" / "output" / "gaps.csv"


def runs(ys):
    out, s, p = [], ys[0], ys[0]
    for y in ys[1:] + [None]:
        if y == p + 1:
            p = y
            continue
        out.append(f"{s}" if s == p else f"{s}-{p}")
        s = p = y
    return ", ".join(out)


def main():
    rows = []
    for ds in sorted(p.name for p in TRENDS.iterdir() if p.is_dir()):
        idx = json.loads((TRENDS / ds / "index.json").read_text())
        for pl in idx["places"]:
            f = TRENDS / ds / f"{pl['key']}.json"
            if not f.exists():
                continue
            ys = sorted({r[0] for r in json.loads(f.read_text())["rows"]})
            if not ys:
                continue
            miss = [y for y in range(ys[0], ys[-1] + 1) if y not in ys]
            rows.append({"source": f"trends/{ds}", "place": pl["name"], "type": pl["type"], "first": ys[0], "last": ys[-1], "missing": miss})
    for path, pub in ((LONG, "adsi"), (LONG_CII, "cii")):
        if not path.exists():
            continue
        by = defaultdict(set)
        for r in csv.DictReader(path.open()):
            by[(r["head"], r["place"], r["ptype"])].add(int(r["year"]))
        for (h, p, t), ys in by.items():
            ys = sorted(ys)
            miss = [y for y in range(ys[0], ys[-1] + 1) if y not in ys]
            rows.append({"source": f"long/{pub}/{h}", "place": p, "type": t, "first": ys[0], "last": ys[-1], "missing": miss})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["source", "place", "type", "first", "last", "n_missing", "missing"])
        for r in rows:
            w.writerow([r["source"], r["place"], r["type"], r["first"], r["last"], len(r["missing"]), runs(r["missing"]) if r["missing"] else ""])
    gaps = [r for r in rows if r["missing"]]
    print(f"{len(rows)} series, {len(gaps)} with missing years, {sum(len(r['missing']) for r in gaps)} missing place-years -> {OUT.relative_to(ROOT)}")
    focus = [r for r in gaps if r["place"] in ("Tamil Nadu", "Chennai")]
    for r in sorted(focus, key=lambda r: (r["place"], r["source"])):
        print(f"  {r['place']:10} {r['source']:32} {r['first']}-{r['last']}  missing {runs(r['missing'])}")
    if "--all" in sys.argv:
        for r in sorted(gaps, key=lambda r: -len(r["missing"])):
            print(f"  {r['place']:22} {r['source']:32} {r['first']}-{r['last']}  missing {runs(r['missing'])}")
    by_src = defaultdict(lambda: [0, 0])
    for r in gaps:
        by_src[r["source"]][0] += 1
        by_src[r["source"]][1] += len(r["missing"])
    print("by source (series with gaps, missing place-years):")
    for s, (n, m) in sorted(by_src.items(), key=lambda x: -x[1][1]):
        print(f"  {s:34} {n:4} {m:6}")


if __name__ == "__main__":
    main()
