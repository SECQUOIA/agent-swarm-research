import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

NINF, PINF = -np.inf, np.inf
PAD = 1e-300


def dn(v):
    return np.nextafter(v, NINF) - PAD


def up(v):
    return np.nextafter(v, PINF) + PAD


def encl(q):
    """two doubles around the exact rational q."""
    f = float(q)
    lo = f if Fr(f) <= q else float(np.nextafter(f, NINF))
    hi = f if Fr(f) >= q else float(np.nextafter(f, PINF))
    assert Fr(lo) <= q <= Fr(hi)
    return lo, hi


def iadd(al, ah, bl, bh):
    return dn(al + bl), up(ah + bh)


def imul(al, ah, bl, bh):
    p1, p2, p3, p4 = al * bl, al * bh, ah * bl, ah * bh
    return dn(np.minimum(np.minimum(p1, p2), np.minimum(p3, p4))), up(np.maximum(np.maximum(p1, p2), np.maximum(p3, p4)))


def isqr(al, ah):
    l2, h2 = al * al, ah * ah
    lo = np.where(al >= 0, l2, np.where(ah <= 0, h2, 0.0))
    hi = np.maximum(l2, h2)
    return np.where((al >= 0) | (ah <= 0), dn(lo), 0.0), up(hi)


LN2_LO, LN2_HI = encl(Fr("0.693147180559945309417232121458176568075500134360255254120680009493393621969694715605863326996418687542001481021"))
NTAY = 14
REM = 1e-18


def _exp_bound(x, upper):
    """rigorous lower (upper=False) or upper (upper=True) bound of exp(x), x a float array <= 1."""
    x = np.asarray(x, float)
    assert np.all(x <= 1.0) and not np.any(np.isnan(x))
    small = x < -700
    xs = np.where(small, 0.0, x)
    k = np.rint(xs / 0.6931471805599453)
    pl, ph = imul(k, k, LN2_LO, LN2_HI)
    rl, rh = dn(xs - ph), up(xs - pl)
    assert np.all(np.abs(rl) <= 0.35) and np.all(np.abs(rh) <= 0.35)
    yl, yh = np.ones_like(xs), np.ones_like(xs)
    for j in range(NTAY, 0, -1):
        tl, th = imul(rl, rh, yl, yh)
        tl, th = dn(tl / j), up(th / j)
        yl, yh = iadd(1.0, 1.0, tl, th)
    ki = k.astype(np.int64)
    if upper:
        v = np.ldexp(up(yh + REM), ki)
        return np.where(small, 1e-300, v)
    v = np.ldexp(dn(yl - REM), ki)
    return np.where(small, 0.0, np.maximum(v, 0.0))


def iexp(al, ah):
    return _exp_bound(al, False), _exp_bound(ah, True)



if __name__ == "__main__":
    import time
    import mpmath as mp
    rng = np.random.default_rng(1)
    for lo_, hi_ in [(-700, -600), (-50, 0), (-1, 1)]:
        x = rng.uniform(lo_, hi_, 200000)
        t0 = time.time(); l = _exp_bound(x, False); h = _exp_bound(x, True); dt = time.time() - t0
        w = (h - l) / l
        print(f"x in [{lo_},{hi_}]: max rel width {w.max():.3e}, median {np.median(w):.3e}; {dt/len(x)*1e9:.0f} ns/arg (both ends)")
