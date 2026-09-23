"""Univariate functions with certified concave pieces.

A function is a sympy expression in the symbol ``X``.  Its domain ``[lo, hi]``
is split at kinks (supplied by the caller); between kinks the second
derivative is enclosed in ball arithmetic and an interval is tagged
``concave`` only when the enclosure is nonpositive.  Everything else,
including undecided slivers around inflection points, is passed to the solver
unchanged.  Only the ``concave`` tag carries a claim (the vertex theorem).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "univariate_envelopes"))
from uenv.curvature import X as UX, certify_pieces  # noqa: E402

X = sp.Symbol("X", real=True)


@dataclass
class Piece:
    lo: float
    hi: float
    concave: bool
    expr: sp.Expr  # smooth expression valid on [lo, hi] (Abs resolved)


@dataclass
class Univariate:
    expr: sp.Expr
    lo: float
    hi: float
    kinks: tuple[float, ...] = ()
    pieces: list[Piece] = field(default_factory=list)

    def __post_init__(self):
        if not self.pieces:
            self.pieces = _curvature_pieces(self)
        self._f = sp.lambdify(X, self.expr, "numpy")

    def __call__(self, x):
        return float(self._f(x))

    @property
    def has_concave(self) -> bool:
        return any(p.concave for p in self.pieces)


def _resolve_abs(expr: sp.Expr, at: float) -> sp.Expr:
    """Replace every Abs(g) by +g or -g according to the sign of g at ``at``."""
    def repl(arg):
        return arg if float(arg.subs(X, at)) >= 0 else -arg
    return expr.replace(sp.Abs, repl)


def _curvature_pieces(u: Univariate) -> list[Piece]:
    """Certified pieces: between kinks, g'' is enclosed in ball arithmetic (uenv.curvature).

    Undecided slivers around inflection points are returned as non-concave pieces.
    """
    cuts = sorted({u.lo, u.hi, *[k for k in u.kinks if u.lo < k < u.hi]})
    pieces: list[Piece] = []
    for a, b in zip(cuts[:-1], cuts[1:]):
        smooth = _resolve_abs(u.expr, 0.5 * (a + b))
        for c in certify_pieces(smooth.subs(X, UX), a, b):
            conc = c.label == "concave"
            if pieces and not conc and not pieces[-1].concave and pieces[-1].expr == smooth:
                pieces[-1].hi = c.hi
            else:
                pieces.append(Piece(c.lo, c.hi, conc, smooth))
    return pieces
