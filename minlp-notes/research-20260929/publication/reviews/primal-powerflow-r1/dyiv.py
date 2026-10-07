"""Outward-rounded interval arithmetic on dyadic numbers (reviewer code, no mpmath).

An interval is a pair of Python ints (lo, hi) meaning [lo / 2^P, hi / 2^P].
Integer arithmetic is exact; every rounding goes outward (floor for lo, ceil
for hi; Python's >> and // floor toward -infinity).  sin and cos use the
Taylor series with the Lagrange remainder bound |x|^(n+1)/(n+1)! (all
derivatives of sin and cos are bounded by 1) at the midpoint m, then widen by
the half-width w, because |sin x - sin m| <= |x - m| (same for cos).
No assumption on any library is needed beyond exact integer arithmetic.
"""
from fractions import Fraction as Fr

P = 320
ONE = 1 << P


def ceil_shift(v, s):
    return -((-v) >> s)


def of_frac(q):
    q = Fr(q)
    return ((q.numerator << P) // q.denominator, -((-q.numerator << P) // q.denominator))


def lo_frac(a):
    return Fr(a[0], ONE)


def hi_frac(a):
    return Fr(a[1], ONE)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[1], a[1] - b[0])


def neg(a):
    return (-a[1], -a[0])


def mul(a, b):
    p = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return (min(p) >> P, ceil_shift(max(p), P))


def div_int(a, n):
    assert n > 0
    return (a[0] // n, -((-a[1]) // n))


def mag(a):
    return max(abs(a[0]), abs(a[1]))


def hull(a, b):
    return (min(a[0], b[0]), max(a[1], b[1]))


def _series(m, first, d0):
    """sum_k t_k with t_0 = first, t_k = -t_{k-1} m^2 / ((d0+2k-1)(d0+2k)) plus remainder;
    sin: first = m, d0 = 1; cos: first = 1, d0 = 0.  m is a point interval."""
    m2 = mul(m, m)
    t = first
    s = first
    k = 1
    M = abs(m[0]) // ONE + 2
    while True:
        a, b = d0 + 2 * k - 1, d0 + 2 * k
        t = div_int(neg(mul(t, m2)), a * b)
        # t is now an enclosure of the degree-(d0+2k) term, i.e. |m|^(d0+2k)/(d0+2k)! in magnitude
        if b > M and mag(t) < 4:          # term below 4 * 2^-P and the series is decreasing
            r = mag(t) + 1                 # Lagrange remainder of the polynomial before this term
            return (s[0] - r, s[1] + r)
        s = add(s, t)
        k += 1


def sin(x):
    m = (x[0] + x[1]) >> 1
    w = max(x[1] - m, m - x[0])
    s = _series((m, m), (m, m), 1)
    return (s[0] - w, s[1] + w)


def cos(x):
    m = (x[0] + x[1]) >> 1
    w = max(x[1] - m, m - x[0])
    s = _series((m, m), (ONE, ONE), 0)
    return (max(s[0] - w, -ONE), min(s[1] + w, ONE))
