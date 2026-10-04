# Hand-read tables

Tables read from the page images of NCRB PDFs we hold, where the OCR models' readings do not add up. One Python file per
table: `KIND`, `YEAR`, `PUB`, `SOURCE` (the PDF), `PAGES`, `CATS` (columns in printed order, the last one the Total),
`ROWS` (section -> place -> figures, totals rows included as printed) and `CORRECTIONS`.

A figure is changed from what the page shows only where the row's printed Total and the printed percentage both
confirm the change; each change is listed in `CORRECTIONS` with its reason. `scripts/check_handread.py <file>` checks
every row against its Total and every column against the printed section totals; analysis code uses only files that
pass. On the charts these figures carry the source "read from the page image".

## Kinds

| KIND | CATS | Check |
|---|---|---|
| `means`, `causes` | the categories in printed order, the last one `Total` | every row adds to its Total; every column adds to the printed section totals; States + UTs = Grand Total |
| `traffic` | `["Road accidents (cases)", "Persons injured", "Persons killed"]`, with `CHECK = "columns"` | each column adds to the printed section totals; States + UTs = Grand Total |
| `suicide_incidence`, `accidental_incidence` | `[count, population in lakh, rate per lakh]`, with `CHECK = "incidence"` | counts add to the section totals; every printed rate = count / population |

Sections are `"States"`, `"U.Ts."`, `"Cities"` and `"Grand"` (`{"GRAND TOTAL": [...]}`); totals rows keep their printed
names (`TOTAL (STATES)`, `TOTAL (U.TS.)`, `TOTAL (CITIES)`). Place names as printed (Madras, Bombay ...). `None` for
N.A. or a figure that cannot be read; a row with any `None` in a count column is left out of the data.

File name: `<pub>_<year>_<kind>.py`, e.g. `adsi_1976_means.py`.
