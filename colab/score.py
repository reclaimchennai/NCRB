"""Rank OCR models by how well their tables add up to NCRB's own printed totals.

NCRB tables print row and column totals. A model that misreads a figure breaks
a total, so the share of totals that match is an accuracy measure that needs no
hand-typed answer key. Only files every compared model has fully read count,
so the comparison is on the same pages.

    python colab/score.py --cache /content/drive/MyDrive/ncrb_ocr/ocr_cache --bench
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from ncrb.vlm_tables import score_tables, tables_from_texts  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/content/drive/MyDrive/ncrb_ocr/ocr_cache")
    ap.add_argument("--bundle", default="/content/ocr_pages")
    ap.add_argument("--bench", action="store_true")
    ap.add_argument("--models", nargs="*", help="model slugs (folders under --cache); default: all")
    args = ap.parse_args()

    files = json.loads((Path(args.bundle) / "manifest.json").read_text())["files"]
    if args.bench:
        files = [f for f in files if f.get("bench")]
    cache = Path(args.cache)
    models = args.models or sorted(p.name for p in cache.iterdir() if p.is_dir())

    def texts(model, f):
        d = cache / model / f["sha16"]
        paths = [d / f"{p:04d}.txt" for p in f["pages"]]
        if not all(p.exists() for p in paths):
            return None
        return {p: path.read_text(encoding="utf-8") for p, path in zip(f["pages"], paths)}

    common = [f for f in files if all(texts(m, f) is not None for m in models)]
    rows = []
    for m in models:
        passed = checked = tables = 0
        for f in common:
            t = tables_from_texts(texts(m, f))
            a, b, _ = score_tables(t)
            passed, checked, tables = passed + a, checked + b, tables + len(t)
        rows.append({"model": m, "files": len(common), "tables": tables, "totals_checked": checked, "totals_matched": passed,
                     "share": round(passed / checked, 4) if checked else 0.0, "score": passed - 2 * (checked - passed)})
    rows.sort(key=lambda r: -r["score"])
    print(f"{len(common)} files read by all of: {', '.join(models)}\n")
    print(f"{'model':32} {'tables':>7} {'totals checked':>15} {'matched':>8} {'share':>7}")
    for r in rows:
        print(f"{r['model']:32} {r['tables']:>7} {r['totals_checked']:>15} {r['totals_matched']:>8} {r['share']:>7.1%}")
    (cache / "leaderboard.json").write_text(json.dumps(rows, indent=1))
    if rows:
        print(f"\nbest: {rows[0]['model']}")


if __name__ == "__main__":
    main()
