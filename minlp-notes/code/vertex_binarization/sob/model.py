"""Separable problems, a small solver-neutral MINLP representation, and the
vertex binarization that maps one to the other.

Problem:   min  sum_i f_i(x_i) + c_y' y
           s.t. A x + B y  (<=, =)  b,   l <= x <= u,   y mixed-integer.

``original_ir`` states it directly.  ``binarized_ir`` adds, for every concave
piece of every f_i, the states "at the lower end", "at the upper end" and
"strictly inside", and the constraint that at most ``rank(A)`` variables are
strictly inside a concave piece (see results/separable-vertex-binarization.md).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import sympy as sp

from .functions import X, Univariate


@dataclass
class SeparableProblem:
    name: str
    funcs: list[Univariate]              # one per x_i; bounds live in the function
    A: np.ndarray                        # rows over x
    sense: list[str]                     # "<=", "==", ">=" per row
    b: np.ndarray
    B: np.ndarray | None = None          # rows over y
    c_y: np.ndarray | None = None
    y_lb: np.ndarray | None = None
    y_ub: np.ndarray | None = None
    y_type: list[str] = field(default_factory=list)   # "C", "B", "I"

    @property
    def n(self) -> int:
        return len(self.funcs)

    def concave_rank(self) -> int:
        """Rank of the columns of the variables that have a concave piece."""
        cols = [i for i, f in enumerate(self.funcs) if f.has_concave]
        return int(np.linalg.matrix_rank(self.A[:, cols])) if cols else 0


@dataclass
class IR:
    """Variables, linear rows, univariate definitions ``w == g(v)``, linear objective."""
    name: str
    vars: dict[str, tuple[float, float, str]] = field(default_factory=dict)
    lin: list[tuple[dict[str, float], str, float]] = field(default_factory=list)
    nl: list[tuple[str, sp.Expr, str]] = field(default_factory=list)   # (w, g(X), v)
    obj: dict[str, float] = field(default_factory=dict)
    obj_const: float = 0.0
    x_affine: list | None = None     # set by binarized_ir: recovers the eliminated x_i

    def var(self, name, lb, ub, vtype="C"):
        self.vars[name] = (float(lb), float(ub), vtype)
        return name


def _range(f: Univariate, expr: sp.Expr, lo: float, hi: float) -> tuple[float, float]:
    """Loose finite bounds for the value of ``expr`` on [lo, hi]."""
    g = sp.lambdify(X, expr, "numpy")
    v = np.broadcast_to(np.asarray(g(np.linspace(lo, hi, 201)), float), (201,))
    pad = 0.05 * (v.max() - v.min()) + 1e-6
    return float(v.min() - pad), float(v.max() + pad)


def _linking_rows(p: SeparableProblem, ir: IR, xaffine):
    """``xaffine(i)`` returns (constant, {var: coef}) with x_i = constant + sum coef*var."""
    for r in range(p.A.shape[0]):
        row: dict[str, float] = {}
        shift = 0.0
        for i in range(p.n):
            if p.A[r, i] != 0.0:
                const, terms = xaffine(i)
                shift += p.A[r, i] * const
                for k, c in terms.items():
                    row[k] = row.get(k, 0.0) + float(p.A[r, i]) * c
        if p.B is not None:
            row.update({f"y{j}": float(p.B[r, j]) for j in range(p.B.shape[1]) if p.B[r, j] != 0.0})
        ir.lin.append((row, p.sense[r], float(p.b[r] - shift)))


def _side_vars(p: SeparableProblem, ir: IR):
    if p.B is None:
        return
    for j in range(p.B.shape[1]):
        ir.var(f"y{j}", p.y_lb[j], p.y_ub[j], p.y_type[j])
        if p.c_y is not None and p.c_y[j] != 0.0:
            ir.obj[f"y{j}"] = float(p.c_y[j])


def original_ir(p: SeparableProblem) -> IR:
    ir = IR(p.name + "-orig")
    for i, f in enumerate(p.funcs):
        ir.var(f"x{i}", f.lo, f.hi)
        ir.var(f"w{i}", *_range(f, f.expr, f.lo, f.hi))
        ir.nl.append((f"w{i}", f.expr, f"x{i}"))
        ir.obj[f"w{i}"] = 1.0
    _side_vars(p, ir)
    _linking_rows(p, ir, lambda i: (0.0, {f"x{i}": 1.0}))
    return ir


def binarized_ir(p: SeparableProblem, budget: int | None = None) -> IR:
    """Vertex binarization.  ``budget`` defaults to ``p.concave_rank()``."""
    ir = IR(p.name + "-sob")
    budget = p.concave_rank() if budget is None else budget
    interior: list[str] = []
    ir.x_affine = []                 # x_i = const + sum coef*var; x_i itself is eliminated
    for i, f in enumerate(p.funcs):
        xdef: dict[str, float] = {}
        xdef_const = 0.0
        select = {}
        single = len(f.pieces) == 1
        for j, pc in enumerate(f.pieces):
            tag = f"{i}_{j}"
            length = pc.hi - pc.lo
            flo = float(sp.lambdify(X, pc.expr)(pc.lo))
            fhi = float(sp.lambdify(X, pc.expr)(pc.hi))
            if single:
                d = None
                ir.obj_const += flo
                xdef_const = pc.lo
            else:
                d = ir.var(f"d{tag}", 0, 1, "B")
                select[d] = 1.0
                ir.obj[d] = ir.obj.get(d, 0.0) + flo
                xdef[d] = pc.lo
            if pc.concave:
                up = ir.var(f"u{tag}", 0, 1, "B")
                t = ir.var(f"t{tag}", 0, 1, "B")
                s = ir.var(f"s{tag}", 0, length)
                g = ir.var(f"g{tag}", *_range(f, pc.expr.subs(X, pc.lo + X) - flo, 0, length))
                interior.append(t)
                xdef[up] = length
                xdef[s] = 1.0
                ir.lin.append(({s: 1.0, t: -length}, "<=", 0.0))
                row = {up: 1.0, t: 1.0}
                if d is not None:
                    row[d] = -1.0
                ir.lin.append((row, "<=", 0.0 if d is not None else 1.0))
                ir.obj[up] = fhi - flo
                ir.obj[g] = 1.0
                ir.nl.append((g, sp.expand(pc.expr.subs(X, pc.lo + X) - flo), s))
            else:
                # off = offset inside the piece; off == 0 when the piece is off.
                off = ir.var(f"o{tag}", 0, length)
                h = ir.var(f"h{tag}", *_range(f, pc.expr, pc.lo, pc.hi))
                xdef[off] = 1.0
                if d is not None:
                    ir.lin.append(({off: 1.0, d: -length}, "<=", 0.0))
                ir.nl.append((h, pc.expr.subs(X, pc.lo + X), off))
                ir.obj[h] = 1.0
                ir.obj_const -= flo    # h == flo when the piece is off; d adds it back when on
        if not single:
            ir.lin.append((select, "==", 1.0))
        ir.x_affine.append((xdef_const, xdef))
    if interior:
        ir.lin.append(({t: 1.0 for t in interior}, "<=", float(budget)))
    _side_vars(p, ir)
    _linking_rows(p, ir, lambda i: ir.x_affine[i])
    return ir
