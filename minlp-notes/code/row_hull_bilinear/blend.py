"""Pilot: multi-product blending with variable source qualities.
  sources i (quality y_i in [0,1], unit price a_i + b_i y_i, capacity C_i), products j (demand B_j exactly,
  minimum quality q_j), arcs x_ij in [0,w].   Bilinear terms t_ij = x_ij y_i.
  min sum_ij (a_i x_ij + b_i t_ij)  s.t.  sum_i x_ij = B_j,  sum_j x_ij <= C_i,  sum_i t_ij >= q_j B_j.
Forms: 'mc' (Gurobi on the plain model), 'ef' (plus the state extended form of every demand row),
'rlt' (plus row x y_k products for every demand row)."""
import sys, time, json
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def gen(m, n, seed):
    rng = np.random.default_rng(seed)
    w = 1.0
    B = np.round(rng.uniform(1.2, min(m - 1, 3.8), n), 3)
    C = np.round(rng.uniform(0.6, 1.0, m) * B.sum() / m * 1.6, 3)
    a = rng.uniform(1, 3, m); b = rng.uniform(2, 6, m)
    q = rng.uniform(0.35, 0.75, n)
    return w, B, C, a, b, q


def build(m, n, seed, form, relax=False):
    w, B, C, a, b, q = gen(m, n, seed)
    M = gp.Model(); M.Params.OutputFlag = 0
    x = M.addVars(m, n, lb=0, ub=w); y = M.addVars(m, lb=0, ub=1); t = M.addVars(m, n, lb=0, ub=w)
    M.addConstrs(x.sum('*', j) == B[j] for j in range(n))
    M.addConstrs(x.sum(i, '*') <= C[i] for i in range(m))
    M.addConstrs(t.sum('*', j) >= q[j] * B[j] for j in range(n))
    for i in range(m):
        for j in range(n):
            if relax:
                M.addConstr(t[i, j] <= x[i, j]); M.addConstr(t[i, j] <= w * y[i]); M.addConstr(t[i, j] >= x[i, j] + w * y[i] - w)
            else:
                M.addConstr(t[i, j] == x[i, j] * y[i])
    if form == "ef":
        for j in range(n):
            k = np.floor(B[j] / w + 1e-9); r = B[j] - k * w
            if r < 1e-6 or w - r < 1e-6: continue
            s = M.addVars(m, 6, lb=0)
            for i in range(m):
                M.addConstr(gp.quicksum(s[i, c] for c in range(6)) == 1)
                M.addConstr(x[i, j] == w * (s[i, 2] + s[i, 3]) + r * (s[i, 4] + s[i, 5]))
                M.addConstr(y[i] == s[i, 1] + s[i, 3] + s[i, 5])
                M.addConstr(t[i, j] == w * s[i, 3] + r * s[i, 5])
            M.addConstr(gp.quicksum(s[i, 2] + s[i, 3] for i in range(m)) == k)
            M.addConstr(gp.quicksum(s[i, 4] + s[i, 5] for i in range(m)) == 1)
    if form == "rlt":
        for j in range(n):
            p = M.addVars(m, m, lb=0, ub=w)            # p[i,k] ~ x_ij y_k
            for i in range(m):
                M.addConstr(p[i, i] == t[i, j])
                for k in range(m):
                    M.addConstr(p[i, k] <= x[i, j]); M.addConstr(p[i, k] <= w * y[k]); M.addConstr(p[i, k] >= x[i, j] + w * y[k] - w)
            for k in range(m):
                M.addConstr(gp.quicksum(p[i, k] for i in range(m)) == B[j] * y[k])
    M.setObjective(gp.quicksum(a[i] * x[i, j] + b[i] * t[i, j] for i in range(m) for j in range(n)))
    return M


if __name__ == "__main__":
    m, n, seeds, TL = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
    for seed in range(seeds):
        lps = {}
        for form in ("mc", "rlt", "ef"):
            M = build(m, n, seed, form, relax=True); M.optimize(); lps[form] = M.ObjVal if M.Status == 2 else None
        out = []
        best = None
        for form in ("mc", "ef"):
            M = build(m, n, seed, form); M.Params.NonConvex = 2; M.Params.TimeLimit = TL; M.Params.Threads = 4; M.Params.MIPGap = 1e-4
            t0 = time.time(); M.optimize(); el = time.time() - t0
            if M.SolCount: best = M.ObjVal if best is None else min(best, M.ObjVal)
            out.append(f"{form}: {M.Status} obj {M.ObjVal if M.SolCount else float('nan'):.4f} bd {M.ObjBound:.4f} nodes {int(M.NodeCount)} {el:.1f}s")
        clos = lambda v: 100 * (v - lps['mc']) / max(best - lps['mc'], 1e-9)
        print(f"{m}x{n} s{seed}: LP mc {lps['mc']:.4f} rlt {lps['rlt']:.4f} ({clos(lps['rlt']):.0f}%) ef {lps['ef']:.4f} ({clos(lps['ef']):.0f}%) | " + " | ".join(out), flush=True)
