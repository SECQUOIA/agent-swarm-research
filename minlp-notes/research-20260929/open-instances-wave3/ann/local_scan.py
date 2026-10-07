"""Local searches (SLSQP, margin 1e-12) started from centers of saved open boxes: finds local minima of R
in the regions the B&B still has to resolve.  Diagnostic only (not part of the certificate)."""
import sys
import numpy as np
import ann_tm as at
import ann_bb as ab
Z = np.load(sys.argv[1]); nst = int(sys.argv[2]) if len(sys.argv) > 2 else 200
M = at.SepModel()
lo, hi, key = Z["lo"], Z["hi"], Z["key"]
rng = np.random.default_rng(3)
o = np.argsort(key)
pick = np.concatenate([o[:nst // 2], rng.choice(len(key), nst - nst // 2, replace=False)])
res = []
for i in pick:
    c = 0.5 * (lo[i] + hi[i])
    u = ab.local_opt(M, c, margin=1e-12)
    ok, fv = M.point_value(u)
    if ok:
        res.append((fv, tuple(np.round((u - M.lo0) / (M.hi0 - M.lo0), 4))))
res.sort()
seen = []
for fv, uu in res:
    if all(np.linalg.norm(np.array(uu) - np.array(s)) > 1e-2 for _, s in seen):
        seen.append((fv, uu))
print(f"{len(res)} feasible local solutions from {len(pick)} starts; distinct (normalized u):")
for fv, uu in seen[:15]:
    print(f"  f = {fv:.10f} at {uu}")
