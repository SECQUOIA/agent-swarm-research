"""Prototype: exact row hulls by brute-force vertex enumeration (small rows), general widths.
Concave transportation: uncapacitated (u_ij=min(s_i,d_j)) or random capacities; cost c*x^p or concave quadratic."""
import sys, itertools, time
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def row_vertices(w, B, tol=1e-9):
    """Vertices (as points) of {sum x = B, 0<=x<=w}."""
    n = len(w); out = set()
    for mask in range(1 << n):
        S = [i for i in range(n) if mask >> i & 1]
        tot = sum(w[i] for i in S)
        for j in range(n):
            if mask >> j & 1: continue
            r = B - tot
            if -tol <= r <= w[j] + tol:
                v = [w[i] if mask >> i & 1 else 0.0 for i in range(n)]
                v[j] = min(max(r, 0.0), w[j])
                out.add(tuple(round(a, 9) for a in v))
    return [np.array(v) for v in out]


def run(m, n, seed, kind, TL):
    rng = np.random.default_rng(seed)
    s = rng.uniform(5, 15, m); d = rng.uniform(5, 15, n); d *= s.sum() / d.sum()
    if kind == "uncap":
        U = np.minimum.outer(s, d)
    else:
        U = rng.uniform(2, 8, (m, n))
        assert (U.sum(1) >= s).all() and (U.sum(0) >= d).all()
    c = rng.uniform(1, 5, (m, n)); p = 0.5
    f = lambda i, j, v: c[i, j] * np.sqrt(np.maximum(v, 0))
    def base():
        M = gp.Model(); M.Params.OutputFlag = 0
        x = M.addVars(m, n, lb=0, name="x")
        for i in range(m):
            for j in range(n): x[i, j].UB = U[i, j]
        t = M.addVars(m, n, lb=0, name="t")
        M.addConstrs(x.sum(i, '*') == s[i] for i in range(m))
        M.addConstrs(x.sum('*', j) == d[j] for j in range(n))
        M.addConstrs(t[i, j] >= f(i, j, U[i, j]) / U[i, j] * x[i, j] for i in range(m) for j in range(n))
        M.setObjective(t.sum()); return M, x, t
    M0, _, _ = base(); M0.optimize()
    M1, x, t = base()
    def addrow(idx, B):
        w = [U[i, j] for i, j in idx]
        V = row_vertices(w, B)
        lam = M1.addVars(len(V), lb=0)
        M1.addConstr(lam.sum() == 1)
        for q, (i, j) in enumerate(idx):
            M1.addConstr(gp.quicksum(lam[k] * V[k][q] for k in range(len(V))) == x[i, j])
            M1.addConstr(gp.quicksum(lam[k] * f(i, j, V[k][q]) for k in range(len(V))) <= t[i, j])
    for i in range(m): addrow([(i, j) for j in range(n)], s[i])
    for j in range(n): addrow([(i, j) for i in range(m)], d[j])
    M1.optimize()
    # exact via Gurobi NL
    M2 = gp.Model(); M2.Params.OutputFlag = 0; M2.Params.TimeLimit = TL; M2.Params.Threads = 4
    x2 = M2.addVars(m, n, lb=0); t2 = M2.addVars(m, n, lb=0)
    for i in range(m):
        for j in range(n):
            x2[i, j].UB = U[i, j]
            M2.addGenConstrPow(x2[i, j], t2[i, j], 0.5)
    M2.addConstrs(x2.sum(i, '*') == s[i] for i in range(m))
    M2.addConstrs(x2.sum('*', j) == d[j] for j in range(n))
    M2.setObjective(gp.quicksum(c[i, j] * t2[i, j] for i in range(m) for j in range(n)))
    M2.Params.FuncNonlinear = 1
    t0 = time.time(); M2.optimize(); el = time.time() - t0
    clos = (M1.ObjVal - M0.ObjVal) / max(M2.ObjVal - M0.ObjVal, 1e-12)
    print(f"{kind} {m}x{n} seed {seed}: term {M0.ObjVal:.4f} rowhull {M1.ObjVal:.4f} best {M2.ObjVal:.4f} bd {M2.ObjBound:.4f} ({el:.1f}s, {int(M2.NodeCount)} nodes) closed {100*clos:.1f}%", flush=True)


if __name__ == "__main__":
    m, n, kind = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    for seed in range(4):
        run(m, n, seed, kind, 60)
