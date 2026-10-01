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
