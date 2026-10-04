"""Checks on what /explore/ shows, run after every rebuild: the problems a reader notices first.

    uv run python -m analysis.audit            # prints counts and examples; exit code 1 if a hard check fails

Hard checks (must be zero): titles with page headers, markup or table labels; titles in capitals; families with no
geography; two families with the same title in one picker; placeholder categories ('col_3', a bare year).
Soft checks (reported): families whose categories cover disjoint years, families thinner than three years of data.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict

from .lib import ROOT

EXPLORE = ROOT / "web" / "data" / "explore"
JUNK = re.compile(r"N\.\s?C\.\s?R\.\s?B|CRIME IN INDIA|\$|\^\{|##|\bTABLE\b|^\s*Table\s*[-–—]?\s*[IVX\d]|\b156_3\b|\s(at the end of|over|during)$")


def caps(t: str) -> bool:
    words = [w for w in re.findall(r"[A-Za-z]{4,}", t)]
    return bool(words) and sum(w.isupper() for w in words) / len(words) > 0.5


def main() -> int:
    idx = json.loads((EXPLORE / "index.json").read_text())
    fams = idx["families"]
    hard, soft = defaultdict(list), defaultdict(list)
    seen = Counter((f["pub"], f["topic"], f["geo"], f["title"]) for f in fams)
    for f in fams:
        t = f["title"]
        if JUNK.search(t):
            hard["junk title"].append(t)
        if caps(t):
            hard["title in capitals"].append(t)
        if not f["geo"]:
            hard["no geography"].append(t)
        if seen[(f["pub"], f["topic"], f["geo"], t)] > 1:
            hard["same title twice in one picker"].append(f"{f['topic']}: {t}")
        p = EXPLORE / f["pub"] / f"{f['id']}.json"
        if not p.exists():
            hard["missing file"].append(f["id"])
            continue
        d = json.loads(p.read_text())
        for c in d["cats"]:
            if re.fullmatch(r"\s*(col_?\d+|(19|20)\d\d)\s*", c["name"]):
                hard["placeholder category"].append(f"{t}: {c['name']}")
        # years of each category (any row, any breakdown)
        span = defaultdict(set)
        for k, a in d["d"].items():
            span[int(k.split(".")[1])].update(a[::2])
        years = set(d["years"])
        if span and years:
            best = max(len(s) for s in span.values()) / len(years)
            if best < 0.6:
                soft["no category covers 60% of the years"].append(f"{t} ({min(years)}-{max(years)})")
        if len(years) < 3:
            soft["fewer than 3 years"].append(t)
    print(f"{len(fams)} families")
    for name, xs in list(hard.items()) + list(soft.items()):
        kind = "HARD" if name in hard else "soft"
        print(f"  {kind} {name}: {len(set(xs))}" + "".join(f"\n      {x[:120]}" for x in sorted(set(xs))[:8]))
    return 1 if any(hard.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
