"""Original physical network checks for the degree-two vertex selector."""
from fractions import Fraction as Q
from itertools import product
import gurobipy as gp
from gurobipy import GRB


def network(n, endpoint=None):
    model = gp.Model()
    model.Params.OutputFlag = 0
    model.Params.NonConvex = 2
    model.Params.FeasibilityTol = 1e-8
    model.Params.OptimalityTol = 1e-8
    model.Params.MIPGap = 1e-8
    model.Params.TimeLimit = 60
    supply = {f'I{j}': float(Q(4) ** (j-n)) for j in range(1, n+1)}
    supply.update(A=1, B=1, Z=1)
    quality = {f'I{j}': n-j for j in range(1, n+1)}
    quality.update(A=1, B=2, Z=0)
    cost = {i: s for i, s in supply.items()}
    cost['Z'] = 2
    revenue = {f'O{j}': float(Q(4) ** (j+1-n)) for j in range(n)}
    revenue.update({f'O{n}': 1, 'W': 1, 'V': 1})
    caps = {f'O{j}': float(Q(4) ** (j+1-n)) for j in range(n)}
    caps.update({f'O{n}': 1, 'W': 1, 'V': 2})
    spec = {'O0': n-1, f'O{n}': 1, 'W': 2, 'V': 1}
    spec.update({f'O{j}': n-j-Q(1, 2) for j in range(1, n)})
    arcs = {}
    for j in range(1, n+1):
        for k in (j-1, j):
            arcs[f'I{j}', f'O{k}'] = model.addVar(ub=supply[f'I{j}'])
    for i, j in [('A', f'O{n}'), ('A', 'P'), ('B', 'P'),
                 ('B', 'W'), ('P', 'W'), ('P', 'V'), ('Z', 'V')]:
        arcs[i, j] = model.addVar(ub=1)
    q = model.addVar(lb=1, ub=2)
    for i, amount in supply.items():
        outgoing = gp.quicksum(v for (a, b), v in arcs.items() if a == i)
        if i == 'Z':
            model.addConstr(outgoing <= amount)
        else:
            model.addConstr(outgoing == amount)
    intake = gp.quicksum(v for (i, j), v in arcs.items() if j == 'P')
    outlet = gp.quicksum(v for (i, j), v in arcs.items() if i == 'P')
    model.addConstr(intake == 1)
    model.addConstr(outlet == intake)
    model.addQConstr(q * outlet == gp.quicksum(
        quality[i] * v for (i, j), v in arcs.items() if j == 'P'))
    for j in caps:
        flow = gp.quicksum(v for (i, b), v in arcs.items() if b == j)
        if j in (f'O{n}', 'W'):
            model.addConstr(flow == caps[j])
        else:
            model.addConstr(flow <= caps[j])
        mass = gp.QuadExpr()
        for (i, b), v in arcs.items():
            if b == j:
                mass += q*v if i == 'P' else quality[i]*v
        model.addQConstr(mass <= float(spec[j])*flow)
    profit = gp.quicksum(revenue[j]*v for (i, j), v in arcs.items() if j in revenue)
    profit -= gp.quicksum(cost[i]*v for (i, j), v in arcs.items() if i in cost)
    model.setObjective(profit, GRB.MAXIMIZE)
    if endpoint is not None:
        model.addConstr(arcs[f'I{n}', f'O{n}'] == float(endpoint))
    assert max(sum(a == i for a, b in arcs) for i in supply) <= 2
    assert max(sum(b == j for a, b in arcs) for j in caps) <= 2
    return model, arcs


def main():
    checks = 0
    for n in range(2, 6):
        m, _ = network(n)
        m.optimize()
        assert m.Status == GRB.OPTIMAL and abs(m.ObjVal) < 1e-7
        checks += 1
        for bits in product((0, 1), repeat=n):
            x = Q(0)
            for bit in bits:
                x = bit + (1-2*bit)*x/4
            m, arcs = network(n, x)
            m.optimize()
            assert m.Status == GRB.OPTIMAL and abs(m.ObjVal) < 1e-7
            assert abs(arcs['Z', 'V'].X-float(x-x*x)) < 1e-7
            checks += 1
    # Interior terminal coordinate absent from every n=3 endpoint pattern.
    m, _ = network(3, Q(1, 2))
    m.optimize()
    assert m.Status == GRB.OPTIMAL and m.ObjVal < -0.01
    checks += 1
    print(f'PASS: {checks} original-network solves, including free global optima, '
          'all terminal vertex slices through n=5, and an interior negative control.')
    slopes = 0
    for n in range(2, 11):
        terminals = {}
        for bits in product((0, 1), repeat=n):
            t = Q(0)
            for bit in bits:
                t = bit + (1-2*bit)*t/4
            terminals[bits] = t
        assert len(set(terminals.values())) == 2**n
        delta = Q(4) ** (-n)
        for bits, t in terminals.items():
            for j in range(n):
                neighbor = bits[:j] + (1-bits[j],) + bits[j+1:]
                dt = terminals[neighbor]-t
                assert -dt*dt+delta*dt < 0
                slopes += 1
    print(f'PASS: {slopes} exact outward edge slopes for the distinct-local-optima '
          'price perturbation, through n=10.')


if __name__ == '__main__':
    main()
