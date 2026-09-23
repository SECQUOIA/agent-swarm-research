"""Lift feasible original points into the independent LP (indep_bound.build) and report the worst row violation."""
import sys, json
import numpy as np
import indep_bound as B

osil, ptsf, G = sys.argv[1], sys.argv[2], int(sys.argv[3])
S = B.Struct(osil)
grid = np.unique(np.concatenate([np.linspace(0, 1, G), np.geomspace(1e-3, 0.05, 6)]))
lp, info = B.build(S, list(grid))
A, rhs, sense, lb, ub, c = B.to_arrays(lp)
D = np.load(ptsf); out = []
for z, t in zip(D["P"], D["tags"]):
    Z = B.lift(S, lp, z); v = B.violation(A, rhs, sense, lb, ub, Z)
    out.append((v["row_rel"], v["row_abs"], v["bound"], str(t), float(c @ Z)))
out.sort(reverse=True)
print("INDEP_POINTS", json.dumps(dict(n=len(out), lp=A.shape, worst=out[:5])))
