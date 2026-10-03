# NCRB: Crime in India, Accidental Deaths & Suicides in India, Prison Statistics India

Every table the National Crime Records Bureau (NCRB) has published for its three
annual statistical reports, taken out of the PDFs and spreadsheets on
[ncrb.gov.in](https://www.ncrb.gov.in) and turned into CSV, JSON and Parquet,
with the source files, the code that did it, and a check on every table.

**Explore it in the browser:** <https://ncrb.reclaimchennai.city/>
(search, read a table as printed, chart and map it, follow it across years).

| Code | Publication | Years | Files | Tables | Figures |
|---|---|---|---:|---:|---:|
| `cii` | Crime in India | 1953–2024 | 9,579 | 27,971 | 21.2 M |
| `adsi` | Accidental Deaths & Suicides in India | 1967–2024 | 1,460 | 3,382 | 4.0 M |
| `psi` | Prison Statistics India | 1995–2024 | 2,480 | 4,778 | 1.7 M |
| | **All** | | **13,519** | **36,131** | **26.9 M** |

Counts and quality for every publication and year: [docs/COVERAGE.md](docs/COVERAGE.md).

## Contents

- [What is in this repository and what is in the releases](#what-is-where)
- [How much to trust the numbers](#how-much-to-trust-the-numbers)
- [How the data was collected and extracted](#how-the-data-was-collected-and-extracted)
- [Using the data](#using-the-data)
- [Rebuilding everything](#rebuilding-everything)
- [Explore: every recurring table](#explore-every-recurring-table-year-by-year) · [long series since 1953](#long-series-since-1953) · [boundaries as they were](#boundaries-as-they-were) · [cloud OCR](colab/README.md)
- [Trends dashboard and the Chennai report](#trends-dashboard-and-the-chennai-report)
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
| `pdf_vlm` | scanned page read by a document AI model (OvisOCR2 on a cloud GPU, see [colab/](colab/README.md); a few by GLM-OCR) | before ~2000 | good, not exact: check against the PDF |
| `pdf_ocr`, `pdf_mixed` | scanned page read by Tesseract OCR | before ~2000 | best effort: digits can be wrong or missing |

**The totals check.** Wherever NCRB prints `TOTAL (STATES)`, `TOTAL (UTs)`,
`TOTAL (CITIES)` or `TOTAL (ALL INDIA)`, the extracted rows above are added up
and compared with the printed figure, column by column. A misread or misplaced
digit breaks the sum, so a table whose totals all match was almost certainly
read correctly. Results per table are `checks_total` / `checks_passed`.

| | Crime in India | ADSI | Prison Statistics |
|---|---:|---:|---:|
| Text PDFs & Excel: share of checked totals that match | 99.4% | 99.7% | 99.3% |
| Scanned volumes: share that match | 90% | 91% | 95% |

The scanned tier was re-read in October 2026 by OvisOCR2, the document model
that reproduced the most printed totals in a bake-off on 280 of NCRB's own
scanned pages (78.9%, against 66.4% for PaddleOCR-VL-1.6). Each scanned file
keeps whichever reading, Tesseract or a model, matches its printed totals best;
where neither has a total to check, the model's reading is used. Across the
scanned years this raised the share of checked totals that match from 57% to
92%, the number of totals that can be checked at all from 12,838 to 41,009,
and the tables extracted from 3,818 to 5,123.

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

## Explore: every recurring table, year by year

**<https://ncrb.reclaimchennai.city/explore/>** follows every table that
Crime in India, ADSI and Prison Statistics printed in three or more editions
(1,157 tables: 891 Crime in India, 101 ADSI, 165 Prison Statistics) across the years, even where NCRB reworded the title. Pick a
report, a topic, a table, a category, a breakdown (all / male / female / ...)
and a State, UT, city or row: a trend line, a ranking and an India map that
play through the years, and a heatmap of every category in every year. Every
chart title and snapshot names the category, breakdown and place shown.
District-wise tables are left out (they are on the Tables page). Built by
`python -m analysis.families` into `web/data/explore/` (not in git; deployed
with the site and in the data release).

How tables are joined, and why gaps remain:

- **Topics** come from [analysis/taxonomy.py](analysis/taxonomy.py): one list of
  topics per report, matched on the table title first and NCRB's chapter
  second. Geography (States/UTs, cities, all India) is a separate property, so
  "Cyber Crimes (States/UTs)" and "Cyber Crimes (Metropolitan Cities)" are one
  topic. Titles lose numbering, years, "(Contd.)", Roman-numeral part labels and
  any running text a chapter PDF carried along.
- **Columns** are split into a category and a breakdown (Total / Male /
  Female / Transgender / Boys / Girls). Categories that cite a section are
  matched by section number, so "Sec. 66" stays one series when its wording
  changes. Totals and subtotals are flagged, listed last and kept off the
  heatmap colour scale. Legal sections and Acts get a plain-language note
  ([web/kit/legal.js](web/kit/legal.js)).
- **Editions** are joined by title words and shared categories. A second pass
  bridges NCRB's 2014 redesign (most Crime in India tables were renamed), and
  one-off titles are attached to the family whose columns they share.
  Figures that later editions reprint for earlier years (the "2014 | 2015 |
  2016" columns) fill years whose own edition has no matching table.
- Tables printed only in the year-wise or chapter PDFs are kept; reprints of an
  individual table are dropped.
- **Gaps that remain are real:** NCRB dropped, split or merged many tables
  (about 410 Crime in India tables stop at 2013; 170 now run across the 2014 redesign), some editions print a
  category in one year only, and scanned pages whose figures do not add up
  to their own totals are left out instead of guessed.

### Long series since 1953

The core Crime in India figures, cases registered under each main IPC crime
head (murder, dacoity, robbery, burglary, theft, riots, kidnapping, cheating,
rape, dowry deaths ... and total IPC crime) for every State, UT and big city,
were printed in every edition but in tables of a different shape in each era.
[analysis/longseries.py](analysis/longseries.py) collects every printed figure
for a place, head and year from whichever table holds it, including the
previous-year columns comparative tables reprint, and keeps the best-supported
reading:

- a text-layer figure (2001 on) is taken as printed;
- before that, a figure printed alike in two or more tables wins;
- otherwise the reading that makes the most consistent series is chosen
  (a table's first column preferred, as it is the cases column), and it is
  kept only if it is within a factor of 2 of its neighbouring years.

Every figure's source table and how it was chosen is in
`web/data/explore/cii/long-series-provenance.csv`. The scanned decades
(1970s–1990s especially) still have gaps where Tesseract garbled the
headings; the cloud OCR run in [colab/](colab/README.md) is meant to close them.

### Boundaries as they were

Maps draw the States and UTs of the year shown: 22 boundary eras from 1951
(Part A/B/C States) through the 1956 reorganisation, Maharashtra and Gujarat
(1960), Punjab and Haryana (1966), the North-East (1972), Sikkim (1975), the
2000 States, Telangana (2014), Ladakh (2019) and the 2020 merger of Dadra &
Nagar Haveli with Daman & Diu, built from 2011 census districts
([web/geo/README.md](web/geo/README.md) lists every approximation). Renamed
States continue under today's name (Madras is Tamil Nadu, Mysore is
Karnataka); States that were split or merged away keep their own (Bombay
State to 1959, Hyderabad State, PEPSU, Travancore-Cochin, Madhya Bharat,
Saurashtra ...), so no modern State's series silently includes another's
territory. Madras State still included Malabar until 1956 and the Andhra
districts until 1953, so Tamil Nadu's figures for 1953–1956 cover more ground.

## Trends dashboard and the Chennai report

**<https://ncrb.reclaimchennai.city/trends/>**: traffic accidents and
suicides for every State, UT and big city, every year, with play, snapshot
and video recording. **<https://ncrb.reclaimchennai.city/chennai/>**: the
same charts arranged as the story of Chennai and Tamil Nadu.

| Dataset | Years | Places |
|---|---|---|
| Traffic accidents by time of day | 1995–2024 | States, UTs, 23 cities (1995–2000), 35 (2001–2010), 53 (2011–) |
| Traffic accidents by month | 1996–2024 | same |
| Persons killed in traffic accidents by time of day / month | 2021–2024 | States and UTs (not printed city-wise) |
| Suicides by means, profession, cause, education (by sex; by age 2001–2012 and 2021–) | 2001–2024 | States and UTs; cities 2004–2015 (causes to 2024) |
| Suicides by age group and sex | 2001–2015, 2021–2024 | States and UTs; cities 2004–2015 and 2019 (NCRB printed only all-India figures in 2016–2020) |
| Suicides, population and rate | 1976, 1988–1992, 1998–2024 | States, UTs, cities |

2001–2003, and the age breakdown of every suicide table up to 2012, come from
*Suicides in India 2001–2012*, the State-wise dataset NCRB contributed to
data.gov.in ([data/ogd/](data/ogd/README.md)); NCRB's site carries no
State-wise suicide tables for 2001–2003. Suicide rates for 1998–2003 and the
2019 city table of suicides by sex and age come from copies of ADSI tables in
Reclaim Chennai's OpenDataChennai repository (also in `data/ogd/`). Everything
else is NCRB's published tables, read and checked as described above. Every
picture or video saved from a chart names the tables and sources behind the
years it shows.

```bash
uv run --extra analysis --extra vlm python -m analysis.export   # web/data/trends/ and analysis/output/trends_*.csv.gz
```

How each series is joined across the years, and the Chennai-only CSVs and
plotly report from the earlier analysis: [analysis/README.md](analysis/README.md).

## Documentation

- [docs/DATA_FORMAT.md](docs/DATA_FORMAT.md): every file and column
- [docs/DATA_NOTES.md](docs/DATA_NOTES.md): accuracy, known problems, comparing years
- [docs/PIPELINE.md](docs/PIPELINE.md): how crawling, downloading and extraction work
- [docs/SOURCES.md](docs/SOURCES.md): the NCRB pages the data comes from
- [docs/COVERAGE.md](docs/COVERAGE.md): counts and check results per year; files NCRB lists but does not serve
- [ARCHITECTURE.md](ARCHITECTURE.md): how the dashboard is deployed
- [analysis/README.md](analysis/README.md): the Chennai time series, how years are joined and checked

## Source and terms

All figures are published by the National Crime Records Bureau, Ministry of
Home Affairs, Government of India, at <https://www.ncrb.gov.in>. This
repository re-formats them; it is not an official NCRB product. When you use
it, cite NCRB and the specific report and table, and check the figure against
the source PDF linked from each table.

The code in this repository is released under the MIT License (see
[LICENSE](LICENSE)).
