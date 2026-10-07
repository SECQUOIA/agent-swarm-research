"""Rigorous audit of the exp and integer-power results used by the independent eg certifier.

Written for the eg-audit rerun (2026-10-04).  It shares no code with the author's egfast.fexp,
kan_iv or ia modules, nor with review r1's own_ia.py.  It uses only IEEE-754 binary64
operations (+, -, *, comparisons, rint, floor, integer bit operations) and exact Python
integer/Fraction arithmetic; no libm or mpmath result is trusted.  The arithmetic hypothesis is
(H0): numpy float64 arithmetic is binary64 with round-to-nearest-even and gradual underflow.

Notation: u = 2^-53.  For a real z whose rounding fl(z) is computed with one IEEE operation,
|fl(z) - z| <= u|fl(z)| + 2^-1075 and |fl(z) - z| <= u|z| + 2^-1075 (normal or subnormal result,
no overflow).

1. exp_ok(x, y): for float arrays x (arguments) and y (= np.exp(x) as used by the certifier),
   returns a boolean array that is True only where the property
       (E)  x >= -708  and  |y - e^x| <= EPS_EXP * e^x,     or
            x <  -708  and  0 <= y <= 2^-1020
   is PROVED.  (The certifier needs only y >= 0 for x < -708; see eg-lemma-A1.md.)
   Method for x in [-708, 709] (enclosure of e^x):
     m  = rint(fl(x * INV_L))  (any integer; correctness does not depend on it),
     p1 = m * L1               (exact: |m| < 2^17 is checked and L1 has 36 significant bits),
     s  = fl(x - p1),  p2 = fl(m * L2),  r = fl(s - p2),  checked |r| <= RMAX = 0.0055,
     where L1 + L2 approximates L = ln2/64 with |L - L1 - L2| <= DL (bounded exactly from the
     series ln 2 = sum_k 1/(k 2^k)).  Then x = m L + r_true with
         |r_true - r| <= u(|r| + |s| + |p2|) + |m| DL + 3 * 2^-1075 <= DR   (a-priori constant).
     H = Horner(c_7, ..., c_0; r) with floats c_i ~ 1/i!.  Higham's Horner bound (Accuracy and
     Stability of Numerical Algorithms, 2nd ed., 2002, Sec. 5.1: gamma_2n sum |c_i||r|^i), plus
     the coefficient errors, the Taylor truncation and an underflow term give |e^r - H| <= EH.
     With m = 64k + j (0 <= j < 64): e^x = 2^k * 2^(j/64) * e^r_true, and
         lo = fl(fl(TLO_j * H) * CLO) * 2^k  <=  e^x  <=  hi = fl(fl(THI_j * H) * CHI) * 2^k,
     where TLO_j <= 2^(j/64) <= THI_j are proved by exact integer arithmetic (T^64 vs 2^j) and
     the float constants CLO, CHI absorb EH, DR and the two product roundings (checked exactly).
     The scalings by 2^k are exact because every result is a normal number (x >= -708).
     Finally  y <= fl(lo * FUP)  and  y >= fl(hi * FDN)  imply (E), with FUP <= (1+eps)/(1+u)
     and FDN >= (1-eps)/(1-u) checked exactly.
2. pow_ok(x, k, y) for k in {2, 3, 4} and y = x ** k as computed by numpy:
       (P)  x >= 0 and |y - x^k| <= EPS_POW * x^k
   is proved by comparison with z = fl(x*x) (k = 2), fl(fl(x*x)*x) (k = 3),
   fl(fl(x*x)*fl(x*x)) (k = 4), for which |z - x^k| <= GZ x^k with GZ = (1+u)^3 - 1 when
   x in [2^-250, 2^250] (no underflow or overflow).  If |fl(y - z)| <= fl(CP * z) then y lies in
   [z/2, 2z], so y - z is exact (Sterbenz) and |y - x^k| <= (CP (1+GZ)(1+u) + GZ) x^k <= eps x^k.
   x = 0 requires y = 0 exactly.  0 < x < 2^-250 is checked in exact rational arithmetic.
   Any other x (negative, NaN, x > 2^250) fails the check.
All constants are derived at import time and every inequality used above is asserted in exact
rational arithmetic (self_test); importing this module fails if any of them does not hold.
"""
from fractions import Fraction as Fr
from math import factorial

import numpy as np

EPS_EXP = Fr(1, 10 ** 14)      # audited relative error bound for exp (exact rational 1e-14)
EPS_POW = Fr(1, 10 ** 14)      # audited relative error bound for integer powers
U = Fr(1, 2 ** 53)
TINY = Fr(1, 2 ** 1075)        # half the smallest subnormal spacing
XMIN, XMAX = -708.0, 709.0     # domain of the enclosure (normal results)
YTINY = 2.0 ** -1020           # bound on y for x < -708
RMAX = 0.0055
MMAX = 2 ** 17
DEG = 7


def _down(q):
    """largest float <= q (q a Fraction)."""
    f = float(q)
    while Fr(f) > q:
        f = float(np.nextafter(f, -np.inf))
    while Fr(float(np.nextafter(f, np.inf))) <= q:
        f = float(np.nextafter(f, np.inf))
    return f


def _up(q):
    """smallest float >= q."""
    return -_down(-q)


def _exp_upper(y, terms=30):
    """exact rational upper bound of e^y for 0 <= y <= 1."""
    s = sum(Fr(y) ** i / factorial(i) for i in range(terms))
    return s + 2 * Fr(y) ** terms / factorial(terms)


# ---------------------------------------------------------------- constants (exact derivation)
_N_SER = 400
_S = sum(Fr(1, k * 2 ** k) for k in range(1, _N_SER + 1))
_LN2_LO, _LN2_HI = _S, _S + Fr(1, _N_SER * 2 ** _N_SER)       # ln 2 in [_LN2_LO, _LN2_HI]
_L_LO, _L_HI = _LN2_LO / 64, _LN2_HI / 64                    # L = ln2/64 in [_L_LO, _L_HI]
_L1q = Fr(int(_L_LO * 2 ** 42), 2 ** 42)                     # 36 significant bits
L1 = float(_L1q)
L2 = float(_L_LO - _L1q)
DL = max(abs(_L_LO - _L1q - Fr(L2)), abs(_L_HI - _L1q - Fr(L2)))
INV_L = float(1 / _L_LO)
_P2MAX = MMAX * abs(Fr(L2)) * (1 + U)
# |r_true - r| <= u(|r| + |s| + |p2|) + |m| DL + 3 TINY with |s| <= |p2| + |r|(1+u) + TINY
DR = U * (Fr(RMAX) + (_P2MAX + Fr(RMAX) * (1 + U) + TINY) + _P2MAX) + MMAX * DL + 4 * TINY
COEF = [float(Fr(1, factorial(i))) for i in range(DEG + 1)]
_EXP_RMAX = _exp_upper(Fr(RMAX))
_GAMMA_2N = 2 * DEG * U / (1 - 2 * DEG * U)                  # gamma_14
_EC = sum(abs(Fr(COEF[i]) - Fr(1, factorial(i))) * Fr(RMAX) ** i for i in range(DEG + 1))
_TRUNC = Fr(RMAX) ** (DEG + 1) / factorial(DEG + 1) * _EXP_RMAX
_ABS_CI = sum(Fr(COEF[i]) * Fr(RMAX) ** i for i in range(DEG + 1))
EH = _GAMMA_2N * _ABS_CI + _EC + _TRUNC + 2 ** 4 * TINY       # |e^r - H| <= EH for |r| <= RMAX
_HMIN = 1 - Fr(RMAX) - EH                                    # e^-RMAX >= 1 - RMAX, so H >= _HMIN
RHO_H = EH / _HMIN                                           # |e^r - H| <= RHO_H * H
CLO = _down((1 - RHO_H) * (1 - DR) / (1 + U) ** 2)
CHI = _up((1 + RHO_H) * (1 + 2 * DR) / (1 - U) ** 2)


def _table():
    lo, hi = [], []
    for j in range(64):
        f = float(2.0 ** (j / 64))
        while Fr(f) ** 64 > 2 ** j:
            f = float(np.nextafter(f, -np.inf))
        while Fr(float(np.nextafter(f, np.inf))) ** 64 <= 2 ** j:
            f = float(np.nextafter(f, np.inf))
        lo.append(f)
        hi.append(f if Fr(f) ** 64 == 2 ** j else float(np.nextafter(f, np.inf)))
    return np.array(lo), np.array(hi)


TLO, THI = _table()
FUP = _down((1 + EPS_EXP) / (1 + U))
FDN = _up((1 - EPS_EXP) / (1 - U))
GZ = (1 + U) ** 3 - 1
CP = _down((EPS_POW - GZ) / ((1 + GZ) * (1 + U)))
PLO, PHI = 2.0 ** -250, 2.0 ** 250


def self_test():
    """assert every inequality the proofs in the module docstring use (exact arithmetic)."""
    assert _LN2_LO < _LN2_HI and _LN2_HI - _LN2_LO < Fr(1, 10 ** 100)
    assert _L1q.denominator <= 2 ** 42 and _L1q.numerator < 2 ** 36 and Fr(L1) == _L1q
    assert DL < Fr(1, 10 ** 27)
    # m * L1 exact for |m| < 2^17: |m * numerator(L1)| < 2^53
    assert MMAX * _L1q.numerator < 2 ** 53
    # every x in [XMIN, XMAX] gives |m| < MMAX and k = floor(m / 64) in [-1022, 1023]
    mx = int(abs(Fr(XMIN)) * Fr(INV_L) * (1 + 4 * U)) + 2
    assert mx < MMAX and -(mx // 64 + 1) >= -1022 and (int(Fr(XMAX) * Fr(INV_L) * (1 + 4 * U)) + 2) // 64 <= 1022
    assert DR < Fr(1, 10 ** 17)
    assert EH < Fr(2, 10 ** 15) and RHO_H < Fr(2, 10 ** 15)
    assert Fr(CLO) * (1 + U) ** 2 <= (1 - RHO_H) * (1 - DR)          # lower enclosure
    assert Fr(CHI) * (1 - U) ** 2 >= (1 + RHO_H) * (1 + 2 * DR)      # upper enclosure
    assert 2 * DR < 1                                                # e^DR <= 1 + 2 DR
    for j in range(64):
        assert Fr(TLO[j]) ** 64 <= 2 ** j <= Fr(THI[j]) ** 64
        assert Fr(THI[j]) - Fr(TLO[j]) <= 2 * U * Fr(TLO[j])
    assert 1 <= TLO.min() and THI.max() < 2
    # Normal range.  The unscaled lower end v = fl(fl(TLO_j H) CLO) satisfies
    # v 2^k >= e^x * W with W = (TLO_j/THI_j) CLO (1-u)^2 / ((1+RHO_H)(1+2DR)) >= 1 - 1e-14, and
    # e^x >= e^-708 > 2^-1022 / (1 - 1e-14); so v 2^k (and lo, hi) are normal and the
    # scaling by 2^k is exact.  e <= E_UP (series with tail bound), hence e^-708 >= E_UP^-708.
    w = min(Fr(TLO[j]) / Fr(THI[j]) for j in range(64)) * Fr(CLO) * (1 - U) ** 2 / ((1 + RHO_H) * (1 + 2 * DR))
    assert w >= 1 - Fr(1, 10 ** 14)
    e_up = sum(Fr(1, factorial(i)) for i in range(30)) + Fr(2, factorial(30))
    assert Fr(1) / e_up ** 708 * (1 - Fr(1, 10 ** 14)) > Fr(1, 2 ** 1022)
    assert Fr(XMIN) == -708 and Fr(XMAX) == 709
    # no overflow: e^709 * (upper factor) < largest float
    assert _exp_upper(Fr(1)) ** 709 * Fr(THI.max()) / Fr(TLO.min()) * Fr(CHI) * (1 + U) ** 2 < Fr(2) ** 1024 * (1 - U)
    assert Fr(FUP) * (1 + U) <= 1 + EPS_EXP and Fr(FDN) * (1 - U) >= 1 - EPS_EXP
    assert Fr(CP) > 0 and Fr(CP) * (1 + GZ) * (1 + U) + GZ <= EPS_POW
    assert Fr(YTINY) <= Fr(1, 10 ** 300)
    return True


def exp_enclosure(x):
    """lo <= e^x <= hi for float arrays x with XMIN <= x <= XMAX; valid[i] False where the
    reduction bound |r| <= RMAX or |m| < MMAX fails (then lo, hi are meaningless)."""
    x = np.asarray(x, dtype=np.float64)
    m = np.rint(x * INV_L)
    s = x - m * L1
    p2 = m * L2
    r = s - p2
    valid = (np.abs(r) <= RMAX) & (np.abs(m) < MMAX)
    h = np.full(x.shape, COEF[DEG])
    for i in range(DEG - 1, -1, -1):
        h = COEF[i] + r * h
    mi = np.where(valid, m, 0.0).astype(np.int64)
    k = mi >> 6
    j = mi - (k << 6)
    two_k = ((k + 1023) << 52).view(np.float64)
    lo = ((TLO[j] * h) * CLO) * two_k
    hi = ((THI[j] * h) * CHI) * two_k
    return lo, hi, valid


def exp_ok(x, y):
    """True where property (E) is proved for (x, y)."""
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    ok = np.zeros(x.shape, bool)
    small = x < XMIN
    ok[small] = (y[small] >= 0.0) & (y[small] <= YTINY)
    mid = (x >= XMIN) & (x <= XMAX)
    if mid.any():
        xm, ym = x[mid], y[mid]
        lo, hi, valid = exp_enclosure(xm)
        ok[mid] = valid & (ym <= lo * FUP) & (ym >= hi * FDN)
    return ok


def pow_ok(x, k, y):
    """True where property (P) is proved for y = x ** k, k in {2, 3, 4}."""
    assert k in (2, 3, 4)
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    x2 = x * x
    z = x2 if k == 2 else (x2 * x if k == 3 else x2 * x2)
    rng = (x >= PLO) & (x <= PHI)
    ok = rng & (np.abs(y - z) <= CP * z)
    ok |= (x == 0.0) & (y == 0.0)
    rare = np.flatnonzero((x > 0.0) & (x < PLO))
    for i in rare:                      # exact rational check (never expected in the eg runs)
        xi = Fr(float(x.flat[i]))
        ex = xi ** k
        ok.flat[i] = abs(Fr(float(y.flat[i])) - ex) <= EPS_POW * ex
    return ok


class Audit:
    """Collects the checks of one Model.natural or Model.taylor call (begin ... end) and turns
    them into one flag per box (axis 0 of every per-box array).  Keeps element counts per call
    site and up to max_examples violation examples."""

    def __init__(self, max_examples=50):
        self.n_checked = {}
        self.n_viol = {}
        self.examples = []
        self.max_examples = max_examples
        self.bad = None

    def begin(self, n_boxes):
        self.bad = np.zeros(n_boxes, bool)

    def end(self):
        b, self.bad = self.bad, None
        return b

    def _note(self, site, ok, x, y, perbox):
        self.n_checked[site] = self.n_checked.get(site, 0) + ok.size
        if ok.all():
            return
        nv = int((~ok).sum())
        self.n_viol[site] = self.n_viol.get(site, 0) + nv
        if perbox:
            self.bad |= (~ok).reshape(len(self.bad), -1).any(1)
        else:
            self.bad[:] = True
        for i in np.flatnonzero(~ok.ravel())[: max(0, self.max_examples - len(self.examples))]:
            self.examples.append((site, float(np.asarray(x).ravel()[i]), float(np.asarray(y).ravel()[i])))

    def exp(self, x, y, site):
        self._note(site, exp_ok(x, y), x, y, True)

    def pow(self, x, k, y, site, perbox=True):
        self._note(site, pow_ok(x, k, y), x, y, perbox)


assert self_test()
