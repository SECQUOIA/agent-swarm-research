"""Tabulate nuclear bounds and solver runs (reads ../nuclear_cw_bounds.json and ../nuclear_runs/*.json).

The proven-bound column is the exact certified objective bound -best_bound_exact rounded down to six
decimals, so the printed value is still a valid lower bound on the objective."""
import json, glob, os
from fractions import Fraction as F
from nuc_verify import dec
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
B = {r["name"]: r for r in json.load(open("nuclear_cw_bounds.json"))}
R = {}
for f in glob.glob("nuclear_runs/*.json"):
    d = json.load(open(f)); R[(d["name"], d["solver"], d["cuts"])] = d
def fm(v): return "none" if v is None or abs(v) >= 1e19 or v != v else (f"{v:.5f}" if abs(v) < 100 else f"{v:.3g}")
def gap(p, d):
    return "inf" if p is None or d is None or abs(d) >= 1e19 else f"{abs(p-d)/min(abs(p),abs(d)):.3g}"
print("| instance | listed primal | listed dual | listed gap | proven bound | gap (listed primal, proven bound) | Gurobi dual: no cuts / cuts | SCIP dual: no cuts / cuts | best primal in these runs (max row viol) |")
print("|---|---|---|---|---|---|---|---|---|")
for nm, b in B.items():
    p, d = b["listed_primal"], b["listed_dual"]
    pb = dec(-F(b["best_bound_exact"]), 6, False)
    runs = [R[(nm, s, c)] for s in ("gurobi", "scip") for c in (0, 1) if (nm, s, c) in R and R[(nm, s, c)]["primal"] is not None]
    best = min(runs, key=lambda r: r["primal"]) if runs else None
    g = lambda s, c: fm(R[(nm, s, c)]["dual"]) if (nm, s, c) in R else "?"
    bp = f"{fm(best['primal'])} ({best['max_row_viol']:.1e})" if best else "none"
    print(f"| {nm} | {fm(p)} | {fm(d)} | {gap(p, d)} | {pb} | {gap(p, -b['best_bound'])} | {g('gurobi',0)} / {g('gurobi',1)} | {g('scip',0)} / {g('scip',1)} | {bp} |")
