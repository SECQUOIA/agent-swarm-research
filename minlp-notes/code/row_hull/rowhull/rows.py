"""Normalized single-row sets.

A row  sum_i a_i v_i (<=,==,>=) b  with bounds l <= v <= u is rewritten as

    sum_k z_k = B,   0 <= z_k <= width_k,

where z_k = a_k (v_k - l_k) for a_k > 0 and z_k = |a_k| (u_k - v_k) for
a_k < 0, plus one slack item for an inequality.  Items whose variable carries a
function f_k that is concave on [l_k, u_k] have the *gap function*

    gamma_k(z) = f_k(v_k(z)) - chord_k(v_k(z)) >= 0,

concave in z and zero at both ends.  All other items have gamma = 0.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Item:
    var: str | None            # model variable name; None for the slack
    a: float                   # row coefficient (sign gives the orientation); 1.0 for slack
    lo: float
    hi: float
    width: float
    tvar: dict | None = None   # epigraph expression {var: coef} if the item has a concave term
                               # (a single epigraph variable, or t + c*y for a fixed charge c with indicator y)
    f: object = None           # vectorized callable on the original variable
    rho: float = 0.0           # max of the gap function (normalization only)
    chord: tuple[float, float] = (0.0, 0.0)   # chord(v) = c0 + c1 v

    def v_of_z(self, z):
        return self.lo + z / self.a if self.a > 0 else self.hi - z / (-self.a)

    def z_of_v(self, v):
        return self.a * (v - self.lo) if self.a > 0 else (-self.a) * (self.hi - v)

    def gap(self, z):
        """gamma(z) for an array z in [0, width]."""
        z = np.asarray(z, float)
        if self.f is None:
            return np.zeros_like(z)
        v = self.v_of_z(z)
        # The inverse affine map can round an exact endpoint into the open
        # interval. At a downward endpoint jump that changes f by an O(1)
        # amount, so evaluate the original endpoint and impose its exact gap.
        v = np.where(z == 0.0, self.lo if self.a > 0 else self.hi, v)
        v = np.where(z == self.width, self.hi if self.a > 0 else self.lo, v)
        g = np.asarray(self.f(v), float) - (self.chord[0] + self.chord[1] * v)
        return np.where((z == 0.0) | (z == self.width), 0.0, np.maximum(g, 0.0))


@dataclass
class NormRow:
    items: list[Item]
    B: float
    slack: int | None = None   # index of the slack item
    name: str = ""
    const: float = 0.0         # B = rhs - const, kept for reporting
    sense: str = "=="
    B0: float = 0.0            # right-hand side in z before the slack was added

    @property
    def n(self):
        return len(self.items)

    @property
    def widths(self):
        return np.array([it.width for it in self.items])

    @property
    def concave(self):
        return [k for k, it in enumerate(self.items) if it.f is not None]


def make_item(var, a, lo, hi, tvar=None, f=None):
    if isinstance(tvar, str):
        tvar = {tvar: 1.0}
    it = Item(var, float(a), float(lo), float(hi), abs(float(a)) * (float(hi) - float(lo)), tvar, f)
    if f is not None:
        flo, fhi = float(f(np.array([lo]))[0]), float(f(np.array([hi]))[0])
        c1 = (fhi - flo) / (hi - lo)
        it.chord = (flo - c1 * lo, c1)
        grid = np.r_[np.linspace(0.0, it.width, 129), 1e-9 * it.width, (1 - 1e-9) * it.width]
        it.rho = float(it.gap(grid).max())
        if it.rho <= 1e-10 * max(1.0, abs(flo), abs(fhi)):
            it.f, it.tvar, it.rho = None, None, 0.0     # numerically linear
    return it


def normalize_row(entries, sense, rhs, name=""):
    """entries: list of (var, a, lo, hi, tvar, f).  Returns NormRow or None if nothing to gain."""
    items, const = [], 0.0
    for var, a, lo, hi, tvar, f in entries:
        if a == 0.0:
            continue
        if hi - lo <= 1e-12:
            const += a * lo
            continue
        it = make_item(var, a, lo, hi, tvar, f)
        const += a * lo if a > 0 else a * hi
        items.append(it)
    B = rhs - const
    B0 = B
    total = sum(it.width for it in items)
    slack = None
    if sense == "<=":
        if B < total - 1e-12:
            items.append(Item(None, 1.0, 0.0, max(B, 0.0), max(B, 0.0)))
            slack = len(items) - 1
        else:
            return None          # row is redundant on the box
    elif sense == ">=":
        # sum z - s = B, s in [0, total-B]; with s' = (total-B) - s: sum z + s' = total
        if B > 1e-12:
            items.append(Item(None, 1.0, 0.0, total - B, total - B))
            slack = len(items) - 1
            B = total
        else:
            return None
    row = NormRow(items, float(B), slack, name, const, sense, float(B0))
    if not row.concave:
        return None
    return row
