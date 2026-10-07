"""Re-evaluate the 0039p tight-run leaves with all angle-row multipliers set to 0 (exact)."""
import json, sys
from fractions import Fraction as Fr
sys.path.insert(0, "/tmp/pfdossier/code")
import pf_model as pm, leafcut as lc
from my_eval import node_rows, certify, dec
name, tag = "powerflow0039p", "bb3t"
M = pm.decode(name); info = lc.leaf_info(M)
D = json.load(open(f"/tmp/pfdossier/data/{name}.{tag}.json"))
mins = []
for Lf in D["leaves"]:
    box = tuple((Fr(a), Fr(c)) for a, c in Lf["box"])
    yb, rows = node_rows(M, info, box)
    raw = [("ineq", None, None) if r["kind"] == "angle" else rv for r, rv in zip(rows, Lf["raw"])]
    amax = max(max(abs(rv[1] or 0), abs(rv[2] or 0)) for r, rv in zip(rows, Lf["raw"]) if r["kind"] == "angle")
    b, eps, stats, vm2 = certify(M, rows, yb, raw)
    mins.append(b)
    print(f"  box {[[float(a), float(c)] for a, c in box]}: largest angle multiplier {amax:.3g}; without angle rows eps {eps}, bound {dec(b)} (stored {dec(Fr(Lf['bound']))})", flush=True)
print("min over leaves without angle rows:", dec(min(mins), 14), ">= 41869.05148485014:", min(mins) >= Fr("41869.05148485014"))
