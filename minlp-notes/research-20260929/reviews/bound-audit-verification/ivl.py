"""Small outward-rounded interval arithmetic with exact rational endpoints.

Endpoints are Fractions. After each operation the endpoints are rounded
outward to dyadic numbers with PREC significant bits, which keeps them short.
+, -, *, / and integer powers are exact before the outward rounding.
sqrt uses integer square roots (exact floor/ceil). exp and ln use mpmath at
EXTRA_DIGITS decimal digits, and the result is widened by a relative 1e-60
(far above mpmath's error at that precision) before outward rounding.
"""
from fractions import Fraction as F
from math import isqrt

import mpmath

PREC = 200
mpmath.mp.dps = 90
PAD = F(1, 10 ** 60)


def _rd(x, up):
    """Round Fraction x to a dyadic with about PREC bits, down or up."""
    if x == 0:
        return F(0)
    n, d = x.numerator, x.denominator
    s = PREC - (abs(n).bit_length() - d.bit_length())
    if s >= 0:
        num, den = n << s, d
    else:
        num, den = n, d << (-s)
    k = num // den if not up else -((-num) // den)
    return F(k, 1 << s) if s >= 0 else F(k << (-s))


class I:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None, exact=True):
        lo = F(lo)
        hi = lo if hi is None else F(hi)
        assert lo <= hi, (lo, hi)
        self.lo, self.hi = lo, hi

    @staticmethod
    def of(v):
        return v if isinstance(v, I) else I(v)

    @staticmethod
    def out(lo, hi):
        r = I.__new__(I)
        r.lo, r.hi = _rd(lo, False), _rd(hi, True)
        return r

    def __repr__(self):
        return f"[{float(self.lo)!r}, {float(self.hi)!r}]"

    def __add__(self, o):
        o = I.of(o)
        return I.out(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        r = I.__new__(I)
        r.lo, r.hi = -self.hi, -self.lo
        return r

    def __sub__(self, o):
        o = I.of(o)
        return I.out(self.lo - o.hi, self.hi - o.lo)

    def __mul__(self, o):
        o = I.of(o)
        if self.lo == self.hi and o.lo == o.hi:
            p = self.lo * o.lo
            return I.out(p, p)
        c = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return I.out(min(c), max(c))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = I.of(o)
        assert o.lo > 0 or o.hi < 0, "division by interval containing 0"
        c = (self.lo / o.lo, self.lo / o.hi, self.hi / o.lo, self.hi / o.hi)
        return I.out(min(c), max(c))

    def sqr(self):
        a, b = self.lo, self.hi
        if a >= 0:
            return I.out(a * a, b * b)
        if b <= 0:
            return I.out(b * b, a * a)
        return I.out(F(0), max(a * a, b * b))

    def powi(self, p):
        assert p >= 0
        if p == 0:
            return I(1)
        if p % 2 == 0:
            return self.sqr().powi(p // 2) if p > 2 else self.sqr()
        # odd power: monotone
        return I.out(self.lo ** p, self.hi ** p)

    def sqrt(self):
        assert self.lo >= 0, "sqrt of negative"
        return I.out(_sqrt_bound(self.lo, False), _sqrt_bound(self.hi, True))

    def exp(self):
        # exp(t) < 2^-7000 for t <= -5000: enclose by [0, 2^-7000] without
        # forming astronomically small Fractions.
        if self.hi <= -5000:
            return I(F(0), F(1, 1 << 7000))
        if self.lo <= -5000:
            hi = _mf(mpmath.exp(mpmath.mpf(self.hi.numerator) / self.hi.denominator)) * (1 + PAD)
            return I.out(F(0), hi)
        lo = mpmath.exp(mpmath.mpf(self.lo.numerator) / self.lo.denominator)
        hi = mpmath.exp(mpmath.mpf(self.hi.numerator) / self.hi.denominator)
        lo = _mf(lo) * (1 - PAD)
        hi = _mf(hi) * (1 + PAD)
        return I.out(lo, hi)

    def ln(self):
        assert self.lo > 0
        lo = _mf(mpmath.log(mpmath.mpf(self.lo.numerator) / self.lo.denominator))
        hi = _mf(mpmath.log(mpmath.mpf(self.hi.numerator) / self.hi.denominator))
        lo -= abs(lo) * PAD + F(1, 10 ** 80)
        hi += abs(hi) * PAD + F(1, 10 ** 80)
        return I.out(lo, hi)

    def contains0(self):
        return self.lo <= 0 <= self.hi

    def mag(self):
        return max(abs(self.lo), abs(self.hi))

    def mid(self):
        return (self.lo + self.hi) / 2

    def rad(self):
        return (self.hi - self.lo) / 2


def _mf(v):
    """Exact Fraction value of an mpmath mpf."""
    man, ex = v.man_exp
    return F(man) * (F(2) ** ex)


def _sqrt_bound(x, up):
    """Rational lower/upper bound of sqrt(x) with about PREC bits."""
    if x == 0:
        return F(0)
    s = 2 * PREC
    n, d = x.numerator, x.denominator
    # sqrt(n/d) = sqrt(n*d)/d ; scale by 2^s
    v = (n * d) << (2 * s)
    r = isqrt(v)
    if up and r * r != v:
        r += 1
    return F(r, d << s)
