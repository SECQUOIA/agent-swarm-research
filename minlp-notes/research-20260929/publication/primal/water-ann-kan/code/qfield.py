"""Exact arithmetic with rationals and quadratic irrationals, one symbol per value.

A value is Val(k, c): the polynomial c[0] + c[1] w_k + c[2] w_k^2 + ... in the
symbol w_k (k = None: a rational constant c[0]).  A symbol is either unsolved
(a free unknown during construction) or solved: then w_k is the unique root of
A w^2 + B w + C (rational A > 0, B, C) inside the rational isolating interval
(lo, hi), and every value in w_k is kept reduced to degree <= 1.

Operations that would combine two different symbols raise Mixed; the
construction code catches this and defers the row.  This keeps every value in
a single field Q(w_k), where equality to zero and signs are decided exactly.
"""
from fractions import Fraction as Fr

import mpmath as mp


class Mixed(Exception):
    pass


class Symbols:
    def __init__(self):
        self.S = []  # dicts: name, solved, A, B, C, lo, hi

    def new(self, name):
        self.S.append(dict(name=name, solved=False, rational=None))
        return len(self.S) - 1

    def solved(self, k):
        return self.S[k]["solved"]


SYM = Symbols()


def _strip(c):
    c = list(c)
    while len(c) > 1 and c[-1] == 0:
        c.pop()
    return tuple(c)


class Val:
    __slots__ = ("k", "c")

    def __init__(self, k, c):
        c = _strip(c)
        if k is not None and SYM.S[k]["solved"] and (len(c) > 2 or (len(c) > 1 and SYM.S[k]["rational"] is not None)):
            c = _reduce(k, c)
        if len(c) == 1:
            k = None
        self.k = k
        self.c = c

    @staticmethod
    def const(q):
        return Val(None, (Fr(q),))

    def norm(self):
        """Re-reduce after the symbol was solved."""
        if self.k is not None and SYM.S[self.k]["solved"]:
            return Val(self.k, self.c)
        return self

    def is_const(self):
        return self.k is None

    def _kk(self, o):
        if self.k is None:
            return o.k
        if o.k is None or o.k == self.k:
            return self.k
        raise Mixed()

    def __add__(self, o):
        if not isinstance(o, Val):
            o = Val.const(o)
        k = self._kk(o)
        n = max(len(self.c), len(o.c))
        a = self.c + (Fr(0),) * (n - len(self.c))
        b = o.c + (Fr(0),) * (n - len(o.c))
        return Val(k, tuple(x + y for x, y in zip(a, b)))

    __radd__ = __add__

    def __neg__(self):
        return Val(self.k, tuple(-x for x in self.c))

    def __sub__(self, o):
        if not isinstance(o, Val):
            o = Val.const(o)
        return self + (-o)

    def __rsub__(self, o):
        return Val.const(o) - self

    def __mul__(self, o):
        if not isinstance(o, Val):
            o = Fr(o)
            return Val(self.k, tuple(x * o for x in self.c))
        k = self._kk(o)
        r = [Fr(0)] * (len(self.c) + len(o.c) - 1)
        for i, x in enumerate(self.c):
            if x == 0:
                continue
            for j, y in enumerate(o.c):
                r[i + j] += x * y
        return Val(k, tuple(r))

    __rmul__ = __mul__

    def inv(self):
        """Inverse; only for constants or values in a solved field."""
        self = self.norm()
        if self.k is None:
            return Val.const(1 / self.c[0])
        s = SYM.S[self.k]
        if not s["solved"]:
            raise Mixed()
        p, r = self.c[0], self.c[1]
        A, B, C = s["A"], s["B"], s["C"]
        # (p + r w)(u + v w) = 1 with w^2 = -(B w + C)/A
        # p u - r v C/A = 1 ; p v + r u - r v B/A = 0
        det = p * (p - r * B / A) + r * r * C / A
        u = (p - r * B / A) / det
        v = -r / det
        return Val(self.k, (u, v))

    def __truediv__(self, o):
        if not isinstance(o, Val):
            return self * (1 / Fr(o))
        return self * o.inv()

    def __repr__(self):
        if self.k is None:
            return f"{self.c[0]}"
        return f"Val(w{self.k}:{SYM.S[self.k]['name']}, {[str(x) for x in self.c]})"


def _reduce(k, c):
    s = SYM.S[k]
    if s["rational"] is not None:
        return (_peval(c, s["rational"]),)
    A, B, C = s["A"], s["B"], s["C"]
    c = list(c)
    for d in range(len(c) - 1, 1, -1):
        t = c[d]
        if t != 0:
            # t w^d = t w^(d-2) w^2 = t w^(d-2) (-(B w + C)/A)
            c[d - 1] += -t * B / A
            c[d - 2] += -t * C / A
        c[d] = Fr(0)
    return _strip(c[:2])


def _isqrt_frac(q):
    """Return sqrt(q) as a Fraction if q is a rational square, else None."""
    import math
    if q < 0:
        return None
    n, d = q.numerator, q.denominator
    a, b = math.isqrt(n), math.isqrt(d)
    if a * a == n and b * b == d:
        return Fr(a, b)
    return None


def _peval(P, x):
    s = Fr(0)
    for c in reversed(P):
        s = s * x + c
    return s


def solve_symbol(k, P, near, width=Fr(1, 10 ** 45)):
    """Solve the symbol w_k from P(w) = 0, P = (c0, c1, c2) rational (degree 1 or 2).
    Choose the root nearest to `near` (a float or mpf).  Returns the rational value if the
    root is rational, else None (the symbol is then marked solved with an isolating
    interval)."""
    s = SYM.S[k]
    assert not s["solved"]
    P = _strip(P)
    assert 2 <= len(P) <= 3, P
    if len(P) == 2:
        root = -P[0] / P[1]
        s.update(solved=True, rational=root)
        return root
    C, B, A = P
    if A < 0:
        A, B, C = -A, -B, -C
    disc = B * B - 4 * A * C
    assert disc >= 0, "no real root"
    sq = _isqrt_frac(disc)
    if sq is not None:
        r1, r2 = (-B + sq) / (2 * A), (-B - sq) / (2 * A)
        root = r1 if abs(float(r1) - float(near)) <= abs(float(r2) - float(near)) else r2
        s.update(solved=True, rational=root)
        return root
    with mp.workdps(80):
        sd = mp.sqrt(mp.mpf(disc.numerator) / disc.denominator)
        mA, mB = mp.mpf(A.numerator) / A.denominator, mp.mpf(B.numerator) / B.denominator
        r1, r2 = (-mB + sd) / (2 * mA), (-mB - sd) / (2 * mA)
        root = r1 if abs(r1 - near) <= abs(r2 - near) else r2
        # rational isolating interval of the chosen root
        m = Fr(mp.nstr(root, 70, min_fixed=-10 ** 9, max_fixed=10 ** 9))
    lo, hi = m - width, m + width
    pl, ph = _peval((C, B, A), lo), _peval((C, B, A), hi)
    assert pl * ph < 0, "isolating interval failed"
    s.update(solved=True, A=A, B=B, C=C, lo=lo, hi=hi, rational=None)
    return None


def sign(v):
    """Exact sign of a Val whose symbol (if any) is solved."""
    v = v.norm()
    if v.k is None:
        return (v.c[0] > 0) - (v.c[0] < 0)
    s = SYM.S[v.k]
    assert s["solved"] and s.get("rational") is None
    assert len(v.c) == 2
    p, r = v.c
    if r == 0:
        return (p > 0) - (p < 0)
    z = -p / r  # p + r w = r (w - z)
    P = (s["C"], s["B"], s["A"])
    lo, hi = s["lo"], s["hi"]
    if z <= lo:
        wz = 1
    elif z >= hi:
        wz = -1
    else:
        pz = _peval(P, z)
        assert pz != 0, "rational root of an irreducible quadratic"
        pl = _peval(P, lo)
        # the root lies between the points where P changes sign
        wz = 1 if (pz > 0) == (pl > 0) else -1  # same sign as at lo -> root in (z, hi) -> w > z
    return wz if r > 0 else -wz


def enclose(v):
    """Rational interval [a, b] containing the value."""
    v = v.norm()
    if v.k is None:
        return v.c[0], v.c[0]
    s = SYM.S[v.k]
    p, r = v.c
    a, b = p + r * s["lo"], p + r * s["hi"]
    return (a, b) if a <= b else (b, a)


def to_mpf(v):
    """High-precision float value (evidence only)."""
    v = v.norm()
    if v.k is None:
        return mp.mpf(v.c[0].numerator) / v.c[0].denominator
    s = SYM.S[v.k]
    A, B, C = (mp.mpf(t.numerator) / t.denominator for t in (s["A"], s["B"], s["C"]))
    disc = B * B - 4 * A * C
    r1, r2 = (-B + mp.sqrt(disc)) / (2 * A), (-B - mp.sqrt(disc)) / (2 * A)
    mid = (mp.mpf(s["lo"].numerator) / s["lo"].denominator)
    w = r1 if abs(r1 - mid) < abs(r2 - mid) else r2
    p, r = v.c
    return mp.mpf(p.numerator) / p.denominator + mp.mpf(r.numerator) / r.denominator * w
