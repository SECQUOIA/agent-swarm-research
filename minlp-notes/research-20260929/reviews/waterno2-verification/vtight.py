"""Nearly feasible points of period subproblems at the certificate multipliers
(SCIP, feastol 1e-9, pump configuration fixed to BARON's), saved for exact repair.
usage: WV_MULT=mult.json python3 vtight.py t b1,b2,...,b9"""
import json, sys
import scip_check as sc
t = int(sys.argv[1])
conf = [int(c) for c in sys.argv[2].split(",")]
M, X, obj = sc.build(t, {"numerics/feastol": 1e-9, "limits/time": 300})
for v, b in zip(sc.bins(t), conf):
    M.fixVar(X[v], b)
M.optimize()
s = M.getBestSol()
x = {v: M.getSolVal(s, X[v]) for v in X}
print(f"period {t} config {conf}: {M.getStatus()} value {M.getPrimalbound():.9f}")
json.dump({sc.m["names"][v]: repr(val) for v, val in x.items()}, open(f"logs/cert_point_p{t}.json", "w"))
