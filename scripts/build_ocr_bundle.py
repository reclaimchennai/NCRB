"""Pack every scanned page into a bundle for the cloud OCR run (colab/).

The source PDFs are 9 GB; only 11,656 of their pages are scans. This writes one
small PDF per source file holding just its scanned pages, a manifest that maps
them back to the original file (SHA-256 and page numbers, which is how the page
cache is keyed), and tars of at most ~1.9 GB for a GitHub release.

    uv run python scripts/build_ocr_bundle.py            # -> data/ocr_bundle/
    uv run python scripts/build_ocr_bundle.py --publish  # also upload as release ocr-pages
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import tarfile
from collections import defaultdict
from pathlib import Path

import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ncrb.vlm_tables import file_sha, scanned_pages  # noqa: E402

OUT = ROOT / "data" / "ocr_bundle"
PART_BYTES = 1_900_000_000
LISTING_ORDER = {"table_content": 0, "additional_table": 0, "table_chapter": 1, "year_wise": 2}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--publish", action="store_true", help="upload the tars and manifest as GitHub release 'ocr-pages'")
    args = ap.parse_args()
    (OUT / "pages").mkdir(parents=True, exist_ok=True)

    files = [r for r in csv.DictReader((ROOT / "data" / "files_index.csv").open(encoding="utf-8")) if int(float(r["pages_ocr"] or 0)) > 0]
    checks = defaultdict(lambda: [0, 0])
    for t in csv.DictReader((ROOT / "data" / "tables_index.csv").open(encoding="utf-8")):
        c = checks[t["source_file"]]
        c[0] += int(t["checks_passed"] or 0)
        c[1] += int(t["checks_total"] or 0)

    manifest = []
    for i, r in enumerate(files, 1):
        src = ROOT / r["source_file"]
        if not src.exists():
            print("missing", r["source_file"])
            continue
        doc = fitz.open(src)
        pages = scanned_pages(doc)
        if not pages:
            doc.close()
            continue
        sha = file_sha(src)
        dst = OUT / "pages" / f"{sha[:16]}.pdf"
        if not dst.exists():
            sub = fitz.open()
            for p in pages:
                sub.insert_pdf(doc, from_page=p - 1, to_page=p - 1)
            sub.save(dst, garbage=4, deflate=True)
            sub.close()
        doc.close()
        passed, total = checks[r["source_file"]]
        manifest.append({
            "sha16": sha[:16], "sha": sha, "source_file": r["source_file"], "publication": r["publication"],
            "year": int(r["year"]), "listing": r["listing"], "pages": pages,
            "checks": [passed, total], "bytes": dst.stat().st_size,
        })
        if i % 200 == 0:
            print(f"{i}/{len(files)} files", flush=True)

    # order: individual tables first, then the files whose totals fail most per page
    def key(m):
        failing = (m["checks"][1] - m["checks"][0]) / len(m["pages"])
        return (LISTING_ORDER.get(m["listing"], 3), -failing, len(m["pages"]), -m["year"])

    manifest.sort(key=key)
    for n, m in enumerate(manifest):
        m["order"] = n
    # a bake-off sample: small individual-table files whose totals can be checked, spread over reports and decades
    picked, per = [], defaultdict(int)
    # up to 8 small files per report and decade: individual-table files first, then chapter/volume files where a
    # decade has none (the 1950s-60s); the totals each model's reading finds are what is scored
    for pref in (("table_content", "additional_table"), ("table_chapter", "year_wise")):
        for m in sorted(manifest, key=lambda m: (m["year"] % 7, m["sha16"])):
            k = (m["publication"], m["year"] // 10)
            if m["listing"] in pref and len(m["pages"]) <= 4 and per[k] < 8 and m["sha16"] not in picked:
                per[k] += 1
                picked.append(m["sha16"])
    for m in manifest:
        m["bench"] = m["sha16"] in picked

    # tars of at most PART_BYTES
    parts, cur, size = [], [], 0
    for m in manifest:
        if cur and size + m["bytes"] > PART_BYTES:
            parts.append(cur)
            cur, size = [], 0
        cur.append(m)
        size += m["bytes"]
    if cur:
        parts.append(cur)
    names = []
    for k, part in enumerate(parts, 1):
        name = f"ncrb-ocr-pages-{k}.tar"
        names.append(name)
        for m in part:
            m["part"] = name
        with tarfile.open(OUT / name, "w") as tar:
            for m in part:
                tar.add(OUT / "pages" / f"{m['sha16']}.pdf", arcname=f"pages/{m['sha16']}.pdf")
    (OUT / "manifest.json").write_text(json.dumps({"files": manifest, "parts": names}, separators=(",", ":")), encoding="utf-8")
    pages = sum(len(m["pages"]) for m in manifest)
    bench = sum(len(m["pages"]) for m in manifest if m["bench"])
    print(f"{len(manifest)} files, {pages} scanned pages ({bench} in the bake-off sample), {len(names)} tars, "
          f"{sum(m['bytes'] for m in manifest) / 1e9:.2f} GB")

    if args.publish:
        tag = "ocr-pages"
        notes = ("Every scanned page of the NCRB source PDFs (one PDF per source file, scanned pages only) and "
                 "manifest.json mapping them to the original file's SHA-256 and page numbers. Input for colab/NCRB_OCR.ipynb.")
        exists = subprocess.run(["gh", "release", "view", tag], cwd=ROOT, capture_output=True).returncode == 0
        if not exists:
            subprocess.run(["gh", "release", "create", tag, "--title", "Scanned pages for cloud OCR", "--notes", notes], cwd=ROOT, check=True)
        subprocess.run(["gh", "release", "upload", tag, "--clobber", str(OUT / "manifest.json"), *[str(OUT / n) for n in names]], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
