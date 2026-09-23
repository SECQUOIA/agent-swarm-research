"""Separation from the convex hull of a univariate curve

    C = {phi(t) = (t, f_1(t), ..., f_k(t)) : t in [l, u]}.

Given a point p, `Curve.separate(p)` returns a cut (c0, c) with c0 + c.phi(t) >= 0 for all t in [l, u]
that maximizes the violation -(c0 + c.p) in scaled coordinates (every coordinate mapped to [0, 1] over
the curve, coefficients bounded by 1 in absolute value), or None if p is (numerically) in the hull.

Method.  The direction c comes from the semi-infinite LP
    min c0 + c.s(p)  s.t.  c0 + c.s(phi(t)) >= 0 for t in T,  -1 <= c <= 1,
solved by cutting planes on T (dense grid plus local refinement adds the most violated t).
The constant c0 is then *not* taken from the LP: it is set to minus a certified lower bound of
c.phi(t) over [l, u].  The certificate uses outward-rounded interval arithmetic on the sympy
expressions of f_j and f_j'':  on a piece [a, b], with M = max(0, sup g''([a, b])),
    g(t) >= min(g(a), g(b)) - M (b - a)^2 / 8
(g minus its chord vanishes at a and b and has second derivative <= M),
and alternatively the natural interval extension of g on [a, b]; the larger of the two is used,
and pieces whose bound is loose are bisected.  Rounding: every interval operation is widened
outward by a relative 1e-14 (transcendental) or 4e-16 (arithmetic) plus 1e-300 absolute; this
assumes the float64 library functions are accurate to far better than 1e-14 relative.
"""
from __future__ import annotations

import math

import numpy as np
import sympy as sp
from scipy.optimize import linprog, minimize_scalar

T = sp.Symbol("t", real=True)
PI = math.pi


# ------------------------------------------------------------------ vectorized interval arithmetic
def _w(lo, hi, rel):
    lo = np.asarray(lo, float)
    hi = np.asarray(hi, float)
    return lo - np.abs(lo) * rel - 1e-300, hi + np.abs(hi) * rel + 1e-300


class IA:
    __slots__ = ("lo", "hi")
    AR, TR = 4e-16, 1e-14

    def __init__(self, lo, hi=None, rel=0.0):
        hi = lo if hi is None else hi
        if rel:
            lo, hi = _w(lo, hi, rel)
        self.lo = np.asarray(lo, float)
        self.hi = np.asarray(hi, float)

    def __add__(s, o):
        o = _ia(o)
        return IA(s.lo + o.lo, s.hi + o.hi, IA.AR)

    def __neg__(s):
        return IA(-s.hi, -s.lo)

    def __mul__(s, o):
        o = _ia(o)
        with np.errstate(invalid="ignore"):
            p = np.stack([s.lo * o.lo, s.lo * o.hi, s.hi * o.lo, s.hi * o.hi])
        p = np.where(np.isnan(p), 0.0, p)  # 0 * inf; only reached for unbounded enclosures
        return IA(p.min(0), p.max(0), IA.AR)

    def recip(s):
        bad = (s.lo <= 0) & (s.hi >= 0)
        with np.errstate(divide="ignore"):
            lo, hi = 1.0 / s.hi, 1.0 / s.lo
        return IA(np.where(bad, -np.inf, lo), np.where(bad, np.inf, hi), IA.AR)

    def ipow(s, n: int):
        if n == 0:
            return IA(np.ones_like(s.lo))
        if n < 0:
            return s.ipow(-n).recip()
        a, b = s.lo ** n, s.hi ** n
        if n % 2:
            return IA(a, b, IA.AR * n)
        lo = np.where((s.lo <= 0) & (s.hi >= 0), 0.0, np.minimum(a, b))
        return IA(lo, np.maximum(a, b), IA.AR * n)

    def rpow(s, p: float):  # real exponent, base must be >= 0 (> 0 if p < 0)
        with np.errstate(divide="ignore", invalid="ignore"):
            a, b = np.power(s.lo, p), np.power(s.hi, p)
        bad = (s.lo < 0) | ((s.lo <= 0) & (p < 0))
        lo, hi = np.minimum(a, b), np.maximum(a, b)
        return IA(np.where(bad, -np.inf, lo), np.where(bad, np.inf, hi), IA.TR)

    def exp(s):
        with np.errstate(over="ignore"):
            return IA(np.exp(s.lo), np.exp(s.hi), IA.TR)

    def log(s):
        with np.errstate(divide="ignore", invalid="ignore"):
            lo, hi = np.log(np.maximum(s.lo, 0)), np.log(s.hi)
        bad = s.lo < 0
        return IA(np.where(bad, -np.inf, lo), np.where(bad | np.isnan(hi), np.inf, hi), IA.TR)

    def sin(s):
        return (s + (-PI / 2)).cos()

    def cos(s):
        a, b = np.cos(s.lo), np.cos(s.hi)
        lo, hi = np.minimum(a, b), np.maximum(a, b)
        eps = 1e-12 * (1 + np.abs(s.lo))
        # max of cos at 2 pi k, min at pi + 2 pi k; test with a small outward margin
        kmax = np.ceil((s.lo - eps) / (2 * PI))
        has_max = 2 * PI * kmax <= s.hi + eps
        kmin = np.ceil((s.lo - PI - eps) / (2 * PI))
        has_min = PI + 2 * PI * kmin <= s.hi + eps
        hi = np.where(has_max, 1.0, hi)
        lo = np.where(has_min, -1.0, lo)
        lo, hi = _w(lo, hi, IA.TR)
        return IA(np.maximum(lo, -1.0), np.minimum(hi, 1.0))

    def abs(s):
        lo = np.where((s.lo <= 0) & (s.hi >= 0), 0.0, np.minimum(np.abs(s.lo), np.abs(s.hi)))
        return IA(lo, np.maximum(np.abs(s.lo), np.abs(s.hi)))


def _ia(o):
    return o if isinstance(o, IA) else IA(float(o))


def _const(e):
    """Enclosure of a sympy constant."""
    v = float(sp.N(e, 30))
    return IA(v, v, 1e-15)


def ieval(e, X: IA) -> IA:
    """Interval enclosure of the sympy expression e(t) over the interval vector X."""
    if e == T:
        return X
    if e.is_Number or (e.is_number and not e.free_symbols):
        return _const(e)
    if e.is_Add:
        out = ieval(e.args[0], X)
        for a in e.args[1:]:
            out = out + ieval(a, X)
        return out
    if e.is_Mul:
        out = ieval(e.args[0], X)
        for a in e.args[1:]:
            out = out * ieval(a, X)
        return out
    if e.is_Pow:
        b, p = e.args
        if not p.free_symbols:
            B = ieval(b, X)
            if p.is_Integer:
                return B.ipow(int(p))
            return B.rpow(float(p))
        # b^p with symbolic exponent: exp(p log b)
        return (ieval(p, X) * ieval(b, X).log()).exp()
    f = e.func
    if f == sp.exp:
        return ieval(e.args[0], X).exp()
    if f == sp.log:
        return ieval(e.args[0], X).log()
    if f == sp.sin:
        return ieval(e.args[0], X).sin()
    if f == sp.cos:
        return ieval(e.args[0], X).cos()
    if f == sp.Abs:
        return ieval(e.args[0], X).abs()
    raise NotImplementedError(f"interval evaluation of {f}")


def _finite(I: IA):
    return np.isfinite(I.lo) & np.isfinite(I.hi)


# ------------------------------------------------------------------ the curve
class Curve:
    """phi(t) = (t, f_1(t), ..., f_k(t)) on [l, u]; `funcs` are sympy expressions in T."""

    def __init__(self, funcs, l, u, npieces=4096, ngrid=4096):
        assert math.isfinite(l) and math.isfinite(u) and u > l
        self.funcs, self.l, self.u = list(funcs), float(l), float(u)
        self.k = len(self.funcs)
        self.num = [sp.lambdify(T, f, "numpy") for f in self.funcs]
        self.d2 = []
        for f in self.funcs:
            try:
                self.d2.append(sp.diff(f, T, 2))
            except Exception:
                self.d2.append(None)
        # grid for the inner minimization (floats)
        self.tg = np.linspace(self.l, self.u, ngrid + 1)
        self.Pg = self.phi(self.tg)  # (k+1, ngrid+1)
        # certified pieces
        self.edges = np.linspace(self.l, self.u, npieces + 1)
        self.edges[0], self.edges[-1] = self.l, self.u
        self.node_enc = self._enc_points(self.edges)
        self.piece = self._enc_pieces(self.edges[:-1], self.edges[1:])
        # rigorous range of each coordinate (for scaling and aux-variable bounds)
        Flo, Fhi, _, _ = self.piece
        self.rlo, self.rhi = Flo.min(1), Fhi.max(1)
        if not (np.all(np.isfinite(self.rlo)) and np.all(np.isfinite(self.rhi))):
            raise ValueError("a function is not finite on the interval")
        # scaling of the LP: every coordinate mapped to about [0, 1] on the curve
        self.off = self.Pg.min(1)
        self.wid = np.maximum(self.Pg.max(1) - self.off, 1e-300)

    def phi(self, t):
        t = np.atleast_1d(np.asarray(t, float))
        rows = [t] + [np.broadcast_to(np.asarray(f(t), float), t.shape) for f in self.num]
        return np.vstack(rows)

    # enclosures ---------------------------------------------------------
    def _enc_points(self, ts):
        X = IA(ts)
        lo, hi = [X.lo], [X.hi]
        for f in self.funcs:
            I = ieval(f, X)
            lo.append(np.broadcast_to(I.lo, ts.shape))
            hi.append(np.broadcast_to(I.hi, ts.shape))
        return np.vstack(lo), np.vstack(hi)

    def _enc_pieces(self, a, b):
        """Per piece: enclosure of phi (Flo, Fhi) and of phi'' (Dlo, Dhi); rows = coordinates."""
        X = IA(a, b)
        n = a.shape
        Flo, Fhi, Dlo, Dhi = [X.lo], [X.hi], [np.zeros(n)], [np.zeros(n)]
        for f, d2 in zip(self.funcs, self.d2):
            I = ieval(f, X)
            Flo.append(np.broadcast_to(I.lo, n)); Fhi.append(np.broadcast_to(I.hi, n))
            try:
                D = ieval(d2, X) if d2 is not None else IA(np.full(n, -np.inf), np.full(n, np.inf))
            except NotImplementedError:
                D = IA(np.full(n, -np.inf), np.full(n, np.inf))
            Dlo.append(np.broadcast_to(D.lo, n)); Dhi.append(np.broadcast_to(D.hi, n))
        return tuple(np.vstack(v) for v in (Flo, Fhi, Dlo, Dhi))

    @staticmethod
    def _lin_lower(c, lo, hi):
        """Rigorous lower bound of sum_j c_j y_j over y_j in [lo_j, hi_j] (columns = cases)."""
        c = c[:, None]
        with np.errstate(invalid="ignore"):
            terms = np.where(c >= 0, c * lo, c * hi)
        terms = np.where(c == 0, 0.0, terms)
        s = terms.sum(0)
        err = (np.abs(terms).sum(0)) * (len(c) + 2) * 2.3e-16 + 1e-300
        return s - err

    def _piece_lower(self, c, a, b, enc_a, enc_b, piece):
        Flo, Fhi, Dlo, Dhi = piece
        direct = self._lin_lower(c, Flo, Fhi)
        ga = self._lin_lower(c, *enc_a)
        gb = self._lin_lower(c, *enc_b)
        d2hi = -self._lin_lower(-c, Dlo, Dhi)  # upper bound of g''
        h = b - a
        with np.errstate(invalid="ignore"):
            m = np.maximum(0.0, d2hi) * (h * h / 8.0) * (1 + 1e-15)
            taylor = np.minimum(ga, gb) - m
        taylor = np.where(np.isnan(taylor), -np.inf, taylor)
        out = np.maximum(direct, taylor)
        return np.where(np.isnan(out), -np.inf, out)

    def certified_min(self, c, target=None, tol=None, maxdepth=30):
        """Rigorous lower bound of c.phi(t) over [l, u].  Pieces whose bound is below
        target - tol are bisected (target defaults to the float minimum on the grid)."""
        c = np.asarray(c, float)
        if target is None:
            target = float((c @ self.Pg).min())
        if tol is None:
            tol = 1e-8 * (1.0 + np.abs(c) @ np.maximum(np.abs(self.rlo), np.abs(self.rhi)))
        a, b = self.edges[:-1], self.edges[1:]
        lo_n, hi_n = self.node_enc
        enc_a, enc_b = (lo_n[:, :-1], hi_n[:, :-1]), (lo_n[:, 1:], hi_n[:, 1:])
        piece = self.piece
        best = np.inf
        for depth in range(maxdepth + 1):
            lb = self._piece_lower(c, a, b, enc_a, enc_b, piece)
            ok = lb >= target - tol
            if np.any(ok):
                best = min(best, float(lb[ok].min()))
            if np.all(ok):
                return best
            a, b = a[~ok], b[~ok]
            if depth == maxdepth or a.size > 200000:
                return min(best, float(lb[~ok].min()))
            mid = 0.5 * (a + b)
            enc_m = self._enc_points(mid)
            ea = (np.hstack([enc_a[0][:, ~ok], enc_m[0]]), np.hstack([enc_a[1][:, ~ok], enc_m[1]]))
            eb = (np.hstack([enc_m[0], enc_b[0][:, ~ok]]), np.hstack([enc_m[1], enc_b[1][:, ~ok]]))
            a, b = np.concatenate([a, mid]), np.concatenate([mid, b])
            enc_a, enc_b = ea, eb
            piece = self._enc_pieces(a, b)
        return best

    # separation ----------------------------------------------------------
    def float_min(self, c, nloc=3):
        """Approximate global minimizer of c.phi(t): grid + bounded local refinement of the best
        grid local minima.  Returns (t*, value, list of local-minimum abscissae)."""
        g = c @ self.Pg
        inner = (g[1:-1] <= g[:-2]) & (g[1:-1] <= g[2:])
        loc = np.concatenate([[0] if g[0] <= g[1] else [], np.nonzero(inner)[0] + 1,
                              [len(g) - 1] if g[-1] <= g[-2] else []]).astype(int)
        loc = loc[np.argsort(g[loc])][:nloc]
        best_t, best_v = self.tg[loc[0]], g[loc[0]]
        found = []
        for i in loc:
            lo = self.tg[max(i - 1, 0)]
            hi = self.tg[min(i + 1, len(self.tg) - 1)]
            r = minimize_scalar(lambda s: float(c @ self.phi(s)[:, 0]), bounds=(lo, hi), method="bounded",
                                options={"xatol": 1e-10 * (1 + abs(hi))})
            t_i, v_i = (r.x, r.fun) if r.fun < g[i] else (self.tg[i], g[i])
            found.append(float(t_i))
            if v_i < best_v:
                best_t, best_v = t_i, v_i
        return float(best_t), float(best_v), found

    def separate(self, p, min_viol=1e-6, max_iter=60):
        """Most violated cut in scaled coordinates.  Returns dict(c0, c, viol_scaled) in original
        coordinates (c0 certified) or None."""
        p = np.asarray(p, float)
        sp_ = (p - self.off) / self.wid
        n = self.k + 1
        Ts = list(np.linspace(self.l, self.u, 129))
        S = lambda ts: ((self.phi(ts) - self.off[:, None]) / self.wid[:, None])
        for _ in range(max_iter):
            Ps = S(np.array(Ts))
            # variables: c0, c_1..c_n ; minimize c0 + c.sp  s.t. -(c0 + c.Ps_i) <= 0
            A = -np.hstack([np.ones((Ps.shape[1], 1)), Ps.T])
            res = linprog(np.concatenate([[1.0], sp_]), A_ub=A, b_ub=np.zeros(Ps.shape[1]),
                          bounds=[(None, None)] + [(-1, 1)] * n, method="highs")
            if res.status != 0:
                return None
            c0s, cs = res.x[0], res.x[1:]
            if res.fun > -min_viol:
                return None
            # most violated t for the scaled direction
            tstar, v, locs = self.float_min(cs / self.wid)
            v_scaled = v - (cs / self.wid) @ self.off
            # stop once the LP direction is nearly feasible; the constant is certified afterwards
            if v_scaled + c0s >= -max(1e-9, 1e-3 * (-res.fun)):
                break
            Ts += locs
        # back to original coordinates; drop negligible coefficients; certify the constant
        corig = cs / self.wid
        scale_terms = np.abs(corig) * np.maximum(np.abs(self.rlo), np.abs(self.rhi))
        corig = np.where(scale_terms < 1e-11 * scale_terms.max(), 0.0, corig)
        lb = self.certified_min(corig)
        if not math.isfinite(lb):
            return None
        c0 = -lb
        viol = -(c0 + corig @ p)
        viol_scaled = viol / max(np.abs(cs).max(), 1e-300)
        if viol_scaled < min_viol:
            return None
        return {"c0": float(c0), "c": corig, "viol_scaled": float(viol_scaled), "lp_viol": float(-res.fun)}


# ------------------------------------------------------------------ exact hull of the moment curve (degree 3)
def moment3_in_hull(p, l, u, tol=1e-9):
    """(x, y, z) in conv{(t, t^2, t^3) : t in [l, u]} iff the two rotated cones hold
    (x - l)(z - l y) >= (y - l x)^2,  (u - x)(u y - z) >= (u x - y)^2, with nonnegative factors.
    Returns the minimum slack (>= -tol means inside)."""
    x, y, z = p
    s = [x - l, z - l * y, u - x, u * y - z,
         (x - l) * (z - l * y) - (y - l * x) ** 2, (u - x) * (u * y - z) - (u * x - y) ** 2]
    return min(s)
