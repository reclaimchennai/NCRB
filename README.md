# NCRB data: Crime in India, Prison Statistics India, Accidental Deaths & Suicides in India

Every file that the National Crime Records Bureau (NCRB) publishes for its three
annual statistical reports, downloaded, catalogued and converted from PDF / Excel
into CSV, JSON and Parquet.

| Code | Publication | Years on ncrb.gov.in |
|---|---|---|
| `cii` | Crime in India | 1953 – 2024 |
| `adsi` | Accidental Deaths & Suicides in India | 1967 – 2024 |
| `psi` | Prison Statistics India | 1995 – 2024 |

Current counts of files, tables and cells per year, and how well each year
extracted, are in [docs/COVERAGE.md](docs/COVERAGE.md).

## How much to trust the numbers

Read this before using the data. There are two quality tiers, and every table
says which one it belongs to (`method` in `data/tables_index.csv` and in each
table's `.json`).

| `method` | Source | Roughly | Reliability |
|---|---|---|---|
| `pdf_text`, `excel` | PDFs with a text layer, Excel workbooks | 2000 onwards | Digits are copied from the file, not recognised. Errors are structural (a value in the wrong column, a split row) and rare. |
| `pdf_ocr`, `pdf_mixed` | Scanned pages read by OCR | before about 2000 | **Best effort.** Individual digits can be wrong or missing. Use for orientation, check against the PDF before quoting a number. |

Each table carries an automatic check: wherever NCRB prints a `TOTAL (STATES)`,
`TOTAL (UTs)`, `TOTAL (ALL INDIA)` or `TOTAL (CITIES)` row, the extracted rows
above it are summed and compared with the printed total. `checks_total` /
`checks_passed` in the index report the result per table. A table whose checks
all pass was almost certainly read correctly; a table with failures needs a look
(some failures are inconsistencies in NCRB's own printing, see
[docs/DATA_NOTES.md](docs/DATA_NOTES.md)). Tables with no total rows cannot be
checked this way and have `checks_total = 0`.

## Layout

```
catalog/
  catalog.csv            every file link found on the NCRB listing pages (title, section, year, URL)
  files.csv              one line per unique file: local path, size, SHA-256, download status
  listing_html/          the listing pages as fetched (provenance)
raw/                     the downloaded PDFs / workbooks (not in git, ~8 GB; rebuild with ncrb.download)
  <pub>/<year>/<listing>/<original file name>
data/
  tables_index.csv       one line per extracted table  <- start here
  files_index.csv        one line per source file: pages, OCR pages, tables found, status
  tables/<pub>/<year>/
    <table_id>.csv       the table as printed: one line per row, one column per column
    <table_id>.long.csv  the same cells, tidy: one line per (row, column)
    <table_id>.json      title, source URL and file, pages, header tree, footnotes, checks
  combined/<pub>_cells.parquet   every cell of a publication in one tidy file
  series/<pub>/*.csv     the same table stacked across years (time series)
  series_index.csv       one line per series: title, years covered
  topics_index.csv       one line per topic (NCRB chapter): years covered, number of tables
  quality_by_year.csv    coverage and check results per publication and year
docs/                    documentation (see below)
src/ncrb/                the pipeline
```

`<listing>` is where NCRB lists the file: `table_content` (individual tables of
the report), `additional_table` (extra tables published only online, mostly
Excel), `table_chapter` (chapter PDFs of older Crime in India volumes) and
`year_wise` (whole volumes, chapters, snapshots, front matter).

## Using the data

Find a table, then load it:

```python
import pandas as pd

idx = pd.read_csv("data/tables_index.csv")
hits = idx[(idx.publication == "adsi") & (idx.year == 2020) & idx.title.str.contains("Profession", case=False)]
print(hits[["table_id", "title", "n_rows", "n_cols", "checks_passed", "checks_total"]])

wide = pd.read_csv("data/tables/adsi/2020/2-8_sii-table-2-7-state-ut-2020.csv")        # as printed
long = pd.read_csv("data/tables/adsi/2020/2-8_sii-table-2-7-state-ut-2020.long.csv")   # tidy
```

The tidy file is already in the shape that `df.stack()` plus splitting the
column name used to produce by hand: one row per cell, with the header levels
in `h1`, `h2`, ... and the number in `value`.

```python
import plotly.express as px

d = long[(long.is_total == 0) & (long.h2 != "Total")]
fig = px.bar(d, x="name", y="value", color="h1", hover_data=["h2"],
             title="Profession-wise distribution of suicides, 2020")
fig.show()
```

A time series across years:

```python
s = pd.read_csv("data/series_index.csv")
s[s.title.str.contains("Incidence and Rate of Suicides", case=False)][["series_id", "first_year", "last_year", "n_years"]]
ts = pd.read_csv("data/series/adsi/<series>.csv")     # columns: year, name_std, column, value, ...
```

Everything at once (DuckDB or pandas):

```python
cells = pd.read_parquet("data/combined/adsi_cells.parquet")
cells[(cells.entity_type == "state") & (cells.column.str.contains("Farming"))]
```

Column-by-column descriptions of every file are in
[docs/DATA_FORMAT.md](docs/DATA_FORMAT.md). A runnable example is in
[examples/quickstart.py](examples/quickstart.py).

## Rebuilding

Requires [uv](https://docs.astral.sh/uv/). OCR of the scanned years needs
`tesseract` on the PATH (`brew install tesseract`); on macOS Apple's Vision
framework is used alongside it.

```bash
uv sync
uv run python -m ncrb.crawl       # listing pages -> catalog/catalog.csv
uv run python -m ncrb.download    # catalog -> raw/  (about 13,600 files, 8 GB)
uv run python -m ncrb.extract     # raw/ -> data/tables/ + data/tables_index.csv
uv run python -m ncrb.build       # data/tables/ -> data/combined/ + data/series/
uv run python -m ncrb.report      # -> data/quality_by_year.csv + docs/COVERAGE.md
```

Every step is incremental: it skips what is already done, so a new NCRB release
is picked up by running the five commands again. `--pub cii|psi|adsi` and
`--year N` restrict `download` and `extract`; `extract --force` redoes existing
output; `extract --no-ocr` skips the scanned years.

## Documentation

- [docs/DATA_FORMAT.md](docs/DATA_FORMAT.md): every output file and column
- [docs/DATA_NOTES.md](docs/DATA_NOTES.md): accuracy, known problems, caveats when comparing years
- [docs/PIPELINE.md](docs/PIPELINE.md): how crawling, downloading and table extraction work
- [docs/SOURCES.md](docs/SOURCES.md): the NCRB pages the data comes from
- [docs/COVERAGE.md](docs/COVERAGE.md): generated; counts and check results per year, and files NCRB lists but does not serve

## Source and terms

All data is published by the National Crime Records Bureau, Ministry of Home
Affairs, Government of India, at <https://www.ncrb.gov.in>. This repository
re-formats it; it is not an official NCRB product. When you publish anything
based on it, cite NCRB and the specific report and table, and check the figure
against the source PDF (its URL is in each table's `.json` and in
`data/tables_index.csv`).
