"""Loose relaxation (superseded): wrong-side halfspace of a point-rule member replaced by ANY null
halfspace, optimized over (theta, phi); also the best member MS returns unchanged (both tangency points
on the slice side).  The relaxation reaches z_K, but MS's construction only uses one of the two
asymptotes (tangency lines in H_0), which ms_asymptote_check.py models; that check shows MS's full
construction still misses z_K on all 13 corners.  Instances: point_rule_check.py 0 40."""
import numpy as np
from scipy.optimize import minimize
from point_rule_check import case2_instance
from core import corner_bound
from orbit_n1 import sylvester
rng = np.random.default_rng(0)
for i in range(40):
    Q, b, c, sbar, P, w = case2_instance(rng)
    zk = corner_bound(Q, b, c, sbar, P, w)
    if not np.isfinite(zk):
        continue
    W, n, m = sylvester(Q, b, c); Wi = np.linalg.inv(W)
    us = W @ np.append(sbar, 1.0); xh, yh = us[:2], us[2]
    D = [W @ np.append(P[:, j], 0.0) for j in range(P.shape[1])]
    hc = lambda v: (Wi @ v)[-1]

    def pair_bound(g1, g2):
        vals = []
        for j, d in enumerate(D):
            al = np.inf
            for (g, s) in ((g1, 1.0), (g2, -1.0)):
                v0 = g @ xh - s * yh; sl = g @ d[:2] - s * d[2]
                if v0 <= 0:
                    return 0.0
                if sl < 0:
                    al = min(al, v0 / -sl)
            if np.isfinite(al):
                vals.append(w[j] * al)
        return min(vals) if vals else np.inf

    def member(th):
        g1 = np.array([np.cos(th), np.sin(th)]); den = g1 @ xh - yh
        if den <= 1e-14:
            return None
        a = (xh @ xh - yh * yh) / (2 * den); bq = a - yh
        if a <= 0 or bq <= 1e-14:
            return None
        return g1, (xh - a * g1) / bq

    def plain(th):
        mm = member(th)
        return 0.0 if mm is None else pair_bound(*mm)

    def relaxed(x):          # x = (theta, phi)
        mm = member(x[0])
        if mm is None:
            return 0.0
        g1, g2 = mm; h1 = hc(np.append(g1, 1.0)); h2 = hc(np.append(g2, -1.0))
        g = np.array([np.cos(x[1]), np.sin(x[1])])
        if h1 >= 0 and h2 >= 0:
            return pair_bound(g1, g2)
        return pair_bound(g1, g) if h1 >= 0 else pair_bound(g, g2)

    ths = np.linspace(0, 2 * np.pi, 4001)
    pv = max(plain(t) for t in ths)
    if pv >= zk * (1 - 1e-4):
        continue
    best = 0.0
    grid = [(t, f) for t in np.linspace(0, 2 * np.pi, 241) for f in np.linspace(0, 2 * np.pi, 241)]
    vals = sorted(((relaxed(np.array(x)), x) for x in grid), key=lambda z: -z[0])[:12]
    for v, x in vals:
        r = minimize(lambda y: -relaxed(y), np.array(x), method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-14, maxiter=4000))
        best = max(best, v, -r.fun)
    good = []
    for t in ths:
        mm = member(t)
        if mm is None:
            continue
        g1, g2 = mm
        if hc(np.append(g1, 1.0)) >= 0 and hc(np.append(g2, -1.0)) >= 0:
            good.append(pair_bound(g1, g2))
    gv = max(good) if good else 0.0
    print('instance %2d: plain point rule %.6f | plain members MS returns unchanged (both tangencies on the slice side) %.6f | loose relaxation (any null halfspace) %.6f (of z_K)'
          % (i, pv / zk, min(gv, zk) / zk, min(best, zk) / zk), flush=True)
