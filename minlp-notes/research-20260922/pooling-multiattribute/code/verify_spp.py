"""Check the rebuilt spp network against a MINLPLib solution file: the solution must be feasible
for the rebuilt nonconvex pq model and reproduce the objective value."""
from pathlib import Path as _CleanupPath
_NOTES_ROOT = _CleanupPath(__file__).resolve().parent.joinpath('../../..').resolve()

import sys
sys.path.insert(0, (str(_NOTES_ROOT) + '/research-20260922/scouting/minlplib-open-data'))
import osil, spp, instance as I
import gurobipy as gp

osil_path, sol_path = sys.argv[1], sys.argv[2]
d = osil.read(osil_path); names = d["names"]
sol = {}
for line in open(sol_path):
    a = line.split()
    if len(a) == 2: sol[a[0]] = float(a[1])
P = spp.SppInst(osil_path)
m, q, y, z, v = I.build_pq(P)
# map rebuilt variables to osil indices through the structure recorded in SppInst
val = lambda idx: sol.get(names[idx], 0.0)
rows = d["rows"]
# recover osil index maps: path w by (i,l,j), q by (i,l), y by (l,j), z by (i,j)
import collections
W = {}; Qi = {}; Yi = {}
wq = {}; wy = {}
for k, r in rows.items():
    if k >= 0 and r["quad"]:
        (w,), ((a_, b_, c_),) = r["lin"].keys(), r["quad"]; wq[w] = a_; wy[w] = b_
# rebuild the same maps as SppInst (re-run its internal logic by re-deriving from P.cpath keys is not possible),
# so evaluate via the linear objective and constraint residuals of the original OSiL model instead:
maxviol = 0.0
for k, r in rows.items():
    if k < 0: continue
    act = sum(c * val(i) for i, c in r["lin"].items()) + sum(c * val(a) * val(b) for a, b, c in r["quad"])
    if r["lb"] is not None and r["lb"] > -1e300: maxviol = max(maxviol, r["lb"] - act)
    if r["ub"] is not None and r["ub"] < 1e300: maxviol = max(maxviol, act - r["ub"])
obj = sum(c * val(i) for i, c in rows[-1]["lin"].items())
print("osil model: max violation", maxviol, "objective", obj, "sol objvar", sol.get("objvar"))
# now the rebuilt model: fix rebuilt variables from the solution using SppInst's variable maps
P2 = spp.SppInst(osil_path)
print("rebuilt sizes", P2.nvar_check)
# fix rebuilt variables to the solution and check feasibility of the rebuilt pq model (bilinear rows included)
for (i, l), var in q.items(): var.LB = var.UB = val(P2.idx_q[(i, l)])
for (l, j), var in y.items(): var.LB = var.UB = val(P2.idx_y[(l, j)])
for (i, j), var in z.items(): var.LB = var.UB = val(P2.idx_z[(i, j)])
for (i, l, j), var in v.items(): var.LB = var.UB = val(P2.idx_w[(i, l, j)])
m.Params.FeasibilityTol = 1e-6
m.optimize()
print("rebuilt pq model with solution fixed: status", m.Status, "objective", m.ObjVal if m.Status == 2 else None)
bil = max(abs(v[i, l, j].LB - q[i, l].LB * y[l, j].LB) for (i, l, j) in v)
print("max |w - q*y| in solution", bil)
