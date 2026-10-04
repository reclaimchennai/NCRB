"""Model output to tables: HTML (<table>, rowspan/colspan), OTSL (<fcel>/<nl> tokens) or Markdown pipes.

Every grid is a list of rows of cell strings, merged cells repeated over their span so header paths can
be read straight down a column.
"""

from __future__ import annotations

import html as htmllib
import re
from html.parser import HTMLParser

Grid = list[list[str]]


class _HTMLTables(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[tuple[str, int, int]]]] = []
        self._rows = self._row = self._cell = None
        self._span = (1, 1)
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self._depth += 1
            if self._depth == 1:
                self._rows = []
        elif self._rows is None:
            return
        elif tag == "tr":
            self._row = []
        elif tag in ("td", "th"):
            self._cell = []
            self._span = (_int(a.get("rowspan")), _int(a.get("colspan")))
        elif tag == "br" and self._cell is not None:
            self._cell.append(" ")

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None and self._row is not None:
            self._row.append((re.sub(r"\s+", " ", "".join(self._cell)).strip(), *self._span))
            self._cell = None
        elif tag == "tr" and self._row is not None and self._rows is not None:
            self._rows.append(self._row)
            self._row = None
        elif tag == "table":
            self._depth -= 1
            if self._depth == 0 and self._rows is not None:
                self.tables.append(self._rows)
                self._rows = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def _int(v) -> int:
    try:
        return max(1, int(v))
    except (TypeError, ValueError):
        return 1


def _expand(rows) -> Grid:
    cells: dict[tuple[int, int], str] = {}
    width = 0
    for r, row in enumerate(rows):
        c = 0
        for text, rs, cs in row:
            while (r, c) in cells:
                c += 1
            for dr in range(rs):
                for dc in range(cs):
                    cells[(r + dr, c + dc)] = text
            c += cs
            width = max(width, c)
    height = 1 + max((r for r, _ in cells), default=-1)
    return [[cells.get((r, c), "") for c in range(width)] for r in range(height)]


OTSL = re.compile(r"<(fcel|ecel|lcel|ucel|xcel|nl|ched|rhed|srow)>")


def _otsl(text: str) -> list[Grid]:
    if not re.search(r"<(fcel|ecel|ched)>", text):
        return []
    text = re.sub(r"</?otsl>|<loc_\d+>", "", text)
    toks = list(OTSL.finditer(text))
    rows: Grid = [[]]
    for k, m in enumerate(toks):
        kind = m.group(1)
        content = text[m.end(): toks[k + 1].start()] if k + 1 < len(toks) else ""
        if kind == "nl":
            rows.append([])
        elif kind in ("fcel", "ched", "rhed", "srow"):
            rows[-1].append(content.strip())
        elif kind == "lcel" and rows[-1]:
            rows[-1].append(rows[-1][-1])
        elif kind == "ucel" and len(rows) > 1 and len(rows[-2]) > len(rows[-1]):
            rows[-1].append(rows[-2][len(rows[-1])])
        else:
            rows[-1].append("")
    rows = [r for r in rows if r]
    w = max((len(r) for r in rows), default=0)
    return [[r + [""] * (w - len(r)) for r in rows]] if rows else []


def _markdown(text: str) -> list[Grid]:
    out, block = [], []
    for line in text.splitlines() + [""]:
        if line.strip().startswith("|"):
            block.append(line)
            continue
        if len(block) >= 2:
            rows = [[c.strip() for c in b.strip().strip("|").split("|")] for b in block]
            rows = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c) for c in r if c)]
            w = max(len(r) for r in rows)
            out.append([r + [""] * (w - len(r)) for r in rows])
        block = []
    return out


def tables(text: str) -> list[Grid]:
    """Every table in one page's model output."""
    text = re.sub(r"```(?:html|markdown)?", "", text or "")
    p = _HTMLTables()
    p.feed(text)
    grids = [_expand(t) for t in p.tables if t]
    return grids or _otsl(text) or _markdown(text)


def text_outside(text: str) -> list[str]:
    """Lines outside the tables (titles, notes)."""
    t = re.sub(r"<table.*?</table>", "\n", text or "", flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return [s for s in (htmllib.unescape(re.sub(r"\s+", " ", ln)).strip() for ln in t.splitlines()) if s and not s.startswith("|")]


NUM = re.compile(r"^[(\[]?-?\d[\d,]*(\.\d+)?[)\]]?$")


def number(cell: str) -> float | None:
    """A cell's figure: '1,23,456' -> 123456.0; '-', 'NA' and words -> None."""
    s = (cell or "").strip().replace(" ", "")
    if not NUM.match(s):
        return None
    try:
        return float(s.strip("()[]").replace(",", ""))
    except ValueError:
        return None
