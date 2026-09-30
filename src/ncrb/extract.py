"""Extract tables from every downloaded PDF into CSV + JSON.

For each source PDF ``raw/<pub>/<year>/<listing>/<name>.pdf`` this writes, per
table found in it, under ``data/tables/<pub>/<year>/``:

    <table_id>.csv        wide: one line per table row, one column per table column
    <table_id>.long.csv   tidy: one line per (row, column) cell, header levels split out
    <table_id>.json       metadata: title, source URL/file, pages, header tree, notes, checks

and one line per table in ``data/tables_index.csv``.

Usage:
    uv run python -m ncrb.extract                  # all PDFs not yet extracted
    uv run python -m ncrb.extract --pub adsi --year 2020
    uv run python -m ncrb.extract --force          # redo everything
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from .assemble import Table, assemble, check_totals
from .crawl import CATALOG, ROOT
from .download import FILES
from .pdftable import TOTAL_RE, col_label, extract_pdf_pages, parse_number
from .xlstable import extract_workbook

OUT = ROOT / "data" / "tables"
INDEX = ROOT / "data" / "tables_index.csv"
FILE_INDEX = ROOT / "data" / "files_index.csv"
MAX_LEVELS = 5

INDEX_FIELDS = [
    "table_id", "publication", "year", "listing", "topic", "section", "serial", "table_no", "title", "pdf_title",
    "method", "n_rows", "n_cols", "n_cells", "pages", "checks_total", "checks_passed", "inferred_pages", "warnings",
    "csv", "source_file", "source_url",
]
FILE_FIELDS = [
    "source_file", "publication", "year", "listing", "pages", "pages_without_text", "pages_ocr", "ocr_conf",
    "pages_with_table", "tables", "status", "error",
]
EXTS = (".pdf", ".xlsx", ".xls")


def slug(s: str, n: int = 70) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:n].rstrip("-")


def topic_of(section: str, listing: str) -> str:
    """NCRB's chapter heading for a file, cleaned: 'Chapter - 2 -- SUICIDES IN INDIA' -> 'Suicides in India'."""
    if listing == "year_wise":
        return ""  # volumes and front matter are listed under the report's name, not a topic
    t = re.sub(r"^\s*chapter\s*[-–]?\s*[0-9A-Za-z]*\s*[-–]+\s*", "", section, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip()
    if t.isupper():
        small = {"In", "Of", "And", "By", "With", "The", "To", "For", "Under", "On"}
        words = [w if w.upper() in ("IPC", "SLL", "SC", "ST", "SCS", "STS", "UT", "UTS", "ADSI", "BNS") or "/" in w else w.capitalize() for w in t.split()]
        t = " ".join(w.lower() if i and w in small else w for i, w in enumerate(words))
    return t


def header_name(path: list[str]) -> str:
    return " | ".join(p for p in path if p)


def write_table(t: Table, meta: dict, base: Path) -> dict:
    base.parent.mkdir(parents=True, exist_ok=True)
    col_ids = list(t.columns)  # insertion order = order of appearance in the document
    names, used = [], {}
    for cid in col_ids:
        name = header_name(t.columns[cid]) or f"col_{cid}"
        used[name] = used.get(name, 0) + 1
        names.append(name)
    # duplicated headings are disambiguated with the printed column number
    names = [f"{n} ({col_label(cid)})" if used[n] > 1 else n for n, cid in zip(names, col_ids)]
    label_name = t.label_header.split(" / ")[-1] if t.label_header else "name"

    with base.with_suffix(".csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["section", "sl_no", label_name or "name", *names])
        for r in t.rows:
            w.writerow([r.section, r.serial, r.label, *[r.cells.get(cid, "") for cid in col_ids]])

    n_cells = 0
    with Path(str(base) + ".long.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["row", "section", "sl_no", "name", "is_total", "col_no", "column", *[f"h{i + 1}" for i in range(MAX_LEVELS)], "value", "raw", "page", "ocr_conf"])
        for i, r in enumerate(t.rows, 1):
            total = int(bool(TOTAL_RE.search(r.label)))
            for cid, name in zip(col_ids, names):
                raw = r.cells.get(cid)
                if raw is None:
                    continue
                v = parse_number(raw)
                path = (t.columns[cid] + [""] * MAX_LEVELS)[:MAX_LEVELS]
                if len(t.columns[cid]) > MAX_LEVELS:
                    path[-1] = " | ".join(t.columns[cid][MAX_LEVELS - 1 :])
                w.writerow([i, r.section, r.serial, r.label, total, col_label(cid), name, *path, "" if v is None else f"{v:g}" if v != int(v) else int(v), raw, r.page, f"{r.conf[cid]:.2f}" if cid in r.conf else ""])
                n_cells += 1

    checks = check_totals(t)
    doc = {
        **meta,
        "table_no": t.table_no,
        "pdf_title": t.title,
        "row_label": t.label_header,
        "pages": t.pages,
        "n_rows": len(t.rows),
        "n_cols": len(col_ids),
        "n_cells": n_cells,
        "columns": [{"col_no": col_label(cid), "name": n, "header": t.columns[cid]} for cid, n in zip(col_ids, names)],
        "notes": t.notes,
        "checks": checks,
        "inferred_pages": t.inferred_pages,
        "ocr_pages": t.ocr_pages,
        "warnings": t.warnings,
    }
    base.with_suffix(".json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    return doc


def process_file(job: dict) -> tuple[dict, list[dict]]:
    """Extract one source file. Returns (file summary, table index rows)."""
    src = ROOT / job["path"]
    summary = {k: job.get(k, "") for k in ("publication", "year", "listing")} | {"source_file": job["path"]}
    rows: list[dict] = []
    try:
        ext = src.suffix.lower()
        if ext in (".xlsx", ".xls"):
            found = extract_workbook(str(src))
            tables = [t for _, t in found]
            for sheet, t in found:
                t.sheet = sheet
            summary |= {"pages": len({s for s, _ in found}), "pages_without_text": 0, "pages_ocr": 0, "pages_with_table": len({s for s, _ in found})}
            method = "excel"
        else:
            segments, st = extract_pdf_pages(str(src), use_ocr=job.get("ocr", True))
            tables = assemble(segments)
            summary |= {k: st[k] for k in ("pages", "pages_without_text", "pages_ocr", "ocr_conf")}
            summary["pages_with_table"] = len({s.page for s in segments})
            method = "pdf_text"
        tables = [t for t in tables if t.rows and t.columns]
        summary["tables"] = len(tables)
        if tables:
            summary["status"] = "ok"
        elif ext == ".pdf" and summary["pages_without_text"] >= 0.8 * max(1, summary["pages"]) and not summary["pages_ocr"]:
            summary["status"] = "scanned_not_ocred"
        else:
            summary["status"] = "no_table"
        stem = slug(Path(job["path"]).stem, 60)
        prefix = slug(job.get("serial", ""), 12)
        seen: dict[str, int] = {}
        for k, t in enumerate(tables, 1):
            tid = "_".join(x for x in (prefix, stem) if x)
            if len(tables) > 1:
                tid += "_t" + (slug(t.table_no) or str(k))
            seen[tid] = seen.get(tid, 0) + 1
            if seen[tid] > 1:
                tid += f"_{seen[tid]}"
            title = job.get("title", "") if len(tables) == 1 else (t.title or job.get("title", ""))
            if method == "pdf_text" and t.ocr_pages:
                m = "pdf_ocr" if t.ocr_pages == len(t.pages) else "pdf_mixed"
            else:
                m = method
            meta = {
                "table_id": f"{job['publication']}/{job['year']}/{tid}",
                "publication": job["publication"],
                "year": int(job["year"]),
                "listing": job["listing"],
                "topic": topic_of(job.get("section", ""), job["listing"]),
                "section": job.get("section", ""),
                "serial": job.get("serial", ""),
                "title": title,
                "listing_title": job.get("title", ""),
                "method": m,
                "sheet": t.sheet,
                "source_url": job["url"],
                "source_file": job["path"],
                "source_sha256": job.get("sha256", ""),
            }
            base = OUT / job["publication"] / str(job["year"]) / tid
            doc = write_table(t, meta, base)
            rows.append({
                **{k: doc.get(k, "") for k in INDEX_FIELDS},
                "pages": f"{t.pages[0]}-{t.pages[-1]}" if t.pages else "",
                "checks_total": doc["checks"]["cells_checked"],
                "checks_passed": doc["checks"]["cells_passed"],
                "warnings": "; ".join(t.warnings),
                "csv": str(base.with_suffix(".csv").relative_to(ROOT)),
            })
    except Exception as e:  # keep going; the failure is recorded against the file
        summary |= {"status": "error", "error": f"{type(e).__name__}: {e}"[:300]}
        traceback.print_exc()
    return summary, rows


def jobs(args) -> list[dict]:
    files = {}
    for state in sorted(FILES.parent.glob("files*.csv")):  # per-run state files of downloads still in progress
        files |= {r["url"]: r for r in csv.DictReader(state.open(encoding="utf-8")) if r["status"] == "ok"}
    out, seen = [], set()
    for r in csv.DictReader(CATALOG.open(encoding="utf-8")):
        f = files.get(r["url"])
        if f is None or r["url"] in seen or not f["path"].lower().endswith(EXTS):
            continue
        if (r["publication"], r["year"], r["listing"]) != (f["publication"], f["year"], f["listing"]):
            continue  # use the catalog row that the file was stored under
        if args.pub and r["publication"] != args.pub:
            continue
        if args.year and int(r["year"]) != args.year:
            continue
        if args.listing and r["listing"] != args.listing:
            continue
        if args.kind and (f["path"].lower().endswith(".pdf")) != (args.kind == "pdf"):
            continue
        seen.add(r["url"])
        out.append({**r, "path": f["path"], "sha256": f["sha256"], "ocr": not args.no_ocr})
    return out


def _load(path: Path, key: str) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    if path.exists():
        for r in csv.DictReader(path.open(encoding="utf-8")):
            out.setdefault(r[key], []).append(r)
    return out


def _save(path: Path, fields: list[str], groups: dict[str, list[dict]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for k in sorted(groups):
            for r in groups[k]:
                w.writerow(r)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pub", choices=["cii", "psi", "adsi"])
    ap.add_argument("--year", type=int)
    ap.add_argument("--listing")
    ap.add_argument("--kind", choices=["pdf", "excel"], help="only this kind of source file")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-ocr", action="store_true", help="skip scanned pages instead of running OCR")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    table_rows = _load(INDEX, "source_file")
    file_rows = _load(FILE_INDEX, "source_file")
    todo = [j for j in jobs(args) if args.force or j["path"] not in file_rows or file_rows[j["path"]][0]["status"] == "error"]
    print(f"{len(todo)} files to extract", flush=True)
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(process_file, j): j for j in todo}
        for n, fut in enumerate(as_completed(futures), 1):
            summary, rows = fut.result()
            file_rows[summary["source_file"]] = [summary]
            table_rows[summary["source_file"]] = rows
            if n % 50 == 0 or n == len(todo):
                _save(INDEX, INDEX_FIELDS, table_rows)
                _save(FILE_INDEX, FILE_FIELDS, file_rows)
                print(f"[{n}/{len(todo)}] tables so far: {sum(len(v) for v in table_rows.values())}", flush=True)
    _save(INDEX, INDEX_FIELDS, table_rows)
    _save(FILE_INDEX, FILE_FIELDS, file_rows)
    prune({r["csv"] for rows in table_rows.values() for r in rows})


def prune(keep: set[str]) -> None:
    """Delete table files left behind by earlier runs that split a source file differently."""
    removed = 0
    for path in OUT.rglob("*.json"):
        if str(path.with_suffix(".csv").relative_to(ROOT)) not in keep:
            for p in (path, path.with_suffix(".csv"), Path(str(path.with_suffix("")) + ".long.csv")):
                p.unlink(missing_ok=True)
            removed += 1
    if removed:
        print(f"removed {removed} stale tables", flush=True)


if __name__ == "__main__":
    main()
