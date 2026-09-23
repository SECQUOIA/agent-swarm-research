"""Pilot: standard pooling (p-formulation) with exact product demands and uniform pool-to-product arc
capacity w.  S sources (contaminant lam_s, cost c_s: cleaner is dearer), I pools, J products
(demand B_j, contaminant limit Q_j).  f_si source->pool, x_ij pool->product, y_i pool quality,
t_ij = x_ij y_i.
   sum_s f_si = sum_j x_ij,  sum_s lam_s f_si = sum_j t_ij,  sum_i x_ij = B_j,  sum_i t_ij <= Q_j B_j.
Forms: mc | ef (state extended form of every product row) | pq (adds the classical pq/RLT rows)."""
import sys, time
import numpy as np
import gurobipy as gp


def gen(S, I, J, seed):
    rng = np.random.default_rng(seed)
    lam = np.sort(rng.uniform(0, 1, S)); lam[0], lam[-1] = 0.0, 1.0
    c = 10 - 8 * lam + rng.uniform(-0.5, 0.5, S)               # clean sources cost more
    B = np.round(rng.uniform(1.2, min(I - 1, 3.8) , J), 3)
    Q = np.round(rng.uniform(0.25, 0.75, J), 3)
    return lam, c, B, Q


def build(S, I, J, seed, form, relax=False, w=1.0):
    lam, c, B, Q = gen(S, I, J, seed)
    M = gp.Model(); M.Params.OutputFlag = 0
    f = M.addVars(S, I, lb=0, ub=J * w); x = M.addVars(I, J, lb=0, ub=w); y = M.addVars(I, lb=0, ub=1); t = M.addVars(I, J, lb=0, ub=w)
    for i in range(I):
        M.addConstr(f.sum('*', i) == x.sum(i, '*'))
        M.addConstr(gp.quicksum(lam[s] * f[s, i] for s in range(S)) == t.sum(i, '*'))
    for j in range(J):
        M.addConstr(x.sum('*', j) == B[j]); M.addConstr(t.sum('*', j) <= Q[j] * B[j])
    for i in range(I):
        for j in range(J):
            if relax:
                M.addConstr(t[i, j] <= x[i, j]); M.addConstr(t[i, j] <= w * y[i]); M.addConstr(t[i, j] >= x[i, j] + w * y[i] - w)
            else:
                M.addConstr(t[i, j] == x[i, j] * y[i])
    if form in ("pq", "efpq"):          # proportions q_si with f_si = q_si * throughput; RLT rows of sum_s q_si = 1
        q = M.addVars(S, I, lb=0, ub=1); v = M.addVars(S, I, J, lb=0, ub=w)     # v_sij ~ q_si x_ij
        for i in range(I):
            M.addConstr(q.sum('*', i) == 1)
            M.addConstr(y[i] == gp.quicksum(lam[s] * q[s, i] for s in range(S)))
            for j in range(J):
                M.addConstr(gp.quicksum(v[s, i, j] for s in range(S)) == x[i, j])
                M.addConstr(gp.quicksum(lam[s] * v[s, i, j] for s in range(S)) == t[i, j])
            for s in range(S):
                M.addConstr(gp.quicksum(v[s, i, j] for j in range(J)) == f[s, i])
                for j in range(J):
                    if relax:
                        M.addConstr(v[s, i, j] <= w * q[s, i]); M.addConstr(v[s, i, j] <= x[i, j]); M.addConstr(v[s, i, j] >= x[i, j] + w * q[s, i] - w)
                    else:
                        M.addConstr(v[s, i, j] == q[s, i] * x[i, j])
    if form in ("ef", "efpq"):
        for j in range(J):
            k = np.floor(B[j] / w + 1e-9); r = B[j] - k * w
            if r < 1e-6 or w - r < 1e-6: continue
            st = M.addVars(I, 6, lb=0)
            for i in range(I):
                M.addConstr(gp.quicksum(st[i, a] for a in range(6)) == 1)
                M.addConstr(x[i, j] == w * (st[i, 2] + st[i, 3]) + r * (st[i, 4] + st[i, 5]))
                M.addConstr(y[i] == st[i, 1] + st[i, 3] + st[i, 5])
                M.addConstr(t[i, j] == w * st[i, 3] + r * st[i, 5])
            M.addConstr(gp.quicksum(st[i, 2] + st[i, 3] for i in range(I)) == k)
            M.addConstr(gp.quicksum(st[i, 4] + st[i, 5] for i in range(I)) == 1)
    M.setObjective(gp.quicksum(c[s] * f[s, i] for s in range(S) for i in range(I)))
    return M


if __name__ == "__main__":
    S, I, J, seeds, TL = (int(a) for a in sys.argv[1:5]) + (float(sys.argv[5]),) if False else (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]))
    for seed in range(seeds):
        lps = {}
        for form in ("mc", "ef", "pq", "efpq"):
            M = build(S, I, J, seed, form, relax=True); M.optimize(); lps[form] = M.ObjVal if M.Status == 2 else float("nan")
        res = {}
        for form in ("mc", "ef", "pq", "efpq"):
            M = build(S, I, J, seed, form); M.Params.NonConvex = 2; M.Params.TimeLimit = TL; M.Params.Threads = 4; M.Params.MIPGap = 1e-4
            t0 = time.time(); M.optimize(); res[form] = (M.Status, M.ObjVal if M.SolCount else float("nan"), M.ObjBound, int(M.NodeCount), time.time() - t0)
        best = np.nanmin([v[1] for v in res.values()])
        gap = lambda v: 100 * (best - v) / abs(best)
        print(f"{S}-{I}-{J} s{seed}: root gap% mc {gap(lps['mc']):.2f} ef {gap(lps['ef']):.2f} pq {gap(lps['pq']):.2f} ef+pq {gap(lps['efpq']):.2f} | " +
              " | ".join(f"{k}: st{v[0]} {v[1]:.3f} nodes {v[3]} {v[4]:.1f}s" for k, v in res.items()), flush=True)
