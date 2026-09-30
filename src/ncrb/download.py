"""Download every file in ``catalog/catalog.csv`` into ``raw/``.

Files are stored as ``raw/<publication>/<year>/<listing>/<original filename>``.
A file that is linked from several listings is downloaded once and recorded
under the first listing that references it. The result of every attempt is
written to ``catalog/files.csv`` (one row per unique URL) with size and
SHA-256 so the raw corpus can be verified or rebuilt later.

Usage:
    uv run python -m ncrb.download                 # everything not yet on disk
    uv run python -m ncrb.download --pub adsi      # one publication
    uv run python -m ncrb.download --retry-failed  # retry rows marked failed
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests

from .crawl import CATALOG, ROOT, UA

RAW = ROOT / "raw"
FILES = ROOT / "catalog" / "files.csv"
DELAY = 0.5
FIELDS = ["url", "publication", "year", "listing", "path", "status", "bytes", "sha256", "content_type", "error"]
# listings are preferred in this order when one URL appears under several
LISTING_ORDER = {"table_content": 0, "additional_table": 1, "table_chapter": 2, "year_wise": 3}
MAGIC = {
    ".pdf": b"%PDF",
    ".xlsx": b"PK",
    ".zip": b"PK",
    ".docx": b"PK",
    ".xls": b"\xd0\xcf\x11\xe0",
    ".doc": b"\xd0\xcf\x11\xe0",
}


def safe_name(url: str) -> str:
    name = unquote(urlsplit(url).path.rsplit("/", 1)[-1])
    return re.sub(r"[^A-Za-z0-9._()\-+&, ]", "_", name).strip() or "file"


def plan() -> list[dict]:
    """One row per unique URL, with a unique local path."""
    rows = list(csv.DictReader(CATALOG.open(encoding="utf-8")))
    rows.sort(key=lambda r: (r["publication"], int(r["year"]), LISTING_ORDER.get(r["listing"], 9)))
    seen: dict[str, dict] = {}
    used: set[str] = set()
    for r in rows:
        if r["url"] in seen:
            continue
        rel = Path(r["publication"]) / r["year"] / r["listing"] / safe_name(r["url"])
        n = 1
        while str(rel).lower() in used:  # macOS filesystems are case-insensitive
            n += 1
            rel = rel.with_name(f"{rel.stem}__{n}{rel.suffix}")
        used.add(str(rel).lower())
        seen[r["url"]] = {
            "url": r["url"],
            "publication": r["publication"],
            "year": r["year"],
            "listing": r["listing"],
            "path": str(Path("raw") / rel),
        }
    return list(seen.values())


def load_state(path: Path = FILES) -> dict[str, dict]:
    if not path.exists():
        return {}
    return {r["url"]: r for r in csv.DictReader(path.open(encoding="utf-8"))}


def save_state(state: dict[str, dict], path: Path = FILES) -> None:
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for url in sorted(state, key=lambda u: state[u]["path"]):
            w.writerow({k: state[url].get(k, "") for k in FIELDS})
    tmp.replace(path)


def fetch(session: requests.Session, url: str, dest: Path) -> dict:
    """Download one file, resuming a partial download when the connection drops."""
    last = ""
    tmp = dest.with_name(dest.name + ".part")
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(6):
        have = tmp.stat().st_size if tmp.exists() else 0
        try:
            headers = {"Range": f"bytes={have}-"} if have else {}
            with session.get(url, timeout=(30, 300), stream=True, headers=headers) as r:
                if r.status_code == 404:
                    return {"status": "missing", "error": "HTTP 404"}
                if r.status_code == 416 and have:  # nothing left to fetch
                    pass
                elif r.status_code not in (200, 206):
                    last = f"HTTP {r.status_code}"
                    raise requests.RequestException(last)
                else:
                    if r.status_code == 200 and have:
                        have = 0  # server ignored the range: start again
                    with tmp.open("ab" if have else "wb") as f:
                        for chunk in r.iter_content(1 << 16):
                            f.write(chunk)
                ctype = r.headers.get("Content-Type", "")
                total = None
                if r.status_code == 206 and "/" in r.headers.get("Content-Range", ""):
                    total = int(r.headers["Content-Range"].rsplit("/", 1)[1])
                elif r.status_code == 200 and r.headers.get("Content-Length"):
                    total = int(r.headers["Content-Length"])
            size = tmp.stat().st_size
            if total is not None and size < total:
                last = f"truncated {size}/{total}"
                raise requests.RequestException(last)
            h = hashlib.sha256()
            with tmp.open("rb") as f:
                head = f.read(8)
                h.update(head)
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            magic = MAGIC.get(dest.suffix.lower())
            if magic and not head.lstrip().startswith(magic):
                if head.startswith(b"%PDF"):
                    # a PDF published under another extension: keep it, named for what it is
                    dest = dest.with_name(dest.name + ".pdf")
                else:
                    # the server answers some dead links with an HTML page
                    tmp.unlink(missing_ok=True)
                    return {"status": "not_a_file", "content_type": ctype, "error": f"bad magic {head!r}"}
            tmp.replace(dest)
            return {"status": "ok", "bytes": size, "sha256": h.hexdigest(), "content_type": ctype, "path": str(dest.relative_to(ROOT))}
        except (requests.RequestException, OSError) as e:
            last = last or repr(e)
            time.sleep(5 * (attempt + 1))
    return {"status": "failed", "error": last[:300]}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pub", choices=["cii", "psi", "adsi"])
    ap.add_argument("--year", type=int)
    ap.add_argument("--retry-failed", action="store_true")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--state", type=Path, default=FILES, help="state file; use a separate one per concurrent run, then --merge")
    ap.add_argument("--merge", type=Path, nargs="+", help="merge these state files into catalog/files.csv and exit")
    args = ap.parse_args()

    if args.merge:
        state = load_state()
        for p in args.merge:
            state.update(load_state(p))
        save_state(state)
        print(f"{len(state)} files recorded in {FILES.relative_to(ROOT)}")
        return
    state = load_state(args.state)
    todo = []
    for row in plan():
        if args.pub and row["publication"] != args.pub:
            continue
        if args.year and int(row["year"]) != args.year:
            continue
        prev = state.get(row["url"])
        if prev:
            if prev["status"] == "ok" and (ROOT / prev["path"]).exists():
                continue
            if prev["status"] in ("missing", "not_a_file", "failed") and not args.retry_failed:
                continue
        todo.append(row)
    if args.limit:
        todo = todo[: args.limit]
    print(f"{len(todo)} files to download", flush=True)

    local = threading.local()

    def work(row: dict) -> dict:
        if not hasattr(local, "session"):
            local.session = requests.Session()
            local.session.headers["User-Agent"] = UA
        result = fetch(local.session, row["url"], ROOT / row["path"])
        time.sleep(DELAY)
        return {**row, **result}

    # a few connections only: this is a small public server
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for i, rec in enumerate(ex.map(work, todo), 1):
            state[rec["url"]] = rec
            if rec["status"] != "ok":
                print(f"  {rec['status']}: {rec['url']} {rec.get('error', '')}", flush=True)
            if i % 50 == 0 or i == len(todo):
                save_state(state, args.state)
                ok = sum(1 for r in state.values() if r["status"] == "ok")
                print(f"[{i}/{len(todo)}] ok={ok} last={rec['path']}", flush=True)
    save_state(state, args.state)

if __name__ == "__main__":
    main()
