"""Solve every forced-in node r(emptyset,{j}), j not in S*, for one seed, in chunk CH of NCH
(j index modulo NCH).  Uses the solver of sparse_s1007_audit.py with tol 1e-6 (relative) and at most 4000 iterations;
the bracket [lo, up] is certified either way.  Usage: SEED CH NCH OUT"""
import os, sys, json, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"):
    os.environ[v] = "1"
import numpy as np
from sparse_s1007_audit import instance, solve_forced_in, n, p, k
seed, ch, nch, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
X, y, lam, S = instance(seed)
XS = X[:, S]
r = y - XS @ np.linalg.solve(XS.T @ XS + lam * np.eye(k), XS.T @ y)
fS = float(y @ r)
with open(out, "w") as fh:
    for j in range(p):
        if j in set(S.tolist()) or j % nch != ch:
            continue
        up, lo, z, its = solve_forced_in(X, y, lam, j, S, iters=4000, tol=1e-6)
        fh.write(json.dumps(dict(j=j, up=up - fS, lo=lo - fS, iters=its)) + "\n"); fh.flush()
