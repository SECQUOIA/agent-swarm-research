#!/usr/bin/env python3
"""Reviewer's own PySCIPOpt runs: fm336 and tiny2 (default and heur+sepa off), seeds; SCIP's own check of the witness."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import json, sys
from fractions import Fraction as F
import pyscipopt
from pyscipopt import Model, SCIP_PARAMSETTING
T = (_PUBLIC_REPO + '/research-20260929/publication/scip-bug/')
print("pyscipopt", pyscipopt.__version__)

def solve(path, seed, hsoff=False, extra=None):
    m = Model(); m.hideOutput(); m.setParam("randomization/randomseedshift", seed)
    m.readProblem(path)
    if hsoff:
        m.setHeuristics(SCIP_PARAMSETTING.OFF); m.setSeparating(SCIP_PARAMSETTING.OFF)
    for k, v in (extra or {}).items():
        m.setParam(k, v)
    m.optimize()
    return m, m.getStatus(), m.getDualbound(), m.getNNodes()

def checkwit(path, wpath):
    m = Model(); m.hideOutput(); m.readProblem(path)
    w = json.load(open(wpath))
    s = m.createSol()
    for v in m.getVars():
        m.setSolVal(s, v, float(F(str(w[v.name]))))
    ok = m.checkSol(s, printreason=True, completely=True, checkbounds=True, checkintegrality=True, checklprows=True, original=True)
    return ok, m.getSolObjVal(s, original=True)

m0 = Model(); print("SCIP", m0.version(), m0.getMajorVersion(), m0.getMinorVersion(), m0.getTechVersion())
for seed in range(10):
    m, st, db, nn = solve(T + "min/fm336_v1010.cip", seed)
    print("fm336 seed %d: %s dual %.15g nodes %d %s" % (seed, st, db, nn, "WRONG" if st == "optimal" and db > 187/270 + 1e-4 else "ok"))
for seed in range(3):
    m, st, db, nn = solve(T + "minimal/tiny2.cip", seed)
    print("tiny2 default seed %d: %s dual %.15g nodes %d" % (seed, st, db, nn))
    m, st, db, nn = solve(T + "minimal/tiny2.cip", seed, hsoff=True)
    print("tiny2 heur+sepa off seed %d: %s dual %.15g nodes %d %s" % (seed, st, db, nn, "WRONG" if st == "optimal" and db > -1.337 + 1e-4 else "ok"))
for mod, wit in [("min/fm336_v1010.cip", "min/fm336_v1010.witness.json"), ("minimal/tiny2.cip", "minimal/tiny2_witness.json"),
                 ("models/p4.cip", "witness/p4.json"), ("models/pair2236.cip", "witness/pair2236.json"),
                 ("min/fm318_master.cip", "min/fm318_master.witness.json")]:
    print("SCIP checkSol witness", mod, checkwit(T + mod, T + wit))
