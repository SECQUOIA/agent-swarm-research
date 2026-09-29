"""Independent recheck library for gcs/a-priori-gap-bounds.md (written from the note's
definitions only; does not import the author's gcslib or the first reviewer's rgcs).

Sets are V-polytopes (vertex arrays) or Euclidean balls.  Lengths: 'l2', 'sq', 'l1',
('aff', c, d, b).  Squared-length perspectives use either an explicit rotated cone
(sq_mode='cone', default) or cvxpy's quad_over_lin (sq_mode='qol')."""
import itertools
import numpy as np
import cvxpy as cp
from scipy.optimize import linprog

SOLVER = "CLARABEL"


class PSet:
    def __init__(self, V=None, center=None, radius=None):
        if V is not None:
            self.kind = "poly"
            self.V = np.atleast_2d(np.asarray(V, float))
            self.dim = self.V.shape[1]
        else:
            self.kind = "ball"
            self.c = np.asarray(center, float)
            self.r = float(radius)
            self.dim = len(self.c)

    def persp(self, z, y):
        """constraints for (z, y) in the homogenization of the set (y >= 0 assumed)."""
        if self.kind == "poly":
            if self.V.shape[0] == 1:
                return [z == self.V[0] * y]
            a = cp.Variable(self.V.shape[0], nonneg=True)
            return [z == self.V.T @ a, cp.sum(a) == y]
        return [cp.norm(z - y * self.c, 2) <= y * self.r]

    def proj(self, x):
        """Euclidean projection (to clean solver noise)."""
        x = np.asarray(x, float)
        if self.kind == "ball":
            d = x - self.c
            n = np.linalg.norm(d)
            return x if n <= self.r else self.c + d * self.r / n
        if self.V.shape[0] == 1:
            return self.V[0].copy()
        # unsquared distance: a squared objective with ~1e-8 tolerance would move points by ~1e-4
        a = cp.Variable(self.V.shape[0], nonneg=True)
        pr = cp.Problem(cp.Minimize(cp.norm(self.V.T @ a - x)), [cp.sum(a) == 1])
        pr.solve(solver=SOLVER)
        if pr.value is not None and pr.value < 1e-7:
            return x  # inside up to solver noise: keep the point
        return self.V.T @ a.value


def pt(*x):
    return PSet(V=[list(x)])


def box(lo, hi):
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    V = [lo + (hi - lo) * np.array(b) for b in itertools.product([0, 1], repeat=len(lo))]
    return PSet(V=np.unique(np.array(V), axis=0))


# ------------------------------------------------------------------ lengths
def lval(kind, x, xp):
    x, xp = np.atleast_1d(np.asarray(x, float)), np.atleast_1d(np.asarray(xp, float))
    if kind == "l2":
        return float(np.linalg.norm(xp - x))
    if kind == "sq":
        return float(np.sum((xp - x) ** 2))
    if kind == "l1":
        return float(np.sum(np.abs(xp - x)))
    if isinstance(kind, tuple) and kind[0] == "aff":
        _, c, d, b = kind
        return float(c @ x + d @ xp + b)
    raise ValueError(kind)


def lpersp(kind, z, zp, y, cons, sq_mode="cone"):
    """perspective y*l(z/y, zp/y) as a cvxpy expression (may append constraints)."""
    if kind == "l2":
        return cp.norm(zp - z, 2)
    if kind == "sq":
        if sq_mode == "qol":
            return cp.quad_over_lin(zp - z, y)
        t = cp.Variable(nonneg=True)
        cons.append(cp.SOC(t + y, cp.hstack([2 * (zp - z), t - y])))  # |zp-z|^2 <= t*y
        return t
    if kind == "l1":
        return cp.norm1(zp - z)
    if isinstance(kind, tuple) and kind[0] == "aff":
        _, c, d, b = kind
        return c @ z + d @ zp + b * y
    raise ValueError(kind)


# ------------------------------------------------------------------ graph
class G:
    def __init__(self, sets, edges, s, t, length):
        self.sets, self.E, self.s, self.t = sets, list(edges), s, t
        self.len = length if isinstance(length, dict) else {e: length for e in self.E}
        self.inn = {v: [e for e in self.E if e[1] == v] for v in sets}
        self.out = {v: [e for e in self.E if e[0] == v] for v in sets}


def relax(g, hull=True, degree=False, sq_mode="cone", solver=SOLVER, extra=None, verbose=False, objective=None):
    """REL (hull=False) or REL_H (hull=True) as defined in note §1.  Returns (value, sol, status)."""
    y = {e: cp.Variable(nonneg=True) for e in g.E}
    z = {e: cp.Variable(g.sets[e[0]].dim) for e in g.E}
    zp = {e: cp.Variable(g.sets[e[1]].dim) for e in g.E}
    cons = []
    for e in g.E:
        cons += g.sets[e[0]].persp(z[e], y[e]) + g.sets[e[1]].persp(zp[e], y[e])
    cons += [sum(y[e] for e in g.out[g.s]) == 1, sum(y[e] for e in g.inn[g.t]) == 1]
    lam, w = {}, {}
    for v in g.sets:
        if v in (g.s, g.t):
            continue
        I, O = g.inn[v], g.out[v]
        if not I and not O:
            continue
        n = g.sets[v].dim
        yin = sum(y[e] for e in I) if I else 0
        yout = sum(y[f] for f in O) if O else 0
        cons.append(yin == yout)
        if degree and I:
            cons.append(yin <= 1)
        zin = sum(zp[e] for e in I) if I else np.zeros(n)
        zout = sum(z[f] for f in O) if O else np.zeros(n)
        cons.append(zin == zout)
        if hull and I and O:
            for e in I:
                for f in O:
                    lam[e, f] = cp.Variable(nonneg=True)
                    w[e, f] = cp.Variable(n)
                    cons += g.sets[v].persp(w[e, f], lam[e, f])
            for e in I:
                cons += [sum(lam[e, f] for f in O) == y[e], sum(w[e, f] for f in O) == zp[e]]
            for f in O:
                cons += [sum(lam[e, f] for e in I) == y[f], sum(w[e, f] for e in I) == z[f]]
    if extra is not None:
        cons += extra(g, y, z, zp, lam, w)
    if objective is None:
        obj = sum(lpersp(g.len[e], z[e], zp[e], y[e], cons, sq_mode) for e in g.E)
    else:  # e.g. a random strictly convex objective, to obtain fractional feasible points
        obj = objective(g, y, z, zp, lam, w)
    prob = cp.Problem(cp.Minimize(obj), cons)
    try:
        prob.solve(solver=solver, verbose=verbose)
    except cp.error.SolverError:
        return np.nan, None, "solver_error"
    if prob.status not in ("optimal", "optimal_inaccurate"):
        return np.nan, None, prob.status
    val = prob.solution.opt_val
    sol = dict(y={e: float(y[e].value) for e in g.E},
               z={e: np.array(z[e].value, float).ravel() for e in g.E},
               zp={e: np.array(zp[e].value, float).ravel() for e in g.E},
               lam={k: float(v.value) for k, v in lam.items()},
               w={k: np.array(v.value, float).ravel() for k, v in w.items()})
    return val, sol, prob.status


def simple_paths(g):
    res = []

    def dfs(v, path):
        if v == g.t:
            res.append(list(path))
            return
        for (_, x) in g.out[v]:
            if x not in path:
                path.append(x)
                dfs(x, path)
                path.pop()

    dfs(g.s, [g.s])
    return res


def path_cost(g, path, solver=SOLVER):
    x = {v: cp.Variable(g.sets[v].dim) for v in path}
    cons, terms = [], []
    for v in path:
        S = g.sets[v]
        if S.kind == "poly":
            if S.V.shape[0] == 1:
                cons.append(x[v] == S.V[0])
            else:
                a = cp.Variable(S.V.shape[0], nonneg=True)
                cons += [x[v] == S.V.T @ a, cp.sum(a) == 1]
        else:
            cons.append(cp.norm(x[v] - S.c) <= S.r)
    for u, v in zip(path[:-1], path[1:]):
        k = g.len[(u, v)]
        if k == "sq":
            terms.append(cp.sum_squares(x[v] - x[u]))
        else:
            terms.append(lpersp(k, x[u], x[v], 1.0, cons))
    prob = cp.Problem(cp.Minimize(sum(terms)), cons)
    prob.solve(solver=solver)
    return prob.value, {v: np.array(x[v].value, float).ravel() for v in path}


def opt_exact(g):
    best = (np.inf, None, None)
    for p in simple_paths(g):
        c, X = path_cost(g, p)
        if c < best[0]:
            best = (c, p, X)
    return best


# ------------------------------------------------------------------ concave envelope / Jensen defect
def pair_vertices(g, e):
    Vu, Vv = g.sets[e[0]].V, g.sets[e[1]].V
    K = [(a, b) for a in Vu for b in Vv]
    vals = np.array([lval(g.len[e], a, b) for a, b in K])
    M = np.array([np.r_[a, b] for a, b in K])
    return M, vals


def cav(g, e, x, xp, pen=1e4):
    """cav_e(x, xp) by LP over vertex pairs of K_e (poly sets).  A tiny L1 slack with large
    penalty absorbs solver noise in (x, xp) (the value then equals cav at a point within noise)."""
    M, vals = pair_vertices(g, e)
    k = np.r_[x, xp]
    m, d = M.shape
    # vars: p (m), sp (d), sm (d)
    c = np.r_[-vals, pen * np.ones(2 * d)]
    Aeq = np.vstack([np.hstack([M.T, np.eye(d), -np.eye(d)]), np.r_[np.ones(m), np.zeros(2 * d)]])
    beq = np.r_[k, 1.0]
    r = linprog(c, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * (m + 2 * d), method="highs")
    p = r.x[:m]
    return float(vals @ p), float(np.sum(r.x[m:]))


def jensen_defect(g, e):
    """Delta_e = max_{p in simplex} sum p l(k_i) - l(sum p k_i) (concave in p)."""
    M, vals = pair_vertices(g, e)
    k = g.len[e]
    if isinstance(k, tuple):
        return 0.0
    n = g.sets[e[0]].dim
    p = cp.Variable(len(vals), nonneg=True)
    mean = M.T @ p
    cons = [cp.sum(p) == 1]
    if k == "sq":
        expr = cp.sum_squares(mean[n:] - mean[:n])
    elif k == "l2":
        expr = cp.norm(mean[n:] - mean[:n], 2)
    else:
        expr = cp.norm1(mean[n:] - mean[:n])
    pr = cp.Problem(cp.Maximize(vals @ p - expr), cons)
    pr.solve(solver=SOLVER)
    return max(0.0, float(pr.value))


def longest_path_dag(g, weight):
    order = topo(g)
    best = {v: -np.inf for v in g.sets}
    best[g.s] = 0.0
    for v in order:
        if best[v] == -np.inf:
            continue
        for e in g.out[v]:
            best[e[1]] = max(best[e[1]], best[v] + weight[e])
    return best[g.t]


def topo(g):
    indeg = {v: len(g.inn[v]) for v in g.sets}
    q = [v for v in g.sets if indeg[v] == 0]
    order = []
    while q:
        v = q.pop()
        order.append(v)
        for e in g.out[v]:
            indeg[e[1]] -= 1
            if indeg[e[1]] == 0:
                q.append(e[1])
    return order


# ------------------------------------------------------------------ norm-case aperture
def sec_aperture(W):
    """sec(theta) for the cone generated by the points W (rows): max t s.t. a.w_hat >= t, |a|<=1."""
    W = np.atleast_2d(W)
    nr = np.linalg.norm(W, axis=1)
    if np.min(nr) < 1e-14:
        return np.inf
    Wh = W / nr[:, None]
    a, t = cp.Variable(W.shape[1]), cp.Variable()
    cp.Problem(cp.Maximize(t), [Wh @ a >= t, cp.norm(a) <= 1]).solve(solver=SOLVER)
    return np.inf if t.value <= 1e-12 else 1.0 / float(t.value)
