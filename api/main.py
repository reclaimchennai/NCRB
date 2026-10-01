"""NCRB data explorer API (FastAPI, read-only DuckDB).

Serves the dashboard in ``web/``: search the 36,000 tables, fetch one table as
printed, follow a table across years, and the per-year quality summary. All
data comes from ``data/web/ncrb.duckdb`` (built by ``python -m ncrb.webdata``).

    uvicorn api.main:app --port 5072
"""

from __future__ import annotations

import csv
import io
import json
import os
import re
import threading
from pathlib import Path

import duckdb
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse, StreamingResponse

ROOT = Path(__file__).resolve().parents[1]
DB = Path(os.environ.get("NCRB_DB", ROOT / "data" / "web" / "ncrb.duckdb"))
PUBS = {"cii": "Crime in India", "adsi": "Accidental Deaths & Suicides in India", "psi": "Prison Statistics India"}

app = FastAPI(title="NCRB data explorer", docs_url="/api/docs", openapi_url="/api/openapi.json")
app.add_middleware(GZipMiddleware, minimum_size=1024)

_local = threading.local()


def db() -> duckdb.DuckDBPyConnection:
    """One read-only connection per worker thread (DuckDB connections are not thread safe)."""
    con = getattr(_local, "con", None)
    if con is None:
        con = duckdb.connect(str(DB), read_only=True)
        _local.con = con
    return con


def rows(sql: str, params: list | tuple = ()) -> list[dict]:
    cur = db().execute(sql, params)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def cached(resp: dict | list, seconds: int = 3600) -> JSONResponse:
    return JSONResponse(resp, headers={"Cache-Control": f"public, max-age={seconds}"})


TABLE_COLS = (
    "table_id, publication, year, listing, topic, serial, table_no, title, method, "
    "n_rows, n_cols, n_cells, checks_total, checks_passed, source_url, pages"
)


@app.get("/healthz")
def healthz():
    n = db().execute("SELECT count(*) FROM tables").fetchone()[0]
    return {"ok": n > 0, "tables": n}


@app.get("/api/meta")
def meta():
    pubs = rows("""
        SELECT publication, min(year) AS first_year, max(year) AS last_year, count(*) AS tables,
               sum(n_cells) AS cells,
               sum(CASE WHEN method IN ('pdf_ocr','pdf_mixed','pdf_vlm') THEN 0 ELSE checks_total END) AS checks_text,
               sum(CASE WHEN method IN ('pdf_ocr','pdf_mixed','pdf_vlm') THEN 0 ELSE checks_passed END) AS passed_text,
               sum(CASE WHEN method IN ('pdf_ocr','pdf_mixed','pdf_vlm') THEN checks_total ELSE 0 END) AS checks_ocr,
               sum(CASE WHEN method IN ('pdf_ocr','pdf_mixed','pdf_vlm') THEN checks_passed ELSE 0 END) AS passed_ocr
        FROM tables GROUP BY publication ORDER BY publication
    """)
    for p in pubs:
        p["name"] = PUBS.get(p["publication"], p["publication"])
    years = rows("SELECT publication, year, count(*) AS tables FROM tables GROUP BY 1, 2 ORDER BY 1, 2")
    topics = rows("SELECT publication, topic, first_year, last_year, n_tables FROM topics ORDER BY publication, n_tables DESC")
    return cached({"publications": pubs, "years": years, "topics": topics,
                   "series": db().execute("SELECT count(*) FROM series").fetchone()[0]})


@app.get("/api/quality")
def quality():
    return cached(rows("SELECT * FROM quality ORDER BY publication, year"))


def _search_clause(q: str, field: str = "title") -> tuple[str, list]:
    words = [w for w in re.split(r"\s+", q.strip()) if w][:8]
    return " AND ".join(f"{field} ILIKE ?" for _ in words), [f"%{w}%" for w in words]


@app.get("/api/tables")
def tables(
    pub: str | None = None,
    year: int | None = None,
    topic: str | None = None,
    q: str | None = None,
    listing: str = Query("individual", pattern="^(individual|all|volume)$"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    where, params = ["n_cells > 0"], []
    if pub:
        where.append("publication = ?"); params.append(pub)
    if year:
        where.append("year = ?"); params.append(year)
    if topic:
        where.append("topic = ?"); params.append(topic)
    if listing == "individual":
        where.append("listing IN ('table_content', 'additional_table', 'table_chapter')")
    elif listing == "volume":
        where.append("listing = 'year_wise'")
    if q:
        clause, p = _search_clause(q, "(title || ' ' || coalesce(topic, '') || ' ' || coalesce(table_no, ''))")
        if clause:
            where.append(clause); params += p
    w = " AND ".join(where)
    total = db().execute(f"SELECT count(*) FROM tables WHERE {w}", params).fetchone()[0]
    items = rows(
        f"SELECT {TABLE_COLS} FROM tables WHERE {w} "
        "ORDER BY year DESC, publication, try_cast(split_part(serial, '.', 1) AS INTEGER) NULLS LAST, serial, table_id "
        "LIMIT ? OFFSET ?",
        params + [limit, offset],
    )
    return cached({"total": total, "items": items}, 600)


def _table(table_id: str) -> tuple[dict, list[dict], list[dict]]:
    t = rows(f"SELECT {TABLE_COLS}, section, pdf_title, inferred_pages, warnings, source_file FROM tables WHERE table_id = ?", [table_id])
    if not t:
        raise HTTPException(404, "no such table")
    m = db().execute("SELECT meta FROM table_meta WHERE table_id = ?", [table_id]).fetchone()
    info = {**t[0], **(json.loads(m[0]) if m else {})}
    cells = rows(
        'SELECT "row", section, sl_no, name, name_std, entity_type, is_total, col_no, "column", value, raw, ocr_conf '
        "FROM cells WHERE table_id = ? ORDER BY \"row\"",
        [table_id],
    )
    series = rows(
        "SELECT s.series_id, s.title, s.first_year, s.last_year, s.n_years FROM series_members m "
        "JOIN series s USING (series_id) WHERE m.table_id = ?",
        [table_id],
    )
    return info, cells, series


@app.get("/api/table/{table_id:path}.csv")
def table_csv(table_id: str):
    info, cells, _ = _table(table_id)
    cols = [c["name"] for c in info.get("columns") or []] or sorted({c["column"] for c in cells})
    by_row: dict[int, dict] = {}
    for c in cells:
        r = by_row.setdefault(c["row"], {"section": c["section"], "sl_no": c["sl_no"], "name": c["name"]})
        r[c["column"]] = c["raw"]
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["section", "sl_no", "name", *cols])
    for _, r in sorted(by_row.items()):
        w.writerow([r["section"], r["sl_no"], r["name"], *[r.get(c, "") for c in cols]])
    name = table_id.replace("/", "_") + ".csv"
    return PlainTextResponse(buf.getvalue(), media_type="text/csv", headers={"Content-Disposition": f'attachment; filename="{name}"'})


@app.get("/api/table/{table_id:path}")
def table(table_id: str):
    info, cells, series = _table(table_id)
    columns = info.pop("columns", None) or [{"col_no": c, "name": c, "header": [c]} for c in dict.fromkeys(x["column"] for x in cells)]
    index = {c["name"]: i for i, c in enumerate(columns)}
    out_rows: dict[int, dict] = {}
    for c in cells:
        r = out_rows.setdefault(c["row"], {
            "row": c["row"], "section": c["section"], "sl_no": c["sl_no"], "name": c["name"],
            "name_std": c["name_std"], "entity_type": c["entity_type"], "is_total": c["is_total"],
            "v": [None] * len(columns), "raw": [None] * len(columns), "conf": None,
        })
        i = index.get(c["column"])
        if i is None:
            continue
        r["v"][i] = c["value"]
        r["raw"][i] = c["raw"]
        if c["ocr_conf"] is not None:
            r["conf"] = min(r["conf"] or 1, c["ocr_conf"])
    return cached({"table": info, "columns": columns, "rows": [out_rows[k] for k in sorted(out_rows)], "series": series})


@app.get("/api/series")
def series_list(pub: str | None = None, q: str | None = None, min_years: int = 3, limit: int = Query(50, le=200)):
    where, params = ["n_years >= ?"], [min_years]
    if pub:
        where.append("publication = ?"); params.append(pub)
    if q:
        clause, p = _search_clause(q)
        if clause:
            where.append(clause); params += p
    return cached(rows(
        f"SELECT series_id, publication, topic, geography, title, first_year, last_year, n_years, methods "
        f"FROM series WHERE {' AND '.join(where)} ORDER BY n_years DESC, last_year DESC LIMIT ?",
        params + [limit],
    ), 600)


@app.get("/api/series/{series_id:path}/data")
def series_data(series_id: str, column: str, names: str | None = None):
    """Values of one column across the series' years, for every row label (or the listed ones)."""
    params: list = [series_id, column]
    name_filter = ""
    if names:
        wanted = [n for n in names.split("|") if n][:20]
        name_filter = f"AND c.name_std IN ({', '.join('?' for _ in wanted)})"
        params += wanted
    data = rows(
        f"""SELECT c.year, c.name_std, any_value(c.entity_type) AS entity_type, max(c.is_total) AS is_total,
                   any_value(c.value) AS value, any_value(c.raw) AS raw, min(c.ocr_conf) AS ocr_conf, any_value(c.table_id) AS table_id
            FROM series_members m JOIN cells c ON c.table_id = m.table_id
            WHERE m.series_id = ? AND c."column" = ? {name_filter}
            GROUP BY c.year, c.name_std ORDER BY c.year""",
        params,
    )
    return cached(data)


@app.get("/api/series/{series_id:path}")
def series(series_id: str):
    s = rows("SELECT * FROM series WHERE series_id = ?", [series_id])
    if not s:
        raise HTTPException(404, "no such series")
    members = rows(
        "SELECT m.table_id, m.year, t.method, t.checks_total, t.checks_passed, t.source_url FROM series_members m "
        "JOIN tables t USING (table_id) WHERE series_id = ? ORDER BY m.year",
        [series_id],
    )
    columns = rows(
        """SELECT c."column", count(DISTINCT c.year) AS years, min(c.year) AS first_year, max(c.year) AS last_year
           FROM series_members m JOIN cells c ON c.table_id = m.table_id
           WHERE m.series_id = ? GROUP BY 1 ORDER BY years DESC, 1""",
        [series_id],
    )
    names = rows(
        """SELECT c.name_std, any_value(c.entity_type) AS entity_type, max(c.is_total) AS is_total, count(DISTINCT c.year) AS years
           FROM series_members m JOIN cells c ON c.table_id = m.table_id
           WHERE m.series_id = ? GROUP BY 1 ORDER BY years DESC, 1""",
        [series_id],
    )
    return cached({"series": s[0], "members": members, "columns": columns, "names": names})


@app.get("/api/headline")
def headline():
    """Long all-India series for the landing page: the most recent table of each, its year rows."""
    picks = [
        ("cii", r"incidence.*rate.*cognizable crimes.*ipc", "Cognizable crimes under IPC"),
        ("adsi", r"incidence and rate of suicides", "Suicides"),
        ("adsi", r"incidence.*rate of accidental deaths", "Accidental deaths"),
        ("psi", r"inmate population|number of inmates|prison population", "Prison inmates"),
    ]
    out = []
    for pub, rx, label in picks:
        t = rows(
            "SELECT table_id, year, title FROM tables WHERE publication = ? AND regexp_matches(lower(title), ?) "
            "AND method IN ('pdf_text', 'excel') AND n_rows BETWEEN 5 AND 40 "
            "ORDER BY year DESC, n_rows DESC LIMIT 1",
            [pub, rx],
        )
        if t:
            out.append({"label": label, "publication": pub, **t[0]})
    return cached(out)


@app.exception_handler(duckdb.Error)
def duck_error(_, exc):
    return JSONResponse({"detail": "query failed"}, status_code=500)
