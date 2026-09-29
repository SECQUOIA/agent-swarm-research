"""E3/E4: value functions of convex network flow problems with continuous flows.

E3 (capacity value function): integer capacities x_e on n chosen arcs,
continuous flows y >= 0 with y_e <= x_e, separable convex arc costs, fixed
supply at node 0 and demand at the last node, plus an expensive uncapacitated
bypass arc so that v is finite.  Question: which discrete convexity does
v(x) = min cost have?  (DDM / integrally convex / L-natural up to sign flips /
M-natural).
E4 (supply value function): integer supplies b_i at n source nodes, sink
absorbs the total, continuous flows with real capacities and non-quadratic
convex costs.  Continuous M-natural convexity of b -> v(b) is classical
(network induction); the question is whether the restriction to Z^n is
M-natural.
"""
import sys
import itertools
import numpy as np
import cvxpy as cp
from dcheck import (ddm_violations, ic_violations, lnat_violations,
                    mnat_violations, ninf_false_local_minima, box, INF)

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
SOLVE = dict(solver=cp.CLARABEL, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)


def rand_graph(V, p):
    arcs = [(i, j) for i in range(V) for j in range(V) if i != j and rng.random() < p]
    for i in range(V - 1):  # guarantee a path 0 -> V-1
        if (i, i + 1) not in arcs:
            arcs.append((i, i + 1))
    return arcs


def cost(t, kind):
    a = rng.uniform(0.2, 2.0)
    b = rng.uniform(0.0, 2.0)
    if kind == "quad":
        return a * cp.square(t) + b * t
    c = rng.uniform(0.2, 2.8)
    return b * t + a * cp.pos(t - c) + 0.5 * a * cp.pos(t - c - rng.uniform(0.3, 1.7)) + (0.3 * cp.exp(0.4 * t) if kind == "exp" else 0)


def capacity_instance(n, V, kind):
    arcs = rand_graph(V, 0.35)
    E = len(arcs)
    cap_arcs = list(rng.choice(E, size=min(n, E), replace=False))
    xp = cp.Parameter(len(cap_arcs))
    y = cp.Variable(E, nonneg=True)
    bypass = cp.Variable(nonneg=True)
    D = rng.uniform(1.0, 4.0)
    cons = []
    for v in range(V):
        out_ = sum(y[k] for k, (i, j) in enumerate(arcs) if i == v)
        in_ = sum(y[k] for k, (i, j) in enumerate(arcs) if j == v)
        sup = (D - bypass) if v == 0 else (-(D - bypass) if v == V - 1 else 0)
        cons.append(out_ - in_ == sup)
    for t, k in enumerate(cap_arcs):
        cons.append(y[k] <= xp[t])
    obj = sum(cost(y[k], kind) for k in range(E)) + 20 * bypass
    return cp.Problem(cp.Minimize(obj), cons), xp, arcs, cap_arcs


def supply_instance(n, V, kind):
    arcs = rand_graph(V, 0.4)
    E = len(arcs)
    srcs = list(range(n))
    sink = V - 1
    bp = cp.Parameter(n)
    y = cp.Variable(E, nonneg=True)
    cons = []
    for v in range(V):
        out_ = sum(y[k] for k, (i, j) in enumerate(arcs) if i == v)
        in_ = sum(y[k] for k, (i, j) in enumerate(arcs) if j == v)
        sup = bp[v] if v in srcs else (-sum(bp[i] for i in srcs) if v == sink else 0)
        cons.append(out_ - in_ == sup)
    caps = rng.uniform(1.5, 6.0, size=E)
    cons.append(y <= caps)
    obj = sum(cost(y[k], kind) for k in range(E))
    return cp.Problem(cp.Minimize(obj), cons), bp


def tab(prob, par, pts):
    f = {}
    for p in pts:
        par.value = np.array(p, dtype=float)
        prob.solve(**SOLVE)
        f[p] = prob.value if prob.status in ("optimal", "optimal_inaccurate") else INF
    return f


def lnat_upto_signs(f, n):
    best = None
    for tau in itertools.product((1, -1), repeat=n):
        g = {tuple(t * a for t, a in zip(tau, p)): v for p, v in f.items()}
        k = len(lnat_violations(g))
        if best is None or k < best:
            best = k
    return best


if __name__ == "__main__":
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    for n in (2, 3):
        for kind in ("quad", "pl", "exp"):
            st = dict(inst=0, ddm=0, ic=0, lnat_signs=0, mnat=0, falselocal=0)
            for _ in range(T):
                prob, xp, arcs, cap = capacity_instance(n, int(rng.integers(4, 7)), kind)
                f = tab(prob, xp, box(0, 3, n))
                if sum(v < INF for v in f.values()) < 2:
                    continue
                st["inst"] += 1
                st["ddm"] += bool(ddm_violations(f))
                st["ic"] += bool(ic_violations(f))
                st["lnat_signs"] += bool(lnat_upto_signs(f, n))
                st["mnat"] += bool(mnat_violations(f))
                st["falselocal"] += bool(ninf_false_local_minima(f))
            print(f"E3 capacity n={n} cost={kind:4s}: {st}", flush=True)
    for n in (2, 3):
        for kind in ("quad", "pl", "exp"):
            st = dict(inst=0, mnat=0, ic=0, ddm=0)
            for _ in range(T):
                prob, bp = supply_instance(n, int(rng.integers(n + 2, n + 5)), kind)
                f = tab(prob, bp, box(0, 3, n))
                if sum(v < INF for v in f.values()) < 2:
                    continue
                st["inst"] += 1
                st["mnat"] += bool(mnat_violations(f))
                st["ic"] += bool(ic_violations(f))
                st["ddm"] += bool(ddm_violations(f))
            print(f"E4 supply   n={n} cost={kind:4s}: {st}", flush=True)
