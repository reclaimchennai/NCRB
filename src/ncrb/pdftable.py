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
TABLE_RE = re.compile(
    r"^\s*(?:Additional\s+|ADDITIONAL\s+)?(TABLE|Table)\s*[-–:]?\s*"
    r"([0-9]+[A-Z]?(?:\s*[.\-]\s*[0-9]+[A-Z]?)*(?:\s*\((?:[A-Za-z]|[ivx]{1,4}|\d{1,2})\))?(?:\s*[A-Z](?![A-Za-z]))?|[IVXL]{1,6}\b)"
)
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
    conf: float = 1.0  # OCR confidence; 1.0 for words from a text layer

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
    conf: dict[int, float] = field(default_factory=dict)  # column id -> OCR confidence (scanned pages only)


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
    ocr: bool = False
    min_conf: float = 1.0
    unlabelled: bool = False  # right-hand half of a two-page table: figures only, rows follow the left page


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
    if t.startswith("-"):
        neg, t = not neg, t[1:]
    if not re.fullmatch(r"\d+\.?\d*|\.\d+", t):
        return None  # also keeps out 'nan' and 'inf', which float() would accept
    v = float(t)
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
    return _join_touching(out)


def _join_touching(words: list[Word]) -> list[Word]:
    """Rejoin tokens that the PDF splits mid-word ('3' + '2' for 32, 'CHHA' + 'TTISGARH').

    Some producers position glyph runs separately; text extraction then sees a
    word break where there is no space at all. Two tokens on one baseline whose
    boxes touch are one token.
    """
    words.sort(key=lambda w: (round(w.y1), w.x0))
    out: list[Word] = []
    for w in words:
        p = out[-1] if out else None
        if p is not None and abs(p.y1 - w.y1) < 1.0 and -1.5 <= w.x0 - p.x1 <= 0.12 * (w.size or 8):
            out[-1] = Word(p.x0, min(p.y0, w.y0), w.x1, max(p.y1, w.y1), p.text + w.text, p.size, p.bold)
        else:
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
        tol = max(2.0, 0.45 * (w.size or 8))
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


LETTERED = 1_000_000  # ids above this encode a lettered column number: '9a' -> 1_000_901


def col_id(base: str, suffix: str = "") -> int:
    """Integer id for a printed column number; sub-columns such as '9a', '9b' get ids of their own."""
    if not suffix:
        return int(base)
    return LETTERED + int(base) * 100 + (ord(suffix.lower()) - 96)


def col_label(cid: int) -> str:
    """The column number as printed ('9a'), from its integer id."""
    if cid > LETTERED:
        n = cid - LETTERED
        return f"{n // 100}{chr(96 + n % 100)}"
    return str(cid)


COLNUM_PART = r"[(\[]?(\d{1,3})([A-Za-z]?)[)\]]"


def _split_colnums(line: list[Word]) -> tuple[list[tuple[int, float, float]], list[Word]]:
    """Column numbers on a line as (id, x0, x1), plus the words that are not column numbers.

    Handles numbers run together as '(3)(4)', square brackets, and lettered sub-columns '(9a)'.
    """
    out, others = [], []
    for w in line:
        parts = re.findall(COLNUM_PART, w.text)
        if parts and not re.sub(COLNUM_PART, "", w.text).strip():
            width = (w.x1 - w.x0) / len(parts)
            out += [(col_id(n, sfx), w.x0 + i * width, w.x0 + (i + 1) * width) for i, (n, sfx) in enumerate(parts)]
        else:
            others.append(w)
    return out, others


OCR_COLNUM_RE = re.compile(r"^[(\[{|]?\s*([0-9IlOo]{1,4})\s*[)\]}|]$|^[(\[{]\s*([0-9IlOo]{1,3})$")


def repair_ocr_anchor(line: list[Word]) -> None:
    """Rewrite an OCR'd column-number row such as '11) 12) (3) 14)' to '(1) (2) (3) (4)' in place."""
    hits = [(w, OCR_COLNUM_RE.match(w.text)) for w in line]
    good = [(w, m) for w, m in hits if m]
    if len(good) < 3 or len(good) < 0.7 * len(line):
        return
    prev = 0
    for w, m in good:
        digits = (m.group(1) or m.group(2)).replace("I", "1").replace("l", "1").replace("O", "0").replace("o", "0")
        cands = [int(digits)]
        if not w.text.startswith(("(", "[", "{")) and digits.startswith("1") and len(digits) >= 2:
            cands.append(int(digits[1:]))  # '(' misread as '1'
        n = prev + 1 if prev + 1 in cands else min(cands, key=lambda c: abs(c - prev - 1))
        w.text = f"({n})"
        prev = n


def find_anchors(lines: list[list[Word]]) -> list[tuple[int, list[Column], list[Word]]]:
    """Every column-number line on the page: (line index, columns, header words sharing the line)."""
    out = []
    for i, line in enumerate(lines):
        nums, others = _split_colnums(line)
        bare = False
        digits = [w for w in line if re.fullmatch(r"\d{1,3}\.?", w.text)]
        lettered = [w for w in line if re.fullmatch(r"\d{1,3}[a-z]", w.text)]  # sub-columns: '9a 10a 11a'
        junk = [w for w in line if w not in digits and w not in lettered]
        if len(nums) < 2 and len(digits) + len(lettered) >= 4 and len(digits) >= 2 and all(len(w.text) <= 2 and w.conf < 0.9 for w in junk) and len(digits) + len(lettered) >= 0.7 * len(line):
            # older volumes number the columns without brackets: '1 2 3 4 5'
            vals = [int(w.text.rstrip(".")) for w in digits]
            steps = [b - a for a, b in zip(vals, vals[1:])]
            # consecutive, except for the jump after the row-label columns on continuation pages ('1 2 12 13 14')
            jumps = [k for k, st in enumerate(steps) if st > 1]
            if all(st > 0 for st in steps) and (not jumps or (jumps == [1] and vals[:2] == [1, 2]) or jumps == [0]) and i + 1 < len(lines):
                toks = sorted(digits + lettered, key=lambda w: w.x0)
                nums = [(col_id(w.text.rstrip(".")[:-1], w.text[-1]) if w in lettered else int(w.text.rstrip(".")), w.x0, w.x1) for w in toks]
                others, bare, line = [], True, toks
        if len(nums) < 2 or len(nums) < 0.6 * len(line):
            continue
        ids = [n[0] for n in nums if n[0] < LETTERED]  # lettered sub-columns sit outside the running order
        if len(ids) < 2 or ids != sorted(ids) or len({n[0] for n in nums}) != len(nums):
            continue
        # must be (nearly) consecutive; '(1) (2)' for the label columns may precede a jump on contd pages
        steps = [b - a for a, b in zip(ids, ids[1:])]
        if sum(1 for s in steps if s == 1) < max(1, len(steps) - 2):
            continue
        if len(nums) == 2 and (ids != [1, 2] or others):
            continue  # too weak to trust
        if bare and out:
            continue  # only the first bare row on a page can be a column-number row
        cols = [Column(n, (a + b) / 2) for n, a, b in nums]
        # a single number missing from the row (dropped by OCR, or never printed) leaves a double-width gap
        gaps = [b.xc - a.xc for a, b in zip(cols, cols[1:]) if b.id - a.id == 1 and a.id >= 2]
        if len(gaps) >= 2 and not any(c.id > LETTERED for c in cols):
            step = statistics.median(gaps)
            filled = [cols[0]]
            for c in cols[1:]:
                if c.id - filled[-1].id == 2 and c.xc - filled[-1].xc > 1.6 * step:
                    filled.append(Column(c.id - 1, c.xc - step))
                filled.append(c)
            cols = filled
        out.append((i, cols, others))
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
    cols[0].right = data[0][0] - 1  # where the figures begin
    return cols


def body_line(line: list[Word], edge: float, need_label: bool = False) -> bool:
    """A row of figures (as opposed to a heading line that happens to contain numbers)."""
    data = [w for w in line if w.x0 >= edge - 1]
    cells = sum(is_cell(w.text) for w in data)
    if cells < 1 or len(data) - cells > max(1, 0.15 * len(data)):
        return False
    if need_label:
        label = [w for w in line if w.x0 < edge - 1 and re.search(r"[A-Za-z]", w.text)]
        return bool(label) and any(is_num(w.text) for w in data)
    return True


# --------------------------------------------------------------------------- header


@dataclass
class Rules:
    """Ruling lines and cell edges of a page region, used to recover merged header cells."""

    vert: list[tuple[float, float, float]] = field(default_factory=list)  # x, y0, y1
    horiz: list[tuple[float, float, float]] = field(default_factory=list)  # y, x0, x1
    last_source: str = ""  # which kind of rule answered the last cell() query

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
        # a rule is often drawn in pieces; only the joined-up line says what it spans
        merged: list[list[float]] = []
        for y, a, b in sorted(r.horiz, key=lambda h: (round(h[0]), h[1])):
            if merged and abs(merged[-1][0] - y) < 0.8 and a <= merged[-1][2] + 1.5:
                merged[-1][2] = max(merged[-1][2], b)
            else:
                merged.append([y, a, b])
        r.horiz = [tuple(m) for m in merged]
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
        below = [(hy, a, b) for hy, a, b in self.horiz if 0 < hy - y <= 22 and a - 3 <= xc <= b + 3 and (b - a) < 0.95 * span]
        if below:
            y0 = min(h[0] for h in below)
            near = [h for h in below if h[0] - y0 <= 1.5]
            holds = [h for h in near if h[1] - 4 <= x0 and x1 <= h[2] + 4]
            _, a, b = min(holds, key=lambda h: h[2] - h[1]) if holds else max(near, key=lambda h: h[2] - h[1])
            # a spanner's underline is centred on its text; a longer rule that merely passes below is not its cell
            if abs((a + b) / 2 - xc) <= 0.1 * (b - a) + 3:
                cands.append((a, b))
        if not cands:
            return None
        # vertical rules are exact for the text's own row; fall back to the underline only
        # when they merely give the outline of the whole table
        if len(cands) == 2 and cands[0][1] - cands[0][0] >= 0.95 * span:
            self.last_source = "h"
            return cands[1]
        self.last_source = "v" if left and right and cands[0] == (max(left), min(right)) else "h"
        if self.last_source == "v" and cands[0][1] - cands[0][0] >= 0.95 * span:
            return None  # just the frame around the table
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


@dataclass
class _Block:
    line: int
    y: float
    x0: float
    x1: float
    text: str
    size: float
    ext: tuple[float, float] | None = None  # cell extent from ruling lines
    idx: tuple[int, ...] = ()
    parts: list = field(default_factory=list)
    from_underline: bool = False

    @property
    def xc(self) -> float:
        return (self.x0 + self.x1) / 2


def _slots(columns: list[Column]) -> list[tuple[float, float]]:
    """x range owned by each column: midpoints between neighbouring column centres."""
    mids = [(a.xc + b.xc) / 2 for a, b in zip(columns, columns[1:])]
    out = []
    for i, c in enumerate(columns):
        left = mids[i - 1] if i else c.xc - (mids[0] - c.xc if mids else 30)
        right = mids[i] if i < len(mids) else c.xc + (c.xc - mids[-1] if mids else 30)
        out.append((left, right))
    return out


def assign_headers(columns: list[Column], header_lines: list[list[Word]], rules: Rules) -> None:
    """Fill ``Column.header`` with the header path (outermost group first).

    Where ruling lines box the header cells they decide which columns a heading
    spans. Otherwise the layout is read geometrically: a heading belongs to the
    columns it lies over, a heading line continued on the next line is joined,
    and a spanning heading is widened to take in the whole of any group beneath
    it that it partly covers (spanners are centred, so their text is narrower
    than their span).
    """
    full = (min(c.xc for c in columns), max(c.xc for c in columns))
    slots = _slots(columns)
    lines: list[list[_Block]] = []
    for li, line in enumerate(header_lines):
        row = []
        for ws in word_blocks(line):
            b = _Block(li, _line_y(ws), ws[0].x0, ws[-1].x1, " ".join(w.text for w in ws), ws[0].size or 8)
            b.parts = [(b.y, b.x0, b.text)]
            b.ext = rules.cell(b.x0, b.x1, b.y, full)
            b.from_underline = b.ext is not None and rules.last_source == "h"
            row.append(b)
        # an underline running beneath several headings of a line is not a cell boundary for any of them
        for b in row:
            if b.from_underline and any(o is not b and b.ext[0] <= o.xc <= b.ext[1] for o in row):
                b.ext = None
        lines.append(row)

    # --- join a heading's continuation line to it (no rules to tell us)
    for li in range(1, len(lines)):
        for parent in [b for b in lines[li - 1] if b.ext is None]:
            under = [b for b in lines[li] if parent.x0 - 2 <= b.xc <= parent.x1 + 2]
            if len(under) != 1:
                continue
            child = under[0]
            if child.ext is not None or child.y - parent.parts[-1][0] > 1.6 * parent.size:
                continue
            if abs(child.xc - parent.xc) > 0.15 * (parent.x1 - parent.x0) + 3 or child.x1 - child.x0 > (parent.x1 - parent.x0) + 12:
                continue
            parent.parts += child.parts
            parent.x0, parent.x1 = min(parent.x0, child.x0), max(parent.x1, child.x1)
            lines[li].remove(child)
            lines[li].append(parent)  # so a third line can chain on
            lines[li - 1].remove(parent)
        lines[li].sort(key=lambda b: b.x0)

    # --- columns covered by each heading
    for row in lines:
        last = -1
        for b in row:
            idx: list[int] = []
            if b.ext is not None:
                idx = [i for i, c in enumerate(columns) if b.ext[0] - 1 <= c.xc <= b.ext[1] + 1]
            if not idx:
                b.ext = None
                for i, (l, r) in enumerate(slots):
                    ov = min(b.x1, r) - max(b.x0, l)
                    if ov >= 0.3 * (r - l) or (l <= b.x0 and b.x1 <= r):
                        idx.append(i)
                if not idx:
                    idx = [max(range(len(slots)), key=lambda i: min(b.x1, slots[i][1]) - max(b.x0, slots[i][0]))]
                if len(idx) == 1 and idx[0] <= last and last + 1 < len(columns):
                    idx = [last + 1]  # headings on one line map left to right
            last = max(last, idx[-1])
            b.idx = tuple(idx)

    # --- a centred spanner is narrower than its span: widen the topmost headings symmetrically
    n = len(columns)
    gaps = sorted(b.xc - a.xc for a, b in zip(columns, columns[1:]))
    pitch = gaps[len(gaps) // 2] if gaps else 40.0
    for li, row in enumerate(lines):
        above = {i for r2 in lines[:li] for o in r2 for i in o.idx}
        lower = {i for r2 in lines[li + 1 :] for o in r2 for i in o.idx}
        for b in row:
            if b.ext is not None or not set(b.idx) <= lower:
                continue
            others = {i for o in row if o is not b for i in o.idx}
            lo, hi = b.idx[0], b.idx[-1]
            best = None
            for i in range(lo, -1, -1):
                if i in others or i in above or i not in lower:
                    break
                for j in range(hi, n):
                    if j in others or j in above or j not in lower:
                        break
                    if (i, j) == (lo, hi) or abs((columns[i].xc + columns[j].xc) / 2 - b.xc) > 0.35 * pitch:
                        continue
                    if best is None or j - i > best[1] - best[0]:
                        best = (i, j)
            if best:
                b.idx = tuple(range(best[0], best[1] + 1))

    # --- widen ruleless spanners over the groups beneath them
    groups: list[tuple[int, ...]] = []
    for row in reversed(lines):
        for b in row:
            if b.ext is None and len(b.idx) > 1:
                cover = set(b.idx)
                for g in groups:
                    if len(g) > 1 and cover & set(g):
                        cover |= set(g)
                b.idx = tuple(range(min(cover), max(cover) + 1))
        groups += [b.idx for b in row]

    cells: dict[tuple[int, ...], list[tuple[float, float, str]]] = {}
    for row in lines:
        for b in row:
            cells.setdefault(b.idx, []).extend(b.parts)
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
    re.compile(r"^(accidental deaths|crime in india|prison statistics).{0,40}\b(19|20)\d\d\b.{0,30}$", re.I),
    re.compile(r"^[\[(]?\s*\d{1,4}\s*[\])]?$"),
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


SECTION_PREFIX_RE = re.compile(r"^\s*((?:STATES?|UNION\s+TERRITOR(?:Y|IES)|UTS?|CITIES|CITY)\s*:)\s*", re.I)
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


def _split_title(above: list[list[Word]], ref_size: float, grid_top=None) -> tuple[str, str, bool, list[list[Word]]]:
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
        if not in_header and grid_top is not None and not TABLE_RE.match(text) and grid_top(ln):
            in_header = True
        if not in_header:
            bigger = size > ref_size + 0.75
            if TABLE_RE.match(text) or bigger or (not multi and not header_lines and (not title_lines or len(ln) >= 4)):
                title_lines.append(text)
                continue
            in_header = True
        header_lines.append(ln)
    title = " ".join(title_lines)
    # keep only the last table heading if stray text precedes it
    starts = [m.start() for m in re.finditer(r"\b(?:Additional\s+)?(TABLE|Table)\s*[-–:]?\s*(\d|[IVXL]+\b)", title)]
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
    ocr: bool = False,
) -> tuple[PageTable | None, int]:
    """Build one table segment. Returns it and the number of ``below`` lines it consumed (data + notes)."""
    ref = [w.size for ln in below[:10] for w in ln] or [8]
    rules = Rules()
    grid_top = None
    y_anchor = anchor_y if anchor_y is not None else (below[0][0].y0 if below else 0)
    if carry is None and above and not ocr:
        rules = Rules.from_page(page, min(w.y0 for ln in above for w in ln) - 3, y_anchor + 6)
        if len({round(x) for x, _, _ in rules.vert}) >= 3:
            first_x = columns[0].xc

            def grid_top(ln: list[Word]) -> bool:
                """True for a line in a ruled cell that spans the figures but not the row-label column: a spanning heading."""
                y = _line_y(ln)
                left = [x for x, a, b in rules.vert if x <= ln[0].x0 + 2 and a - 2 <= y <= b + 2]
                return bool(left) and max(left) > first_x + 1

    table_no, title, contd, header_lines = _split_title(above, statistics.median(ref), grid_top)
    if carry is None:
        if header_lines:
            y0 = min(w.y0 for ln in header_lines for w in ln) - 3
            rules.vert = [v for v in rules.vert if v[2] >= y0]
            rules.horiz = [h for h in rules.horiz if h[0] >= y0]
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

    _realign(body, columns)

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
        unlabelled = not label_cols and columns[0].id > 2 and len(numeric) >= 0.8 * len(columns)
        if not label_cols and not unlabelled:
            label_cols = [columns[0].id]
        if not body:
            # header only (its rows are overleaf): the label columns are the ones before the numbering jumps
            ids = [c.id for c in columns]
            jump = next((k for k in range(1, len(ids)) if ids[k] - ids[k - 1] > 1 and ids[k] < LETTERED), None)
            label_cols = ids[:jump] if jump else ids[: 2 if ids[:2] == [1, 2] and len(ids) > 2 else 1]
    data_cols = [c.id for c in columns if c.id not in label_cols]
    if not data_cols:
        return None, 0

    rows: list[Row] = []
    notes: list[str] = []
    section = carry.rows[-1].section if carry is not None and carry.rows else ""
    pending: list[tuple[float, str]] = []  # label-only lines waiting for an owner
    data_ys = [y for y, bc in body if _has_data(bc, data_cols)]
    pitches = [b - a for a, b in zip(data_ys, data_ys[1:]) if 0 < b - a < 60]
    pitch = statistics.median(pitches) if pitches else 12.0  # distance between rows of figures
    last_data_idx = max((i for i, (_, bc) in enumerate(body) if _has_data(bc, data_cols)), default=-1)
    serial_col = label_cols[0] if len(label_cols) > 1 else None
    serial_re = re.compile(r"\d{1,4}[.)]?|\(?[ivxlc]+\)|[A-Za-z][.)]")
    consumed = 0
    low = 1.0  # lowest OCR confidence among the cells read

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
        confs: dict[int, float] = {}
        spill: list[Word] = []
        for cid in data_cols:
            ws = by_col.get(cid, [])
            if ocr:
                for w in ws:
                    w.text = fix_ocr_number(w.text)
                if len(ws) > 1 and any(is_num(w.text) for w in ws):
                    ws = [w for w in ws if w.text != "-"]  # specks beside a figure
            vals = [w for w in ws if is_cell(w.text)]
            junk = [w for w in ws if not is_cell(w.text)]
            if ocr and junk and cid != data_cols[0] and len(junk) <= 2:
                # a misread number stays in its cell as raw text instead of leaking into the row label
                vals = ws
            else:
                spill += junk
            if vals:
                cells[cid] = " ".join(w.text for w in vals) if len(vals) > 1 else vals[0].text
                if ocr:
                    confs[cid] = min(w.conf for w in vals)
                    low = min(low, confs[cid])
        serial = ""
        if serial_col is not None:
            sw = [w for w in by_col.get(serial_col, []) if serial_re.fullmatch(w.text)]
            if sw:
                serial = sw[0].text.rstrip(".") if sw[0].text.startswith("(") else sw[0].text.rstrip(".)")
                label_words = [w for w in label_words if w is not sw[0]]
        elif label_words and re.fullmatch(r"\d{1,3}[.)]?", label_words[0].text) and len(label_words) > 1:
            serial = label_words[0].text.rstrip(".)")
            label_words = label_words[1:]
        if ocr:
            label_words = strip_leader_junk(sorted(label_words + spill, key=lambda w: w.x0))
            spill = []
        label = " ".join(w.text for w in sorted(label_words + spill, key=lambda w: w.x0)).strip()
        if ocr:
            label = re.sub(r"\bT[oO0][tTrR][aA][lLnNI1]\b", "TOTAL", label)  # small capitals defeat the recogniser
        if cells and _has_data(by_col, data_cols):
            row = Row(label, serial, section, cells, page_no, y, confs)
            if not label and not pending and rows and y - rows[-1].y <= 1.2 * pitch:
                # a second line of figures under a row (e.g. rates printed beneath counts)
                base = re.sub(r" \[line \d+\]$", "", rows[-1].label)
                k = int(m.group(1)) + 1 if (m := re.search(r" \[line (\d+)\]$", rows[-1].label)) else 2
                row.label = f"{base} [line {k}]"
            # wrapped label: text lines just above belong to a row whose own line has no label
            if pending and pending[-1][0] > y - 0.8 * pitch:
                limit = 0.8 * pitch
                take = [t for py, t in pending if y - py <= limit]
                for py, t in pending:
                    if y - py > limit:
                        section = t
                row.label = " ".join(take + ([label] if label else []))
            else:
                for _, t in pending:
                    section = t
            m = SECTION_PREFIX_RE.match(row.label)
            if m and m.end() < len(row.label):
                section, row.label = m.group(1).strip(), row.label[m.end():].strip()
            if not row.serial and (m := re.match(r"^(\d{1,3})[.)]?\s+(?=[A-Za-z])", row.label)) and serial_col is not None:
                row.serial, row.label = m.group(1), row.label[m.end():]
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
    pt.ocr = ocr
    pt.min_conf = low
    pt.unlabelled = not label_cols
    return pt, consumed


def _realign(body: list[tuple[float, dict[int, list[Word]]]], columns: list[Column]) -> None:
    """Move figures that landed in a neighbouring column because the column is right-aligned.

    Column positions come from the centred column numbers, but the figures are
    usually right-aligned, so a short number near a boundary can sit closer to
    the next column's centre. Where a column's figures share a right edge, that
    edge decides.
    """
    edges: dict[int, float] = {}
    for c in columns:
        x1 = sorted(w.x1 for _, bc in body for w in bc.get(c.id, []) if is_cell(w.text))
        if len(x1) < 4:
            continue
        med = x1[len(x1) // 2]
        if sum(abs(v - med) <= 1.5 for v in x1) >= 0.7 * len(x1):
            edges[c.id] = med
    if len(edges) < 2:
        return
    for _, bc in body:
        for cid in list(bc):
            for w in list(bc[cid]):
                if not is_cell(w.text) or (cid in edges and abs(w.x1 - edges[cid]) <= 2.0):
                    continue
                hit = [k for k, e in edges.items() if abs(w.x1 - e) <= 2.0]
                if len(hit) == 1 and hit[0] != cid:
                    bc[cid].remove(w)
                    if not bc[cid]:
                        del bc[cid]
                    bc.setdefault(hit[0], []).append(w)


def _add_label_columns(columns: list[Column], body: list[list[Word]]) -> list[Column]:
    """Give a continuation page its row-label columns when the column-number row omits them.

    Some volumes number only the data columns on '(Contd.)' pages ('12 13 14 ...') although the
    serial number and State/UT name are printed again. Without columns of their own those labels
    would be swallowed by the first data column.
    """
    if columns[0].id <= 2 or len(columns) < 2:
        return columns
    pitch = columns[1].xc - columns[0].xc
    edge = columns[0].xc - 0.6 * pitch
    rows = [ln for ln in body if sum(is_cell(w.text) for w in ln if w.x0 >= edge) >= 2]
    labelled = [ln for ln in rows if any(w.x1 < edge and re.search(r"[A-Za-z]{2}", w.text) for w in ln)]
    if len(rows) < 2 or len(labelled) < 0.5 * len(rows):
        return columns
    text_x = statistics.median([min(w.x0 for w in ln if w.x1 < edge and re.search(r"[A-Za-z]{2}", w.text)) for ln in labelled])
    serial = [w for ln in labelled for w in ln if w.x1 <= text_x and re.fullmatch(r"\d{1,3}[.)]?", w.text)]
    out = []
    if len(serial) >= 0.5 * len(labelled):
        out.append(Column(1, statistics.median([w.xc for w in serial])))
    text_right = statistics.median([max(w.x1 for w in ln if w.x1 < edge) for ln in labelled])
    out.append(Column(2, max((text_x + text_right) / 2, out[0].xc + 8 if out else 0)))
    return out + columns


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


def fix_ocr_number(t: str) -> str:
    """Undo the usual misreadings of digits in a numeric column ('ll' for 11, 'O' for 0, '20°' for 20)."""
    u = t.strip("'\"`:;*^|!")
    if u in ("°", "o", "O", "Q", "D", "()", "QO"):
        return "0"  # a lone zero is the digit OCR most often turns into something else
    u = u.strip("°")
    if u.endswith(")") and "(" not in u:
        u = u[:-1]
    if u.startswith("(") and ")" not in u:
        u = u[1:]
    if len(u) > 1 and u.endswith(".") and u[:-1].replace(",", "").isdigit():
        u = u[:-1]
    if re.fullmatch(r"[lI|!\]\[1]+", u):
        return "1" * len(u)
    if re.fullmatch(r"[0-9lIOoSsB,.()%\-]+", u) and re.search(r"\d", u):
        u = u.translate(str.maketrans("lIOoSsB", "1100558"))
    return u if is_cell(u) else t


def strip_leader_junk(words: list[Word]) -> list[Word]:
    """Drop what OCR makes of the dot leaders between a row label and its first figure."""
    for i in range(1, len(words)):
        tail = words[i:]
        gap = words[i].x0 - words[i - 1].x1
        leader = re.fullmatch(r"[.…·•,:;'`\"_\-]+", words[i].text) is not None
        if (leader or gap > 0.9 * (words[i].size or 8)) and not any(re.search(r"[A-Za-z]{4}", w.text) and w.conf >= 0.8 for w in tail):
            words = words[:i]
            break
    if words:
        words[-1].text = re.sub(r"[.…·•]{2,}$", "", words[-1].text) or words[-1].text
    return words


def clean_ocr_words(words: list[Word]) -> list[Word]:
    """Drop ruling-line artefacts ('|', '_') that OCR reads as characters."""
    out = []
    for w in words:
        if w.conf < 0.3 and not re.search(r"\d", w.text) and not re.fullmatch(r"[-—–_=~]{1,4}", w.text):
            continue
        t = w.text.strip("|¦")
        if re.fullmatch(r"[-—–_=~]{1,4}", t):
            t = "-"  # nil entries are printed as dashes of every length
        t = t.strip("_")
        t = re.sub(r"(?<=\d)[|](?=\d)", " ", t)
        # a raised decimal point in old typesetting is read as '-', ':' or a bullet: '(148-9)' is 148.9
        t = re.sub(r"^[(\[]?(\d{1,4})[-·•:](\d{1,2})[)\]]?$", r"(\1.\2)", t) if re.match(r"^[(\[]", t) or re.search(r"[)\]]$", t) else t
        t = t.replace("•", ".") if re.fullmatch(r"[(\d][\d,]*•\d+\)?", t) else t
        if not t or re.fullmatch(r"[|_\-—~=.:;'`]+", t) and t not in ("-", "--", ".."):
            continue
        parts = t.split()
        if len(parts) > 1:
            width = (w.x1 - w.x0) / len(t)
            pos = 0
            for part in parts:
                k = t.index(part, pos)
                out.append(Word(w.x0 + k * width, w.y0, w.x0 + (k + len(part)) * width, w.y1, part, w.size, w.bold, w.conf))
                pos = k + len(part)
        else:
            w.text = t
            out.append(w)
    return out


def extract_page(
    page: fitz.Page, page_no: int, words: list[Word] | None = None, prev: PageTable | None = None, ocr: bool = False
) -> list[PageTable]:
    """All table segments on a page, in reading order.

    ``prev`` is the last segment of the previous page; a page (or the top of a
    page) that carries on its rows without repeating the header inherits its
    columns.
    """
    words = page_words(page) if words is None else words
    if ocr:
        words = clean_ocr_words(words)
    lines = [ln for ln in group_lines(words) if not is_page_furniture(line_text(ln))]
    if not lines:
        return []
    if ocr:
        for ln in lines:
            repair_ocr_anchor(ln)
    anchors = find_anchors(lines)
    out: list[PageTable] = []
    start = 0

    def headless(upto: int) -> None:
        """Rows with no column-number row above them: a continuation of the previous table, or an unnumbered table."""
        nonlocal start, prev
        pos = start
        while pos < upto:
            region = lines[pos:upto]
            # a table heading that is not the first line ends this stretch
            cut = next((k for k, ln in enumerate(region) if k > 0 and TABLE_RE.match(line_text(ln))), len(region))
            region = region[:cut]
            pos += len(region)
            if sum(numeric_line(ln) for ln in region) < 2:
                continue
            cols = infer_columns(region)
            if cols is None:
                continue
            edge = cols[0].right
            first = next((k for k, ln in enumerate(region) if body_line(ln, edge, need_label=True)), None)
            if first is None:
                first = next((k for k, ln in enumerate(region) if body_line(ln, edge)), None)
            if first is None:
                continue
            cols = infer_columns(region[first:]) or cols
            head = region[:first]
            # a lone short line above the figures is a section heading ('CITIES:'), not a column header
            has_header = len(head) > 1 or any(len(word_blocks(ln)) > 1 or TABLE_RE.match(line_text(ln)) for ln in head)
            pt = None
            if prev is not None and prev.columns and not has_header:
                cloned = _clone_columns(prev, cols)
                if cloned is not None:
                    pt, _ = _segment(page, page_no, [], cloned, None, region, False, carry=prev, ocr=ocr)
            elif not anchors:
                pt, _ = _segment(page, page_no, head, cols, None, region[first:], True, ocr=ocr)
            if pt is not None and pt.rows:
                out.append(pt)
                prev = pt
                start = pos  # only lines actually turned into rows are consumed

    headless(anchors[0][0] if anchors else len(lines))
    for k, (ai, columns, stray) in enumerate(anchors):
        if ai < start:
            continue
        end = anchors[k + 1][0] if k + 1 < len(anchors) else len(lines)
        above = lines[start:ai] + ([stray] if stray else [])
        if not ocr:  # scanned right-hand pages really have no labels; OCR noise must not invent them
            columns = _add_label_columns(columns, lines[ai + 1 : end])
        pt, used = _segment(page, page_no, above, columns, _line_y(lines[ai]), lines[ai + 1 : end], False, more_below=k + 1 < len(anchors), ocr=ocr)
        if pt is None:
            start = ai + 1
            continue
        # a header at the foot of a page whose rows follow overleaf is kept so the next page can inherit it
        out.append(pt)
        prev = pt
        start = ai + 1 + used
    return out


def extract_pdf_pages(path: str, use_ocr: bool = True) -> tuple[list[PageTable], dict]:
    """Table segments of a PDF in order, plus page statistics.

    Pages without a text layer are read with OCR when ``use_ocr`` is set.
    """
    doc = fitz.open(path)
    out: list[PageTable] = []
    stats = {"pages": len(doc), "pages_without_text": 0, "pages_ocr": 0, "ocr_conf": []}
    prev: PageTable | None = None
    for i, page in enumerate(doc):
        words = page_words(page)
        ocr = False
        if len(words) < 5:
            stats["pages_without_text"] += 1
            if not use_ocr:
                continue
            from .ocr import ocr_page_words

            words, conf = ocr_page_words(page)
            if len(words) < 5:
                continue
            stats["pages_ocr"] += 1
            stats["ocr_conf"].append(conf)
            ocr = True
        segs = extract_page(page, i + 1, words, prev, ocr=ocr)
        if segs:
            prev = segs[-1]
        out.extend(segs)
    doc.close()
    stats["ocr_conf"] = round(sum(stats["ocr_conf"]) / len(stats["ocr_conf"]), 3) if stats["ocr_conf"] else ""
    return out, stats
