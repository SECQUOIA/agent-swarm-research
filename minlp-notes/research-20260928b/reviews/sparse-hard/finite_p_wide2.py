"""Targeted continuation of finite_p_wide.py (stopped at p = 1e8.5 for time):
largest certified log-clique L at p = 1e9, 1e10, 1e12 over k <= 3000, alpha up to 4096."""
import numpy as np
from finite_p import best_L

for lamrule in ['zero', 'sqrt(n log p)']:
    for lp in [9.0, 10.0, 12.0]:
        p = 10 ** lp
        best = (-np.inf, None)
        for k in np.unique(np.geomspace(10, 3000, 12).astype(int)):
            for alpha in [16, 64, 256, 1024, 4096]:
                n = int(round(alpha * k * np.log(p)))
                lam = 0.0 if lamrule == 'zero' else np.sqrt(n * np.log(p))
                L, arg = best_L(n, p, k, lam, Rs=(3, 6, 16, 64), nm=10)
                if L > best[0]:
                    best = (round(L, 2), (int(k), alpha, n, arg))
        print("lam=%s p=1e%.0f: best L=%s at (k, alpha, n, (R,m)) = %s" % (lamrule, lp, best[0], best[1]), flush=True)
