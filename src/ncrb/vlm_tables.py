"""Tables from scanned PDFs read by a document VLM, cached and stitched across pages.

Each page is read once per model; the raw model output is kept under
``data/ocr_cache/<model>/<file sha256>/<page>.txt`` so a run can be stopped
and resumed, moved to another machine, or re-parsed without re-running the
model. Page tables are turned into the same ``PageTable`` segments the
geometric extractor produces and stitched by ``assemble``.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pymupdf as fitz

from .assemble import Table, assemble
from .crawl import ROOT
from .pdftable import TABLE_RE, CONTD_RE, Column, PageTable, Row, page_words
from .xlstable import tables_from_grid

CACHE = ROOT / "data" / "ocr_cache"
LABEL_ID = 0  # column id given to the row-label column of a VLM table


def model_slug(model_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9.]+", "-", model_id.split("/")[-1]).strip("-")


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cache_path(model_id: str, sha: str, page_no: int) -> Path:
    return CACHE / model_slug(model_id) / sha[:16] / f"{page_no:04d}.txt"


def scanned_pages(doc: fitz.Document) -> list[int]:
    """1-based numbers of the pages that have no text layer."""
    return [i + 1 for i, p in enumerate(doc) if len(page_words(p)) < 5]


def read_page(doc: fitz.Document, page_no: int, sha: str, model_id: str, run_model: bool = True) -> str | None:
    """Model output for one page, from the cache or by running the model."""
    path = cache_path(model_id, sha, page_no)
    if path.exists():
        return path.read_text(encoding="utf-8")
    if not run_model:
        return None
    from .vlm import page_image, read_image

    text = read_image(page_image(doc[page_no - 1]), model_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".part")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)
    return text


def _clean(cell: str) -> str:
    c = cell.replace("—", "-").replace("–", "-").replace("−", "-").strip()
    if re.fullmatch(r"[.·…:\s]+", c):      # dot leaders written as cells of their own ('Madras | . | . | . | 898')
        return ""
    c = re.sub(r"^-{2,}$", "-", c)
    return re.sub(r"(?<=\d) (?=\d{3}\b)", ",", c) if re.fullmatch(r"[\d ,.]+", c) else c


ANCHOR_CELL = re.compile(r"^[\[(]?\d{1,3}[a-z]?[\])]?$")


def _last_filled(row: list[str]) -> int:
    return max((j for j, v in enumerate(row) if v.strip()), default=-1)


def fix_grid(rows: list[list[str]], merged: list[tuple[int, int, int, int]]):
    """Repair the two mistakes document models make most on these tables.

    1. A heading cell that covers both label columns ('Sl. No. / State') is
       written one column wide, so every heading to its right lands one column
       too far left. The data rows (and the row of column numbers) show the
       true width; the headings are shifted right to match.
    2. A total's label is written on a row of its own, its figures on the next
       row with the label cells empty. The two rows are joined.
    """
    from .xlstable import _kind

    kinds = [_kind(r) for r in rows]
    first_data = next((i for i, k in enumerate(kinds) if k in ("data", "anchor")), None)
    if first_data:
        head = list(range(first_data))
        body = [i for i in range(first_data, len(rows)) if kinds[i] in ("data", "anchor")]
        w_body = max((_last_filled(rows[i]) for i in body), default=-1) + 1
        w_head = 0
        for i in head:
            w_head = max(w_head, _last_filled(rows[i]) + 1)
        for r0, r1, c0, c1 in merged:
            if r0 < first_data:
                w_head = max(w_head, c1)
        k = w_body - w_head
        if 0 < k <= 2:
            for i in head:
                rows[i] = (rows[i][:1] + [""] * k + rows[i][1:])[: len(rows[i])]
            fixed = []
            for r0, r1, c0, c1 in merged:
                if r0 < first_data:
                    fixed.append((r0, r1, c0, c1 + k) if c0 == 0 else (r0, r1, c0 + k, c1 + k))
                else:
                    fixed.append((r0, r1, c0, c1))
            merged = fixed
    # 3. The row of column numbers is often written one or two cells off. The figures fix the
    #    true data columns; the trailing numbers belong to them, the leading ones to the labels.
    a = next((i for i, k in enumerate(kinds) if k == "anchor"), None)
    if a is not None:
        data_rows = [r for i, r in enumerate(rows) if i > a and kinds[i] == "data"]
        width = max((len(r) for r in rows), default=0)
        numeric_cols = [j for j in range(width) if sum(1 for r in data_rows if j < len(r) and re.fullmatch(r"[-\d,.]+", r[j] or "x")) >= 0.5 * max(1, len(data_rows))]
        ids = [v for v in rows[a] if ANCHOR_CELL.match(v.strip())]
        if numeric_cols and len(ids) >= len(numeric_cols):
            new = [""] * width
            lead = ids[: len(ids) - len(numeric_cols)]
            for j, v in zip(range(numeric_cols[0]), lead[-numeric_cols[0]:] if numeric_cols[0] else []):
                new[j] = v
            for j, v in zip(numeric_cols, ids[len(ids) - len(numeric_cols):]):
                new[j] = v
            rows[a] = new
    out_rows, out_kinds = [], []
    i = 0
    while i < len(rows):
        r = rows[i]
        nxt = rows[i + 1] if i + 1 < len(rows) else None
        text = [v for v in r if v.strip()]
        if (
            nxt is not None and kinds[i] == "single" and len(text) == 1 and kinds[i + 1] == "data"
            and not nxt[0].strip() and not (len(nxt) > 1 and re.search(r"[A-Za-z]", nxt[1]))
        ):
            joined = list(nxt)
            joined[1 if len(joined) > 2 and not re.fullmatch(r"\d{1,3}", text[0]) else 0] = text[0]
            out_rows.append(joined)
            i += 2
            continue
        out_rows.append(r)
        i += 1
    return out_rows, merged if len(out_rows) == len(rows) else [m for m in merged if m[0] < (first_data or 0)]


def page_segments(text: str, page_no: int) -> list[PageTable]:
    """PageTable segments for one page of model output."""
    from .vlm import parse_output

    lines, grids = parse_output(text)
    title_line = next((ln for ln in lines if TABLE_RE.match(ln)), "")
    out: list[PageTable] = []
    for g in grids:
        rows, merged = fix_grid([[_clean(c) for c in r] for r in g.rows], list(g.merged))
        for t in tables_from_grid(rows, merged):
            title = t.title or " ".join(lines[:3])
            m = TABLE_RE.match(title_line or title)
            table_no = t.table_no or (re.sub(r"\s+", "", m.group(2)) if m else "")
            contd = bool(CONTD_RE.search(title_line + " " + title))
            for r in t.rows:
                m2 = re.match(r"^(\d{1,3})[.)]?\s+(?=\D)", r.label)
                if m2 and not r.serial:  # serial and name written into one cell
                    r.serial, r.label = m2.group(1), r.label[m2.end():]
            # columns the page numbered but that hold no figures (a label column the model merged away)
            empty = [cid for cid in t.columns if not any(cid in r.cells for r in t.rows)]
            for cid in empty:
                del t.columns[cid]
            if not t.columns:
                continue
            unlabelled = all(not r.label and not r.serial for r in t.rows)
            label_cols = [] if unlabelled else [LABEL_ID]
            columns = ([] if unlabelled else [Column(LABEL_ID, 0.0, header=[t.label_header] if t.label_header else [])]) + [
                Column(cid, 0.0, header=list(h)) for cid, h in t.columns.items()
            ]
            # column numbers transcribed from the page are real ids; positional ones are not
            inferred = all(cid == k + 1 for k, cid in enumerate(t.columns)) and min(t.columns, default=0) <= 3
            prows = [Row(r.label, r.serial, r.section, dict(r.cells), page_no, float(k * 10)) for k, r in enumerate(t.rows)]
            pt = PageTable(page_no, table_no, re.sub(r"\s+", " ", CONTD_RE.sub(" ", title)).strip(), contd, columns, label_cols, prows, list(t.notes), inferred)
            pt.unlabelled = unlabelled
            pt.ocr = True
            out.append(pt)
    return out


def tables_from_texts(texts: dict[int, str]) -> list[Table]:
    """Tables from cached model output alone ({page number: text}); no PDF needed, so it also runs on Colab."""
    segs: list[PageTable] = []
    for p in sorted(texts):
        segs.extend(page_segments(texts[p], p))
    return [t for t in assemble(segs) if t.rows and t.columns]


def score_tables(tables: list[Table]) -> tuple[int, int, int]:
    """(totals matched, totals checked, score): a failed total costs twice what a matched one earns."""
    from .assemble import check_totals

    passed = total = 0
    for t in tables:
        c = check_totals(t)
        passed += c["cells_passed"]
        total += c["cells_checked"]
    return passed, total, passed - 2 * (total - passed)


def consistency(tables: list[Table]) -> float:
    """Every internal sum a reading reproduces, for choosing between readings of the same file: State/UT/
    all-India total rows (weight 1), total rows inside lists (0.5) and row totals (0.5); a miss costs twice
    a match."""
    from .assemble import check_row_totals, check_totals

    s = 0.0
    for t in tables:
        c = check_totals(t)
        s += c["cells_passed"] - 2 * (c["cells_checked"] - c["cells_passed"])
        s += 0.5 * (c["other_totals_passed"] - 2 * (c["other_totals_checked"] - c["other_totals_passed"]))
        p, n = check_row_totals(t)
        if n and p >= 0.5 * n:      # most rows add up: the grouping is right, so a miss is a misread figure
            s += 0.5 * (p - 2 * (n - p))
    return s


NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")


def numbers(tables: list[Table]) -> list[str]:
    """The figures a reading found, in order, for measuring how far two readings agree."""
    return [m.replace(",", "") for t in tables for r in t.rows for cid in sorted(r.cells) for m in NUM.findall(r.cells[cid] or "")]


def agreement(a: list[str], b: list[str]) -> float:
    """Share of figures two readings have in common (as multisets): 1 when they read the same numbers."""
    from collections import Counter

    if not a or not b:
        return 0.0
    ca, cb = Counter(a), Counter(b)
    return sum((ca & cb).values()) / max(len(a), len(b))


def vlm_tables(path: Path, model_id: str, run_model: bool = True) -> tuple[list[Table], dict]:
    """Tables of a scanned PDF read by the VLM, and how many pages were read / missing."""
    doc = fitz.open(path)
    sha = file_sha(path)
    segs: list[PageTable] = []
    stats = {"pages": len(doc), "pages_vlm": 0, "pages_missing": 0}
    for p in scanned_pages(doc):
        text = read_page(doc, p, sha, model_id, run_model)
        if text is None:
            stats["pages_missing"] += 1
            continue
        stats["pages_vlm"] += 1
        segs.extend(page_segments(text, p))
    doc.close()
    tables = [t for t in assemble(segs) if t.rows and t.columns]
    return tables, stats
