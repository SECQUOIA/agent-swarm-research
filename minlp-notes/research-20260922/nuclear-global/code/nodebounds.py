"""Node bounds for a branch and bound over F1 reload patterns; evaluated at the root, at partial patterns
and at complete patterns (leaves).  All bounds are upper bounds on lam_T valid for every feasible point
consistent with the (partial) pattern; proofs in assessment.md, Section 3.

  B1  Perron monotonicity:     lam_T <= rho(G diag(kh_T))
  B2  node-adaptive peaking CW: lam_T <= min_y max_{p in P} y'Gp / sum_i y_i p_i / kh_i,   P = {V'p = 1, 0 <= p <= c}
      (y by LP bisection; with y = left Perron vector of G diag(kh) it equals B1, so B2 <= B1 up to rounding)
  B3  burn-aware kh from interval equilibrium propagation (iep.py, partial reload), then B1/B2 with that kh
  B4  aggregate-burn relaxation at a complete pattern: keep the eigen rows at t = T and linear burn
      k_T = k_1 - a b,  V'b = T - 1,  0 <= b <= (T-1) c,  k_1 = KF f + R k_T,  drop the eigen rows at t < T;
      solved globally by Gurobi (small nonconvex QCP).
kh = per-node upper bound on k_{i,T}.  Floating point throughout (assessment, not certificates).
usage: nodebounds.py name pattern-json|best  [order: slot order for partial patterns]
"""
import sys, json, numpy as np
import gurobipy as gp
from nucsim import Data, equilibrium
from iep import rho, perron_box, ENV


def b2(D, kh, iters=40):
    N = D.N; lo, hi = 0.0, rho(D.G, kh) * (1 + 1e-9); best = hi
    for _ in range(iters):
        beta = (lo + hi) / 2
        m = gp.Model(env=ENV)
        y = m.addMVar(N, lb=1e-9); mu = m.addVar(lb=-gp.GRB.INFINITY); nu = m.addMVar(N, lb=0)
        m.addConstr(y.sum() == 1)
        m.addConstr(mu + D.c * nu.sum() <= 0)
        GTy = D.G.T @ y
        for j in range(N):
            m.addConstr(D.V[j] * mu + nu[j] - GTy[j] + (beta / kh[j]) * y[j] >= 0)
        m.optimize()
        if m.Status == gp.GRB.OPTIMAL: hi = beta; best = beta
        else: lo = beta
    return best


def a_priori_K1(D, typ_partial):
    """K_1 boxes from ages: assigned type of age A: [KF - A a c (T-1), KF]; unassigned: hull over remaining types."""
    remaining = [g for g in range(D.ntypes) if g not in set(x for x in typ_partial if x is not None)]
    lo = lambda g: D.KF - D.a * D.c * (D.T - 1) * D.age[g]
    K1l = np.array([lo(g) if g is not None else min(lo(h) for h in remaining) for g in typ_partial])
    K1h = np.full(D.N, D.KF)
    fixed = np.array([g is not None and D.fresh[g] for g in typ_partial])
    K1l[fixed] = D.KF
    return K1l, K1h


def iep_partial(D, typ_partial, sweeps=40):
    """IEP with reload applied only where the node's type and its predecessor type are both assigned."""
    T, N = D.T, D.N
    K1l, K1h = a_priori_K1(D, typ_partial)
    where = {}
    for j, g in enumerate(typ_partial):
        if g is not None: where.setdefault(g, []).append(j)
    Kl = [K1l.copy()] + [np.full(N, -np.inf)] * (T - 1); Kh = [K1h.copy()] + [np.full(N, np.inf)] * (T - 1)
    Kl = [x.copy() for x in Kl]; Kh = [x.copy() for x in Kh]
    last = None
    for s in range(sweeps):
        for t in range(T - 1):
            Ll, Lh = rho(D.G, Kl[t]), rho(D.G, Kh[t])
            box = perron_box(D, Kl[t], Kh[t], Ll, Lh)
            if box is None: return None
            pl, ph = box
            Kl[t + 1] = np.maximum(Kl[t + 1], Kl[t] - D.a * ph); Kh[t + 1] = np.minimum(Kh[t + 1], Kh[t] - D.a * pl)
        for i, g in enumerate(typ_partial):
            if g is None or D.fresh[g] or D.pred[g] not in where: continue
            src = where[D.pred[g]]
            Kl[0][i] = max(Kl[0][i], sum(D.V[j] * Kl[T - 1][j] for j in src))
            Kh[0][i] = min(Kh[0][i], sum(D.V[j] * Kh[T - 1][j] for j in src))
        ub = rho(D.G, Kh[T - 1])
        if last is not None and last - ub < 1e-7: break
        last = ub
    return Kl, Kh


def b4(D, typ, tlim=600):
    N, T = D.N, D.T
    f, R = D.reload_matrix(typ)
    m = gp.Model(env=ENV); m.Params.NonConvex = 2; m.Params.TimeLimit = tlim; m.Params.Threads = 2
    lo = D.KF - D.a * D.c * (T - 1) * D.nages
    kT = m.addMVar(N, lb=lo, ub=D.KF); k1 = m.addMVar(N, lb=lo, ub=D.KF); bb = m.addMVar(N, lb=0, ub=(T - 1) * D.c)
    p = m.addMVar(N, lb=0, ub=D.c); lam = m.addVar(lb=0, ub=D.KF * 1.2); s = m.addMVar(N, lb=0)
    m.addConstr(kT == k1 - D.a * bb); m.addConstr(D.V @ bb == T - 1); m.addConstr(k1 == D.KF * f + R @ kT)
    m.addConstr(D.V @ p == 1); m.addConstr(s == D.G @ p)
    for i in range(N): m.addConstr(lam * p[i] == kT[i] * s[i])
    m.setObjective(lam, gp.GRB.MAXIMIZE); m.optimize()
    return m.ObjBound, (m.ObjVal if m.SolCount else None), m.Status


if __name__ == "__main__":
    name = sys.argv[1]; D = Data(name)
    typ = json.load(open("../runs/ls_best.json"))[name]["typ"] if sys.argv[2] == "best" else json.loads(sys.argv[2])
    sim = equilibrium(D, typ)
    print(f"{name}: pattern {typ}, simulated lam_T = {sim['lam_T']:.6f} (feasible {sim['feasible']})")
    slots = [i for i in range(D.N) if i not in {j for _, j in D.ties}]
    partner = {i: j for i, j in D.ties}
    # branching order: fresh slots first, then by age (a natural "ages first" order)
    order = sorted(slots, key=lambda s: (D.age[typ[s]], s))
    rows = []
    for depth in [0, 3, 6, 9, len(slots)]:
        tp = [None] * D.N
        for s in order[:depth]:
            tp[s] = typ[s]
            if s in partner: tp[partner[s]] = typ[s]
        K1l, K1h = a_priori_K1(D, tp)
        kh0 = K1h  # without burn information k_T <= k_1 <= KF
        r = iep_partial(D, tp)
        if r is None:
            rows.append((depth, "IEP proves infeasible")); print(depth, "infeasible"); continue
        Kl, Kh = r
        khT = Kh[D.T - 1]
        out = dict(depth=depth, B1_apriori=rho(D.G, kh0), B1_iep=rho(D.G, khT), B2_iep=b2(D, khT))
        if depth == len(slots):
            out["B4_bound"], out["B4_val"], out["B4_status"] = b4(D, typ)
        rows.append(out); print(out, flush=True)
    json.dump(dict(name=name, typ=typ, sim=sim["lam_T"], rows=rows), open(f"../runs/bounds_{name}.json", "w"), default=float)
