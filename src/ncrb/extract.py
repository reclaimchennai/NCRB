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
EXTS = (".pdf", ".xlsx", ".xls", ".doc", ".docx", ".rtf")


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


def _score(tables) -> tuple[int, int, int]:
    from .vlm_tables import score_tables

    return score_tables(tables)


# ties go to the reading of the model that won the bake-off on NCRB's own scans (colab/), the larger page first
VLM_PREFERRED = ["ATH-MaaS/OvisOCR2@2048", "ATH-MaaS/OvisOCR2", "PaddlePaddle/PaddleOCR-VL-1.6@2048", "mlx-community/GLM-OCR-bf16",
                 "PaddlePaddle/PaddleOCR-VL-1.6", "zai-org/GLM-OCR"]


def best_vlm(src: Path, cur_passed: int, cur_total: int, cur_is_vlm: bool = False):
    """The best cached VLM reading of a scanned file, if it should replace the current reading.

    Every model reading that covers all the file's scanned pages (laptop or cloud GPU, see colab/) is
    ranked by, in order:
      1. the State/UT/all-India totals check (a failed total costs twice a matched one);
      2. every other internal sum it reproduces: total rows inside lists and row totals ('Male + Female
         = Total'), ncrb.vlm_tables.consistency;
      3. agreement: the share of its figures that the other readings also found. Independent readings
         rarely misread the same digit the same way, so where nothing can be checked, the reading the
         others agree with is the likeliest right;
      4. the preferred model.
    Against a Tesseract reading, a model reading with totals to check is used only when it scores higher
    on (1), so no file whose totals could be checked gets worse; when the Tesseract reading has no total to
    check, a model reading that reproduces at least half of its own is used; when neither has a total, the
    best model reading is used. When the current reading is already a model's, the best model reading is used.
    Returns (tables, model, note) or None.
    """
    try:
        from .vlm import VLM_MODELS
        from .vlm_tables import agreement, consistency, numbers, vlm_tables
    except ImportError:
        return None
    order = VLM_PREFERRED + [m for m in VLM_MODELS if m not in VLM_PREFERRED]
    cands = []
    for rank, model in enumerate(order):
        vt, st = vlm_tables(src, model, run_model=False)
        if not vt or st["pages_missing"]:
            continue
        vp, vtot, vscore = _score(vt)
        cands.append({"model": model, "vt": vt, "vp": vp, "vtot": vtot, "vscore": vscore, "rank": rank,
                      "cons": consistency(vt), "nums": numbers(vt)})
    if not cands:
        return None
    for c in cands:
        others = [agreement(c["nums"], o["nums"]) for o in cands if o is not c]
        c["agree"] = sum(others) / len(others) if others else 0.0
    cur_score = cur_passed - 2 * (cur_total - cur_passed)
    if cur_is_vlm:
        eligible = cands
    else:
        # a Tesseract reading with no total to check (headings read as col_3, col_4 ...) cannot win by scoring 0
        # against a model reading that reproduces at least half of its printed totals (CII 1993/1995 crime tables)
        eligible = [c for c in cands if (c["vtot"] and c["vscore"] > cur_score) or (not c["vtot"] and not cur_total)
                    or (not cur_total and c["vtot"] and c["vp"] >= 0.5 * c["vtot"])]
    if not eligible:
        return None
    b = max(eligible, key=lambda c: (c["vtot"] > 0, c["vscore"], c["cons"], round(c["agree"], 3), -c["rank"]))
    if b["vtot"]:
        how = f"totals {b['vp']}/{b['vtot']}" + ("" if cur_is_vlm else f" against {cur_passed}/{cur_total}")
    else:
        how = "no State or all-India total to check"
    extra = f"; consistency {b['cons']:g}" + (f"; agrees {b['agree']:.0%} with {len(cands) - 1} other reading(s)" if len(cands) > 1 else "")
    return b["vt"], b["model"], f"VLM reading used ({b['model'].split('/')[-1]}): {how}{extra}"


def choose_vlm(src: Path, ocr_tables: list):
    tp, ttot, _ = _score(ocr_tables)
    r = best_vlm(src, tp, ttot)
    return (r[0], r[2]) if r else None


DOCX_CACHE = ROOT / "data" / "docx_cache"


def docx_tables(path: Path) -> list:
    """Tables of a .docx, cell by cell (python-docx), each with the paragraphs just above it as its title."""
    import html as htmllib

    from docx import Document
    from docx.table import Table as DocxTable
    from docx.text.paragraph import Paragraph

    from .assemble import assemble
    from .vlm_tables import page_segments

    doc = Document(str(path))
    segs, recent = [], []
    for el in doc.element.body.iterchildren():
        tag = el.tag.rsplit("}", 1)[-1]
        if tag == "p":
            txt = Paragraph(el, doc).text.strip()
            if txt:
                recent = (recent + [txt])[-4:]
        elif tag == "tbl":
            t = DocxTable(el, doc)
            rows = []
            for r in t.rows:
                cells, prev = [], None
                for c in r.cells:            # a merged cell repeats: keep one, spanning
                    if c._tc is prev:
                        cells[-1][1] += 1
                        continue
                    prev = c._tc
                    cells.append([" ".join(p.text.strip() for p in c.paragraphs if p.text.strip()), 1])
                rows.append("<tr>" + "".join(f'<td colspan="{n}">{htmllib.escape(x)}</td>' if n > 1 else f"<td>{htmllib.escape(x)}</td>"
                                             for x, n in cells) + "</tr>")
            # the title starts at its 'TABLE 12A' label; a footnote of the table before can precede it
            head = "\n".join(recent)
            m = list(re.finditer(r"\bTABLE[\s-]*\d+[A-Z]?\b", head, re.I))
            if m:
                head = head[m[-1].start():]
            html = head + "\n<table>" + "".join(rows) + "</table>"
            segs.extend(page_segments(html, len(segs) + 1))
            recent = []
    return [t for t in assemble(segs) if len(t.rows) >= 4 and len(t.columns) >= 2]


def word_tables(src: Path) -> list:
    """Tables of a Word file (Crime in India 2000's chapters, Prison Statistics 2001 ...): macOS textutil turns it
    into HTML, and each table with the text just before it (its title) goes through the same parser as the OCR
    models' HTML output, so headers, row labels and the totals check are shared."""
    import html as htmllib
    import subprocess

    from .assemble import assemble
    from .vlm_tables import file_sha, page_segments

    # a .doc converted by LibreOffice (scripts/convert_doc.sh) keeps its table cells; textutil merges them
    cached = DOCX_CACHE / f"{file_sha(src)[:16]}.docx"
    if src.suffix.lower() == ".docx":
        return docx_tables(src)
    if cached.exists():
        return docx_tables(cached)
    out = subprocess.run(["textutil", "-convert", "html", "-stdout", str(src)], capture_output=True, timeout=300)
    if out.returncode != 0:
        raise RuntimeError(f"textutil failed: {out.stderr[:200]!r}")
    body = out.stdout.decode("utf-8", "replace")
    body = re.sub(r"(?is)^.*?<body[^>]*>|</body>.*$", "", body)
    segs, text = [], ""
    for part in re.split(r"(?is)(<table.*?</table>)", body):
        if part[:6].lower() == "<table":
            pre = htmllib.unescape(re.sub(r"<[^>]+>", "\n", text))
            lines = [ln.strip() for ln in pre.splitlines() if ln.strip()][-4:]   # the title is just above the table
            segs.extend(page_segments("\n".join(lines) + "\n" + part, len(segs) + 1))
            text = ""
        else:
            text += part
    # narrative chapters wrap single sentences in tables: keep real ones only
    return [t for t in assemble(segs) if len(t.rows) >= 4 and len(t.columns) >= 2]


def process_file(job: dict) -> tuple[dict, list[dict]]:
    """Extract one source file. Returns (file summary, table index rows)."""
    src = ROOT / job["path"]
    summary = {k: job.get(k, "") for k in ("publication", "year", "listing")} | {"source_file": job["path"]}
    rows: list[dict] = []
    try:
        ext = src.suffix.lower()
        if ext in (".doc", ".docx", ".rtf"):
            tables = word_tables(src)
            summary |= {"pages": len(tables), "pages_without_text": 0, "pages_ocr": 0, "pages_with_table": len(tables)}
            method = "word"
        elif ext in (".xlsx", ".xls"):
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
            if st["vision_failed"]:
                summary["error"] = f"Apple Vision unavailable on {st['vision_failed']} of {st['pages_ocr']} OCR pages; Tesseract used alone"
            summary["pages_with_table"] = len({s.page for s in segments})
            method = "pdf_text"
            if st["pages_ocr"]:
                choice = choose_vlm(src, [t for t in tables if t.rows and t.columns])
                if choice is not None:
                    tables, note = choice
                    method = "pdf_vlm"
                    summary["error"] = note
        rows = write_tables(job, tables, method, summary)
    except Exception as e:  # keep going; the failure is recorded against the file
        summary |= {"status": "error", "error": f"{type(e).__name__}: {e}"[:300]}
        traceback.print_exc()
    return summary, rows


def write_tables(job: dict, tables: list, method: str, summary: dict) -> list[dict]:
    """Write a file's tables (json, csv, long csv) and return their index rows; sets the summary's status."""
    rows: list[dict] = []
    ext = Path(job["path"]).suffix.lower()
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
        if method == "pdf_vlm":
            m = "pdf_vlm"
        elif method == "pdf_text" and t.ocr_pages:
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
    return rows


def rescore_file(job: dict, cur_passed: int, cur_total: int, summary: dict):
    """A scanned file's cached VLM readings against its current one, without re-running OCR: rewritten only if better."""
    try:
        r = best_vlm(ROOT / job["path"], cur_passed, cur_total, cur_is_vlm=str(summary.get("error", "")).startswith("VLM reading used"))
        if r is None:
            return None
        tables, model, note = r
        summary = dict(summary) | {"error": note}
        return summary, write_tables(job, tables, "pdf_vlm", summary)
    except Exception as e:
        traceback.print_exc()
        return None


def vlm_ready(path: Path) -> bool:
    """True when the VLM page cache holds every scanned page of this file."""
    import pymupdf

    from .vlm import VLM_MODELS
    from .vlm_tables import cache_path, file_sha, scanned_pages

    if path.suffix.lower() != ".pdf":
        return False
    doc = pymupdf.open(path)
    pages = scanned_pages(doc)
    doc.close()
    if not pages:
        return False
    sha = file_sha(path)
    return any(all(cache_path(m, sha, p).exists() for p in pages) for m in VLM_MODELS)


def jobs(args) -> list[dict]:
    files = {}
    for state in sorted(FILES.parent.glob("files*.csv")):  # per-run state files of downloads still in progress
        files |= {r["url"]: r for r in csv.DictReader(state.open(encoding="utf-8")) if r["status"] == "ok"}
    out, seen = [], set()
    scanned = set()
    if args.scanned and FILE_INDEX.exists():
        scanned = {r["source_file"] for r in csv.DictReader(FILE_INDEX.open(encoding="utf-8")) if int(r["pages_ocr"] or 0) > 0}
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
        if args.scanned and f["path"] not in scanned:
            continue
        if args.vlm_ready and not vlm_ready(ROOT / f["path"]):
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
    ap.add_argument("--scanned", action="store_true", help="only files with scanned pages")
    ap.add_argument("--vlm-ready", action="store_true", help="only scanned files whose every page an OCR model has read")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-ocr", action="store_true", help="skip scanned pages instead of running OCR")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--revalue", action="store_true", help="only recompute `value` from `raw` in existing long files")
    ap.add_argument("--vlm-rescore", action="store_true",
                    help="scanned files: use a cached VLM reading where it beats the current one (no OCR is re-run)")
    args = ap.parse_args()
    if args.revalue:
        revalue()
        return
    if args.vlm_rescore:
        vlm_rescore(args)
        return

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


def vlm_rescore(args) -> None:
    table_rows = _load(INDEX, "source_file")
    file_rows = _load(FILE_INDEX, "source_file")
    todo = []
    for j in jobs(args):
        f = file_rows.get(j["path"], [{}])[0]
        if not j["path"].lower().endswith(".pdf") or int(float(f.get("pages_ocr") or 0)) == 0:
            continue
        cur = table_rows.get(j["path"], [])
        todo.append((j, sum(int(r["checks_passed"] or 0) for r in cur), sum(int(r["checks_total"] or 0) for r in cur), f))
    print(f"{len(todo)} scanned files to re-score", flush=True)
    changed = 0
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(rescore_file, j, p, t, f): j for j, p, t, f in todo}
        for n, fut in enumerate(as_completed(futures), 1):
            res = fut.result()
            if res is not None:
                summary, rows = res
                file_rows[summary["source_file"]] = [summary]
                table_rows[summary["source_file"]] = rows
                changed += 1
            if n % 200 == 0 or n == len(todo):
                _save(INDEX, INDEX_FIELDS, table_rows)
                _save(FILE_INDEX, FILE_FIELDS, file_rows)
                print(f"[{n}/{len(todo)}] {changed} files now use a VLM reading", flush=True)
    prune({r["csv"] for rows in table_rows.values() for r in rows})


def revalue() -> None:
    """Recompute the `value` column of every long file from `raw` with the current number parser."""
    n = changed = 0
    for path in OUT.rglob("*.long.csv"):
        rows = list(csv.reader(path.open(encoding="utf-8")))
        if not rows:
            continue
        head = rows[0]
        vi, ri = head.index("value"), head.index("raw")
        dirty = False
        for row in rows[1:]:
            v = parse_number(row[ri])
            new = "" if v is None else (f"{v:g}" if v != int(v) else str(int(v)))
            if new != row[vi]:
                row[vi] = new
                dirty = True
                changed += 1
        if dirty:
            with path.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(rows)
        n += 1
    print(f"revalued {n} long files, {changed} cells changed")


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
