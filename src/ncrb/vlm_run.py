"""Run the OCR model over scanned pages, filling the page cache.

Long-running and resumable: every finished page is written to
``data/ocr_cache`` at once, and pages already there are skipped. Stop it at
any time; run it again to continue. Afterwards ``ncrb.extract --vlm`` turns
the cached pages into tables.

Usage:
    uv run --extra vlm python -m ncrb.vlm_run                  # all scanned table pages, in priority order
    uv run --extra vlm python -m ncrb.vlm_run --files bench/pages.json
    uv run --extra vlm python -m ncrb.vlm_run --limit 200 --pub cii
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

import pymupdf as fitz

from .crawl import ROOT
from .extract import FILE_INDEX, INDEX
from .vlm import DEFAULT_MODEL
from .vlm_tables import cache_path, file_sha, read_page, scanned_pages

# individual tables first, then chapters, then whole volumes (which repeat the tables)
LISTING_ORDER = {"table_content": 0, "additional_table": 0, "table_chapter": 1, "year_wise": 2}


_scanned: dict[str, list[int]] = {}


def scanned_pages_cached(doc, path) -> list[int]:
    key = str(path)
    if key not in _scanned:
        _scanned[key] = scanned_pages(doc)
    return _scanned[key]


def priority_files(pub: str | None) -> list[str]:
    """Scanned source files, the ones whose current tables fail the totals check first."""
    files = [r for r in csv.DictReader(FILE_INDEX.open(encoding="utf-8")) if int(r["pages_ocr"] or 0) > 0]
    if pub:
        files = [r for r in files if r["publication"] == pub]
    score: dict[str, tuple[int, int]] = {}
    for t in csv.DictReader(INDEX.open(encoding="utf-8")):
        a, b = score.get(t["source_file"], (0, 0))
        score[t["source_file"]] = (a + int(t["checks_passed"] or 0), b + int(t["checks_total"] or 0))

    def key(r):
        # most failed totals per page first: the biggest gain for the model's time
        passed, total = score.get(r["source_file"], (0, 0))
        failing = (total - passed) / max(1, int(r["pages_ocr"] or 1))
        return (LISTING_ORDER.get(r["listing"], 3), -failing, int(r["pages_ocr"] or 0), -int(r["year"]))

    return [r["source_file"] for r in sorted(files, key=key)]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--files", help="JSON list of {source_file} to do, instead of the priority order")
    ap.add_argument("--pages", help="JSON list of {source_file, pages: [first, last]}: only those pages")
    ap.add_argument("--pub", choices=["cii", "psi", "adsi"])
    ap.add_argument("--listing", help="only files from this listing")
    ap.add_argument("--limit", type=int, help="stop after this many pages")
    args = ap.parse_args()

    if args.pages:
        # specific pages: [{"source_file": ..., "pages": [first, last]}, ...]
        done = 0
        for item in json.load(open(args.pages)):
            path = ROOT / item["source_file"]
            doc = fitz.open(path)
            sha = file_sha(path)
            first, last = item.get("pages", [1, len(doc)])
            for p in range(first, min(last, len(doc)) + 1):
                if p not in scanned_pages_cached(doc, path) or cache_path(args.model, sha, p).exists():
                    continue
                t = time.time()
                read_page(doc, p, sha, args.model)
                done += 1
                print(f"[{done}] {item['source_file']} p{p} {time.time() - t:.0f}s", flush=True)
            doc.close()
        return
    if args.files:
        todo = list(dict.fromkeys(x["source_file"] for x in json.load(open(args.files))))
    else:
        todo = priority_files(args.pub)
        if args.listing:
            listing = {r["source_file"]: r["listing"] for r in csv.DictReader(FILE_INDEX.open(encoding="utf-8"))}
            todo = [f for f in todo if listing.get(f) == args.listing]

    done = 0
    t0 = time.time()
    for rel in todo:
        path = ROOT / rel
        doc = fitz.open(path)
        sha = file_sha(path)
        for p in scanned_pages(doc):
            if cache_path(args.model, sha, p).exists():
                continue
            t = time.time()
            read_page(doc, p, sha, args.model)
            done += 1
            rate = (time.time() - t0) / done
            print(f"[{done}] {rel} p{p} {time.time() - t:.0f}s (avg {rate:.0f}s/page)", flush=True)
            if args.limit and done >= args.limit:
                return
        doc.close()


if __name__ == "__main__":
    main()
