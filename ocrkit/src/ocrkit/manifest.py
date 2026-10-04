"""Which pages to read: a manifest of files, each with its pages and where the GPU machine gets it.

Two ways for the GPU machine to get a file, chosen per file:
  url     a public address; the machine downloads it itself (checked by SHA-256). Fastest: nothing to upload
          from your computer. Use it whenever the sources are on the open web.
  bundle  for files that are not online (or sites that block cloud machines): the pages are cut into small
          PDFs and packed into tars of at most ~1.9 GB (a GitHub release asset limit) that you host anywhere.

    ocrkit manifest *.pdf --out work/                       # scanned pages of local files, bundled
    ocrkit manifest --urls list.csv --out work/             # url,path (path: a local copy, to find the pages)
    ocrkit manifest ... --all-pages                         # every page, not only those without a text layer

manifest.json: {"files": [{"id", "source", "url"?, "sha256", "pages": [...], "part"?, "order", "bench"}],
                "parts": [...], "parts_base": URL or null}
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import tarfile
from collections import defaultdict
from pathlib import Path

PART_BYTES = 1_900_000_000


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scanned_pages(path: Path, min_words: int = 5) -> list[int]:
    """1-based numbers of the pages with no text layer (fewer than min_words words)."""
    import pymupdf

    with pymupdf.open(path) as doc:
        return [i + 1 for i, p in enumerate(doc) if len(p.get_text("words")) < min_words]


def all_pages(path: Path) -> list[int]:
    import pymupdf

    with pymupdf.open(path) as doc:
        return list(range(1, len(doc) + 1))


def bench_sample(files: list[dict], n_files: int, key=lambda f: Path(f["source"]).parent.name, seed: int = 7) -> set[str]:
    """A bake-off sample: small files spread over groups (by default the source folder, e.g. a year)."""
    rng = random.Random(seed)
    by = defaultdict(list)
    for f in files:
        if len(f["pages"]) <= 4:
            by[key(f)].append(f)
    for v in by.values():
        rng.shuffle(v)
    picked, groups = [], list(by.values())
    while len(picked) < n_files and any(groups):
        for g in groups:
            if g and len(picked) < n_files:
                picked.append(g.pop()["id"])
    return set(picked)


def build(sources: list[tuple[Path, str | None]], out: Path, every_page: bool = False, bench_files: int = 150,
          parts_base: str | None = None) -> dict:
    """sources: (local path, public url or None). Files with a url are fetched by the GPU machine; the rest are
    bundled into tars under out/."""
    out.mkdir(parents=True, exist_ok=True)
    files = []
    for n, (path, url) in enumerate(sources):
        pages = all_pages(path) if every_page else scanned_pages(path)
        if not pages:
            continue
        sha = sha256(path)
        files.append({"id": sha[:16], "source": str(path), "url": url, "sha256": sha, "pages": pages, "order": n})
    # one entry per distinct file
    seen, uniq = set(), []
    for f in files:
        if f["id"] not in seen:
            seen.add(f["id"])
            uniq.append(f)
    files = uniq
    bench = bench_sample(files, bench_files)
    for f in files:
        f["bench"] = f["id"] in bench
    # bundle the files without a url
    local = [f for f in files if not f["url"]]
    parts = []
    if local:
        import pymupdf

        pages_dir = out / "pages"
        pages_dir.mkdir(exist_ok=True)
        cur, size = [], 0
        for f in local:
            dst = pages_dir / f"{f['id']}.pdf"
            if not dst.exists():
                with pymupdf.open(f["source"]) as doc, pymupdf.open() as sub:
                    for p in f["pages"]:
                        sub.insert_pdf(doc, from_page=p - 1, to_page=p - 1)
                    sub.save(dst, garbage=4, deflate=True)
            b = dst.stat().st_size
            if cur and size + b > PART_BYTES:
                parts.append(cur)
                cur, size = [], 0
            cur.append(f)
            size += b
        if cur:
            parts.append(cur)
        names = []
        for k, part in enumerate(parts, 1):
            name = f"pages-{k}.tar"
            names.append(name)
            with tarfile.open(out / name, "w") as tar:
                for f in part:
                    f["part"] = name
                    tar.add(pages_dir / f"{f['id']}.pdf", arcname=f"pages/{f['id']}.pdf")
        parts = names
    man = {"files": files, "parts": parts, "parts_base": parts_base}
    (out / "manifest.json").write_text(json.dumps(man, separators=(",", ":")))
    return man


def from_csv(path: Path) -> list[tuple[Path, str | None]]:
    """url,path rows (path: a local copy used to find the pages; url: where the GPU machine fetches it)."""
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    return [(Path(r["path"]), r.get("url") or None) for r in rows if r.get("path") and Path(r["path"]).exists()]
