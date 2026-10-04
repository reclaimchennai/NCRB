"""Bring OCR output made on a cloud GPU (colab/NCRB_OCR.ipynb) into the page cache.

The zip holds ``<model slug>/<sha16>/<page>.txt``, the same layout as
``data/ocr_cache``. Pages already in the cache are kept unless --overwrite.

    uv run python -m ncrb.vlm_import ~/Downloads/TeleOCR.zip
    uv run python -m ncrb.extract --scanned --vlm-ready --force    # re-read the scanned files
"""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path

from .vlm_tables import CACHE

# <model>/<sha16>/<page>.txt, under any folders (a Drive folder download wraps it in round2/ ...)
PAGE = re.compile(r"(?:^|/)(?P<model>[A-Za-z0-9.\-]+)/(?P<sha>[0-9a-f]{16})/(?P<page>\d{4})\.txt$")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("src", help="zip file or folder from the Colab run")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()
    src = Path(args.src).expanduser()
    added = kept = 0
    models: dict[str, int] = {}

    def put(rel: str, data: bytes):
        nonlocal added, kept
        m = PAGE.search(rel)
        if not m:
            return
        rel = f"{m['model']}/{m['sha']}/{m['page']}.txt"
        dst = CACHE / rel
        if dst.exists() and not args.overwrite:
            kept += 1
            return
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        added += 1
        models[m["model"]] = models.get(m["model"], 0) + 1

    if src.is_dir():
        for p in src.rglob("*.txt"):
            put(p.relative_to(src).as_posix(), p.read_bytes())
    else:
        with zipfile.ZipFile(src) as z:
            for name in z.namelist():
                if name.endswith(".txt"):
                    put(name, z.read(name))
                elif name.endswith("leaderboard.json"):
                    print("bake-off:", json.dumps(json.loads(z.read(name)), indent=1))
    print(f"{added} pages added ({', '.join(f'{k}: {v}' for k, v in models.items()) or 'none'}), {kept} already in the cache")
    print("next: uv run python -m ncrb.extract --scanned --vlm-ready --force && uv run python -m ncrb.build && uv run python -m ncrb.webdata")


if __name__ == "__main__":
    main()
