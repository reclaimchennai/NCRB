"""Interactive charts (plotly) for the series built by run.py, and one report page.

Every chart is saved on its own (analysis/output/charts/*.html) and all of them
together, with a short reading of each, in analysis/output/report.html.
Years read from scanned pages are drawn dashed; years whose figures do not add
up to their own printed total are left out of the charts (they stay in the CSVs
with check = 'mismatch').
"""

from __future__ import annotations

import html

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from .harmonise import AGE_ORDER, YOUNG
from .lib import OUT
from .series import MONTHS, SLOTS

# reference data-viz palette (validated): categorical order, one-hue sequential ramp, chart ink
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
SEQ = ["#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
INK, INK2, MUTED, GRID, BASE, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
HEAT = ["#f0efec", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'
CHARTS = OUT / "charts"


def years_palette(n: int) -> list[str]:
    """Distinct colours for many years, in order (viridis without its faintest yellow): old = yellow-green, recent = deep violet."""
    from plotly.colors import sample_colorscale

    return sample_colorscale("Viridis", [0.88 - 0.88 * i / max(1, n - 1) for i in range(n)])


def ramp(n: int) -> list[str]:
    """n colours along the sequential ramp, oldest lightest."""
    if n == 1:
        return [SEQ[-1]]
    idx = np.linspace(0, len(SEQ) - 1, n)
    out = []
    for x in idx:
        a, b = int(np.floor(x)), int(np.ceil(x))
        t = x - a
        ca, cb = (np.array([int(SEQ[i][k:k + 2], 16) for k in (1, 3, 5)]) for i in (a, b))
        out.append("#%02x%02x%02x" % tuple(int(round(v)) for v in ca + (cb - ca) * t))
    return out


def style(fig: go.Figure, title: str, subtitle: str = "", height: int = 520) -> go.Figure:
    fig.update_layout(
        title=dict(text=f"<b>{html.escape(title)}</b>" + (f"<br><span style='font-size:13px;color:{INK2}'>{html.escape(subtitle)}</span>" if subtitle else ""),
                   x=0, xanchor="left", font=dict(size=17, color=INK)),
        font=dict(family=FONT, size=13, color=INK2),
        paper_bgcolor=SURFACE, plot_bgcolor=SURFACE, height=height,
        margin=dict(l=60, r=30, t=max(130 if fig.layout.updatemenus else 90, fig.layout.margin.t or 0), b=60),
        hoverlabel=dict(bgcolor="white", font=dict(family=FONT, color=INK), bordercolor=BASE),
        legend=dict(font=dict(size=12, color=INK2), bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=GRID, linecolor=BASE, zeroline=False, tickfont=dict(color=MUTED))
    fig.update_yaxes(gridcolor=GRID, linecolor=BASE, zeroline=False, tickfont=dict(color=MUTED))
    return fig


def good(d: pd.DataFrame) -> pd.DataFrame:
    return d[d["check"].isin(["ok", "derived (sum of sexes)"])]


# --------------------------------------------------------------------------- traffic


def polar_time(t: pd.DataFrame, group: str = "Road", value: str = "value", title: str = "", subtitle: str = "", what: str = "accidents") -> go.Figure:
    """One closed line per year around a 24-hour clock (midnight at the top), coloured light (old) to dark (new)."""
    t = t[t.group == group]
    years = sorted(t.year.unique())
    colors = years_palette(len(years))
    fig = go.Figure()
    numbers, shares, dash = [], [], []
    for y, col in zip(years, colors):
        g = t[t.year == y].set_index("slot").reindex(SLOTS)
        r = g[value].tolist()
        tot = np.nansum(r)
        sh = [round(100 * v / tot, 1) if tot else None for v in r]
        scanned = g.source.iloc[0] in ("ocr", "ai_ocr")
        numbers.append(r + r[:1])
        shares.append(sh + sh[:1])
        dash.append("dash" if scanned else "solid")
        fig.add_trace(go.Scatterpolar(
            r=r + r[:1], theta=SLOTS + SLOTS[:1], mode="lines", name=f"{y}{' (scan)' if scanned else ''}",
            line=dict(color=col, width=2, dash=dash[-1]),
            customdata=[[v, s] for v, s in zip(r + r[:1], sh + sh[:1])],
            hovertemplate=f"<b>{y}</b> · %{{theta}} h<br>%{{customdata[0]:,.0f}} {what}<br>%{{customdata[1]}}% of the day<extra></extra>",
        ))
    n = len(years)
    highlight = [dict(label="All years", method="restyle", args=[{"line.color": colors, "line.width": [2] * n, "opacity": [1] * n}])]
    for i, y in enumerate(years):
        highlight.append(dict(label=str(y), method="restyle", args=[{
            "line.color": [colors[j] if j == i else GRID for j in range(n)],
            "line.width": [4 if j == i else 1.5 for j in range(n)], "opacity": [1] * n}]))
    fig.update_layout(
        polar=dict(
            bgcolor=SURFACE,
            angularaxis=dict(type="category", direction="clockwise", rotation=90 - 22.5, gridcolor=GRID, linecolor=BASE, tickfont=dict(color=INK2, size=13),
                             ticktext=[f"{s[:2]}–{s[3:]} h" for s in SLOTS], tickvals=SLOTS),
            radialaxis=dict(gridcolor=GRID, linecolor=BASE, tickfont=dict(color=MUTED, size=11), angle=90, tickangle=90),
        ),
        margin=dict(t=150),
        updatemenus=[
            dict(type="buttons", direction="right", x=0, y=1.04, xanchor="left", yanchor="bottom", showactive=True, bgcolor="white", bordercolor=BASE,
                 buttons=[dict(label=f"Number of {what}", method="restyle", args=[{"r": numbers}]),
                          dict(label="Share of the day (%)", method="restyle", args=[{"r": shares}])]),
            dict(type="dropdown", x=1, y=1.04, xanchor="right", yanchor="bottom", bgcolor="white", bordercolor=BASE, buttons=highlight),
        ],
        legend=dict(title=dict(text="Year"), traceorder="normal"),
    )
    return style(fig, title, subtitle, height=720)


def heat_month(m: pd.DataFrame, group: str = "Road", title: str = "", subtitle: str = "") -> go.Figure:
    m = m[m.group == group]
    piv = m.pivot_table(index="year", columns="month", values="value", aggfunc="first").reindex(columns=MONTHS)
    share = piv.div(piv.sum(axis=1), axis=0) * 100
    years = [str(y) for y in piv.index]
    fig = go.Figure(go.Heatmap(
        z=share.values, x=MONTHS, y=years, colorscale=[[i / (len(HEAT) - 1), c] for i, c in enumerate(HEAT)],
        customdata=piv.values, xgap=2, ygap=2, colorbar=dict(title="% of year", thickness=12, outlinewidth=0),
        hovertemplate="<b>%{x} %{y}</b><br>%{customdata:,.0f} accidents<br>%{z:.1f}% of the year<extra></extra>",
    ))
    fig.update_layout(updatemenus=[dict(type="buttons", direction="right", x=0, y=1.02, xanchor="left", yanchor="bottom", bgcolor="white", bordercolor=BASE, buttons=[
        dict(label="Share of the year (%)", method="restyle", args=[{"z": [share.values], "colorbar.title.text": "% of year"}]),
        dict(label="Number of accidents", method="restyle", args=[{"z": [piv.values], "colorbar.title.text": "accidents"}]),
    ])])
    fig.update_yaxes(autorange="reversed", type="category", gridcolor=SURFACE)
    fig.update_xaxes(gridcolor=SURFACE)
    return style(fig, title, subtitle, height=max(480, 22 * len(years) + 160))


def line_totals(series: dict[str, pd.Series], title: str, subtitle: str = "", ytitle: str = "", dashed_before: int | None = None, fmt: str = ",.0f") -> go.Figure:
    fig = go.Figure()
    for i, (name, s) in enumerate(series.items()):
        s = s.dropna().sort_index()
        if len(s):  # missing years break the line instead of being bridged
            s = s[~s.index.duplicated()].reindex(range(int(s.index.min()), int(s.index.max()) + 1))
        fig.add_trace(go.Scatter(x=s.index, y=s.values, name=name, mode="lines+markers", line=dict(color=CAT[i % 8], width=2), marker=dict(size=6), connectgaps=False,
                                 hovertemplate=f"<b>{html.escape(name)}</b> %{{x}}: %{{y:{fmt}}}<extra></extra>"))
    if dashed_before:
        fig.add_vrect(x0=min(s.index.min() for s in series.values() if len(s.dropna())) - 0.5, x1=dashed_before - 0.5, fillcolor="#f0efec", opacity=0.6, line_width=0,
                      annotation_text="read from scans", annotation_position="top left", annotation_font_color=MUTED)
    fig.update_yaxes(title=ytitle, rangemode="tozero")
    fig.update_xaxes(dtick=2)
    return style(fig, title, subtitle)


# --------------------------------------------------------------------------- shares over time


def share_area(d: pd.DataFrame, cat: str, title: str, subtitle: str = "", top: int = 7, breaks: dict[int, str] | None = None, sex: str = "Total") -> go.Figure:
    """100% stacked area of categories over the years; the smallest fold into 'All other'."""
    d = d[d.sex == sex]
    piv = d.pivot_table(index="year", columns=cat, values="value", aggfunc="sum").fillna(0)
    # an area chart would draw straight across a gap of years: keep the unbroken run up to the latest year
    yrs = list(piv.index)
    start = len(yrs) - 1
    while start > 0 and yrs[start - 1] == yrs[start] - 1:
        start -= 1
    piv = piv.loc[yrs[start]:]
    order = piv.sum().sort_values(ascending=False).index.tolist()
    keep = [c for c in order if c != "Other / not known"][:top]
    piv["All other"] = piv[[c for c in piv.columns if c not in keep]].sum(axis=1)
    piv = piv[keep + ["All other"]]
    share = piv.div(piv.sum(axis=1), axis=0) * 100
    fig = go.Figure()
    for i, c in enumerate(piv.columns):
        col = CAT[i] if c != "All other" else "#c3c2b7"
        fig.add_trace(go.Scatter(x=share.index, y=share[c], name=c, stackgroup="one", mode="lines", line=dict(width=0.5, color=SURFACE),
                                 fillcolor=col, customdata=piv[c], hovertemplate=f"<b>{html.escape(c)}</b> %{{x}}<br>%{{y:.1f}}% · %{{customdata:,.0f}} suicides<extra></extra>"))
    for y, label in (breaks or {}).items():
        fig.add_vline(x=y - 0.5, line=dict(color=INK2, width=1, dash="dot"))
        fig.add_annotation(x=y - 0.5, y=103, text=label, showarrow=False, font=dict(size=11, color=INK2), xanchor="left")
    fig.update_yaxes(title="% of suicides", range=[0, 106], ticksuffix="%")
    fig.update_xaxes(dtick=2, range=[piv.index.min(), piv.index.max()])
    fig.update_layout(hovermode="x unified", legend=dict(traceorder="reversed"))
    return style(fig, title, subtitle, height=560)


def small_lines(d: pd.DataFrame, cat: str, title: str, subtitle: str = "", cats: list[str] | None = None) -> go.Figure:
    """Count per category over the years, one line each, sexes as buttons."""
    cats = cats or d.groupby(cat).value.sum().sort_values(ascending=False).index.tolist()[:8]
    fig = go.Figure()
    sexes = [s for s in ["Total", "Male", "Female"] if s in set(d.sex)]
    for si, sex in enumerate(sexes):
        for i, c in enumerate(cats):
            s = d[(d.sex == sex) & (d[cat] == c)].groupby("year").value.sum()
            fig.add_trace(go.Scatter(x=s.index, y=s.values, name=c, legendgroup=c, showlegend=si == 0, visible=si == 0, mode="lines+markers",
                                     line=dict(color=CAT[i % 8], width=2), marker=dict(size=5),
                                     hovertemplate=f"<b>{html.escape(c)}</b> ({sex}) %{{x}}: %{{y:,.0f}}<extra></extra>"))
    n = len(cats)
    fig.update_layout(updatemenus=[dict(type="buttons", direction="right", x=0, y=1.02, xanchor="left", yanchor="bottom", bgcolor="white", bordercolor=BASE, buttons=[
        dict(label=sex if sex != "Total" else "Both sexes", method="update",
             args=[{"visible": [k // n == si for k in range(n * len(sexes))], "showlegend": [k // n == si for k in range(n * len(sexes))]}])
        for si, sex in enumerate(sexes)])])
    fig.update_yaxes(title="suicides", rangemode="tozero")
    fig.update_xaxes(dtick=2)
    return style(fig, title, subtitle)


def heat_cat_age(d: pd.DataFrame, cat: str, title: str, subtitle: str = "") -> go.Figure:
    """Category x age group, both sexes, one year at a time (2021 onwards tables)."""
    # these tables print each sex by age, and only a grand total for both: add the sexes up
    d = good(d[d.sex.isin(["Male", "Female", "Transgender"])])
    years = sorted(d.year.unique())
    bands = [b for b in AGE_ORDER if b in set(d.age_band) and b != "all ages"]
    zs, cats = [], None
    for y in years:
        piv = d[d.year == y].pivot_table(index=cat, columns="age_band", values="value", aggfunc="sum").reindex(columns=bands).fillna(0)
        if cats is None:
            cats = piv.sum(axis=1).sort_values().index.tolist()
        zs.append(piv.reindex(cats).values)
    if not zs:
        return None
    fig = go.Figure(go.Heatmap(z=zs[-1], x=bands, y=cats, colorscale=[[i / (len(HEAT) - 1), c] for i, c in enumerate(HEAT)], xgap=2, ygap=2,
                               colorbar=dict(title="suicides", thickness=12, outlinewidth=0), hovertemplate="<b>%{y}</b>, age %{x}<br>%{z:,.0f} suicides<extra></extra>",
                               texttemplate="%{z:,.0f}", textfont=dict(size=11)))
    fig.update_layout(updatemenus=[dict(type="buttons", direction="right", x=0, y=1.02, xanchor="left", yanchor="bottom", bgcolor="white", bordercolor=BASE, active=len(years) - 1,
                                        buttons=[dict(label=str(y), method="restyle", args=[{"z": [z]}]) for y, z in zip(years, zs)])])
    fig.update_xaxes(gridcolor=SURFACE, title="age group (years)")
    fig.update_yaxes(gridcolor=SURFACE)
    return style(fig, title, subtitle, height=max(420, 34 * len(cats) + 180))


# --------------------------------------------------------------------------- age and sex


def age_lines(d: pd.DataFrame, title: str, subtitle: str = "") -> go.Figure:
    """Suicides by age group over the years. The under-30 groups were re-cut in 2014, so they are drawn together."""
    d = good(d)
    fig = go.Figure()
    sexes = [s for s in ["Total", "Male", "Female"] if s in set(d.sex)]
    bands = ["under 30", "30-44", "45-59", "60+"]
    for si, sex in enumerate(sexes):
        x = d[d.sex == sex].copy()
        x["band"] = x.age_band.map(lambda b: "under 30" if b in YOUNG and b != "0-17" else b)
        x = x[x.band.isin(bands)]
        # a year counts only with all its young groups present (0-17 alone, as in 2022+ profession tables, is not under 30)
        piv = x.pivot_table(index="year", columns="band", values="value", aggfunc="sum")
        piv = piv.reindex(range(int(piv.index.min()), int(piv.index.max()) + 1))  # gaps in the years break the lines
        for i, b in enumerate(bands):
            if b not in piv:
                continue
            s = piv[b]
            fig.add_trace(go.Scatter(x=s.index, y=s.values, name=b, legendgroup=b, showlegend=si == 0, visible=si == 0, mode="lines+markers",
                                     line=dict(color=CAT[i], width=2), marker=dict(size=6), connectgaps=False,
                                     hovertemplate=f"<b>age {b}</b> ({sex}) %{{x}}: %{{y:,.0f}}<extra></extra>"))
    n = len(bands)
    fig.update_layout(updatemenus=[dict(type="buttons", direction="right", x=0, y=1.02, xanchor="left", yanchor="bottom", bgcolor="white", bordercolor=BASE, buttons=[
        dict(label=sex if sex != "Total" else "Both sexes", method="update",
             args=[{"visible": [tr.legendgroup is not None and k // n == si for k, tr in enumerate(fig.data)]}]) for si, sex in enumerate(sexes)])])
    fig.update_yaxes(title="suicides", rangemode="tozero")
    fig.update_xaxes(dtick=2)
    return style(fig, title, subtitle)


def city_age_bars(cs: pd.DataFrame, cities: list[str], title: str, subtitle: str = "") -> go.Figure:
    """Age profile of suicides in the big cities, one year at a time, both sexes."""
    cs = good(cs[(cs.sex == "Total") & cs.city.isin(cities)])
    years = sorted(cs.year.unique())
    fig = go.Figure()
    traces_per_year = []
    for yi, y in enumerate(years):
        x = cs[(cs.year == y) & (cs.age_band != "all ages")]
        bands = [b for b in AGE_ORDER if b in set(x.age_band)]
        piv = x.pivot_table(index="city", columns="age_band", values="value", aggfunc="sum").reindex(cities).reindex(columns=bands)
        share = piv.div(piv.sum(axis=1), axis=0) * 100
        k = 0
        for i, b in enumerate(bands):
            fig.add_trace(go.Bar(y=share.index, x=share[b], name=b, orientation="h", marker=dict(color=CAT[i], line=dict(color=SURFACE, width=2)),
                                 visible=yi == len(years) - 1, customdata=piv[b], legendgroup=f"{y}",
                                 hovertemplate=f"<b>%{{y}}</b> {y}, age {b}: %{{x:.1f}}% · %{{customdata:,.0f}}<extra></extra>"))
            k += 1
        traces_per_year.append(k)
    vis = []
    for yi in range(len(years)):
        vis.append([j == yi for j, k in enumerate(traces_per_year) for _ in range(k)])
    fig.update_layout(barmode="stack", updatemenus=[dict(type="dropdown", x=0, y=1.02, xanchor="left", yanchor="bottom", bgcolor="white", bordercolor=BASE, active=len(years) - 1,
                                                         buttons=[dict(label=str(y), method="update", args=[{"visible": v}]) for y, v in zip(years, vis)])])
    fig.update_xaxes(title="% of the city's suicides", ticksuffix="%", range=[0, 100])
    fig.update_yaxes(autorange="reversed", gridcolor=SURFACE)
    return style(fig, title, subtitle, height=max(420, 40 * len(cities) + 180))


# --------------------------------------------------------------------------- rates


def rate_heat(r: pd.DataFrame, kind: list[str], title: str, subtitle: str = "", highlight: str = "Tamil Nadu", top: int | None = None) -> go.Figure:
    r = r[r.entity_type.isin(kind) & r.rate.notna() & (r.rate_check == "ok")]
    piv = r.pivot_table(index="name_std", columns="year", values="rate", aggfunc="first")
    latest = piv.columns.max()
    piv = piv[piv[latest].notna()].sort_values(latest, ascending=False)
    if top:
        piv = piv.head(top)
    labels = [f"<b>{n}</b>" if n == highlight else n for n in piv.index]
    fig = go.Figure(go.Heatmap(z=piv.values, x=[str(c) for c in piv.columns], y=labels, colorscale=[[i / (len(HEAT) - 1), c] for i, c in enumerate(HEAT)],
                               xgap=1, ygap=1, colorbar=dict(title="per lakh", thickness=12, outlinewidth=0),
                               hovertemplate="<b>%{y}</b> %{x}<br>%{z:.1f} suicides per lakh people<extra></extra>"))
    fig.update_yaxes(autorange="reversed", gridcolor=SURFACE, tickfont=dict(size=11))
    fig.update_xaxes(gridcolor=SURFACE, type="category", tickangle=-90)
    return style(fig, title, subtitle, height=max(500, 17 * len(piv) + 200))


# --------------------------------------------------------------------------- page


def page(sections: list[tuple[str, str, list]], path, title: str, intro: str) -> None:
    parts = []
    for i, (head, text, figs) in enumerate(sections):
        divs = "".join(f'<div class="fig">{f.to_html(full_html=False, include_plotlyjs=False, config=dict(displaylogo=False, responsive=True))}</div>' for f in figs if f is not None)
        parts.append(f'<section id="s{i}"><h2>{html.escape(head)}</h2>{text}{divs}</section>')
    toc = "".join(f'<li><a href="#s{i}">{html.escape(h)}</a></li>' for i, (h, _, _) in enumerate(sections))
    path.write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<script src="https://cdn.jsdelivr.net/npm/plotly.js-dist-min@3.1.0/plotly.min.js"></script>
<style>
:root{{--surface:{SURFACE};--plane:#f9f9f7;--ink:{INK};--ink2:{INK2};--muted:{MUTED};--line:{GRID}}}
body{{margin:0;background:var(--plane);color:var(--ink);font:15px/1.55 {FONT}}}
main{{max-width:1100px;margin:0 auto;padding:24px 16px 80px}}
h1{{font-size:26px;margin:8px 0 4px}} h2{{font-size:20px;margin:40px 0 8px;padding-top:8px;border-top:1px solid var(--line)}}
p,li{{color:var(--ink2)}} .lede{{font-size:16px}} ul.toc{{columns:2;padding-left:18px}} a{{color:#256abf}}
.fig{{background:var(--surface);border:1px solid rgba(11,11,11,.08);border-radius:8px;margin:14px 0;padding:4px;overflow:hidden}}
.note{{font-size:13px;color:var(--muted)}} table{{border-collapse:collapse;font-size:13px;font-variant-numeric:tabular-nums}}
td,th{{padding:3px 8px;border-bottom:1px solid var(--line);text-align:right}} th:first-child,td:first-child{{text-align:left}}
@media (max-width:700px){{ul.toc{{columns:1}}}}
</style></head><body><main><h1>{html.escape(title)}</h1>{intro}<ul class="toc">{toc}</ul>{''.join(parts)}</main></body></html>""", encoding="utf-8")


def save_fig(fig: go.Figure | None, name: str) -> None:
    if fig is None:
        return
    CHARTS.mkdir(parents=True, exist_ok=True)
    fig.write_html(CHARTS / f"{name}.html", include_plotlyjs="cdn", config=dict(displaylogo=False, responsive=True))
