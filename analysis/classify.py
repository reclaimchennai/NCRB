"""Label table titles and column headings with a language model, as a second opinion on the regex rules.

The model only labels text: what a table counts (every case, or only a group's), and which crime head a column
heading is and whether it is that head's count of cases. It never sees or writes a figure, so it cannot invent
data; every figure still comes from the printed tables and must pass the same checks. Labels are kept in
data/classify/*.json (key: the exact text), with the model that gave them, so they can be audited and are reused.

Where the model and the regex rules disagree, a stronger model decides (`--arbiter`), shown both readings.

    NCRB_ENV_FILE=../assembly/.../.env uv run --with anthropic python -m analysis.classify
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
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "classify"
MODEL = "claude-sonnet-5-5"
ARBITER = "claude-opus-5-5"

SCOPES = {
    "all": "counts every case (or death, or prisoner) of its kind in each place listed: e.g. 'Incidence & Rate of "
           "Cognizable Crimes (IPC) under different crime heads', 'IPC Crimes (Crime Head-wise & City-wise)', "
           "'Comparative incidence ...', 'Murder cases (City-wise) 2014-2016', 'Suicides in States', "
           "'Accidental deaths by States'. A table of one crime head for all places is 'all'.",
    "group": "counts only the cases against or by one group or agency, a subset of all cases: crimes against women, "
             "children, Scheduled Castes/Tribes, senior citizens, foreigners; crimes by juveniles, foreigners, "
             "insurgents, extremists; cases of the railway police (GRP); cyber crimes; crimes in one district list "
             "of one State; one cause, means, profession, age group or sex of suicides or accidents.",
    "other": "not counts of cases registered/deaths: arrests, persons, victims, accused, disposal by police or "
             "courts, pending, conviction, property stolen/recovered, value, motives, police strength, rates or "
             "percentages only, budget, jail capacity, or anything else.",
}
HEADS = {
    "cii": ["total", "murder", "attempt_murder", "chna", "rape", "kidnapping", "dacoity", "robbery", "burglary", "theft",
            "riots", "cbt", "cheating", "counterfeiting", "arson", "hurt", "dowry_deaths", "molestation", "cruelty"],
    "adsi": ["suicides", "accidental", "road"],
}
HEAD_HELP = {
    "total": "total cognizable crimes under the IPC (or IPC/BNS); NOT the IPC+SLL total, NOT special & local laws",
    "murder": "murder (Sec. 302 IPC / 103 BNS) as a whole; not attempt, not culpable homicide, not murder with rape, "
              "not kidnapping for murder, not dowry",
    "attempt_murder": "attempt to commit murder", "chna": "culpable homicide not amounting to murder",
    "rape": "rape as a whole (Sec. 376); not attempt to rape, not custodial or gang rape alone",
    "kidnapping": "kidnapping & abduction as a whole (all victims)", "dacoity": "dacoity (not preparation/assembly)",
    "robbery": "robbery (not dacoity, not 'loot (robbery & dacoity)')", "burglary": "burglary / house-breaking",
    "theft": "theft as a whole (not auto theft or other theft alone)", "riots": "riots as a whole",
    "cbt": "criminal breach of trust", "cheating": "cheating", "counterfeiting": "counterfeiting as a whole",
    "arson": "arson", "hurt": "hurt as a whole (simple + grievous); not grievous or simple alone, not hurt by rash driving",
    "dowry_deaths": "dowry deaths", "molestation": "assault on women with intent to outrage her modesty",
    "cruelty": "cruelty by husband or his relatives",
    "suicides": "number of suicides (persons who died by suicide)",
    "accidental": "number of accidental deaths (all causes; or 'unnatural causes' total of accidental deaths)",
    "road": "deaths in road accidents",
}
KINDS = {
    "cases": "the head's number of cases registered / incidence / reported (or deaths, for suicides and accidents), "
             "for all of it (a 'Total' of the head counts as all of it)",
    "part": "only a part of the head: a sub-category or section, one sex, the IPC half or the BNS half of 2024, "
            "attempt only, one kind of victim",
    "other": "not a count of cases: victims, persons, rate, percentage, share, rank, variation, arrests, "
             "charge-sheets, disposal, value, or a population",
}

_lock = threading.Lock()


def api_key() -> str:
    """ANTHROPIC_API_KEY from the environment, else from the .env file NCRB_ENV_FILE names (never printed)."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return os.environ["ANTHROPIC_API_KEY"]
    path = os.environ.get("NCRB_ENV_FILE")
    if path and Path(path).expanduser().exists():
        for line in Path(path).expanduser().read_text().splitlines():
            m = re.match(r"\s*ANTHROPIC_API_KEY\s*=\s*['\"]?([^'\"\s]+)", line)
            if m:
                return m.group(1)
    sys.exit("no ANTHROPIC_API_KEY (set it, or NCRB_ENV_FILE to a .env file that has it)")


def load(name: str) -> dict:
    p = OUT / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else {}


def save(name: str, d: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / f"{name}.json.tmp"
    tmp.write_text(json.dumps(dict(sorted(d.items())), ensure_ascii=False, indent=0))
    tmp.replace(OUT / f"{name}.json")


def ask(client, model: str, system: str, items: list[str], check, tries: int = 4) -> list[dict]:
    """One batch: the model returns a JSON list with one object per item, in order; anything malformed is retried."""
    body = "\n".join(f"{i}. {json.dumps(x, ensure_ascii=False)}" for i, x in enumerate(items))
    msg = f"Label each of these {len(items)} items. Reply with only a JSON array of {len(items)} objects, in order, each with \"i\".\n\n{body}"
    for t in range(tries):
        try:
            r = client.messages.create(model=model, max_tokens=16000, temperature=0, system=system,
                                       messages=[{"role": "user", "content": msg}])
            text = "".join(b.text for b in r.content if b.type == "text")
            arr = json.loads(text[text.index("["): text.rindex("]") + 1])
            if len(arr) != len(items) or any(int(a.get("i", -1)) != i for i, a in enumerate(arr)) or not all(check(a) for a in arr):
                raise ValueError("labels do not match the items")
            return arr
        except Exception as e:
            print(f"  retry {t + 1}: {type(e).__name__}: {str(e)[:120]}", flush=True)
            time.sleep(3 * (t + 1))
    return []


def title_system() -> str:
    return ("You classify table titles from India's National Crime Records Bureau (Crime in India, Accidental Deaths & "
            "Suicides in India). Titles can be OCR-garbled; judge from what is readable. For each title give \"scope\", "
            "one of:\n" + "\n".join(f"- {k}: {v}" for k, v in SCOPES.items()) +
            "\nIf a title is unreadable or empty, use \"other\". Do not guess beyond the words given.")


def column_system(pub: str) -> str:
    hs = HEADS[pub]
    return ("You classify column headings of tables from India's National Crime Records Bureau. A heading joins its "
            "parent headings with ' | '; numbers in brackets are column numbers; single letters at the end mean I = "
            "incidence (cases), V = victims, R = rate. Headings can be OCR-garbled. For each heading give \"head\": one "
            "of " + ", ".join(hs) + ", or \"none\" when the heading is not one of these heads; and \"kind\": one of\n" +
            "\n".join(f"- {k}: {v}" for k, v in KINDS.items()) +
            "\nThe heads:\n" + "\n".join(f"- {h}: {HEAD_HELP[h]}" for h in hs) +
            "\nA heading that is only a year, 'Total', 'Incidence' or 'Cases' (no head named) is head \"none\", kind \"cases\". "
            "Use only the words given; when unsure, \"none\".")


def run(name: str, items: list[str], system: str, check, model: str, batch: int, workers: int) -> dict:
    import anthropic

    client = anthropic.Anthropic(api_key=api_key())
    done = load(name)
    todo = [x for x in items if x not in done]
    print(f"{name}: {len(items) - len(todo)} labelled, {len(todo)} to go ({model})", flush=True)
    batches = [todo[i:i + batch] for i in range(0, len(todo), batch)]

    def one(b):
        arr = ask(client, model, system, b, check)
        with _lock:
            for x, a in zip(b, arr):
                done[x] = {k: v for k, v in a.items() if k != "i"} | {"model": model}
        return len(arr)

    n = 0
    with cf.ThreadPoolExecutor(workers) as ex:
        for k, got in enumerate(ex.map(one, batches), 1):
            n += got
            if k % 10 == 0 or k == len(batches):
                with _lock:
                    save(name, done)
                print(f"  {n}/{len(todo)}", flush=True)
    save(name, done)
    return done


def items_from_db() -> tuple[dict, dict]:
    import duckdb

    con = duckdb.connect(str(ROOT / "data" / "web" / "ncrb.duckdb"), read_only=True)
    titles = {pub: [t for (t,) in con.execute("SELECT DISTINCT title FROM tables WHERE publication = ? AND title IS NOT NULL "
                                              "AND n_cells > 0", [pub]).fetchall() if t.strip()] for pub in ("cii", "adsi")}
    kw = {"cii": r"murd|homicide|rape|kidnap|abduct|dacoit|robber|burglar|house.?break|theft|riot|breach of trust|cheat|"
                 r"counterfeit|arson|hurt|dowry|modesty|molest|cruelty|total|cogni[sz]able|ipc|bns",
          "adsi": r"suicid|accident|death|died|killed|total|unnatural"}
    cols = {}
    for pub in ("cii", "adsi"):
        cs = [c for (c,) in con.execute('SELECT DISTINCT c."column" FROM cells c JOIN tables t USING (table_id) '
                                        'WHERE t.publication = ? AND c."column" IS NOT NULL', [pub]).fetchall()]
        cols[pub] = [c for c in cs if re.search(kw[pub], c, re.I)]
    return titles, cols


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--batch", type=int, default=120)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0, help="only the first N items of each list (a trial)")
    args = ap.parse_args()
    titles, cols = items_from_db()
    for pub in ("cii", "adsi"):
        t = sorted(titles[pub])[: args.limit or None]
        run(f"titles-{pub}", t, title_system(), lambda a: a.get("scope") in SCOPES, args.model, args.batch, args.workers)
        c = sorted(cols[pub])[: args.limit or None]
        hs = set(HEADS[pub]) | {"none"}
        run(f"columns-{pub}", c, column_system(pub), lambda a, hs=hs: a.get("head") in hs and a.get("kind") in KINDS,
            args.model, args.batch, args.workers)


if __name__ == "__main__":
    main()
