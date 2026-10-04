"""Label table titles and column headings with TypeSafe's Jev, as a second opinion on the regex rules.

Jev is a classifier: for each question it picks one of the options given here and returns calibrated
probabilities and a confidence. It sees only the text of a title or heading, never a figure, and cannot answer
outside the options, so it cannot invent data. Every figure still comes from the printed tables and passes the
same checks. Labels are kept in data/classify/*.jsonl (one line per text: the text, the label, its probability,
confidence and the model version), so they can be audited and are not asked again.

    uv run python -m analysis.classify label            # TYPESAFE_API_KEY from the environment or ./.env
    uv run python -m analysis.classify compare          # where Jev and the regex rules disagree
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "classify"
API = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-1.13.0"            # pinned: an alias can move and change answers
PUBS = {"cii": "Crime in India", "adsi": "Accidental Deaths & Suicides in India"}

# what a table counts; the code maps these to keep / drop
SCOPE = {
    "cii": {
        "all_cases": "every case registered (reported) under the crime heads it lists, in each State, Union Territory, "
                     "city or district: e.g. 'Incidence & Rate of Cognizable Crimes (IPC) under different crime heads', "
                     "'IPC Crimes (Crime Head-wise & State/UT-wise)', 'Comparative incidence of ...', 'Violent crimes', "
                     "'Murder cases (City-wise)', or one crime head (such as 'MURDER' or 'Total cognizable crime') across places",
        "women": "only crimes committed against women",
        "children": "only crimes committed against children",
        "sc_st": "only crimes or atrocities against Scheduled Castes or Scheduled Tribes",
        "senior_citizens": "only crimes against senior citizens",
        "foreigners": "only crimes against foreigners or tourists, or crimes committed by foreigners",
        "juveniles": "only crimes committed by juveniles",
        "cyber": "only cyber crimes, crimes through computers or communication devices, or IT Act cases",
        "railways": "only crimes on the railways or cases of the Government Railway Police (GRP)",
        "insurgents": "only crimes by insurgents, extremists, naxalites or terrorists",
        "other_subset": "only one other part of all cases (not one of the groups above)",
        "not_cases": "not a count of cases registered: persons arrested, charge-sheeted, convicted or acquitted; victims; "
                     "disposal of cases by police or courts; pending cases; property stolen or recovered and its value; "
                     "motives; police strength; only rates, percentages or shares; or anything else",
        "unreadable": "the title is empty, unreadable, or does not say what the table counts",
    },
    "adsi": {
        "all_deaths": "the total number of suicides, or of accidental deaths, in each State, Union Territory or city "
                      "(possibly with the split by sex, the rate, or the share)",
        "road_traffic": "deaths or accidents on roads, in traffic accidents",
        "breakdown": "suicides or accidental deaths split by one attribute: cause, means, profession, education, "
                     "social or economic status, age group, marital status, month, time of day, or type of accident other "
                     "than road",
        "not_deaths": "not a count of deaths: injured persons, numbers of accidents only, rates or percentages only, "
                      "or anything else",
        "unreadable": "the title is empty, unreadable, or does not say what the table counts",
    },
}
HEAD = {
    "cii": {
        "total": "total cognizable crimes under the IPC (or IPC/BNS): not a total that includes special & local laws (SLL), "
                 "not a total of one group",
        "murder": "murder as a whole (Sec. 302 IPC / 103 BNS)",
        "attempt_murder": "attempt to commit murder",
        "chna": "culpable homicide not amounting to murder",
        "rape": "rape as a whole (Sec. 376 IPC)",
        "kidnapping": "kidnapping and abduction as a whole",
        "dacoity": "dacoity",
        "robbery": "robbery",
        "burglary": "burglary or house-breaking",
        "theft": "theft as a whole",
        "riots": "riots",
        "cbt": "criminal breach of trust",
        "cheating": "cheating",
        "counterfeiting": "counterfeiting",
        "arson": "arson",
        "hurt": "hurt (simple and grievous hurt together)",
        "dowry_deaths": "dowry deaths",
        "molestation": "assault on women with intent to outrage her modesty (molestation)",
        "cruelty": "cruelty by husband or his relatives",
        "other_head": "a crime head not in this list (e.g. forgery, causing death by negligence, special & local laws), "
                      "or a combination of heads",
        "no_head": "names no crime head: only a year, 'Total', 'Incidence', 'Cases', 'I', 'V', 'R', a place, or a number",
    },
    "adsi": {
        "suicides": "suicides (persons who died by suicide)",
        "accidental": "accidental deaths of all kinds, or deaths due to unnatural causes",
        "road": "deaths in road or traffic accidents",
        "other_head": "something else: one cause or means, injured persons, number of accidents, population",
        "no_head": "names nothing: only a year, 'Total', 'Number', 'Died', 'Male', 'Female', a place, or a number",
    },
}
KIND = {
    "whole": "the number of cases (incidence, cases reported or registered) for the whole of what it names; for deaths, "
             "the number of persons who died, all sexes. A 'Total' of the head counts as the whole.",
    "part": "only a part: a sub-category or section of the head, one sex, one age group, attempts only, only the IPC "
            "half or only the BNS half of 2024, or one kind of victim",
    "victims_persons": "a number of victims or persons (arrested, injured, accused), not of cases",
    "rate_share": "a rate, percentage, share, rank, ratio, or change over a year",
    "other": "anything else: a population, a value in rupees, a year, a column number",
}


def api_key() -> str:
    if os.environ.get("TYPESAFE_API_KEY"):
        return os.environ["TYPESAFE_API_KEY"]
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            m = re.match(r"\s*TYPESAFE_API_KEY\s*=\s*['\"]?([^'\"\s]+)", line)
            if m:
                return m.group(1)
    sys.exit("no TYPESAFE_API_KEY (set it, or put it in .env)")


def call(state: dict, questions: dict, key: str, tries: int = 6) -> dict:
    body = json.dumps({"model": MODEL, "state": state, "questions": questions}).encode()
    for t in range(tries):
        req = urllib.request.Request(API, data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(float(e.headers.get("retry-after") or 2 * (t + 1)))
                continue
            raise RuntimeError(f"HTTP {e.code}: {e.read()[:200]!r}")
        except (urllib.error.URLError, TimeoutError):
            time.sleep(2 * (t + 1))
    raise RuntimeError("no answer after retries")


def choice(instructions: str, options: dict, reverse: bool = False) -> dict:
    items = list(options.items())
    return {"type": "choice", "instructions": instructions, "criteria": dict(reversed(items) if reverse else items)}


def questions_for(kind: str, pub: str, reverse: bool = False) -> dict:
    if kind == "titles":
        return {"scope": choice("For each place it lists, what does the table titled `table_title` count?", SCOPE[pub], reverse)}
    return {"head": choice("Which head does the column heading `column_heading` name?", HEAD[pub], reverse),
            "kind": choice("What kind of number is in the column headed `column_heading`?", KIND, reverse)}


def state_for(kind: str, pub: str, text: str) -> dict:
    if kind == "titles":
        return {"publication": PUBS[pub], "table_title": text}
    return {"publication": PUBS[pub], "column_heading": text,
            "note": "Parent headings are joined with ' | '. A trailing I means incidence (cases), V victims, R rate. "
                    "Text may be garbled by OCR."}


def path(kind: str, pub: str) -> Path:
    return OUT / f"{kind}-{pub}.jsonl"


def load(kind: str, pub: str) -> dict:
    p = path(kind, pub)
    if not p.exists():
        return {}
    out = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out[r["text"]] = r
    return out


def label(kind: str, pub: str, texts: list[str], workers: int, key: str, reverse: bool = False) -> dict:
    """Ask Jev about each text once; answers are appended to the .jsonl as they come."""
    done = load(kind, pub)
    field = "rev" if reverse else None
    todo = [t for t in texts if t not in done or (reverse and "rev" not in done[t])]
    print(f"{kind}-{pub}{' (options reversed)' if reverse else ''}: {len(texts) - len(todo)} done, {len(todo)} to ask", flush=True)
    if not todo:
        return done
    OUT.mkdir(parents=True, exist_ok=True)
    lock, n, errors = threading.Lock(), 0, 0

    def one(text):
        r = call(state_for(kind, pub, text), questions_for(kind, pub, reverse), key)
        ans = {q: {"label": a["choice"], "p": round(a["probabilities"][a["choice"]], 3), "conf": round(a["confidence"], 3)}
               for q, a in r["answers"].items()}
        return text, ans, r.get("model")

    with cf.ThreadPoolExecutor(workers) as ex:
        futs = [ex.submit(one, t) for t in todo]
        for f in cf.as_completed(futs):
            try:
                text, ans, model = f.result()
            except Exception as e:
                errors += 1
                print("  error:", str(e)[:160], flush=True)
                continue
            with lock:
                rec = done.get(text, {"text": text})
                if field:
                    rec["rev"] = ans
                else:
                    rec.update(ans)
                rec["model"] = model
                done[text] = rec
                n += 1
                if n % 500 == 0:
                    print(f"  {n}/{len(todo)}", flush=True)
                    write(kind, pub, done)
    write(kind, pub, done)
    print(f"  {n} answered, {errors} errors", flush=True)
    return done


def write(kind: str, pub: str, done: dict) -> None:
    tmp = path(kind, pub).with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(done[t], ensure_ascii=False, sort_keys=True) + "\n" for t in sorted(done)), encoding="utf-8")
    tmp.replace(path(kind, pub))


def texts_from_db() -> dict:
    import duckdb

    con = duckdb.connect(str(ROOT / "data" / "web" / "ncrb.duckdb"), read_only=True)
    kw = {"cii": r"murd|homicide|rape|kidnap|abduct|dacoit|robber|burglar|house.?break|theft|riot|breach of trust|cheat|"
                 r"counterfeit|arson|hurt|dowry|modesty|molest|cruelty|total|cogni[sz]able|ipc|bns",
          "adsi": r"suicid|accident|death|died|killed|total|unnatural"}
    out = {}
    for pub in PUBS:
        out[("titles", pub)] = sorted(t for (t,) in con.execute(
            "SELECT DISTINCT title FROM tables WHERE publication = ? AND n_cells > 0 AND title IS NOT NULL", [pub]).fetchall()
            if t.strip())
        cols = [c for (c,) in con.execute('SELECT DISTINCT c."column" FROM cells c JOIN tables t USING (table_id) '
                                          'WHERE t.publication = ? AND c."column" IS NOT NULL', [pub]).fetchall()]
        out[("columns", pub)] = sorted(c for c in cols if c.strip() and re.search(kw[pub], c, re.I))
    return out


# ------------------------------------------------------------------ what the long series does with the labels
KEEP_SCOPE = {"cii": {"all_cases"}, "adsi": {"all_deaths", "road_traffic"}}
WOMEN_HEADS = {"rape", "dowry_deaths", "molestation", "cruelty"}       # a table of crimes against women has all of these


def compare() -> None:
    """Where Jev and the regex rules of analysis.longseries disagree, for review."""
    from .longseries import ADSI_HEADS, ADSI_NOT_TABLE, IPC_HEADS, NOT_CASES_COL, NOT_CASES_TABLE, NOT_COUNT_COL, head_of

    for pub, not_table, heads, not_col in (("cii", NOT_CASES_TABLE, IPC_HEADS, NOT_CASES_COL),
                                           ("adsi", ADSI_NOT_TABLE, ADSI_HEADS, NOT_COUNT_COL)):
        t = load("titles", pub)
        dis = [(x, r["scope"]) for x, r in t.items() if bool(not_table.search(x)) == (r["scope"]["label"] in KEEP_SCOPE[pub])]
        print(f"\n{pub} titles: {len(t)} labelled, {len(dis)} where the regex and Jev disagree on keep/drop")
        for x, s in sorted(dis, key=lambda d: -d[1]["conf"])[:40]:
            print(f"  regex {'drop' if not_table.search(x) else 'keep'} | jev {s['label']:14} {s['conf']:.2f} | {x[:110]}")
        c = load("columns", pub)
        hd = []
        for x, r in c.items():
            rh = head_of(x, heads)
            jh = r["head"]["label"]
            jh = None if jh in ("other_head", "no_head") else jh
            if rh != jh:
                hd.append((x, rh, jh, r["head"]["conf"]))
        print(f"{pub} columns: {len(c)} labelled, {len(hd)} where the head differs")
        for x, rh, jh, cf_ in sorted(hd, key=lambda d: -d[3])[:40]:
            print(f"  regex {str(rh):14} jev {str(jh):14} {cf_:.2f} | {x[:110]}")


def verify(pub: str, not_table, workers: int, key: str) -> None:
    """Ask again, with the options in reverse order, about every title where Jev changes the rules' verdict."""
    labels = load("titles", pub)
    keep_all = table_policy(pub, list(labels), not_table)
    rule = {t: ("drop" if not_table.search(t) else "keep") for t in labels}
    changed = [t for t in labels if keep_all[t] != rule[t]]
    label("titles", pub, changed, workers, key, reverse=True)
    labels = load("titles", pub)
    flip = sum(1 for t in changed if labels[t].get("rev", {}).get("scope", {}).get("label") != labels[t]["scope"]["label"])
    print(f"{pub}: {len(changed)} titles where Jev changes the verdict; {flip} answered differently with the options reversed (rules kept for those)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("what", choices=["label", "compare", "verify"])
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", choices=["titles", "columns"])
    args = ap.parse_args()
    if args.what == "compare":
        return compare()
    key = api_key()
    if args.what == "verify":
        from .longseries import ADSI_NOT_TABLE, NOT_CASES_TABLE
        from .longseries import ADSI_HEADS, IPC_HEADS
        for pub, nt, hs in (("cii", NOT_CASES_TABLE, IPC_HEADS), ("adsi", ADSI_NOT_TABLE, ADSI_HEADS)):
            if path("titles", pub).exists():
                verify(pub, nt, args.workers, key)
            if path("columns", pub).exists():
                verify_columns(pub, hs, args.workers, key)
        return
    for (kind, pub), texts in texts_from_db().items():
        if args.only and kind != args.only:
            continue
        label(kind, pub, texts[: args.limit or None], args.workers, key)



# ------------------------------------------------------------------ used by analysis.longseries
SUBSETS = {"cii": {"children", "sc_st", "senior_citizens", "foreigners", "juveniles", "cyber", "railways", "insurgents",
                   "other_subset"},
           "adsi": {"breakdown"}}
NOT_COUNTS = {"cii": "not_cases", "adsi": "not_deaths"}
SURE = 0.8          # Jev's confidence needed to drop a table the rules keep
VERY_SURE = 0.9     # ... to call it not a count at all, or to take back one the rules drop


def table_policy(pub: str, titles, not_table) -> dict:
    """title -> 'keep', 'drop', 'women' (only the heads of crimes against women) or 'cities' (only rows named as a
    city: the district-and-city tables of the 1970s-80s). Jev decides only where it is sure; otherwise the rules."""
    labels = load("titles", pub)
    out = {}
    for ti in set(titles):
        ti_s = str(ti or "")
        rule_drop = bool(not_table.search(ti_s))
        rec = labels.get(ti_s, {})
        lab = rec.get("scope")
        if lab and "rev" in rec and rec["rev"]["scope"]["label"] != lab["label"]:
            lab = None                  # the answer changed with the order of the options: not sure
        verdict = "drop" if rule_drop else "keep"
        if lab:
            l, c = lab["label"], lab["conf"]
            if l in SUBSETS[pub] and c >= SURE:
                verdict = "drop"
            elif l == NOT_COUNTS[pub] and c >= VERY_SURE:
                verdict = "drop"
            elif l == "women" and c >= SURE:
                verdict = "drop" if rule_drop else "women"
            elif pub == "cii" and l == "all_cases" and c >= VERY_SURE and rule_drop \
                    and re.search(r"district", ti_s, re.I) and re.search(r"city", ti_s, re.I) \
                    and not not_table.search(re.sub(r"district", "", ti_s, flags=re.I)):
                verdict = "cities"
        out[ti] = verdict
    return out



def column_veto(pub: str, columns, head_of_col: dict) -> set:
    """Column headings whose figures are not the head the rules matched: Jev is sure (and gives the same answer with
    its options reversed, where asked) that the heading names another head, or holds rates or counts of victims."""
    labels = load("columns", pub)
    out = set()
    for col in set(columns):
        h = head_of_col.get(col)
        r = labels.get(col)
        if not h or not r:
            continue
        if veto_reason(r, h) and ("rev" not in r or veto_reason({"head": r["rev"]["head"], "kind": r["rev"]["kind"]}, h)):
            out.add(col)
    return out


def veto_reason(r: dict, h: str) -> str | None:
    jh, hc, jk, kc = r["head"]["label"], r["head"]["conf"], r["kind"]["label"], r["kind"]["conf"]
    if jh not in (h, "no_head", "other_head") and hc >= SURE:
        return f"names {jh}"
    if jh == "other_head" and hc >= 0.85:
        return "names another head"
    if jk in ("rate_share", "victims_persons") and kc >= SURE:
        return jk
    return None


def verify_columns(pub: str, heads, workers: int, key: str) -> None:
    """Ask again, options reversed, about every column heading Jev would veto."""
    from .longseries import head_of

    labels = load("columns", pub)
    hoc = {c: head_of(c, heads) for c in labels}
    first = [c for c in labels if hoc[c] and veto_reason(labels[c], hoc[c])]
    label("columns", pub, first, workers, key, reverse=True)
    kept = column_veto(pub, first, hoc)
    print(f"{pub}: {len(first)} column headings Jev would veto; {len(first) - len(kept)} answered differently reversed (kept)")


if __name__ == "__main__":
    main()
