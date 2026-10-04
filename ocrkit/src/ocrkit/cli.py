"""ocrkit command line.

    ocrkit manifest FILES... --out work/ [--all-pages] [--urls list.csv] [--parts-base URL]
    ocrkit fetch ZIPS_OR_FOLDERS... --cache data/ocr_cache
    ocrkit score --cache data/ocr_cache --manifest work/manifest.json      # compare readings already fetched
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(prog="ocrkit")
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("manifest", help="list the pages to read (and bundle files that are not online)")
    m.add_argument("files", nargs="*")
    m.add_argument("--urls", help="CSV with url,path columns: files the GPU machine downloads itself")
    m.add_argument("--out", required=True)
    m.add_argument("--all-pages", action="store_true")
    m.add_argument("--bench-files", type=int, default=150)
    m.add_argument("--parts-base", help="URL the bundle tars will be served from (e.g. a GitHub release download URL)")
    f = sub.add_parser("fetch", help="import readings from zips or folders")
    f.add_argument("sources", nargs="+")
    f.add_argument("--cache", required=True)
    f.add_argument("--overwrite", action="store_true")
    s = sub.add_parser("score", help="sums matched per reading, on the files every reading covers")
    s.add_argument("--cache", required=True)
    s.add_argument("--manifest", required=True)
    a = ap.parse_args()

    if a.cmd == "manifest":
        from .manifest import build, from_csv

        srcs = [(Path(x), None) for x in a.files] + (from_csv(Path(a.urls)) if a.urls else [])
        man = build(srcs, Path(a.out), every_page=a.all_pages, bench_files=a.bench_files, parts_base=a.parts_base)
        n = sum(len(x["pages"]) for x in man["files"])
        print(f"{len(man['files'])} files, {n} pages ({sum(1 for x in man['files'] if x['url'])} fetched by URL); "
              f"bundle parts: {man['parts'] or 'none'}; bake-off sample: {sum(1 for x in man['files'] if x['bench'])} files")
    elif a.cmd == "fetch":
        from .fetch import fetch

        print(fetch(a.sources, a.cache, a.overwrite))
    elif a.cmd == "score":
        from .score import consistency

        files = json.loads(Path(a.manifest).read_text())["files"]
        cache = Path(a.cache)
        models = [p.name for p in cache.iterdir() if p.is_dir()]
        def texts(mdl, f):
            ps = [cache / mdl / f["id"] / f"{p:04d}.txt" for p in f["pages"]]
            return {p: x.read_text(encoding="utf-8") for p, x in zip(f["pages"], ps)} if all(x.exists() for x in ps) else None
        common = [f for f in files if all(texts(mm, f) is not None for mm in models)]
        for mm in models:
            mt = ck = 0
            for f in common:
                x, y = consistency(texts(mm, f))
                mt, ck = mt + x, ck + y
            print(f"{mm:32} {mt}/{ck} sums ({mt / ck:.1%})" if ck else f"{mm:32} nothing to check", f"on {len(common)} files")


if __name__ == "__main__":
    main()
