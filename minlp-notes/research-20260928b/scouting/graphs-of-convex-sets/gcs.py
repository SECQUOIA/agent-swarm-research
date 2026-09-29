"""Small GCS shortest-path toolkit for integrality-gap experiments.

Sets are convex: ('point', c), ('ball', c, r), ('box', lo, hi), ('poly', A, b).
Edge length: ||x_v - x_u||_2 (norm='l2') or ||x_v - x_u||_2^2 (norm='sq').
Graph: DAG given as edge list; s, t fixed.

relax(inst, hull=False): perspective relaxation of Marcucci et al. (SIOPT 2024,
eq. (5.5)); hull=True adds the vertex-local convex hull (their eq. (7.4)).
exact(inst): enumerate all s-t paths and solve each convex restriction.
"""
import itertools
import numpy as np
import cvxpy as cp

SOLVER = "CLARABEL"


def persp(S, z, y):
    """Constraints (z, y) in homogenization of set S."""
    kind = S[0]
    if kind == "point":
        return [z == y * np.asarray(S[1], float)]
    if kind == "ball":
        c, r = np.asarray(S[1], float), float(S[2])
        return [cp.norm(z - y * c, 2) <= r * y]
    if kind == "box":
        lo, hi = np.asarray(S[1], float), np.asarray(S[2], float)
        return [z >= y * lo, z <= y * hi]
    if kind == "poly":
        A, b = np.asarray(S[1], float), np.asarray(S[2], float)
        return [A @ z <= y * b]
    raise ValueError(kind)


def member(S, x):
    return persp(S, x, 1.0)


def edge_cost(z, zp, y, norm, lin=None):
    if norm == "lin":
        c, d = lin
        return c @ z + d @ zp
    if norm == "l2":
        return cp.norm(zp - z, 2)
    if norm == "sq":
        return cp.quad_over_lin(zp - z, y)
    raise ValueError(norm)


class Inst:
    def __init__(self, sets, edges, s, t, dim, norm="l2"):
        self.sets, self.edges, self.s, self.t = sets, list(edges), s, t
        self.dim, self.norm = dim, norm
        self.V = sorted(sets)
        self.inn = {v: [e for e in self.edges if e[1] == v] for v in self.V}
        self.out = {v: [e for e in self.edges if e[0] == v] for v in self.V}


def relax(inst, hull=False, return_sol=False, mip=False):
    n = inst.dim
    y = {e: (cp.Variable(boolean=True) if mip else cp.Variable(nonneg=True)) for e in inst.edges}
    z = {e: cp.Variable(n) for e in inst.edges}
    zp = {e: cp.Variable(n) for e in inst.edges}
    cons = []
    for e in inst.edges:
        u, v = e
        cons += persp(inst.sets[u], z[e], y[e])
        cons += persp(inst.sets[v], zp[e], y[e])
    s, t = inst.s, inst.t
    cons.append(sum(y[e] for e in inst.out[s]) == 1)
    cons.append(sum(y[e] for e in inst.inn[t]) == 1)
    pair = {}
    for v in inst.V:
        if v in (s, t):
            continue
        I, O = inst.inn[v], inst.out[v]
        if not I and not O:
            continue
        yin = sum(y[e] for e in I) if I else 0
        yout = sum(y[e] for e in O) if O else 0
        cons.append(yin == yout)
        cons.append(yin <= 1)
        zin = sum(zp[e] for e in I) if I else np.zeros(n)
        zout = sum(z[e] for e in O) if O else np.zeros(n)
        cons.append(zin == zout)
        # degree-constraint lift (Lemma 5.4 applied to y_v <= 1); needs a free x_v
        xv = cp.Variable(n)
        cons += persp(inst.sets[v], xv - zin, 1 - yin)
        if hull and I and O:
            for e in I:
                for f in O:
                    lam = cp.Variable(nonneg=True)
                    w = cp.Variable(n)
                    pair[(e, f)] = (lam, w)
                    cons += persp(inst.sets[v], w, lam)
            for e in I:
                cons.append(sum(pair[(e, f)][0] for f in O) == y[e])
                cons.append(sum(pair[(e, f)][1] for f in O) == zp[e])
            for f in O:
                cons.append(sum(pair[(e, f)][0] for e in I) == y[f])
                cons.append(sum(pair[(e, f)][1] for e in I) == z[f])
    obj = sum(edge_cost(z[e], zp[e], y[e], inst.norm, getattr(inst, 'lin', {}).get(e)) for e in inst.edges)
    prob = cp.Problem(cp.Minimize(obj), cons)
    if mip:
        prob.solve(solver='SCIP', scip_params={'limits/time': 600})
    else:
        prob.solve(solver=SOLVER)
    if prob.status not in ("optimal", "optimal_inaccurate"):
        raise RuntimeError(prob.status)
    if not return_sol:
        return prob.value
    sol = {
        "y": {e: float(y[e].value) for e in inst.edges},
        "z": {e: np.array(z[e].value) for e in inst.edges},
        "zp": {e: np.array(zp[e].value) for e in inst.edges},
        "pair": {k: (float(l.value), np.array(w.value)) for k, (l, w) in pair.items()},
    }
    return prob.value, sol


def all_paths(inst):
    out = {}
    for u, v in inst.edges:
        out.setdefault(u, []).append(v)
    res = []

    def dfs(v, path):
        if v == inst.t:
            res.append(list(path))
            return
        for w in out.get(v, []):
            if w not in path:
                path.append(w)
                dfs(w, path)
                path.pop()

    dfs(inst.s, [inst.s])
    return res


def path_cost(inst, path, return_x=False):
    n = inst.dim
    x = {v: cp.Variable(n) for v in path}
    cons = []
    for v in path:
        cons += member(inst.sets[v], x[v])
    if inst.norm == "lin":
        obj = sum(inst.lin[(a, b)][0] @ x[a] + inst.lin[(a, b)][1] @ x[b] for a, b in zip(path, path[1:]))
    elif inst.norm == "l2":
        obj = sum(cp.norm(x[b] - x[a], 2) for a, b in zip(path, path[1:]))
    else:
        obj = sum(cp.sum_squares(x[b] - x[a]) for a, b in zip(path, path[1:]))
    prob = cp.Problem(cp.Minimize(obj), cons)
    prob.solve(solver=SOLVER)
    if return_x:
        return prob.value, {v: x[v].value for v in path}
    return prob.value


def exact(inst, return_path=False):
    best, bp = np.inf, None
    for p in all_paths(inst):
        c = path_cost(inst, p)
        if c < best:
            best, bp = c, p
    return (best, bp) if return_path else best
