"""Write the trends dashboard's data: web/data/trends/<dataset>/{index.json, <place>.json}.

    uv run --extra analysis --extra vlm python -m analysis.export

index.json holds what the controls and the ranking views need: the places
with the years each has, the category, sex, age and group lists, and every
place's yearly figures for both sexes and all ages. <place>.json holds that
place's full breakdown, as rows [year, group, cat, sex, age, value].

Also writes analysis/output/trends_<dataset>.csv.gz with every record and its
source, for anyone who would rather not read JSON.
"""

from __future__ import annotations

import json
import re
import time

import pandas as pd

from .engine import DATASETS, OK, POS_CHECK
from .harmonise import AGE_ORDER
from .lib import OUT, ROOT

WEB = ROOT / "web" / "data" / "trends"
SEX_ORDER = ["Total", "Male", "Female", "Transgender"]
PTYPE_ORDER = {"total": 0, "state": 1, "ut": 2, "city": 3}


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def clean(d: pd.DataFrame) -> pd.DataFrame:
    """Records that passed their checks; numbers as plain ints where they are counts."""
    d = d[d["check"].isin(OK) | d["check"].isin(["no total", "ok (adds up to the grand total)", "computed", POS_CHECK])].copy()
    d = d[d["value"].notna()]
    # where the figure comes from, for the credit line: NCRB's own tables however they were read, the two others, or
    # worked out here (a rate from NCRB's count and population, where NCRB printed none)
    d["source"] = d["source"].where(d["source"].isin(["ogd", "odc", "computed"]), "ncrb")
    d["year"] = d["year"].astype(int)
    for c in ("group", "cat", "sex", "age"):
        d[c] = d[c].fillna("").astype(str)
    return d.drop_duplicates(["year", "place", "ptype", "group", "cat", "sex", "age"])


def num(v):
    return int(v) if float(v).is_integer() else round(float(v), 2)


def write(name: str, spec: dict, d: pd.DataFrame) -> dict:
    out = WEB / name
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.json"):
        f.unlink()
    cats = spec.get("cats") or (d.groupby("cat").value.sum().sort_values(ascending=False).index.tolist())
    cats = [c for c in cats if c in set(d.cat)] + sorted(set(d.cat) - set(cats))
    groups = [g for g in spec.get("groups", [""]) if g in set(d.group)] or [""]
    sexes = [s for s in SEX_ORDER if s in set(d.sex)] or [""]
    ages = [a for a in AGE_ORDER if a in set(d.age)] or [""]
    places = []
    for (place, ptype), g in sorted(d.groupby(["place", "ptype"]), key=lambda kv: (PTYPE_ORDER.get(kv[0][1], 9), kv[0][0])):
        key = slug(f"{ptype}-{place}")
        rows = g.sort_values(["year", "group", "cat", "sex", "age"])
        (out / f"{key}.json").write_text(json.dumps({
            "place": place, "type": ptype,
            "rows": [[int(r.year), groups.index(r.group) if r.group in groups else 0, cats.index(r.cat), sexes.index(r.sex) if r.sex in sexes else 0,
                      ages.index(r.age) if r.age in ages else 0, num(r.value)] for r in rows.itertuples()],
            "sources": {str(y): sorted(set(x.source)) for y, x in g.groupby("year")},
        }, separators=(",", ":")), encoding="utf-8")
        # headline figures for the ranking and map views: first group, both sexes, all ages
        head_age = "all ages" if "all ages" in ages else ages[0]
        head = g[(g.group == groups[0]) & (g.sex == sexes[0]) & (g.age == head_age)]
        series = {}
        for cat, x in head.groupby("cat"):
            series[cats.index(cat)] = {int(y): num(v) for y, v in zip(x.year, x.value)}
        places.append({"key": key, "name": place, "type": ptype, "years": sorted(int(y) for y in g.year.unique()), "head": series})
    from .engine import PROV

    tables = {}
    for t in spec.get("topics", []):
        pv = PROV.get(t)
        if pv is None:
            continue
        for r in pv.itertuples():
            lst = tables.setdefault(str(int(r.year)), [])
            if not any(x["title"] == r.title for x in lst):
                lst.append({"title": re.sub(r"\s+", " ", str(r.title)).strip()[:200], "url": r.source_url})
    meta = {
        "id": name, "title": spec["title"], "unit": spec["unit"],
        "tables": tables,
        "year_sources": {str(y): sorted(set(x.source)) for y, x in d.groupby("year")},
        "cats": cats, "groups": groups, "sexes": sexes, "ages": ages,
        "years": sorted(int(y) for y in d.year.unique()),
        "sources": sorted(set(d.source)),
        "places": places,
        "built": time.strftime("%Y-%m-%d"),
    }
    (out / "index.json").write_text(json.dumps(meta, separators=(",", ":")), encoding="utf-8")
    d.to_csv(OUT / f"trends_{name}.csv.gz", index=False, compression="gzip")
    return {"id": name, "title": spec["title"], "unit": spec["unit"], "years": [meta["years"][0], meta["years"][-1]],
            "places": len(places), "records": len(d)}


def main(only: list[str] | None = None) -> None:
    WEB.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    catalog_path = WEB / "catalog.json"
    catalog = {c["id"]: c for c in json.loads(catalog_path.read_text())["datasets"]} if catalog_path.exists() else {}
    for name, spec in DATASETS.items():
        if only and name not in only:
            continue
        t = time.time()
        d = clean(spec["build"]())
        catalog[name] = write(name, spec, d)
        print(f"  {name}: {len(d):,} records, {catalog[name]['places']} places, {catalog[name]['years']} ({time.time() - t:.0f}s)")
    order = list(DATASETS)
    catalog_path.write_text(json.dumps({"datasets": [catalog[k] for k in order if k in catalog], "built": time.strftime("%Y-%m-%d")},
                                       separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    import sys

    main(sys.argv[1:] or None)
