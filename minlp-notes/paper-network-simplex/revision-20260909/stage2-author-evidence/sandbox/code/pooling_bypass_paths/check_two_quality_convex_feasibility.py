"""Original arbitrary-topology pooling versus the one-convex-QP algorithm.

All optimization calls here are numerical Gurobi solves. The proof, not
this checker, supplies exact rational complexity and boundary guarantees.
"""
from fractions import Fraction as F
from random import Random

import gurobipy as gp
from gurobipy import GRB

ENV = gp.Env(empty=True)
ENV.setParam('OutputFlag', 0)
ENV.start()


def model():
    m = gp.Model(env=ENV)
    m.Params.OutputFlag = 0
    m.Params.FeasibilityTol = 1e-9
    m.Params.OptimalityTol = 1e-9
    m.Params.DualReductions = 0
    return m


def original(data, fixed_q=None, outlet_lower=None, pool_cap=None):
    C, a, b, B, bounds, feeds, outlets = data
    m = model()
    m.Params.NonConvex = 2
    m.Params.TimeLimit = 30
    z = {e: m.addVar(lb=float(lo), ub=float(hi)) for e, (lo, hi) in bounds.items()}
    y = {i: m.addVar(lb=float(lo), ub=float(hi)) for i, (lo, hi) in feeds.items()}
    v = {j: m.addVar(lb=float((outlet_lower or {}).get(j, 0)), ub=float(cap))
         for j, cap in outlets.items()}
    q = m.addVar(lb=0, ub=1) if fixed_q is None else float(fixed_q)
    for i in range(len(C)):
        alo, ahi = a[i] if isinstance(a[i], tuple) else (a[i], a[i])
        actual = y.get(i, 0)+gp.quicksum(zz for (ii, j), zz in z.items() if ii == i)
        m.addConstr(actual >= float(alo))
        m.addConstr(actual <= float(ahi))
    for j in range(len(b)):
        m.addConstr(v.get(j, 0)+gp.quicksum(zz for (i, jj), zz in z.items() if jj == j) == float(b[j]))
        m.addConstr(q*v.get(j, 0)+gp.quicksum(C[i]*zz for (i, jj), zz in z.items() if jj == j) == float(b[j]*B[j]))
    m.addConstr(gp.quicksum(y.values()) == gp.quicksum(v.values()))
    m.addConstr(gp.quicksum(C[i]*yy for i, yy in y.items()) == q*gp.quicksum(v.values()))
    if pool_cap is not None:
        m.addConstr(gp.quicksum(v.values()) <= float(pool_cap))
    m.optimize()
    assert m.Status in (GRB.OPTIMAL, GRB.INFEASIBLE), m.Status
    answer = m.Status == GRB.OPTIMAL
    m.dispose()
    return answer


def convex(data, pool_cap=None):
    C, a, b, B, bounds, feeds, outlets = data
    if original(data, F(0), pool_cap=pool_cap) or original(data, F(1), pool_cap=pool_cap):
        return True, 'endpoint'
    m = model()
    q, r = m.addVar(lb=0, ub=1), m.addVar(lb=0, ub=1)
    w = {e: m.addVar(lb=-float(hi), ub=float(hi)) for e, (lo, hi) in bounds.items()}
    for (i, j), ww in w.items():
        lo, hi = bounds[i, j]
        gamma = C[i]-q
        m.addConstr(ww >= float(lo if C[i] else hi)*gamma)
        m.addConstr(ww <= float(hi if C[i] else lo)*gamma)
    t, h = {}, {}
    for i in range(len(C)):
        alo, ahi = a[i] if isinstance(a[i], tuple) else (a[i], a[i])
        flo, fhi = feeds.get(i, (F(0), F(0)))
        t[i] = m.addVar(lb=-float(ahi), ub=float(ahi))
        h[i] = m.addVar(lb=-float(fhi), ub=float(fhi))
        gamma = C[i]-q
        m.addConstr(t[i] >= float(alo if C[i] else ahi)*gamma)
        m.addConstr(t[i] <= float(ahi if C[i] else alo)*gamma)
        m.addConstr(h[i] >= float(flo if C[i] else fhi)*gamma)
        m.addConstr(h[i] <= float(fhi if C[i] else flo)*gamma)
        m.addConstr(t[i] == h[i]+gp.quicksum(ww for (ii, j), ww in w.items() if ii == i))
    total_high = sum(bj*Bj for bj, Bj in zip(b, B))
    total_low = sum(b)-total_high
    m.addConstr(gp.quicksum(t[i] for i in t if C[i] == 0) == -float(total_low)*q)
    m.addConstr(gp.quicksum(t[i] for i in t if C[i] == 1) == float(total_high)*(1-q))
    for j in range(len(b)):
        low = gp.quicksum(ww for (i, jj), ww in w.items() if jj == j and C[i] == 0)
        total = gp.quicksum(ww for (i, jj), ww in w.items() if jj == j)
        m.addConstr(total == float(b[j]*B[j])-float(b[j])*q)
        affine = float(b[j]*(B[j]-1))*q
        m.addConstr(low >= affine)
        m.addConstr(low <= affine+float(outlets.get(j, 0))*(q-r))
    if pool_cap is not None:
        low_total = gp.quicksum(ww for (i, j), ww in w.items() if C[i] == 0)
        m.addConstr(low_total <= float(sum(bj*(Bj-1) for bj, Bj in zip(b, B)))*q+float(pool_cap)*(q-r))
    margin = m.addVar(lb=0, ub=.5)
    m.addConstr(margin <= q)
    m.addConstr(margin <= 1-q)
    m.setObjective(margin, GRB.MAXIMIZE)
    m.optimize()
    if m.Status == GRB.INFEASIBLE or margin.X < 1e-8:
        m.dispose()
        return False, 'no-interior-polytope'
    p = (q.X, r.X)
    m.setObjective(q*q-r, GRB.MINIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    value, quality = m.ObjVal, q.X
    if value < -1e-7:
        answer, branch = True, 'negative-QP'
        rho = -value
        lam = rho/(2*(rho+1))
        mixed_q, mixed_r = (1-lam)*q.X+lam*p[0], (1-lam)*r.X+lam*p[1]
        assert 0 < mixed_q < 1 and mixed_q*mixed_q-mixed_r < 0
    elif value > 1e-7:
        answer, branch = False, 'positive-QP'
    else:
        answer, branch = 1e-7 < quality < 1-1e-7, 'zero-QP'
    m.dispose()
    return answer, branch


def cases():
    rng = Random(710305)
    for case in range(32):
        n, m = 4+case % 4, 3+case % 3
        C = [i % 2 for i in range(n)]
        edges = [(i, j) for i in range(n) for j in range(m)
                 if case % 2 == 0 or rng.random() > .3]
        known_z = {e: F(rng.randrange(1, 5), 4) for e in edges}
        y = [F(rng.randrange(1, 4), 4) for _ in range(n)]
        if case % 8 == 1:
            y = [yi if C[i] == 0 else F(0) for i, yi in enumerate(y)]
        if case % 8 == 2:
            y = [yi if C[i] == 1 else F(0) for i, yi in enumerate(y)]
        T = sum(y)
        q = sum(ci*yi for ci, yi in zip(C, y))/T
        v = [T/m]*m
        a = [y[i]+sum(zz for (ii, j), zz in known_z.items() if ii == i) for i in range(n)]
        b = [v[j]+sum(zz for (i, jj), zz in known_z.items() if jj == j) for j in range(m)]
        B = [(q*v[j]+sum(C[i]*zz for (i, jj), zz in known_z.items() if jj == j))/b[j] for j in range(m)]
        bounds = {e: (max(F(0), zz-F(1, 8)), zz+F(1, 8)) for e, zz in known_z.items()}
        feeds = {i: (yi/2, yi+F(1, 8)) for i, yi in enumerate(y)}
        outlets = {j: vv+F(1, 8) for j, vv in enumerate(v)}
        net = C, a, b, B, bounds, feeds, outlets
        yield net, None
        yield net, max(F(0), T-F(1, 2))
        intervals = [(ai/2, ai+F(1, 4)) for ai in a]
        interval_net = C, intervals, b, B, bounds, feeds, outlets
        yield interval_net, None
        yield interval_net, max(F(0), T-F(1, 2))
        altered = dict(outlets)
        altered[case % m] = max(F(0), v[case % m]-F(1, 2))
        yield (C, a, b, B, bounds, feeds, altered), None


def main():
    from collections import Counter
    counts = Counter()
    for data, pool_cap in cases():
        actual = original(data, pool_cap=pool_cap)
        predicted, branch = convex(data, pool_cap=pool_cap)
        assert actual == predicted, (actual, predicted, branch)
        counts[branch] += 1
        counts['feasible'] += actual
    # Positive outlet lower bounds cannot simply be dropped.
    control = ([0, 1], [F(1), F(1)], [F(1), F(1)], [F(1), F(0)],
               {(1, 0): (F(0), F(1))}, {0: (F(0), F(1)), 1: (F(0), F(1))}, {0: F(1), 1: F(1)})
    assert not original(control, outlet_lower={0: F(1, 2)})
    assert convex(control)[0]
    print(f'PASS: 160 original global pooling versus convex-QP decisions; {dict(counts)}')
    cap_control = ([0, 1], [F(1), F(1)], [F(1), F(1)], [F(1, 4), F(3, 4)],
                   {(0, 0): (F(0), F(1)), (1, 1): (F(0), F(1))},
                   {0: (F(0), F(1)), 1: (F(0), F(1))}, {0: F(1), 1: F(1)})
    assert not original(cap_control, pool_cap=F(3, 4))
    assert not convex(cap_control, F(3, 4))[0]
    assert original(cap_control, pool_cap=F(1))
    assert convex(cap_control, F(1))[0]
    print('PASS: deleting a positive pool-outlet lower bound changes infeasible to feasible.')
    print('PASS: common pool cap3/4 is infeasible, cap1 is feasible in the exact control.')
    print('All solver decisions here are numerical; exact complexity follows from the proof.')


if __name__ == '__main__':
    main()
