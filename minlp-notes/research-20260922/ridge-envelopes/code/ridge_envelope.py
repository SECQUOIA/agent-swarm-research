"""Envelope of f(x) = sigma(a^T x + b) over a box by Theorem 1 of theory.md.

The dual program (D) is solved by a cutting-plane LP in y = (psi(t_0), ..., psi(t_n)):
concavity of the interpolant is imposed exactly; the semi-infinite chord
constraints (1-th) y_k + th y_{k+1} <= sigma(t_k + th d_k) are separated on a grid
with golden-section refinement of every local maximum. At the end all y are
shifted down by the largest remaining chord violation found on a fine grid, so
the returned y define a feasible psi (up to the accuracy of that 1-D search) and
the returned value is a lower bound of (D). The final LP value is an upper bound
of (D) because the LP is a relaxation.
"""
import gurobipy as gp
import numpy as np
from gurobipy import GRB

from common import gurobi_model, maximize_rows


def _chord_violation_fun(t, y, sig):
    d = np.diff(t)

    def fun(theta, rows):
        return (1 - theta) * y[rows] + theta * y[rows + 1] - sig(t[rows] + theta * d[rows])

    return fun


def max_chord_violation(t, y, sig, ngrid=20001):
    """Largest value of (chord of (t_k, y_k)) - sigma over all segments."""
    if len(t) == 1:
        return float(y[0] - sig(np.array([t[0]]))[0])
    theta = np.linspace(0.0, 1.0, ngrid)
    grid = np.repeat(theta[None, :], len(t) - 1, axis=0)
    res = maximize_rows(_chord_violation_fun(t, y, sig), grid, topk=3)
    return max(float(r[0, 1]) for r in res)


def solve_D(t, p, sig, ngrid=401, tol=3e-9, maxit=400, kstar=None):
    """Solve (D) for nodes t (strictly increasing) and weights p.

    Returns dict with y (feasible node values), low (p.y), up (LP bound), viol.
    Tolerances are relative to scale = max(1, range of sigma on [t_0, t_n]).
    kstar (optional) restricts to the S-shape structure claimed in theory.md:
    y_k = sigma(t_k) for k > kstar and y_0..y_kstar collinear. Returns None if
    that restricted program is infeasible.
    """
    t = np.asarray(t, float)
    p = np.asarray(p, float)
    K = len(t)
    if K == 1:
        y = sig(t)
        return dict(y=y, low=float(y[0]), up=float(y[0]), viol=0.0, iters=0)
    ss = sig(np.linspace(t[0], t[-1], 2001))
    scale = max(1.0, float(ss.max() - ss.min()))
    d = np.diff(t)
    m = gurobi_model()
    y = [m.addVar(lb=-GRB.INFINITY) for _ in range(K)]
    m.setObjective(gp.LinExpr(p.tolist(), y), GRB.MAXIMIZE)
    for k in range(1, K - 1):
        m.addConstr((y[k + 1] - y[k]) / d[k] - (y[k] - y[k - 1]) / d[k - 1] <= 0)

    if kstar is not None:
        for k in range(kstar + 1, K):
            m.addConstr(y[k] == float(sig(np.array([t[k]]))[0]))
        for k in range(1, kstar):
            m.addConstr((y[k + 1] - y[k]) / d[k] - (y[k] - y[k - 1]) / d[k - 1] == 0)

    def add_cut(k, th):
        m.addConstr((1 - th) * y[k] + th * y[k + 1] <= float(sig(np.array([t[k] + th * d[k]]))[0]))

    for k in range(K - 1):
        for th in np.linspace(0, 1, 9):
            add_cut(k, th)
    theta = np.linspace(0.0, 1.0, ngrid)
    grid = np.repeat(theta[None, :], K - 1, axis=0)
    it = 0
    for it in range(maxit):
        m.optimize()
        if kstar is not None and m.Status in (GRB.INFEASIBLE, GRB.INF_OR_UNBD):
            return None
        assert m.Status == GRB.OPTIMAL, m.Status
        yv = np.array([v.X for v in y])
        res = maximize_rows(_chord_violation_fun(t, yv, sig), grid, topk=3)
        added = 0
        for k, r in enumerate(res):
            for th, v in r:
                if v > tol * scale:
                    add_cut(k, th)
                    added += 1
        if added == 0:
            break
    up = m.ObjVal
    V = max(0.0, max_chord_violation(t, yv, sig))
    yv = yv - V
    return dict(y=yv, low=float(p @ yv), up=float(up), viol=V, iters=it + 1, scale=scale)


def normalize(l, u, a, b):
    """Affine normalization of Theorem 1 (drop a_i = 0, flip a_i < 0, scale to [0,1])."""
    l, u, a = (np.asarray(v, float) for v in (l, u, a))
    keep = (a != 0) & (u > l)
    fixed = (a != 0) & (u == l)
    sgn = np.sign(a[keep])
    base = np.where(sgn > 0, l[keep], u[keep])
    w = (u - l)[keep]
    an = np.abs(a[keep]) * w
    b0 = float(b + a[keep] @ base + a[fixed] @ l[fixed])
    return dict(keep=keep, sgn=sgn, base=base, w=w, an=an, b0=b0)


def staircase(xn, an):
    """Nodes t_k and weights p_k of T_x for normalized x in [0,1]^n, a > 0."""
    n = len(xn)
    order = np.argsort(-xn, kind="stable")
    xs = np.clip(xn[order], 0.0, 1.0)
    p = np.empty(n + 1)
    p[0] = 1.0 - xs[0]
    p[1:n] = xs[:-1] - xs[1:]
    p[n] = xs[-1]
    t = np.concatenate([[0.0], np.cumsum(an[order])])
    return order, t, np.maximum(p, 0.0)


def envelope_box(sig, l, u, a, b, x, **kw):
    """vex over the box [l,u] of sigma(a^T z + b) at z = x, with a linear cut.

    Returns dict(value, value_up, c0, g, ...) where h(z) = c0 + g^T z is a valid
    underestimator with h(x) = value.
    """
    x = np.asarray(x, float)
    nd = normalize(l, u, a, b)
    keep = nd["keep"]
    b0 = nd["b0"]
    sig_n = lambda s: sig(np.asarray(s, float) + b0)
    if not keep.any():
        v = float(sig(np.array([b0]))[0])
        return dict(value=v, value_up=v, c0=v, g=np.zeros(len(x)), t=np.array([0.0]), p=np.array([1.0]), y=np.array([v]))
    xn = nd["sgn"] * (x[keep] - nd["base"]) / nd["w"]
    order, t, p = staircase(xn, nd["an"])
    D = solve_D(t, p, sig_n, **kw)
    y = D["y"]
    gn = np.zeros(len(xn))
    gn[order] = np.diff(y)
    g = np.zeros(len(x))
    g[keep] = gn * nd["sgn"] / nd["w"]
    c0 = float(y[0] - np.sum(gn * nd["sgn"] * nd["base"] / nd["w"]))
    return dict(value=D["low"], value_up=D["up"], c0=c0, g=g, t=t + b0, p=p, y=y, viol=D["viol"], iters=D["iters"])


def chain_law(C, X):
    """Comonotone sum of the block vertex laws sum_i X[j][i] delta_{C[j][i]}.

    Returns strictly increasing nodes t and weights p. The endpoints of
    I = [sum_j min C_j, sum_j max C_j] are added with weight 0 when missing.
    """
    cums, vals = [], []
    for c, x in zip(C, X):
        o = np.argsort(c, kind="stable")
        vals.append(np.asarray(c, float)[o])
        cums.append(np.cumsum(np.asarray(x, float)[o]))
    brk = np.unique(np.concatenate([[0.0]] + [np.minimum(cu, 1.0) for cu in cums] + [[1.0]]))
    nodes, wts = [], []
    for u0, u1 in zip(brk[:-1], brk[1:]):
        if u1 - u0 <= 0:
            continue
        mid = 0.5 * (u0 + u1)
        tv = sum(v[min(np.searchsorted(cu, mid, side="left"), len(v) - 1)] for v, cu in zip(vals, cums))
        nodes.append(tv)
        wts.append(u1 - u0)
    nodes, wts = np.array(nodes), np.array(wts)
    tu, inv = np.unique(nodes, return_inverse=True)
    pu = np.zeros(len(tu))
    np.add.at(pu, inv, wts)
    lo = sum(v[0] for v in vals)
    hi = sum(v[-1] for v in vals)
    if tu[0] > lo:
        tu, pu = np.concatenate([[lo], tu]), np.concatenate([[0.0], pu])
    if tu[-1] < hi:
        tu, pu = np.concatenate([tu, [hi]]), np.concatenate([pu, [0.0]])
    return tu, pu / pu.sum()


def envelope_simplices_merge(sig, C, b, X, **kw):
    """Corollary 3, original variables: (D) on the comonotone merged block laws."""
    t, p = chain_law(C, X)
    return solve_D(t, p, lambda s: sig(np.asarray(s, float) + b), **kw)


def envelope_simplices_tailsum(sig, C, b, X, **kw):
    """Corollary 3 via the tail-sum map to a chain order polytope and Theorem 1.

    Blocks must have distinct values. Returns value and a cut in the original
    one-hot variables: h(x) = c0 + sum_j G[j] . x_j.
    """
    a, z, meta = [], [], []
    b0 = b
    for j, (c, x) in enumerate(zip(C, X)):
        o = np.argsort(c, kind="stable")
        cs, xs = np.asarray(c, float)[o], np.asarray(x, float)[o]
        b0 += cs[0]
        tails = np.cumsum(xs[::-1])[::-1][1:]  # z_i = x_{i+1} + ... + x_r
        a.extend(np.diff(cs))
        z.extend(tails)
        meta.append(o)
    a, z = np.array(a), np.array(z)
    N = len(a)
    E = envelope_box(sig, np.zeros(N), np.ones(N), a, b0, z, **kw)
    # map the cut back: z_{j,i} = sum_{i' > i} x_{j,o[i']}
    G, pos = [], 0
    for c, o in zip(C, meta):
        r = len(c)
        gz = E["g"][pos:pos + r - 1]
        pos += r - 1
        gs = np.concatenate([[0.0], np.cumsum(gz)])  # coefficient of sorted vertex i
        gj = np.zeros(r)
        gj[o] = gs
        G.append(gj)
    E["G"] = G
    return E


def vex_interval_hull(sig, lo, hi, npts=20001):
    """Lower convex hull of dense samples of sigma on [lo, hi]; evaluate with np.interp."""
    s = np.linspace(lo, hi, npts)
    v = sig(s)
    hull = []
    for i in range(npts):
        while len(hull) >= 2:
            i0, i1 = hull[-2], hull[-1]
            if (s[i1] - s[i0]) * (v[i] - v[i0]) - (v[i1] - v[i0]) * (s[i] - s[i0]) <= 0:
                hull.pop()
            else:
                break
        hull.append(i)
    return s[hull], v[hull]
