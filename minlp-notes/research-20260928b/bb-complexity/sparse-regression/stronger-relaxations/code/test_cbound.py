"""Validity check of the certified upper bounds (cbound.py) against exact relaxation values:
for random small instances, at the root and at a forced-in node, check
  SDP1 (exact, Clarabel) <= L1 upper bound   and   L2 (exact, Clarabel) <= L2 upper bound."""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import numpy as np
from relax import instance, ridge, sdp1, L2
from cbound import best_small_F_bound, delta_opt_persp
bad = 0; tot = 0; fin = 0
for seed in range(12):
    n, p, k = 8, 40, 2
    X, y, lam, S = instance(n, p, k, seed=500 + seed, tau0=1.0)
    fS, bS, r = ridge(X, y, lam, S)
    a = np.abs(X.T @ r); a[list(S)] = -1
    order = [int(j) for j in np.argsort(-a)]
    for S0, S1 in [((), ()), ((), (order[0],)), ((S[0],), ())]:
        cand = [j for j in order if j not in S1][:10]
        b1, b2, info = best_small_F_bound(X, y, lam, k, S, cand, hs=(1, 2, 3, 5), S0=S0, S1=S1, delta=delta_opt_persp(X, lam))
        v1 = sdp1(X, y, lam, k, S0, S1); v2 = L2(X, y, lam, k, S0, S1)
        tot += 1; fin += np.isfinite(b2)
        ok = v1 <= b1 * (1 + 1e-6) and v2 <= b2 * (1 + 1e-6)   # tolerance = solver accuracy
        bad += not ok
        print(seed, S0, S1, 'SDP1=%.5f L1ub=%.5f  L2=%.5f L2ub=%.5f' % (v1, b1, v2, b2), 'ok' if ok else 'VIOLATION', flush=True)
print('checked', tot, 'nodes;', fin, 'with finite L2 bound; violations:', bad)
