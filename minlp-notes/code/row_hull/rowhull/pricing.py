"""Pricing over the vertices of  {sum z = B, 0 <= z <= width}.

A vertex is (S, j): z_i = width_i on S, z_j = r = B - width(S) in [0, width_j],
zero elsewhere.  For duals (pi, omega) we need

    phi* = min_{(S,j)}  omega_j gamma_j(r) - pi_j r - sum_{i in S} pi_i width_i .

The subset sums are tracked by a sparse dynamic program.  When the number of
distinct sums exceeds ``kmax`` they are merged into intervals [lo, hi] that
keep the largest profit; since r -> omega_j gamma_j(r) - pi_j r is concave, its
minimum over the induced r-interval is attained at an endpoint.  The returned
``lower`` is therefore a valid lower bound on phi* (up to floating point),
and equals phi* when no merging happened.  Each state keeps the bitmask of one
subset, from which exact vertices are rebuilt for column generation.
"""
from __future__ import annotations

import numpy as np

TOL = 1e-9


class States:
    __slots__ = ("lo", "hi", "P", "mask", "merged")

    def __init__(self, lo, hi, P, mask, merged=False):
        self.lo, self.hi, self.P, self.mask, self.merged = lo, hi, P, mask, merged

    @classmethod
    def empty(cls):
        return cls(np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1, dtype=np.uint64), False)


def _compress(lo, hi, P, mask, B, kmax, merged):
    scale = max(1.0, abs(B))
    # Sums that agree up to rounding belong to one state: keep the largest profit (and its subset),
    # the smallest lo and the largest hi.  (Sorting by profit inside a float tie is not enough:
    # 2.37 + 5.12 and 3.49 + 4.00 differ in the last place, and the order would follow that error.)
    order = np.lexsort((hi, lo))
    lo, hi, P, mask = lo[order], hi[order], P[order], mask[order]
    new = np.ones(len(lo), bool)
    new[1:] = (lo[1:] - lo[:-1] > 1e-11 * scale) | (np.abs(hi[1:] - hi[:-1]) > 1e-11 * scale)
    if not new.all():
        starts = np.flatnonzero(new)
        grp = np.cumsum(new) - 1
        best = np.maximum.reduceat(P, starts)
        idx = np.flatnonzero(P >= best[grp])
        first = np.unique(grp[idx], return_index=True)[1]
        lo, hi, P, mask = (np.minimum.reduceat(lo, starts), np.maximum.reduceat(hi, starts),
                           best, mask[idx[first]])
    if len(lo) > kmax:
        merged = True
        edges = np.minimum((lo / (B + 1e-300) * kmax).astype(np.int64), kmax - 1)
        starts = np.flatnonzero(np.r_[True, edges[1:] != edges[:-1]])
        hi2 = np.maximum.reduceat(hi, starts)
        lo2 = lo[starts]
        # argmax of P within each group
        grp = np.repeat(np.arange(len(starts)), np.diff(np.r_[starts, len(lo)]))
        best = np.full(len(starts), -np.inf)
        np.maximum.at(best, grp, P)
        idx = np.flatnonzero(P >= best[grp])
        first = np.unique(grp[idx], return_index=True)[1]
        mask2 = mask[idx[first]]
        lo, hi, P, mask = lo2, hi2, best, mask2
    return States(lo, hi, P, mask, merged)


def add_items(st: States, idxs, widths, profit, B, kmax):
    for i in idxs:
        w, p = widths[i], profit[i]
        ok = st.lo + w <= B + TOL * max(1.0, abs(B))
        if not ok.any():
            continue
        nm = st.mask[ok] | (np.uint64(1) << np.uint64(i))
        st = _compress(np.r_[st.lo, st.lo[ok] + w], np.r_[st.hi, st.hi[ok] + w],
                       np.r_[st.P, st.P[ok] + p], np.r_[st.mask, nm], B, kmax, st.merged)
    return st


def price(row, pi, omega, kmax=4000, per_item=True):
    """Return (lower, columns).  columns: list of exact vertices (mask, j, r, value)."""
    n, B, widths = row.n, row.B, row.widths
    assert n <= 63, "rows with more than 63 items are not supported"
    profit = pi * widths
    tolB = TOL * max(1.0, abs(B))
    best_lower = np.inf
    cols = []

    def leaf(j, st):
        nonlocal best_lower
        it = row.items[j]
        rlo, rhi = B - st.hi, B - st.lo
        feas = (rlo <= it.width + tolB) & (rhi >= -tolB)
        if not feas.any():
            return
        a = np.clip(rlo[feas], 0.0, it.width)
        b = np.clip(rhi[feas], 0.0, it.width)
        ha = omega[j] * it.gap(a) - pi[j] * a
        hb = omega[j] * it.gap(b) - pi[j] * b
        val = np.minimum(ha, hb) - st.P[feas]
        k = int(np.argmin(val))
        best_lower = min(best_lower, float(val[k]))
        # exact vertex from the representative subset
        mask = int(st.mask[feas][k])
        wS = sum(widths[i] for i in range(n) if mask >> i & 1)
        r = B - wS
        if -tolB <= r <= it.width + tolB:
            r = min(max(r, 0.0), it.width)
            exact = omega[j] * float(it.gap(np.array([r]))[0]) - pi[j] * r - sum(
                profit[i] for i in range(n) if mask >> i & 1)
            cols.append((mask, j, r, exact))

    def rec(idxs, st):
        if len(idxs) == 1:
            leaf(idxs[0], st)
            return
        h = len(idxs) // 2
        L, R = idxs[:h], idxs[h:]
        rec(L, add_items(st, R, widths, profit, B, kmax))
        rec(R, add_items(st, L, widths, profit, B, kmax))

    # adding items in order of decreasing width keeps the state sets small longer
    order = list(np.argsort(-widths))
    rec(order, States.empty())
    return best_lower, cols
