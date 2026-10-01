# How the pipeline works

Five stages, each a module under `src/ncrb/` that can be run on its own.

```
ncrb.crawl     ncrb.gov.in listing pages  ->  catalog/catalog.csv
ncrb.download  catalog                    ->  raw/ + catalog/files.csv
ncrb.extract   raw/                       ->  data/tables/ + data/tables_index.csv + data/files_index.csv
ncrb.build     data/tables/               ->  data/combined/*.parquet + data/series/
ncrb.report    indexes                    ->  data/quality_by_year.csv + docs/COVERAGE.md
```

## 1. Crawl (`crawl.py`)

NCRB lists each publication's files on pages with a year filter
(see [SOURCES.md](SOURCES.md)). For every listing and every year in its
drop-down the crawler requests `<page>.html?year=<Y>&category=&keyword=` and
records every link to a `.pdf`, `.xls(x)`, `.doc(x)`, `.zip` or `.csv` file,
together with the heading it appears under, its serial number and its title.

Two details matter when re-running it:

- The site serves Hindi until the session language is switched. The crawler
  does what the site's own "English" button does: `POST /api/language/set`
  with the page's CSRF token.
- Each fetched page is saved in `catalog/listing_html/` and reused on the next
  run. Use `--refresh` to fetch again (needed to pick up a new release).

Requests are sequential with a one-second pause.

## 2. Download (`download.py`)

One download per unique URL, three connections at most, with retries. A file
linked from several listings is stored once, under the most specific listing
(`table_content` before `additional_table`, `table_chapter`, `year_wise`). Every
file is checked against its type's magic number, because the server answers
some dead links with HTTP 200 and an HTML error page; those are recorded as
`not_a_file`. Size and SHA-256 are written to `catalog/files.csv`.

## 3. Extract (`extract.py`, `pdftable.py`, `assemble.py`, `xlstable.py`, `ocr.py`)

### PDFs with a text layer

The extractor works from word coordinates (PyMuPDF), not from a generic table
detector. NCRB tables share a convention that makes this reliable: under the
column headings there is a row of column numbers, `(1) (2) (3) ...`, and the
numbering continues on "(Contd...)" pages.

Per page (`pdftable.py`):

1. **Words and lines.** Words are grouped into visual lines. Tokens that the
   PDF splits mid-word with no gap (`3` `2` for 32) are rejoined. Page headers,
   footers and page numbers are dropped.
2. **Anchor.** The column-number row is located. It fixes each column's x
   position and identity. Older tables print bare numbers (`1 2 3 4`); those
   are accepted when they run consecutively. A page may hold several anchors
   (several tables, or a table continued in blocks); each starts a segment.
3. **Title and header.** Lines above the anchor are split into title (larger
   type, `TABLE n`, outside the ruled grid) and header.
4. **Header hierarchy.** Each heading is attached to the columns it spans.
   Where the PDF draws cell borders or shaded cells, those rectangles give the
   exact span of merged cells. Otherwise geometry decides: a heading belongs to
   the columns it lies over; a continuation line is joined to the heading above
   it; a centred spanner, narrower than its span, is widened symmetrically and
   over any group beneath it that it partly covers.
5. **Body.** Every token below the anchor is put in the column whose range
   contains it. Because figures are right-aligned while the column numbers are
   centred, columns whose figures share a right edge are re-assigned by that
   edge. Leading non-numeric columns are the row label (with a serial-number
   column if present). Label lines without figures become section headings
   (`STATES`, `UNION TERRITORIES`) or, when they hug a row, part of a wrapped
   label. Text after the last row of figures is kept as notes.
6. **No anchor.** Tables printed without column numbers (typically exported
   from Excel) get columns from where the figures line up; the ruled grid then
   supplies the header spans. Pages that continue a table without repeating its
   header inherit the previous page's columns.

Across pages (`assemble.py`): segments with the same table number, or untitled
continuations, are merged into one table. A page whose rows are already known
adds columns; a page with new rows adds rows. Rows are matched on serial number
and label, tolerating a missing serial or a label that wraps differently. When
the document reuses a printed column number for a different column (wide tables
repeat `(3) No. of cases` in each block), the later column gets a new number
from 10001 up rather than overwriting the earlier one.

### Excel workbooks (`xlstable.py`)

The grid is given, so the work is segmentation: each sheet is scanned for
title rows, header rows (merged cells give the hierarchy), an optional
column-number row and body rows; several tables stacked on a sheet are
separated; blocks that continue a table sideways are joined.

### Scanned pages (`ocr.py`)

Pages without a text layer are rendered at 300 dpi and recognised:

1. Ruling lines are erased from the image first. Figures touching a cell
   border are otherwise dropped or misread; on the gridded 1990s tables this
   step is what makes whole columns readable at all.
2. Tesseract 5 (`--psm 6`) supplies words with boxes and confidences. Apple
   Vision can be added (`NCRB_OCR_ENGINE=both`, macOS only) to fill in tokens
   Tesseract missed, notably rows of column numbers; it is off by default
   because it refuses to run in worker processes while the screen is locked,
   which would make results depend on the session. The published data was
   produced with Tesseract alone.
3. Coordinates are deskewed using Tesseract's line grouping.
4. The words go through the same table logic as text PDFs, with repairs
   specific to OCR: column numbers such as `14)` for `(4)`; `ll` for 11; a lone
   `O` for 0; a raised decimal point read as `-` (`148-9` for 148.9); dot
   leaders between label and figures; `TOTAL` set in small capitals.
5. Book scans print wide tables across facing pages. The right-hand page has
   no row labels; its rows are attached to the left-hand page's rows in order
   when the counts agree, and flagged in `warnings` when they do not.

Each OCR cell keeps its confidence (`ocr_conf`).

### Scanned pages, second reading: a document AI model (`vlm.py`, `vlm_tables.py`, `vlm_run.py`)

Character OCR leaves the table structure to be rebuilt from word positions,
which is where most errors on the old scans come from. A document
vision-language model reads the page image and writes the whole table as HTML,
merged header cells included. The model is **GLM-OCR** (Z.ai), run locally
through `mlx-vlm` on Apple Silicon with the prompt `Table Recognition:` on a
rendering of the page at 1,600 px on its long edge.

Five recent document models were tried on the same pages (GLM-OCR,
PaddleOCR-VL 1.5, dots.ocr, DeepSeek-OCR-2, Qwen3-VL-8B); GLM-OCR was the
fastest of the accurate ones and reproduced a gridded 1997 table cell for
cell. On the benchmark in `bench/pages.json` (20 scanned files across the
three publications, 1971–2000) its tables matched 365 of 433 checked totals
(84.3%) against 300 of 431 (69.6%) for the Tesseract path.

The model's HTML is parsed into a grid (rowspan/colspan become merged ranges)
and goes through the Excel reader. Three mistakes the model makes are repaired
first:

- a heading cell that covers both label columns is written one column wide,
  shifting every heading to its right; the headings are realigned to the width
  of the data rows;
- the row of column numbers is written a cell or two off; the trailing numbers
  are given to the columns that hold figures;
- a total's label is written on its own row above its figures; the rows are
  joined.

Occasionally the model writes plain lines instead of a table; those are
rebuilt row by row, keeping only rows with the full number of figures.

Raw model output is cached per page in `data/ocr_cache/<model>/<file
hash>/<page>.txt` (published in the `data-*` release), so readings survive
restarts and can be re-parsed without re-running the model. `vlm_run.py` works
through the scanned files in priority order: individual tables before chapters
and volumes, and within those the files whose current tables fail the most
totals first.

**Choosing between the two readings.** For each scanned file both readings are
scored on the totals check: matched totals minus twice the failed ones. The AI
reading replaces the Tesseract one only if it scores higher; such files are
marked `method = pdf_vlm` and `files_index.csv` records both scores. Files
with no totals to check keep the Tesseract reading. So the switch can only
improve the files whose correctness can be measured.

At about 50 seconds a page on the laptop used (its GPU shared with other
work), the 11,656 scanned pages are a multi-day job; the published data
includes the pages read so far, and `files_index.csv` shows which files use
the AI reading.

### Validation

For every table, each printed geographic total (`TOTAL (STATES)`,
`TOTAL (UTs)`, `TOTAL (CITIES)`, `TOTAL (ALL INDIA)`) is compared with the sum
of the rows it covers, column by column; an all-India total is compared with
the sum of the state and UT totals. Columns of rates, percentages and averages
(recognised by heading or by containing decimals) are skipped, as are tables
that are rates throughout. Results are stored per table and summarised in
[COVERAGE.md](COVERAGE.md).

This check catches misplaced, split and missing figures in the rows it covers.
It does not cover header text, row labels, or tables without total rows.

## 4. Build (`build.py`, `entities.py`)

Concatenates the long files into one Parquet file per publication, adding a
standard State/UT name, and stacks same-titled tables across years into series
(see [DATA_FORMAT.md](DATA_FORMAT.md)).

## 5. Report (`report.py`)

Aggregates the indexes into `data/quality_by_year.csv` and regenerates
[COVERAGE.md](COVERAGE.md).
