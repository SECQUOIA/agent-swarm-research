"""SCIP's own feasibility check of the witness points (rounded to doubles).

Not part of the proof (the proof is exact_check.py).  It shows that SCIP itself
accepts, within its tolerances, the points that its 'optimal' claims exclude.
usage: python3 checksol_witness.py      (prints logs/checksol_witness.log content)
"""
import json
from fractions import Fraction as F

import pyscipopt as ps

CASES = {"p0": ("models/p0.cip", "witness/p0.json"), "p4": ("models/p4.cip", "witness/p4.json"),
         "p5": ("models/p5.cip", "witness/p5.json"), "pair2236": ("models/pair2236.cip", "witness/pair2236.json"),
         "tiny2": ("minimal/tiny2.cip", "minimal/tiny2_witness.json"),
         "pumps_default": ("minimal/pumps_default.cip", "minimal/pumps_default_witness.json")}

for key, (path, wpath) in CASES.items():
    w = {k: float(F(v)) for k, v in json.load(open(wpath)).items()}
    m = ps.Model()
    m.hideOutput()
    m.readProblem(path)
    sol = m.createOrigSol()
    for v in m.getVars(transformed=False):
        m.setSolVal(sol, v, w[v.name])
    ok = m.checkSol(sol, printreason=True, completely=True, original=True)
    print(f"{key}: SCIP 10.0.2 checkSol (original problem, default tolerances): feasible = {ok}; "
          f"objective {m.getSolObjVal(sol, original=True)!r}")
    m.freeProb()
