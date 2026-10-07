"""Where does SCIP (default settings) cut off the cheaper point x* of period t?
Checks the global bounds of the transformed problem against x* after presolve
and after node limits 1, 2, 5, 20, 100, ... (x* is better than any incumbent SCIP
has at that time, so no valid reduction may exclude it).
usage: python3 scip_diag2.py t setting"""
import sys
import scip_check as sc
from scip_diag import load_point

t, name = int(sys.argv[1]), sys.argv[2]
cfg = sc.SETTINGS[name]
x = load_point(t)


def check(M, X, label):
    viol = []
    for v, var in X.items():
        tv = M.getTransformedVar(var)
        lb, ub = tv.getLbGlobal(), tv.getUbGlobal()
        if x[v] < lb - 1e-6 or x[v] > ub + 1e-6:
            viol.append((sc.m["names"][v], round(x[v], 9), lb, ub))
    inc = M.getPrimalbound() if M.getNSols() else None
    print(f"{label}: stage {M.getStage()} incumbent {inc} dual {M.getDualbound():.6f} "
          f"x* excluded by {len(viol)} global bounds {viol[:8]}", flush=True)


for lim in [None, 1, 2, 3, 5, 10, 20, 50, 100, 200, 400, 820]:
    M, X, obj = sc.build(t, dict(cfg.get("params", {}), **{"limits/time": 300}), cfg.get("emphasis"),
                         cfg.get("presolve_off", False), cfg.get("heur_off", False))
    if lim is None:
        M.presolve()
        check(M, X, "after presolve")
    else:
        M.setParam("limits/nodes", lim)
        M.optimize()
        check(M, X, f"node limit {lim} (status {M.getStatus()}, nodes {M.getNNodes()})")
    M.freeProb()
