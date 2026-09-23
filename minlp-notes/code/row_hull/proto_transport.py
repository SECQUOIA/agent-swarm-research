"""Prototype: root-gap closure of row-hull EF on concave quadratic transportation
with uniform arc capacity U.  f_ij(x) = a_ij x - b_ij x^2 on [0,U]."""
import sys, time
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def gen(m, n, U, seed):
    rng = np.random.default_rng(seed)
    # supplies/demands: non-multiples of U, balanced
    s = rng.uniform(1.2, 3.8, m) * U
    d = rng.uniform(1.2, 3.8, n) * U
    d *= s.sum() / d.sum()
    assert d.max() <= m * U and s.max() <= n * U
    b = rng.uniform(0.5, 1.5, (m, n))
    a = 2 * b * U + rng.uniform(0.0, 2.0, (m, n))  # increasing on [0,U]
    return s, d, a, b


def build(s, d, a, b, U, mode, relax=False):
    """mode: 'obj' (nonconvex objective), 'epi' (epigraph), 'hull' (epigraph+row EF).
    relax=True: replace f by chord (LP)."""
    m, n = a.shape
    M = gp.Model()
    M.Params.OutputFlag = 0
    x = M.addVars(m, n, lb=0, ub=U, name="x")
    for i in range(m):
        M.addConstr(gp.quicksum(x[i, j] for j in range(n)) == s[i])
    for j in range(n):
        M.addConstr(gp.quicksum(x[i, j] for i in range(m)) == d[j])
    f = lambda i, j, v: a[i, j] * v - b[i, j] * v * v
    if mode == "obj" and not relax:
        M.setObjective(gp.quicksum(a[i, j] * x[i, j] - b[i, j] * x[i, j] * x[i, j]
                                   for i in range(m) for j in range(n)))
        return M
    t = M.addVars(m, n, lb=-GRB.INFINITY, name="t")
    M.setObjective(t.sum())
    for i in range(m):
        for j in range(n):
            ch = f(i, j, U) / U
            M.addConstr(t[i, j] >= ch * x[i, j])
            if not relax:
                M.addConstr(t[i, j] >= a[i, j] * x[i, j] - b[i, j] * x[i, j] * x[i, j])
    if mode == "hull":
        def row(idx, B, tag):
            k = np.floor(B / U + 1e-9)
            r = B - k * U
            if r < 1e-7 or U - r < 1e-7:
                return
            z = M.addVars(len(idx), lb=0, name=f"z{tag}")
            M.addConstr(z.sum() == 1)
            for q, (i, j) in enumerate(idx):
                M.addConstr(r * z[q] <= x[i, j])
                M.addConstr((U - r) * z[q] <= U - x[i, j])
                delta = f(i, j, r) - f(i, j, U) / U * r
                M.addConstr(t[i, j] >= f(i, j, U) / U * x[i, j] + delta * z[q])
        for i in range(m):
            row([(i, j) for j in range(n)], s[i], f"s{i}")
        for j in range(n):
            row([(i, j) for i in range(m)], d[j], f"d{j}")
    return M


if __name__ == "__main__":
    m, n = int(sys.argv[1]), int(sys.argv[2])
    TL = float(sys.argv[3]) if len(sys.argv) > 3 else 60
    U = 1.0
    for seed in range(5):
        s, d, a, b = gen(m, n, U, seed)
        lp0 = build(s, d, a, b, U, "epi", relax=True); lp0.optimize()
        lp1 = build(s, d, a, b, U, "hull", relax=True); lp1.optimize()
        out = [f"seed {seed} LPterm {lp0.ObjVal:.4f} LPhull {lp1.ObjVal:.4f}"]
        best = None
        for mode in ["obj", "epi", "hull"]:
            M = build(s, d, a, b, U, mode)
            M.Params.NonConvex = 2; M.Params.TimeLimit = TL; M.Params.Threads = 4
            t0 = time.time(); M.optimize(); el = time.time() - t0
            out.append(f"{mode}: obj {M.ObjVal:.4f} bd {M.ObjBound:.4f} t {el:.1f}s nodes {int(M.NodeCount)}")
            if best is None or M.ObjVal < best: best = M.ObjVal
        clos = (lp1.ObjVal - lp0.ObjVal) / max(best - lp0.ObjVal, 1e-12)
        out.append(f"gap closed {100*clos:.1f}%")
        print(" | ".join(out), flush=True)
