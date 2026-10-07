"""Diagnose SCIP's wrong 'optimal' claims (see scip_check.py).

For a period t and a SCIP setting:
  (a) solve; afterwards compare the cheaper point x* (logs/cheap_point_p{t}.json)
      with the GLOBAL bounds of the transformed variables; a global bound that
      excludes x* by more than 1e-6 is an invalid reduction (x* has a better
      objective value than any cutoff SCIP could have used);
  (b) solve again with x* handed to SCIP as a starting solution and report
      whether SCIP accepts it and the final status/bounds.
usage: python3 scip_diag.py t setting [setting ...]
"""
import json
import sys

import pyscipopt as ps

import scip_check as sc


def load_point(t):
    import os
    d = json.load(open(os.environ.get("WV_POINT", f"logs/cheap_point_p{t}.json")))
    idx = {sc.m["names"][v]: v for v in sc.I["per_vars"][t]}
    return {idx[n]: float(s) for n, s in d.items()}


def run(t, name):
    cfg = sc.SETTINGS[name]
    x = load_point(t)
    M, X, obj = sc.build(t, dict(cfg.get("params", {}), **{"limits/time": 300}), cfg.get("emphasis"),
                         cfg.get("presolve_off", False), cfg.get("heur_off", False))
    vstar = float(sum(a * sc.F(x[v]) for v, a in obj.items()))
    M.optimize()
    st, db = M.getStatus(), M.getDualbound()
    viol = []
    for v, var in X.items():
        tv = M.getTransformedVar(var)
        lb, ub = tv.getLbGlobal(), tv.getUbGlobal()
        if x[v] < lb - 1e-6 or x[v] > ub + 1e-6:
            viol.append((sc.m["names"][v], x[v], lb, ub, str(tv.getStatus()) if hasattr(tv, "getStatus") else ""))
    print(f"period {t} setting {name}: status {st} dual {db:.6f}; value of x* {vstar:.6f}; "
          f"global bounds of transformed vars excluding x*: {len(viol)}", flush=True)
    for r in viol[:15]:
        print("    ", r)
    M.freeProb()
    # (b) x* as a starting solution
    M, X, obj = sc.build(t, dict(cfg.get("params", {}), **{"limits/time": 300}), cfg.get("emphasis"),
                         cfg.get("presolve_off", False), cfg.get("heur_off", False))
    s = M.createSol()
    for v, var in X.items():
        M.setSolVal(s, var, x[v])
    acc = M.addSol(s, free=True)
    M.optimize()
    print(f"    with x* as start solution: accepted {acc}; status {M.getStatus()} primal {M.getPrimalbound():.6f} "
          f"dual {M.getDualbound():.6f}", flush=True)
    M.freeProb()


if __name__ == "__main__":
    t = int(sys.argv[1])
    for name in sys.argv[2:]:
        run(t, name)
