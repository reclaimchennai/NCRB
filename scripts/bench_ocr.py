"""Compare OCR engines on the benchmark pages by the totals check.

For every file in bench/pages.json whose pages are all in the VLM cache, the
VLM tables are assembled and checked, and set against the current
(Tesseract-based) tables for the same file. Prints per file and overall.

    uv run --extra vlm python scripts/bench_ocr.py [--model mlx-community/GLM-OCR-bf16]
"""
import argparse
import csv
import json
from pathlib import Path

import pymupdf as fitz

from ncrb.assemble import check_totals
from ncrb.crawl import ROOT
from ncrb.vlm import DEFAULT_MODEL
from ncrb.vlm_tables import cache_path, file_sha, scanned_pages, vlm_tables

ap = argparse.ArgumentParser()
ap.add_argument("--model", default=DEFAULT_MODEL)
args = ap.parse_args()

index = list(csv.DictReader((ROOT / "data/tables_index.csv").open()))
tot = {"tess": [0, 0], "vlm": [0, 0]}
for item in json.load(open(ROOT / "bench/pages.json")):
    path = ROOT / item["source_file"]
    doc = fitz.open(path)
    sha = file_sha(path)
    if not all(cache_path(args.model, sha, p).exists() for p in scanned_pages(doc)):
        continue
    tess = [r for r in index if r["source_file"] == item["source_file"]]
    tp, tt = sum(int(r["checks_passed"]) for r in tess), sum(int(r["checks_total"]) for r in tess)
    tables, _ = vlm_tables(path, args.model, run_model=False)
    vp = vt = 0
    for t in tables:
        c = check_totals(t)
        vp += c["cells_passed"]; vt += c["cells_checked"]
    tot["tess"][0] += tp; tot["tess"][1] += tt; tot["vlm"][0] += vp; tot["vlm"][1] += vt
    print(f"{item['source_file'][4:60]:56}  tesseract {tp:>4}/{tt:<4}  vlm {vp:>4}/{vt:<4}  tables {len(tess)}->{len(tables)}")
for k, (p, t) in tot.items():
    print(f"{k:10} {p}/{t}  {100 * p / max(1, t):.1f}% of checked totals match")
