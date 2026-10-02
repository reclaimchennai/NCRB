"""Every NCRB table that recurs across editions, joined over the years, for /explore/.

    uv run --extra analysis --extra vlm python -m analysis.families            # all three reports
    uv run --extra analysis --extra vlm python -m analysis.families psi        # one

A *family* is one table followed through every edition that printed it, even
when NCRB reworded its title ("Profile of suicide victims by profession" ->
"Profession-wise distribution of suicides") or reordered it: titles are
reduced to their content words, without years, numbering and geography, and
tables whose word sets match are one family. For each year the best printing
is used (the table published on its own over the full report, text over
scans), together with its continuation pages.

Columns are matched across years by their cleaned headings; a scanned year
whose headings were garbled is matched by position when it has the same
number of columns as the clean years. Rows are States, UTs and cities where
the table is State/UT/city-wise (named as today), or the table's own row
labels (crime heads, causes, age groups...) where it is not. A year whose
printed totals mostly fail to add up is left out.

Output (not in git; deployed with the site and published in the data release):
    web/data/explore/index.json                   every family: report, topic, title, years
    web/data/explore/<pub>/<family>.json          rows x columns x years
"""

from __future__ import annotations

import json
import re
import sys
import time
from collections import Counter, defaultdict
from functools import lru_cache

import pandas as pd

from .lib import ROOT, SCANNED, col_order, q

OUT = ROOT / "web" / "data" / "explore"
LISTING_RANK = {"table_content": 0, "additional_table": 1, "table_chapter": 2, "year_wise": 3}
METHOD_RANK = {"pdf_text": 0, "excel": 0, "pdf_vlm": 1, "pdf_mixed": 2, "pdf_ocr": 3}
PUB_NAME = {"cii": "Crime in India", "adsi": "Accidental Deaths & Suicides in India", "psi": "Prison Statistics India"}

STOP = set("""
during of the in and by for to on at as with from under vs versus a an
wise table list statement appendix figure contd concld continued concluded
distribution profile incidence details detail categorised categorized classified according number no nos
state states ut uts union territory territories city cities all india india total
""".split())
GEO = [
    (re.compile(r"city|cities|metropolitan", re.I), "city"),
    (re.compile(r"state|\but\b|uts\b", re.I), "state"),
    (re.compile(r"all.?india", re.I), "india"),
]


SYN = {"gender": "sex", "prisoner": "inmate", "jail": "prison", "convicted": "convict", "accidental": "accident",
       "suicidal": "suicide", "occurrence": "occurrence", "month": "month", "months": "month"}


def stem(w: str) -> str:
    w = w.lower()
    w = SYN.get(w, w)
    for a, b in (("ies", "y"), ("sses", "ss")):
        if w.endswith(a) and len(w) > 5:
            return w[: -len(a)] + b
    if w.endswith("s") and len(w) > 4 and not w.endswith("ss"):
        return w[:-1]
    return w


def family_key(title: str) -> tuple[str, str]:
    t = re.sub(r"\((?:contd|concld|concluded|continued)[^)]*\)", " ", title or "", flags=re.I)
    t = re.sub(r"^\W*(?:(?:table|list|figure|statement|appendix)\W*)?[0-9ivxl]+[A-Z]?(?:[.\-][0-9]+[A-Z]?)*\W+", "", t, flags=re.I)
    geo = next((tag for rx, tag in GEO if rx.search(t)), "")
    t = re.sub(r"\b(19|20)\d\d\b", " ", t)
    words = [SYN.get(x, x) for x in (stem(w) for w in re.findall(r"[A-Za-z]+", t))]
    words = sorted({w for w in words if w not in STOP and len(w) > 1})
    return " ".join(words), geo


def col_key(label: str) -> str:
    s = (label or "").lower()
    s = re.sub(r"\(\s*col[^)]*\)|\bcol\.?\s*\d+[^|]*|\(\s*\d+\s*\)|\[\s*\d+\s*\]", " ", s)
    s = re.sub(r"[^a-z0-9%|]+", " ", s)
    s = re.sub(r"\s*\|\s*", "|", s)
    return re.sub(r"\s+", " ", s).strip(" |")


SKIP_COL = re.compile(r"^(sl|s|si)\.? ?no|^rank|^serial", re.I)


@lru_cache(maxsize=200_000)
def place_of(name: str, section: str, scanned: bool):
    from .engine import resolve

    try:
        return resolve(name, section, scanned)
    except Exception:
        return None


def row_key(name: str) -> str:
    s = re.sub(r"^[\W\d]+[.)]?\s*", "", str(name or "")).lower()
    s = re.sub(r"[^a-z0-9%]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def slug(s: str, n: int = 90) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:n].strip("-")


def build(pub: str) -> list[dict]:
    t = q("SELECT table_id, publication, year, listing, topic, title, method, n_rows, n_cols, n_cells, checks_total, checks_passed, source_url "
          "FROM tables WHERE publication = ? AND n_cells > 0", [pub])
    individual = set(t.loc[t.listing.isin(["table_content", "additional_table"]), "year"])
    t = t[t.listing.isin(["table_content", "additional_table"]) | ~t.year.isin(individual)]
    # district-wise tables run to 700+ rows a year and need their own treatment; left out here
    t = t[~t.title.fillna("").str.contains(r"district", case=False)]
    keys = t.title.fillna("").map(family_key)
    t["fkey"] = keys.map(lambda k: k[0])
    t["geo"] = keys.map(lambda k: k[1])
    t = t[t.fkey.str.len() > 3]
    t["_l"] = t.listing.map(LISTING_RANK).fillna(9)
    t["_m"] = t.method.map(METHOD_RANK).fillna(9)
    out = []
    groups = t.groupby(["fkey", "geo"])
    for gi, ((fkey, geo), g) in enumerate(groups):
        if g.year.nunique() < 3:
            continue
        # for each year, the best listing and method, with every table of that printing (continuation pages)
        chosen = []
        for y, gy in g.groupby("year"):
            best = gy.sort_values(["_l", "_m", "n_cells"], ascending=[True, True, False]).iloc[0]
            same = gy[(gy.listing == best.listing) & (gy.method == best.method)]
            # a scanned printing that mostly fails its own totals is not used
            ok = same[~((same.checks_total >= 5) & (same.checks_passed < 0.7 * same.checks_total) & same.method.isin(SCANNED))]
            if len(ok):
                chosen.append(ok)
        if len(chosen) < 3:
            continue
        ch = pd.concat(chosen)
        fam = read_family(pub, fkey, geo, ch)
        if fam:
            out.append(fam)
        if gi % 200 == 0:
            print(f"  {pub}: {gi}/{len(groups)} groups, {len(out)} families", flush=True)
    return out


def read_family(pub: str, fkey: str, geo: str, ch: pd.DataFrame) -> dict | None:
    ids = ch.table_id.tolist()
    marks = ",".join("?" for _ in ids)
    c = q(f'SELECT table_id, "row", section, name, col_no, "column", value FROM cells WHERE table_id IN ({marks}) AND value IS NOT NULL', ids)
    if c.empty:
        return None
    c = c.merge(ch[["table_id", "year", "method"]], on="table_id")
    c["ck"] = c["column"].map(col_key)
    c = c[(c.ck != "") & ~c.ck.str.match(SKIP_COL)]
    c["_o"] = c.col_no.map(col_order)
    years = sorted(c.year.unique())
    # --- columns: headings seen in at least half the clean years, in the latest year's order
    clean = c[~c.method.isin(SCANNED)]
    basis = clean if clean.year.nunique() >= 2 else c
    per_year = basis.groupby("year").ck.apply(lambda s: set(s))
    cnt = Counter(k for s in per_year for k in s)
    need = max(2, 0.5 * len(per_year))
    keep = [k for k, n in cnt.items() if n >= need]
    if not keep:
        return None
    latest = basis[basis.year == basis.year.max()]
    order = latest.groupby("ck")._o.min().to_dict()
    keep.sort(key=lambda k: order.get(k, 1e9))
    keep = keep[:80]
    label_of = latest.groupby("ck")["column"].first().to_dict()
    for k in keep:
        label_of.setdefault(k, c.loc[c.ck == k, "column"].iloc[-1])
    # scanned years whose headings did not survive: by position, when the column count matches
    kset = set(keep)
    fixed = []
    for y, gy in c.groupby("year"):
        cols_y = gy.drop_duplicates("col_no").sort_values("_o")
        hit = cols_y.ck.isin(kset).mean()
        if hit < 0.5 and len(cols_y) == len(keep):
            m = dict(zip(cols_y.col_no, keep))
            gy = gy.assign(ck=gy.col_no.map(m))
        fixed.append(gy)
    c = pd.concat(fixed)
    c = c[c.ck.isin(kset)]
    if c.empty:
        return None
    # --- rows: places, or the table's own row labels
    names = c.drop_duplicates(["table_id", "row"])
    res = [place_of(str(n), str(s or ""), m in SCANNED) for n, s, m in zip(names.name, names.section, names.method)]
    share_places = sum(r is not None for r in res) / max(1, len(res))
    mode = "places" if share_places >= 0.6 else "categories"
    rowmap = {}
    for (tid, r), p in zip(zip(names.table_id, names["row"]), res):
        rowmap[(tid, r)] = p
    if mode == "places":
        c["rk"] = [rowmap.get((tid, r)) for tid, r in zip(c.table_id, c["row"])]
        c = c[c.rk.notna()]
        c["rname"] = c.rk.map(lambda p: p[0])
        c["rtype"] = c.rk.map(lambda p: p[1])
    else:
        c["rname"] = c.name.map(row_key)
        c = c[c.rname.str.len() > 1]
        present = c.groupby("rname").year.nunique()
        keep_rows = present[present >= max(2, 0.4 * len(years))].index
        c = c[c.rname.isin(keep_rows)]
        c["rtype"] = "row"
    if c.empty:
        return None
    # one value per row, column and year: the first printing of it
    c = c.sort_values(["year", "table_id", "row", "_o"]).drop_duplicates(["rname", "rtype", "ck", "year"])
    years = sorted(int(y) for y in c.year.unique())
    if len(years) < 3:
        return None
    # labels: places by name; category rows by their latest printed wording
    if mode == "categories":
        lab = c.sort_values("year").groupby("rname").name.last().to_dict()
        first = c.groupby("rname")._o.size()  # keep NCRB's own row order from the latest year
        roworder = c[c.year == c.year.max()].groupby("rname")["row"].min().to_dict()
        rows = sorted(c.rname.unique(), key=lambda r: roworder.get(r, 1e9))[:80]
        c = c[c.rname.isin(rows)]
        rowlist = [{"name": re.sub(r"^[\W\d]+[.)]?\s*", "", str(lab[r])).strip() or r, "type": "row"} for r in rows]
        rindex = {(r, "row"): i for i, r in enumerate(rows)}
    else:
        tord = {"total": 0, "state": 1, "ut": 2, "city": 3}
        pl = sorted({(n, t) for n, t in zip(c.rname, c.rtype)}, key=lambda x: (tord.get(x[1], 9), x[0]))
        rowlist = [{"name": n, "type": t} for n, t in pl]
        rindex = {k: i for i, k in enumerate(pl)}
    cindex = {k: i for i, k in enumerate(keep)}
    data = defaultdict(list)
    for rn, rt, ck, y, v in zip(c.rname, c.rtype, c.ck, c.year, c.value):
        i = rindex.get((rn, rt))
        if i is None:
            continue
        data[f"{i}.{cindex[ck]}"] += [int(y), round(float(v), 2) if not float(v).is_integer() else int(v)]
    newest = ch.sort_values(["year", "_l"], ascending=[False, True]).iloc[0]
    title = re.sub(r"^\W*(?:(?:table|list|figure)\W*)?[0-9]+[A-Z]?(?:\.[0-9]+[A-Z]?)*\s*[-–—_]*\s*", "", str(newest.title), flags=re.I)
    title = re.sub(r"\s*[-–]?\s*\b(during\s+)?(19|20)\d\d\b(\s*(to|-|–)\s*(19|20)\d\d)?", "", title).strip(" -–")
    fid = slug(f"{geo}-{fkey}" if geo else fkey)
    srcs = {}
    for r in ch.itertuples():
        lst = srcs.setdefault(str(int(r.year)), [])
        if not any(x["url"] == r.source_url for x in lst):
            lst.append({"title": re.sub(r"\s+", " ", str(r.title)).strip()[:160], "url": r.source_url, "method": r.method})
    topic = Counter(ch.topic.fillna("")).most_common(1)[0][0] or "Other tables"
    return {
        "id": fid, "pub": pub, "topic": topic, "title": title, "geo": geo, "mode": mode,
        "years": years, "cols": [re.sub(r"\s*\(\s*(col\.?\s*)?\d+\s*\)", "", str(label_of[k])).strip() for k in keep],
        "rows": rowlist, "d": data, "sources": srcs,
    }


def main(pubs: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    idx_path = OUT / "index.json"
    index = json.loads(idx_path.read_text()) if idx_path.exists() else {"families": []}
    index["families"] = [f for f in index["families"] if f["pub"] not in pubs]
    for pub in pubs:
        t0 = time.time()
        d = OUT / pub
        d.mkdir(parents=True, exist_ok=True)
        for f in d.glob("*.json"):
            f.unlink()
        fams = build(pub)
        seen = Counter()
        for f in fams:
            seen[f["id"]] += 1
            if seen[f["id"]] > 1:
                f["id"] = f"{f['id']}-{seen[f['id']]}"
            (d / f"{f['id']}.json").write_text(json.dumps(f, separators=(",", ":")), encoding="utf-8")
            index["families"].append({k: f[k] for k in ("id", "pub", "topic", "title", "geo", "mode")} | {
                "y0": f["years"][0], "y1": f["years"][-1], "n": len(f["years"]), "rows": len(f["rows"]), "cols": len(f["cols"])})
        print(f"{pub}: {len(fams)} families ({time.time() - t0:.0f}s)")
    index["families"].sort(key=lambda f: (list(PUB_NAME).index(f["pub"]), f["topic"], -f["n"], f["title"]))
    index["reports"] = PUB_NAME
    index["built"] = time.strftime("%Y-%m-%d")
    idx_path.write_text(json.dumps(index, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:] or ["psi", "adsi", "cii"])
