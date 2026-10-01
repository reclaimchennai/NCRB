# Chennai over time: traffic accidents and suicides

These scripts follow single NCRB tables across every year they were published, from the oldest edition to 2024. They pull out the rows for Chennai (printed as Madras until 1996), Tamil Nadu, and every State, UT and city, and join the years into one tidy series per question. The point is to show how the numbers changed over time, without opening the raw tables.

```bash
uv run --extra analysis --extra vlm python -m analysis.run
```

The run takes about 30 seconds. It reads `data/web/ncrb.duckdb`, which holds every extracted cell and is built with `python -m ncrb.webdata`, and it writes everything to `analysis/output/`. Open **`analysis/output/report.html`** to see all the charts, each with a short note computed from the data. Each chart is also saved on its own in `analysis/output/charts/`.

## Every State, UT and city: `engine.py` and `export.py`

`engine.py` reads every row of the same tables (not just Chennai's and Tamil
Nadu's), works out which State, UT or city each row is (`resolve`: NCRB's
spellings, old names such as Madras and Bombay, and OCR'd names snapped to the
53 cities NCRB prints), and returns one tidy record per place, year, category,
sex and age group. `export.py` writes them for the website:

```bash
uv run --extra analysis --extra vlm python -m analysis.export          # all datasets, ~6 min
uv run --extra analysis --extra vlm python -m analysis.export traffic_time suicide_rate
```

- `web/data/trends/catalog.json`, and per dataset `index.json` (places, categories, sexes, ages, and every place's headline series) plus one `<type>-<place>.json` per place with rows `[year, group, cat, sex, age, value]` (indexes into the lists in `index.json`).
- `analysis/output/trends_<dataset>.csv.gz`: every record with its source (`ncrb` or `ogd`) and check.

Datasets: `traffic_time`, `traffic_month`, `road_deaths_time`, `road_deaths_month`,
`suicide_means`, `suicide_profession`, `suicide_causes`, `suicide_education`,
`suicide_sex_age`, `suicide_rate`. Causes and education are harmonised like
means and professions (`harmonise.CAUSES`, `harmonise.EDUCATION`).

**Why there are gaps, and which are NCRB's own.** NCRB's site carries no
State-wise suicide tables for 1993–2003: for 1993–2000 it publishes only the
accident tables, and the suicide chapters of those reports hold text and
summary tables (all read with the AI model; only 1993 has a State table, and
its State names did not survive the scan). 2001–2003 come from the data.gov.in
dataset in `data/ogd/`. Real
gaps in the source: suicides by age and sex were printed only for all India in
2016–2020; city-wise tables of suicides by means, profession, education, age
and sex stop after 2015; deaths in traffic accidents by hour and month are
printed only State-wise and only from 2021. A scanned year whose figures do
not add up to the totals printed with them is left out.

## The Chennai-only series (`run.py`)

## What is covered

| Question | Output | Years | Notes |
|---|---|---|---|
| Traffic accidents in Chennai by time of day (polar chart) | `chennai_traffic_by_time.csv` | 1996–1999 (AI OCR), 2001–2024 | Road, railway-crossing, railway and total. NCRB's city tables count **accidents** by time of day, not deaths. |
| Traffic accidents in Chennai by month | `chennai_traffic_by_month.csv` | 1997–1998 (AI OCR), 2000–2024 | Same four groups. |
| Persons killed or injured in traffic accidents by time and month | `tn_traffic_persons_by_time.csv`, `tn_traffic_persons_by_month.csv` | 2021–2024 | Printed only state-wise. These are the only tables that count deaths by time of day. |
| Suicides in Tamil Nadu by means | `tn_suicides_by_means.csv` | 1972 (AI OCR), 2004–2024 | Means names harmonised (`harmonise.py`), printed label kept. |
| … by means, sex and age group | `tn_suicides_by_means_age.csv` | 2021–2024 | |
| Suicides in Tamil Nadu by profession and sex | `tn_suicides_by_profession.csv` | 2004–2024 | In 2014 NCRB split "others" into daily wage earners, agricultural labourers and other groups. |
| … by profession, sex and age group | `tn_suicides_by_profession_age.csv` | 2021–2024 | |
| Suicides by sex and age group, Tamil Nadu | `tn_suicides_by_sex_age.csv` | 2004–2015, 2021–2024 | For 2016–2020 NCRB printed age by sex only for all India. |
| Suicides by sex and age group, Chennai and all big cities | `chennai_suicides_by_sex_age.csv`, `cities_suicides_by_sex_age.csv` | 2004–2015 | Not printed since 2015. |
| Suicide rate, every State/UT and city | `suicide_rates.csv` | 1976, 1988–1992 (scanned), 2004–2024 | Number, % share, population (lakh) and rate per lakh. |
| Chennai's headline figures side by side | `chennai_summary.csv` | 1976–2024 | Joined from the tables above. |
| Every figure printed for Chennai | `chennai_all_figures.csv.gz` | 1953–2024 | All tables in Crime in India and ADSI, about 115,000 cells. |

Each CSV has a `*_sources.csv` file next to it. It lists the table used for each year, how that table was read (`pdf_text`, `excel`, `pdf_ocr` or `pdf_vlm`), its page numbers and the NCRB URL.

**About the 2019 ICD-10 request.** A 2019 "distribution of suicidal deaths in major cities by sex and age group (ICD-10 S00–T98)" comes from the Registrar General's *Medical Certification of Cause of Death* report, not from NCRB, so it is not in this data. The closest NCRB series are the city tables of suicides by sex and age (2004–2015) and city suicide counts and rates (to 2024).

## How a year gets in

1. **Choosing a table.** `topics.py` defines each question as a title pattern, with exclusions and a required column heading. For each year it picks one table that names the place. The table published on its own wins over one cut from the full report, and text or Excel wins over scans.
2. **Reading the row.** The place's row is read and its columns are mapped to categories (time slot, month, means, profession, age group, sex):
   - Text and Excel tables are mapped by NCRB's fixed column order.
   - Scanned tables are mapped by their headings, with position as the fallback.
   - Where a spanning heading was printed over only its last column (for example "Others" in 2004–2011), the columns are moved back to the right category.
3. **Choosing between readings.** For scanned years there can be two readings of the same page: Tesseract and the GLM-OCR document model (`ncrb.vlm`). The one whose figures add up wins.
4. **Checking each year.** Each year is checked against its own printed total, and the result goes into the `check` column:
   - `ok`: the categories add up to the printed total.
   - `mismatch`: they don't.
   - `no total`: nothing to check against.
   - `derived`: a both-sexes figure that was added up from the sexes.

   Charts draw only `ok` and `derived` years. Years read from scans are drawn dashed or shaded.
5. **Extra checks.**
   - Chennai's time-of-day and month tables are two cuts of the same accidents, so their totals must agree. 2000 fails this test and is left out.
   - A suicide rate is kept only where suicides ÷ population matches the printed rate.
   - In a scanned means table, the categories added together must also match Tamil Nadu's total for the year, from the table's grand-total row or the rates table. A single category can pass its own check by chance on a misread page.
   - Rates above 100 per lakh are treated as misreads and blanked.

## Things to know when reading the charts

- **Age groups changed in 2014.** Up to 2013 the groups were up to 14, 15–29, 30–44, 45–59 and 60+. From 2014 they are below 14, 14–17, 18–29, 30–44, 45–59 and 60+, so 30–44, 45–59 and 60+ run unbroken from 2004. The age charts draw the younger groups together as "under 30".
- **City rates use a fixed census population.** Chennai's is 64.3 lakh up to 2010 and 87 lakh from 2011, so a change in Chennai's rate is a change in the count. The count fell from 2,699 in 2021 to 1,581 in 2022.
- **2018 and 2020 time-of-day figures.** In both years Chennai's 00–03 h count is unusually large. That is how NCRB printed it, and the same figures appear in the state/city table and in the full report.
- **Gaps:**
  - Chennai's 1995 time-of-day table is read, but its road figures are 3% off the printed total, so it is left out.
  - The 1993–2003 suicide-rate tables are not on NCRB's site as separate tables.
  - The scanned suicide tables from before 1993 are noisy. They are being re-read with the AI model; see below.

## Filling the older years

The AI OCR pass runs page by page, at about a minute per page on an M-series Mac. Its cache lives in `data/ocr_cache/`. The scanned tables these questions need are queued first:

- `vlm_targets.json`: Chennai traffic 1996–2000; suicide means, rates, and sex and age 1967–1992.
- `vlm_targets_extra.json`: Chennai traffic 1995 and 1999; state-wise means tables 1967–1990.

To queue them yourself:

```bash
uv run --extra vlm python -m ncrb.vlm_run --pages analysis/vlm_targets.json
uv run --extra vlm python -m ncrb.vlm_run --pages analysis/vlm_targets_extra.json
```

When pages are cached, re-run `python -m analysis.run`. `series.py` reads the AI OCR cache directly and uses a reading wherever it adds up better than Tesseract's.

## Files

| File | Role |
|---|---|
| `lib.py` | Database access; finding tables; one table per year; place patterns (Chennai/Madras, Tamil Nadu) |
| `topics.py` | The questions, as table-finding rules |
| `series.py` | Reading a place's row into categories, checks, the AI OCR alternative, State/city rate parsing |
| `harmonise.py` | One list for means, professions and age groups across editions |
| `run.py` | Builds every CSV |
| `charts.py`, `report.py` | Plotly charts and `report.html` |
