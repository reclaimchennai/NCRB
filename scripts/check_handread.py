"""Check a hand-read table: every row's categories add up to its Total, and every column's places add up to the
printed section totals (and States + UTs to the Grand Total). Prints every mismatch; exit 1 if any."""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("t", sys.argv[1]); t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
bad = 0
n = len(t.CATS) - 1
if getattr(t, "CHECK", "sum") == "columns":
    # a table of separate measures (road accidents, persons injured, persons killed): each column adds to the totals
    for sec, rows in t.ROWS.items():
        tot = [k for k in rows if k.upper().startswith("TOTAL")]
        if not tot:
            continue
        places = [v for k, v in rows.items() if k not in tot]
        for j, c in enumerate(t.CATS):
            if rows[tot[0]][j] is None:
                continue
            s_ = sum((v[j] or 0) for v in places)
            if s_ != rows[tot[0]][j]:
                print(f"col  {sec}/{c}: places add to {s_}, {tot[0]} printed {rows[tot[0]][j]}"); bad += 1
    if "Grand" in t.ROWS:
        g = t.ROWS["Grand"]["GRAND TOTAL"]
        st = next((v for k, v in t.ROWS.get("States", {}).items() if k.upper().startswith("TOTAL")), None)
        ut = next((v for k, v in t.ROWS.get("U.Ts.", {}).items() if k.upper().startswith("TOTAL")), None)
        if st and ut:
            for j, c in enumerate(t.CATS):
                if None not in (g[j], st[j], ut[j]) and st[j] + ut[j] != g[j]:
                    print(f"grand {c}: States + UTs = {st[j] + ut[j]}, Grand Total printed {g[j]}"); bad += 1
    print(f"{sum(len(r) for r in t.ROWS.values())} rows checked, {bad} mismatches")
    sys.exit(1 if bad else 0)
if getattr(t, "CHECK", "sum") == "incidence":
    # an incidence table: CATS = [count, population (lakh), rate]; counts add up to the section totals, and every
    # printed rate is count / population (to the printed decimal)
    for sec, rows in t.ROWS.items():
        tot = [k for k in rows if k.upper().startswith("TOTAL")]
        places = {k: v for k, v in rows.items() if k not in tot and not k.upper().startswith("GRAND")}
        if tot and rows[tot[0]][0] is not None:
            s_ = sum(v[0] or 0 for v in places.values())
            if s_ != rows[tot[0]][0]:
                print(f"col  {sec}/{t.CATS[0]}: places add to {s_}, {tot[0]} printed {rows[tot[0]][0]}"); bad += 1
        for k, v in rows.items():
            c, pop, rate = (v + [None, None, None])[:3]
            if None not in (c, pop, rate) and pop > 0 and abs(c / pop - rate) > 0.06 + 0.01 * rate:
                print(f"rate {sec}/{k}: {c}/{pop} = {c / pop:.2f}, printed {rate}"); bad += 1
    if "Grand" in t.ROWS:
        g = t.ROWS["Grand"]["GRAND TOTAL"][0]
        parts = [next((v[0] for k, v in t.ROWS[sec].items() if k.upper().startswith("TOTAL")), None) for sec in ("States", "U.Ts.") if sec in t.ROWS]
        if g is not None and None not in parts and sum(parts) != g:
            print(f"grand: States + UTs = {sum(parts)}, Grand Total printed {g}"); bad += 1
    print(f"{sum(len(r) for r in t.ROWS.values())} rows checked, {bad} mismatches")
    sys.exit(1 if bad else 0)
z = lambda v: [x or 0 for x in v]          # N.A. (None) counts as 0 in the sums
for sec, rows in t.ROWS.items():
    rows = {k: z(v) for k, v in rows.items()}
    for name, v in rows.items():
        if sum(v[:n]) != v[n]:
            print(f"row  {sec}/{name}: categories add to {sum(v[:n])}, Total printed {v[n]}"); bad += 1
    tot = [k for k in rows if k.upper().startswith("TOTAL")]
    if tot:
        places = [v for k, v in rows.items() if k not in tot]
        for j, c in enumerate(t.CATS):
            s = sum(v[j] for v in places)
            if s != rows[tot[0]][j]:
                print(f"col  {sec}/{c}: places add to {s}, {tot[0]} printed {rows[tot[0]][j]}"); bad += 1
if "Grand" in t.ROWS:
    g = z(t.ROWS["Grand"]["GRAND TOTAL"])
    st = z(t.ROWS["States"]["TOTAL (STATES)"]); ut = z(next(v for k, v in t.ROWS["U.Ts."].items() if k.startswith("TOTAL")))
    for j, c in enumerate(t.CATS):
        if st[j] + ut[j] != g[j]:
            print(f"grand {c}: States + UTs = {st[j] + ut[j]}, Grand Total printed {g[j]}"); bad += 1
print(f"{sum(len(r) for r in t.ROWS.values())} rows checked, {bad} mismatches")
sys.exit(1 if bad else 0)
