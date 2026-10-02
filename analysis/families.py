"""Every NCRB table that recurs across editions, joined over the years, for /explore/.

    uv run --extra analysis --extra vlm python -m analysis.families            # all three reports
    uv run --extra analysis --extra vlm python -m analysis.families psi        # one

A *family* is one table followed through every edition that printed it:

1. Each table gets a topic from analysis/taxonomy.py (one stable list instead
   of NCRB's drifting chapter names), a geography (States/UTs, cities, all
   India) and a cleaned title.
2. Tables whose cleaned titles have the same content words are one family.
3. Families in the same topic and geography whose years do not overlap, and
   whose column headings largely agree, are joined: this links tables across
   NCRB's redesigns (most Crime in India tables were renamed in 2014, many
   Prison Statistics tables in 2016).
4. For each year the best printing is used (the table published on its own
   over the full report, text over scans), with its continuation pages; a
   scanned printing that mostly fails its own totals is left out.

Columns are split into a *category* and a *breakdown*: "Bankruptcy or
Indebtedness | Male" is the category "Bankruptcy or Indebtedness" broken down
by "Male". Categories and breakdowns are matched across years by their
cleaned headings (a garbled scanned year is matched by position when it has
the same number of columns). Totals and subtotals are flagged so the charts
can keep them apart. Rows are States, UTs and cities (named as today) where
the table is place-wise, or the table's own row labels where it is not.

Output (not in git; deployed with the site and published in the data release):
    web/data/explore/index.json
    web/data/explore/<pub>/<family>.json
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from functools import lru_cache

import pandas as pd

from .lib import ROOT, SCANNED, col_order, q
from .taxonomy import prose, running_text, clean_title, geo_of, topic_of

OUT = ROOT / "web" / "data" / "explore"
LISTING_RANK = {"table_content": 0, "additional_table": 1, "table_chapter": 2, "year_wise": 3}
METHOD_RANK = {"pdf_text": 0, "excel": 0, "pdf_vlm": 1, "pdf_mixed": 2, "pdf_ocr": 3}
PUB_NAME = {"cii": "Crime in India", "adsi": "Accidental Deaths & Suicides in India", "psi": "Prison Statistics India"}

STOP = set("""
during of the in and by for to on at as with from under vs versus a an
wise table list statement appendix figure contd concld continued concluded
distribution profile incidence details detail categorised categorized classified according number no nos
state states ut uts union territory territories city cities all india india total metropolitan mega
""".split())
SYN = {"gender": "sex", "prisoner": "inmate", "jail": "prison", "convicted": "convict", "accidental": "accident",
       "suicidal": "suicide", "months": "month", "crimes": "crime", "cyber": "cyber"}


def stem(w: str) -> str:
    w = SYN.get(w.lower(), w.lower())
    for a, b in (("ies", "y"), ("sses", "ss")):
        if w.endswith(a) and len(w) > 5:
            return w[: -len(a)] + b
    if w.endswith("s") and len(w) > 4 and not w.endswith("ss"):
        w = w[:-1]
    return SYN.get(w, w)


def tokens(title: str) -> frozenset:
    return frozenset(w for w in (stem(x) for x in re.findall(r"[A-Za-z]+", title or "")) if w not in STOP and len(w) > 1)


def jacc(a, b) -> float:
    return len(a & b) / max(1, len(a | b))


# ---------------------------------------------------------------- columns

SEX = {"male": "Male", "males": "Male", "men": "Male", "m": "Male", "female": "Female", "females": "Female", "women": "Female",
       "f": "Female", "transgender": "Transgender", "tg": "Transgender", "third gender": "Transgender", "total": "Total", "t": "Total",
       "persons": "Total", "boys": "Boys", "girls": "Girls"}
TOTAL_RX = re.compile(r"(^|[^a-z])(grand\s+)?(sub[\s-]*)?(?<!to )(?<!of )(?<!in )total([^a-z]|$)|\(total\)", re.I)
SKIP_COL = re.compile(r"^(sl|s|si)\.? ?no|^rank|^serial|^state|^ut$|^city$|^name of", re.I)


ZW = re.compile(r"[\u200b-\u200f\u2060\ufeff]")
ENUM = re.compile(r"^\s*(?:[A-Z]|[a-z]\d?|[ivx]{1,4}|\d{1,2})\s*[.)]\s+")


def clean_head(s: str) -> str:
    s = ZW.sub("", str(s or ""))
    # words broken across a narrow column ('Apprehen ded', 'Communicatio n') and headings printed twice ('Apprehend Apprehend')
    s = re.sub(r"\b([A-Za-z]{4,}) (lity|ity|mpt|ng|ing|tion|tions|sion|sions|ment|ments|ted|ded|ed|n|ly|al|ies|ive|ives|ance|ence|ble|ous|ary|ory|ure|ism|ist|ful|cy|nal|ical|es)\b", r"\1\2", s)
    s = re.sub(r"\b(\w+) \1\b", r"\1", s, flags=re.I)
    s = re.sub(r"\(\s*col[^)]*\)|\bcol\.?\s*\d+[^|]*|\(\s*\d+\s*\)|\[\s*\d+\s*\]|\{[^}]*\}", " ", s)
    s = re.sub(r"\(\s*(19|20)\d\d\s*\)|\+\+?|\*+", " ", s)      # '(2016)', footnote marks
    s = re.sub(r"\s+", " ", s).strip(" .:-–")
    return ENUM.sub("", s).strip()


SEC_RX = re.compile(r"(?:\bsec(?:tion)?s?\.?|\bu/s\.?)\s*(\d{1,3}\s*[a-f]?(?:\s*\(\d+\))?(?:\s*(?:,|&|/|and|to|-|r/w)\s*(?:sec\.?\s*)?\d{1,3}\s*[a-f]?)*)", re.I)
GENERIC = {"others", "other", "total", "sub total", "subtotal", "grand total", "others please specify", "others specify", "other crimes",
           "other offences", "other sections", "male", "female", "cases", "persons", "number", "percentage", "share", "percentage share",
           "rate", "crime rate", "incidence", "total cases", "variation", "percentage variation"}


# the same measure under each edition's wording
CANON = [(re.compile(r"^crimerate|^rateof(total|cognizable)|^rateof\w*crimes?$|^rate$"), "rate"),
         (re.compile(r"^(%|percentage|percent)share|^%contribution|^percentagecontribution"), "share"),
         (re.compile(r"midyear.*population|^population.*lakh|^projectedpopulation"), "population"),
         (re.compile(r"^(incidence|casesregistered|casesreported|totalcases|noofcases|numberofcases)$"), "cases"),
         (re.compile(r"^(%|percentage)variation"), "variation")]


def _norm(s: str) -> str:
    s = clean_head(s).lower()
    s = re.sub(r"\br/w\b.*$", "", s)                 # 'read with ...' qualifiers change between editions
    return re.sub(r"[^a-z0-9%]+", "", s)             # no spaces: survives words split across lines ('communicatio n')


def key_of(s: str) -> str:
    """A category's identity across editions: its section numbers where the heading names them, else its wording."""
    parts = [p for p in str(s or "").split(" · ") if p.strip()]
    if not parts:
        return ""
    leaf = parts[-1]
    m = SEC_RX.search(leaf)
    if m:
        secs = sorted(set(re.findall(r"\d{1,3}\s*[a-f]?", m.group(1).lower().replace(" ", ""))))
        return f"sec:{','.join(secs)}"
    base = _norm(leaf)
    if len(parts) == 1:
        for rx, canon in CANON:
            if rx.search(base):
                return canon
    words = re.sub(r"[^a-z ]+", " ", clean_head(leaf).lower()).strip()
    if words in GENERIC or len(base) < 4:
        return f"{_norm(parts[-2]) if len(parts) > 1 else ''}/{base}"
    return base


def split_col(label: str) -> tuple[str, str]:
    """(category, breakdown). The breakdown is a sex/total level at either end of the heading path; else empty."""
    if re.search(r"col\.?\s*\d+\s*/\s*\d+|/\s*\(?\s*col\.?\s*\d|col\.?\s*\d+(\s*[+,]?\s*\d+){2,}", str(label or ""), re.I):
        return "", ""                                   # '%share (Col.9/109) x 100': worked out from other columns
    parts = [clean_head(p) for p in str(label or "").split("|")]
    parts = [p for p in parts if p]
    # a word broken across two heading rows: 'Apprehend | ed were Convicted in Past'
    for i in range(len(parts) - 1, 0, -1):
        if re.match(r"^(ed|ded|ted|n|ing|tion|ment)\b", parts[i]):
            parts[i - 1:i + 1] = [parts[i - 1] + parts[i]]
    if parts and re.fullmatch(r"(19|20)\d\d", parts[-1]):
        # a figure for an earlier (or the same) year printed alongside: kept, under its own category, dated to that year
        return f"@{parts[-1]}@{' · '.join(parts[:-1]) or 'Cases registered'}", ""
    if not parts:
        return "", ""
    last, first = parts[-1].lower(), parts[0].lower()
    if len(parts) > 1 and last in SEX:
        return " · ".join(parts[:-1]), SEX[last]
    if len(parts) > 1 and first in SEX:
        return " · ".join(parts[1:]), SEX[first]
    if len(parts) == 1 and last in SEX and last != "total":
        return "All", SEX[last]
    return " · ".join(parts), ""


@lru_cache(maxsize=200_000)
def place_of(name: str, section: str, scanned: bool, year: int | None = None):
    from .engine import resolve

    try:
        return resolve(name, section, scanned, year)
    except Exception:
        return None


def row_key(name: str) -> str:
    s = re.sub(r"^[\W\d]+[.)]?\s*", "", str(name or "")).lower()
    s = re.sub(r"[^a-z0-9%]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def slug(s: str, n: int = 90) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:n].strip("-")


# ---------------------------------------------------------------- grouping

def build(pub: str) -> list[dict]:
    t = q("SELECT table_id, publication, year, listing, topic AS chapter, title, method, n_rows, n_cols, n_cells, checks_total, checks_passed, source_url "
          "FROM tables WHERE publication = ? AND n_cells > 0", [pub])
    # district-wise tables run to 700+ rows a year; they stay on the Tables page
    t = t[~t.title.fillna("").str.contains(r"district", case=False)].copy()
    t["ctitle"] = t.title.map(clean_title)
    t["chapter"] = t.chapter.fillna("")
    t["topic"] = [topic_of(pub, c, x) for c, x in zip(t.chapter, t.title)]
    t["geo"] = [geo_of(c, x) for c, x in zip(t.chapter, t.title)]
    t["tok"] = t.ctitle.map(tokens)
    t = t[t.tok.map(len) > 0]
    # the categories each table prints, for joining families across redesigns
    heads = q('SELECT c.table_id, c."column" FROM cells c JOIN tables x USING (table_id) WHERE x.publication = ? GROUP BY 1, 2', [pub])
    cats_of = defaultdict(set)
    for tid, col in zip(heads.table_id, heads["column"]):
        cat, _ = split_col(col)
        k = key_of(re.sub(r"^@\d{4}@", "", cat))
        if k and not SKIP_COL.match(k):
            cats_of[tid].add(k)
    # year-wise and chapter PDFs reprint most individual tables, but some tables (e.g. Cyber Crimes - IT Act Cases,
    # 2017-2024) are printed only there: a reprint is dropped, a table found nowhere else is kept
    ind = t.listing.isin(["table_content", "additional_table"])
    by_year = defaultdict(list)
    for tid, y, g, tok in zip(t.table_id[ind], t.year[ind], t.geo[ind], t.tok[ind]):
        by_year[y].append((cats_of[tid], g, tok))
    def reprint(tid, y, g, tok):
        mine = cats_of[tid]
        return any((g == g2 or "" in (g, g2)) and ((mine and jacc(mine, c2) >= 0.6) or (not mine and jacc(tok, t2) >= 0.8))
                   for c2, g2, t2 in by_year.get(y, []))
    keep = [True if i else not reprint(tid, y, g, tok) for i, tid, y, g, tok in zip(ind, t.table_id, t.year, t.geo, t.tok)]
    t = t[keep].copy()
    t["_l"] = t.listing.map(LISTING_RANK).fillna(9)
    t["_m"] = t.method.map(METHOD_RANK).fillna(9)
    t["fk"] = [f"{tp}|{g}|{' '.join(sorted(k))}" for tp, g, k in zip(t.topic, t.geo, t.tok)]
    groups = []
    for fk, g in t.groupby("fk"):
        cats = set().union(*(cats_of[i] for i in g.table_id))
        groups.append({"topic": g.topic.iloc[0], "geo": g.geo.iloc[0], "tok": g.tok.iloc[0], "years": set(g.year), "rows": g, "cats": cats})
    # join families of one topic and geography across non-overlapping years when their columns agree
    groups.sort(key=lambda x: (x["topic"], x["geo"], -len(x["years"])))
    merged: list[dict] = []
    for gr in groups:
        home = None
        for m in merged:
            if m["topic"] != gr["topic"] or (m["geo"] != gr["geo"] and "" not in (m["geo"], gr["geo"])):
                continue
            if len(m["years"] & gr["years"]) > 1:
                continue
            ct, tt = jacc(m["cats"], gr["cats"]), jacc(m["tok"], gr["tok"])
            same_geo = m["geo"] == gr["geo"]
            if (ct >= 0.45 and tt >= 0.2) or (same_geo and ((ct >= 0.3 and tt >= 0.45) or (ct >= 0.15 and tt >= 0.6) or tt >= 0.75)):
                home = m
                break
        if home:
            home["geo"] = home["geo"] or gr["geo"]
            home["years"] |= gr["years"]
            home["rows"] = pd.concat([home["rows"], gr["rows"]])
            home["cats"] |= gr["cats"]
        else:
            merged.append(dict(gr))
    # one- or two-year tables with a title of their own (e.g. 'Cyber Crimes Incidence & Crime Rate - 2014-2016'):
    # attached to the family of the same topic and geography whose columns contain theirs
    big = [m for m in merged if len(m["years"]) > 3]
    for sm in [m for m in merged if len(m["years"]) <= 3 and m["cats"]]:
        best, bs = None, 0
        for m in big:
            if m["topic"] != sm["topic"] or (m["geo"] != sm["geo"] and "" not in (m["geo"], sm["geo"])) or (m["years"] & sm["years"]):
                continue
            cont, tt = len(sm["cats"] & m["cats"]) / len(sm["cats"]), jacc(m["tok"], sm["tok"])
            if cont >= 0.6 and (tt >= 0.3 or (cont >= 0.8 and tt >= 0.15)) and cont + tt > bs:
                best, bs = m, cont + tt
        if best is not None:
            best["rows"] = pd.concat([best["rows"], sm["rows"]]); best["years"] |= sm["years"]; best["cats"] |= sm["cats"]
            sm["years"] = set()
    merged = [m for m in merged if m["years"]]
    # the 2014 redesign renamed most tables: an old series (to 2013/14) and a new one (from 2013/14) of one topic and
    # geography are joined when they are each other's closest match, on looser terms than above
    def score(a, b):
        if a["topic"] != b["topic"] or (a["geo"] != b["geo"] and "" not in (a["geo"], b["geo"])) or len(a["years"] & b["years"]) > 1:
            return 0
        ct, tt = jacc(a["cats"], b["cats"]), jacc(a["tok"], b["tok"])
        cont = len(a["cats"] & b["cats"]) / max(1, min(len(a["cats"]), len(b["cats"])))
        return ct + tt + cont / 2 if ((tt >= 0.35 and ct >= 0.1) or ct >= 0.3 or tt >= 0.5 or (cont >= 0.5 and tt >= 0.3)) else 0
    old = [m for m in merged if 2010 <= max(m["years"]) <= 2016 and min(m["years"]) < 2010 and len(m["years"]) >= 3]
    new = [m for m in merged if min(m["years"]) >= 2013 and len(m["years"]) >= 3]
    pairs = sorted(((score(a, b), ia, ib) for ia, a in enumerate(old) for ib, b in enumerate(new)), reverse=True)
    used_a, used_b, gone = set(), set(), set()
    for sc, ia, ib in pairs:
        if sc <= 0:
            break
        if ia in used_a or ib in used_b:
            continue
        used_a.add(ia); used_b.add(ib)
        a, b = old[ia], new[ib]
        b["rows"] = pd.concat([a["rows"], b["rows"]]); b["years"] |= a["years"]; b["cats"] |= a["cats"]
        b["geo"] = b["geo"] or a["geo"]
        gone.add(id(a))
    merged = [m for m in merged if id(m) not in gone]
    out = []
    for i, m in enumerate(merged):
        g = m["rows"]
        if g.year.nunique() < 3:
            continue
        chosen = []
        for y, gy in g.groupby("year"):
            best = gy.sort_values(["_l", "_m", "n_cells"], ascending=[True, True, False]).iloc[0]
            same = gy[(gy.listing == best.listing) & (gy.method == best.method) & (gy.fk == best.fk)]
            ok = same[~((same.checks_total >= 5) & (same.checks_passed < 0.7 * same.checks_total) & same.method.isin(SCANNED))]
            if len(ok):
                chosen.append(ok)
        if len(chosen) < 3:
            continue
        fam = read_family(pub, m["topic"], m["geo"], pd.concat(chosen))
        if fam:
            out.append(fam)
        if i % 200 == 0:
            print(f"  {pub}: {i}/{len(merged)} families read, {len(out)} kept", flush=True)
    return out


# ---------------------------------------------------------------- one family

NUM_LEAF = re.compile(r"^(no\.?|nos\.?|number|numbers|cases|incidence|total no\.?)$", re.I)
PCT_LEAF = re.compile(r"^(%|percentage|percent|%\s*share|percentage share)(\s+(to|of)\s+(the\s+)?total)?$", re.I)


KEEP_CASE = {"Act", "Acts", "Code", "Penal", "Procedure", "India", "Indian", "Sanhita", "Nyaya", "Bharatiya", "Government", "Railway", "Railways", "Police",
             "Sec", "Section", "Sections", "Hindu", "Muslim", "Christian", "Sikh", "Scheduled", "Caste", "Castes", "Tribe", "Tribes"}


def display_cat(label: str) -> str:
    """A category as a reader should see it: 'Old offenders convicted in the past · Thrice or more' rather than
    '... · Thrice Or More · No', '... (% of total)' rather than '... · Percentage To Total'."""
    parts = [p.strip() for p in str(label).split(" · ") if p.strip()]
    pct = ""
    if len(parts) > 1 and NUM_LEAF.match(parts[-1]):
        parts = parts[:-1]
    elif len(parts) > 1 and PCT_LEAF.match(parts[-1]):
        parts, pct = parts[:-1], " (% of total)"
    out = []
    for p in parts:
        w = p.split()
        if len(w) > 2 and sum(x[:1].isupper() for x in w) / len(w) > 0.6:     # 'Convicted In The Past' -> 'Convicted in the past'
            p = " ".join([w[0]] + [x if (x.isupper() and len(x) > 1) or re.search(r"\d", x) or x.strip("(),.") in KEEP_CASE else x.lower() for x in w[1:]])
        out.append(p)
    return (" · ".join(out) + pct) if out else str(label)


def shift_fix(c: pd.DataFrame) -> pd.DataFrame:
    """Headings drawn one column early (ADSI 2006-2011): 'Illness (Paralysis) | Male' appears twice, the second time
    over what is really the next category's Male column. A category's second Male column goes to the column after it."""
    cols = c.drop_duplicates(["table_id", "col_no"])[["table_id", "col_no", "_o", "cat", "brk"]].sort_values(["table_id", "_o"])
    fix = {}
    for tid, g in cols.groupby("table_id", sort=False):
        rows = list(g.itertuples(index=False))
        seen_male = set()
        for i, r in enumerate(rows):
            if r.brk != "Male":
                continue
            if r.cat in seen_male and i + 1 < len(rows) and rows[i + 1].cat != r.cat:
                nxt = rows[i + 1].cat
                if not any(x.cat == nxt and x.brk == "Male" for x in rows):
                    fix[(tid, r.col_no)] = nxt
            seen_male.add(r.cat)
    if fix:
        key = list(zip(c.table_id, c.col_no))
        c = c.assign(cat=[fix.get(k, v) for k, v in zip(key, c.cat)])
    return c


def unify(c: pd.DataFrame) -> pd.Series:
    """Categories renamed between editions ('Illness (Insanity)' -> 'Illness (Insanity/Mental illness)', 'Death of Dear a
    Person' -> 'Death of Dear Person'): joined when they never appear in the same year, sit under the same parent
    heading, and most words of the shorter name are in the longer."""
    years = c.groupby("ck").year.apply(set).to_dict()
    label = c.sort_values("year").groupby("ck").cat.last().to_dict()
    info = {}
    for k, lab in label.items():
        if k.startswith("sec:"):
            continue
        parts = lab.split(" · ")
        info[k] = (" · ".join(parts[:-1]).lower(), tokens(parts[-1]), bool(TOTAL_RX.search(lab)))
    pairs = []
    keys = list(info)
    for i, a in enumerate(keys):
        pa, ta, xa = info[a]
        if not ta:
            continue
        for b in keys[i + 1:]:
            pb, tb, xb = info[b]
            if pa != pb or xa != xb or not tb or (years[a] & years[b]):
                continue
            inter = len(ta & tb)
            sim, jj = inter / min(len(ta), len(tb)), inter / len(ta | tb)
            # 'Status' is what a two-line heading 'Bankruptcy or sudden change in economic | Status' kept in some years
            def tail(short, long):
                w = re.sub(r"[^a-z ]", "", label[short].split(" · ")[-1].lower()).strip()
                return " " not in w and len(w) > 3 and w not in GENERIC and label[long].lower().rstrip(") ").endswith(" " + w)
            if (sim >= 0.67 and jj >= 0.34) or (sim >= 0.99 and jj >= 0.25) or tail(a, b) or tail(b, a):
                pairs.append((sim + jj, a, b))
    root = {k: k for k in years}
    def find(k):
        while root[k] != k:
            k = root[k]
        return k
    span = {k: set(v) for k, v in years.items()}
    for _, a, b in sorted(pairs, reverse=True):
        ra, rb = find(a), find(b)
        if ra == rb or (span[ra] & span[rb]):
            continue
        # the newer name carries the series
        keep, drop = (ra, rb) if max(span[ra]) >= max(span[rb]) else (rb, ra)
        root[drop] = keep
        span[keep] |= span[drop]
    return c.ck.map(find)


def read_family(pub: str, topic: str, geo: str, ch: pd.DataFrame) -> dict | None:
    ids = ch.table_id.tolist()
    marks = ",".join("?" for _ in ids)
    c = q(f'SELECT table_id, "row", section, name, col_no, "column", value FROM cells WHERE table_id IN ({marks}) AND value IS NOT NULL', ids)
    if c.empty:
        return None
    c = c.merge(ch[["table_id", "year", "method"]], on="table_id")
    sp = c["column"].map(split_col)
    c["cat"] = sp.map(lambda x: x[0])
    c["brk"] = sp.map(lambda x: x[1])
    # year columns ('2014', '2015', '2016' in a 2016 table): re-dated, and used only where no edition of that year has the figure
    yc = c.cat.str.match(r"^@\d{4}@")
    if yc.any():
        c["year"] = c.year.astype("int64")
        c.loc[yc, "year"] = c.loc[yc, "cat"].str.slice(1, 5).astype("int64")
        c.loc[yc, "cat"] = c.loc[yc, "cat"].str.slice(6)
        c["_late"] = (yc & (c.year != c.table_id.map(dict(zip(ch.table_id, ch.year))))).astype(int)
    else:
        c["_late"] = 0
    c["_o"] = c.col_no.map(col_order)
    c = shift_fix(c)
    c["ck"] = c.cat.map(key_of)
    c = c[(c.ck != "") & ~c.ck.str.match(SKIP_COL)]
    if c.empty:
        return None
    c["ck"] = unify(c)
    # categories printed in at least two years (in a joined family the old and new halves each count)
    clean = c[~c.method.isin(SCANNED)]
    basis = clean if clean.year.nunique() >= 2 else c
    per_year = basis.groupby("year").ck.apply(set)
    cnt = Counter(k for s in per_year for k in s)
    keep = [k for k, n in cnt.items() if n >= 2]
    if not keep:
        return None
    # scanned years whose headings did not survive: by position, when the column count matches a clean year's
    full = c.assign(fk=c.ck + "|" + c.brk)
    clean_full = full[~full.method.isin(SCANNED)]
    ref = clean_full[clean_full.year == clean_full.year.max()] if not clean_full.empty else full[full.year == full.year.max()]
    ref_cols = ref.drop_duplicates("col_no").sort_values("_o")
    fixed = []
    kset = set(keep)
    for y, gy in full.groupby("year"):
        cols_y = gy.drop_duplicates("col_no").sort_values("_o")
        if cols_y.ck.isin(kset).mean() < 0.5 and len(cols_y) == len(ref_cols):
            m_ck = dict(zip(cols_y.col_no, ref_cols.ck)); m_b = dict(zip(cols_y.col_no, ref_cols.brk))
            gy = gy.assign(ck=gy.col_no.map(m_ck), brk=gy.col_no.map(m_b))
        fixed.append(gy)
    c = pd.concat(fixed)
    c = c[c.ck.isin(kset)]
    if c.empty:
        return None
    # rows: places, or the table's own row labels
    names = c.drop_duplicates(["table_id", "row"])
    res = [place_of(str(n), str(s or ""), m in SCANNED, int(y)) for n, s, m, y in zip(names.name, names.section, names.method, names.year)]
    share_places = sum(r is not None for r in res) / max(1, len(res))
    mode = "places" if share_places >= 0.6 else "categories"
    years_all = sorted(c.year.unique())
    if mode == "places":
        rowmap = {(tid, r): p for (tid, r), p in zip(zip(names.table_id, names["row"]), res)}
        c["rk"] = [rowmap.get((tid, r)) for tid, r in zip(c.table_id, c["row"])]
        c = c[c.rk.notna()]
        c["rname"] = c.rk.map(lambda p: p[0])
        c["rtype"] = c.rk.map(lambda p: p[1])
    else:
        c["rname"] = c.name.map(row_key)
        c = c[c.rname.str.len() > 1]
        present = c.groupby("rname").year.nunique()
        c = c[c.rname.isin(present[present >= max(2, 0.3 * len(years_all))].index)]
        c["rtype"] = "row"
    if c.empty:
        return None
    c = c.merge(ch[["table_id", "year"]].rename(columns={"year": "_ed"}), on="table_id", how="left")
    c = c.sort_values(["_late", "_ed", "table_id", "row", "_o"], ascending=[True, False, True, True, True]).drop_duplicates(["rname", "rtype", "ck", "brk", "year"])
    years = sorted(int(y) for y in c.year.unique())
    if len(years) < 3:
        return None
    # category labels and order: the latest wording, NCRB's latest column order; totals last
    latest = c.sort_values("year")
    cat_label = latest.groupby("ck").cat.last().to_dict()
    cat_order = c[c.year == c.year.max()].groupby("ck")._o.min().to_dict()
    first_seen = c.groupby("ck")._o.min().to_dict()
    cats = sorted(c.ck.unique(), key=lambda k: (bool(TOTAL_RX.search(cat_label[k])), cat_order.get(k, 1e6 + first_seen.get(k, 0))))[:90]
    brks = [b for b in ["Total", "Male", "Female", "Transgender", "Boys", "Girls", ""] if b in set(c.brk)]
    if mode == "categories":
        lab = latest.groupby("rname").name.last().to_dict()
        roworder = c[c.year == c.year.max()].groupby("rname")["row"].min().to_dict()
        rows = sorted(c.rname.unique(), key=lambda r: (bool(TOTAL_RX.search(str(lab[r]))), roworder.get(r, 1e9)))[:90]
        rowlist = [{"name": re.sub(r"^[\W\d]+[.)]?\s*", "", str(lab[r])).strip() or r, "type": "row", **({"total": 1} if TOTAL_RX.search(str(lab[r])) else {})} for r in rows]
        rindex = {(r, "row"): i for i, r in enumerate(rows)}
    else:
        tord = {"total": 0, "state": 1, "ut": 2, "city": 3}
        pl = sorted({(n, t) for n, t in zip(c.rname, c.rtype)}, key=lambda x: (tord.get(x[1], 9), x[0]))
        rowlist = [{"name": n, "type": t} for n, t in pl]
        rindex = {k: i for i, k in enumerate(pl)}
    cindex = {k: i for i, k in enumerate(cats)}
    bindex = {b: i for i, b in enumerate(brks)}
    data = defaultdict(list)
    for rn, rt, ck, b, y, v in zip(c.rname, c.rtype, c.ck, c.brk, c.year, c.value):
        i, j = rindex.get((rn, rt)), cindex.get(ck)
        if i is None or j is None:
            continue
        v = float(v)
        data[f"{i}.{j}.{bindex[b]}"] += [int(y), int(v) if v.is_integer() else round(v, 2)]
    # the newest title that reads as a title (chapter PDFs sometimes carry the running text along)
    cand = ch.assign(_p=ch.ctitle.map(prose)).sort_values(["_p", "_l", "year"], ascending=[True, True, False]).iloc[0]
    title = cand.ctitle or clean_title(cand.title)
    if running_text(title):
        return None
    if len(title) > 140:
        title = title[:130].rsplit(" ", 1)[0] + "…"
    srcs = {}
    for r in ch.itertuples():
        lst = srcs.setdefault(str(int(r.year)), [])
        if not any(x["url"] == r.source_url for x in lst):
            lst.append({"title": re.sub(r"\s+", " ", str(r.title)).strip()[:160], "url": r.source_url, "method": r.method})
    olds = sorted({str(x) for x in ch.ctitle.unique() if x and x != title})[:6]
    return {
        "id": slug(f"{topic}-{geo}-{title}"), "pub": pub, "topic": topic, "title": title, "geo": geo, "mode": mode,
        "also": olds, "years": years,
        "cats": [{"name": display_cat(cat_label[k]), **({"total": 1} if TOTAL_RX.search(cat_label[k]) else {})} for k in cats],
        "brks": brks, "rows": rowlist, "d": data, "sources": srcs,
    }


def main(pubs: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    idx_path = OUT / "index.json"
    index = json.loads(idx_path.read_text()) if idx_path.exists() else {"families": []}
    index["families"] = [f for f in index.get("families", []) if f["pub"] not in pubs and "cats" in f]
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
                "y0": f["years"][0], "y1": f["years"][-1], "n": len(f["years"]), "rows": len(f["rows"]), "cats": len(f["cats"]),
                "also": f["also"][:3]})
        print(f"{pub}: {len(fams)} families ({time.time() - t0:.0f}s)")
    index["families"].sort(key=lambda f: (list(PUB_NAME).index(f["pub"]), f["topic"], {"state": 0, "city": 1, "india": 2}.get(f["geo"], 3), -f["n"], f["title"]))
    index["reports"] = PUB_NAME
    index["built"] = time.strftime("%Y-%m-%d")
    idx_path.write_text(json.dumps(index, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:] or ["psi", "adsi", "cii"])
