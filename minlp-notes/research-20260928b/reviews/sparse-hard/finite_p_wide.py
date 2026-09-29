"""Part C of the finite-p check: larger alpha, and thresholds for clique >= 2, > k+1, >= e^10."""
import numpy as np
from finite_p import best_L
for lamrule in ['zero', 'sqrt(n log p)']:
    first = {}
    for lp in np.arange(5.0, 12.01, 0.5):
        p = 10 ** lp
        best = {}
        for k in np.unique(np.geomspace(3, min(p / 100, 3e4), 24).astype(int)):
            for alpha in [16, 32, 64, 128, 256, 512, 1024, 4096]:
                n = int(round(alpha * k * np.log(p)))
                lam = 0.0 if lamrule == 'zero' else np.sqrt(n * np.log(p))
                L, arg = best_L(n, p, k, lam)
                if not np.isfinite(L):
                    continue
                for name, thr in [('>=2', np.log(2)), ('>k+1', np.log(k + 2)), ('>=e^10', 10.0)]:
                    if L >= thr and (name not in best or L > best[name][0]):
                        best[name] = (round(L, 2), int(k), alpha)
        for name in ['>=2', '>k+1', '>=e^10']:
            if name in best and name not in first:
                first[name] = (lp, best[name])
        print("lam=%s p=1e%.1f: %s" % (lamrule, lp, best), flush=True)
        if len(first) == 3:
            break
    print("FIRST (lam=%s):" % lamrule, first, flush=True)
