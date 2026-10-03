"""Recover Crime in India files NCRB no longer serves, from the Internet Archive's copies of its old website.

NCRB's current site lists 107 files it does not serve (404 or an HTML error page): most of the 1996, 2000
and 2012 editions. Its old site (ncrb.nic.in, and ncrb.gov.in/StatPublications) published those editions in
other forms, and the Wayback Machine kept them:

- 2000: the tables as Word files (tb13.doc, tb14-18.doc ... tb93-99.doc, and the chapters);
- 2012: every chapter as a text PDF, the 1953-2012 tables, the annexure and the additional tables;
- 1996: whatever survives of cii1996/.

Each file is fetched from its archived copy (web.archive.org/web/<timestamp>id_/<original>, the bytes as
archived) and added to catalog/catalog.csv and catalog/files.csv under listing 'archived', with the archive
URL as its source, so every figure from it links back to the copy it came from.

    uv run python scripts/recover_wayback.py            # list what would be fetched
    uv run python scripts/recover_wayback.py --fetch
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CDX = "http://web.archive.org/cdx/search/cdx"
# (publication, year, archive path patterns)
SOURCES = [
    ("cii", 2000, ["ncrb.nic.in/StatPublications/CII/CII2000/*", "ncrb.gov.in/StatPublications/CII/CII2000/*",
                   "ncrb.nic.in/ciiprevious/Data/CD-CII2000/*"]),
    ("cii", 2012, ["ncrb.gov.in/StatPublications/CII/CII2012/*", "ncrb.nic.in/StatPublications/CII/CII2012/*"]),
    ("cii", 1996, ["ncrb.nic.in/StatPublications/CII/CII1996/*", "ncrb.gov.in/StatPublications/CII/CII1996/*",
                   "ncrb.nic.in/ciiprevious/Data/CII1996/*"]),
]
KEEP = re.compile(r"\.(pdf|docx?|xlsx?|rtf)$", re.I)
SKIP = re.compile(r"feedback|disclaimer|preface|officers|limitations|cover|snapshot|contents|maps", re.I)


def cdx(pattern: str) -> list[dict]:
    q = f"{CDX}?url={urllib.parse.quote(pattern)}&filter=statuscode:200&collapse=urlkey&fl=timestamp,original,mimetype,length&output=json&limit=5000"
    for attempt in range(4):
        try:
            rows = json.load(urllib.request.urlopen(q, timeout=120))
            return [dict(zip(rows[0], r)) for r in rows[1:]] if rows else []
        except Exception:
            time.sleep(10 * (attempt + 1))
    return []


def name_of(original: str) -> str:
    p = urllib.parse.unquote(original).replace("\\", "/")
    return p.rstrip("/").rsplit("/", 1)[-1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--matches", help="JSON list of {pub, year, ts, orig}: fetch exactly these archived files")
    args = ap.parse_args()
    files_csv = ROOT / "catalog" / "files.csv"
    have = {r["sha256"] for r in csv.DictReader(files_csv.open(encoding="utf-8"))}
    known_urls = {r["url"] for r in csv.DictReader(files_csv.open(encoding="utf-8"))}
    todo = []
    if args.matches:
        for m in json.loads(Path(args.matches).read_text()):
            todo.append((m["pub"], int(m["year"]), {"timestamp": m["ts"], "original": m["orig"], "mimetype": ""}, name_of(m["orig"])))
    for pub, year, patterns in ([] if args.matches else SOURCES):
        seen = set()
        for pat in patterns:
            for r in cdx(pat):
                nm = name_of(r["original"])
                if not KEEP.search(nm) or SKIP.search(nm) or nm.lower() in seen:
                    continue
                seen.add(nm.lower())
                todo.append((pub, year, r, nm))
            time.sleep(2)
    print(f"{len(todo)} archived files")
    for pub, year, r, nm in todo:
        print(f"  {pub} {year} {r['timestamp']} {nm}")
    if not args.fetch:
        return
    cat_rows, file_rows = [], []
    for pub, year, r, nm in todo:
        src = f"https://web.archive.org/web/{r['timestamp']}id_/{r['original']}"
        if src in known_urls:
            continue
        dest = ROOT / "raw" / pub / str(year) / "archived" / re.sub(r"[^\w.\-]+", "_", nm)
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = None
        for attempt in range(4):
            try:
                data = urllib.request.urlopen(src, timeout=300).read()
                break
            except Exception as e:
                print("  retry", nm, e)
                time.sleep(15 * (attempt + 1))
        if not data or data[:5].lower().startswith((b"<!doc", b"<html")):
            print("  not a file:", nm)
            continue
        sha = hashlib.sha256(data).hexdigest()
        if sha in have:
            print("  already have:", nm)
            continue
        dest.write_bytes(data)
        have.add(sha)
        title = re.sub(r"\.[^.]+$", "", nm).replace("_", " ")
        cat_rows.append({"publication": pub, "listing": "archived", "year": year, "section": f"Crime in India {year} (archived copy of NCRB's old site)",
                         "serial": "", "title": title, "url": src, "size_text": f"[ {len(data) / 1024:.1f} KB ]",
                         "listing_url": r["original"]})
        file_rows.append({"url": src, "publication": pub, "year": year, "listing": "archived", "path": str(dest.relative_to(ROOT)),
                          "status": "ok", "bytes": len(data), "sha256": sha, "content_type": r.get("mimetype", ""), "error": ""})
        print(f"  got {nm} ({len(data) / 1e6:.1f} MB)")
        time.sleep(1.5)
    for path, rows in ((ROOT / "catalog" / "catalog.csv", cat_rows), (files_csv, file_rows)):
        if not rows:
            continue
        with path.open(encoding="utf-8") as f:
            fields = next(csv.reader(f))
        with path.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            for row in rows:
                w.writerow({k: row.get(k, "") for k in fields})
    print(f"added {len(file_rows)} files")


if __name__ == "__main__":
    main()
