"""Default-settings reproducer: SCIP reports 'optimal' at 1.198 on a 20-variable
pump model (pumps_default.cip) that has an exactly feasible point of value 0.612.

The point (pumps_default_witness.json, exact rationals) has pumps 0, 1, 2 off and
pump 3 on at speed 0.8.  The script solves the model with default settings for
random seed shifts 0..4, then checks the point with SCIP's own solution checker.
usage: python3 repro_pumps.py [pumps_default.cip]
"""
import json
import os
import sys
from fractions import Fraction

import pyscipopt as ps

here = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "pumps_default.cip")
point = {k: float(Fraction(v)) for k, v in json.load(open(os.path.join(here, "pumps_default_witness.json"))).items()}
print("PySCIPOpt", ps.__version__)
ps.Model().printVersion()
sys.stdout.flush()

for seed in range(5):
    m = ps.Model()
    m.hideOutput()
    m.readProblem(path)
    m.setParam("randomization/randomseedshift", seed)
    m.optimize()
    print(f"seed shift {seed}: status {m.getStatus()}, dual bound {m.getDualbound()!r}, nodes {m.getNNodes()}")
    if seed == 0:
        sol = m.createOrigSol()
        for v in m.getVars(transformed=False):
            m.setSolVal(sol, v, point[v.name])
        ok = m.checkSol(sol, printreason=True, original=True)
        print(f"   SCIP checkSol of the known point (objective {m.getSolObjVal(sol, original=True)!r}): feasible = {ok}")
    m.freeProb()
