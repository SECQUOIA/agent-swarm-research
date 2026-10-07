"""One-off probe: cmax anisotropic residual lambda_min(M - 2 eps I - ββ^T/|σ|) on example A near tau+,
for two differencing schemes and several steps (step = frac * (t - tau))."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import sys, os, numpy as np, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/reviews/window-exactness-confirm-r2-checks'))
from d1_shE import *
p = EX["A"]
Pf, dg = continuous_family(p, EPS, delta1=None)
th = find_switch(p)[0]
sa, sb = sigma_pieces(p, th)
def res(s, lo, hi, scheme, frac):
    hs = min(1e-6, frac * (s - lo), frac * (hi - s))
    if scheme == 5:
        dP = (-Pf(s + 2 * hs) + 8 * Pf(s + hs) - 8 * Pf(s - hs) + Pf(s - 2 * hs)) / (12 * hs)
    else:
        dP = (Pf(s + hs) - Pf(s - hs)) / (2 * hs)
    P = Pf(s)
    M = dP + Am.T @ P + P @ Am + p.Hxx; M = (M + M.T) / 2
    beta = P @ b - p.w
    sg = abs(float(sb(s))) if s > th else abs(float(sa(s)))
    R = M - 2 * EPS * np.eye(2) - (1.0 / sg) * np.outer(beta, beta)
    return np.linalg.eigvalsh(R)[0], np.linalg.norm(M), beta @ beta / sg
for s in [1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.04]:
    for scheme, frac in [(5, 0.05), (2, 0.1), (2, 0.01), (5, 0.005)]:
        r = res(th + s, th, th + 0.05, scheme, frac)
        print(f"s={s:.0e} scheme={scheme} frac={frac}: aniso={r[0]:.3e}  |M|={r[1]:.3e}  rel={abs(r[0])/r[1]:.2e}")
# where is my max?
g = 1e-4
for lo, hi, grid in [(0, th, np.linspace(g, th - g, 2500)), (th, th + 0.05, th + np.geomspace(1e-8, 0.05 - g, 2500)), (th + 0.05, p.T, np.linspace(th + 0.05 + g, p.T - g, 2500))]:
    vals = [(abs(res(s, lo, hi, 5, 0.05)[0]), s) for s in grid]
    m = max(vals)
    print("segment", lo, hi, "max |aniso|", m[0], "at t - tau =", m[1] - th)
