"""Mechanism experiment: nested designs with n, k, lam, y fixed and p growing.
For each seed, X_full is n x pmax; the instance with p features uses the first p columns; S* = {0..k-1};
b = 1, sigma = 0.5, lam = 1.5 sigma sqrt(2 n log 200)/b (fixed across p).
Records f(S*), the perspective root value (certified dual bound), the PWE ratio max|a_l|/m0,
certified upper bounds on the L_1 (optimal perspective) and L_2 (pairwise lifted hull) root values
(cbound.best_small_F_bound, supports S u top-h violators), and exact relaxation values where affordable:
    sdp1 (Clarabel p <= P1C, SCS p <= P1S), sdp2 (Clarabel p <= P2), zb (SCS p <= PZB).
usage: exp_mech.py OUT n k pmax plist seeds nproc [P1C P1S P2 PZB]
"""
import os, sys, json, time
for v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[v] = "1"
import numpy as np
from multiprocessing import Pool
from relax import ridge, sdp1, sdp2, zb, persp
from cbound import best_small_F_bound, delta_opt_persp

b, sigma = 1.0, 0.5


def make(n, k, pmax, p, seed):
    rng = np.random.default_rng(seed)
    Xf = rng.standard_normal((n, pmax))
    beta = np.zeros(pmax); beta[:k] = b * rng.choice([-1.0, 1.0], k)
    y = Xf @ beta + sigma * rng.standard_normal(n)
    lam = 1.5 * sigma * np.sqrt(2 * n * np.log(200)) / b
    return Xf[:, :p], y, lam, tuple(range(k))


def job(args):
    n, k, pmax, p, seed, lim = args
    X, y, lam, S = make(n, k, pmax, p, seed)
    t0 = time.time()
    fS, bS, r = ridge(X, y, lam, S)
    a = np.abs(X.T @ r); a[list(S)] = -1.0
    m0 = lam * np.abs(bS).min()
    cand = [int(j) for j in np.argsort(-a)[:20]]
    P = persp(X, y, lam, k)[0]
    delta = delta_opt_persp(X, lam)
    L1ub, L2ub, info = best_small_F_bound(X, y, lam, k, S, cand, hs=(1, 2, 3, 5, 8, 12, 20, 30), delta=delta)
    out = dict(n=n, k=k, p=p, seed=seed, lam=lam, fS=fS, P=P, maxratio=float(a.max() / m0),
               nviol=int((a > m0).sum()), tau2=float((m0 / np.linalg.norm(r)) ** 2), delta=delta,
               L1_ub=L1ub, L2_ub=L2ub, ub_info=info)
    P1C, P1S, P2, PZB = lim
    if p <= P1C: out['sdp1'] = sdp1(X, y, lam, k)
    elif p <= P1S: out['sdp1'] = sdp1(X, y, lam, k, solver='SCS'); out['sdp1_solver'] = 'SCS'
    if p <= P2: out['sdp2'] = sdp2(X, y, lam, k)
    if p <= PZB: out['zb'] = zb(X, y, lam, k, solver='SCS'); out['zb_solver'] = 'SCS'
    out['time'] = time.time() - t0
    return out


if __name__ == '__main__':
    OUT, n, k, pmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    plist = [int(v) for v in sys.argv[5].split(',')]; seeds = int(sys.argv[6]); nproc = int(sys.argv[7])
    lim = [int(v) for v in sys.argv[8:12]] if len(sys.argv) > 8 else [80, 320, 80, 160]
    jobs = [(n, k, pmax, p, 2000 + s, lim) for s in range(seeds) for p in plist]
    jobs.sort(key=lambda j: -j[3])
    with Pool(nproc) as pool, open(OUT, 'a') as f:
        for res in pool.imap_unordered(job, jobs):
            f.write(json.dumps(res, default=float) + '\n'); f.flush()
            print(res['p'], res['seed'], '%.1fs' % res['time'], flush=True)
