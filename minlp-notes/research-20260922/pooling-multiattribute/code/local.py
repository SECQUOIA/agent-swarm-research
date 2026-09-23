"""Local test: is conv(T^K) equal to the intersection of per-attribute hulls?

T^K(P, B) = {(x, z, u, y, t): x, z >= 0, x + z <= 1, t in P, u = x t,
             y in z B, u + y <= 0}
with P = conv(G) (pool excess vectors), B = conv(Bv) (bypass excess vectors).

Compared relaxations (support function h(c) = max c.p):
  h0 : McCormick/pq-type polytope R0 = {u in xP, t-u in (1-x)P, y in zB, ...}
  hR : R0 intersected with the per-attribute hulls conv T^1_k (Luedtke sets
       with interval data proj_k P, proj_k B), inner-approximated by a fine
       grid in t_k (grid points are feasible, so hR_grid <= hR).
  hK : exact max over T^K by Gurobi (spatial B&B).
If hR_grid > hK + tol, the intersection is strictly larger than conv(T^K).
"""
import itertools, sys, json
import numpy as np
import gurobipy as gp
from gurobipy import GRB

ENV = gp.Env(params={"OutputFlag": 0})


def fiber_vertices_1d(t, bl, bu):
    """Vertices of {(x,z,y): x,z>=0, x+z<=1, bl z <= y <= bu z, x t + y <= 0}."""
    # constraints a.v <= b over v=(x,z,y)
    A = np.array([[-1, 0, 0], [0, -1, 0], [1, 1, 0], [0, bl, -1], [0, -bu, 1], [t, 0, 1]], float)
    b = np.array([0, 0, 1, 0, 0, 0], float)
    out = []
    for S in itertools.combinations(range(6), 3):
        M = A[list(S)]
        if abs(np.linalg.det(M)) < 1e-12:
            continue
        v = np.linalg.solve(M, b[list(S)])
        if np.all(A @ v <= b + 1e-9):
            out.append(v)
    return out


def cloud_1d(a, b, bl, bu, n):
    pts = []
    for t in np.linspace(a, b, n):
        for x, z, y in fiber_vertices_1d(t, bl, bu):
            pts.append((x, z, x * t, y, t))
    return np.unique(np.round(np.array(pts), 12), axis=0)


def add_R0(m, G, Bv):
    K = G.shape[1]
    x = m.addVar(lb=0, ub=1); z = m.addVar(lb=0, ub=1)
    u = m.addVars(K, lb=-GRB.INFINITY); y = m.addVars(K, lb=-GRB.INFINITY); t = m.addVars(K, lb=-GRB.INFINITY)
    w = m.addVars(len(G), lb=0); r = m.addVars(len(G), lb=0); v = m.addVars(len(Bv), lb=0)
    m.addConstr(x + z <= 1)
    m.addConstr(w.sum() == x); m.addConstr(r.sum() == 1 - x); m.addConstr(v.sum() == z)
    for k in range(K):
        m.addConstr(u[k] == gp.quicksum(G[i, k] * w[i] for i in range(len(G))))
        m.addConstr(t[k] - u[k] == gp.quicksum(G[i, k] * r[i] for i in range(len(G))))
        m.addConstr(y[k] == gp.quicksum(Bv[b, k] * v[b] for b in range(len(Bv))))
        m.addConstr(u[k] + y[k] <= 0)
    return x, z, u, y, t


def obj(c, x, z, u, y, t, K):
    return c[0] * x + c[1] * z + gp.quicksum(c[2 + k] * u[k] + c[2 + K + k] * y[k] + c[2 + 2 * K + k] * t[k] for k in range(K))


def h0(c, G, Bv):
    m = gp.Model(env=ENV); K = G.shape[1]
    x, z, u, y, t = add_R0(m, G, Bv)
    m.setObjective(obj(c, x, z, u, y, t, K), GRB.MAXIMIZE); m.optimize()
    return m.ObjVal


def hR(c, G, Bv, clouds):
    m = gp.Model(env=ENV); K = G.shape[1]
    x, z, u, y, t = add_R0(m, G, Bv)
    for k in range(K):
        C = clouds[k]
        lam = m.addMVar(len(C), lb=0)
        m.addConstr(lam.sum() == 1)
        for col, var in enumerate([x, z, u[k], y[k], t[k]]):
            m.addConstr(C[:, col] @ lam == var)
    m.setObjective(obj(c, x, z, u, y, t, K), GRB.MAXIMIZE); m.optimize()
    return m.ObjVal


def hK(c, G, Bv):
    m = gp.Model(env=ENV); K = G.shape[1]
    m.Params.NonConvex = 2; m.Params.MIPGap = 1e-9; m.Params.MIPGapAbs = 1e-9
    x = m.addVar(lb=0, ub=1); z = m.addVar(lb=0, ub=1)
    q = m.addVars(len(G), lb=0); v = m.addVars(len(Bv), lb=0)
    t = m.addVars(K, lb=-GRB.INFINITY); u = m.addVars(K, lb=-GRB.INFINITY); y = m.addVars(K, lb=-GRB.INFINITY)
    m.addConstr(q.sum() == 1); m.addConstr(v.sum() == z); m.addConstr(x + z <= 1)
    for k in range(K):
        m.addConstr(t[k] == gp.quicksum(G[i, k] * q[i] for i in range(len(G))))
        m.addConstr(y[k] == gp.quicksum(Bv[b, k] * v[b] for b in range(len(Bv))))
        m.addConstr(u[k] == x * t[k])
        m.addConstr(u[k] + y[k] <= 0)
    m.setObjective(obj(c, x, z, u, y, t, K), GRB.MAXIMIZE); m.optimize()
    return m.ObjBound, m.ObjVal


def run_case(G, Bv, ndir=60, ngrid=801, seed=0):
    rng = np.random.default_rng(seed)
    K = G.shape[1]
    clouds = [cloud_1d(G[:, k].min(), G[:, k].max(), Bv[:, k].min(), Bv[:, k].max(), ngrid) for k in range(K)]
    rows = []
    for _ in range(ndir):
        c = rng.normal(size=2 + 3 * K)
        a0 = h0(c, G, Bv); aR = hR(c, G, Bv, clouds); bK, vK = hK(c, G, Bv)
        rows.append((a0, aR, bK, vK))
    return np.array(rows)


def summarize(rows, tol=1e-6):
    a0, aR, bK, vK = rows.T
    gap0 = a0 - bK
    rem = aR - bK
    sig = gap0 > 1e-6
    strict = rem > tol
    frac = np.where(sig, np.maximum(rem, 0) / np.maximum(gap0, 1e-12), 0)
    return dict(n=len(rows), n_mc_gap=int(sig.sum()), n_strict=int(strict.sum()),
                max_remaining_frac=float(frac.max()), mean_remaining_frac_over_gap=float(frac[sig].mean()) if sig.any() else 0.0,
                max_abs_remaining=float(rem.max()))


if __name__ == "__main__":
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    out = []
    for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 6):
        K = 2
        kind = ["box", "segment", "random"][trial % 3]
        if kind == "box":  # independent intervals: P, B boxes
            a = rng.uniform(-2, 0.5, K); b = a + rng.uniform(0.5, 3, K)
            G = np.array(list(itertools.product(*[(a[k], b[k]) for k in range(K)])))
            bl = rng.uniform(-3, 0.5, K); bu = bl + rng.uniform(0.2, 3, K)
            Bv = np.array(list(itertools.product(*[(bl[k], bu[k]) for k in range(K)])))
        elif kind == "segment":  # two-sided spec of one physical quality: t2 = d - t1
            a = rng.uniform(-2, 0.3); b = a + rng.uniform(0.5, 3); d = -rng.uniform(0.2, 2)
            G = np.array([[a, d - a], [b, d - b]])
            bl = rng.uniform(-3, 0.3); bu = bl + rng.uniform(0.3, 3)
            Bv = np.array([[bl, d - bl], [bu, d - bu]])
        else:  # few inputs with random quality vectors
            G = rng.uniform(-2, 1.5, (3, K)); Bv = rng.uniform(-2.5, 1, (2, K))
        rows = run_case(G, Bv, seed=trial)
        s = summarize(rows); s.update(kind=kind, G=G.round(3).tolist(), B=Bv.round(3).tolist())
        print(json.dumps(s)); sys.stdout.flush(); out.append(s)
