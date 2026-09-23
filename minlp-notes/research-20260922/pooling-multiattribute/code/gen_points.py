"""Feasible points of the original MINLPLib pq model (OSiL order), for validity tests of the added relaxation rows.

Sources: MINLPLib .sol files; alternating LP local search (fix q -> LP in (y,w,z); fix y -> LP in (q,w,z)) from
random simplex starts, with the true objective or a random objective. With q (or y) fixed, w = q*y is linear, so
every LP solution is feasible for the original model up to LP tolerances (reported)."""
import sys, json
import numpy as np
import gurobipy as gp
import indep_bound as B

ENV = gp.Env(params={"OutputFlag": 0})


def read_sol(path, names):
    idx = {n: i for i, n in enumerate(names)}; z = np.zeros(len(names))
    for line in open(path):
        a = line.split()
        if len(a) == 2 and a[0] in idx: z[idx[a[0]]] = float(a[1])
    return z


def lp_step(S, fixed, vals, obj):
    """fixed='q': q = vals[q], LP in y,w,z. fixed='y': y = vals[y], LP in q,w,z."""
    m = gp.Model(env=ENV); m.Params.FeasibilityTol = 1e-9; m.Params.OptimalityTol = 1e-9
    x = m.addMVar(S.n, lb=0, ub=[float(u) for u in S.ub], obj=obj)
    for (row, lb, ub, r) in S.lin:
        e = gp.quicksum(float(a) * x[j] for j, a in row.items())
        if ub is not None: m.addConstr(e <= float(ub))
        if lb is not None: m.addConstr(e >= float(lb))
    for w, (q, y) in S.W.items():
        if fixed == "q": m.addConstr(x[w] == vals[q] * x[y])
        else: m.addConstr(x[w] == vals[y] * x[q])
    idx = [q for q, y in S.W.values()] if fixed == "q" else [y for q, y in S.W.values()]
    for j in set(idx): x[j].LB = x[j].UB = vals[j]
    m.optimize()
    assert m.Status == 2, m.Status
    z = x.X.copy()
    return z


def maxviol(S, z):
    v = 0.0
    for (row, lb, ub, r) in S.lin:
        a = sum(float(c) * z[j] for j, c in row.items())
        if ub is not None: v = max(v, a - float(ub))
        if lb is not None: v = max(v, float(lb) - a)
    for w, (q, y) in S.W.items(): v = max(v, abs(z[w] - z[q] * z[y]))
    v = max(v, float(np.max(-z)), max(z[j] - float(S.ub[j]) for j in range(S.n)))
    return v


if __name__ == "__main__":
    osil, out, nstart = sys.argv[1], sys.argv[2], int(sys.argv[3]); sols = sys.argv[4:]
    S = B.Struct(osil); rng = np.random.default_rng(1)
    c = np.array([float(S.c.get(j, 0)) for j in range(S.n)])
    pts, tags = [], []
    for s in sols:
        z = read_sol(s, S.M.vnames); pts.append(z); tags.append(s.split("/")[-1])
    for st in range(nstart):
        vals = np.zeros(S.n)
        for pool in S.pools:
            vals[pool] = rng.dirichlet(np.full(len(pool), rng.choice([0.2, 1.0, 5.0])))
        obj = c if st % 2 == 0 else c * rng.uniform(0, 2, S.n) - rng.uniform(0, 5, S.n) * (c != 0)
        fixed = "q"
        for it in range(6):
            z = lp_step(S, fixed, vals, obj); pts.append(z); tags.append(f"s{st}_it{it}_{fixed}")
            vals = z; fixed = "y" if fixed == "q" else "q"
    # local search from the MINLPLib points (true objective)
    for s, z0 in zip(sols, list(pts[:len(sols)])):
        vals, fixed = z0, "y"
        for it in range(4):
            z = lp_step(S, fixed, vals, c); pts.append(z); tags.append(f"{s.split('/')[-1]}_ls{it}_{fixed}")
            vals = z; fixed = "y" if fixed == "q" else "q"
    P = np.array(pts)
    objs = P @ c; viol = [maxviol(S, z) for z in P]
    np.savez(out, P=P, tags=np.array(tags), obj=objs, viol=np.array(viol))
    print(json.dumps(dict(n=len(P), best=float(objs.min()), worst_viol=float(max(viol)),
                          objs=sorted(float(o) for o in objs)[:5])))
