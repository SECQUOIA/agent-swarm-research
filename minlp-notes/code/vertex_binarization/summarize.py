"""Tabulate a sweep: per (family, n, m, solver), orig vs sob status/time/gap, and objective agreement."""
import json
import sys
from collections import defaultdict

rows = [json.loads(l) for l in open(sys.argv[1])]
by = defaultdict(dict)
for r in rows:
    by[(r["family"], r["n"], r["m"], r["seed"], r["solver"])][r["form"]] = r
best = defaultdict(lambda: float("inf"))
for r in rows:
    if "true_obj" in r:
        k = (r["family"], r["n"], r["m"], r["seed"])
        best[k] = min(best[k], r["true_obj"])

def cell(r, bk):
    if r is None or "time" not in r:
        return "      -      "
    gap = abs(bk - r["dual"]) / max(1e-9, abs(bk))
    flag = "" if r["status"] in ("optimal", "gaplimit") else "*"
    sub = "!" if r.get("true_obj", bk) > bk + 1e-4 * max(1, abs(bk)) else ""
    return f"{r['time']:7.1f}s {100*gap:6.2f}%{flag}{sub}"

print(f"{'family':8} {'n':>4} {'m':>2} {'seed':>4} {'solver':7} | {'orig (time, gap to best)':>24} | {'sob':>24}")
for k in sorted(by):
    bk = best[k[:4]]
    print(f"{k[0]:8} {k[1]:4d} {k[2]:2d} {k[3]:4d} {k[4]:7} | {cell(by[k].get('orig'), bk):>24} | {cell(by[k].get('sob'), bk):>24}")
print("* = limit reached; ! = returned point worse than best known by >1e-4 relative")
