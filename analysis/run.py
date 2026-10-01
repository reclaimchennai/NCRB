"""Build every time series, chart and the report in analysis/output/.

    uv run --extra analysis --extra vlm python -m analysis.run

Each series follows one NCRB table across every year it was printed (see
topics.py), reads the row for Chennai / Tamil Nadu / every State and city,
maps the printed headings to fixed categories (series.py, harmonise.py) and
checks each year against its own printed total. Next to every CSV a
*_sources.csv names the table used for each year and how it was read.

    chennai_summary                 headline Chennai figures, one row per year, joined from all tables
    chennai_traffic_by_time         road/railway accidents in Chennai by time of day (1996-)
    chennai_traffic_by_month        ... by month (2000-)
    tn_traffic_persons_by_time      persons injured and died in traffic accidents, Tamil Nadu, by time (2021-)
    tn_traffic_persons_by_month     ... by month (2021-)
    tn_suicides_by_means            suicides in Tamil Nadu by means adopted and sex (2004-)
    tn_suicides_by_means_age        ... by means, sex and age group (2021-)
    tn_suicides_by_profession       suicides in Tamil Nadu by profession and sex (2004-)
    tn_suicides_by_profession_age   ... by profession, sex and age group (2021-)
    tn_suicides_by_sex_age          suicides in Tamil Nadu by sex and age group (2004-2015, 2021-)
    chennai_suicides_by_sex_age     suicides in Chennai by sex and age group (2004-2015)
    cities_suicides_by_sex_age      every big city, by sex and age group (2004-2015)
    suicide_rates                   suicides, population and rate for every State, UT and city (1976-)
    chennai_all_figures.csv.gz      every figure printed against Chennai/Madras in any table
    report.html, charts/*.html      the charts, with a short reading of each
"""

from __future__ import annotations

import re
import warnings

import pandas as pd

from .harmonise import AGE_ORDER, MEANS, PROFESSION, age_band, standard
from .lib import OUT, PLACES, provenance, q, save
from .lib import SCANNED
from .series import CITY_NAMES, MONTHS, SLOTS, category_series, month_slot, suicide_rates, time_slot, traffic, traffic_persons

warnings.filterwarnings("ignore")


def note(df: pd.DataFrame, name: str, picked: pd.DataFrame | None = None) -> None:
    path = save(df, name)
    if picked is not None and not picked.empty:
        save(provenance(picked), f"{name}_sources")
    print(f"  {path.relative_to(OUT.parent.parent)}: {len(df):,} rows")


# --------------------------------------------------------------------------- traffic


def traffic_series() -> dict[str, pd.DataFrame]:
    out = {}
    t, pt = traffic("traffic_time_chennai", 8, time_slot, SLOTS)
    m, pm = traffic("traffic_month_chennai", 12, month_slot, MONTHS)
    # the time-of-day and month tables are two cuts of the same accidents: their totals must agree
    for df in (t, m):
        df.rename(columns={"category": "slot" if df is t else "month"}, inplace=True)
    tot_t = t[t.group == "Road"].groupby("year").printed_total.first()
    tot_m = m[m.group == "Road"].groupby("year").printed_total.first()
    agree = pd.concat([tot_t, tot_m], axis=1, keys=["time", "month"]).dropna()
    bad = agree[(agree.time - agree.month).abs() > 0.02 * agree.month].index
    t.loc[t.year.isin(bad) & (t.source != "text"), "check"] = "disagrees with month table"
    note(t, "chennai_traffic_by_time", pt)
    note(m, "chennai_traffic_by_month", pm)
    out["time"], out["month"] = t, m
    slot_rx = [(lab, rf"^{lab[:2]}\s*:?\s*00\s*hrs?\.?\s*to\s*{lab[3:]}") for lab in SLOTS] + [("Total", r"total")]
    month_rx = [(m, rf"^{m}") for m in MONTHS] + [("Total", r"total")]
    for topic, name, rx in (("traffic_time_deaths_tn", "tn_traffic_persons_by_time", slot_rx), ("traffic_month_deaths_tn", "tn_traffic_persons_by_month", month_rx)):
        d, p = traffic_persons(topic, rx)
        note(d, name, p)
        out[name] = d
    return out


# --------------------------------------------------------------------------- suicides, Tamil Nadu


SEXES = {"Male", "Female", "Transgender"}


def with_age(d: pd.DataFrame) -> pd.DataFrame:
    """age_band column for tables that also split by age (2021 onwards); a sex's own total is 'all ages'."""
    d = d.copy()
    d["age_band"] = d.age.map(lambda a: "all ages" if a in ("", "Total") else age_band(a))
    return d


def check_vs_grand_total(d: pd.DataFrame) -> pd.DataFrame:
    """Old editions print no 'both sexes' column; check instead that every means, both sexes, adds up to the grand-total row."""
    d = d.copy()
    for y, g in d[d.check == "no total"].groupby("year"):
        grand = g[g.category.str.match(r"^\W*grand|^\W*total\W*$", case=False)]
        parts = g[g.means.notna() & g.sex.isin(SEXES)]
        if grand.empty or parts.empty:
            continue
        gt = grand.value.max()
        if gt and abs(parts.value.sum() - gt) <= max(2, 0.01 * gt):
            d.loc[g.index, "check"] = "ok (vs grand total)"
    return d


def whole_year_check(d: pd.DataFrame, cat: str, tn_total: pd.Series) -> pd.DataFrame:
    """Scanned years: per-category checks can pass by chance on a misread table, so the categories
    together (both sexes) must also match Tamil Nadu's total for the year, from the grand-total row or the rates table."""
    d = d.copy()
    for y, g in d[d.source != "text"].groupby("year"):
        parts = g[g[cat].notna() & g.sex.isin(SEXES)].value.sum()
        grand = g[g.category.str.match(r"^\W*grand|^\W*total\W*$", case=False)].value.max()
        target = [x for x in (grand, tn_total.get(y)) if x == x and x]
        if not any(abs(parts - t) <= 0.02 * t for t in target):
            d.loc[g.index, "check"] = d.loc[g.index, "check"].map(lambda c: c if not str(c).startswith("ok") else "categories do not add up to the year's total")
    return d


def means(tn_total: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame]:
    d, p = category_series("suicide_means_tn")
    d["means"] = d.category.map(lambda c: standard(c, MEANS))
    d = whole_year_check(check_vs_grand_total(d), "means", tn_total)
    d = d[d.means.notna()].rename(columns={"category": "means_as_printed"}).drop(columns="age")
    note(d, "tn_suicides_by_means", p)
    a, pa = category_series("suicide_means_age_tn")
    if not a.empty:
        a["means"] = a.category.map(lambda c: standard(c, MEANS))
        a = with_age(a[a.means.notna()]).rename(columns={"category": "means_as_printed"})
        note(a, "tn_suicides_by_means_age", pa)
    return d, a


def professions() -> tuple[pd.DataFrame, pd.DataFrame]:
    d, p = category_series("suicide_profession_tn")
    d["profession"] = d.category.map(lambda c: standard(c, PROFESSION))
    d = d[d.profession.notna()].rename(columns={"category": "profession_as_printed"}).drop(columns="age")
    note(d, "tn_suicides_by_profession", p)
    a, pa = category_series("suicide_profession_age_tn")
    if not a.empty:
        a["profession"] = a.category.map(lambda c: standard(c, PROFESSION))
        a = with_age(a[a.profession.notna()]).rename(columns={"category": "profession_as_printed"})
        note(a, "tn_suicides_by_profession_age", pa)
    return d, a


def tidy_sex_age(d: pd.DataFrame) -> pd.DataFrame:
    """One row per year, age group and sex, whichever way round the edition printed them."""
    rows = []
    for r in d.itertuples():
        if r.category in SEXES:
            sex, age = r.category, r.age or "Total"
        elif re.match(r"grand", r.category, re.I):
            sex, age = "Total", "Total"
        else:
            sex, age = r.sex, r.category
        if not sex:
            continue
        rows.append({"year": r.year, "age_as_printed": age, "age_band": age_band(age), "sex": sex, "value": r.value, "check": r.check, "source": r.source})
    t = pd.DataFrame(rows).drop_duplicates(["year", "age_band", "sex"])
    # a year whose headings could not be read as age groups (garbled scans) is left out
    t = t[t.age_band.isin(AGE_ORDER)]
    t = t[t.groupby("year").age_band.transform("nunique") >= 4]
    return add_both_sexes(t)


def add_both_sexes(t: pd.DataFrame) -> pd.DataFrame:
    """Where an edition prints no 'both sexes' figure for an age group (2014-15 workbooks, 2021+ tables), add the sexes up."""
    add = []
    for (y, band), g in t.groupby(["year", "age_band"]):
        if "Total" not in set(g.sex):
            add.append({"year": y, "age_as_printed": g.age_as_printed.iloc[0], "age_band": band, "sex": "Total",
                        "value": g[g.sex.isin(SEXES)].value.sum(), "check": "derived (sum of sexes)", "source": g.source.iloc[0]})
    return pd.concat([t, pd.DataFrame(add)], ignore_index=True).sort_values(["year", "age_band", "sex"])


def sex_age() -> dict[str, pd.DataFrame]:
    out = {}
    for topic, name in (("suicide_sex_age_tn", "tn_suicides_by_sex_age"), ("suicide_sex_age_chennai", "chennai_suicides_by_sex_age")):
        d, p = category_series(topic)
        if d.empty:
            continue
        d = tidy_sex_age(d)
        if topic == "suicide_sex_age_tn":
            # 2016-2020 printed no state-wise age table; from 2021 the means x age table's total row is one
            a, pa = category_series("suicide_means_age_tn")
            a = a[a.category.str.match(r"^\W*(grand\s+)?total\W*$", case=False) & a.sex.isin(SEXES | {"Total"})]
            a = a.assign(age_as_printed=a.age.replace("", "Total"))
            a["age_band"] = a.age_as_printed.map(age_band)
            d = pd.concat([d, a[["year", "age_as_printed", "age_band", "sex", "value", "check", "source"]]], ignore_index=True)
            # those tables print both sexes only for all ages: rebuild every 2021+ 'Total' from the sexes, consistently
            d = add_both_sexes(d[~((d.sex == "Total") & d.year.isin(a.year.unique()))])
            p = pd.concat([p, pa])
        note(d, name, p)
        out[name] = d
    return out


def cities_sex_age(rates_df: pd.DataFrame) -> pd.DataFrame:
    """Every city's suicides by sex and age group, in the years NCRB printed them (2004-2015, and 1989-90 scans)."""
    import difflib

    from .lib import rows_for
    from .series import categories, tables_for

    cities = sorted(set(rates_df.loc[rates_df.entity_type == "city", "name_std"]))
    picked = tables_for("suicide_sex_age_chennai")
    out = []
    for t in picked.itertuples():
        ids = [t.table_id]
        m = re.match(r"(.+_t)\d+$", t.table_id)
        if t.method == "excel" and m:  # 2014-15: one sheet per sex
            ids = q("SELECT table_id FROM tables WHERE table_id LIKE ?", [m.group(1) + "%"]).table_id.tolist()
        cells = rows_for(ids, r".")
        cells = cells[cells.section.fillna("").str.contains("cit", case=False) | (t.method == "excel")]
        cells["source"] = "ocr" if t.method in SCANNED else "text"
        for name, g in cells.groupby("name"):
            clean = re.sub(r"\s*\(.*?\)|[*#@]", "", name).strip().title()
            clean = CITY_NAMES.get(clean, clean)
            hit = difflib.get_close_matches(clean, cities, n=1, cutoff=0.85)
            if not hit:
                continue
            parts = []
            for tid, gg in g.groupby("table_id"):
                gg = gg[gg["row"] == gg["row"].min()]
                parts.append(gg)
            d = categories(pd.concat(parts, ignore_index=True))
            if d.empty:
                continue
            d["year"], d["source"] = int(t.year), cells.source.iloc[0]
            d = tidy_sex_age(d)
            out.append(d.assign(city=hit[0]))
    d = pd.concat(out, ignore_index=True).drop_duplicates(["year", "city", "age_band", "sex"])
    d = d[["year", "city", "age_band", "age_as_printed", "sex", "value", "check", "source"]]
    note(d, "cities_suicides_by_sex_age", picked)
    return d


# --------------------------------------------------------------------------- rates


def rates() -> pd.DataFrame:
    d, p = suicide_rates()
    note(d, "suicide_rates", p)
    return d


# --------------------------------------------------------------------------- everything about Chennai


def chennai_all() -> pd.DataFrame:
    """Every figure printed against Chennai (Madras before 1996) in any table of the three reports."""
    d = q(
        'SELECT c.table_id, c.publication, c.year, t.title, t.listing, t.method, c.section, c.name, c."column", c.value, c.raw '
        "FROM cells c JOIN tables t USING (table_id) WHERE regexp_matches(lower(c.name), '^\\s*(chennai|madras)')"
    )
    d = d[d.name.str.lower().str.contains(PLACES["chennai"], regex=True)].sort_values(["year", "publication", "table_id"])
    path = OUT / "chennai_all_figures.csv.gz"  # ~100k rows: compressed
    d.to_csv(path, index=False, compression="gzip")
    print(f"  {path.relative_to(OUT.parent.parent)}: {len(d):,} rows")
    return d


def chennai_summary(tr: dict, sa: dict, r: pd.DataFrame) -> pd.DataFrame:
    """The headline Chennai figures side by side, one row per year, from every table that has them."""
    t, m = good_rows(tr["time"]), good_rows(tr["month"])
    cols = {
        "road_accidents_time_table": t[t.group == "Road"].groupby("year").printed_total.first(),
        "road_accidents_month_table": m[m.group == "Road"].groupby("year").printed_total.first(),
        "traffic_accidents_all": t[t.group == "Total traffic"].groupby("year").printed_total.first(),
    }
    for name, place in (("chennai", "Chennai"), ("tamil_nadu", "Tamil Nadu"), ("india", "All India")):
        x = r[(r.name_std == place) & (r.rate_check == "ok")].set_index("year")  # scanned rows only when their figures agree
        cols[f"suicides_{name}"] = x.suicides
        cols[f"suicide_rate_{name}"] = x.rate
        if name == "chennai":
            cols["population_lakh_chennai"] = x.population_lakh
    c = sa.get("chennai_suicides_by_sex_age")
    if c is not None:
        c = c[c.age_band == "all ages"].pivot_table(index="year", columns="sex", values="value", aggfunc="first")
        for sex in ("Male", "Female"):
            if sex in c:
                cols[f"suicides_chennai_{sex.lower()}"] = c[sex]
    d = pd.DataFrame(cols).sort_index()
    d.index.name = "year"
    d = d.reset_index()
    note(d, "chennai_summary")
    return d


def good_rows(d: pd.DataFrame) -> pd.DataFrame:
    return d[d["check"] == "ok"]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("building series")
    res = {"traffic": traffic_series()}
    res["rates"] = rates()
    r = res["rates"]
    tn_total = r[(r.name_std == "Tamil Nadu") & (r.rate_check == "ok")].set_index("year").suicides
    res["means"], res["means_age"] = means(tn_total)
    res["profession"], res["profession_age"] = professions()
    res["sex_age"] = sex_age()
    res["cities_sex_age"] = cities_sex_age(res["rates"])
    res["chennai_summary"] = chennai_summary(res["traffic"], res["sex_age"], res["rates"])
    chennai_all()
    from .report import build

    print("drawing charts")
    build(res)


if __name__ == "__main__":
    main()
