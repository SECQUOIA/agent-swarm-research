"""SCIP node counts on the path family (same model as research-20260929/scratch/probe3.py).

Usage: python3 scip_runs.py kappa cmode absgap timelimit n1 n2 ... [noprop]   (cmode: zero | seed0 | seed1)
With the last argument "noprop": presolving off, all propagators off (maxrounds 0), OBBT off.
With the last argument "nominor": SCIP's minor separator (PSD cuts on 2x2 principal minors) off.
"""
import sys
import time
import numpy as np
from pyscipopt import Model, quicksum


def build(n, cmode, kappa, b=0.8):
    c = np.zeros(n) if cmode == "zero" else np.random.default_rng(int(cmode[4:])).uniform(-0.3, 0.3, n)
    m = Model()
    m.hideOutput()
    x = [m.addVar(lb=-1, ub=1, name=f"x{i}") for i in range(n)]
    ts = []
    for i in range(n):
        ti = m.addVar(lb=None, name=f"t{i}")
        expr = x[i] * x[i] - kappa * x[i] ** 4
        if i < n - 1:
            expr = expr + b * x[i] * x[i + 1]
        m.addCons(ti >= expr)
        ts.append(ti)
    m.setObjective(quicksum(ts) + quicksum(float(c[i]) * x[i] for i in range(n)), "minimize")
    return m


def main():
    kappa, cmode, eps, tl = float(sys.argv[1]), sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    noprop = sys.argv[-1] == "noprop"
    nominor = sys.argv[-1] == "nominor"
    for n in [int(a) for a in sys.argv[5:] if a not in ("noprop", "nominor")]:
        m = build(n, cmode, kappa)
        m.setParam("limits/time", tl)
        m.setParam("limits/absgap", eps)
        m.setParam("limits/gap", 0.0)
        m.setParam("parallel/maxnthreads", 1)
        if noprop:
            from pyscipopt import SCIP_PARAMSETTING
            m.setPresolve(SCIP_PARAMSETTING.OFF)
            m.setParam("propagating/maxrounds", 0)
            m.setParam("propagating/maxroundsroot", 0)
            m.setParam("propagating/obbt/freq", -1)
        if nominor:
            m.setParam("separating/minor/freq", -1)
        t0 = time.time()
        m.optimize()
        print(f"scip{'-noprop' if noprop else ''}{'-nominor' if nominor else ''} kappa={kappa} {cmode} absgap={eps:.0e} n={n} nodes={m.getNNodes()} {m.getStatus()} "
              f"t={time.time()-t0:.1f}s primal={m.getPrimalbound():.8f} dual={m.getDualbound():.8f}", flush=True)


if __name__ == "__main__":
    main()
