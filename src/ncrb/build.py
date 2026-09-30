"""Build the combined datasets from the per-table extractions.

Outputs:
    data/combined/<pub>_cells.parquet   every extracted cell of a publication, tidy
    data/series/<pub>/<series>.csv      the same table stacked across years
    data/series_index.csv               one line per series: years covered, source tables

A "series" is the set of tables, one per year, whose titles are the same once
the year is removed (NCRB renumbers tables between editions, so table numbers
cannot be used). Row labels get a standard State/UT name so years line up.

Usage:
    uv run python -m ncrb.build
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from .crawl import ROOT
from .entities import standardise
from .extract import INDEX, slug

COMBINED = ROOT / "data" / "combined"
SERIES = ROOT / "data" / "series"
SERIES_INDEX = ROOT / "data" / "series_index.csv"

YEAR = r"(?:19|20)\d\d"
YEAR_RE = re.compile(
    rf"(?:\b(?:during|in|for|of|upto|up to|as on|at the end of|since|from|over)\s+)?(?:the\s+)?(?:year\s+)?"
    rf"(?:\d{{1,2}}(?:st|nd|rd|th)?[\s.-]+(?:january|december|dec|jan|march|april)[\s.,-]+)?"
    rf"{YEAR}(?:\s*(?:-|–|to|&|and|over|/|,)\s*(?:{YEAR}|\d\d)\b)*",
    re.I,
)
GEO = [
    (re.compile(r"state\s*/?\s*(&|and)?\s*u\.?t\.?s?\s*(&|and|/|,)\s*cit(y|ies)", re.I), "state-ut-city"),
    (re.compile(r"metropolitan|mega\s*cit|cit(y|ies)\s*-?\s*wise|\bcities\b", re.I), "city"),
    (re.compile(r"state\s*/?\s*(&|and)?\s*u\.?t\.?s?|state\s*-?\s*wise|states\b", re.I), "state-ut"),
    (re.compile(r"all[\s-]*india", re.I), "all-india"),
]

SCHEMA = pa.schema(
    [
        ("publication", pa.string()), ("year", pa.int16()), ("table_id", pa.string()), ("method", pa.string()),
        ("row", pa.int32()), ("section", pa.string()), ("sl_no", pa.string()), ("name", pa.string()),
        ("name_std", pa.string()), ("entity_type", pa.string()), ("is_total", pa.int8()),
        ("col_no", pa.int32()), ("column", pa.string()),
        ("h1", pa.string()), ("h2", pa.string()), ("h3", pa.string()), ("h4", pa.string()), ("h5", pa.string()),
        ("value", pa.float64()), ("raw", pa.string()), ("page", pa.int32()), ("ocr_conf", pa.float32()),
    ]
)


def series_key(title: str) -> tuple[str, str]:
    """(normalised title without years, geography tag)."""
    t = re.sub(r"\((?:contd|concld|concluded|continued)[^)]*\)", " ", title, flags=re.I)
    geo = next((tag for rx, tag in GEO if rx.search(t)), "")
    t = YEAR_RE.sub(" ", t)
    t = re.sub(r"\(\s*\)", " ", t)
    return slug(t, 110), geo


def load_long(path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    for c in ("row", "col_no", "page", "is_total"):
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype("int32")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["ocr_conf"] = pd.to_numeric(df["ocr_conf"], errors="coerce").astype("float32")
    std = {n: standardise(n) for n in df["name"].unique()}
    df["name_std"] = df["name"].map(lambda n: std[n][0])
    df["entity_type"] = df["name"].map(lambda n: std[n][1])
    return df


def main() -> None:
    tables = list(csv.DictReader(INDEX.open(encoding="utf-8")))
    COMBINED.mkdir(parents=True, exist_ok=True)
    writers: dict[str, pq.ParquetWriter] = {}
    groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    n_cells = 0
    for i, t in enumerate(tables, 1):
        long_path = ROOT / t["csv"].replace(".csv", ".long.csv")
        if not long_path.exists():
            continue
        df = load_long(long_path)
        if df.empty:
            continue
        df.insert(0, "method", t["method"])
        df.insert(0, "table_id", t["table_id"])
        df.insert(0, "year", int(t["year"]))
        df.insert(0, "publication", t["publication"])
        pub = t["publication"]
        if pub not in writers:
            writers[pub] = pq.ParquetWriter(COMBINED / f"{pub}_cells.parquet", SCHEMA, compression="zstd")
        writers[pub].write_table(pa.Table.from_pandas(df[[f.name for f in SCHEMA]], schema=SCHEMA, preserve_index=False))
        n_cells += len(df)
        key, geo = series_key(t["title"] or t["pdf_title"])
        if key:
            groups[(pub, key, geo)].append(t)
        if i % 1000 == 0:
            print(f"[{i}/{len(tables)}] {n_cells:,} cells", flush=True)
    for w in writers.values():
        w.close()
    print(f"combined: {n_cells:,} cells from {len(tables)} tables")

    # --- series
    if SERIES.exists():
        for f in SERIES.rglob("*.csv"):
            f.unlink()
    index_rows = []
    for (pub, key, geo), members in sorted(groups.items()):
        years = sorted({int(m["year"]) for m in members})
        if len(years) < 2:
            continue
        sid = f"{key}__{geo}" if geo else key
        frames = []
        for m in sorted(members, key=lambda m: (int(m["year"]), m["table_id"])):
            df = load_long(ROOT / m["csv"].replace(".csv", ".long.csv"))
            df.insert(0, "table_id", m["table_id"])
            df.insert(0, "year", int(m["year"]))
            frames.append(df)
        out = SERIES / pub / f"{sid}.csv"
        out.parent.mkdir(parents=True, exist_ok=True)
        cols = ["year", "table_id", "section", "sl_no", "name", "name_std", "entity_type", "is_total", "col_no", "column", "h1", "h2", "h3", "h4", "h5", "value", "raw", "ocr_conf"]
        pd.concat(frames)[cols].to_csv(out, index=False)
        methods = sorted({m["method"] for m in members})
        index_rows.append({
            "series_id": f"{pub}/{sid}",
            "publication": pub,
            "geography": geo,
            "title": max((m["title"] for m in members), key=len),
            "first_year": years[0],
            "last_year": years[-1],
            "n_years": len(years),
            "years": " ".join(map(str, years)),
            "n_tables": len(members),
            "methods": " ".join(methods),
            "csv": str(out.relative_to(ROOT)),
        })
    with SERIES_INDEX.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(index_rows[0]) if index_rows else ["series_id"])
        w.writeheader()
        w.writerows(index_rows)
    print(f"series: {len(index_rows)} written")


if __name__ == "__main__":
    main()
