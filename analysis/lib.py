"""Helpers for following one NCRB table, one place, across every year it was printed.

NCRB renumbers and rewords its tables between editions, so a topic is found by
a title pattern, one table is picked per year, and the rows for a place are
pulled out of it. Column headers are matched by pattern too, because their
wording and order drift (and on scanned years the OCR'd headers are noisy).

Everything reads the dashboard database (``data/web/ncrb.duckdb``), which holds
every extracted cell; build it with ``python -m ncrb.webdata``.
"""

from __future__ import annotations

import re
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "web" / "ncrb.duckdb"
OUT = ROOT / "analysis" / "output"

# Chennai was printed as MADRAS until 1996; Tamil Nadu has OCR variants in the scans
PLACES = {
    "chennai": r"^\s*(?:chennai|madras)\b(?!.*(?:rural|suburban))",
    "tamil_nadu": r"^\s*tamil\s*-?\s*n[a-z]{1,2}du\b",
}
LISTING_RANK = {"table_content": 0, "additional_table": 1, "table_chapter": 2, "year_wise": 3}
METHOD_RANK = {"pdf_text": 0, "excel": 0, "pdf_vlm": 1, "pdf_mixed": 2, "pdf_ocr": 3}
SCANNED = {"pdf_ocr", "pdf_mixed", "pdf_vlm"}

_con = None


def con() -> duckdb.DuckDBPyConnection:
    global _con
    if _con is None:
        _con = duckdb.connect(str(DB), read_only=True)
    return _con


def q(sql: str, params=()) -> pd.DataFrame:
    return con().execute(sql, list(params)).df()


def find_tables(pub: str, title: str, exclude: str | None = None, years: tuple[int, int] = (1900, 2100)) -> pd.DataFrame:
    """Every table of a publication whose title matches ``title`` (regex, case-insensitive)."""
    df = q(
        "SELECT table_id, year, listing, method, title, n_rows, n_cols, checks_total, checks_passed, source_url, pages "
        "FROM tables WHERE publication = ? AND regexp_matches(lower(title), ?) AND year BETWEEN ? AND ? AND n_cells > 0",
        [pub, title.lower(), *years],
    )
    if exclude:
        df = df[~df.title.str.lower().str.contains(exclude, regex=True)]
    return df.sort_values(["year", "listing"]).reset_index(drop=True)


def rows_for(table_ids: list[str], place: str) -> pd.DataFrame:
    """All cells of the rows naming a place (see PLACES) in the given tables."""
    if not table_ids:
        return pd.DataFrame()
    rx = PLACES.get(place, place)
    marks = ",".join("?" for _ in table_ids)
    df = q(
        f'SELECT table_id, year, "row", section, name, name_std, col_no, "column", h1, h2, h3, h4, h5, value, raw '
        f"FROM cells WHERE table_id IN ({marks})",
        table_ids,
    )
    df = df[df.name.str.lower().str.contains(rx, regex=True, na=False)].copy()
    df["_o"] = df.col_no.map(col_order)
    return df.sort_values(["table_id", "row", "_o"]).drop(columns="_o")


def tables_with_column(table_ids: list[str], pattern: str) -> set[str]:
    """Tables having at least one column whose header matches ``pattern``."""
    if not table_ids:
        return set()
    marks = ",".join("?" for _ in table_ids)
    df = q(f'SELECT DISTINCT table_id, "column" FROM cells WHERE table_id IN ({marks})', table_ids)
    return set(df[df["column"].str.lower().str.contains(pattern, regex=True, na=False)].table_id)


def pick_per_year(candidates: pd.DataFrame, place: str | None = None, prefer_cols: int | None = None, require: str | None = None) -> pd.DataFrame:
    """One table per year: the individually published, text-read one wins; it must name the place.

    Tables cut from whole volumes are used only for years with nothing better.
    """
    if candidates.empty:
        return candidates
    c = candidates.copy()
    if require:
        c = c[c.table_id.isin(tables_with_column(c.table_id.tolist(), require))]
    if place:
        has = set(rows_for(c.table_id.tolist(), place).table_id)
        c = c[c.table_id.isin(has)]
    c["_l"] = c.listing.map(LISTING_RANK).fillna(9)
    c["_m"] = c.method.map(METHOD_RANK).fillna(9)
    c["_c"] = 0 if prefer_cols is None else (c.n_cols - prefer_cols).abs()
    return c.sort_values(["year", "_m", "_l", "_c", "n_rows"], ascending=[True, True, True, True, False]).groupby("year").head(1).drop(columns=["_l", "_m", "_c"])


def col_order(c: str) -> float:
    """Sort key for printed column numbers, which are text ('12', '9a', '10003')."""
    m = re.match(r"(\d+)([a-z]?)", str(c))
    return int(m.group(1)) + (ord(m.group(2)) - 96) / 100 if m and m.group(2) else (int(m.group(1)) if m else 1e9)


def first_number(s: str) -> float | None:
    m = re.search(r"\d+(\.\d+)?", s or "")
    return float(m.group()) if m else None


def save(df: pd.DataFrame, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.csv"
    df.to_csv(path, index=False)
    return path


def provenance(picked: pd.DataFrame) -> pd.DataFrame:
    """The table used for each year, for the record kept beside every output."""
    return picked[["year", "table_id", "method", "title", "source_url", "pages", "checks_passed", "checks_total"]]
