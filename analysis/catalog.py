"""One catalog of everything the site can chart, for the search box and the Browse page, and the coverage ledger.

- every Explore family (a table joined across editions) with its categories, the years it has and which of them
  were read from scans;
- the Trends datasets and the Dowry dashboard's measures;
- coverage by report and edition: files NCRB lists, files held, tables read, and what became of each table
  (analysis/output/table_ledger.csv, written by analysis.families).

    uv run --extra analysis python -m analysis.catalog      -> web/data/catalog.json
"""

from __future__ import annotations

import csv
import json
import time
from collections import Counter, defaultdict

from .lib import ROOT

WEB = ROOT / "web" / "data"
OUT = WEB / "catalog.json"
TEXT = ("pdf_text", "excel", "word")

DOWRY = [
    ("death_cases", "Dowry deaths (cases registered)", 1990), ("death_rate_women", "Dowry deaths per lakh women", 1990),
    ("death_victims", "Victims of dowry deaths", 2014), ("dpa_cases", "Dowry Prohibition Act cases", 1988),
    ("suicides_dowry", "Suicides over dowry disputes", 1984), ("death_cs_rate", "Charge-sheeting rate, dowry deaths", 2000),
    ("death_conv_rate", "Conviction rate, dowry deaths", 2000),
]


def main() -> None:
    idx = json.loads((WEB / "explore" / "index.json").read_text())
    tables = []
    for f in idx["families"]:
        fam = json.loads((WEB / "explore" / f["pub"] / f"{f['id']}.json").read_text())
        ys = fam["years"]
        sc = sorted(int(y) for y, l in fam["sources"].items() if any(x["method"] not in TEXT for x in l))
        tables.append({"k": "x", "id": f["id"], "pub": f["pub"], "topic": f["topic"], "title": f["title"], "geo": f["geo"] or "india",
                       "ys": ys, "sc": sc, "rows": len(fam["rows"]), "also": f.get("also", [])[:2],
                       "cats": [c["name"] for c in fam["cats"]]})
    # Trends datasets
    cat = json.loads((WEB / "trends" / "catalog.json").read_text())
    for d in cat["datasets"]:
        meta = json.loads((WEB / "trends" / d["id"] / "index.json").read_text())
        ys = sorted({int(y) for p in meta["places"] for h in p["head"].values() for y in h})
        tables.append({"k": "t", "id": d["id"], "pub": "adsi", "topic": "Dashboards: crashes and suicides", "title": d["title"], "geo": "state",
                       "ys": ys, "sc": [], "rows": len(meta["places"]), "also": [], "cats": meta["cats"]})
    dj = WEB / "dowry" / "dowry.json"
    if dj.exists():
        D = json.loads(dj.read_text())
        for m, lab, y0 in DOWRY:
            ys = sorted({a[i] for a in D["data"].get(m, {}).values() for i in range(0, len(a), 2)})
            tables.append({"k": "d", "id": m, "pub": "cii", "topic": "Dashboards: dowry", "title": lab, "geo": "state", "ys": ys, "sc": [],
                           "rows": len(D["data"].get(m, {})), "also": [], "cats": []})
    # coverage by report and edition
    files = list(csv.DictReader((ROOT / "catalog" / "files.csv").open(encoding="utf-8")))
    fidx = {r["source_file"]: r for r in csv.DictReader((ROOT / "data" / "files_index.csv").open(encoding="utf-8"))}
    cov = defaultdict(lambda: defaultdict(Counter))
    for f in files:
        c = cov[f["publication"]][int(f["year"])]
        c["files"] += 1
        r = fidx.get(f["path"])
        if f.get("status") not in ("ok", "", None) or not (ROOT / f["path"]).exists():
            c["not_served"] += 1          # NCRB's site lists it but does not serve it
        elif r and int(r.get("tables") or 0) > 0:
            c["with_tables"] += 1
            if int(r.get("pages_without_text") or 0) > 0:
                c["scanned"] += 1
    led = ROOT / "analysis" / "output" / "table_ledger.csv"
    status = Counter()
    if led.exists():
        for r in csv.DictReader(led.open(encoding="utf-8")):
            c = cov[r["publication"]][int(r["year"])]
            c["tables"] += 1
            s = r["status"]
            key = ("joined" if s in ("in a family", "another printing of a year in a family", "reprint of a table of the same year")
                   else "district" if s.startswith("district") else "single")
            c[key] += 1
            status[s] += 1
    coverage = {p: {str(y): dict(c) for y, c in sorted(ys.items())} for p, ys in cov.items()}
    OUT.write_text(json.dumps({"built": time.strftime("%Y-%m-%d"), "reports": idx["reports"], "tables": tables, "coverage": coverage,
                               "ledger": dict(status)}, separators=(",", ":")), encoding="utf-8")
    n_ind = sum(max(1, len(t["cats"])) for t in tables)
    print(f"catalog: {len(tables)} tables and dashboards, {n_ind} indicators, {OUT.stat().st_size / 1e6:.1f} MB; ledger {dict(status.most_common(4))}")


if __name__ == "__main__":
    main()
