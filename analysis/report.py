"""Assemble analysis/output/report.html (and charts/*.html) from the series built by run.py.

The short readings under each chart are computed from the data, so they stay
true when the series are rebuilt with more years.
"""

from __future__ import annotations

import html

import pandas as pd

from . import charts as C
from .lib import OUT
from .series import SLOTS

METROS = ["Chennai", "Delhi", "Mumbai", "Kolkata", "Bengaluru", "Hyderabad", "Ahmedabad", "Pune"]


def pct(a, b) -> str:
    return f"{100 * a / b:.0f}%" if b else "–"


def span(years) -> str:
    years = sorted(set(int(y) for y in years))
    if not years:
        return "none"
    runs, start, prev = [], years[0], years[0]
    for y in years[1:] + [None]:
        if y is not None and y == prev + 1:
            prev = y
            continue
        runs.append(f"{start}" if start == prev else f"{start}–{prev}")
        if y is not None:
            start = prev = y
    return ", ".join(runs)


def run_start(years) -> int:
    """First year of the unbroken run of years that ends with the latest one."""
    ys = sorted(set(int(y) for y in years))
    i = len(ys) - 1
    while i > 0 and ys[i - 1] == ys[i] - 1:
        i -= 1
    return ys[i]


def p(text: str) -> str:
    return f"<p>{text}</p>"


def table(df: pd.DataFrame) -> str:
    head = "".join(f"<th>{html.escape(str(c))}</th>" for c in df.columns)
    def cell(c, v):
        if pd.isna(v):
            return ""
        if c == "year":
            return str(int(v))
        if isinstance(v, float) and v % 1:
            return f"{v:,.1f}"
        return f"{v:,.0f}" if isinstance(v, (int, float)) else html.escape(str(v))

    rows = "".join("<tr>" + "".join(f"<td>{cell(c, v)}</td>" for c, v in zip(df.columns, r)) + "</tr>" for r in df.itertuples(index=False))
    return f'<div style="overflow-x:auto"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'


def build(res: dict) -> None:
    tr, sections = res["traffic"], []

    # ------------------------------------------------------------------ traffic, Chennai
    t = C.good(tr["time"])
    road = t[t.group == "Road"]
    tot = road.groupby("year").value.sum()
    first_text = int(road[road.source == "text"].year.min())
    last = int(road.year.max())
    peak = road.loc[road.groupby("year").value.idxmax()].set_index("year").slot
    sh = road.pivot_table(index="year", columns="slot", values="value").reindex(columns=SLOTS)
    sh = sh.div(sh.sum(axis=1), axis=0) * 100
    night = sh[["18-21", "21-24", "00-03", "03-06"]].sum(axis=1)
    f_polar = C.polar_time(t, "Road", title="Road accidents in Chennai by time of day",
                           subtitle=f"{span(road.year.unique())} · one line per year, yellow-green = older, violet = recent · dashed = read from scanned pages",
                           what="accidents")
    f_tot = C.line_totals({"Road accidents": tot}, "Road accidents in Chennai per year", f"sum of the time-of-day table, {span(tot.index)}",
                          "accidents", dashed_before=first_text)
    sections.append(("Chennai road accidents by time of day", "".join([
        p(f"NCRB's city tables count <b>accidents</b>, not deaths, by time of day; Chennai (Madras until 1996) is printed every year from "
          f"{int(road.year.min())}. Missing: {span(set(range(int(road.year.min()), last + 1)) - set(road.year))} (no readable table yet, or "
          "figures that do not add up to the printed total)."),
        p(f"The busiest three hours were {peak.mode().iloc[0]} h in {(peak == peak.mode().iloc[0]).sum()} of {len(peak)} years "
          f"(in {last}: {peak.loc[last]} h). The evening and night (18–06 h) held {night.loc[first_text]:.0f}% of road accidents in {first_text} "
          f"and {night.loc[last]:.0f}% in {last}. Use the buttons to switch between counts and each year's share of the day, and the "
          f"menu to pick out one year."),
        p(f"Road accidents peaked at {tot.max():,.0f} in {int(tot.idxmax())} and were {tot.loc[last]:,.0f} in {last}. "
          "2018 and 2020 put an unusually large count in 00–03 h; that is how NCRB printed them (the same figures appear in the "
          "state/city table and the full report)."),
    ]), [f_polar, f_tot]))
    C.save_fig(f_polar, "chennai_traffic_polar_time")
    C.save_fig(f_tot, "chennai_traffic_per_year")

    # ------------------------------------------------------------------ traffic, Chennai, month
    m = C.good(tr["month"])
    mr = m[m.group == "Road"]
    piv = mr.pivot_table(index="year", columns="month", values="value")
    msh = piv.div(piv.sum(axis=1), axis=0) * 100
    f_month = C.heat_month(m, "Road", "Road accidents in Chennai by month", f"{span(mr.year.unique())} · colour = month's share of the year")
    sections.append(("Chennai road accidents by month", "".join([
        p(f"Month tables for Chennai cover {span(mr.year.unique())}. Over these years the month with the largest average share was "
          f"{msh.mean().idxmax()} ({msh.mean().max():.1f}%) and the smallest {msh.mean().idxmin()} ({msh.mean().min():.1f}%); "
          f"an even spread would be 8.3% a month." + (f" April 2020 (lockdown) held {msh.loc[2020, 'Apr']:.1f}% of that year." if 2020 in msh.index else "")),
    ]), [f_month]))
    C.save_fig(f_month, "chennai_traffic_month_heatmap")

    # ------------------------------------------------------------------ traffic, Tamil Nadu persons died
    tp = tr["tn_traffic_persons_by_time"]
    died = tp[(tp.measure == "Died") & (tp.category != "Total")].rename(columns={"category": "slot"})
    died = died.assign(source="text", check="ok")
    f_tn_polar = C.polar_time(died, "Road", title="Persons killed in road accidents in Tamil Nadu by time of day",
                              subtitle=f"{span(died.year.unique())} · state-wise tables, the only ones that count deaths by time", what="deaths")
    tm = tr["tn_traffic_persons_by_month"]
    dm = tm[(tm.measure == "Died") & (tm.category != "Total") & (tm.group == "Road")].rename(columns={"category": "month"}).assign(check="ok")
    f_tn_month = C.heat_month(dm.assign(group="Road"), "Road", "Persons killed in road accidents in Tamil Nadu by month", span(dm.year.unique()))
    f_tn_month.update_traces(hovertemplate="<b>%{x} %{y}</b><br>%{customdata:,.0f} deaths<br>%{z:.1f}% of the year<extra></extra>")
    f_tn_month.layout.updatemenus[0].buttons[1].label = "Number of deaths"
    f_tn_month.layout.updatemenus[0].buttons[1].args[0]["colorbar.title.text"] = "deaths"
    dt = died[died.group == "Road"].pivot_table(index="year", columns="slot", values="value").reindex(columns=SLOTS)
    sections.append(("Road deaths by time of day (Tamil Nadu)", "".join([
        p("Deaths by time of day and month are printed only state-wise, and only from 2021; for Chennai NCRB publishes the number of "
          "accidents and, separately, yearly totals of persons killed. "
          f"In Tamil Nadu {dt.loc[dt.index.max(), '18-21'] / dt.loc[dt.index.max()].sum() * 100:.0f}% of road deaths in {dt.index.max()} happened between 18 and 21 h."),
    ]), [f_tn_polar, f_tn_month]))
    C.save_fig(f_tn_polar, "tn_road_deaths_polar_time")
    C.save_fig(f_tn_month, "tn_road_deaths_month_heatmap")

    # ------------------------------------------------------------------ suicides by means
    mn = C.good(res["means"])
    mt = mn[mn.sex == "Total"].pivot_table(index="year", columns="means", values="value", aggfunc="sum")
    msh = mt.div(mt.sum(axis=1), axis=0) * 100
    y0, y1 = run_start(mt.index), int(mt.index.max())
    f_means = C.share_area(mn, "means", "Suicides in Tamil Nadu by means adopted", f"{y0}–{y1} · share of all suicides, both sexes")
    f_means_l = C.small_lines(mn[mn.year >= y0], "means", "Suicides in Tamil Nadu by means adopted, number", f"{y0}–{y1} · buttons: sex")
    figs = [f_means, f_means_l]
    if res.get("means_age") is not None and not res["means_age"].empty:
        figs.append(C.heat_cat_age(res["means_age"], "means", "Means adopted by age group, Tamil Nadu", "both sexes · 2021 onwards (state-wise age tables)"))
    sections.append(("Suicides in Tamil Nadu by means", "".join([
        p(f"Hanging was {msh.loc[y0, 'Hanging']:.0f}% of suicides in {y0} and {msh.loc[y1, 'Hanging']:.0f}% in {y1}; "
          f"poisoning (insecticides and other poison together) went from {msh.loc[y0, [c for c in msh if c.startswith('Poison')]].sum():.0f}% "
          f"to {msh.loc[y1, [c for c in msh if c.startswith('Poison')]].sum():.0f}%. NCRB's wording of the means changes between editions; "
          "they are mapped to one list (analysis/harmonise.py) and the printed label is kept in the CSV. "
          + (f"Earlier years read from scans ({span(y for y in mt.index if y < y0)}) are in the CSV but not drawn: the scanned means tables are "
             "being re-read with the AI model." if mt.index.min() < y0 else "")),
    ]), figs))
    C.save_fig(f_means, "tn_suicides_means_share")
    C.save_fig(figs[-1] if len(figs) > 2 else None, "tn_suicides_means_age")

    # ------------------------------------------------------------------ suicides by profession
    pr = C.good(res["profession"])
    pt = pr[pr.sex == "Total"].pivot_table(index="year", columns="profession", values="value", aggfunc="sum")
    psh = pt.div(pt.sum(axis=1), axis=0) * 100
    y0, y1 = int(pt.index.min()), int(pt.index.max())
    f_prof = C.share_area(pr, "profession", "Suicides in Tamil Nadu by profession", f"{span(pt.index)} · share of all suicides, both sexes",
                          breaks={2014: "2014: new categories (daily wage earner, agricultural labourer)"})
    f_prof_l = C.small_lines(pr, "profession", "Suicides in Tamil Nadu by profession, number", f"{span(pt.index)} · buttons: sex")
    figs = [f_prof, f_prof_l]
    if res.get("profession_age") is not None and not res["profession_age"].empty:
        figs.append(C.heat_cat_age(res["profession_age"], "profession", "Profession by age group, Tamil Nadu", "both sexes · 2021 onwards (state-wise age tables)"))
    dw = psh.get("Daily wage earner")
    sections.append(("Suicides in Tamil Nadu by profession", "".join([
        p(f"Profession tables run {span(pt.index)}. In 2014 NCRB split 'others' into new groups, so shares before and after 2014 are not "
          f"comparable for the 'other' professions. " + (f"Daily wage earners, counted from 2014, were {dw.loc[2014]:.0f}% of suicides in 2014 and {dw.loc[y1]:.0f}% in {y1}. " if dw is not None and 2014 in dw.index else "")
          + " ".join(f"{label} were {psh[c].dropna().iloc[0]:.1f}% in {int(psh[c].dropna().index[0])} and {psh.loc[y1, c]:.1f}% in {y1}."
                     for c, label in (("House wife", "House wives"), ("Student", "Students"), ("Unemployed", "Unemployed people")) if c in psh)),
        p("Profession by sex <i>and</i> age is printed state-wise only from 2021 (the third chart)."),
    ]), figs))
    C.save_fig(f_prof, "tn_suicides_profession_share")
    C.save_fig(figs[-1] if len(figs) > 2 else None, "tn_suicides_profession_age")

    # ------------------------------------------------------------------ sex and age
    sa = res["sex_age"]
    figs, text = [], []
    for key, place in (("tn_suicides_by_sex_age", "Tamil Nadu"), ("chennai_suicides_by_sex_age", "Chennai")):
        d = sa.get(key)
        if d is None:
            continue
        d = C.good(d)
        figs.append(C.age_lines(d, f"Suicides in {place} by age group", f"{span(d.year.unique())} · buttons: sex · under-30 groups were re-cut in 2014, shown together"))
        a = d[d.age_band == "all ages"].pivot_table(index="year", columns="sex", values="value", aggfunc="first")
        if {"Male", "Total"} <= set(a.columns):
            ms = (a.Male / a.Total * 100).dropna()
            text.append(f"{place}: men were {ms.iloc[0]:.0f}% of suicides in {int(ms.index[0])} and {ms.iloc[-1]:.0f}% in {int(ms.index[-1])}.")
    tn_years = sa["tn_suicides_by_sex_age"].year.unique() if "tn_suicides_by_sex_age" in sa else []
    ch_years = sa["chennai_suicides_by_sex_age"].year.unique() if "chennai_suicides_by_sex_age" in sa else []
    sections.append(("Suicides by sex and age group", "".join([
        p(f"Sex and age by state is printed for {span(tn_years)} (from 2021 taken from the means-by-age table's total row); for cities, "
          f"including Chennai, for {span(ch_years)}. Between 2016 and 2020 NCRB printed age and sex only for all India. " + " ".join(text)),
    ]), figs))
    for f, n in zip(figs, ["tn_suicides_age", "chennai_suicides_age"]):
        C.save_fig(f, n)

    # ------------------------------------------------------------------ rates
    r = res["rates"]
    ok = r[(r.rate_check == "ok") & r.rate.notna()]
    lines = {n: ok[ok.name_std == n].set_index("year").rate for n in ["Chennai", "Tamil Nadu", "All India", "Total (Cities)"]}
    f_rate = C.line_totals(lines, "Suicide rate: Chennai, Tamil Nadu, India and all cities", "suicides per lakh people, as printed · years whose figures agree",
                           "per lakh", dashed_before=2004, fmt=".1f")
    f_states = C.rate_heat(r, ["state", "ut"], "Suicide rate by State and UT", "per lakh people · sorted by the latest year · Tamil Nadu in bold")
    f_cities = C.rate_heat(r, ["city"], "Suicide rate by city", "per lakh people · sorted by the latest year · Chennai in bold", highlight="Chennai")
    met = {n: ok[(ok.name_std == n) & (ok.entity_type == "city")].set_index("year").rate for n in METROS}
    f_metro = C.line_totals(met, "Suicide rate in the metros", "per lakh people", "per lakh", dashed_before=2004, fmt=".1f")
    st = ok[ok.entity_type.isin(["state", "ut"])]
    latest = int(st.year.max())
    rank = st[st.year == latest].sort_values("rate", ascending=False).reset_index(drop=True)
    tn_rank = int(rank.index[rank.name_std == "Tamil Nadu"][0]) + 1 if (rank.name_std == "Tamil Nadu").any() else None
    ch = lines["Chennai"]
    pop = r[(r.name_std == "Chennai") & (r.entity_type == "city")].set_index("year").population_lakh
    sections.append(("Suicide rates: States, UTs and cities", "".join([
        p(f"Rates are printed for {span(ok.year.unique())} (1993–2003 are not in the downloadable tables; the scanned years before 1993 are "
          f"kept only where suicides ÷ population matches the printed rate). In {latest} Tamil Nadu's rate was {lines['Tamil Nadu'].get(latest, float('nan')):.1f} "
          f"against {lines['All India'].get(latest, float('nan')):.1f} for India" + (f", {tn_rank}{'st' if tn_rank == 1 else 'nd' if tn_rank == 2 else 'rd' if tn_rank == 3 else 'th'} of {len(rank)} States/UTs" if tn_rank else "") + "."),
        p(f"Chennai's rate was {ch.get(2021, float('nan')):.1f} in 2021 and {ch.get(latest, float('nan')):.1f} in {latest}. City rates use a fixed census "
          f"population (Chennai {pop.get(2010, float('nan')):.1f} lakh to 2010, {pop.get(latest, float('nan')):.1f} lakh from 2011), so a change in the rate is a change in the "
          f"count of suicides; Chennai's count fell from {r[(r.name_std == 'Chennai') & (r.year == 2021)].suicides.max():,.0f} in 2021 to "
          f"{r[(r.name_std == 'Chennai') & (r.year == 2022)].suicides.max():,.0f} in 2022."),
    ]), [f_rate, f_metro, f_states, f_cities]))
    for f, n in zip([f_rate, f_metro, f_states, f_cities], ["suicide_rate_lines", "suicide_rate_metros", "suicide_rate_states", "suicide_rate_cities"]):
        C.save_fig(f, n)

    # ------------------------------------------------------------------ major cities, sex and age
    cs = res["cities_sex_age"]
    f_city = C.city_age_bars(cs, METROS, "Age profile of suicides in the metros", "both sexes · choose the year · city age tables exist for 2004–2015")
    fem = C.good(cs[(cs.age_band == "all ages")]).pivot_table(index=["city", "year"], columns="sex", values="value", aggfunc="first")
    fem = (fem.Female / fem.Total * 100).unstack(0) if {"Female", "Total"} <= set(fem.columns) else pd.DataFrame()
    f_fem = C.line_totals({c: fem[c] for c in METROS if c in fem}, "Women's share of suicides in the metros", "% of each city's suicides", "%", fmt=".0f")
    sections.append(("Major cities by sex and age group", "".join([
        p("NCRB printed suicides by sex and age for each of the 35 (from 2011, 53) big cities in 2004–2015, and in the scanned 1989–1990 reports; "
          "it has not printed them since. The request for a 2019 distribution in major cities by sex and age with ICD-10 codes S00–T98 "
          "matches the Registrar General's <i>Medical Certification of Cause of Death</i> report, not NCRB, so it is not in this dataset."),
    ]), [f_city, f_fem]))
    C.save_fig(f_city, "metros_suicides_age")
    C.save_fig(f_fem, "metros_suicides_female_share")

    # ------------------------------------------------------------------ Chennai at a glance
    s = res["chennai_summary"]
    show = s[["year", "road_accidents_time_table", "road_accidents_month_table", "suicides_chennai", "suicide_rate_chennai",
              "suicides_tamil_nadu", "suicide_rate_tamil_nadu", "suicide_rate_india"]].copy()
    show = show.dropna(how="all", subset=show.columns[1:])
    show.columns = ["year", "road accidents (time table)", "road accidents (month table)", "Chennai suicides", "Chennai rate", "TN suicides", "TN rate", "India rate"]
    sections.insert(0, ("Chennai at a glance", p("The headline figures from every table, side by side (analysis/output/chennai_summary.csv). "
                                                 "The two traffic columns come from different tables and agree wherever both were printed.") + table(show), []))

    intro = p("<b>What changed over time in NCRB's figures on traffic accidents and suicides, for Chennai, Tamil Nadu and India.</b> "
              "Each series follows one table across every year it was printed, oldest first; scanned years (before about 2000) were read with "
              "OCR and an AI document model, and a year is shown only when its figures add up to the total printed with them.") + \
        f'<p class="note">Built by analysis/run.py from the NCRB tables in this repository. Data: NCRB, Accidental Deaths &amp; Suicides in India (ADSI).</p>'
    C.page(sections, OUT / "report.html", "Chennai: traffic accidents and suicides over time", intro)
    print(f"  {OUT / 'report.html'}")
