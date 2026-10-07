"""Floating-point cross-check (evidence only, not a proof): SCIP's own OSIL reader
evaluates the stored point (fixed values and box centres rounded to double).

    python3 scip_check.py <name>

SCIP's reader adds two objective helper variables: objconstvar (fixed to the
objective constant) and nlobjvar with the row objcons (nlobjvar = quadratic part
of the objective).  Their values are set from SCIP's own data, so no part of this
check uses osilx or pfmodel.  checkSol is run with feastol 1e-9 on the original
problem, and the objective is evaluated from SCIP's coefficients.
"""
import json
import os
import sys
from fractions import Fraction as Fr

import pyscipopt

HERE = os.path.dirname(os.path.abspath(__file__))
OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")


def main(name):
    P = json.load(open(os.path.join(HERE, "points", f"{name}.json")))
    val = {v: float(Fr(d["value"])) for v, d in P["fixed"].items()}
    val.update({v: float(Fr(s)) for v, s in P["free"].items()})
    m = pyscipopt.Model()
    m.hideOutput()
    m.readProblem(os.path.join(OSIL, f"{name}.osil"))
    m.setParam("numerics/feastol", 1e-9)
    vs = {v.name: v for v in m.getVars()}
    helpers = sorted(set(vs) - set(val))
    assert set(val) <= set(vs) and set(helpers) <= {"objconstvar", "nlobjvar", "objvar"}, helpers
    if "objconstvar" in vs:
        v = vs["objconstvar"]
        assert v.getLbOriginal() == v.getUbOriginal()
        val["objconstvar"] = v.getLbOriginal()
    if "nlobjvar" in vs:
        (oc,) = [c for c in m.getConss() if c.name == "objcons"]
        bil, quad, lin = m.getTermsQuadratic(oc)
        q = sum(a * val[x.name] * val[y.name] for x, y, a in bil)
        q += sum(a2 * val[x.name] ** 2 + a1 * val[x.name] for x, a2, a1 in quad)
        q += sum(a * val[x.name] for x, a in lin if x.name != "nlobjvar")
        coef = [a for x, a in lin if x.name == "nlobjvar"]
        assert coef == [-1.0], coef  # objcons: quad - nlobjvar (<=|=) 0
        val["nlobjvar"] = q
    s = m.createSol()
    for nm, v in vs.items():
        m.setSolVal(s, v, val[nm])
    feas = m.checkSol(s, printreason=True, completely=True, original=True)
    obj = m.getSolObjVal(s, original=True)
    print(f"{name}: SCIP checkSol (feastol 1e-9, original problem) feasible = {feas}; "
          f"SCIP objective at the rounded centre = {obj!r}; helper variables {helpers}")


if __name__ == "__main__":
    main(sys.argv[1])
