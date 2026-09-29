"""Seed 1007 (p = 3200, lam = sqrt n): forced-in margins across the null ranking, and the terms of
Heuristic 3.8 (price m0^2/lam, saturated gain sum (|a_l|-m0)_+^2/n, own fit a_j^2/(n+lam))."""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import numpy as np
from rc_common import make_instance, fit, solve_node
p, k, n = 3200, 5, 121
for seed in [1007, 1000]:
    X, y, lam, S = make_instance(n, p, k, seed, 'sqrtn')
    fS, bS, r = fit(X, y, lam, S)
    a = X.T @ r; rn = np.linalg.norm(r); m0 = lam * np.abs(bS).min()
    nulls = np.array([j for j in range(p) if j not in set(S)])
    order = nulls[np.argsort(-np.abs(a[nulls]))]
    sat = float(np.sum(np.clip(np.abs(a[nulls]) - m0, 0, None) ** 2) / n)
    print("seed %d: price m0^2/lam = %.3f, saturated gain sum(|a_l|-m0)_+^2/n = %.3f, #violators %d" %
          (seed, m0 ** 2 / lam, sat, int((np.abs(a[nulls]) > m0).sum())))
    root = solve_node(X, y, lam, k, W0=S, maxrounds=300)
    W0 = set(S) | set(np.nonzero(root['z'] > 1e-7)[0].tolist())
    for rk in [1, 2, 5, 6, 10, 50, 100, 200, 500, 1600, 3195]:
        j = int(order[rk - 1])
        res = solve_node(X, y, lam, k, (), (j,), W0=W0, maxrounds=300)
        print("  rank %4d j=%4d |a_j|/||r||=%.3f own fit %.3f: node - f(S*) = %.3f" %
              (rk, j, abs(a[j]) / rn, a[j] ** 2 / (n + lam), res['lb'] - fS), flush=True)
