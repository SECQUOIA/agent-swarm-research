"""Re-examine a certification record whose rbb bound stayed below its SCIP-based
target: SCIP under other settings, and rbb's own LP point at the minimum leaf."""
import sys, pickle
import numpy as np
sys.path.insert(0, "..")
import tasks, period, bundle
from dpcells import CellPlan  # noqa
P = pickle.load(open(sys.argv[1], "rb"))
rid = int(sys.argv[2])
rec = P.crecs[rid]
tasks.init(P.T, "../logs/implied_06.json", True)
D = tasks._W["D"]
t = rec["t"]
box = tasks._box(D, t, rec["cin_box"], rec["cout_box"])
lam = [[0.0] * 3 for _ in range(P.T - 1)]
if t > 0: lam[t - 1] = rec["lam_in"]
if t < P.T - 1: lam[t] = rec["lam_out"]
print("record", rid, "period", t, "target", rec["target"], "rbb bound", rec["bound"])
for name, prm in (("noprop", bundle.NOPROP), ("default", {}), ("noprop feastol1e-9", dict(bundle.NOPROP, **{"numerics/feastol": 1e-9})),
                  ("default seed7", {"randomization/randomseedshift": 7})):
    r = period.solve_window(D, t, t + 1, lam, 0.0, 60, prm, box)
    x = r["x"]
    bins = None if x is None else [int(round(x[v])) for v in D["S"]["per_vars"][t] if D["M"]["vt"][v] == "B"]
    print(f"  SCIP {name}: status {r['status']} primal {r['primal']:.6f} dual {r['dual']:.6f} bins {bins}", flush=True)
