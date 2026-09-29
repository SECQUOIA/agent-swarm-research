"""Total-energy noise (sigma = gamma/sqrt n), lam = sqrt n, equal magnitudes b = 1.
Checks the Step 1 claim ||r||^2 ~ omega_lam^2, m0 ~ lam b_lam (so tau_hat ~ tau_lam) and the exactness
probability at S*, P = E[(1 - 2 Phibar(m0/||r||))^(p-k)] (exact conditional law of the null maximum),
at n = c * 2 (k + gamma^2/b^2) log p, for gamma^2/b^2 small (0.25) and comparable to k (= k).
usage: python3 total_energy.py"""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import numpy as np
from scipy.stats import norm

rng = np.random.default_rng(2029)
k, b, reps = 20, 1.0, 300
print("k=%d, b=1, lam=sqrt n, sigma=gamma/sqrt n; P(root exact at S*) and median tau_hat^2/tau_lam^2" % k)
for g2 in [0.25, 20.0]:
    for p in [1e6, 1e12]:
        line = []
        for c in [0.8, 1.0, 1.25]:
            n = int(round(c * 2 * (k + g2 / b ** 2) * np.log(p)))
            lam = np.sqrt(n); sigma = np.sqrt(g2 / n)
            bl = b * n / (n + lam)
            om2 = n * sigma ** 2 + k * b ** 2 * lam ** 2 * n / (n + lam) ** 2
            tl2 = (lam * bl) ** 2 / om2
            pe, ratio = [], []
            for _ in range(reps):
                XS = rng.standard_normal((n, k)); w = rng.standard_normal(n)
                beta = b * rng.choice([-1.0, 1.0], k)
                y = XS @ beta + sigma * w
                bS = np.linalg.solve(XS.T @ XS + lam * np.eye(k), XS.T @ y)
                r = y - XS @ bS
                t = lam * np.abs(bS).min() / np.linalg.norm(r)
                pe.append(np.exp((p - k) * np.log1p(-2 * norm.sf(t))))
                ratio.append(t * t / tl2)
            line.append("c=%.2f n=%d: P=%.2f, tau_hat^2/tau_lam^2=%.3f, tau_lam^2/(2 log p)=%.3f" % (
                c, n, np.mean(pe), np.median(ratio), tl2 / (2 * np.log(p))))
        print("gamma^2/b^2=%g p=%.0e | " % (g2, p) + " | ".join(line), flush=True)
