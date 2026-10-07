"""Minimal reproducer: SCIP reports a wrong optimal value on a 3-variable MINLP.

    min  0.2 b - 2.4 s + p
    s.t. p = s^3              (cube)
         s - 0.3 b <= 0.7     (speed)
         b in {0,1},  0.7 <= s <= 1,  0.343 <= p <= 1

The point b = 0, s = 0.7, p = 0.343 is exactly feasible (0.7^3 = 0.343) with
objective -1.337, the true optimum (for b = 1 the best value is about
-1.2311).  With primal heuristics and separation switched off, SCIP prunes the
b = 0 branch and reports 'optimal' at -1.2310845.  SCIP's own solution checker
accepts the point with value -1.337.

usage: python3 repro_tiny.py [tiny2.cip]
"""
import os
import sys

import pyscipopt as ps
from pyscipopt import SCIP_PARAMSETTING

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "tiny2.cip")
print("PySCIPOpt", ps.__version__)
ps.Model().printVersion()
sys.stdout.flush()

for label in ("default settings", "heuristics off + separating off"):
    m = ps.Model()
    m.hideOutput()
    m.readProblem(path)
    if label != "default settings":
        m.setHeuristics(SCIP_PARAMSETTING.OFF)
        m.setSeparating(SCIP_PARAMSETTING.OFF)
    m.optimize()
    print(f"{label:35s}: status {m.getStatus()}, dual bound {m.getDualbound()!r}, primal bound {m.getPrimalbound()!r}, "
          f"nodes {m.getNNodes()}")
    # check the known point with SCIP's own checker (original problem)
    sol = m.createOrigSol()
    for v in m.getVars(transformed=False):
        m.setSolVal(sol, v, {"b": 0.0, "s": 0.7, "p": 0.343}[v.name])
    ok = m.checkSol(sol, printreason=True, original=True)
    print(f"{'':35s}  SCIP checkSol(b=0, s=0.7, p=0.343; objective -1.337) -> feasible: {ok}")
    m.freeProb()
