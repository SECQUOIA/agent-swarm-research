"""Recompute, from the audit's results.json, the numbers quoted in the revised audit-report.md
(own code): class counts per (instance, solver) pair, the gross / tolerance-scale split at
1e-6 |d|, the (i) versus (i-r) slack rule, margins d - f and (d - f)/|d|, the margin histogram,
per-solver counts, and closing / solved flags of class (i) pairs."""
import json
import os
from collections import Counter, defaultdict
from decimal import Decimal as D, getcontext

getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "..", "..", "bound-audit", "results.json")))
RANK = ["(i) proven invalid", "(i-r) invalid as listed, within rounding of shown digits", "(iii) undecided",
        "(ii) tolerance effect (proven)", "(ii) tolerance effect"]
SHORT = dict(zip(RANK, ["i", "i-r", "iii", "ii proven", "ii repair"]))
bad = 0
for r in R:  # per-row rule checks
    if r["cls"] in RANK[:2]:
        d, lo, hi = D(r["d_listed"].rstrip(".")), D(r["obj_lo"]), D(r["obj_hi"])
        m = d - hi if r["sense"] == "min" else lo - d
        is_i = m > D(repr(r["d_slack"]))
        gross = m > abs(d) / 10**6
        ok = (is_i == (r["cls"] == RANK[0])) and (not is_i or (r["i_group"] == ("gross" if gross else "tolerance-scale")))
        ok &= abs(float(m) - r["margin_proved"]) <= 1e-9 * max(1, abs(float(m)))
        ok &= abs(float(m / abs(d)) - r["rel_margin"]) <= 1e-9 * abs(float(m / abs(d)))
        bad += not ok
print("rule/margin mismatches in (i)/(i-r) rows:", bad)
per = defaultdict(list)
for r in R:
    per[(r["name"], r["solver"])].append(r)
best = {k: min(v, key=lambda r: (RANK.index(r["cls"]), -r.get("margin_proved", -1e300))) for k, v in per.items()}


def lab(r):
    s = SHORT[r["cls"]]
    return s + " " + r["i_group"] if s == "i" else s


cnt, inst = Counter(), defaultdict(set)
for (n, s), r in best.items():
    cnt[lab(r)] += 1
    inst[lab(r)].add(n)
print("pairs:", len(best), {c: (cnt[c], len(inst[c])) for c in cnt})
bins = [(0, 1e-9), (1e-9, 1e-7), (1e-7, 1e-5), (1e-5, 1e-3), (1e-3, 1e-1), (1e-1, 1e99)]
h = Counter()
for (n, s), r in sorted(best.items()):
    if SHORT[r["cls"]] == "i":
        h[next(b for b in bins if b[0] <= r["rel_margin"] < b[1])] += 1
        print(f"  (i) {n} {s} {r['i_group']}: d={r['d_listed']} d-f={r['margin_proved']:.4g} (d-f)/|d|={r['rel_margin']:.3g} "
              f"margin/slack={r['margin_proved'] / r['d_slack']:.3g} solved={r['solved']} closing={r['closing']}")
print("histogram of (d-f)/|d| over class (i) pairs:", {f"[{a:g},{b:g})": v for (a, b), v in sorted(h.items())})
bys = defaultdict(Counter)
for (n, s), r in best.items():
    bys[s][lab(r)] += 1
for s in sorted(bys):
    print(" ", s, sum(bys[s].values()), dict(bys[s]))
