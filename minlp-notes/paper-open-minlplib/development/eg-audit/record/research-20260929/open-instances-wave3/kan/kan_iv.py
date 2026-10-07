"""Rigorous interval tools for the KAN bounds (numpy, outward rounding).

Builds on ia.NI from open-instances-wave2/small (each + - * / computed in IEEE
round-to-nearest and widened by one ulp).  Adds
  - frac_iv(q):   tight enclosure of a Fraction by doubles
  - iexp_pt(x):   rigorous exp of float arrays from + - * / only
                  (x = k ln2 + r, Taylor series with remainder bound)
  - silu ranges:  sigma(z) = z/(1+e^-z) and its first two derivatives
  - poly_range:   range enclosure of a polynomial (degree <= 3) over an interval
                  by the centered Taylor form
No libm transcendental result is trusted.
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import sys
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave2/small")
from ia import NI, dn, up  # noqa: E402,F401

INF = np.inf


def frac_iv(q):
    """[lo, hi] doubles with lo <= q <= hi (tight: exact if representable)."""
    q = Fr(q)
    x = float(q)          # correctly rounded (int/int true division)
    fx = Fr(x)
    if fx == q:
        return x, x
    if fx < q:
        return x, float(np.nextafter(x, INF))
    return float(np.nextafter(x, -INF)), x


def NIq(q):
    lo, hi = frac_iv(q)
    return NI(lo, hi)


def NIarr(qs):
    lo = np.array([frac_iv(q)[0] for q in qs])
    hi = np.array([frac_iv(q)[1] for q in qs])
    return NI(lo, hi)


# ---- ln 2 bracket (mpmath 60 digits, compared exactly with the doubles)
with mp.workdps(60):
    _l2 = mp.log(2)
    _l2f = float(_l2)
    _l2q = Fr(mp.nstr(_l2, 55, strip_zeros=False))
    _l2lo = _l2f if Fr(_l2f) <= _l2q - Fr(1, 10**50) else float(np.nextafter(_l2f, -INF))
    _l2hi = _l2f if Fr(_l2f) >= _l2q + Fr(1, 10**50) else float(np.nextafter(_l2f, INF))
LN2 = NI(_l2lo, _l2hi)
_NT = 18
_INVFACT = [NI(1.0) / NI(float(np.prod(np.arange(1, j + 1, dtype=np.float64)))) if j > 0 else NI(1.0)
            for j in range(_NT + 1)]   # j! exact in double for j <= 22
_REM = 1e-21   # >= |r|^(NT+1)/(NT+1)! * e^|r| for |r| <= 0.36


def iexp_pt(x):
    """enclosure of exp(x) for a float array x with |x| <= 700."""
    x = np.asarray(x, dtype=np.float64)
    assert np.all(np.abs(x) <= 700)
    k = np.rint(x / 0.6931471805599453)
    r = NI(x) - NI(k) * LN2
    assert np.all(np.maximum(np.abs(r.lo), np.abs(r.hi)) <= 0.36)
    acc = _INVFACT[_NT]
    for j in range(_NT - 1, -1, -1):
        acc = _INVFACT[j] + r * acc
    acc = NI(dn(acc.lo - _REM), up(acc.hi + _REM))
    ki = k.astype(np.int64)
    return NI(np.ldexp(acc.lo, ki), np.ldexp(acc.hi, ki))   # exact scaling (no under/overflow here)


def iexp(X):
    """exp over an interval (monotone)."""
    return NI(iexp_pt(X.lo).lo, iexp_pt(X.hi).hi)


def logistic(X):
    """s(z) = 1/(1+e^-z), increasing."""
    lo = (NI(1.0) / (NI(1.0) + iexp_pt(-X.lo))).lo
    hi = (NI(1.0) / (NI(1.0) + iexp_pt(-X.hi))).hi
    return NI(lo, hi)


def silu_pt(x):
    """enclosure of sigma(x) at float points x."""
    x = np.asarray(x, dtype=np.float64)
    return NI(x) / (NI(1.0) + iexp_pt(-x))


# critical point of sigma: sigma'(z) = s(z)(1 + z(1 - s(z))) = 0 near z* = -1.27846454...
def _dsilu_nat(Z):
    S = logistic(Z)
    return S * (NI(1.0) + Z * (NI(1.0) - S))


_ZS_LO, _ZS_HI = -1.27846454277, -1.27846454275
assert _dsilu_nat(NI(_ZS_LO, _ZS_LO)).hi < 0 and _dsilu_nat(NI(_ZS_HI, _ZS_HI)).lo > 0
_zsI = NI(_ZS_LO, _ZS_HI)
_zm = 0.5 * (_ZS_LO + _ZS_HI)
# mean-value form on the bracket: sigma(z) in sigma(zm) + sigma'(Zs) (Zs - zm)
SILU_MIN_LO = float((silu_pt(_zm) + _dsilu_nat(_zsI) * (_zsI - _zm)).lo)   # sigma >= SILU_MIN_LO
assert -0.27846454276108 < SILU_MIN_LO < -0.278464542761


def silu_range(Z):
    """enclosure of sigma over an interval (monotone decreasing then increasing)."""
    fa, fb = silu_pt(Z.lo), silu_pt(Z.hi)
    dec = Z.hi <= _ZS_LO
    inc = Z.lo >= _ZS_HI
    lo = np.where(dec, fb.lo, np.where(inc, fa.lo, SILU_MIN_LO))
    hi = np.where(dec, fa.hi, np.where(inc, fb.hi, np.maximum(fa.hi, fb.hi)))
    return NI(lo, hi)


def dsilu_range(Z):
    return _dsilu_nat(Z)


def d2silu_range(Z):
    S = logistic(Z)
    return S * (NI(1.0) - S) * (NI(2.0) + Z * (NI(1.0) - S * 2.0))


def poly_range(C, S):
    """Range enclosure of q(s) = sum_m C[m] s^m (C: list of NI, degree <= 3)
    over the interval S (NI), by the Taylor form at the midpoint of S."""
    deg = len(C) - 1
    sm = 0.5 * (S.lo + S.hi)
    rho = up(np.maximum(up(S.hi - sm), up(sm - S.lo)))
    rho = np.maximum(rho, 0.0)
    SM = NI(sm)
    # Taylor coefficients at sm: c_j = sum_{m>=j} binom(m,j) C[m] sm^(m-j)
    from math import comb
    T = []
    for j in range(deg + 1):
        acc = None
        for m in range(deg, j - 1, -1):
            term = C[m] * float(comb(m, j))
            acc = term if acc is None else acc * SM + term
        T.append(acc)
    R = NI(-rho, rho)
    out = T[0]
    if deg >= 1:
        out = out + T[1] * R
    if deg >= 2:
        r2 = up(rho * rho)
        out = out + T[2] * NI(np.zeros_like(r2), r2)
    if deg >= 3:
        r3 = up(up(rho * rho) * rho)
        out = out + T[3] * NI(-r3, r3)
    return out


def hull(A, B):
    return NI(np.minimum(A.lo, B.lo), np.maximum(A.hi, B.hi))


def meet(A, lo, hi):
    return NI(np.maximum(A.lo, lo), np.minimum(A.hi, hi))


# ---- faster rigorous exp: table of exp(j ln2/64) (mpmath, 50 digits, widened 1 ulp)
_TN = 64
with mp.workdps(50):
    _tbl = [mp.exp(mp.mpf(j) * mp.log(2) / _TN) for j in range(_TN)]
_TLO = np.array([float(np.nextafter(frac_iv(Fr(mp.nstr(t, 45)))[0], -INF)) for t in _tbl])
_THI = np.array([float(np.nextafter(frac_iv(Fr(mp.nstr(t, 45)))[1], INF)) for t in _tbl])
LN2_64 = NI(_l2lo / _TN, _l2hi / _TN)          # exact scaling by a power of 2
_NT2 = 8
_INVF2 = _INVFACT[:_NT2 + 1]
_REM2 = 1e-25   # >= |r|^9/9! e^|r| for |r| <= 0.0055


def iexp_pt_fast(x):
    """enclosure of exp(x), float array x, |x| <= 700 (table + degree-8 Taylor)."""
    x = np.asarray(x, dtype=np.float64)
    assert np.all(np.abs(x) <= 700)
    m = np.rint(x * (_TN / 0.6931471805599453))
    r = NI(x) - NI(m) * LN2_64
    assert np.all(np.maximum(np.abs(r.lo), np.abs(r.hi)) <= 0.0055)
    acc = _INVF2[_NT2]
    for j in range(_NT2 - 1, -1, -1):
        acc = _INVF2[j] + r * acc
    acc = NI(dn(acc.lo - _REM2), up(acc.hi + _REM2))
    mi = m.astype(np.int64)
    k = np.floor_divide(mi, _TN)
    j = mi - k * _TN
    acc = acc * NI(_TLO[j], _THI[j])
    return NI(np.ldexp(acc.lo, k), np.ldexp(acc.hi, k))
