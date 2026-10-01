# Open Government Data: Suicides in India 2001–2012

`suicides-in-india-2001-2012.csv.gz` is the State-wise dataset of suicides by
causes, means adopted, professional profile, educational status and social
status, by sex and age group, for 2001–2012, that NCRB contributed to the Open
Government Data platform (data.gov.in). This copy was taken from the mirror at
github.com/elseasama/Indian-cities-births-and-deaths
(`Suicides in India 2001-2012.csv`), unchanged apart from compression.

Columns: `State, Year, Type_code, Type, Gender, Age_group, Total`.

It is used by `analysis/engine.py` to fill 2001–2003 (NCRB's website carries
no State-wise suicide tables for those years) and to give the age breakdown of
every suicide table up to 2012. Where NCRB's own published table exists for a
year, that table is used for the figures it prints; the two agree on the
yearly totals for 2004–2012 except Professional Profile in 2009 (14,136 here
against 14,424 printed for Tamil Nadu).

## OpenDataChennai copies of ADSI tables

Two tables copied from the ADSI reports into Reclaim Chennai's
github.com/elseasama/OpenDataChennai repository, unchanged here:

- `opendatachennai-suicide-rate-state-city-1998-2020.csv` (there:
  `suicideratestatecity2009-2020.csv`): number, share, population and rate of
  suicides for every State, UT and city, 1998–2020. For 2004–2020 it matches
  NCRB's published tables figure for figure; `analysis/engine.py` uses it only
  for 1998–2003, which NCRB's site does not carry, and drops rows whose
  number ÷ population does not give the rate, or whose rate is more than
  three times off the place's own 2004–2010 level (Chennai 1998–1999).
- `opendatachennai-suicides-major-cities-sex-age-2019.csv` (there:
  `SuicidalDeathsinMajorCitiesSexAge2020.csv`): suicides by sex and age group
  in the 53 big cities. Its city totals equal NCRB's 2019 figures (Agra 129,
  Ahmedabad 763, Asansol 469; 2020 is 115, 871, 329), so it is the 2019 table
  and is used as such. NCRB's site does not list this table.
