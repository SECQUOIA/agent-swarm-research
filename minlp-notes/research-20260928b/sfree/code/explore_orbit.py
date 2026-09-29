"""Exploration: exact best sliced-orbit bound (LMI bisection) vs exact corner bound,
random bilinear corners.  Also records the support of the corner minimizer."""
import sys, json
import numpy as np
from core import (bilinear_quadratic, corner_bound, qval, best_orbit_bound, Mmat)
from scout_sfree import ms_set, ic_bound

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 3
T = int(sys.argv[3]) if len(sys.argv) > 3 else 20
rows = []
for t in range(T):
    side = '+' if rng.random() < 0.5 else '-'
    Q, b, c = bilinear_quadratic(side)
    while True:
        sbar = rng.normal(size=3)
        if qval(Q, b, c, sbar) > 0.05:
            break
    P = rng.normal(size=(3, N)); w = rng.uniform(0.1, 1.0, N)
    zk, lam = corner_bound(Q, b, c, sbar, P, w, return_point=True)
    if not np.isfinite(zk):
        continue
    supp = int(np.sum(lam > 1e-9))
    zk3, lam3 = corner_bound(Q, b, c, sbar, P, w, max_support=3, return_point=True)
    G, cs = ms_set(Q, b, c, sbar)
    zms = ic_bound(G, sbar, P, w)[0]
    cert, hi, F = best_orbit_bound(side, sbar, P, w, zk)
    rows.append(dict(side=side, supp=supp, zk=zk, zk3=zk3, scip=min(zms, zk) / zk, orbit_cert=cert / zk, orbit_hi=hi / zk))
    print(t, side, 'supp', supp, 'zK %.5f (3-supp %.5f)' % (zk, zk3), 'scip %.4f' % (min(zms, zk) / zk),
          'orbit %.6f / %.6f' % (cert / zk, hi / zk), flush=True)
R = np.array([[r['scip'], r['orbit_cert'], r['orbit_hi']] for r in rows])
print('mean scip %.4f orbit %.5f  min orbit %.5f  frac orbit>=0.999 %.3f' % (R[:, 0].mean(), R[:, 1].mean(), R[:, 1].min(), np.mean(R[:, 1] >= 0.999)))
