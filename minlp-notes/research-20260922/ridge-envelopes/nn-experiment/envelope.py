"""Batched Theorem 1 cuts with certified validity.

A problem asks for a linear underestimator of  s * sigma(a^T x + b)  on the box
[l, u] (s = +1: convex-envelope side, s = -1: concave-envelope side), deepest at
the point x. The 1-D factorable envelope of sigma on [L, U] is the case n = 1
(a = [1], b = 0, box [L, U]), so R0 and R1 cuts come from the same code.

Steps per problem:
 1. normalize (theory.md): flip a_i < 0, scale the box to [0,1]^n, absorb b;
    coordinates with a negligible range |a_i|(u_i - l_i) are fixed at their
    midpoint and paid for with a Lipschitz slack L1 * range / 2;
 2. staircase nodes t_k and weights p_k of x;
 3. solve (D) approximately: LP in y_k with exact concavity rows and chord rows
    (1-th) y_k + th y_{k+1} <= s sigma(t_k + th d_k) on a theta grid, refined at
    the most violated theta of each segment (all problems in one Gurobi model);
 4. repair and certify (required for validity on the whole box): each segment
    line l_k through (t_k, y_k), (t_{k+1}, y_{k+1}) is shifted down by a
    certified upper bound of max(l_k - s sigma) over its segment plus a margin,
    psi = min_k l_k is then concave and psi <= s sigma on I, and the cut uses
    y'_k = psi(t_k);
 5. cut h(x) = y'_0 + sum_j (y'_j - y'_{j-1}) xn_{pi(j)}, mapped back.

The certified bound in step 4 uses |sigma''| <= M2 (acts.py): on a piece of
length h (in theta), e <= max(e(ends)) + M2 d^2 h^2 / 8, with adaptive bisection.
"""
import math

import gurobipy as gp
import numpy as np
import scipy.sparse as sp
from gurobipy import GRB

from acts import ACTS

_ENV = None
_GR = (math.sqrt(5.0) - 1.0) / 2.0
DROP_REL = 1e-7     # coordinates with range <= DROP_REL * max(1, total range) are fixed
CERT_EPS = 1e-10    # absolute resolution of the certified maximum
MARGIN_REL = 1e-9   # safety margin, relative to max(1, |sigma| scale)
REFINE_TOL = 1e-7   # add a theta row when the chord violation exceeds this (cut loses at most this)
stats = dict(calls=0, problems=0, refine_rounds=0)


def env():
    global _ENV
    if _ENV is None:
        _ENV = gp.Env(empty=True)
        _ENV.setParam("OutputFlag", 0)
        _ENV.setParam("Threads", 1)
        _ENV.start()
    return _ENV


def lp_model():
    m = gp.Model(env=env())
    m.Params.FeasibilityTol = 1e-9
    m.Params.OptimalityTol = 1e-9
    m.Params.Presolve = 0
    m.Params.Method = 1
    return m


class Problem:
    __slots__ = ("sgn", "l", "u", "a", "b", "x", "tag", "keep", "flip", "base", "w", "b0", "slack",
                 "order", "t", "p", "d", "off", "y", "yc", "c0", "g", "value", "shift", "lpval")

    def __init__(self, sgn, l, u, a, b, x, tag=None):
        self.sgn, self.tag = sgn, tag
        self.l, self.u, self.a = (np.asarray(v, float) for v in (l, u, a))
        self.b = float(b)
        self.x = np.asarray(x, float)


def _prepare(P, act):
    r = np.abs(P.a) * np.maximum(P.u - P.l, 0.0)
    tot = r.sum()
    keep = r > DROP_REL * max(1.0, tot)
    mid = 0.5 * (P.l + P.u)
    P.slack = act.L1 * 0.5 * float(r[~keep].sum())
    P.keep = keep
    P.flip = np.sign(P.a[keep])
    P.base = np.where(P.flip > 0, P.l[keep], P.u[keep])
    P.w = (P.u - P.l)[keep]
    P.b0 = float(P.b + P.a[keep] @ P.base + P.a[~keep] @ mid[~keep])
    an = r[keep]
    xn = np.clip(P.flip * (P.x[keep] - P.base) / P.w, 0.0, 1.0)
    n = len(xn)
    order = np.argsort(-xn, kind="stable")
    xs = xn[order]
    p = np.empty(n + 1)
    if n == 0:
        p[0] = 1.0
    else:
        p[0] = 1.0 - xs[0]
        p[1:n] = xs[:-1] - xs[1:]
        p[n] = xs[-1]
    P.order = order
    P.t = P.b0 + np.concatenate([[0.0], np.cumsum(an[order])])  # nodes in sigma coordinates
    P.p = np.maximum(p, 0.0)
    P.d = np.diff(P.t)


def _golden_max(fun, lo, hi, iters=40):
    a, b = lo.copy(), hi.copy()
    c = b - _GR * (b - a)
    d = a + _GR * (b - a)
    fc, fd = fun(c), fun(d)
    for _ in range(iters):
        left = fc >= fd
        b = np.where(left, d, b)
        a = np.where(left, a, c)
        nc = b - _GR * (b - a)
        nd = a + _GR * (b - a)
        new_c = np.where(left, nc, d)
        new_d = np.where(left, c, nd)
        fnew = fun(np.where(left, nc, nd))
        fc, fd = np.where(left, fnew, fd), np.where(left, fc, fnew)
        c, d = new_c, new_d
    return np.where(fc >= fd, c, d), np.maximum(fc, fd)


def certified_max(act, sgn, T0, D, ya, yb, m0=16, maxit=60):
    """Certified upper bound, per segment, of max(0, max_{th in [0,1]} e(th)),
    e(th) = (1-th) ya + th yb - sgn sigma(T0 + th D).

    All arguments are arrays over segments. Returns (ub, lb, argmax_theta), where
    lb is the largest e found (exact value at argmax_theta).
    """
    S = len(T0)
    if S == 0:
        return np.zeros(0), np.zeros(0), np.zeros(0)
    th = np.linspace(0.0, 1.0, m0 + 1)
    E = (1 - th)[None, :] * ya[:, None] + th[None, :] * yb[:, None] - sgn[:, None] * act.f(T0[:, None] + th[None, :] * D[:, None])
    lb = E.max(axis=1)
    arg = th[E.argmax(axis=1)]
    D2 = D ** 2 / 8.0
    seg = np.repeat(np.arange(S), m0)
    ta = np.tile(th[:-1], S)
    tb = np.tile(th[1:], S)
    ea = E[:, :-1].ravel()
    eb = E[:, 1:].ravel()
    ub_final = lb + CERT_EPS

    def piece_ub(seg, ta, tb, ea, eb):
        # e'' = -sgn sigma'' D^2, so e <= max(ends) + max|sigma''| D^2 h^2 / 8 on a piece of length h
        M2 = act.M2_on(T0[seg] + ta * D[seg], T0[seg] + tb * D[seg])
        return np.maximum(ea, eb) + M2 * D2[seg] * (tb - ta) ** 2

    for _ in range(maxit):
        ub = piece_ub(seg, ta, tb, ea, eb)
        # only max(e, 0) matters for the shift, so resolve each segment to max(lb, 0) + eps
        act_mask = ub > np.maximum(lb[seg], 0.0) + CERT_EPS
        if not act_mask.any():
            break
        seg, ta, tb, ea, eb = seg[act_mask], ta[act_mask], tb[act_mask], ea[act_mask], eb[act_mask]
        tm = 0.5 * (ta + tb)
        em = (1 - tm) * ya[seg] + tm * yb[seg] - sgn[seg] * act.f(T0[seg] + tm * D[seg])
        better = em > lb[seg]
        if better.any():
            # several pieces of one segment may improve; take the best per segment
            order = np.argsort(em[better])
            s_b, e_b, t_b = seg[better][order], em[better][order], tm[better][order]
            lb[s_b] = np.maximum(lb[s_b], e_b)
            arg[s_b] = t_b  # last write per segment is the largest value
        seg = np.concatenate([seg, seg])
        ta, tb = np.concatenate([ta, tm]), np.concatenate([tm, tb])
        ea, eb = np.concatenate([ea, em]), np.concatenate([em, eb])
    else:
        np.maximum.at(ub_final, seg, piece_ub(seg, ta, tb, ea, eb))
    ub_final = np.maximum(ub_final, np.maximum(lb, 0.0) + CERT_EPS)
    return ub_final, lb, arg


def solve_batch(actname, problems, grid=9, grid1=129, refine_rounds=40):
    """Solve (D) for all problems and attach certified cuts (c0, g) and values."""
    act = ACTS[actname]
    if not problems:
        return problems
    for P in problems:
        _prepare(P, act)
    stats["calls"] += 1
    stats["problems"] += len(problems)
    # variable offsets
    off = 0
    for P in problems:
        P.off = off
        off += len(P.t)
    N = off
    m = lp_model()
    Y = m.addMVar(N, lb=-GRB.INFINITY, obj=np.concatenate([P.p for P in problems]))
    m.ModelSense = GRB.MAXIMIZE

    def add_sparse(k0, cols, vals, rhs):
        # rows r: sum_i vals[r, i] Y[cols[r, i]] <= rhs[r]
        R, K = cols.shape
        A = sp.csr_matrix((vals.ravel(), cols.ravel(), np.arange(0, R * K + 1, K)), shape=(R, N))
        m.addMConstr(A, Y, "<", rhs)
    # concavity rows (scaled): d_k y_{k-1} - (d_{k-1}+d_k) y_k + d_{k-1} y_{k+1} <= 0
    i0, c0, c1, c2 = [], [], [], []
    for P in problems:
        n = len(P.d)
        if n >= 2:
            dl, dr = P.d[:-1], P.d[1:]
            s = dl + dr
            i0.append(P.off + np.arange(n - 1))
            c0.append(dr / s)
            c1.append(-np.ones(n - 1))
            c2.append(dl / s)
    if i0:
        i0 = np.concatenate(i0)
        add_sparse(0, np.stack([i0, i0 + 1, i0 + 2], 1),
                   np.stack([np.concatenate(c0), np.concatenate(c1), np.concatenate(c2)], 1), np.zeros(len(i0)))
    # segment arrays
    segP = np.concatenate([np.full(len(P.d), i) for i, P in enumerate(problems)])
    segk = np.concatenate([P.off + np.arange(len(P.d)) for P in problems])
    T0 = np.concatenate([P.t[:-1] for P in problems])
    D = np.concatenate([P.d for P in problems])
    sg = np.array([P.sgn for P in problems], float)[segP]
    nseg_of = np.array([len(P.d) for P in problems])[segP]

    def add_rows(sidx, th):
        rhs = sg[sidx] * act.f(T0[sidx] + th * D[sidx])
        k = segk[sidx]
        add_sparse(0, np.stack([k, k + 1], 1), np.stack([1 - th, th], 1), rhs)

    if len(T0):
        g = np.where(nseg_of == 1, grid1, grid)
        sidx = np.repeat(np.arange(len(T0)), g)
        th = np.concatenate([np.linspace(0, 1, gi) for gi in g])
        add_rows(sidx, th)
    # problems with a single node (no kept coordinate): y_0 <= s sigma(t_0)
    for P in problems:
        if len(P.t) == 1:
            m.addConstr(Y[P.off] <= P.sgn * float(act.f(np.array([P.t[0]]))[0]))
    yv = None
    viol = np.zeros(0, bool)
    for _ in range(refine_rounds + 1):
        m.optimize()
        if m.Status != GRB.OPTIMAL:
            raise RuntimeError("D-LP status %d" % m.Status)
        yv = Y.X
        if not len(T0):
            break
        ya, yb = yv[segk], yv[segk + 1]
        ub, lbv, arg = certified_max(act, sg, T0, D, ya, yb)
        viol = lbv > REFINE_TOL
        if not viol.any():
            break
        add_rows(np.nonzero(viol)[0], arg[viol])
        stats["refine_rounds"] += 1
    lpval = float(m.ObjVal)
    m.dispose()
    for P in problems:
        P.y = yv[P.off:P.off + len(P.t)].copy()
    # repair and certify: ub is the certified maximum violation of the final yv
    if len(T0) and viol.any():
        ub, _, _ = certified_max(act, sg, T0, D, yv[segk], yv[segk + 1])
    for i, P in enumerate(problems):
        y = yv[P.off:P.off + len(P.t)]
        scale = max(1.0, float(np.abs(y).max()))
        margin = MARGIN_REL * scale
        n = len(P.d)
        if n == 0:
            yc = y - margin
        else:
            sel = segP == i
            shift = np.maximum(ub[sel], 0.0) + margin
            # lines l_k(s) = y_k - shift_k + slope_k (s - t_k), evaluated at all nodes
            slope = (y[1:] - y[:-1]) / P.d
            L = (y[:-1] - shift)[:, None] + slope[:, None] * (P.t[None, :] - P.t[:-1, None])
            yc = L.min(axis=0)
        P.yc = yc
        P.lpval = float(P.p @ y)
        # map back
        gn = np.diff(yc)
        gk = np.zeros(len(P.w))
        gk[P.order] = gn
        gfull = np.zeros(len(P.a))
        gfull[P.keep] = gk * P.flip / P.w
        P.g = gfull
        P.c0 = float(yc[0] - np.sum(gk * P.flip * P.base / P.w)) - P.slack
        P.value = float(P.c0 + P.g @ P.x)
    return problems


def cut_violation_samples(actname, P, npts=2000, rng=None, return_outside=False):
    """Max of h(x) - s sigma(a^T x + b) over random points, random vertices, all
    vertices (n <= 10) and x itself; should be <= 0.

    With return_outside, also returns the fraction of the sample points that lie
    outside the staircase simplex of the separation point (validity there relies
    on the concavity of psi, not only on the chord constraints).
    """
    act = ACTS[actname]
    rng = rng or np.random.default_rng(0)
    n = len(P.a)
    X = [rng.uniform(P.l, P.u, (npts, n)), np.where(rng.random((npts, n)) < 0.5, P.l, P.u), P.x[None, :]]
    if n <= 10:
        V = np.array(np.meshgrid(*[[0, 1]] * n)).reshape(n, -1).T
        X.append(np.where(V > 0, P.u, P.l))
    X = np.concatenate(X)
    viol = float(np.max(P.c0 + X @ P.g - P.sgn * act.f(X @ P.a + P.b)))
    if not return_outside:
        return viol
    Xn = P.flip * (X[:, P.keep] - P.base) / P.w
    inside = np.all(np.diff(Xn[:, P.order], axis=1) <= 1e-12, axis=1)
    return viol, float(1.0 - inside.mean())
