"""Consistency check of a rigorous bound against a tight-tolerance point.

Builds period t of waterno2_T from vbb2's own model data (rows, bounds incl.
logs/my_implied_TT.json, Lagrangian objective at the authors' multipliers),
solves it with SCIP at the given numerics/feastol (SCIP is only a point
generator here), and evaluates the returned point EXACTLY (Fraction): row
and bound violations, integrality, Lagrangian value.
usage: python3 scip_point.py T t time_limit [feastol, default 1e-9]
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import sys
from fractions import Fraction as F

import pyscipopt as ps

import vbb2

W2 = _RESEARCH + "/open-instances-wave2/waterno2/logs/"
T, t, tl = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
feastol = float(sys.argv[4]) if len(sys.argv) > 4 else 1e-9
mult = json.load(open(W2 + f"mult_{T:02d}_w1_impl.json"))
lam = [[float(v) for v in l] for l in mult["lam"]]
P = vbb2.PeriodF(T, t, lam, float(mult["mu"]), json.load(open(f"logs/my_implied_{T:02d}.json")))
M = ps.Model()
M.hideOutput()
M.setParam("numerics/feastol", feastol)
M.setParam("limits/time", tl)
M.setParam("parallel/maxnthreads", 1)
X = []
for j in range(P.n0):
    lo = None if P.lo0[j] == -vbb2.INF else P.lo0[j]
    hi = None if P.hi0[j] == vbb2.INF else P.hi0[j]
    X.append(M.addVar(P.names[j], vtype="B" if P.isbin[j] else "C", lb=lo, ub=hi))
E = list(X)
for (kind, x, y, w) in P.aux:
    E.append(X[x] * X[x] if kind == "sq" else X[x] * X[x] * X[x] if kind == "cube" else X[x] * X[y])
for (cols, cf, L, U, nm) in P.rows:
    e = ps.quicksum(float(a) * E[c] for c, a in zip(cols, cf))
    if L is not None and U is not None and L == U:
        M.addCons(e == float(L), name=nm)
    else:
        if L is not None:
            M.addCons(e >= float(L), name=nm + "_lo")
        if U is not None:
            M.addCons(e <= float(U), name=nm + "_up")
M.setObjective(ps.quicksum(float(P.c[j]) * X[j] for j in range(P.n0) if P.c[j] != 0), "minimize")
M.optimize()
print(f"T={T} period {t}, feastol {feastol}: SCIP status {M.getStatus()}, primal {M.getPrimalbound():.9f}, "
      f"dual {M.getDualbound():.9f} (SCIP bound not trusted)")
s = M.getBestSol()
z = [F(M.getSolVal(s, X[j])) for j in range(P.n0)]
for j in range(P.n0):          # binaries: round (SCIP returns values within 1e-9 of 0/1)
    if P.isbin[j]:
        z[j] = F(round(z[j]))
for (kind, x, y, w) in P.aux:
    z.append(z[x] ** 2 if kind == "sq" else z[x] ** 3 if kind == "cube" else z[x] * z[y])
rv, bv = F(0), F(0)
for (cols, cf, L, U, nm) in P.rows:
    v = sum(a * z[c] for c, a in zip(cols, cf))
    rv = max(rv, (L - v) if L is not None else 0, (v - U) if U is not None else 0)
for j in range(P.n0):
    if P.lo0[j] != -vbb2.INF:
        bv = max(bv, F(P.lo0[j]) - z[j])
    if P.hi0[j] != vbb2.INF:
        bv = max(bv, z[j] - F(P.hi0[j]))
val = sum(P.c[j] * z[j] for j in range(P.n0))
print(f"exact evaluation: Lagrangian value {float(val)!r}, max row violation {float(rv):.3e}, "
      f"max bound violation {float(bv):.3e} (binaries rounded)")
print("pump configuration (binaries):", [int(z[j]) for j in range(P.n0) if P.isbin[j]])
