"""Reviewer: directional second differences of the 2-D trapezoidal catmix
objective at the author's saved smooth point (no Hessian), N = 100, 200.
Tapered alternating direction on the free block; value / |v|^2 compared with
the symbol prediction f(pi)(J+1) = -0.02729 h^3 (J+1)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import sys
import numpy as np
import mpmath as mp
import importlib.util
mp.mp.dps = 50
ROOT = (_PUBLIC_REPO + '/research-20260929/')
for N in (100, 200):
    sys.argv = ['x', str(N)]
    src = open('v6_catmix_trap_saddle.py').read().split("uc = [mp.mpf")[0]
    ns = {}
    exec(src, ns)
    J = ns['J']
    us = [mp.mpf(float(v)) for v in np.load(ROOT + 'theory-bangbang/singular/logs/catmix%d_smooth_u.npy' % N)]
    usf = np.array([float(v) for v in us])
    free = [i for i in range(N + 1) if 1e-9 < usf[i] < 1 - 1e-9]
    n = len(free)
    J0 = J(us)
    e = mp.mpf(10)**-6
    g = max(abs((J([v + (e if k == i else 0) for k, v in enumerate(us)]) - J([v - (e if k == i else 0) for k, v in enumerate(us)]))/(2*e)) for i in free)
    for name, wv in (('tapered alternating', np.array([(-1)**k*np.sin(np.pi*(k + 0.5)/n)**2 for k in range(n)])),
                     ('plain alternating', np.array([(-1.0)**k for k in range(n)]))):
        eps = mp.mpf(10)**-4
        up = list(us); um = list(us)
        for k, i in enumerate(free):
            up[i] += eps*wv[k]; um[i] -= eps*wv[k]
        q = (J(up) - 2*J0 + J(um))/eps**2/float(wv@wv)
        print('N=%d free=%d max|grad|=%s  %s: v^T H v/|v|^2 = %.3e   symbol f(pi)(J+1) = %.3e'
              % (N, n, mp.nstr(g, 2), name, float(q), -0.02729*(1.0/N)**3*(1 + float(J0))), flush=True)
