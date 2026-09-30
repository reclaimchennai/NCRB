# Data notes: accuracy, known problems, caveats

## Two tiers

**Text-layer PDFs and Excel (`pdf_text`, `excel`)**: roughly 2000 onwards. The
digits are taken from the file, so a figure is either right or in the wrong
place; it is not misread. Measured by the totals check (see below), these
tables reproduce NCRB's printed totals in about 99% of the cells checked; the
current figures per year are in [COVERAGE.md](COVERAGE.md). What can still go
wrong:

- a heading attached to the wrong column, or a multi-level heading flattened
  in a different order than printed. The figures are in the right column
  position (`col_no`), but the `column` name may be off. Most likely in
  2001–2013 PDFs, which draw no cell borders; least likely from 2014, where
  borders or shading give exact spans.
- a wrapped row label split into two rows or joined to its neighbour;
- a row that appears twice because its label was printed differently on a
  continuation page (the extra row then holds only that page's columns).

**Scanned PDFs (`pdf_ocr`, `pdf_mixed`)**: roughly before 2000, i.e. all of
Crime in India 1953–1999, ADSI 1967–1999 and the first Prison Statistics
volumes. These are photographs of printed books, some at low resolution, read
by OCR. Expect wrong digits (3/8, 5/6, 1/7), dropped digits, missing cells and
garbled headings. `ocr_conf` on each cell is the recogniser's own confidence;
low values are worth checking first, but a high value is not a guarantee. The
totals check passes for well under half of the checked cells in this tier,
and one wrong digit anywhere in a column fails that column's check, so the
per-cell error rate is much lower than that figure suggests, but it is not
negligible. **Treat every OCR figure as unverified until compared with the PDF.**

Particular weaknesses of the scanned tier:

- Wide tables printed across two facing pages are joined row by row. When OCR
  finds a different number of rows on the two pages the right-hand half cannot
  be aligned; those rows are kept, labelled `[unmatched row, page N]`, and the
  table's `warnings` says so.
- Table titles and column headings are often damaged. The `title` in the index
  comes from NCRB's listing where the file holds a single table, which avoids
  this; headings inside the table do not have that fallback.
- Years before about 1970 were typeset with raised decimal points and small
  capitals; both are repaired heuristically.

## What the totals check does and does not tell you

`checks_total` counts cells in printed `TOTAL (STATES)`, `TOTAL (UTs)`,
`TOTAL (CITIES)` and `TOTAL (ALL INDIA)` rows that could be compared with the
sum of the rows above; `checks_passed` counts those that matched.

- All passed: the rows covered by those totals were read correctly, with near
  certainty (a misplaced or misread digit breaks the sum).
- Some failed: either an extraction error in that column, or the source does
  not add up. NCRB tables do contain totals that differ from the sum of their
  rows (late revisions applied to the total only, rounding, a city counted in
  two places). The `.json` lists the failing cells with both numbers, so a
  failure can be judged in seconds against the PDF.
- `checks_total = 0`: the table has no geographic total rows (all-India tables,
  year-wise tables, lists of crime heads), or is a table of rates. Its accuracy
  is unmeasured, not poor.

The check says nothing about column names, row labels, or rate and percentage
columns.

## Files NCRB lists but does not serve

Some links on the listing pages are dead: HTTP 404, an HTML error page
("Some Error occured"), or an empty file. They are recorded in
`catalog/files.csv` with status `missing` or `not_a_file` and listed at the
end of [COVERAGE.md](COVERAGE.md). The tables they would contain may still be
present in the full-volume or chapter files of the same year.

Word documents (`.doc`, 57 files: prefaces, snapshots and similar front matter
from around 2000–2003) are downloaded but not parsed.

## Duplicates

The same table often exists twice: as an individual `table_content` file and
inside a volume or chapter under `year_wise` / `table_chapter`. Both are
extracted and both are in `tables_index.csv` and the combined Parquet files.
Use `listing` to pick one. The series files already avoid the duplication.

## Comparing years

The data is what NCRB printed for each year. It is not harmonised.

- **Boundaries changed.** Chhattisgarh, Jharkhand and Uttarakhand (as
  Uttaranchal) appear from 2000–2001; Telangana from 2014; Ladakh from 2019–2020,
  when Jammu & Kashmir became a UT; Dadra & Nagar Haveli and Daman & Diu are
  one UT from 2020. `name_std` gives one spelling per name, it does not
  reconstruct territories: "Andhra Pradesh" before and after 2014 is the same
  `name_std` but not the same area.
- **The set of cities changed** several times: the city tables cover 23
  cities in the 1990s, 35 in the 2000s and 53 later, and Crime in India moved
  to a shorter list of metropolitan cities (19, and 34 in the online tables)
  from 2016. `TOTAL (CITIES)` is not comparable across those changes; check
  how many city rows a table has before comparing.
- **Definitions and classifications changed**: crime heads were regrouped in
  2014 and again in 2017; suicides by profession was reclassified in 2014
  (farming sector separated); "Transgender" columns appear from 2014; the
  Bharatiya Nyaya Sanhita replaces IPC headings from 2024.
- **Rates** depend on the population estimate NCRB used that year (census
  projections, revised after each census).
- **Table numbers are not stable.** Table 2.7 in one edition is not table 2.7
  in the next; the series files match on titles for that reason, and a change
  of wording splits a series.
- **Revisions.** NCRB sometimes re-issues figures in a later edition (the
  "previous year" column of a later report). This dataset keeps each edition
  as published.

## Conventions in the source worth knowing

- `-`, `NA`, `NR` and blank can each mean nil or not reported, depending on
  the table and year; they are kept as printed in `raw` and left empty in
  `value`. Do not read them as zero without checking the table's notes.
- Indian digit grouping (`1,23,456`) is parsed correctly (123456).
- Figures marked with `*`, `@`, `#` refer to footnotes; the mark is kept in
  `raw`, stripped for `value`, and the footnote text is in the `.json` `notes`.
- Abbreviated headings: `I` incidence (cases), `V` victims or volume, `R` rate,
  `P` percentage, `M`/`F`/`T` male/female/total, `CPV` cases pending
  verification, and so on. They are kept as printed; the expansions are given
  in the table's notes or in the report's glossary (downloaded under
  `raw/<pub>/<year>/year_wise/`).
