"""Forced-in node values at p = 3200, lam = sqrt n, k = 5, alpha = 3 (n = 121) for seeds 1007 and 1000:
nulls ranked 1..60 by |a_j| plus ranks 100, 500, median and weakest (seed 1007), and ranks
1, 2, 5, 6, 10, 50, 100, 500, median, weakest (seed 1000).  Node values by column generation to
convergence (certified dual bound and restricted primal value agree)."""
import os
for v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]: os.environ[v] = "1"
import sys, json, numpy as np
from multiprocessing import Pool
from core import instance, ridge, solve_node_cg
def job(args):
    seed, rank, j = args
    X, y, lam, S = instance(121, 3200, 5, seed=seed)
    f, b, r = ridge(X, y, lam, S)
    LB, val, z, a, rd = solve_node_cg(X, y, lam, 5, (), (int(j),), init=S, maxrounds=300, add=60)
    return dict(seed=seed, rank=rank, j=int(j), zj=float(abs(X[:, j] @ r) / np.linalg.norm(r)), LB_minus_f=LB - f, val_minus_f=val - f, rounds=rd)
if __name__ == '__main__':
    jobs = []
    for seed, ranks in [(1007, list(range(1, 61)) + [100, 500, 'median', 'weakest']), (1000, [1, 2, 5, 6, 10, 50, 100, 500, 'median', 'weakest'])]:
        X, y, lam, S = instance(121, 3200, 5, seed=seed)
        f, b, r = ridge(X, y, lam, S); a = np.abs(X.T @ r)
        nul = np.array([j for j in range(3200) if j not in S]); order = nul[np.argsort(-a[nul])]
        print(seed, 'f(S*) %.4f price m0^2/lam %.3f  #violators %d  sat-gain sum (|a|-m0)_+^2/n %.2f' % (
            f, (lam * np.abs(b).min()) ** 2 / lam, (a[nul] > lam * np.abs(b).min()).sum(),
            np.sum(np.maximum(a[nul] - lam * np.abs(b).min(), 0) ** 2) / 121), flush=True)
        for rk in ranks:
            idx = {'median': len(order) // 2, 'weakest': len(order) - 1}.get(rk, rk - 1 if isinstance(rk, int) else 0)
            jobs.append((seed, rk, order[idx]))
    with Pool(5) as pool:
        for res in pool.imap(job, jobs):
            print(json.dumps(res), flush=True)
