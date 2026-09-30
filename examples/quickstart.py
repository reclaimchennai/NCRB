"""Find a table, load it, plot it; then follow one table across years.

Run from the repository root:

    uv run --with plotly python examples/quickstart.py

Writes two HTML charts into examples/.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent

# --- 1. one table -----------------------------------------------------------
idx = pd.read_csv(ROOT / "data" / "tables_index.csv", low_memory=False)
hits = idx[
    (idx.publication == "adsi")
    & (idx.year == 2020)
    & (idx.listing == "table_content")
    & idx.title.str.contains("Profession", case=False)
    & idx.title.str.contains("State", case=False)
]
print(hits[["table_id", "title", "n_rows", "n_cols", "checks_passed", "checks_total"]].to_string(index=False))

table = hits.iloc[0]
long = pd.read_csv(ROOT / table.csv.replace(".csv", ".long.csv"))

# one line per (State/UT, profession, sex); drop total rows and the 'Total' sex column
d = long[(long.is_total == 0) & (long.h2 != "Total") & (long.h1 != "Total")]
fig = px.bar(
    d, x="name", y="value", color="h1", hover_data=["h2"],
    title=f"{table.title} (source: NCRB, ADSI {table.year})", height=800,
)
fig.update_layout(xaxis={"categoryorder": "total descending"}, xaxis_title="", yaxis_title="Suicides")
fig.write_html(OUT / "profession_wise_suicides_2020.html")

# --- 2. a time series -------------------------------------------------------
series = pd.read_csv(ROOT / "data" / "series_index.csv")
cand = series[(series.publication == "adsi") & (series.geography == "state-ut")].sort_values("n_years", ascending=False)
print(cand[["series_id", "title", "first_year", "last_year", "n_years"]].head(10).to_string(index=False))

s = cand.iloc[0]
ts = pd.read_csv(ROOT / s.csv)
states = ts[(ts.entity_type == "state") & ts.value.notna()]
first_col = states.column.iloc[0]
fig = px.line(
    states[states.column == first_col], x="year", y="value", color="name_std",
    title=f"{s.title}: {first_col} (source: NCRB)", height=700,
)
fig.write_html(OUT / "series_example.html")
print("charts written to", OUT)
