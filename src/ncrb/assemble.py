"""Stitch per-page extractions into whole tables and validate them."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .pdftable import TOTAL_RE, PageTable, parse_number


@dataclass
class TableRow:
    section: str
    serial: str
    label: str
    cells: dict[int, str]
    page: int


@dataclass
class Table:
    table_no: str
    title: str
    columns: dict[int, list[str]] = field(default_factory=dict)  # data column id -> header path
    label_header: str = ""
    rows: list[TableRow] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    pages: list[int] = field(default_factory=list)
    inferred_pages: int = 0
    warnings: list[str] = field(default_factory=list)
    _index: dict = field(default_factory=dict, repr=False)
    _sigs: dict = field(default_factory=dict, repr=False)


def norm_label(s: str) -> str:
    return re.sub(r"[^A-Z0-9]+", " ", s.upper()).strip()


def _add_page(t: Table, pt: PageTable) -> None:
    data_cols = [c for c in pt.columns if c.id not in pt.label_cols]
    ids = {c.id: c.id for c in data_cols}
    if pt.anchor_inferred:
        # synthetic ids restart on every page; a page with new headings is a column continuation
        sig = tuple(" | ".join(c.header) for c in data_cols)
        if sig in t._sigs:
            ids = dict(zip((c.id for c in data_cols), t._sigs[sig]))
        else:
            base = max(t.columns, default=1)
            if t.columns and any(sig):
                ids = {c.id: base + k + 1 for k, c in enumerate(data_cols)}
            t._sigs[sig] = [ids[c.id] for c in data_cols]
        t.inferred_pages += 1
    for c in data_cols:
        t.columns.setdefault(ids[c.id], list(c.header))
    if not t.label_header:
        labels = [c for c in pt.columns if c.id in pt.label_cols]
        t.label_header = " / ".join(" ".join(c.header) for c in labels if c.header)
    t.pages.append(pt.page)
    seen: dict[tuple, int] = {}
    for r in pt.rows:
        base_key = (r.serial, norm_label(r.label))
        occ = seen.get(base_key, 0)
        seen[base_key] = occ + 1
        key = (*base_key, occ)
        cells = {ids[cid]: v for cid, v in r.cells.items() if cid in ids}
        existing = t._index.get(key)
        if existing is not None and not (set(cells) & set(existing.cells)):
            existing.cells.update(cells)
        else:
            row = TableRow(r.section, r.serial, r.label, cells, r.page)
            t.rows.append(row)
            # later pages with the same label and new columns merge into the newest such row
            t._index[key] = row
    for n in pt.notes:
        n = n.replace("", "•").strip()
        if n and n not in t.notes:
            t.notes.append(n)


def assemble(pages: list[PageTable | None]) -> list[Table]:
    tables: list[Table] = []
    cur: Table | None = None
    for pt in pages:
        if pt is None:
            continue
        new = cur is None
        if cur is not None and not pt.carried:
            if pt.table_no and cur.table_no and pt.table_no != cur.table_no:
                new = True
            elif pt.table_no and not cur.table_no:
                new = True
            elif not pt.table_no and not pt.contd and pt.title and norm_label(pt.title) != norm_label(cur.title):
                # untitled continuation pages have an empty title; a different title is a different table
                new = bool(cur.title)
        if new:
            cur = Table(pt.table_no, pt.title)
            tables.append(cur)
        elif pt.title and len(pt.title) > len(cur.title) and not cur.title:
            cur.title = pt.title
        _add_page(cur, pt)
    for t in tables:
        t._index.clear()
        t._sigs.clear()
    return tables


# --------------------------------------------------------------------------- validation

RATE_RE = re.compile(r"rate|percent|%|share|ratio|per\s+lakh|variation|rank|density|average|mid[- ]?year|population", re.I)
GRAND_RE = re.compile(r"all[\s-]*india|grand|\(\s*all\s*\)|states?\s*(\+|&|and)\s*uts?", re.I)


def check_totals(t: Table) -> dict:
    """Compare every 'TOTAL' row with the sum of the rows it should cover.

    Only count-like columns are tested (rates and percentages do not add up).
    Returns the number of cells checked and passed; a table with a high pass
    rate was read correctly with near certainty, because a single misplaced
    digit breaks the sum.
    """
    checked = passed = 0
    failures: list[str] = []
    cols = [cid for cid, hdr in t.columns.items() if not RATE_RE.search(" ".join(hdr))]
    for cid in cols:
        acc = 0.0
        acc_n = 0
        subtotals: list[float] = []
        ok_run = True  # False when a row in the run had no readable number
        for r in t.rows:
            raw = r.cells.get(cid)
            v = parse_number(raw) if raw is not None else None
            if TOTAL_RE.search(r.label):
                if v is None:
                    continue
                if GRAND_RE.search(r.label) and subtotals:
                    expect, n = sum(subtotals), len(subtotals)
                    subtotals = []
                else:
                    expect, n = acc, acc_n
                    subtotals.append(v)
                    acc, acc_n = 0.0, 0
                if n >= 2 and ok_run:
                    checked += 1
                    if abs(expect - v) <= 0.51:
                        passed += 1
                    elif len(failures) < 8:
                        failures.append(f"col {cid} '{r.label}': printed {v:g}, sum {expect:g}")
                ok_run = True
            else:
                if v is None:
                    if raw is not None and raw.strip() not in ("-", "–", "—", "NA", "NR", "Nil", "NIL", "..", "..."):
                        ok_run = False
                else:
                    acc += v
                    acc_n += 1
    return {"cells_checked": checked, "cells_passed": passed, "failures": failures}
