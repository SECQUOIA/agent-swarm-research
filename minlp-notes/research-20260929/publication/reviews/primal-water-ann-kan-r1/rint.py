"""Reviewer's own rigorous interval arithmetic (no floating point, no mpmath).

Values are V objects: either an exact Fraction (q) or an interval [lo, hi] with Fraction
endpoints.  Exact rational operations stay exact; anything else is enclosed, and endpoints are
rounded OUTWARD to PREC significant bits after each operation (floor for lo, ceil for hi).
exp is enclosed from a Taylor polynomial evaluated exactly in rationals after argument
reduction, with the Lagrange remainder bound |R_N(r)| <= |r|^(N+1)/(N+1)! * e^|r| <= 2|r|^(N+1)/(N+1)!
for |r| <= 1/4, then repeated squaring with outward rounding.  tanh(x) = 1 - 2/(exp(2x)+1) is
increasing, so tanh([a,b]) = [tanh_lo(a), tanh_hi(b)].
Assumption: none beyond exact rational arithmetic (Python Fractions/ints).
"""
from fractions import Fraction as Fr

PREC = 320  # significant bits kept at endpoints (~96 decimal digits)


def _rd(q, up):
    """Round the rational q to PREC significant bits, down (up=False) or up (up=True)."""
    if q == 0:
        return Fr(0)
    n, d = q.numerator, q.denominator
    e = abs(n).bit_length() - d.bit_length()
    s = PREC - e  # scale 2^s
    if s <= 0:
        t = Fr(n, d * 2 ** (-s)) if s < 0 else Fr(n, d)
        m = -((-t.numerator) // t.denominator) if up else t.numerator // t.denominator
        return Fr(m * 2 ** (-s))
    num = n * 2 ** s
    m = -((-num) // d) if up else num // d
    return Fr(m, 2 ** s)


class V:
    __slots__ = ("q", "lo", "hi")

    def __init__(self, lo, hi=None, exact=False):
        if exact:
            self.q = Fr(lo)
            self.lo = self.hi = self.q
        else:
            self.q = None
            self.lo, self.hi = _rd(Fr(lo), False), _rd(Fr(hi), True)
            assert self.lo <= self.hi

    @staticmethod
    def num(q):
        return V(q, exact=True)

    def is_exact(self):
        return self.q is not None

    def __add__(self, o):
        if self.q is not None and o.q is not None:
            return V(self.q + o.q, exact=True)
        return V(self.lo + o.lo, self.hi + o.hi)

    def __neg__(self):
        if self.q is not None:
            return V(-self.q, exact=True)
        r = V.__new__(V)
        r.q, r.lo, r.hi = None, -self.hi, -self.lo
        return r

    def __sub__(self, o):
        return self + (-o)

    def __mul__(self, o):
        if self.q is not None and o.q is not None:
            return V(self.q * o.q, exact=True)
        if (self.q is not None and self.q == 0) or (o.q is not None and o.q == 0):
            return V(0, exact=True)  # 0 * (any real) = 0
        p = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return V(min(p), max(p))

    def inv(self):
        if self.q is not None:
            assert self.q != 0
            return V(1 / self.q, exact=True)
        assert self.lo > 0 or self.hi < 0, "division by an interval containing 0"
        return V(1 / self.hi, 1 / self.lo)

    @staticmethod
    def div(a, b):
        if a.q is not None and b.q is not None:
            return V(a.q / b.q, exact=True)
        return a * b.inv()

    def contains0(self):
        return self.lo <= 0 <= self.hi

    def mid_rad(self):
        return (self.lo + self.hi) / 2, (self.hi - self.lo) / 2

    @staticmethod
    def exp(x):
        if x.q is not None and x.q == 0:
            return V(1, exact=True)
        return V(exp_bounds(x.lo)[0], exp_bounds(x.hi)[1])

    @staticmethod
    def tanh(x):
        if x.q is not None and x.q == 0:
            return V(0, exact=True)
        a, _ = exp_bounds(2 * x.lo)
        _, b = exp_bounds(2 * x.hi)
        return V(1 - Fr(2) / (a + 1), 1 - Fr(2) / (b + 1))


_EXPC = {}
NTAY = 60


def exp_bounds(x):
    """Rational lo <= exp(x) <= hi for a rational x."""
    x = Fr(x)
    if x in _EXPC:
        return _EXPC[x]
    k = 0
    r = x
    while abs(r) > Fr(1, 4):
        r /= 2
        k += 1
    # Taylor sum, exact in rationals but with r rounded outward first would change r; keep r exact
    rr = _rd(r, False), _rd(r, True)
    # use exact r but keep the sum's size bounded by rounding terms outward
    s_lo = s_hi = Fr(0)
    term = Fr(1)
    for n in range(NTAY + 1):
        if n > 0:
            term = term * r / n
        s_lo = _rd(s_lo + term, False)
        s_hi = _rd(s_hi + term, True)
        # rounding after each add only widens [s_lo, s_hi] outward; term itself is exact
        if term.denominator.bit_length() > 4 * PREC:
            # keep the exact term short: replace it by an enclosure (then track both ends)
            break
    else:
        rem = 2 * abs(r) ** (NTAY + 1)
        f = 1
        for i in range(2, NTAY + 2):
            f *= i
        rem /= f
        lo, hi = _rd(s_lo - rem, False), _rd(s_hi + rem, True)
        assert lo > 0
        for _ in range(k):
            lo, hi = _rd(lo * lo, False), _rd(hi * hi, True)
        _EXPC[x] = (lo, hi)
        return lo, hi
    return _exp_bounds_iv(x)


def _exp_bounds_iv(x):
    """Same bound, with r enclosed by a short interval when exact terms get too long."""
    k = 0
    r = x
    while abs(r) > Fr(1, 4):
        r /= 2
        k += 1
    rl, rh = _rd(r, False), _rd(r, True)
    R = V(rl, rh)
    S = V(1, exact=True)
    T = V(1, exact=True)
    for n in range(1, NTAY + 1):
        T = T * R * V(Fr(1, n), exact=True)
        S = S + T
    m = max(abs(rl), abs(rh))
    f = 1
    for i in range(2, NTAY + 2):
        f *= i
    rem = 2 * m ** (NTAY + 1) / f
    lo, hi = _rd(S.lo - rem, False), _rd(S.hi + rem, True)
    assert lo > 0
    for _ in range(k):
        lo, hi = _rd(lo * lo, False), _rd(hi * hi, True)
    _EXPC[x] = (lo, hi)
    return lo, hi
