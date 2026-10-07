"""Exact envelopes, ranges and cuts for one univariate function on an interval.

For any slope s, the line  s*x + min_{[l,u]} (g(x) - s*x)  underestimates g on
[l, u].  The inner minimum is taken piece by piece: endpoints on concave
pieces, the stationary point (or an endpoint) on convex pieces, and a rigorous
enclosure on the tiny ``unknown`` pieces.  Validity of a cut therefore does
not depend on the outer search for the slope that supports the envelope at x*.
"""
from __future__ import annotations

import bisect
import math

import numpy as np
import sympy as sp
from scipy.optimize import brentq

from .curvature import X, Piece, certify_pieces

_SAFETY = 1e-11


class Univariate:
    def __init__(self, expr: sp.Expr, lo: float, hi: float):
        self.expr, self.lo, self.hi = expr, float(lo), float(hi)
        self.g = sp.lambdify(X, expr, "math")
        self.dg = sp.lambdify(X, sp.diff(expr, X), "math")
        self._dg_raw = self.dg
        self.dg = self._dg_safe
        self.pieces = certify_pieces(expr, self.lo, self.hi)
        neg = [Piece(p.lo, p.hi, {"convex": "concave", "concave": "convex"}.get(p.label, p.label),
                     -p.ghi, -p.glo) for p in self.pieces]
        self._sides = {+1: self.pieces, -1: neg}
        self._starts = [p.lo for p in self.pieces]
        self._gcache: dict[float, float] = {}
        self._dcache: dict[float, float] = {}

    def _g(self, x: float) -> float:
        v = self._gcache.get(x)
        if v is None:
            if len(self._gcache) > 200000:
                self._gcache.clear()
            v = self._gcache[x] = self.g(x)
        return v

    def _d(self, x: float) -> float:
        v = self._dcache.get(x)
        if v is None:
            if len(self._dcache) > 200000:
                self._dcache.clear()
            v = self._dcache[x] = self.dg(x)
        return v

    def _dg_safe(self, x: float) -> float:
        """g'(x); at a singular endpoint, nudge inwards and keep the sign with a huge magnitude."""
        try:
            v = self._dg_raw(x)
            if math.isfinite(v):
                return v
        except (ZeroDivisionError, ValueError, OverflowError):
            pass
        eps = 1e-9 * max(1.0, self.hi - self.lo)
        probe = x + eps if x - self.lo < self.hi - x else x - eps
        return math.copysign(1e300, self._dg_raw(probe))

    # ---- inner problem: min over [l,u] of sign*g(x) - s*x, with a minimizer ----
    def _inner(self, sign: int, s: float, l: float, u: float, rigorous: bool = True) -> tuple[float, float]:
        """``rigorous=False`` skips the unknown slivers; use it only to steer the slope search."""
        g, dg = self._g, self._d
        best, arg = math.inf, l
        side = self._sides[sign]
        first = max(bisect.bisect_right(self._starts, l) - 1, 0)
        for p in side[first:]:
            if p.lo > u:
                break
            a, b = max(p.lo, l), min(p.hi, u)
            if a > b:
                continue
            if p.label == "unknown" and not rigorous:
                continue
            if p.label == "unknown":
                val = p.glo - max(s * a, s * b)
                cands = [(val, 0.5 * (a + b))]
            else:
                cands = [(sign * g(a) - s * a, a), (sign * g(b) - s * b, b)]
                if p.label == "convex" and b > a:
                    da, db = sign * dg(a) - s, sign * dg(b) - s
                    if da < 0.0 < db:
                        raw = self.dg
                        x0 = brentq(lambda x: sign * raw(x) - s, a, b, xtol=1e-14, rtol=1e-14)
                        # convexity: phi(x) >= phi(x0) + phi'(x0)(x - x0) on the piece
                        slack = abs(sign * raw(x0) - s) * (b - a)
                        cands.append((sign * self.g(x0) - s * x0 - slack, x0))
            for val, x in cands:
                if val < best:
                    best, arg = val, x
        return best, arg

    def _support(self, sign: int, l: float, u: float, xstar: float) -> tuple[float, float]:
        """Slope and intercept of a line below sign*g on [l,u], tight for the envelope at xstar."""
        if u - l <= 1e-12 * max(1.0, abs(l), abs(u)):
            h, _ = self._inner(sign, 0.0, l, u)
            return 0.0, h - _SAFETY * (1.0 + abs(h))
        xs = min(max(xstar, l + 1e-9 * (u - l)), u - 1e-9 * (u - l))
        grid = np.linspace(l, u, 19)
        slopes = [sign * self.dg(float(t)) for t in grid]
        cap = 1e8 * max(1.0, abs(self.g(l)), abs(self.g(u))) / max(u - l, 1e-12)
        s_lo, s_hi = max(min(slopes) - 1.0, -cap), min(max(slopes) + 1.0, cap)
        for _ in range(60):
            s = 0.5 * (s_lo + s_hi)
            _, arg = self._inner(sign, s, l, u, rigorous=False)
            if arg < xs:
                s_lo = s
            else:
                s_hi = s
            if s_hi - s_lo <= 1e-12 * (1.0 + abs(s)):
                break
        # Both bracket ends give valid lines; keep the one that is higher at xstar.
        best = None
        for s in (s_lo, s_hi):
            h, _ = self._inner(sign, s, l, u)
            h -= _SAFETY * (1.0 + abs(h))
            if best is None or s * xs + h > best[0] * xs + best[1]:
                best = (s, h)
        return best

    def under(self, l: float, u: float, xstar: float) -> tuple[float, float]:
        """g(x) >= a*x + c on [l,u]; returns (a, c)."""
        return self._support(+1, l, u, xstar)

    def over(self, l: float, u: float, xstar: float) -> tuple[float, float]:
        """g(x) <= a*x + c on [l,u]; returns (a, c)."""
        a, c = self._support(-1, l, u, xstar)
        return -a, -c

    def range(self, l: float, u: float) -> tuple[float, float]:
        lo, _ = self._inner(+1, 0.0, l, u)
        hi, _ = self._inner(-1, 0.0, l, u)
        return lo - _SAFETY * (1 + abs(lo)), -hi + _SAFETY * (1 + abs(hi))
