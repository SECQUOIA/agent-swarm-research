"""Certified curvature pieces of a univariate sympy expression.

``certify_pieces`` bisects [lo, hi] and evaluates the second derivative in
ball arithmetic (python-flint ``arb``).  An interval is labelled ``convex``
(``concave``) only when the enclosure of g'' is nonnegative (nonpositive).
Intervals narrower than ``min_width`` that cannot be decided are labelled
``unknown`` and carry a rigorous enclosure of g itself.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp
from flint import arb

X = sp.Symbol("X", real=True)


_ARB_FUNCS = {name: (lambda b, _n=name: getattr(b, _n)()) for name in
              ("exp", "log", "sin", "cos", "tan", "tanh", "sqrt", "atan", "sinh", "cosh")}
_ARB_FUNCS["Abs"] = abs


def compile_ball(e: sp.Expr):
    """Compile ``e`` once into a function of an ``arb`` ball (much faster than walking the tree)."""
    unsupported = {type(f).__name__ for f in e.atoms(sp.Function)} - set(_ARB_FUNCS)
    if unsupported or e.has(sp.Derivative, sp.zoo, sp.nan):
        raise NotImplementedError(f"unsupported in ball arithmetic: {unsupported or e}")
    f = sp.lambdify(X, e, modules=[_ARB_FUNCS, {"pi": arb.pi(), "E": arb(1).exp()}])
    return lambda x: arb(f(x))


def _ball(a: float, b: float) -> arb:
    return arb((a + b) / 2, (b - a) / 2).union(arb(a)).union(arb(b))


def range_enclosure(expr: sp.Expr, a: float, b: float, depth: int = 60, fn=None) -> arb:
    """Enclosure of expr on [a, b] that tolerates a singular endpoint (e.g. x**0.6 at 0).

    The interval is split dyadically towards an endpoint where ball evaluation
    fails; the remaining sliver of relative length 2**-depth (2**-20 at worst,
    see below) is represented by the exact value at the endpoint, so continuity
    of expr there is assumed.
    """
    fn = fn or compile_ball(expr)

    def ev(lo, hi):
        try:
            v = fn(_ball(lo, hi))
            return v if v.is_finite() else None
        except (ZeroDivisionError, ValueError):
            return None

    v = ev(a, b)
    if v is not None:
        return v
    for end, other in ((a, b), (b, a)):
        at = sp.N(expr.subs(X, sp.Float(end, 30)), 30)
        if not at.is_finite:
            continue
        acc = arb(float(at))
        hi = other
        ok = True
        for k in range(depth):
            lo = end + (other - end) * 2.0 ** (-k - 1)
            if lo == end:          # the rest is below floating-point resolution
                break
            piece = ev(min(lo, hi), max(lo, hi))
            if piece is None:
                # Rounding of the ball can touch the singular point when the endpoint is not 0.
                # Past 2**-20 of the sliver the endpoint value stands in, as for the final sliver.
                ok = k >= 20
                break
            acc = acc.union(piece)
            hi = lo
        if ok:
            return acc
    raise ValueError(f"cannot enclose expression on [{a}, {b}]")


@dataclass
class Piece:
    lo: float
    hi: float
    label: str                 # "convex", "concave", "unknown"
    glo: float = 0.0           # rigorous range of g, filled for "unknown" pieces
    ghi: float = 0.0


def certify_pieces(expr: sp.Expr, lo: float, hi: float, min_width: float = 1e-7,
                   max_intervals: int = 20000) -> list[Piece]:
    """Raises if ``expr`` uses unsupported functions, is too large, or needs too many intervals."""
    if sp.count_ops(expr) > 400:
        raise NotImplementedError("expression too large")
    g0, d2 = compile_ball(expr), compile_ball(sp.diff(expr, X, 2))
    d3 = compile_ball(sp.diff(expr, X, 3))
    min_width *= max(1.0, hi - lo)
    out: list[Piece] = []
    stack = [(lo, hi)]
    work = 0
    while stack:
        a, b = stack.pop()
        work += 1
        if work > max_intervals:
            raise ValueError("curvature certification needs too many intervals")
        try:
            ball = _ball(a, b)
            # g itself must be defined on the interval, not only its second derivative
            finite = g0(ball).is_finite()
            enc = d2(ball) if finite else None
            finite = finite and enc.is_finite()
        except (ZeroDivisionError, ValueError):
            finite = False
        if finite and not (enc >= 0 or enc <= 0):
            # Mean-value form of the second derivative, d2(m) + d3(I)(I - m): sharper on small intervals.
            try:
                mid = arb(0.5 * (a + b))
                mv = d2(mid) + d3(ball) * (ball - mid)
                if mv.is_finite() and (mv >= 0 or mv <= 0):
                    enc = mv
            except (ZeroDivisionError, ValueError):
                pass
        if finite and enc >= 0:
            label = "convex"
        elif finite and enc <= 0:
            label = "concave"
        elif b - a <= min_width:
            label = "unknown"
        else:
            mid = 0.5 * (a + b)
            stack += [(mid, b), (a, mid)]      # process the left half first
            continue
        if out and out[-1].label == label and label != "unknown":
            out[-1].hi = b
        else:
            out.append(Piece(a, b, label))
    for p in out:
        if p.label == "unknown":
            g = range_enclosure(expr, p.lo, p.hi, fn=g0)
            p.glo, p.ghi = float(g.lower()), float(g.upper())
    return out
