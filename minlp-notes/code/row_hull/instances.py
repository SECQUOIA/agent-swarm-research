"""Instance families for the row-hull study: concave-cost transportation problems."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vertex_binarization"))
from sob.functions import X, Univariate, Piece  # noqa: E402
from sob.model import SeparableProblem  # noqa: E402


def _concave(expr, lo, hi):
    """Univariate with the concavity supplied by construction (no certification run)."""
    return Univariate(expr, lo, hi, pieces=[Piece(lo, hi, True, expr)])


def transport(m, n, seed, cap="uniform", cost="quad"):
    """m sources, n sinks, arcs (i,j) -> variable i*n+j.

    cap: 'uniform' (all capacities 1, supplies/demands in [1.2,3.8]),
         'random'  (capacities U(2,8), supplies/demands U(5,15)),
         'uncap'   (capacity min(s_i,d_j)).
    cost: 'quad' a x - b x^2 increasing on the arc; 'sqrt' c sqrt(x); 'pow' c x^0.6.
    """
    rng = np.random.default_rng(seed)
    if cap == "uniform":
        s = rng.uniform(1.2, 3.8, m); d = rng.uniform(1.2, 3.8, n)
    else:
        s = rng.uniform(5, 15, m); d = rng.uniform(5, 15, n)
    d *= s.sum() / d.sum()
    s, d = np.round(s, 4), np.round(d, 4)
    d[-1] = round(s.sum() - d[:-1].sum(), 4)
    if cap == "uniform":
        U = np.ones((m, n))
    elif cap == "random":
        U = np.round(rng.uniform(2, 8, (m, n)), 2)
    else:
        U = np.minimum.outer(s, d)
    assert (U.sum(1) >= s).all() and (U.sum(0) >= d).all(), "infeasible draw"
    funcs = []
    for i in range(m):
        for j in range(n):
            u = float(U[i, j])
            if cost == "quad":
                b = rng.uniform(0.5, 1.5) / u
                a = 2 * b * u + rng.uniform(0.0, 2.0)
                expr = sp.Float(a) * X - sp.Float(b) * X**2
            elif cost == "sqrt":
                expr = sp.Float(rng.uniform(1, 5)) * sp.sqrt(X)
            elif cost == "log":          # smooth economies of scale with a finite slope at zero
                expr = sp.Float(rng.uniform(1, 5)) * sp.log(1 + sp.Float(4.0 / u) * X)
            else:
                expr = sp.Float(rng.uniform(1, 5)) * X ** sp.Float(0.6)
            funcs.append(_concave(expr, 0.0, u))
    A = np.zeros((m + n, m * n))
    for i in range(m):
        A[i, i * n:(i + 1) * n] = 1.0
    for j in range(n):
        A[m + j, j::n] = 1.0
    b = np.r_[s, d]
    return SeparableProblem(f"transport-{cap}-{cost}-{m}x{n}-s{seed}", funcs, A, ["=="] * (m + n), b)


def netflow(nv, deg, seed, cap="random", cost="sqrt"):
    """Single-commodity transshipment on a random sparse digraph with concave arc costs.

    Every node gets ``deg`` random out-neighbours; a third of the nodes are sources, a third sinks.
    cap: 'uniform' (all arc capacities 1) or 'random' (U(2,8) rounded to 2 decimals).
    Supplies are scaled so that a feasible flow exists (checked by a linear program).
    """
    import gurobipy as gp
    rng = np.random.default_rng(seed)
    return _netflow(nv, deg, seed, cap, cost, rng, gp)


def _netflow(nv, deg, seed, cap, cost, rng, gp):
    arcs = sorted({(i, int(j)) for i in range(nv) for j in rng.choice([k for k in range(nv) if k != i], deg, replace=False)})
    U = np.ones(len(arcs)) if cap == "uniform" else np.round(rng.uniform(2, 8, len(arcs)), 2)
    perm = rng.permutation(nv)
    src, snk = perm[: nv // 3], perm[nv // 3: 2 * (nv // 3)]
    raw_s, raw_d = rng.uniform(1, 2, len(src)), rng.uniform(1, 2, len(snk))
    raw_d *= raw_s.sum() / raw_d.sum()
    # largest scale theta with a feasible flow, then use 60% of it
    m = gp.Model(); m.Params.OutputFlag = 0
    x = m.addVars(len(arcs), lb=0.0); th = m.addVar(lb=0.0, obj=-1.0)
    for e in range(len(arcs)):
        x[e].UB = U[e]
    bal = {v: gp.LinExpr() for v in range(nv)}
    for e, (i, j) in enumerate(arcs):
        bal[i] += x[e]; bal[j] -= x[e]
    for q, v in enumerate(src):
        m.addConstr(bal[int(v)] == th * raw_s[q])
    for q, v in enumerate(snk):
        m.addConstr(bal[int(v)] == -th * raw_d[q])
    for v in set(range(nv)) - set(map(int, src)) - set(map(int, snk)):
        m.addConstr(bal[v] == 0)
    m.addConstr(th <= 1e4)
    m.optimize()
    if th.X < 1e-6:                      # sources cannot reach the sinks: draw another graph
        return _netflow(nv, deg, seed, cap, cost, rng, gp)
    theta = 0.6 * th.X
    b = np.zeros(nv)
    b[src] = np.round(theta * raw_s, 3)
    b[snk] = -np.round(theta * raw_d, 3)
    b[snk[-1]] = -round(b[src].sum() + b[snk[:-1]].sum(), 3)
    funcs = []
    for e in range(len(arcs)):
        u = float(U[e])
        if cost == "quad":
            bq = rng.uniform(0.5, 1.5) / u
            expr = sp.Float(2 * bq * u + rng.uniform(0.0, 2.0)) * X - sp.Float(bq) * X**2
        elif cost == "log":
            expr = sp.Float(rng.uniform(1, 5)) * sp.log(1 + sp.Float(4.0 / u) * X)
        else:
            expr = sp.Float(rng.uniform(1, 5)) * sp.sqrt(X)
        funcs.append(_concave(expr, 0.0, u))
    A = np.zeros((nv, len(arcs)))
    for e, (i, j) in enumerate(arcs):
        A[i, e], A[j, e] = 1.0, -1.0
    return SeparableProblem(f"netflow-{cap}-{cost}-{nv}n{deg}d-s{seed}", funcs, A, ["=="] * nv, b)


def transport_fc(m, n, seed, cap="uniform", cost="quad", fc=1.0):
    """Transportation with a fixed charge plus a concave variable cost on every arc
    (the structure of Lim, Linderoth and Luedtke 2018).  Fixed charges are U(0.5,1.5)*fc times the
    variable cost of a full arc."""
    base = transport(m, n, seed, cap, cost)
    rng = np.random.default_rng(10_000 + seed)
    N = m * n
    U = np.array([f.hi for f in base.funcs])
    charge = np.array([rng.uniform(0.5, 1.5) * fc * f(f.hi) for f in base.funcs])
    A = np.vstack([base.A, np.eye(N)])                       # x_i - u_i y_i <= 0
    Bm = np.vstack([np.zeros((m + n, N)), -np.diag(U)])
    p = SeparableProblem(base.name.replace("transport", "transportfc"), base.funcs, A,
                         base.sense + ["<="] * N, np.r_[base.b, np.zeros(N)], B=Bm, c_y=charge,
                         y_lb=np.zeros(N), y_ub=np.ones(N), y_type=["B"] * N)
    p.fixed_charge = {i: (i, float(charge[i])) for i in range(N)}
    return p
