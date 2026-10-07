"""Negative / positive control for vbb2 on an exactly feasible point.

waterno2_06 period 0 at the SCIP-reproduction multipliers
(open-instances-wave2/waterno2/logs/scip_repro_mult.json).  The first verifier
built an exactly feasible rational point there (logs/exact_point_p0.json).
This script re-checks the point exactly (all rows, OSIL bounds, integrality),
evaluates its Lagrangian value v with vbb2's objective, and then runs vbb2
  (a) with target v + 0.05 (unreachable): must NOT certify, and its rigorous
      bound must be <= v;
  (b) with target v - 1e-3 (reachable): expected to certify.
usage: python3 control.py time_limit
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import sys
from fractions import Fraction as F

import vbb2
from vbb2 import vbb

W2 = _RESEARCH + "/open-instances-wave2/waterno2/logs/"
V1 = _RESEARCH + "/reviews/waterno2-verification/logs/"
tl = float(sys.argv[1]) if len(sys.argv) > 1 else 600.0
mult = json.load(open(W2 + "scip_repro_mult.json"))
lam = [[float(v) for v in l] for l in mult["lam"]]
P = vbb2.PeriodF(6, 0, lam, float(mult["mu"]))
pt = {k: F(v) for k, v in json.load(open(V1 + "exact_point_p0.json")).items()}
z = [pt[nm] for nm in P.names]
for (kind, x, y, w) in P.aux:
    z.append(z[x] ** 2 if kind == "sq" else z[x] ** 3 if kind == "cube" else z[x] * z[y])
m = vbb.vmodel.instance(6)["m"]
idx = {n: k for k, n in enumerate(m["names"])}
viol = F(0)
for nm, v in zip(P.names, z):
    g = idx[nm]
    if m["lb"][g].upper() != "-INF":
        viol = max(viol, F(m["lb"][g]) - v)
    if m["ub"][g].upper() not in ("INF", "+INF"):
        viol = max(viol, v - F(m["ub"][g]))
    if m["vt"][g] == "B":
        assert v in (0, 1)
for (cols, cf, L, U, name) in P.rows:
    s = sum(a * z[c] for c, a in zip(cols, cf))
    if L is not None:
        viol = max(viol, L - s)
    if U is not None:
        viol = max(viol, s - U)
val = sum(P.c[j] * z[j] for j in range(P.n))
print(f"exact point: max violation {viol} (must be 0); Lagrangian value {float(val)!r}", flush=True)
assert viol == 0
for name, target in (("unreachable", float(val) + 0.05), ("reachable", float(val) - 1e-3)):
    res = vbb2.solve(P, target, 10**8, tl, verbose=False)
    b = None if res["bound"] is None else F(res["bound"])
    ok = (res["status"] != "certified" and b is not None and b <= val) if name == "unreachable" \
        else res["status"] == "certified"
    print(f"{name}: target {target!r} -> status {res['status']}, bound {res['bound_float']!r}, "
          f"bound - value = {float(b - val) if b is not None else None!r}, nodes {res['nodes']}, "
          f"time {res['time']:.0f}s -> {'as expected' if ok else 'UNEXPECTED'}", flush=True)
