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
    headless: bool = False  # header found but its rows are on the next page
    carried: bool = False  # rows that inherited their columns from the previous segment


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


def _split_colnums(line: list[Word]) -> tuple[list[tuple[int, float, float]], list[Word]]:
    """Column numbers on a line as (id, x0, x1), plus the words that are not column numbers.

    Handles numbers run together as '(3)(4)'.
    """
    out, others = [], []
    for w in line:
        parts = re.findall(r"\(?(\d{1,3})\)", w.text)
        if parts and not re.sub(r"\(?\d{1,3}\)", "", w.text).strip():
            width = (w.x1 - w.x0) / len(parts)
            out += [(int(p), w.x0 + i * width, w.x0 + (i + 1) * width) for i, p in enumerate(parts)]
        else:
            others.append(w)
    return out, others


def find_anchors(lines: list[list[Word]]) -> list[tuple[int, list[Column], list[Word]]]:
    """Every column-number line on the page: (line index, columns, header words sharing the line)."""
    out = []
    for i, line in enumerate(lines):
        nums, others = _split_colnums(line)
        if len(nums) < 2 or len(nums) < 0.6 * len(line):
            continue
        ids = [n[0] for n in nums]
        if ids != sorted(ids) or len(set(ids)) != len(ids):
            continue
        # must be (nearly) consecutive; '(1) (2)' for the label columns may precede a jump on contd pages
        steps = [b - a for a, b in zip(ids, ids[1:])]
        if sum(1 for s in steps if s == 1) < max(1, len(steps) - 2):
            continue
        if len(nums) == 2 and (ids != [1, 2] or others):
            continue  # too weak to trust
        out.append((i, [Column(n, (a + b) / 2) for n, a, b in nums], others))
    return out


def numeric_line(line: list[Word]) -> bool:
    toks = sum(1 for w in line if is_cell(w.text))
    return toks >= 2 and toks >= 0.4 * len(line)


def infer_columns(lines: list[list[Word]]) -> list[Column] | None:
    """Columns for lines of data that have no column-number row.

    Numeric tokens whose x ranges overlap (across lines) form one column.
    Returns a label column with id 1 followed by data columns numbered from 2.
    """
    rows = [ln for ln in lines if numeric_line(ln)]
    if len(rows) < 2:
        return None
    text_right = [max((w.x1 for w in ln if not is_cell(w.text)), default=None) for ln in rows]
    text_right = [x for x in text_right if x is not None]
    label_edge = statistics.median(text_right) if len(text_right) >= 0.5 * len(rows) else None
    spans = sorted((w.x0, w.x1) for ln in rows for w in ln if is_cell(w.text))
    groups: list[list[float]] = []  # x0, x1, count
    for x0, x1 in spans:
        if groups and x0 <= groups[-1][1] + 0.5:
            groups[-1][1] = max(groups[-1][1], x1)
            groups[-1][2] += 1
        else:
            groups.append([x0, x1, 1])
    need = max(2, 0.25 * len(rows))
    data = [g for g in groups if g[2] >= need]
    if label_edge is not None:
        # numbers left of where row labels end are serial numbers, not data
        first_text = statistics.median([min(w.x0 for w in ln if not is_cell(w.text)) for ln in rows if any(not is_cell(w.text) for w in ln)])
        data = [g for g in data if (g[0] + g[1]) / 2 > first_text]
    if not data:
        return None
    label_x = min(w.x0 for ln in rows for w in ln)
    cols = [Column(1, (label_x + data[0][0]) / 2)]
    cols += [Column(k + 2, (g[0] + g[1]) / 2) for k, g in enumerate(data)]
    return cols


# --------------------------------------------------------------------------- header


@dataclass
class Rules:
    """Ruling lines and cell edges of a page region, used to recover merged header cells."""

    vert: list[tuple[float, float, float]] = field(default_factory=list)  # x, y0, y1
    horiz: list[tuple[float, float, float]] = field(default_factory=list)  # y, x0, x1

    @classmethod
    def from_page(cls, page: fitz.Page, y_top: float, y_bottom: float) -> "Rules":
        r = cls()
        try:
            drawings = page.get_drawings()
        except Exception:
            return r
        for d in drawings:
            for it in d["items"]:
                if it[0] == "l":
                    p, q = it[1], it[2]
                    if abs(p.x - q.x) < 0.7 and abs(p.y - q.y) >= 3:
                        r._v(p.x, min(p.y, q.y), max(p.y, q.y), y_top, y_bottom)
                    elif abs(p.y - q.y) < 0.7 and abs(p.x - q.x) >= 6:
                        r._h(p.y, min(p.x, q.x), max(p.x, q.x), y_top, y_bottom)
                elif it[0] == "re":
                    rc = it[1]
                    if rc.width < 2 and rc.height >= 3:
                        r._v((rc.x0 + rc.x1) / 2, rc.y0, rc.y1, y_top, y_bottom)
                    elif rc.height < 2 and rc.width >= 6:
                        r._h((rc.y0 + rc.y1) / 2, rc.x0, rc.x1, y_top, y_bottom)
                    elif rc.width >= 6 and rc.height >= 3:  # a shaded or boxed cell
                        r._v(rc.x0, rc.y0, rc.y1, y_top, y_bottom)
                        r._v(rc.x1, rc.y0, rc.y1, y_top, y_bottom)
        return r

    def _v(self, x, y0, y1, top, bottom):
        if y1 >= top and y0 <= bottom:
            self.vert.append((x, y0, y1))

    def _h(self, y, x0, x1, top, bottom):
        if top <= y <= bottom:
            self.horiz.append((y, x0, x1))

    def cell(self, x0: float, x1: float, y: float, full: tuple[float, float]) -> tuple[float, float] | None:
        """x extent of the header cell holding text at (x0..x1, y), if the rules determine it."""
        xc = (x0 + x1) / 2
        cands = []
        left = [x for x, a, b in self.vert if x <= xc and a - 2 <= y <= b + 2]
        right = [x for x, a, b in self.vert if x >= xc and a - 2 <= y <= b + 2]
        if left and right:
            L, R = max(left), min(right)
            if R - L >= (x1 - x0) - 12:
                cands.append((L, R))
        # a rule under the text (spanner underline or the cell's bottom border)
        span = full[1] - full[0]
        below = [(hy, a, b) for hy, a, b in self.horiz if hy > y and a - 3 <= xc <= b + 3 and (b - a) < 0.95 * span]
        if below:
            y0 = min(h[0] for h in below)
            near = [h for h in below if h[0] - y0 <= 1.5]
            holds = [h for h in near if h[1] - 4 <= x0 and x1 <= h[2] + 4]
            _, a, b = min(holds, key=lambda h: h[2] - h[1]) if holds else max(near, key=lambda h: h[2] - h[1])
            cands.append((a, b))
        if not cands:
            return None
        # vertical rules are exact for the text's own row; fall back to the underline only
        # when they merely give the outline of the whole table
        if len(cands) == 2 and cands[0][1] - cands[0][0] >= 0.95 * span:
            return cands[1]
        return cands[0]


def word_blocks(line: list[Word]) -> list[list[Word]]:
    """Split a header line into blocks of words separated by more than a normal space."""
    blocks: list[list[Word]] = []
    for w in line:
        space = 0.5 * (w.size or 8)
        if blocks and w.x0 - blocks[-1][-1].x1 <= space:
            blocks[-1].append(w)
        else:
            blocks.append([w])
    return blocks


def assign_headers(columns: list[Column], header_lines: list[list[Word]], rules: Rules) -> None:
    """Fill ``Column.header`` with the header path (outermost group first)."""
    cells: dict[tuple[int, ...], list[tuple[float, float, str]]] = {}
    full = (min(c.xc for c in columns), max(c.xc for c in columns))
    for line in header_lines:
        last = -1  # index of the last column used on this line; blocks on a line map left to right
        for block in word_blocks(line):
            x0, x1 = block[0].x0, block[-1].x1
            xc, y = (x0 + x1) / 2, _line_y(block)
            text = " ".join(w.text for w in block)
            ext = rules.cell(x0, x1, y, full)
            idx: list[int] = []
            if ext is not None:
                idx = [i for i, c in enumerate(columns) if ext[0] - 1 <= c.xc <= ext[1] + 1]
            if not idx:
                # no usable rule: the columns the text physically covers, else the one it sits in
                idx = [i for i, c in enumerate(columns) if x0 - 2 <= c.xc <= x1 + 2]
                if not idx:
                    idx = [min(range(len(columns)), key=lambda i: (not columns[i].left <= xc < columns[i].right, abs(columns[i].xc - xc)))]
                if ext is None and idx[0] <= last and idx[-1] + 1 < len(columns) and len(idx) == 1:
                    idx = [last + 1] if last + 1 < len(columns) else idx
            last = max(last, idx[-1])
            cells.setdefault(tuple(idx), []).append((y, x0, text))
    # widest span first = outermost header level
    for idx, parts in sorted(cells.items(), key=lambda kv: (-len(kv[0]), min(p[0] for p in kv[1]))):
        text = _join_header(t for _, _, t in sorted(parts))
        for i in idx:
            if text:
                columns[i].header.append(text)


def _join_header(parts) -> str:
    out = ""
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if out.endswith("-") and p[:1].islower():
            out = out[:-1] + p  # 'Trans-' + 'gender'
        elif out.endswith("-") and p[:1].isupper() and out[-2:-1].isupper():
            out = out[:-1] + p  # 'KIDNAP-' + 'PING'
        else:
            out = f"{out} {p}" if out else p
    return re.sub(r"\s+", " ", out)


# --------------------------------------------------------------------------- page


def _set_bounds(columns: list[Column], rules: Rules, y: float, page_w: float) -> None:
    mids = [(a.xc + b.xc) / 2 for a, b in zip(columns, columns[1:])]
    for i, c in enumerate(columns):
        c.left = mids[i - 1] if i else -1e6
        c.right = mids[i] if i < len(mids) else 1e6
    # snap to the ruled cell around the column number, when it isolates this column
    for c in columns:
        ext = None
        left = [x for x, a, b in rules.vert if x <= c.xc and a - 2 <= y <= b + 2]
        right = [x for x, a, b in rules.vert if x >= c.xc and a - 2 <= y <= b + 2]
        if left and right:
            ext = (max(left), min(right))
        if ext and not [o for o in columns if o is not c and ext[0] <= o.xc <= ext[1]]:
            c.left, c.right = ext
    for a, b in zip(columns, columns[1:]):  # snapped and unsnapped neighbours must not overlap or gap
        if a.right != b.left:
            a.right = b.left = (a.right + b.left) / 2 if a.right > b.left else (b.left if b.left < 1e5 else a.right)
    columns[0].left = min(columns[0].left, 0)
    columns[-1].right = max(columns[-1].right, page_w)


FOOTER_RES = [
    re.compile(r"^(accidental deaths|crime in india|prison statistics).{0,40}\b(19|20)\d\d\b.{0,12}$", re.I),
    re.compile(r"^\[?\s*\d{1,4}\s*\]?$"),
    re.compile(r"^page\s*:?\s*\d+", re.I),
    re.compile(r"^[-–]?\s*\d{1,4}\s*[-–]?$"),
    re.compile(r"^table\b.*\bpage\b", re.I),  # 'TABLE 3.3 - Page 1 of 3'
    re.compile(r"^https?://\S+(\s+\d+/\d+)?$", re.I),  # browser-printed pages
    re.compile(r"^\d{1,2}/\d{1,2}/\d{4}\b"),  # browser print header: date + page title
    re.compile(r"^(N\.?C\.?R\.?B\.?|National Crime Records Bureau)\b.{0,60}$", re.I),
]
BROWSER_DATE_RE = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}\s+")


def is_page_furniture(text: str) -> bool:
    t = text.strip()
    return any(r.match(t) for r in FOOTER_RES)


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


def _split_title(above: list[list[Word]], ref_size: float) -> tuple[str, str, bool, list[list[Word]]]:
    """Separate title lines from header lines. Returns (table_no, title, contd, header lines)."""
    title_lines: list[str] = []
    header_lines: list[list[Word]] = []
    in_header = False
    for ln in above:
        text = line_text(ln)
        if is_page_furniture(text):
            continue
        if BROWSER_DATE_RE.match(text):  # 'dd/mm/yyyy <page title>' printed by a browser
            continue
        size = statistics.median([w.size for w in ln])
        blocks = word_blocks(ln)
        multi = len(blocks) > 1 and max(b[0].x0 - a[-1].x1 for a, b in zip(blocks, blocks[1:])) > 12
        if not in_header:
            bigger = size > ref_size + 0.75
            if TABLE_RE.match(text) or bigger or (not multi and not header_lines and (not title_lines or len(ln) >= 4)):
                title_lines.append(text)
                continue
            in_header = True
        header_lines.append(ln)
    title = " ".join(title_lines)
    # keep only the last table heading if stray text precedes it
    starts = [m.start() for m in re.finditer(r"\b(TABLE|Table)\s*[-–:]?\s*\d", title)]
    if starts and starts[-1] > 0:
        title = title[starts[-1] :]
    m = TABLE_RE.match(title)
    table_no = re.sub(r"\s+", "", m.group(2)).strip("-.") if m else ""
    contd = bool(CONTD_RE.search(title))
    title = CONTD_RE.sub(" ", title[m.end() :] if m else title)
    title = re.sub(r"\s+", " ", title).strip(" -–:.")
    return table_no, title, contd, header_lines


def _segment(
    page: fitz.Page,
    page_no: int,
    above: list[list[Word]],
    columns: list[Column],
    anchor_y: float | None,
    below: list[list[Word]],
    inferred: bool,
    carry: PageTable | None = None,
    more_below: bool = False,
) -> tuple[PageTable | None, int]:
    """Build one table segment. Returns it and the number of ``below`` lines it consumed (data + notes)."""
    ref = [w.size for ln in below[:10] for w in ln] or [8]
    table_no, title, contd, header_lines = _split_title(above, statistics.median(ref))
    rules = Rules()
    if carry is None:
        y_anchor = anchor_y if anchor_y is not None else (below[0][0].y0 if below else 0)
        if header_lines:
            y0 = min(w.y0 for ln in header_lines for w in ln) - 3
            rules = Rules.from_page(page, y0, y_anchor + 6)
        _set_bounds(columns, rules, y_anchor, page.rect.width)
        if header_lines:
            assign_headers(columns, header_lines, rules)
    else:
        _set_bounds(columns, rules, 0, page.rect.width)
        table_no, title, contd = carry.table_no, "", True

    body: list[tuple[float, dict[int, list[Word]]]] = []
    for ln in below:
        if TABLE_RE.match(line_text(ln)):
            break  # the next table's heading
        by_col: dict[int, list[Word]] = {}
        for w in ln:
            col = next((c for c in columns if c.left <= w.xc < c.right), None)
            if col is None:
                col = min(columns, key=lambda c: abs(c.xc - w.xc))
            by_col.setdefault(col.id, []).append(w)
        body.append((_line_y(ln), by_col))

    if carry is not None:
        label_cols = list(carry.label_cols)
    else:
        # which columns hold numbers?
        stats = {c.id: [0, 0] for c in columns}
        for _, by_col in body:
            for cid, ws in by_col.items():
                stats[cid][1] += 1
                if all(is_cell(w.text) for w in ws):
                    stats[cid][0] += 1
        numeric = {cid for cid, (n, tot) in stats.items() if tot and n / tot >= 0.6}
        # label columns are the leading non-numeric ones, plus a leading serial-number column
        label_cols = []
        for c in columns:
            hdr = " ".join(c.header).lower()
            is_serial = bool(re.search(r"\b(s[lr]?\.?\s*no|sl\.?|s\.?\s*n\.?|serial)\b", hdr)) or (
                c is columns[0] and len(columns) > 2 and c.id == 1 and not inferred
            )
            if c.id not in numeric or (is_serial and not label_cols):
                label_cols.append(c.id)
            else:
                break
        if not label_cols:
            label_cols = [columns[0].id]
        if not body:
            # header only (its rows are overleaf): the label columns are the ones before the numbering jumps
            ids = [c.id for c in columns]
            jump = next((k for k in range(1, len(ids)) if ids[k] - ids[k - 1] > 1), None)
            label_cols = ids[:jump] if jump else ids[: 2 if ids[:2] == [1, 2] and len(ids) > 2 else 1]
    data_cols = [c.id for c in columns if c.id not in label_cols]
    if not data_cols:
        return None, 0

    rows: list[Row] = []
    notes: list[str] = []
    section = carry.rows[-1].section if carry is not None and carry.rows else ""
    pending: list[tuple[float, str]] = []  # label-only lines waiting for an owner
    pitches = [b[0] - a[0] for a, b in zip(body, body[1:]) if 0 < b[0] - a[0] < 60]
    pitch = statistics.median(pitches) if pitches else 12.0
    last_data_idx = max((i for i, (_, bc) in enumerate(body) if _has_data(bc, data_cols)), default=-1)
    serial_col = label_cols[0] if len(label_cols) > 1 else None
    serial_re = re.compile(r"\d{1,4}[.)]?|\(?[ivxlc]+\)|[A-Za-z][.)]")
    consumed = 0

    for i, (y, by_col) in enumerate(body):
        line_words = sorted((w for ws in by_col.values() for w in ws), key=lambda w: w.x0)
        text = " ".join(w.text for w in line_words)
        if i > last_data_idx:
            # trailing prose belongs to this table only while it looks like notes;
            # when another table follows on the page, anything else is that table's heading
            if more_below and not (NOTE_START_RE.match(text) or (notes and len(word_blocks(line_words)) == 1 and len(line_words) > 3)):
                break
            notes.append(text)
            consumed = i + 1
            continue
        consumed = i + 1
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
            sw = [w for w in by_col.get(serial_col, []) if serial_re.fullmatch(w.text)]
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
                limit = 1.6 * pitch if not label else 0.8 * pitch
                take = [t for py, t in pending if y - py <= limit]
                for py, t in pending:
                    if y - py > limit:
                        section = t
                row.label = " ".join(take + ([label] if label else []))
            else:
                for _, t in pending:
                    section = t
            row.section = section
            pending = []
            rows.append(row)
        elif label or serial or cells:
            if cells:  # prose line that happens to contain a number
                label = text
            ltext = (serial + " " + label).strip() if not label else label
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
                prev.label = (prev.label + " " + ltext).strip()  # continuation below the numbers
                if serial and not prev.serial:
                    prev.serial = serial
            else:
                pending.append((y, ltext))
    for _, t in pending:
        notes.insert(0, t)
    notes = [n for n in notes if n.strip() and not is_page_furniture(n)]
    pt = PageTable(page_no, table_no, title, contd, columns, label_cols, rows, notes, inferred)
    pt.headless = not rows
    pt.carried = carry is not None
    return pt, consumed


def _clone_columns(prev: PageTable, inferred: list[Column]) -> list[Column] | None:
    """Columns of a headerless continuation page: previous ids/headers at this page's x positions."""
    prev_data = [c for c in prev.columns if c.id not in prev.label_cols]
    data = inferred[1:]
    if len(data) != len(prev_data):
        return None
    labels = [c for c in prev.columns if c.id in prev.label_cols]
    cols = []
    if len(labels) > 1:
        # keep the relative layout of the label columns, shifted to this page
        shift = data[0].xc - prev_data[0].xc
        cols = [Column(c.id, c.xc + shift, header=list(c.header)) for c in labels]
    else:
        cols = [Column(labels[0].id, inferred[0].xc, header=list(labels[0].header))]
    cols += [Column(p.id, d.xc, header=list(p.header)) for p, d in zip(prev_data, data)]
    return cols


def extract_page(page: fitz.Page, page_no: int, words: list[Word] | None = None, prev: PageTable | None = None) -> list[PageTable]:
    """All table segments on a page, in reading order.

    ``prev`` is the last segment of the previous page; a page (or the top of a
    page) that carries on its rows without repeating the header inherits its
    columns.
    """
    words = page_words(page) if words is None else words
    lines = [ln for ln in group_lines(words) if not is_page_furniture(line_text(ln))]
    if not lines:
        return []
    anchors = find_anchors(lines)
    out: list[PageTable] = []
    start = 0

    def headless(upto: int) -> None:
        """Rows before the first heading on the page, continuing the previous table."""
        nonlocal start, prev
        region = lines[start:upto]
        cut = next((k for k, ln in enumerate(region) if TABLE_RE.match(line_text(ln))), len(region))
        region = region[:cut]
        if sum(numeric_line(ln) for ln in region) < 2:
            return
        cols = infer_columns(region)
        if cols is None:
            return
        first = next(k for k, ln in enumerate(region) if numeric_line(ln))
        if prev is not None and prev.columns:
            cloned = _clone_columns(prev, cols)
            if cloned is not None:
                # label-only lines directly above the first numbers (section headings) stay with the body
                pt, used = _segment(page, page_no, [], cloned, None, region, False, carry=prev)
                if pt is not None and pt.rows:
                    out.append(pt)
                    prev = pt
                    start += used
                return
        if not anchors:
            pt, used = _segment(page, page_no, region[:first], cols, None, region[first:], True)
            if pt is not None and pt.rows:
                out.append(pt)
                prev = pt
                start += first + used

    headless(anchors[0][0] if anchors else len(lines))
    for k, (ai, columns, stray) in enumerate(anchors):
        if ai < start:
            continue
        end = anchors[k + 1][0] if k + 1 < len(anchors) else len(lines)
        above = lines[start:ai] + ([stray] if stray else [])
        pt, used = _segment(page, page_no, above, columns, _line_y(lines[ai]), lines[ai + 1 : end], False, more_below=k + 1 < len(anchors))
        if pt is None:
            start = ai + 1
            continue
        # a header at the foot of a page whose rows follow overleaf is kept so the next page can inherit it
        out.append(pt)
        prev = pt
        start = ai + 1 + used
    return out


def extract_pdf_pages(path: str) -> tuple[list[PageTable], int, int]:
    """Table segments of a PDF in order, the page count, and the number of pages with no text layer."""
    doc = fitz.open(path)
    out: list[PageTable] = []
    no_text = 0
    prev: PageTable | None = None
    for i, page in enumerate(doc):
        words = page_words(page)
        if len(words) < 5:
            no_text += 1
            continue
        segs = extract_page(page, i + 1, words, prev)
        if segs:
            prev = segs[-1]
        out.extend(segs)
    n = len(doc)
    doc.close()
    return out, n, no_text
