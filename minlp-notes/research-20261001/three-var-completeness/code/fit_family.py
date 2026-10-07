"""Fit a numerical quadratic to lambda * (q_{h,d,k} o g) over the 48 cube
symmetries g and the full valid parameter range (h real, d,k >= 0)."""
import numpy as np
from scipy.optimize import least_squares
from cube3 import *

def comp_matrix(g):
    M = np.zeros((10, 10))
    for j, k in enumerate(QKEYS):
        M[:, j] = vector_from_quad(compose({k: 1}, g))
    return M

GMATS = [comp_matrix(g) for g in GROUP]

def fam_vec(h, d1, d2, d3, k):
    D = d1 + d2 - h
    return np.array([h*h, -2*h*d1, -2*h*d2, 2*h*d3 + 2*d3*k, d1*d1, d2*d2, d3*d3,
                     2*d1*d2 + k*(2*D + k), -2*d1*d3 - 2*d3*k, -2*d2*d3 - 2*d3*k])

def fit(pvec, n_starts=10, seed=0):
    rng = np.random.default_rng(seed)
    pvec = np.asarray(pvec, float); pvec = pvec / np.linalg.norm(pvec)
    best = (np.inf, None, None)
    for gi, M in enumerate(GMATS):
        def resid(z):
            h, a1, a2, a3, kk = z
            v = M @ fam_vec(h, a1**2, a2**2, a3**2, kk**2)
            nv = np.linalg.norm(v)
            if nv == 0: return np.ones(10)
            v = v / nv
            return v - pvec
        for s in range(n_starts):
            z0 = np.concatenate([rng.normal(size=1), rng.uniform(0.3, 1.5, 4)])
            r = least_squares(resid, z0, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=3000)
            if r.cost < best[0]:
                h, a1, a2, a3, kk = r.x
                best = (r.cost, GROUP[gi], (h, a1**2, a2**2, a3**2, kk**2))
    return best

if __name__ == '__main__':
    import json, sys
    d = json.load(open(sys.argv[1]))
    seen = 0
    for o in d:
        if o.get('r0', 0) < -1e-6:
            c, g, par = fit(o['p'])
            h, d1, d2, d3, k = par
            D = d1 + d2 - h
            print('residual %.2e' % c, 'g', g, 'h,d1,d2,d3,k', np.round(par, 5).tolist(),
                  'contact ratios h/d1 %.3f h/d2 %.3f (d1-h)/d3 %.3f (d2-h)/d3 %.3f (D+k)/d3 %.3f' % (h/d1, h/d2, (d1-h)/d3, (d2-h)/d3, (D+k)/d3), flush=True)
            seen += 1
            if seen >= int(sys.argv[2]): break
