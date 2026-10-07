#!/usr/bin/env python3
"""Reviewer: rerun pair2236 seeds 0 and 7 in PySCIPOpt; evaluate SCIP's point exactly (decimal data and binary64 data)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import json, sys
from fractions import Fraction as F
import pyscipopt as ps
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/publication/reviews/scip-bug-r1'))
from rv_cip_exact import parse_cip
T = (_PUBLIC_REPO + '/research-20260929/publication/scip-bug/')
P = T + "models/pair2236.cip"
var, order, cons = parse_cip(P)
wit = json.load(open(T + "witness/pair2236.json"))
print("witness binaries:", {n: wit[n] for n in order if var[n]["type"] == "binary"})
def viol(x, rnd):
    r = (lambda q: F(float(q))) if rnd else (lambda q: q)
    wr, wb = (F(0), None), (F(0), None)
    for cname, kind, terms, rel, rhs in cons:
        a = sum((r(c) * eval_prod(x, ns) for c, ns in terms), F(0))
        rr = r(rhs)
        v = {"<=": a - rr, ">=": rr - a, "==": abs(a - rr)}[rel]
        if v > wr[0]: wr = (v, cname)
    for n in order:
        lb, ub = var[n]["lb"], var[n]["ub"]
        v = max(F(0), (r(lb) - x[n]) if lb is not None else F(0), (x[n] - r(ub)) if ub is not None else F(0))
        if v > wb[0]: wb = (v, n)
    return wr, wb
def eval_prod(x, ns):
    p = F(1)
    for n in ns: p *= x[n]
    return p
for seed in (0, 7):
    m = ps.Model(); m.hideOutput(); m.readProblem(P); m.setParam("randomization/randomseedshift", seed); m.optimize()
    s = m.getBestSol()
    x = {v.name: F(m.getSolVal(s, v)) for v in m.getVars()}
    obj = sum((var[n]["obj"] * x[n] for n in order), F(0))
    print("seed %d: %s dual %r nodes %d; exact objective of SCIP point %.12g" % (seed, m.getStatus(), m.getDualbound(), m.getNNodes(), float(obj)))
    print("   binaries:", {n: int(round(float(x[n]))) for n in order if var[n]["type"] == "binary"})
    for rnd in (False, True):
        (vr, cr), (vb, nb) = viol(x, rnd)
        print("   %s data: max row violation %.3e (%s), max bound violation %.3e (%s)" % ("binary64" if rnd else "decimal", float(vr), cr, float(vb), nb))
# witness under binary64 data
xw = {n: F(str(wit[n])) for n in order}
(vr, cr), (vb, nb) = viol(xw, True)
print("witness under binary64 data: max row violation %.3e (%s), max bound violation %.3e (%s)" % (float(vr), cr, float(vb), nb))
