"""Distribution of the minimal support size of corner minimizers for random bilinear corners."""
import sys
import numpy as np
from core import bilinear_quadratic, corner_bound, qval
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
for N in (3, 6, 10):
    cnt = {1: 0, 2: 0, 3: 0}; tot = 0
    for t in range(300):
        side = '+' if rng.random() < 0.5 else '-'
        Q, b, c = bilinear_quadratic(side)
        while True:
            sbar = rng.normal(size=3)
            if qval(Q, b, c, sbar) > 0.05:
                break
        P = rng.normal(size=(3, N)); w = rng.uniform(0.1, 1.0, N)
        zk, lam = corner_bound(Q, b, c, sbar, P, w, max_support=3, return_point=True)
        if not np.isfinite(zk):
            continue
        tot += 1; cnt[int(np.sum(lam > 1e-9))] += 1
    print('N', N, 'instances', tot, 'support counts', cnt)
