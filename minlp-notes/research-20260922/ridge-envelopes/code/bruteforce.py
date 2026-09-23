"""Brute-force envelopes, independent of Theorem 1.

1. grid_upper_box: LP over a regular grid of the box in the original
   coordinates (min sum lam f(z) s.t. sum lam z = x). Upper bound on vex f(x).
2. certified_bounds: exact semi-infinite LP over affine minorants of
   F(lam) = sigma(b + sum_j c_j . lam_j) on a product of simplices P (the box
   is the case of two-vertex blocks), solved by cutting planes. Separation of
   an affine function alpha + beta . lam is exact up to a 1-D search: for fixed
   s = sum_j c_j . lam_j, max beta . lam over P is the upper concave hull M(s)
   of the Minkowski sum of the block point sets {(c_ji, beta_ji)}; then
   max_s alpha + M(s) - sigma(b + s) is a 1-D problem (grid + golden refine).
   The LP value is an UPPER bound (finitely many constraints); the LP
   minorant shifted down by its true maximum violation gives a LOWER bound.
"""
import itertools

import gurobipy as gp
import numpy as np
from gurobipy import GRB

from common import golden_max, gurobi_model, local_maxima_rows


def grid_upper_box(sig, l, u, a, b, x, npts):
    grids = [np.linspace(l[i], u[i], npts) for i in range(len(l))]
    Z = np.array(list(itertools.product(*grids)))
    fz = sig(Z @ a + b)
    m = gurobi_model()
    lam = [m.addVar(lb=0.0) for _ in range(len(Z))]
    for i in range(Z.shape[1]):
        m.addConstr(gp.LinExpr(Z[:, i].tolist(), lam) == float(x[i]))
    m.addConstr(gp.LinExpr([1.0] * len(Z), lam) == 1.0)
    m.setObjective(gp.LinExpr(fz.tolist(), lam), GRB.MINIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    return m.ObjVal


def _upper_hull(c, v):
    o = np.lexsort((-v, c))
    pts = []
    for i in o:
        if pts and c[pts[-1]] == c[i]:
            continue
        while len(pts) >= 2:
            i0, i1 = pts[-2], pts[-1]
            if (c[i1] - c[i0]) * (v[i] - v[i0]) - (v[i1] - v[i0]) * (c[i] - c[i0]) >= 0:
                pts.pop()
            else:
                break
        pts.append(i)
    return pts


class MinkowskiSeparator:
    """max over P of beta . lam subject to c . lam = s, as a function of s."""

    def __init__(self, C, betas):
        self.C = C
        self.hulls = [_upper_hull(np.asarray(c, float), np.asarray(bt, float)) for c, bt in zip(C, betas)]
        edges = []
        for j, (c, bt, h) in enumerate(zip(C, betas, self.hulls)):
            for q in range(len(h) - 1):
                i0, i1 = h[q], h[q + 1]
                dc, dv = c[i1] - c[i0], bt[i1] - bt[i0]
                edges.append((dv / dc, dc, dv, j, i0, i1))
        edges.sort(key=lambda e: -e[0])
        self.edges = edges
        s0 = sum(c[h[0]] for c, h in zip(C, self.hulls))
        v0 = sum(bt[h[0]] for bt, h in zip(betas, self.hulls))
        self.S = np.concatenate([[s0], s0 + np.cumsum([e[1] for e in edges])])
        self.M = np.concatenate([[v0], v0 + np.cumsum([e[2] for e in edges])])

    def value(self, s):
        return np.interp(s, self.S, self.M)

    def point(self, s):
        lam = [np.zeros(len(c)) for c in self.C]
        state = [h[0] for h in self.hulls]
        e = int(np.searchsorted(self.S, s, side="right")) - 1
        e = min(max(e, 0), len(self.edges) - 1) if self.edges else -1
        for q in range(max(e, 0)):
            state[self.edges[q][3]] = self.edges[q][5]
        for j, st in enumerate(state):
            lam[j][st] = 1.0
        if e >= 0:
            _, dc, _, j, i0, i1 = self.edges[e]
            th = min(max((s - self.S[e]) / dc, 0.0), 1.0)
            lam[j][:] = 0.0
            lam[j][i0] = 1.0 - th
            lam[j][i1] = th
        return lam


def max_violation(sig, C, b, alpha, betas, ngrid=4001, topk=6):
    """Local maxima of alpha + beta.lam - sigma(b + c.lam) over P, refined.

    Returns list of (value, lam) sorted by value.
    """
    sep = MinkowskiSeparator(C, betas)
    lo, hi = sep.S[0], sep.S[-1]
    if hi <= lo:
        lam = sep.point(lo)
        return [(float(alpha + sep.value(lo) - sig(np.array([b + lo]))[0]), lam)]
    s = np.unique(np.concatenate([np.linspace(lo, hi, ngrid), sep.S]))
    g = lambda s_, _k=None: alpha + sep.value(s_) - sig(b + s_)
    vals = g(s)
    idx = np.nonzero(local_maxima_rows(vals))[0]
    idx = idx[np.argsort(-vals[idx])][:topk]
    lo_b = s[np.maximum(idx - 1, 0)]
    hi_b = s[np.minimum(idx + 1, len(s) - 1)]
    sr, vr = golden_max(lambda x_, k: g(x_), lo_b, hi_b)
    out = [(float(v), sep.point(x_)) for x_, v in zip(sr, vr)]
    out.sort(key=lambda e: -e[0])
    return out


def certified_bounds(sig, C, b, X, extra_points=(), tol=3e-9, maxit=3000):
    """Lower and upper bounds on vex_P F at X (list of block weight vectors)."""
    r = [len(c) for c in C]
    R = sum(r)
    offs = np.concatenate([[0], np.cumsum(r)])
    cflat = np.concatenate([np.asarray(c, float) for c in C])
    xflat = np.concatenate([np.asarray(x, float) for x in X])
    ss = sig(b + np.linspace(sum(min(c) for c in C), sum(max(c) for c in C), 2001))
    scale = max(1.0, float(ss.max() - ss.min()))
    m = gurobi_model()
    alpha = m.addVar(lb=-GRB.INFINITY)
    beta = [m.addVar(lb=-GRB.INFINITY) for _ in range(R)]
    for j in range(len(C)):  # remove the per-block redundancy
        beta[offs[j]].lb = 0.0
        beta[offs[j]].ub = 0.0
    m.setObjective(alpha + gp.LinExpr(xflat.tolist(), beta), GRB.MAXIMIZE)

    def add_point(lam):
        lf = np.concatenate(lam)
        m.addConstr(alpha + gp.LinExpr(lf.tolist(), beta) <= float(sig(np.array([b + cflat @ lf]))[0]))

    nvert = int(np.prod(r))
    verts = itertools.product(*[range(k) for k in r])
    if nvert > 4096:
        rng = np.random.default_rng(0)
        verts = [tuple(rng.integers(0, k) for k in r) for _ in range(4096)]
    for v in verts:
        add_point([np.eye(k)[i] for k, i in zip(r, v)])
    for lam in extra_points:
        add_point(lam)
    it = 0
    for it in range(maxit):
        m.optimize()
        assert m.Status == GRB.OPTIMAL, m.Status
        bv = np.array([v.X for v in beta])
        betas = [bv[offs[j]:offs[j + 1]] for j in range(len(C))]
        viol = max_violation(sig, C, b, alpha.X, betas)
        added = 0
        for v, lam in viol:
            if v > tol * scale:
                add_point(lam)
                added += 1
        if added == 0:
            break
    up = m.ObjVal
    V = max_violation(sig, C, b, alpha.X, betas, ngrid=200001, topk=10)[0][0]
    low = up - max(V, 0.0)
    return dict(low=low, up=up, iters=it + 1, final_viol=V, scale=scale)


def box_as_simplices(l, u, a, x):
    """Box [l,u] as a product of two-vertex simplices: z_i = l_i lam_i0 + u_i lam_i1."""
    C = [np.array([a_i * l_i, a_i * u_i]) for a_i, l_i, u_i in zip(a, l, u)]
    xi = (np.asarray(x) - l) / (u - l)
    X = [np.array([1.0 - t, t]) for t in xi]
    return C, X


def exact_cut_violation_box(sig, l, u, a, b, c0, g):
    """max over the box of h(z) - f(z) with h(z) = c0 + g.z (1-D reduction)."""
    C = [np.array([a_i * l_i, a_i * u_i]) for a_i, l_i, u_i in zip(a, l, u)]
    betas = [np.array([g_i * l_i, g_i * u_i]) for g_i, l_i, u_i in zip(g, l, u)]
    return max_violation(sig, C, b, c0, betas, ngrid=200001, topk=10)[0][0]


def exact_cut_violation_simplices(sig, C, b, c0, G):
    return max_violation(sig, C, b, c0, G, ngrid=200001, topk=10)[0][0]
