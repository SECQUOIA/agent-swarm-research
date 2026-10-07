"""Vectorized interval arithmetic on numpy float64 arrays (rational operations only).

An interval is a pair (lo, hi) of arrays. Each +, -, *, / is computed in IEEE
round-to-nearest double arithmetic (correctly rounded, error <= 0.5 ulp) and the
result is moved one ulp outward with np.nextafter, so it encloses the exact result.
Decimal constants are enclosed by const(): nearest double widened by one ulp.
(Same construction as research-20260929/open-instances/ivnp.py.)
"""
import numpy as np

INF = np.inf


def dn(x):
    return np.nextafter(x, -INF)


def up(x):
    return np.nextafter(x, INF)


def const(s):
    x = np.float64(float(s))
    return (dn(x), up(x))


def pt(x):
    x = np.asarray(x, dtype=np.float64)
    return (x, x)


def add(a, b):
    return (dn(a[0] + b[0]), up(a[1] + b[1]))


def sub(a, b):
    return (dn(a[0] - b[1]), up(a[1] - b[0]))


def neg(a):
    return (-a[1], -a[0])


def mul(a, b):
    p1, p2, p3, p4 = a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]
    lo = np.minimum(np.minimum(p1, p2), np.minimum(p3, p4))
    hi = np.maximum(np.maximum(p1, p2), np.maximum(p3, p4))
    return (dn(lo), up(hi))


def div_pos(a, b):
    """a / b, requires b > 0 (asserted)."""
    assert np.all(b[0] > 0), "division by interval not bounded away from 0"
    q1, q2, q3, q4 = a[0] / b[0], a[0] / b[1], a[1] / b[0], a[1] / b[1]
    lo = np.minimum(np.minimum(q1, q2), np.minimum(q3, q4))
    hi = np.maximum(np.maximum(q1, q2), np.maximum(q3, q4))
    return (dn(lo), up(hi))


def scale(a, s):
    """a * s for a nonnegative exact float array s."""
    return (dn(a[0] * s), up(a[1] * s))


def poly(coefs, u):
    """Horner evaluation, coefs = [c0, c1, c2, ...] intervals, u interval."""
    r = coefs[-1]
    for c in reversed(coefs[:-1]):
        r = add(mul(r, u), c)
    return r


def take(a, idx):
    return (a[0][idx], a[1][idx])
