"""First-order Taylor models (affine arithmetic with a remainder), rigorous in IEEE double.

A TM (c, a, r) of array shape S stands for the statement: for every eps in [-1, 1]^m the true
value lies in [c + a.eps - r, c + a.eps + r], where c + a.eps is evaluated exactly (in real
arithmetic) from the stored doubles. Every rounding error of the float computations is added to r.

Assumptions: IEEE double round-to-nearest for + - * (numpy elementwise), Python float(str) and
mpmath's float conversion round to nearest, and mpmath.iv is a correct interval library.

Products use the standard affine-arithmetic rule with the eps_k^2 refinement:
  (x.eps)(y.eps) = 1/2 sum_k x_k y_k + N,  |N| <= Sx Sy - 1/2 sum_k |x_k y_k|,  Sx = sum_k |x_k|.
Nonlinear scalar functions f (convex on the argument range) are replaced by a line
alpha t + beta with a rigorous error bound delta (see linearize).
"""
import numpy as np
import mpmath as mp

iv = mp.iv
iv.dps = 40
U = 2.0 ** -52          # >= 2 * unit roundoff: relative error bound of one RN operation
TINY = 1e-290           # absolute slack covering underflow
M = [16]                # number of noise symbols (set by the caller before building TMs)


def upb(x):
    """upper bound for a nonnegative quantity computed by a sum of <= 2^10 nonnegative terms"""
    return np.asarray(x) * (1 + 2.0 ** -40) + TINY


def lowb(x):
    return np.maximum(np.asarray(x) * (1 - 2.0 ** -40) - TINY, 0.0)


def f2iv(x):
    return iv.mpf(float(x))


class TM:
    __slots__ = ("c", "a", "r")

    def __init__(self, c, a, r):
        self.c = np.asarray(c, dtype=np.float64)
        self.a = np.asarray(a, dtype=np.float64)
        self.r = np.asarray(r, dtype=np.float64)

    @property
    def S(self):
        return upb(np.abs(self.a).sum(-1))

    @staticmethod
    def const(c, r=0.0, shape=()):
        c = np.broadcast_to(np.asarray(c, dtype=np.float64), shape).copy()
        return TM(c, np.zeros(shape + (M[0],)), np.broadcast_to(np.asarray(r, dtype=np.float64), shape).copy())

    @staticmethod
    def dec(s, shape=()):
        """exact decimal constant: correctly rounded double, radius one relative ulp"""
        x = float(s)
        return TM.const(x, abs(x) * U + TINY, shape)

    @staticmethod
    def from_iv(v):
        lo, hi = np.nextafter(float(v.a), -np.inf), np.nextafter(float(v.b), np.inf)
        c = 0.5 * (lo + hi)
        r = max(np.nextafter(hi - c, np.inf), np.nextafter(c - lo, np.inf))
        return TM.const(c, upb(r + abs(c) * U))

    def range(self):
        """outward float enclosure [lo, hi] of all values"""
        w = upb(self.S + self.r + np.abs(self.c) * U)
        return np.nextafter(self.c - w, -np.inf), np.nextafter(self.c + w, np.inf)

    def __add__(self, o):
        if not isinstance(o, TM):
            o = TM.const(o)
        c = self.c + o.c
        a = self.a + o.a
        r = upb(self.r + o.r + U * (np.abs(c) + np.abs(a).sum(-1)))
        return TM(c, a, r)

    __radd__ = __add__

    def __neg__(self):
        return TM(-self.c, -self.a, self.r)

    def __sub__(self, o):
        return self + (-o)

    def __rsub__(self, o):
        return (-self) + o

    def __mul__(self, o):
        if not isinstance(o, TM):
            o = TM.const(o)
        m = M[0]
        xc, yc, xa, ya = self.c, o.c, self.a, o.a
        c0 = xc * yc
        xy = xa * ya
        c = c0 + 0.5 * xy.sum(-1)
        a = xc[..., None] * ya + yc[..., None] * xa
        Sx, Sy = self.S, o.S
        axy = np.abs(xy).sum(-1)
        nl = np.maximum(upb(Sx * Sy) - lowb(0.5 * axy), 0.0)
        rnd = U * (2 * np.abs(c0) + (m + 2) * axy + 2 * np.abs(c)
                   + 2 * (np.abs(xc) * Sy + np.abs(yc) * Sx + np.abs(a).sum(-1)))
        r = upb(nl + o.r * upb(np.abs(xc) + Sx) + self.r * upb(np.abs(yc) + Sy) + self.r * o.r + rnd)
        return TM(c, a, r)

    __rmul__ = __mul__

    def col(self):
        return TM(self.c[:, None], self.a[:, None, :], self.r[:, None])

    def row(self):
        return TM(self.c[None, :], self.a[None, :, :], self.r[None, :])


def linearize(x, f, fprime, fprime_inv):
    """Enclosure of f(x) for a scalar TM x, f convex on the range of x.
    f, fprime: mpmath-iv functions; fprime_inv(alpha): float point where f' = alpha (any float
    in the range is valid; it only affects tightness).
    Line alpha t + beta +- delta: h = f - alpha t is convex, so max h is at an end point and
    min h >= h(t0) - |h'(t0)| max|t - t0| for any t0 in the range."""
    lo, hi = x.range()
    lo, hi = float(lo), float(hi)
    if hi - lo < 1e-300:
        return TM.from_iv(f(iv.mpf([lo, hi])))
    Flo, Fhi = f(f2iv(lo)), f(f2iv(hi))
    alpha = float(((Fhi.mid - Flo.mid) / (hi - lo)).mid)
    t0 = min(max(fprime_inv(alpha), lo), hi)
    A = f2iv(alpha)
    hmax = max(float((f(f2iv(lo)) - A * f2iv(lo)).b), float((f(f2iv(hi)) - A * f2iv(hi)).b))
    hmax = np.nextafter(hmax, np.inf)
    h0 = f(f2iv(t0)) - A * f2iv(t0)
    dh = fprime(f2iv(t0)) - A
    hmin = np.nextafter(float((h0 - abs(dh) * f2iv(max(t0 - lo, hi - t0))).a), -np.inf)
    hmin = min(hmin, hmax)
    beta = 0.5 * (hmax + hmin)
    delta = max(float((f2iv(hmax) - f2iv(beta)).b), float((f2iv(beta) - f2iv(hmin)).b))
    delta = np.nextafter(delta, np.inf) * (1 + 2.0 ** -40) + TINY
    return x * TM.const(alpha) + TM.const(beta, delta)
