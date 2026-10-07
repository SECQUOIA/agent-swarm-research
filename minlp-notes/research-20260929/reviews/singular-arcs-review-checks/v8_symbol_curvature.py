"""Reviewer: curvature of the trapezoidal accessory symbol at omega = pi, and
the implied oscillation length of the alternating envelope.  If
f(pi + d) ~ f(pi) + (1/2) f2 d^2 with f(pi) < 0 < f2, the Jacobi equation for a
slowly varying envelope A of (-1)^i A_i is -(1/2) f2 A'' + f(pi) A = 0, whose
solutions oscillate with wavenumber d0 = sqrt(2|f(pi)|/f2) per stage; zeros
(conjugate points) are pi/d0 stages apart.  Uses the author's scheme code
catmix_schemes.py (symbol formula re-derived in the review) at h = 1/100,
1/200.  Also measures the envelope of the saved saddle controls."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import sys
import numpy as np
import mpmath as mp
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/theory-bangbang/singular'))
import catmix_schemes as S
mp.mp.dps = 50
for N in (100, 200):
    h = mp.mpf(1)/N
    FL = S.scheme('trapezoid', h)
    t, u, q, d = S.fixed_point(FL)
    f0 = S.symbol(d, q, mp.pi)
    dd = mp.mpf('0.01')
    f2 = (S.symbol(d, q, mp.pi + dd) - 2*f0 + S.symbol(d, q, mp.pi - dd))/dd**2
    d0 = mp.sqrt(2*abs(f0)/f2)
    print('N=%d f(pi)/h^3 = %.5f  f\'\'(pi)/h^3 = %.4f  d0 = %.4f rad/stage  zero spacing pi/d0 = %.1f stages, period %.1f'
          % (N, float(f0/h**3), float(f2/h**3), float(d0), float(mp.pi/d0), float(2*mp.pi/d0)), flush=True)
ROOT = (_PUBLIC_REPO + '/research-20260929/theory-bangbang/singular/logs/')
for N in (100, 200):
    u = np.load(ROOT + 'catmix%d_smooth_u.npy' % N)
    fr = np.where((u > 1e-9) & (u < 1 - 1e-9))[0]
    v = u[fr]
    a = np.array([(-1)**k*(v[k] - 0.25*(v[k-1] + 2*v[k] + v[k+1])) for k in range(1, len(v) - 1)])
    zc = np.where(np.sign(a[1:]) != np.sign(a[:-1]))[0]
    print('N=%d saved saddle: alternating envelope sign changes at arc stages %s; spacings %s'
          % (N, zc.tolist(), np.diff(zc).tolist()))
