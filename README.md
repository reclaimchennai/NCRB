# NCRB: Crime in India, Accidental Deaths & Suicides in India, Prison Statistics India

Every table the National Crime Records Bureau (NCRB) has published for its three
annual statistical reports, taken out of the PDFs and spreadsheets on
[ncrb.gov.in](https://www.ncrb.gov.in) and turned into CSV, JSON and Parquet,
with the source files, the code that did it, and a check on every table.

**Explore it in the browser:** <https://cpi.reclaimchennai.city/ncrb/>
(search, read a table as printed, chart and map it, follow it across years).

| Code | Publication | Years | Files | Tables | Figures |
|---|---|---|---:|---:|---:|
| `cii` | Crime in India | 1953–2024 | 9,579 | 27,971 | 21.2 M |
| `adsi` | Accidental Deaths & Suicides in India | 1967–2024 | 1,460 | 3,383 | 4.0 M |
| `psi` | Prison Statistics India | 1995–2024 | 2,480 | 4,778 | 1.7 M |
| | **All** | | **13,519** | **36,132** | **26.9 M** |

Counts and quality for every publication and year: [docs/COVERAGE.md](docs/COVERAGE.md).

## Contents

- [What is in this repository and what is in the releases](#what-is-where)
- [How much to trust the numbers](#how-much-to-trust-the-numbers)
- [How the data was collected and extracted](#how-the-data-was-collected-and-extracted)
- [Using the data](#using-the-data)
- [Rebuilding everything](#rebuilding-everything)
- [Documentation](#documentation) · [Source and terms](#source-and-terms)

## What is where

**In the repository** (browsable on GitHub):

```
data/
  tables_index.csv          one line per table: title, year, topic, method, size, totals check, source URL   <- start here
  tables/<pub>/<year>/
    <table>.csv             the table as printed: one row per row, one column per column, cells exactly as printed
    <table>.json            title, source URL, pages, header levels, footnotes, totals-check result
  files_index.csv           one line per source file: pages, scanned pages, tables found
  series_index.csv          tables followed across years (1,871 series)
  series_members.csv        which table of which year belongs to which series
  topics_index.csv          NCRB's chapter headings, with the years each covers
  quality_by_year.csv       coverage and check results per publication and year
catalog/
  catalog.csv               every link found on the NCRB listing pages: title, chapter, year, URL
  files.csv                 one line per file: URL, local path, size, SHA-256, download status
  listing_html/             the listing pages as fetched, for provenance
docs/                       format, method, caveats, sources, coverage
src/ncrb/                   the pipeline (Python)
api/, web/                  the dashboard
```

**In the [releases](https://github.com/reclaimchennai/NCRB/releases)** (too large for git):

| Release | Asset | What |
|---|---|---|
| `raw-files` | `ncrb-raw-<pub>-<years>.tar` | every source PDF, Excel and Word file as downloaded (8.3 GB in six parts). Untar in the repository root to get `raw/<pub>/<year>/<listing>/<file>`; `catalog/files.csv` has each file's URL and SHA-256 |
| `data-<date>` | `ncrb-tables-long-<pub>.tar.zst` | the tidy version of every table: one row per cell, header levels split into columns, numbers parsed |
| | `ncrb-cells-<pub>.parquet` | all cells of a publication in one file (with standard State/UT names) |
| | `ncrb-series-<pub>.tar.zst` | each series as one CSV, all years stacked |
| | `ncrb-dashboard.duckdb.zst` | the database behind the dashboard |
| | `ncrb-ocr-cache.tar.zst` | raw output of the OCR model for every scanned page it has read |

Unpack `.tar.zst` with `zstd -d -c file.tar.zst | tar -x` (or `tar --zstd -xf`).

## How much to trust the numbers

Every table says how it was read (`method` in `tables_index.csv` and in its
`.json`), and every table that prints State, UT, city or all-India totals is
checked against them.

| `method` | Source | Years | Reliability |
|---|---|---|---|
| `pdf_text` | PDF with a text layer | ~2000 on | digits copied from the file, not recognised |
| `excel` | NCRB's own spreadsheets | 2004 on (online tables) | digits copied |
| `pdf_vlm` | scanned page read by a document AI model (GLM-OCR) | before ~2000 | good, not exact: check against the PDF |
| `pdf_ocr`, `pdf_mixed` | scanned page read by Tesseract OCR | before ~2000 | best effort: digits can be wrong or missing |

**The totals check.** Wherever NCRB prints `TOTAL (STATES)`, `TOTAL (UTs)`,
`TOTAL (CITIES)` or `TOTAL (ALL INDIA)`, the extracted rows above are added up
and compared with the printed figure, column by column. A misread or misplaced
digit breaks the sum, so a table whose totals all match was almost certainly
read correctly. Results per table are `checks_total` / `checks_passed`.

| | Crime in India | ADSI | Prison Statistics |
|---|---:|---:|---:|
| Text PDFs & Excel: share of checked totals that match | 99.4% | 99.7% | 99.3% |
| Scanned volumes (OCR): share that match | 53% | 51% | 37% |

Failures in the text tier are mostly NCRB's own totals not adding up, or a
heading put on the wrong column; in the scanned tier they are misread digits.
Tables without total rows (`checks_total = 0`) are unmeasured, not bad. The
details, and what changes between years (State boundaries, city lists, crime
heads), are in [docs/DATA_NOTES.md](docs/DATA_NOTES.md). **Check any figure
from before 2000 against its source PDF before publishing it.** Every table's
`.json` and index row has the source URL and page numbers.

## How the data was collected and extracted

1. **Catalogue.** The crawler reads NCRB's listing pages for each publication,
   every year in each page's year filter (`year_wise`, `table_content`,
   `additional_table`, `table_chapter`; see [docs/SOURCES.md](docs/SOURCES.md)).
   The site serves Hindi until the session is switched to English through the
   site's own language API. 13,626 file links were found; 13,519 downloaded;
   107 are dead links on NCRB's side (listed in COVERAGE.md).
2. **Download.** One copy per file, checked against its file type (the server
   answers some dead links with an HTML error page), with size and SHA-256
   recorded in `catalog/files.csv`.
3. **Text PDFs** (the bulk of the data, ~2000 onwards). Tables are rebuilt from
   word coordinates. NCRB prints a row of column numbers `(1) (2) (3)…` under
   every header, continued across "(Contd.)" pages; that row fixes every
   column's position and identity, so a table split over dozens of pages, by
   rows or by columns, is stitched back exactly. Header levels come from the
   ruled or shaded header cells where the PDF draws them, otherwise from the
   layout. Figures are assigned to columns by their right edge (they are
   right-aligned); wrapped row labels, section headings and footnotes are
   recognised. Details: [docs/PIPELINE.md](docs/PIPELINE.md).
4. **Excel workbooks.** Merged header cells give the header levels; sheets that
   stack several tables, or place them side by side, are split.
5. **Scanned volumes** (before ~2000: 11,656 pages). Two readings are made:
   - **Tesseract 5** on the page with its ruling lines erased first (lines
     touching digits are the main cause of dropped figures), deskewed, then the
     same table logic as text PDFs, with OCR-specific repairs (`ll`→11, raised
     decimal points, two-page spreads joined row by row).
   - **GLM-OCR** (Z.ai), a small (about 1B-parameter) document vision-language
     model, run locally with [mlx-vlm](https://github.com/Blaizzy/mlx-vlm) on
     Apple Silicon. It reads the page image and writes the table as HTML,
     structure included; the HTML is parsed into the same grid the Excel
     reader uses. On a benchmark of scanned pages, its totals matched 84.3%
     of the time against 69.6% for Tesseract.
   For each scanned file the reading that scores better on the totals check is
   kept (a failed total counts twice a matched one), so no file whose totals
   can be checked got worse. The model is slow on a laptop (~50 s a page), so
   the AI reading covers the scanned pages processed so far, worst-scoring
   tables first; `files_index.csv` notes which files use it. Run
   `python -m ncrb.vlm_run` to continue it.
6. **Build.** All cells into one Parquet file per publication, standard
   State/UT names (`ORISSA` → Odisha), tables grouped into series across years
   by title, and the dashboard database.

## Using the data

Find a table, then load it:

```python
import pandas as pd

idx = pd.read_csv("data/tables_index.csv", low_memory=False)
hits = idx[(idx.publication == "adsi") & (idx.year == 2020) & idx.title.str.contains("Profession", case=False)]
print(hits[["table_id", "title", "n_rows", "n_cols", "checks_passed", "checks_total"]])

wide = pd.read_csv("data/tables/adsi/2020/2-8_sii-table-2-7-state-ut-2020.csv")   # as printed
```

The long (tidy) file, from the `data-*` release or rebuilt locally, has one row
per cell with the header levels in `h1`…`h5` and the number in `value`, the
shape that `df.stack()` and splitting column names would produce by hand:

```python
import plotly.express as px

long = pd.read_csv("data/tables/adsi/2020/2-8_sii-table-2-7-state-ut-2020.long.csv")
d = long[(long.is_total == 0) & (long.h2 != "Total")]
px.bar(d, x="name", y="value", color="h1", hover_data=["h2"]).show()
```

Everything at once:

```python
cells = pd.read_parquet("ncrb-cells-adsi.parquet")     # from the release
cells[(cells.entity_type == "state") & cells.column.str.contains("Farming")]
```

Every file and column is described in [docs/DATA_FORMAT.md](docs/DATA_FORMAT.md);
[examples/quickstart.py](examples/quickstart.py) finds a table, charts it and
plots a series.

## Rebuilding everything

Requires [uv](https://docs.astral.sh/uv/) and, for the scanned years,
`tesseract` (`brew install tesseract`). The AI OCR needs Apple Silicon
(`uv sync --extra vlm`).

```bash
uv sync
uv run python -m ncrb.crawl       # listing pages      -> catalog/catalog.csv
uv run python -m ncrb.download    # catalog            -> raw/  (or untar the raw-files release)
uv run python -m ncrb.extract     # raw/               -> data/tables/, data/tables_index.csv
uv run --extra vlm python -m ncrb.vlm_run   # optional: AI reading of scanned pages (resumable)
uv run python -m ncrb.extract --force --scanned --vlm-ready   # re-extract files the AI has finished
uv run python -m ncrb.build       # -> combined Parquet, series
uv run python -m ncrb.report      # -> data/quality_by_year.csv, docs/COVERAGE.md
uv run python -m ncrb.webdata     # -> dashboard database
```

Every step is incremental. `--pub cii|adsi|psi`, `--year N` and `--listing`
narrow `download` and `extract`.

## Documentation

- [docs/DATA_FORMAT.md](docs/DATA_FORMAT.md): every file and column
- [docs/DATA_NOTES.md](docs/DATA_NOTES.md): accuracy, known problems, comparing years
- [docs/PIPELINE.md](docs/PIPELINE.md): how crawling, downloading and extraction work
- [docs/SOURCES.md](docs/SOURCES.md): the NCRB pages the data comes from
- [docs/COVERAGE.md](docs/COVERAGE.md): counts and check results per year; files NCRB lists but does not serve
- [ARCHITECTURE.md](ARCHITECTURE.md): how the dashboard is deployed

## Source and terms

All figures are published by the National Crime Records Bureau, Ministry of
Home Affairs, Government of India, at <https://www.ncrb.gov.in>. This
repository re-formats them; it is not an official NCRB product. When you use
it, cite NCRB and the specific report and table, and check the figure against
the source PDF linked from each table.

The code in this repository is released under the MIT License (see
[LICENSE](LICENSE)).
