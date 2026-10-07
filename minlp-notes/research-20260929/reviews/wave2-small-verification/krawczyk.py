"""Generic Krawczyk existence test for a square subsystem of an OSIL model.

Unknowns U (indices), all other variables fixed at exact values (given as
Fractions / decimal strings, enclosed with mpmath iv).  Rows `rows` (equalities,
len == len(U)).  Centre xt (doubles), radius r (doubles), X = xt + [-r, r].

Test (midpoint-radius form of Krawczyk's operator):
    beta = |R Fc| + |R| Fr + |I - R Jc| r + |R| Jr r  <  r   (componentwise)
where F(xt) in Fc +- Fr and J(X) in Jc +- Jr are rigorous iv enclosures
(forward-mode interval AD on the OSIL trees, 40 digits), R ~ inv(Jc) is any
double matrix.  Then K(X) is inside int(X), so X contains exactly one solution
of F(x, p) = 0 for every parameter value p in its enclosure (in particular for
the exact decimals).
Floating-point products are bounded rigorously: for nonnegative data the
computed matrix-vector product underestimates the exact one by at most a factor
(1 - gamma_n), gamma_n = n u/(1 - n u) (any summation order, with or without
FMA); signed products carry the error gamma_n |R||v|.  All such bounds are
inflated by SAFE = 1 + 1e-6 (>> 2 gamma_n for n <= 3000) plus 1e-300 absolute
(underflow).  Assumes IEEE double arithmetic in numpy/BLAS.
"""
import math

import mpmath
import numpy as np
from mpmath import iv

import common

U_ROUND = 2.0 ** -53
SAFE = 1 + 1e-6
TINY = 1e-300


class AD:
    __slots__ = ("v", "d")

    def __init__(self, v, d=None):
        self.v = v
        self.d = d or {}

    def _lift(o):
        return o if isinstance(o, AD) else AD(o)

    def __add__(a, b):
        b = AD._lift(b)
        d = dict(a.d)
        for k, x in b.d.items():
            d[k] = d[k] + x if k in d else x
        return AD(a.v + b.v, d)

    __radd__ = __add__

    def __neg__(a):
        return AD(-a.v, {k: -x for k, x in a.d.items()})

    def __sub__(a, b):
        return a + (-AD._lift(b))

    def __rsub__(a, b):
        return AD._lift(b) + (-a)

    def __mul__(a, b):
        b = AD._lift(b)
        d = {k: x * b.v for k, x in a.d.items()}
        for k, x in b.d.items():
            d[k] = d[k] + a.v * x if k in d else a.v * x
        return AD(a.v * b.v, d)

    __rmul__ = __mul__

    def __truediv__(a, b):
        b = AD._lift(b)
        q = a.v / b.v
        d = {k: x / b.v for k, x in a.d.items()}
        for k, x in b.d.items():
            t = -q * x / b.v
            d[k] = d[k] + t if k in d else t
        return AD(q, d)

    def __rtruediv__(a, b):
        return AD._lift(b) / a


def ad_exp(a):
    e = iv.exp(a.v)
    return AD(e, {k: e * x for k, x in a.d.items()})


def ad_square(a):
    return AD(a.v ** 2, {k: 2 * a.v * x for k, x in a.d.items()})


def ev_ad(t, x):
    op = t[0]
    if op == "num":
        return AD(iv.mpf(t[1]))
    if op == "var":
        v = x[t[1]]
        return v if t[2] == "1" else v * iv.mpf(t[2])
    a = [ev_ad(c, x) for c in t[1:]]
    if op == "sum":
        s = a[0]
        for b in a[1:]:
            s = s + b
        return s
    if op == "product":
        s = a[0]
        for b in a[1:]:
            s = s * b
        return s
    if op == "minus":
        return a[0] - a[1]
    if op == "negate":
        return -a[0]
    if op == "divide":
        return a[0] / a[1]
    if op == "square":
        return ad_square(a[0])
    if op == "exp":
        return ad_exp(a[0])
    raise NotImplementedError(op)


def row_ad(row, x):
    s = AD(iv.mpf(row["constant"]))
    for j, c in row["lin"].items():
        s = s + x[j] * iv.mpf(c)
    for i, j, c in row["quad"]:
        s = s + x[i] * x[j] * iv.mpf(c)
    if row["nl"] is not None:
        s = s + ev_ad(row["nl"], x)
    return s


def enclose_to_float(I):
    """interval -> (mid double, radius double) with [mid - rad, mid + rad] containing I."""
    with mpmath.workprec(300):  # endpoint copies are exact at 300 bits (iv works at ~136 bits)
        a, b = mpmath.mpf(I.a), mpmath.mpf(I.b)
        c = float((a + b) / 2)
        rad = max(b - mpmath.mpf(c), mpmath.mpf(c) - a)
    return c, float(np.nextafter(float(rad), np.inf)) if rad > 0 else 0.0


def fixed_iv(v):
    if isinstance(v, str):
        return iv.mpf(v)
    return iv.mpf(v.numerator) / iv.mpf(v.denominator)  # Fraction


def build_x(nvar, U, xU_iv, fixed, with_ad):
    x = [None] * nvar
    for j, v in fixed.items():
        x[j] = AD(fixed_iv(v)) if with_ad else AD(fixed_iv(v))
    for k, j in enumerate(U):
        x[j] = AD(xU_iv[k], {k: iv.mpf(1)}) if with_ad else AD(xU_iv[k])
    assert all(v is not None for v in x)
    return x


def residual(m, rows, U, xt, fixed):
    x = build_x(len(m["names"]), U, [iv.mpf(float(v)) for v in xt], fixed, False)
    Fc, Fr = np.zeros(len(rows)), np.zeros(len(rows))
    for i, r in enumerate(rows):
        row = m["cons"][r]
        val = row_ad(row, x).v - iv.mpf(row["lb"])
        Fc[i], Fr[i] = enclose_to_float(val)
    return Fc, Fr


def jacobian(m, rows, U, X_iv, fixed):
    n = len(U)
    x = build_x(len(m["names"]), U, X_iv, fixed, True)
    Jc, Jr = np.zeros((n, n)), np.zeros((n, n))
    for i, r in enumerate(rows):
        g = row_ad(m["cons"][r], x).d
        for k, I in g.items():
            Jc[i, k], Jr[i, k] = enclose_to_float(I)
    return Jc, Jr


def newton_polish(m, rows, U, x0, fixed, iters=4):
    """double-precision Newton with residuals from 40-digit interval midpoints (not rigorous)."""
    x = np.array(x0, float)
    for _ in range(iters):
        Fc, _ = residual(m, rows, U, x, fixed)
        Jc, _ = jacobian(m, rows, U, [iv.mpf(float(v)) for v in x], fixed)
        x = x - np.linalg.solve(Jc, Fc)
    Fc, _ = residual(m, rows, U, x, fixed)
    return x, float(np.abs(Fc).max())


def test(m, rows, U, xt, r, fixed):
    """returns dict with ok flag and the worst ratio max(beta/r)."""
    n = len(U)
    assert len(rows) == n
    iv.dps = 40
    Fc, Fr = residual(m, rows, U, xt, fixed)
    lo = np.nextafter(xt - r, -np.inf)
    hi = np.nextafter(xt + r, np.inf)
    X_iv = [iv.mpf([float(lo[k]), float(hi[k])]) for k in range(n)]
    # exact inner / outer radii of X about xt (X - xt within [-r_out, r_out]; X contains xt +- r_in)
    r_in, r_out = np.zeros(n), np.zeros(n)
    with mpmath.workprec(200):
        for k in range(n):
            dl = mpmath.mpf(float(xt[k])) - mpmath.mpf(float(lo[k]))
            dh = mpmath.mpf(float(hi[k])) - mpmath.mpf(float(xt[k]))
            r_in[k] = np.nextafter(float(min(dl, dh)), -np.inf)
            r_out[k] = np.nextafter(float(max(dl, dh)), np.inf)
    assert np.all(r_in > 0)
    Jc, Jr = jacobian(m, rows, U, X_iv, fixed)
    # centre-point Jacobian for R
    Jp, _ = jacobian(m, rows, U, [iv.mpf(float(v)) for v in xt], fixed)
    R = np.linalg.inv(Jp)
    gam = n * U_ROUND / (1 - n * U_ROUND)
    aR = np.abs(R)
    a1 = np.abs(R @ Fc) + gam * (aR @ np.abs(Fc))
    a2 = aR @ Fr
    M = R @ Jc
    E = np.eye(n) - M
    a3 = np.abs(E) @ r_out + gam * (aR @ (np.abs(Jc) @ r_out))
    a4 = aR @ (Jr @ r_out)
    beta = SAFE * SAFE * (a1 + a2 + a3 + a4) + TINY
    ratio = beta / r_in
    return dict(ok=bool(np.all(beta < r_in)), worst_ratio=float(ratio.max()), n=n,
                max_resid_mid=float(np.abs(Fc).max()), max_resid_rad=float(Fr.max()),
                max_I_minus_RJ_row=float((np.abs(E).sum(axis=1)).max()),
                max_Jr=float(Jr.max()), max_absR=float(aR.max()),
                terms_max=[float(a1.max()), float(a2.max()), float(a3.max()), float(a4.max())]), X_iv
