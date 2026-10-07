"""Seed-dependent case (models/pair2236.cip): which pump binaries do SCIP's two
kinds of 'optimal' solutions use, and are they exactly feasible for the data
rounded to binary64?

For seed shifts 0 (claim 55.69) and 7 (claim 65.12) the script solves the
model with PySCIPOpt (default settings otherwise), prints the claim, the
binaries, and the largest row and bound violation of SCIP's point, evaluated
in exact rational arithmetic with every coefficient, side and bound first
rounded to the nearest double (indep_check.parse reads the file).
usage: python3 pair_semantics.py
"""
import os
from fractions import Fraction

import pyscipopt as ps

import indep_check as ic

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "models", "pair2236.cip")
V, R = ic.parse(PATH)


def d(q):
    return Fraction(float(q))  # nearest double, as an exact rational


for seed in (0, 7):
    m = ps.Model()
    m.hideOutput()
    m.readProblem(PATH)
    m.setParam("randomization/randomseedshift", seed)
    m.optimize()
    s = m.getBestSol()
    x = {v.name: Fraction(m.getSolVal(s, v)) for v in m.getVars()}
    worst_row = (Fraction(0), None)
    for name, terms, sense, rhs in R:
        val = Fraction(0)
        for c, names in terms:
            t = d(c)
            for n in names:
                t *= x[n]
            val += t
        r = d(rhs)
        viol = abs(val - r) if sense == "==" else max(Fraction(0), (r - val) if sense == ">=" else (val - r))
        if viol > worst_row[0]:
            worst_row = (viol, name)
    worst_bnd = (Fraction(0), None)
    for n, (kind, obj, lb, ub) in V.items():
        v = max(Fraction(0), d(lb) - x[n] if lb is not None else Fraction(0), x[n] - d(ub) if ub is not None else Fraction(0))
        if v > worst_bnd[0]:
            worst_bnd = (v, n)
    bins = {n: int(round(float(x[n]))) for n, (kind, *_r) in V.items() if kind == "binary"}
    print(f"seed {seed}: status {m.getStatus()}, claimed optimum {m.getDualbound()!r}, nodes {m.getNNodes()}")
    print(f"   binaries: {bins}")
    print(f"   binary64 data, exact arithmetic: max row violation {float(worst_row[0]):.3e} ({worst_row[1]}), "
          f"max bound violation {float(worst_bnd[0]):.3e} ({worst_bnd[1]})")
    m.freeProb()
