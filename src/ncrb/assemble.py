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
    conf: dict[int, float] = field(default_factory=dict)


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
    ocr_pages: int = 0
    sheet: str = ""
    warnings: list[str] = field(default_factory=list)
    _index: dict = field(default_factory=dict, repr=False)
    _labels: dict = field(default_factory=dict, repr=False)
    _serials: dict = field(default_factory=dict, repr=False)
    _sigs: dict = field(default_factory=dict, repr=False)
    _last_rows: list = field(default_factory=list, repr=False)
    _remap_sig: tuple = field(default=(), repr=False)
    _remap: dict = field(default_factory=dict, repr=False)
    _next_id: int = field(default=10000, repr=False)


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
            if t.columns and any(sig):
                ids = {}
                for c in data_cols:
                    t._next_id += 1  # same counter as the remapped printed numbers, so the two never collide
                    ids[c.id] = t._next_id
            t._sigs[sig] = [ids[c.id] for c in data_cols]
        t.inferred_pages += 1
    # --- which existing row, if any, does each row of this page continue?
    matches: list[tuple[tuple, tuple, TableRow | None]] = []
    seen: dict[tuple, int] = {}
    seen_label: dict[str, int] = {}
    for r in pt.rows:
        base_key = (r.serial, norm_label(r.label))
        occ = seen.get(base_key, 0)
        seen[base_key] = occ + 1
        label_key = (base_key[1], seen_label.get(base_key[1], 0))
        seen_label[base_key[1]] = label_key[1] + 1
        existing = t._index.get((*base_key, occ))
        if existing is None:
            # the serial number is missing on some pages: fall back to the label when it is unambiguous
            same = t._labels.get(label_key, [])
            if len(same) == 1 and (not r.serial or not same[0].serial):
                existing = same[0]
        if existing is None and r.serial and len(base_key[1]) >= 4:
            # a long label wraps differently from page to page ('Indore (Madhya' / 'Indore (Madhya Pradesh)')
            near = [
                x for x in t._serials.get(r.serial, [])
                if norm_label(x.label).startswith(base_key[1]) or base_key[1].startswith(norm_label(x.label)) and len(norm_label(x.label)) >= 4
            ]
            if len(near) == 1:
                existing = near[0]
        matches.append(((*base_key, occ), label_key, existing))

    if not pt.anchor_inferred and not pt.unlabelled:
        # A printed column number reused for a different column (NCRB repeats e.g. '(3) No. of cases'
        # in each block of a wide table) must not overwrite the earlier one.
        sig = tuple(c.id for c in data_cols)
        if sig == t._remap_sig:
            ids.update(t._remap)
        else:
            t._remap_sig, t._remap = sig, {}
            pairs = [(r, m[2]) for r, m in zip(pt.rows, matches) if m[2] is not None]
            if pt.rows and len(pairs) >= 0.5 * len(pt.rows):  # same rows again: this page adds columns
                for c in data_cols:
                    if c.id in t.columns and any(old.cells.get(c.id) not in (None, r.cells.get(c.id)) for r, old in pairs):
                        t._next_id += 1
                        t._remap[c.id] = t._next_id
                ids.update(t._remap)
    for c in data_cols:
        t.columns.setdefault(ids[c.id], list(c.header))
    if not t.label_header:
        labels = [c for c in pt.columns if c.id in pt.label_cols]
        t.label_header = " / ".join(" ".join(c.header) for c in labels if c.header)
    t.pages.append(pt.page)
    t.ocr_pages += int(pt.ocr)
    if pt.unlabelled:
        # the right-hand page of a spread carries no row labels; its rows follow the left page in order
        left = t._last_rows
        if len(left) == len(pt.rows):
            for a, b in zip(left, pt.rows):
                a.cells.update({ids[cid]: v for cid, v in b.cells.items() if cid in ids})
                a.conf.update({ids[cid]: v for cid, v in b.conf.items() if cid in ids})
        else:
            t.warnings.append(f"page {pt.page}: {len(pt.rows)} unlabelled rows could not be matched to {len(left)} rows of the facing page")
            for b in pt.rows:
                t.rows.append(TableRow(b.section, "", f"[unmatched row, page {pt.page}]", {ids[cid]: v for cid, v in b.cells.items() if cid in ids}, b.page))
        return
    first_new = len(t.rows)
    for r, (key, label_key, existing) in zip(pt.rows, matches):
        cells = {ids[cid]: v for cid, v in r.cells.items() if cid in ids}
        conf = {ids[cid]: v for cid, v in r.conf.items() if cid in ids}
        if existing is not None and not any(existing.cells.get(k, v) != v for k, v in cells.items()):
            existing.cells.update(cells)
            existing.conf.update(conf)
            if len(r.label) > len(existing.label) and norm_label(r.label).startswith(norm_label(existing.label)):
                existing.label = r.label  # keep the fullest form of a wrapped label
            if r.serial and not existing.serial:
                existing.serial = r.serial
        else:
            row = TableRow(r.section, r.serial, r.label, cells, r.page, conf)
            t.rows.append(row)
            # later pages with the same label and new columns merge into the newest such row
            t._index[key] = row
            t._labels.setdefault(label_key, []).append(row)
            if r.serial:
                t._serials.setdefault(r.serial, []).append(row)
    t._last_rows = t.rows[first_new:] or t._last_rows
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
        if cur is not None and not pt.carried and not pt.unlabelled:
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
        t._labels.clear()
        t._serials.clear()
        t._sigs.clear()
        t._last_rows = []
    return tables


# --------------------------------------------------------------------------- validation

RATE_RE = re.compile(r"rate|percent|%|share|ratio|per\s+lakh|variation|rank|density|average|mid[- ]?year|population", re.I)
GRAND_RE = re.compile(r"all[\s-]*india|grand|\(\s*all\s*\)|states?\s*(\+|&|and)\s*uts?", re.I)


RATE_TABLE_RE = re.compile(
    r"^\W*(percentage|rate|ratio)\b|\b(conviction|charge-?sheeting|pendency|occupancy|recidivism)\s+(rate|percentage)|\bper\s+(staff|case|inmate|lakh)\b",
    re.I,
)
GEO_TOTAL_RE = re.compile(r"total.*(state|u\.?\s*t|union|cit(y|ies)|district|all[\s-]*india)|all[\s-]*india|^\s*india\s*$", re.I)
SUBITEM_RE = re.compile(r"^\(?([ivxlc]{1,5}|[a-z])\)$|^\([ivxlc]{1,5}$|^\([a-z]$", re.I)


def check_totals(t: Table) -> dict:
    """Compare every 'TOTAL' row with the sum of the rows it should cover.

    Only count-like columns are tested (rates and percentages do not add up).
    Lists with sub-items ('2. Service: (i) Government (ii) Private') are summed
    both with and without the sub-items and either reading may match. Returns
    the number of cells checked and passed; a table with a high pass rate was
    read correctly with near certainty, because a single misplaced digit breaks
    the sum.
    """
    checked = passed = other_checked = other_passed = 0
    failures: list[str] = []
    if RATE_TABLE_RE.search(t.title):  # a table of rates or percentages has no additive totals
        return {"cells_checked": 0, "cells_passed": 0, "failures": [], "other_totals_checked": 0, "other_totals_passed": 0}
    # rates, shares and averages do not add up; they are recognised by their heading or by carrying decimals
    decimal = {cid for r in t.rows for cid, raw in r.cells.items() if "." in raw and any(ch.isdigit() for ch in raw)}
    cols = [cid for cid, hdr in t.columns.items() if cid not in decimal and not RATE_RE.search(" ".join(hdr))]
    sub = []
    in_group = False  # after a heading row such as '13 Poisoning:' until the next numbered row
    for r in t.rows:
        numbered = bool(re.fullmatch(r"\d{1,3}", r.serial))
        is_sub = (
            bool(SUBITEM_RE.match(r.serial))
            or bool(re.match(r"^\(([ivxlc]{1,5}|[a-z])\)|^\d{1,2}\.\d{1,2}\b", r.label, re.I))
            or bool(re.fullmatch(r"\d{1,2}\.\d{1,2}", r.serial))
        )
        if numbered or TOTAL_RE.search(r.label):
            in_group = False
        sub.append(is_sub or in_group)
        if r.label.rstrip().endswith(":"):
            in_group = True
    for cid in cols:
        acc = top = 0.0
        acc_n = 0
        subtotals: list[float] = []
        ok_run = True  # False when a row in the run had no readable number
        for r, is_sub in zip(t.rows, sub):
            raw = r.cells.get(cid)
            v = parse_number(raw) if raw is not None else None
            if TOTAL_RE.search(r.label):
                if v is None:
                    continue
                if GRAND_RE.search(r.label) and subtotals:
                    expect, n = [sum(subtotals)], len(subtotals)
                    subtotals = []
                else:
                    expect, n = [acc, top], acc_n
                    subtotals.append(v)
                    acc, top, acc_n = 0.0, 0.0, 0
                if n >= 2 and ok_run:
                    ok = any(abs(e - v) <= 0.51 for e in expect)
                    if GEO_TOTAL_RE.search(r.label):
                        checked += 1
                        passed += ok
                        if not ok and len(failures) < 8:
                            failures.append(f"col {cid} '{r.label}': printed {v:g}, sum {expect[0]:g}")
                    else:
                        # totals inside lists of crime heads, causes etc. nest in ways only the
                        # source defines; they are counted apart and not used to judge the extraction
                        other_checked += 1
                        other_passed += ok
                ok_run = True
            else:
                if v is None:
                    if raw is not None and raw.strip() not in ("-", "–", "—", "NA", "NR", "Nil", "NIL", "..", "..."):
                        ok_run = False
                else:
                    acc += v
                    acc_n += 1
                    if not is_sub:
                        top += v
    return {
        "cells_checked": checked,
        "cells_passed": passed,
        "failures": failures,
        "other_totals_checked": other_checked,
        "other_totals_passed": other_passed,
    }
