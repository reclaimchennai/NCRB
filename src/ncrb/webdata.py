"""Build the dashboard's database, ``data/web/ncrb.duckdb``.

One DuckDB file holds everything the dashboard API reads: every cell (from the
combined Parquet files), the table, series and topic indexes, each table's
JSON metadata, and the per-year quality summary. Cells are stored sorted by
table so a table or a series is a narrow range scan.

Usage:
    uv run python -m ncrb.webdata
"""

from __future__ import annotations

import json

import duckdb

from .crawl import ROOT

WEB = ROOT / "data" / "web"
DB = WEB / "ncrb.duckdb"


def main() -> None:
    WEB.mkdir(parents=True, exist_ok=True)
    tmp = DB.with_suffix(".tmp")
    tmp.unlink(missing_ok=True)
    con = duckdb.connect(str(tmp))
    d = ROOT / "data"
    con.execute(f"""
        CREATE TABLE tables AS
        SELECT * FROM read_csv('{d / "tables_index.csv"}', header=true, all_varchar=true)
    """)
    con.execute("""
        ALTER TABLE tables ALTER year TYPE INTEGER;
        ALTER TABLE tables ALTER n_rows TYPE INTEGER;
        ALTER TABLE tables ALTER n_cols TYPE INTEGER;
        ALTER TABLE tables ALTER n_cells TYPE INTEGER;
        ALTER TABLE tables ALTER checks_total TYPE INTEGER;
        ALTER TABLE tables ALTER checks_passed TYPE INTEGER;
    """)
    con.execute(f"CREATE TABLE series AS SELECT * FROM read_csv('{d / 'series_index.csv'}', header=true)")
    con.execute(f"CREATE TABLE series_members AS SELECT * FROM read_csv('{d / 'series_members.csv'}', header=true)")
    con.execute(f"CREATE TABLE topics AS SELECT * FROM read_csv('{d / 'topics_index.csv'}', header=true)")
    con.execute(f"CREATE TABLE quality AS SELECT * FROM read_csv('{d / 'quality_by_year.csv'}', header=true)")
    con.execute(f"""
        CREATE TABLE cells AS
        SELECT table_id, publication, year, "row", section, sl_no, name, name_std, entity_type, is_total,
               col_no, "column", h1, h2, h3, h4, h5, value, raw, ocr_conf
        FROM read_parquet('{d / "combined"}/*_cells.parquet')
        ORDER BY table_id, "row", col_no
    """)
    metas = []
    for t in con.execute("SELECT table_id, csv FROM tables").fetchall():
        path = ROOT / t[1].replace(".csv", ".json")
        if path.exists():
            m = json.loads(path.read_text(encoding="utf-8"))
            keep = {k: m.get(k) for k in ("row_label", "pages", "columns", "notes", "checks", "listing_title", "source_sha256", "sheet")}
            metas.append((t[0], json.dumps(keep, ensure_ascii=False)))
    con.execute("CREATE TABLE table_meta (table_id VARCHAR, meta VARCHAR)")
    con.executemany("INSERT INTO table_meta VALUES (?, ?)", metas)
    con.execute("CREATE INDEX cells_table ON cells(table_id)")
    n = con.execute("SELECT count(*) FROM cells").fetchone()[0]
    con.close()
    tmp.replace(DB)
    print(f"wrote {DB.relative_to(ROOT)}: {n:,} cells, {DB.stat().st_size / 1e6:.0f} MB")


if __name__ == "__main__":
    main()
