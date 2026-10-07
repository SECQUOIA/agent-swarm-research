"""Orbit (sliced C_F) exactness restricted to corners whose minimizer has support 2."""
import sys
import numpy as np
from core import bilinear_quadratic, corner_bound, qval, best_orbit_bound
from scout_sfree import ms_set, ic_bound
import warnings; warnings.filterwarnings('ignore')
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 3
want = int(sys.argv[3]) if len(sys.argv) > 3 else 15
got = 0; res = []
while got < want:
    side = '+' if rng.random() < 0.5 else '-'
    Q, b, c = bilinear_quadratic(side)
    while True:
        sbar = rng.normal(size=3)
        if qval(Q, b, c, sbar) > 0.05:
            break
    P = rng.normal(size=(3, N)); w = rng.uniform(0.1, 1.0, N)
    zk, lam = corner_bound(Q, b, c, sbar, P, w, return_point=True)
    if not np.isfinite(zk) or np.sum(lam > 1e-9) != 2:
        continue
    got += 1
    G, cs = ms_set(Q, b, c, sbar)
    zms = ic_bound(G, sbar, P, w)[0]
    cert, hi, F = best_orbit_bound(side, sbar, P, w, zk)
    res.append((min(zms, zk) / zk, cert / zk, hi / zk))
    print(got, side, 'scip %.4f orbit cert %.6f bisect %.6f' % res[-1], flush=True)
R = np.array(res)
print('mean', R.mean(0).round(4), 'min', R.min(0).round(4))
