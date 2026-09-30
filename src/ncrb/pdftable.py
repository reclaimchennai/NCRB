"""Geometry-based table extraction for NCRB statistical tables.

NCRB tables share one convention that makes them tractable: directly under the
column headings there is a row of column numbers, ``(1) (2) (3) ...``. That row
fixes the x position and identity of every column, and the numbering continues
across "(Contd...)" pages, so a table that is split over many pages (more rows
or more columns) can be stitched back together exactly.

The pipeline for one page is:

1. words with coordinates (PyMuPDF), tagged with font size
2. find the column-number row (the "anchor")
3. everything above it is title + header, everything below is body + notes
4. header text is attached to columns using the shaded header-cell rectangles
   when the PDF has them (they give exact merged-cell spans), otherwise by
   horizontal overlap
5. body lines become rows; wrapped row labels are merged

Pages without an anchor row fall back to column inference from the numbers
themselves (see ``infer_anchor``).
"""

from __future__ import annotations

import re
import statistics
from dataclasses import dataclass, field

import pymupdf as fitz

COLNUM_RE = re.compile(r"^\(?(\d{1,3})\)$|^\((\d{1,3})\)?$")
# a cell value: number with optional sign/commas/decimals/percent, or a dash / NA style placeholder
NUM_RE = re.compile(r"^[-+−–]?\(?[-+−–]?\d[\d,]*(\.\d+)?\)?%?[*@#$^+]*$|^[-+−–]?\.\d+$")
PLACEHOLDER_RE = re.compile(r"^(-+|–|—|\.\.+|NA|N\.A\.?|NR|N\.R\.?|Nil|NIL|@|\*+|#|\$|&)$")
TABLE_RE = re.compile(r"^\s*(TABLE|Table)\s*[-–:]?\s*([0-9]+[A-Z]?(?:\s*[.\-]\s*[0-9]+[A-Z]?)*(?:\s*\((?:[A-Za-z]|[ivx]{1,4}|\d{1,2})\))?(?:\s*[A-Z](?![A-Za-z]))?)")
CONTD_RE = re.compile(r"\(?\s*(contd|continued|concld|concluded)\.?[\s.…]*\)?", re.I)
TOTAL_RE = re.compile(r"^\s*(grand\s+)?total\b|\btotal\s*\(|\ball[\s-]*india\b", re.I)


@dataclass
class Word:
    x0: float
    y0: float
    x1: float
    y1: float
    text: str
    size: float = 0.0
    bold: bool = False

    @property
    def xc(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def yc(self) -> float:
        return (self.y0 + self.y1) / 2


@dataclass
class Column:
    id: int
    xc: float
    left: float = 0.0
    right: float = 0.0
    header: list[str] = field(default_factory=list)


@dataclass
class Row:
    label: str
    serial: str
    section: str
    cells: dict[int, str]  # column id -> raw text
    page: int
    y: float


@dataclass
class PageTable:
    page: int
    table_no: str
    title: str
    contd: bool
    columns: list[Column]
    label_cols: list[int]
    rows: list[Row]
    notes: list[str]
    anchor_inferred: bool
    rotated: bool = False


def is_num(t: str) -> bool:
    return bool(NUM_RE.match(t))


def is_cell(t: str) -> bool:
    return bool(NUM_RE.match(t) or PLACEHOLDER_RE.match(t))


def parse_number(raw: str) -> float | None:
    """Numeric value of a raw cell, or None for placeholders / non-numbers."""
    t = raw.strip().replace("−", "-").replace("–", "-").replace(" ", "")
    t = re.sub(r"[*@#$^]+$", "", t)
    if not t or PLACEHOLDER_RE.match(t):
        return None
    neg = False
    if t.startswith("(") and t.endswith(")") and len(t) > 2:
        t = t[1:-1]
        if t.startswith("-"):
            neg, t = True, t[1:]
        elif t.startswith("+"):
            t = t[1:]
    t = t.rstrip("%+").replace(",", "")
    if t.startswith("+"):
        t = t[1:]
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


# --------------------------------------------------------------------------- words / lines


def page_words(page: fitz.Page) -> list[Word]:
    """Words with font size and boldness, in unrotated reading coordinates."""
    spans = []
    for block in page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]:
        for line in block.get("lines", []):
            for sp in line["spans"]:
                if sp["text"].strip():
                    spans.append((fitz.Rect(sp["bbox"]), sp["size"], bool(sp["flags"] & 16) or "bold" in sp["font"].lower()))
    out = []
    for x0, y0, x1, y1, text, *_ in page.get_text("words"):
        w = Word(x0, y0, x1, y1, text)
        cx, cy = w.xc, w.yc
        for r, size, bold in spans:
            if r.x0 - 1 <= cx <= r.x1 + 1 and r.y0 - 1 <= cy <= r.y1 + 1:
                w.size, w.bold = size, bold
                break
        else:
            w.size = y1 - y0
        out.append(w)
    return out


def rotate_words(words: list[Word], page_height: float, clockwise: bool) -> list[Word]:
    """Map words of a sideways (landscape-on-portrait) table to upright coordinates."""
    out = []
    for w in words:
        if clockwise:  # text reads top-to-bottom
            out.append(Word(w.y0, page_height and -w.x1, w.y1, -w.x0, w.text, w.size, w.bold))
        else:  # text reads bottom-to-top
            out.append(Word(-w.y1, w.x0, -w.y0, w.x1, w.text, w.size, w.bold))
    return out


def group_lines(words: list[Word]) -> list[list[Word]]:
    """Cluster words into visual lines by vertical centre."""
    lines: list[list[Word]] = []
    for w in sorted(words, key=lambda w: (w.yc, w.x0)):
        tol = max(2.0, 0.35 * (w.size or 8))
        if lines and abs(lines[-1][-1].yc - w.yc) <= tol and abs(_line_y(lines[-1]) - w.yc) <= tol:
            lines[-1].append(w)
        else:
            lines.append([w])
    for ln in lines:
        ln.sort(key=lambda w: w.x0)
    return lines


def _line_y(line: list[Word]) -> float:
    return sum(w.yc for w in line) / len(line)


def line_text(line: list[Word]) -> str:
    return " ".join(w.text for w in line)


# --------------------------------------------------------------------------- anchor


def _split_colnums(line: list[Word]) -> list[tuple[int, float, float]]:
    """(id, x0, x1) for each column number on a line; handles '(3)(4)' run together."""
    out = []
    for w in line:
        parts = re.findall(r"\(?(\d{1,3})\)", w.text)
        if not parts or re.sub(r"\(?\d{1,3}\)", "", w.text).strip():
            if COLNUM_RE.match(w.text):
                parts = [COLNUM_RE.match(w.text).group(1) or COLNUM_RE.match(w.text).group(2)]
            else:
                return []
        width = (w.x1 - w.x0) / len(parts)
        for i, p in enumerate(parts):
            out.append((int(p), w.x0 + i * width, w.x0 + (i + 1) * width))
    return out


def find_anchor(lines: list[list[Word]]) -> tuple[int, list[Column]] | None:
    """Index of the column-number line and its columns."""
    best = None
    for i, line in enumerate(lines):
        nums = _split_colnums(line)
        if len(nums) < 2:
            continue
        ids = [n[0] for n in nums]
        if ids != sorted(ids) or len(set(ids)) != len(ids):
            continue
        # must be (nearly) consecutive; a '(1) (2)' pair for label columns may precede a jump on contd pages
        steps = [b - a for a, b in zip(ids, ids[1:])]
        if sum(1 for s in steps if s == 1) < max(1, len(steps) - 2):
            continue
        if best is None or len(nums) > len(best[1]):
            best = (i, [Column(n, (a + b) / 2) for n, a, b in nums])
        if best and len(best[1]) >= 3:
            break  # the first good anchor on the page is the table's
    return best


def infer_anchor(lines: list[list[Word]]) -> tuple[int, list[Column]] | None:
    """Fallback for tables without a column-number row.

    Columns are inferred from where numeric tokens line up (by right edge,
    since numbers are right-aligned or centred in a narrow column). Returns the
    index of the last header line and synthetic columns numbered from 2, with
    column 1 reserved for the row label.
    """
    numeric_lines = []
    for i, line in enumerate(lines):
        toks = [w for w in line if is_cell(w.text)]
        if len(toks) >= 2 and len(toks) >= 0.4 * len(line):
            numeric_lines.append(i)
    if len(numeric_lines) < 3:
        return None
    centres = sorted(w.xc for i in numeric_lines for w in lines[i] if is_cell(w.text))
    sizes = [w.size for i in numeric_lines for w in lines[i] if w.size]
    gap = max(6.0, 1.2 * (statistics.median(sizes) if sizes else 8))
    clusters: list[list[float]] = [[centres[0]]]
    for c in centres[1:]:
        if c - clusters[-1][-1] <= gap:
            clusters[-1].append(c)
        else:
            clusters.append([c])
    need = max(2, 0.3 * len(numeric_lines))
    cols = [statistics.mean(c) for c in clusters if len(c) >= need]
    if len(cols) < 2:
        return None
    first = numeric_lines[0]
    # drop a leading cluster that is really the serial-number column
    label_right = min((w.x0 for i in numeric_lines for w in lines[i] if not is_cell(w.text)), default=None)
    columns = [Column(1, (label_right or cols[0]) - 1)]
    sn = [c for c in cols if label_right is not None and c < label_right]
    data = [c for c in cols if c not in sn]
    if len(data) < 1:
        return None
    columns = [Column(1, min(w.xc for i in numeric_lines for w in lines[i] if not is_cell(w.text)) if label_right else data[0] - 40)]
    columns += [Column(k + 2, c) for k, c in enumerate(data)]
    return first - 1, columns


# --------------------------------------------------------------------------- header


def header_extents(page: fitz.Page, y_top: float, y_bottom: float) -> list[tuple[float, float]]:
    """Distinct x extents of filled/stroked cell rectangles in the header band."""
    ext: set[tuple[int, int]] = set()
    try:
        drawings = page.get_drawings()
    except Exception:
        return []
    for d in drawings:
        r = d.get("rect")
        if r is None or r.y1 < y_top or r.y0 > y_bottom:
            continue
        if r.width < 8 or r.height < 0.05:
            continue
        ext.add((round(r.x0), round(r.x1)))
    return [(float(a), float(b)) for a, b in sorted(ext)]


def word_blocks(line: list[Word]) -> list[list[Word]]:
    """Split a header line into blocks of words separated by more than a normal space."""
    blocks: list[list[Word]] = []
    for w in line:
        space = 0.45 * (w.size or 8)
        if blocks and w.x0 - blocks[-1][-1].x1 <= space:
            blocks[-1].append(w)
        else:
            blocks.append([w])
    return blocks


def assign_headers(columns: list[Column], header_lines: list[list[Word]], extents: list[tuple[float, float]]) -> None:
    """Fill ``Column.header`` with the header path (outermost group first)."""
    cells: dict[tuple[float, float], list[tuple[float, float, str]]] = {}
    lo, hi = columns[0].left, columns[-1].right
    for line in header_lines:
        for block in word_blocks(line):
            x0, x1 = block[0].x0, block[-1].x1
            xc, y = (x0 + x1) / 2, _line_y(block)
            text = " ".join(w.text for w in block)
            ext = None
            fits = [e for e in extents if e[0] - 1 <= xc <= e[1] + 1 and e[0] - 6 <= x0 and x1 <= e[1] + 6]
            if fits:
                ext = min(fits, key=lambda e: e[1] - e[0])
            if ext is None:
                # no usable rectangle: span the columns the text physically covers
                covered = [c for c in columns if x0 - 2 <= c.xc <= x1 + 2]
                if covered:
                    ext = (covered[0].left, covered[-1].right)
                else:
                    near = min(columns, key=lambda c: abs(c.xc - xc))
                    ext = (near.left, near.right)
            cells.setdefault(ext, []).append((y, x0, text))
    spans = []
    for (a, b), parts in cells.items():
        covered = [c for c in columns if a - 1 <= c.xc <= b + 1]
        if not covered:
            covered = [min(columns, key=lambda c: abs(c.xc - (a + b) / 2))]
        text = _join_header(t for _, _, t in sorted(parts))
        spans.append((len(covered), min(p[0] for p in parts), covered, text))
    # widest span first = outermost header level
    for n, y, covered, text in sorted(spans, key=lambda s: (-s[0], s[1])):
        for c in covered:
            if text and text not in c.header:
                c.header.append(text)


def _join_header(parts) -> str:
    out = ""
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if out.endswith("-") and p[:1].islower():
            out = out[:-1] + p  # 'Trans-' + 'gender'
        else:
            out = f"{out} {p}" if out else p
    return re.sub(r"\s+", " ", out)


# --------------------------------------------------------------------------- page


def _set_bounds(columns: list[Column], extents: list[tuple[float, float]], page_w: float) -> None:
    mids = [(a.xc + b.xc) / 2 for a, b in zip(columns, columns[1:])]
    for i, c in enumerate(columns):
        c.left = mids[i - 1] if i else -1e6
        c.right = mids[i] if i < len(mids) else 1e6
    # snap to the narrowest cell rectangle containing the column centre, when there is one
    for c in columns:
        fits = [e for e in extents if e[0] <= c.xc <= e[1]]
        if fits:
            a, b = min(fits, key=lambda e: e[1] - e[0])
            others = [o for o in columns if o is not c and a <= o.xc <= b]
            if not others:
                c.left, c.right = a, b
    columns[0].left = min(columns[0].left, 0)
    columns[-1].right = max(columns[-1].right, page_w)


FOOTER_RES = [
    re.compile(r"^(accidental deaths|crime in india|prison statistics).{0,40}\b(19|20)\d\d\b.{0,12}$", re.I),
    re.compile(r"^\[?\s*\d{1,4}\s*\]?$"),
    re.compile(r"^page\s+\d+", re.I),
    re.compile(r"^[-–]?\s*\d{1,4}\s*[-–]?$"),
]


def is_page_furniture(text: str) -> bool:
    t = text.strip()
    return any(r.match(t) for r in FOOTER_RES)


def extract_page(page: fitz.Page, page_no: int, words: list[Word] | None = None, rotated: bool = False) -> PageTable | None:
    words = page_words(page) if words is None else words
    if not words:
        return None
    lines = group_lines(words)
    found = find_anchor(lines)
    inferred = False
    if found is None:
        found = infer_anchor(lines)
        inferred = True
    if found is None:
        return None
    ai, columns = found
    anchor_y = _line_y(lines[ai]) if ai >= 0 else lines[0][0].y0 - 1
    above = lines[: ai + 1] if inferred else lines[:ai]
    below = lines[ai + 1 :]

    # --- title vs header
    anchor_size = statistics.median([w.size for w in lines[ai]]) if ai >= 0 and not inferred else statistics.median(
        [w.size for ln in below[:10] for w in ln] or [8]
    )
    title_lines, header_lines = [], []
    in_header = False
    for ln in above:
        text = line_text(ln)
        if is_page_furniture(text):
            continue
        size = statistics.median([w.size for w in ln])
        multi = len(word_blocks(ln)) > 1 and max(b[0].x0 - a[-1].x1 for a, b in zip(word_blocks(ln), word_blocks(ln)[1:])) > 12
        if not in_header:
            looks_title = TABLE_RE.match(text) or size > anchor_size + 0.75 or (not multi and not title_lines)
            if looks_title and not (multi and size <= anchor_size + 0.75):
                title_lines.append(text)
                continue
            if not multi and title_lines and size >= anchor_size + 0.75:
                title_lines.append(text)
                continue
            in_header = True
        header_lines.append(ln)
    title = " ".join(title_lines)
    m = TABLE_RE.match(title)
    table_no = re.sub(r"\s+", "", m.group(2)) if m else ""
    contd = bool(CONTD_RE.search(title))
    title = CONTD_RE.sub("", title[m.end() :] if m else title).strip(" -–:.")

    # --- header → columns
    extents: list[tuple[float, float]] = []
    if header_lines and not rotated:
        y0 = min(w.y0 for ln in header_lines for w in ln) - 3
        extents = header_extents(page, y0, anchor_y + 4)
    _set_bounds(columns, extents, page.rect.width)
    if header_lines:
        assign_headers(columns, header_lines, extents)

    # --- body
    body: list[tuple[float, dict[int, list[Word]]]] = []
    for ln in below:
        if is_page_furniture(line_text(ln)):
            continue
        by_col: dict[int, list[Word]] = {}
        for w in ln:
            col = next((c for c in columns if c.left <= w.xc < c.right), None)
            if col is None:
                col = min(columns, key=lambda c: abs(c.xc - w.xc))
            by_col.setdefault(col.id, []).append(w)
        body.append((_line_y(ln), by_col))

    # which columns hold numbers?
    stats = {c.id: [0, 0] for c in columns}
    for _, by_col in body:
        for cid, ws in by_col.items():
            text = "".join(w.text for w in ws)
            stats[cid][1] += 1
            if is_cell(text) or all(is_cell(w.text) for w in ws):
                stats[cid][0] += 1
    numeric = {cid for cid, (n, tot) in stats.items() if tot and n / tot >= 0.6}
    # label columns are the leading non-numeric ones, plus a leading serial-number column
    label_cols: list[int] = []
    for c in columns:
        hdr = " ".join(c.header).lower()
        is_serial = bool(re.search(r"\b(s[lr]?\.?\s*no|sl\.?|s\.?\s*n\.?|serial)\b", hdr)) or (c is columns[0] and len(columns) > 2 and c.id == 1 and not inferred)
        if c.id not in numeric or (is_serial and not label_cols):
            label_cols.append(c.id)
        else:
            break
    if not label_cols:
        label_cols = [columns[0].id]
    data_cols = [c.id for c in columns if c.id not in label_cols]
    if not data_cols:
        return None

    # a label that overflows into data columns (e.g. 'TOTAL (ALL INDIA)') must not be read as data
    rows: list[Row] = []
    notes: list[str] = []
    section = ""
    pending: list[tuple[float, str]] = []  # label-only lines waiting for an owner
    pitches = [b[0] - a[0] for a, b in zip(body, body[1:]) if 0 < b[0] - a[0] < 60]
    pitch = statistics.median(pitches) if pitches else 12.0
    last_data_idx = max((i for i, (_, bc) in enumerate(body) if _has_data(bc, data_cols)), default=-1)
    serial_col = label_cols[0] if len(label_cols) > 1 else None

    for i, (y, by_col) in enumerate(body):
        if i > last_data_idx:
            text = " ".join(w.text for cid in sorted(by_col) for w in by_col[cid])
            notes.append(" ".join(w.text for w in sorted((w for ws in by_col.values() for w in ws), key=lambda w: w.x0)))
            continue
        label_words = [w for cid in label_cols for w in by_col.get(cid, [])]
        cells: dict[int, str] = {}
        spill: list[Word] = []
        for cid in data_cols:
            ws = by_col.get(cid, [])
            vals = [w for w in ws if is_cell(w.text)]
            spill += [w for w in ws if not is_cell(w.text)]
            if vals:
                cells[cid] = " ".join(w.text for w in vals) if len(vals) > 1 else vals[0].text
        serial = ""
        if serial_col is not None:
            sw = [w for w in by_col.get(serial_col, []) if re.fullmatch(r"\d{1,4}[.)]?|\(?[ivxlc]+\)|[A-Za-z][.)]", w.text)]
            if sw:
                serial = sw[0].text.rstrip(".)")
                label_words = [w for w in label_words if w is not sw[0]]
        elif label_words and re.fullmatch(r"\d{1,3}[.)]?", label_words[0].text) and len(label_words) > 1:
            serial = label_words[0].text.rstrip(".)")
            label_words = label_words[1:]
        label = " ".join(w.text for w in sorted(label_words + spill, key=lambda w: w.x0)).strip()
        if cells and _has_data(by_col, data_cols):
            row = Row(label, serial, section, cells, page_no, y)
            # wrapped label: text lines just above belong to a row whose own line has no label
            if pending and (not label or pending[-1][0] > y - 0.8 * pitch):
                take = [t for py, t in pending if y - py <= 1.6 * pitch] if not label else [t for py, t in pending if y - py <= 0.8 * pitch]
                keep = [(py, t) for py, t in pending if t not in take]
                for _, t in keep:
                    section = t
                row.section = section
                row.label = " ".join(take + ([label] if label else []))
                pending = []
            else:
                for _, t in pending:
                    section = t
                row.section = section
                pending = []
            rows.append(row)
        elif label or serial or cells:
            if cells:  # prose line that happens to contain a number
                label = " ".join(w.text for w in sorted((w for ws in by_col.values() for w in ws), key=lambda w: w.x0))
            text = (serial + " " + label).strip() if not label else label
            prev = rows[-1] if rows else None
            nxt = body[i + 1] if i + 1 <= last_data_idx else None
            # the next row has numbers but no label of its own: this line is the top half of its wrapped label
            feeds_next = (
                nxt is not None
                and nxt[0] - y <= 0.8 * pitch
                and _has_data(nxt[1], data_cols)
                and not any(not re.fullmatch(r"\d{1,4}[.)]?", w.text) for cid in label_cols for w in nxt[1].get(cid, []))
            )
            if prev is not None and y - prev.y <= 0.8 * pitch and not pending and not feeds_next:
                prev.label = (prev.label + " " + text).strip()  # continuation below the numbers
                if serial and not prev.serial:
                    prev.serial = serial
            else:
                pending.append((y, text))
    for _, t in pending:
        notes.insert(0, t)
    if not rows:
        return None
    return PageTable(page_no, table_no, title, contd, columns, label_cols, rows, [n for n in notes if n.strip()], inferred, rotated)


NOTE_START_RE = re.compile(r"^\s*(note|source|foot\s*note|n\.?b\.?)\b|^\s*[•\uf0b7*@#$+]", re.I)


def _has_data(by_col: dict[int, list[Word]], data_cols: list[int]) -> bool:
    """True for a line of table values; False for prose that merely contains a number."""
    words = [w for cid in data_cols for w in by_col.get(cid, [])]
    cells = sum(1 for w in words if is_cell(w.text))
    if not cells:
        return False
    first = min((w for ws in by_col.values() for w in ws), key=lambda w: w.x0)
    if NOTE_START_RE.match(first.text) and cells < 0.5 * len(words):
        return False
    return len(words) - cells <= max(3, cells)


def extract_pdf_pages(path: str) -> tuple[list[PageTable | None], int]:
    """One PageTable (or None) per page of the PDF, plus the number of pages with no text layer."""
    doc = fitz.open(path)
    out: list[PageTable | None] = []
    no_text = 0
    for i, page in enumerate(doc):
        words = page_words(page)
        if len(words) < 5:
            no_text += 1
            out.append(None)
            continue
        pt = extract_page(page, i + 1, words)
        out.append(pt)
    doc.close()
    return out, no_text
