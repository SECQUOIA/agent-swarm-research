"""Vectorized outward-rounded interval arithmetic (numpy) and interval forward-mode AD.

NI: interval with numpy float64 arrays (lo, hi). + - * / are computed in
round-to-nearest IEEE arithmetic (error <= 0.5 ulp) and widened outward by one
ulp with nextafter, so the result encloses the exact result. Decimal constants
are enclosed by widening the correctly rounded double by one ulp each side.

log/exp: numpy's float64 log/exp are not guaranteed correctly rounded; the
results are widened by LOGW ulps of the result plus an absolute 1e-300. This
assumes libm error <= LOGW ulps (glibc and numpy's SIMD code claim <= 4 ulp).
Scripts that need full rigor re-verify their leaf boxes with mpmath.iv
(arbitrary-precision, rigorous), using the same AD class with mpmath intervals.

AD: value plus gradient (tuple) over any interval type supporting + - * /.
"""
import numpy as np

INF = np.inf
LOGW = 16


def dn(x):
    return np.nextafter(x, -INF)


def up(x):
    return np.nextafter(x, INF)


class NI:
    __slots__ = ("lo", "hi")
    __array_priority__ = 100

    def __init__(self, lo, hi=None):
        self.lo = np.asarray(lo, dtype=np.float64)
        self.hi = self.lo if hi is None else np.asarray(hi, dtype=np.float64)

    @staticmethod
    def const(s):
        x = np.float64(float(s))
        if float(x) == 0.0 and float(s) == 0.0:
            return NI(0.0, 0.0)
        return NI(dn(x), up(x))

    @staticmethod
    def wrap(o):
        if isinstance(o, NI):
            return o
        if isinstance(o, str):
            return NI.const(o)
        x = np.float64(o)
        return NI(x, x)  # exact float value

    def __add__(self, o):
        o = NI.wrap(o)
        return NI(dn(self.lo + o.lo), up(self.hi + o.hi))

    __radd__ = __add__

    def __neg__(self):
        return NI(-self.hi, -self.lo)

    def __sub__(self, o):
        o = NI.wrap(o)
        return NI(dn(self.lo - o.hi), up(self.hi - o.lo))

    def __rsub__(self, o):
        return NI.wrap(o) - self

    def __mul__(self, o):
        o = NI.wrap(o)
        p = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        lo = np.minimum(np.minimum(p[0], p[1]), np.minimum(p[2], p[3]))
        hi = np.maximum(np.maximum(p[0], p[1]), np.maximum(p[2], p[3]))
        return NI(dn(lo), up(hi))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = NI.wrap(o)
        assert np.all((o.lo > 0) | (o.hi < 0)), "division by interval containing 0"
        p = [self.lo / o.lo, self.lo / o.hi, self.hi / o.lo, self.hi / o.hi]
        lo = np.minimum(np.minimum(p[0], p[1]), np.minimum(p[2], p[3]))
        hi = np.maximum(np.maximum(p[0], p[1]), np.maximum(p[2], p[3]))
        return NI(dn(lo), up(hi))

    def __rtruediv__(self, o):
        return NI.wrap(o) / self

    def __getitem__(self, k):
        return NI(self.lo[k], self.hi[k])


def _widen(r_lo, r_hi):
    lo = r_lo - LOGW * np.spacing(np.abs(r_lo)) - 1e-300
    hi = r_hi + LOGW * np.spacing(np.abs(r_hi)) + 1e-300
    return lo, hi


def nlog(a):
    """log with libm results widened by LOGW ulps (see module docstring)."""
    assert np.all(a.lo > 0), "log of nonpositive interval"
    lo, hi = _widen(np.log(a.lo), np.log(a.hi))
    return NI(lo, hi)


_LN2 = NI(dn(np.float64(0.6931471805599453)), up(np.float64(0.6931471805599453)))
_K = 12
_INV = [NI(1.0) / NI(float(2 * j + 1)) for j in range(_K + 1)]


def _log_point(x):
    """Rigorous enclosure of log(x) for float arrays x > 0 using only IEEE + - * /
    with outward rounding: x = m 2^e (exact), m in [sqrt(.5), sqrt(2)), s = (m-1)/(m+1),
    log m = 2 atanh s = 2 sum_j s^(2j+1)/(2j+1), truncated after j = _K with the
    remainder bounded by |s|^(2K+3)/((2K+3)(1-s^2)) <= 1e-19 (|s| <= 0.1716)."""
    m, e = np.frexp(x)
    small = m < 0.7071067811865476
    m = np.where(small, m * 2.0, m)             # exact
    e = np.where(small, e - 1, e).astype(np.float64)
    num = NI(m - 1.0)                           # exact (Sterbenz)
    den = NI(m) + 1.0
    s = num / den
    s2 = s * s
    acc = _INV[_K]
    for j in range(_K - 1, -1, -1):
        acc = _INV[j] + s2 * acc
    at = s * acc
    sabs = np.maximum(np.abs(s.lo), np.abs(s.hi))
    assert np.all(sabs < 0.1716)
    rem = 1e-19
    at = NI(dn(at.lo - rem), up(at.hi + rem))
    return NI(e) * _LN2 + at * 2.0


def ilog(a):
    """Rigorous interval log (monotone: lower end from log(lo), upper end from log(hi))."""
    assert np.all(a.lo > 0), "log of nonpositive interval"
    return NI(_log_point(a.lo).lo, _log_point(a.hi).hi)


def nexp(a):
    lo, hi = _widen(np.exp(a.lo), np.exp(a.hi))
    return NI(np.maximum(lo, 0.0), hi)


class AD:
    """Forward-mode AD: value v and gradient g (tuple), entries of any interval type."""
    __slots__ = ("v", "g")

    def __init__(self, v, g):
        self.v, self.g = v, g

    def __add__(self, o):
        if isinstance(o, AD):
            return AD(self.v + o.v, tuple(a + b for a, b in zip(self.g, o.g)))
        return AD(self.v + o, self.g)

    __radd__ = __add__

    def __neg__(self):
        return AD(-self.v, tuple(-a for a in self.g))

    def __sub__(self, o):
        return self + (-o)

    def __rsub__(self, o):
        return (-self) + o

    def __mul__(self, o):
        if isinstance(o, AD):
            return AD(self.v * o.v, tuple(a * o.v + self.v * b for a, b in zip(self.g, o.g)))
        return AD(self.v * o, tuple(a * o for a in self.g))

    __rmul__ = __mul__

    def __truediv__(self, o):
        if isinstance(o, AD):
            q = self.v / o.v
            return AD(q, tuple((a - q * b) / o.v for a, b in zip(self.g, o.g)))
        return AD(self.v / o, tuple(a / o for a in self.g))


def ad_log(a, logf):
    return AD(logf(a.v), tuple(g / a.v for g in a.g))


def ad_exp(a, expf):
    e = expf(a.v)
    return AD(e, tuple(g * e for g in a.g))


def ev_ad(t, x, num, fns):
    """Evaluate an osilx expression tree with AD (or plain interval) variables x.

    Keeps AD operands on the left of mixed operations so that constant intervals
    (numpy NI or mpmath iv) never have to handle AD objects."""
    op = t[0]
    if op == "num":
        return num(t[1])
    if op == "var":
        v = x[t[1]]
        return v if t[2] == "1" else v * num(t[2])
    a = [ev_ad(c, x, num, fns) for c in t[1:]]
    if op in ("sum", "plus", "product", "times"):
        a.sort(key=lambda z: not isinstance(z, AD))
        s = a[0]
        for b in a[1:]:
            s = s + b if op in ("sum", "plus") else s * b
        return s
    if op == "minus":
        return a[0] - a[1] if isinstance(a[0], AD) or not isinstance(a[1], AD) else (-a[1]) + a[0]
    if op == "negate":
        return -a[0]
    if op == "divide":
        if isinstance(a[0], AD) or not isinstance(a[1], AD):
            return a[0] / a[1]
        return AD(a[0], tuple(0 * g for g in a[1].g)) / a[1]
    if op == "square":
        return a[0] * a[0]
    return fns[op](*a)


def isqrt(a):
    """sqrt of an interval with a.lo >= 0 (IEEE sqrt is correctly rounded)."""
    assert np.all(a.lo >= 0)
    return NI(np.maximum(dn(np.sqrt(a.lo)), 0.0), up(np.sqrt(a.hi)))
