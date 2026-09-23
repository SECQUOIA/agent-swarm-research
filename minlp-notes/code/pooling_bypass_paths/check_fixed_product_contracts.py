"""Compare original fixed-split pooling LPs with the conserved-mass substitution.

These tests retain path interior variables. They check the new substitution,
not the separately reviewed endpoint projection or a full algebraic solver.
"""
from fractions import Fraction as F
import random
import gurobipy as gp
from gurobipy import GRB

ENV = gp.Env(empty=True)
ENV.setParam("OutputFlag", 0)
ENV.start()


def solve(data, theta, substituted, relax_internal=False):
    n, qualities, supply, edges, demand, spec, inlet_caps, poolcap, recv_upper = data
    k = len(qualities[0])
    receivers = [0, n]
    model = gp.Model(env=ENV)
    model.Params.OutputFlag = 0
    model.Params.DualReductions = 0
    z = {e: model.addVar(lb=0, ub=4, name=f'z{e}') for e in edges}
    v = {j: model.addVar(lb=0, ub=sum(supply), name=f'v{j}') for j in receivers}
    if substituted:
        intake = {i: float(supply[i])-gp.quicksum(z[e] for e in edges if e[0] == i)
                  for i in range(n)}
        for i in range(n):
            model.addConstr(intake[i] >= 0)
            model.addConstr(intake[i] <= inlet_caps[i])
    else:
        intake = {i: model.addVar(lb=0, ub=inlet_caps[i], name=f'y{i}') for i in range(n)}
        for i in range(n):
            model.addConstr(intake[i]+gp.quicksum(z[e] for e in edges if e[0] == i) == float(supply[i]))
    for j in range(1, n):
        model.addConstr(gp.quicksum(z[e] for e in edges if e[1] == j) == float(demand[j]))
        for a in range(k):
            mass = gp.quicksum(qualities[i][a]*z[i, j] for i, jj in edges if jj == j)
            if relax_internal:
                model.addConstr(mass <= float(demand[j]*spec[j][a]))
            else:
                model.addConstr(mass == float(demand[j]*spec[j][a]))
    boundary = [e for e in edges if e[1] in receivers]
    if substituted:
        total = float(sum(supply)-sum(demand.values()))-gp.quicksum(z[e] for e in boundary)
        mass = [float(sum(qualities[i][a]*supply[i] for i in range(n))
                      -sum(demand[j]*spec[j][a] for j in demand))
                -gp.quicksum(qualities[i][a]*z[i, j] for i, j in boundary) for a in range(k)]
    else:
        total = gp.quicksum(intake.values())
        mass = [gp.quicksum(qualities[i][a]*intake[i] for i in range(n)) for a in range(k)]
    model.addConstr(total >= 0)
    model.addConstr(total <= poolcap)
    model.addConstr(gp.quicksum(v.values()) == total)
    for t, j in zip(theta, receivers):
        model.addConstr(v[j] == float(t)*total)
        through = v[j]+gp.quicksum(z[e] for e in boundary if e[1] == j)
        for a in range(k):
            incoming_mass = float(t)*mass[a]+gp.quicksum(qualities[i][a]*z[i, jj] for i, jj in boundary if jj == j)
            model.addConstr(incoming_mass <= recv_upper[j][a]*through)
        model.addConstr(through >= (F(1, 4) if recv_upper[j][0] < 0 else 0))
    revenue = gp.quicksum((j+1)*(v[j]+gp.quicksum(z[e] for e in boundary if e[1] == j)) for j in receivers)
    constant = sum((j+1)*demand[j] for j in demand)-sum((i+1)*supply[i] for i in range(n))
    model.setObjective(revenue+float(constant), GRB.MAXIMIZE)
    model.optimize()
    if model.Status == GRB.INFEASIBLE:
        return None
    assert model.Status == GRB.OPTIMAL, model.Status
    zi = {e: F(z[e].X).limit_denominator(10**8) for e in edges}
    actual_y = [supply[i]-sum(zi[e] for e in edges if e[0] == i) for i in range(n)]
    boundary_total = sum(supply)-sum(demand.values())-sum(zi[e] for e in boundary)
    assert abs(float(sum(actual_y)-boundary_total)) < 1e-7
    if not relax_internal:
        for a in range(k):
            boundary_mass = sum(qualities[i][a]*supply[i] for i in range(n))-sum(demand[j]*spec[j][a] for j in demand)-sum(qualities[i][a]*zi[i, j] for i, j in boundary)
            assert abs(float(sum(qualities[i][a]*actual_y[i] for i in range(n))-boundary_mass)) < 1e-6
    return model.ObjVal


def instance(rng, trial):
    n = 3+trial % 6
    k = 1+trial % 3
    qualities = [[rng.randrange(4) for _ in range(k)] for _ in range(n)]
    if trial % 5 == 0:
        qualities = [[1]*k for _ in range(n)]
    edges = [(i, j) for i in range(n) for j in (i, i+1)]
    flow = {e: F(rng.randrange(1, 5), 4) for e in edges}
    inlet_caps = [0 if (i+trial) % 4 == 0 else 2 for i in range(n)]
    initial_y = [F(rng.randrange(5), 4) if inlet_caps[i] else F(0) for i in range(n)]
    if trial % 7 == 0:
        initial_y = [F(0)]*n
    supply = [initial_y[i]+flow[i, i]+flow[i, i+1] for i in range(n)]
    demand = {j: sum(flow[e] for e in edges if e[1] == j) for j in range(1, n)}
    spec = {j: [sum(qualities[i][a]*flow[i, jj] for i, jj in edges if jj == j)/demand[j] for a in range(k)] for j in demand}
    poolcap = 0 if trial % 7 == 0 else sum(inlet_caps)
    upper = {0: [3]*k, n: [3]*k}
    if trial % 6 == 1:
        upper[0] = [-1]*k
    elif trial % 6 == 2:
        upper[n] = [0]*k
    return n, qualities, supply, edges, demand, spec, inlet_caps, poolcap, upper


def negative_control():
    # Exact supplies A=B=1. Only bypass A->X, with X exact demand1.
    # Treating X's upper quality1 as an exact mass falsely changes pool mass2 to1.
    results = []
    for substituted in (False, True):
        model = gp.Model(env=ENV)
        model.Params.OutputFlag = 0
        x = model.addVar(lb=0, ub=1)
        ya = model.addVar(lb=0, ub=1)
        yb = model.addVar(lb=0, ub=1)
        v = model.addVar(lb=0, ub=1)
        model.addConstr(x == 1)
        model.addConstr(x+ya == 1)
        model.addConstr(yb == 1)
        model.addConstr(v == ya+yb)
        model.addConstr(v == 1)
        poolmass = 2-x if substituted else 2*yb
        model.addConstr(poolmass <= 1.5*v)
        model.optimize()
        results.append(model.Status == GRB.OPTIMAL)
    assert results == [False, True], results
    return results


def main():
    rng = random.Random(83)
    feasible = 0
    count = 0
    for trial in range(30):
        data = instance(rng, trial)
        for theta in ((F(1, 2), F(1, 2)), (F(0), F(1)), (F(1), F(0))):
            original = solve(data, theta, False)
            compressed = solve(data, theta, True)
            assert (original is None) == (compressed is None), (trial, theta, original, compressed)
            if original is not None:
                assert abs(original-compressed) < 1e-6, (trial, theta, original, compressed)
                feasible += 1
            count += 1
    print(f'PASS: {count} original/substituted fixed-split comparisons ({2*count} LP solves), {feasible} feasible fibers.')
    print(f'PASS: omitted-exact-quality negative control actual/invalid-substitution feasibility = {negative_control()}.')


if __name__ == '__main__':
    main()
