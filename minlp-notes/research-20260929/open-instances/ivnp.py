"""Minimal vectorized interval arithmetic on numpy float64 arrays.

An interval is a pair (lo, hi) of arrays. Every basic operation (+, -, *, /, sqrt)
is computed in round-to-nearest IEEE double arithmetic (correctly rounded, error at
most 0.5 ulp) and the result is widened outward by one ulp with np.nextafter, so the
returned interval contains the exact result. Decimal constants are enclosed by
const(), which widens the nearest double by one ulp on each side.
"""
import numpy as np

INF = np.inf


def dn(x):
    return np.nextafter(x, -INF)


def up(x):
    return np.nextafter(x, INF)


def const(x):
    x = np.float64(x)
    return (dn(x), up(x))


def point(x):
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
    """a / b for b > 0 (asserted)."""
    assert np.all(b[0] > 0)
    q1, q2, q3, q4 = a[0] / b[0], a[0] / b[1], a[1] / b[0], a[1] / b[1]
    lo = np.minimum(np.minimum(q1, q2), np.minimum(q3, q4))
    hi = np.maximum(np.maximum(q1, q2), np.maximum(q3, q4))
    return (dn(lo), up(hi))


def sqr(a):
    lo2, hi2 = a[0] * a[0], a[1] * a[1]
    hi = up(np.maximum(lo2, hi2))
    lo = np.where((a[0] <= 0) & (a[1] >= 0), 0.0, dn(np.minimum(lo2, hi2)))
    return (np.maximum(lo, 0.0), hi)


def sqrt(a):
    assert np.all(a[0] >= 0)
    return (np.maximum(dn(np.sqrt(a[0])), 0.0), up(np.sqrt(a[1])))


def absval(a):
    lo = np.where(a[0] >= 0, a[0], np.where(a[1] <= 0, -a[1], 0.0))
    hi = np.maximum(np.abs(a[0]), np.abs(a[1]))
    return (lo, hi)


def sum_lo(a):
    """Rigorous lower bound of the sum of the lower ends (sequential, rounded down each step)."""
    s = np.float64(0.0)
    for v in np.ravel(a):
        s = dn(s + v)
    return s


def quad_min_lo(A, B, lo, hi):
    """Lower bound of min_{v in [lo, hi]} A v^2 + B v for interval coefficients A, B
    (arrays broadcastable). Uses A v^2 >= A_lo v^2. If A_lo > 0 and the stationary
    point may lie in [lo, hi], the global minimum -B^2/(4 A_lo) (lower end) is used;
    otherwise the minimum over the two endpoints (correct for convex functions whose
    minimizer lies outside, and for concave or linear functions)."""
    a = (A[0], A[0])
    e1 = add(mul(a, sqr(point(lo))), mul(B, point(lo)))[0]
    e2 = add(mul(a, sqr(point(hi))), mul(B, point(hi)))[0]
    m = np.minimum(e1, e2)
    conv = A[0] > 0
    with np.errstate(divide="ignore", invalid="ignore"):
        s_lo = np.where(conv, -B[1] / (2 * A[0]), 0.0)
        s_hi = np.where(conv, -B[0] / (2 * A[0]), 0.0)
        # widen generously (the enclosure only decides whether the stationary value is used)
        s_lo, s_hi = s_lo - 1e-9 * (1 + np.abs(s_lo)), s_hi + 1e-9 * (1 + np.abs(s_hi))
        inside = conv & (s_hi >= lo) & (s_lo <= hi)
        b2hi = np.maximum(B[0] * B[0], B[1] * B[1])
        stat = dn(-up(up(b2hi) / dn(4 * A[0])))
    return np.where(inside, np.minimum(m, stat), m)
