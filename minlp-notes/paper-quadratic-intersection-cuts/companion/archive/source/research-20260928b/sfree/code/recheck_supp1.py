"""Re-generate explore_orbit.py (seed 1, N=3) instances and recheck the orbit ratio with a
rescaled problem (divide rays so that z_K = 1) and tighter bisection."""
import numpy as np, warnings; warnings.filterwarnings('ignore')
from core import bilinear_quadratic, corner_bound, qval, best_orbit_bound
from scout_sfree import ms_set, ic_bound
rng = np.random.default_rng(1); N = 3
for t in range(20):
    side = '+' if rng.random() < 0.5 else '-'
    Q, b, c = bilinear_quadratic(side)
    while True:
        sbar = rng.normal(size=3)
        if qval(Q, b, c, sbar) > 0.05: break
    P = rng.normal(size=(3, N)); w = rng.uniform(0.1, 1.0, N)
    zk, lam = corner_bound(Q, b, c, sbar, P, w, return_point=True)
    if not np.isfinite(zk): continue
    G, cs = ms_set(Q, b, c, sbar); zms = ic_bound(G, sbar, P, w)[0]
    if t in (19,):
        wn = w / zk      # rescale costs so that z_K = 1
        cert, hi, F = best_orbit_bound(side, sbar, P, wn, 1.0, iters=50)
        print('instance', t, 'support', int(np.sum(lam > 1e-9)), 'cert %.10f hi %.10f' % (cert, hi))
