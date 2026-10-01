# Data format

All text files are UTF-8 CSV with a header line. Paths are relative to the
repository root.

## Identifiers

- **publication**: `cii` (Crime in India), `adsi` (Accidental Deaths & Suicides
  in India), `psi` (Prison Statistics India).
- **year**: the year NCRB files the item under, i.e. the reference year of the
  report (Crime in India 2020 covers calendar year 2020).
- **table_id**: `<publication>/<year>/<name>`, unique across the dataset. It is
  also the path of the table's files under `data/tables/`. `<name>` is built from
  NCRB's serial number in the listing and the source file name; when one source
  file holds several tables, `_t<table number>` is appended.

## `data/tables_index.csv`: one line per extracted table

| Column | Meaning |
|---|---|
| `table_id` | see above |
| `publication`, `year` | see above |
| `listing` | NCRB listing the source file came from: `table_content`, `additional_table`, `table_chapter`, `year_wise` |
| `topic` | NCRB's chapter heading for the table, cleaned (`Suicides in India`, `Crime Against Women (States/UTs)`); empty for volumes and front matter |
| `section` | the heading exactly as shown on ncrb.gov.in (`Chapter - 2 -- SUICIDES IN INDIA`) |
| `serial` | NCRB's serial number for the file in that listing (e.g. `2.7`) |
| `table_no` | table number printed in the document itself (e.g. `2.7`, `1B.4`, `VII`), if found |
| `title` | table title. For single-table files this is NCRB's listing title (clean); for tables cut out of multi-table files it is the title read from the page |
| `pdf_title` | title as read from the page, always |
| `method` | `pdf_text`, `excel`, `pdf_vlm` (scanned, read by the document AI model), `pdf_ocr` (scanned, read by Tesseract), `pdf_mixed` (some pages scanned) |
| `n_rows`, `n_cols`, `n_cells` | size; `n_cols` counts data columns, `n_cells` non-empty cells |
| `pages` | first-last page of the table in the source PDF |
| `checks_total`, `checks_passed` | cells of printed geographic TOTAL rows compared with the sum of the rows they cover, and how many matched |
| `inferred_pages` | pages where the table had no printed column numbers and columns were inferred from the layout |
| `warnings` | assembly problems, e.g. facing pages of a scan that could not be aligned |
| `csv` | path of the wide CSV |
| `source_file`, `source_url` | local path under `raw/` and the NCRB URL |

## `data/tables/<pub>/<year>/<name>.csv`: the table as printed ("wide")

One line per table row.

| Column | Meaning |
|---|---|
| `section` | the group heading the row sits under in the table, e.g. `STATES`, `UNION TERRITORIES`, `CITIES`, a crime-head group |
| `sl_no` | the printed serial number of the row |
| third column | the row label (State/UT, city, crime head, year ...). The column is named after the printed heading when one was found, otherwise `name` |
| remaining columns | one per data column, in document order. The name is the header path joined with ` \| `, e.g. `Professionals/Salaried Persons (Total) \| Male`. If two columns end up with the same name, the printed column number is appended in parentheses |

Cells hold the text exactly as printed (`1,234`, `-`, `NA`, `12.5`). Nothing is
converted here; use the long file for numbers.

## `data/tables/<pub>/<year>/<name>.long.csv`: tidy ("long")

One line per non-empty cell.

| Column | Meaning |
|---|---|
| `row` | row order within the table, from 1 |
| `section`, `sl_no`, `name` | as in the wide file |
| `is_total` | 1 if the row is a total / all-India row, else 0 |
| `col_no` | the column number printed under the header: `3`, `4`, ... or a lettered sub-column such as `9a`. Tables without printed numbers get `2`, `3`, ... by position. Numbers from `10001` up are assigned by the extractor when the document reuses a printed number for a different column, or for a block of the table that has no numbers |
| `column` | full column name, same as in the wide file |
| `h1` ... `h5` | the header path split into levels, outermost first (`h1` = spanning heading, last non-empty level = leaf such as `Male`) |
| `value` | the cell as a number; empty when the cell is not numeric (`-`, `NA`, or unreadable) |
| `raw` | the cell text as printed |
| `page` | page of the source PDF (0 for Excel) |
| `ocr_conf` | Tesseract's confidence for the cell, 0–1, on scanned pages; empty for text-layer, Excel and AI-read (`pdf_vlm`) sources |

Number parsing: thousands separators are removed; a trailing `%` and footnote
marks (`*`, `@`, `#`) are dropped; a value in parentheses is read as the number
inside. Dashes, `NA`, `NR`, `Nil` give an empty `value` (not zero: NCRB uses
them for "not available" as well as for nil).

## `data/tables/<pub>/<year>/<name>.json`: metadata

```
table_id, publication, year, listing, section, serial
title, listing_title, pdf_title, table_no
method, sheet (Excel sheet name)
source_url, source_file, source_sha256
row_label            printed heading of the label column(s)
pages                list of source pages
n_rows, n_cols, n_cells
columns              [{col_no, name, header: [level1, level2, ...]}, ...]
notes                footnotes and notes printed under the table
checks               {cells_checked, cells_passed, failures: [...],
                      other_totals_checked, other_totals_passed}
inferred_pages, ocr_pages, warnings
```

`checks.failures` lists up to eight mismatches in words, e.g.
`col 16 'TOTAL (STATES)': printed 15307, sum 15284`. `other_totals_*` count
non-geographic totals (totals inside lists of crime heads or causes); they are
reported but not used as a quality signal because such lists nest sub-items in
ways that differ from table to table.

## `data/files_index.csv`: one line per source file

`source_file`, `publication`, `year`, `listing`, `pages`, `pages_without_text`
(scanned pages), `pages_ocr` (scanned pages that were OCR'd), `ocr_conf` (mean
OCR confidence), `pages_with_table`, `tables`, `status`, `error`.

`status` is `ok` (at least one table), `no_table` (forewords, maps, chapters of
prose, snapshots), `scanned_not_ocred` (run with `--no-ocr`) or `error`.

## `data/combined/<pub>_cells.parquet`

Every line of every `.long.csv` of a publication, with these columns added in
front: `publication`, `year`, `table_id`, `method`, and after `name`:

| Column | Meaning |
|---|---|
| `name_std` | standard name of the row when it is a State, UT or total row (`Odisha` for `ORISSA`, `All India` for `TOTAL (ALL INDIA)`); otherwise the label unchanged |
| `entity_type` | `state`, `ut`, `total` or `other` |

State/UT status is the current one (Delhi, Jammu & Kashmir and Ladakh are
`ut` in every year). See `src/ncrb/entities.py` for the alias list.

Tables from `year_wise` and `table_chapter` files repeat tables that are also
published individually under `table_content`; filter on `table_id` via
`tables_index.csv` (`listing`) if you need each table only once.

## `data/series/<pub>/<series>.csv` and `data/series_index.csv`

A series is one table followed across years. Tables are grouped when their
titles are identical after removing the year ("... during 2019" and
"... during 2020"), within one publication and one geography (`all-india`,
`state-ut`, `city`, `state-ut-city`). Only `table_content` and
`additional_table` tables are used, plus chapter/volume tables for years that
have no individual table files.

Series file columns: `year`, `table_id`, then the long-format columns
(`section`, `sl_no`, `name`, `name_std`, `entity_type`, `is_total`, `col_no`,
`column`, `h1`–`h5`, `value`, `raw`, `ocr_conf`).

`series_index.csv`: `series_id`, `publication`, `topic`, `geography`, `title`,
`first_year`, `last_year`, `n_years`, `years`, `n_tables`, `methods`, `csv`.

Grouping is by title only. NCRB changes wording, column sets and definitions
over time, so a series can break where the title changed (you will find two
series) and columns within a series are not guaranteed to mean the same thing
in every year. Compare the `column` values across years before plotting.

## `data/topics_index.csv`

One line per publication and topic: `publication`, `topic`, `first_year`,
`last_year`, `n_years`, `n_tables`, `n_cells`. Topics are NCRB's own chapter
headings, so they change when NCRB reorganises a report (Crime in India was
restructured in 2016, Prison Statistics in 2016); the same subject can appear
under two headings in different periods.

## `catalog/catalog.csv` and `catalog/files.csv`

`catalog.csv` has one line per link on an NCRB listing page: `publication`,
`listing`, `year`, `section`, `serial`, `title`, `url`, `size_text` (size as
shown on the site), `listing_url`.

`files.csv` has one line per unique URL: `url`, `publication`, `year`,
`listing`, `path` (under `raw/`), `status`, `bytes`, `sha256`, `content_type`,
`error`. `status` is `ok`, `missing` (HTTP 404), `not_a_file` (the server
answered with an error page or an empty body) or `failed` (network error after
retries).
