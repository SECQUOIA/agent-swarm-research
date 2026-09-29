"""Counterexample to PWE Theorem 2 as stated (per-entry noise N(0,gamma^2), rho = sqrt n).
p = 50, k = 5, b = 1 (w_min = 1, ||w*||^2 = 5), gamma = 0.5, rho = lam = sqrt n.
For each instance: PWE certificate at S* (Corollary 2.4: root exact at S* iff it holds), root value R
(Clarabel, certified bound), and an exact decision of C1 at S* (which, if it holds, certifies that S* is
the unique optimal support, so R < f(S*) = OPT means the relaxation is not exact)."""
import os
for v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]: os.environ[v] = "1"
import numpy as np
from scipy.stats import norm
from core import ridge, solve_node, decide_c1_exact
p, k, b, gam = 50, 5, 1.0, 0.5
print("limit P(root exact at S*) as n -> inf: (1-2 Phibar(b/gamma))^(p-k) = %.4f" % (1 - 2 * norm.sf(b / gam)) ** (p - k))
for n in [500, 5000]:
    c0 = n / ((gam ** 2 + k * b * b) / b ** 2 * np.log(p))
    cert = inexact = uniq = 0
    for seed in range(10):
        rng = np.random.default_rng(700 + seed)
        X = rng.standard_normal((n, p)); S = np.sort(rng.choice(p, k, replace=False))
        beta = np.zeros(p); beta[S] = b * rng.choice([-1.0, 1.0], k)
        y = X @ beta + gam * rng.standard_normal(n); lam = np.sqrt(n)
        fS, bS, r = ridge(X, y, lam, list(S)); a = np.abs(X.T @ r)
        nul = [j for j in range(p) if j not in set(S)]
        c = bool(a[nul].max() <= lam * np.abs(bS).min())
        LB, val, z, al = solve_node(X, y, lam, k)
        d = decide_c1_exact(X, y, lam, k, S)
        cert += c; uniq += (d['status'] == 'C1'); inexact += (val < fS * (1 - 1e-9))
        print("n=%d seed=%d  PWE cert %s  (f(S*)-R)/f(S*) = %.2e  C1 at S* (S* unique optimum): %s" % (n, seed, c, (fS - val) / fS, d['status']))
    print("n=%d (c0 = %.0f): certificate %d/10, S* certified unique optimum %d/10, root value < f(S*) %d/10" % (n, c0, cert, uniq, inexact))
