"""How much of a reading can be trusted, without an answer key.

Statistical tables carry their own checks: a 'Total' row is the sum of the rows above it, a 'Total' column
the sum of its group. A misread digit breaks a sum, so the share of sums a reading reproduces measures it.
Where a table has no totals, independent readings (two models, two page sizes) still check each other: two
models rarely misread the same digit the same way, so the reading the others agree with is the likeliest.

A project with stronger checks (NCRB's State/UT/all-India totals) passes its own scorer to the job
('module:function', called with {page: text} and the manifest entry, returning (matched, checked)).
"""

from __future__ import annotations

import re
from collections import Counter

from .tables import number, tables

TOTAL = re.compile(r"^\s*(grand\s+)?(sub[\s-]*)?total\b|\btotal\s*$|\(\s*total\s*\)|^\s*all\s+india\b", re.I)
RATE = re.compile(r"rate|percent|%|share|ratio|average|per\s+(lakh|cent|1000)|variation|rank|population", re.I)


def _header_rows(g) -> int:
    """Rows at the top with no figures in them."""
    n = 0
    for row in g:
        if sum(number(c) is not None for c in row[1:]) >= max(1, (len(row) - 1) // 2):
            break
        n += 1
    return n


def check_grid(g) -> tuple[int, int]:
    """(sums matched, sums checked) in one table: total rows against the rows above, total columns against
    their group. Rates and percentages are left out (they do not add up)."""
    if len(g) < 3 or len(g[0]) < 3:
        return 0, 0
    h = _header_rows(g)
    head = [" ".join(dict.fromkeys(g[r][c] for r in range(h) if g[r][c])) for c in range(len(g[0]))]
    cols = [c for c in range(1, len(g[0])) if not RATE.search(head[c]) and not any("." in (g[r][c] or "") for r in range(h, len(g)))]
    matched = checked = 0
    # total rows: the figures since the previous total row add up to it
    for c in cols:
        acc, n = 0.0, 0
        for r in range(h, len(g)):
            label = " ".join(g[r][:2])
            v = number(g[r][c])
            if TOTAL.search(label):
                if v is not None and n >= 2:
                    checked += 1
                    matched += abs(acc - v) <= 0.51
                acc, n = 0.0, 0
            elif v is not None:
                acc += v
                n += 1
    # total columns: the count columns since the previous total column (or under the same parent heading)
    groups, run = [], []
    for c in cols:
        leaf = g[h - 1][c] if h else head[c]
        if TOTAL.search(leaf or ""):
            if len(run) >= 2:
                groups.append((c, list(run)))
            run = []
        else:
            run.append(c)
    for r in range(h, len(g)):
        for tot, members in groups:
            tv = number(g[r][tot])
            vals = [number(g[r][m]) for m in members]
            if tv is None or any(v is None for v in vals) or (tv == 0 and not any(vals)):
                continue
            checked += 1
            matched += abs(sum(vals) - tv) <= 0.51
    return matched, checked


def consistency(texts: dict[int, str]) -> tuple[int, int]:
    """(matched, checked) over every table of a file's pages."""
    m = c = 0
    for t in texts.values():
        for g in tables(t):
            a, b = check_grid(g)
            m, c = m + a, c + b
    return m, c


def figures(texts: dict[int, str]) -> list[str]:
    return [re.sub(r"[,\s]", "", cell) for t in texts.values() for g in tables(t) for row in g for cell in row if number(cell) is not None]


def agreement(a: list[str], b: list[str]) -> float:
    """Share of figures two readings share (as multisets): 1 when they read the same numbers."""
    if not a or not b:
        return 0.0
    return sum((Counter(a) & Counter(b)).values()) / max(len(a), len(b))


def score(matched: int, checked: int) -> int:
    """A missed sum costs twice a matched one."""
    return matched - 2 * (checked - matched)
