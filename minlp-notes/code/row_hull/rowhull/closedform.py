"""The closed-form row inequality

    sum_k min{ z_k / a_k, (w_k - z_k) / (w_k - b_k), tau_k / delta_k } >= 1,

valid when every vertex of {sum z = B, 0 <= z <= w} has exactly one coordinate
strictly inside its interval and, whenever that coordinate is k, its value lies
in [a_k, b_k] with 0 < a_k <= b_k < w_k; delta_k = min(gamma_k(a_k), gamma_k(b_k)).
It is the convex hull when all widths are equal (results/row-hull-separable-concave.md).

``residual_bounds`` computes outer bounds [a_k, b_k] with the interval subset-sum
program of ``pricing``; items that can never be the interior coordinate get None.
It returns None for the whole row if some vertex may have no interior coordinate.
"""
from __future__ import annotations

import numpy as np

from .pricing import States, add_items, TOL


def residual_bounds(row, kmax=4000):
    n, B, widths = row.n, row.B, row.widths
    tolB = 1e-7 * max(1.0, abs(B))
    if widths.max() - widths.min() <= 1e-9 * widths.max():      # equal widths: r = B mod w
        w = float(widths.mean())
        r = B - np.floor(B / w + 1e-9) * w
        if r <= tolB or r >= w - tolB:
            return None
        return [(r, r)] * n
    out = [None] * n
    ok = True

    def leaf(j, st):
        nonlocal ok
        w = widths[j]
        rlo, rhi = B - st.hi, B - st.lo
        feas = (rlo <= w + TOL * max(1.0, abs(B))) & (rhi >= -TOL * max(1.0, abs(B)))
        if not feas.any():
            return
        a = float(np.clip(rlo[feas], 0.0, w).min())
        b = float(np.clip(rhi[feas], 0.0, w).max())
        if a <= tolB or b >= w - tolB:
            ok = False           # a vertex with coordinate j at a bound: degenerate
        out[j] = (a, b)

    def rec(idxs, st):
        if not ok:
            return
        if len(idxs) == 1:
            leaf(idxs[0], st)
            return
        h = len(idxs) // 2
        L, R = idxs[:h], idxs[h:]
        zero = np.zeros(n)
        rec(L, add_items(st, R, widths, zero, B, kmax))
        rec(R, add_items(st, L, widths, zero, B, kmax))

    rec(list(np.argsort(-widths)), States.empty())
    return out if ok else None


def _z_expr(row, k):
    """z_k of a non-slack item as (const, {var: coef})."""
    it = row.items[k]
    if it.a > 0:
        return -it.a * it.lo, {it.var: it.a}
    return (-it.a) * it.hi, {it.var: it.a}


def equal_width_inequality_rows(row, tag):
    """Theorem 2(b): all non-slack widths equal w, row  sum z <= k w + r  or  sum z >= k w + r.

        sum_i min{z_i/r, (w-z_i)/(w-r), tau_i/delta_i} >= (sum z - k w)/r            (<=)
        sum_i min{z_i/r, (w-z_i)/(w-r), tau_i/delta_i} >= ((k+1) w - sum z)/(w-r)    (>=)
    """
    idx = [k for k in range(row.n) if k != row.slack]
    w = float(row.widths[idx].mean())
    kk = np.floor(row.B0 / w + 1e-9)
    r = row.B0 - kk * w
    if r <= 1e-7 * w or r >= (1 - 1e-7) * w:
        return None
    new_vars, lin, tot = {}, [], {}
    sum_const, sum_terms = 0.0, {}
    gain = False
    for k in idx:
        it = row.items[k]
        zv = f"zeta_{tag}_{k}"
        new_vars[zv] = (0.0, 1.0, "C")
        tot[zv] = 1.0
        c, terms = _z_expr(row, k)
        sum_const += c
        for kk_, vv in terms.items():
            sum_terms[kk_] = sum_terms.get(kk_, 0.0) + vv
        r1 = {zv: r}
        r2 = {zv: w - r}
        for kk_, vv in terms.items():
            r1[kk_] = r1.get(kk_, 0.0) - vv
            r2[kk_] = r2.get(kk_, 0.0) + vv
        lin.append((r1, "<=", c))
        lin.append((r2, "<=", w - c))
        d = float(it.gap(np.array([r]))[0]) if it.f is not None else 0.0
        if d > 1e-12:
            gain = True
            tau_row = {zv: d, it.var: it.chord[1]}
            for tv, tc in it.tvar.items():
                tau_row[tv] = tau_row.get(tv, 0.0) - tc
            lin.append((tau_row, "<=", -it.chord[0]))
    if not gain:
        return None
    lin.append((dict(tot), "<=", 1.0))
    if row.sense == "<=":      # r * sum zeta >= sum z - k w
        link = {zv: r for zv in tot}
        for kk_, vv in sum_terms.items():
            link[kk_] = link.get(kk_, 0.0) - vv
        lin.append((link, ">=", sum_const - kk * w))
    else:                      # (w-r) * sum zeta >= (k+1) w - sum z
        link = {zv: w - r for zv in tot}
        for kk_, vv in sum_terms.items():
            link[kk_] = link.get(kk_, 0.0) + vv
        lin.append((link, ">=", (kk + 1) * w - sum_const))
    return new_vars, lin


def closed_form_rows(row, tag, kmax=4000):
    """IR pieces for one row: (new_vars, lin_rows) or None."""
    if row.slack is not None:
        idx = [k for k in range(row.n) if k != row.slack]
        ww = row.widths[idx]
        if ww.max() - ww.min() <= 1e-9 * ww.max():
            return equal_width_inequality_rows(row, tag)
    rb = residual_bounds(row, kmax)
    if rb is None:
        return None
    gains = []
    for k, it in enumerate(row.items):
        if rb[k] is None:
            continue
        a, b = rb[k]
        d = float(min(it.gap(np.array([a]))[0], it.gap(np.array([b]))[0])) if it.f is not None else 0.0
        gains.append((k, a, b, d))
    if not gains or all(d <= 1e-9 for *_, d in gains):
        return None
    new_vars, lin = {}, []
    one = {}

    def z_expr(k):
        """z_k as (const, {var: coef}); the slack is B minus the others."""
        it = row.items[k]
        if it.var is None:
            const, terms = row.B, {}
            for q, o in enumerate(row.items):
                if q != k:
                    c, t = z_expr(q)
                    const -= c
                    for kk, vv in t.items():
                        terms[kk] = terms.get(kk, 0.0) - vv
            return const, terms
        if it.a > 0:
            return -it.a * it.lo, {it.var: it.a}
        return (-it.a) * it.hi, {it.var: it.a}

    for k, a, b, d in gains:
        it = row.items[k]
        zv = f"zeta_{tag}_{k}"
        new_vars[zv] = (0.0, 1.0, "C")
        one[zv] = 1.0
        c, terms = z_expr(k)
        # a*zeta <= z_k
        r1 = {zv: a}
        for kk, vv in terms.items():
            r1[kk] = r1.get(kk, 0.0) - vv
        lin.append((r1, "<=", c))
        # (w-b)*zeta <= w - z_k
        r2 = {zv: it.width - b}
        for kk, vv in terms.items():
            r2[kk] = r2.get(kk, 0.0) + vv
        lin.append((r2, "<=", it.width - c))
        if it.f is not None and d > 0:
            # d*zeta <= t - chord(v)
            tau_row = {zv: d, it.var: it.chord[1]}
            for tv, tc in it.tvar.items():
                tau_row[tv] = tau_row.get(tv, 0.0) - tc
            lin.append((tau_row, "<=", -it.chord[0]))
    lin.append((one, "==", 1.0))
    return new_vars, lin
