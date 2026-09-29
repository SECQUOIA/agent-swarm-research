"""Theorem 3.1 at large p: root exactness vs n = alpha k log p, optimized over lam.
Exact conditional law: given (X_S, w), null a_l/||r|| are iid N(0,1), so
P(root exact | X_S, w) = (1 - 2 Phibar(m0/||r||))^(p-k) (Corollary 2.4).  Also records tau_hat^2/tau_lam^2.
usage: python3 root_large.py"""
import os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
import numpy as np
from scipy.stats import norm

def tau_lam2(n, k, lam, b, s):
    bl = b * n / (n + lam)
    return (lam * bl) ** 2 / (n * s ** 2 + k * bl ** 2 * lam ** 2 / n)

b, sig, k, seeds = 1.0, 0.5, 200, 12
print(f"k={k}, b={b}, sigma={sig}, {seeds} seeds; lam = (sigma/b) sqrt(C log p * n), best C per cell")
for p in (10 ** 4, 10 ** 8, 10 ** 16):
    L = np.log(p)
    for alpha in (1.6, 1.8, 2.0, 2.2, 2.5, 3.0):
        n = int(round(alpha * k * L))
        best = None
        for C in (2, 4, 8, 16, 32, 64):
            lam = sig / b * np.sqrt(C * L * n)
            Ps, ratios, lamn = [], [], lam / n
            for s in range(seeds):
                rng = np.random.default_rng(1000 * s + 7)
                XS = rng.standard_normal((n, k)); w = rng.standard_normal(n)
                y = XS @ (b * rng.choice([-1.0, 1.0], k)) + sig * w
                bS = np.linalg.solve(XS.T @ XS + lam * np.eye(k), XS.T @ y)
                r = y - XS @ bS
                th = lam * np.min(np.abs(bS)) / np.linalg.norm(r)
                Ps.append(np.exp((p - k) * np.log1p(-2 * norm.sf(th))))
                ratios.append(th ** 2 / tau_lam2(n, k, lam, b, sig))
            rec = (np.mean(Ps), C, lamn, tau_lam2(n, k, lam, b, sig) / (2 * L), np.mean(ratios), np.min(ratios))
            if best is None or rec[0] > best[0]:
                best = rec
        print(f"  p=1e{int(np.log10(p)):<3d} alpha={alpha:.1f} n={n:6d}: P(root exact)={best[0]:.3f} (C={best[1]}, lam/n={best[2]:.3f}, "
              f"tau_lam^2/(2log p)={best[3]:.3f}, tau_hat^2/tau_lam^2 mean {best[4]:.3f} min {best[5]:.3f})", flush=True)
