"""Re-check of the Remark 3.5 numbers from the note's check_pwe.py instances (same seeds 700+s,
same generation order), with own code: PWE certificate at S*, root value (certified bracket),
and strict C1 at S* (which certifies that S* is the unique optimal support).
Also: the limit (1 - 2 Phibar(w_min/gamma))^(d-k).
usage: python3 pwe_recheck.py"""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import numpy as np
from scipy.stats import norm
from rc_common import fit, solve_node, decide_c1

p, k, b, gam = 50, 5, 1.0, 0.5
print("limit (1 - 2 Phibar(2))^45 = %.4f" % (1 - 2 * norm.sf(b / gam)) ** (p - k))
for n in [500, 5000]:
    both = 0; gaps = []
    for seed in range(10):
        rng = np.random.default_rng(700 + seed)
        X = rng.standard_normal((n, p)); S = np.sort(rng.choice(p, k, replace=False))
        beta = np.zeros(p); beta[S] = b * rng.choice([-1.0, 1.0], k)
        y = X @ beta + gam * rng.standard_normal(n); lam = np.sqrt(n)
        S = [int(s) for s in S]
        fS, bS, r = fit(X, y, lam, S)
        a = np.abs(X.T @ r); nul = [j for j in range(p) if j not in S]
        cert = bool(a[nul].max() <= lam * np.abs(bS).min())
        root = solve_node(X, y, lam, k, W0=S)
        d = decide_c1(X, y, lam, k, S)
        inexact = root['ub'] < fS * (1 - 1e-9)
        if inexact and d['status'] == 'C1':
            both += 1; gaps.append((fS - root['ub']) / fS)
        print("n=%d seed=%d cert %-5s  root bracket [%.8f, %.8f]  f(S*) %.8f  rel gap (by ub) %.2e  C1: %s" % (
            n, seed, cert, root['lb'], root['ub'], fS, (fS - root['ub']) / fS, d['status']), flush=True)
    print("n=%d: S* certified unique optimum AND root value certified below f(S*): %d/10; rel gaps %s" % (
        n, both, ["%.1e" % g for g in sorted(gaps)]))
