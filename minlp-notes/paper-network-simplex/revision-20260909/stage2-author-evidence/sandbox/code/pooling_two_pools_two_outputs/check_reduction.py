"""Cross-check the two-pool/two-output reduction against original equations.

The reference optimum is computed by exact rational vertex enumeration in
small simplex polytopes. The tested model contains only original pooling
flow/quality equations and the constructed output inequalities; it does not
contain the source polytope constraints directly.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import random

import gurobipy as gp
from gurobipy import GRB
import sympy as sp


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def vertices(n, rows):
    """Exact vertices of {z>=0,sum(z)=1,A z<=d}."""
    all_rows = list(rows) + [([-int(i == j) for i in range(n)], 0)
                              for j in range(n)]
    result = set()
    for active in combinations(all_rows, n-1):
        mat = sp.Matrix([[1]*n] + [list(a) for a, _ in active])
        if mat.det() == 0:
            continue
        rhs = sp.Matrix([1] + [b for _, b in active])
        z = tuple(F(x) for x in mat.inv()*rhs)
        if all(dot(a, z) <= b for a, b in all_rows):
            result.add(z)
    return sorted(result)


def reference(a, b, rows):
    vs = vertices(len(a), rows)
    if not vs:
        return F(0), []
    assert all(dot(a, z) >= 1 and dot(b, z) >= 0 for z in vs)
    # f(a,b)=b(1+1/a) is quasiconvex for a>=1,b>=0: f<=t is
    # b<=t*a/(a+1), a hypograph of a concave function for t>=0.
    # Thus a maximum on this compact polytope occurs at a vertex.
    return max(dot(b, z)*(1+1/dot(a, z)) for z in vs), vs


def solve_pooling(a, b, rows, *, shift=False, bypass=False,
                  omit_output_one_rows=False):
    n = len(a)
    qualities = [list(a)] + [list(row) for row, _ in rows]
    anchor = [0] + [bound for _, bound in rows]
    mu1 = [1] + [bound for _, bound in rows]
    mu2 = [max([0] + list(a))] + [bound for _, bound in rows]
    if shift:
        for k in range(len(qualities)):
            offset = -min([0, anchor[k], mu1[k], mu2[k]] + qualities[k])
            qualities[k] = [v+offset for v in qualities[k]]
            anchor[k] += offset
            mu1[k] += offset
            mu2[k] += offset
    model = gp.Model()
    model.Params.OutputFlag = 0
    model.Params.NonConvex = 2
    model.Params.MIPGap = 0
    model.Params.MIPGapAbs = 1e-8
    model.Params.FeasibilityTol = 1e-9
    model.Params.OptimalityTol = 1e-9
    model.Params.TimeLimit = 30
    x = model.addVars(n, ub=2, name='intake')
    t = model.addVar(ub=2, name='throughput')
    y = model.addVars(2, ub=1, name='outflow')
    h = model.addVar(ub=1, name='anchor_inflow')
    if bypass:
        anchor_out = h
    else:
        anchor_out = model.addVar(ub=1, name='anchor_pool_outflow')
        model.addConstr(h == anchor_out)
    model.addConstr(gp.quicksum(x.values()) == t)
    model.addConstr(y[0]+y[1] == t)
    model.addConstr(y[0]+anchor_out <= 1)
    p, ph = [], []
    for k, lam in enumerate(qualities):
        p.append(model.addVar(lb=float(min(lam)), ub=float(max(lam)),
                             name=f'quality_{k}'))
        model.addConstr(gp.quicksum(float(lam[i])*x[i] for i in range(n))
                        == p[k]*t)
        if bypass:
            anchor_mass = float(anchor[k])*h
        else:
            ph.append(model.addVar(lb=float(anchor[k]), ub=float(anchor[k]),
                                   name=f'anchor_quality_{k}'))
            model.addConstr(float(anchor[k])*h == ph[k]*anchor_out)
            anchor_mass = ph[k]*anchor_out
        if not (omit_output_one_rows and k > 0):
            model.addConstr(p[k]*y[0]+anchor_mass
                            <= float(mu1[k])*(y[0]+anchor_out))
        model.addConstr(p[k]*y[1] <= float(mu2[k])*y[1])
    model.setObjective(gp.quicksum(float(b[i])*x[i] for i in range(n)),
                       GRB.MAXIMIZE)
    model.optimize()
    assert model.Status == GRB.OPTIMAL, model.Status
    answer = model.ObjVal
    model.dispose()
    return answer


def generate(rng, n):
    # Signed coefficients deliberately exercise generators outside P.
    a = [rng.randint(-4, 7) for _ in range(n)]
    b = [rng.randint(-4, 9) for _ in range(n)]
    a = [F(v)+2-F(sum(a), n) for v in a]
    b = [F(v)+2-F(sum(b), n) for v in b]
    rows = [([-v for v in a], F(-1)), ([-v for v in b], F(0))]
    for _ in range(2):
        row = [rng.randint(-3, 4) for _ in range(n)]
        rows.append((row, F(sum(row), n)+F(rng.randint(0, 2), 3)))
    return a, b, rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--trials', type=int, default=12)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    checked = 0
    for trial in range(args.trials):
        a, b, rows = generate(rng, 2+trial % 2)
        expected, vs = reference(a, b, rows)
        for shift, bypass in [(False, False), (True, False), (True, True)]:
            actual = solve_pooling(a, b, rows, shift=shift, bypass=bypass)
            assert abs(actual-float(expected)) <= 2e-5, (
                trial, shift, bypass, actual, expected)
            checked += 1
        print(f'trial={trial} vertices={len(vs)} profit={expected}', flush=True)
    # Boundary cases: a=1, b=0, singleton P, and an empty P.
    boundaries = [([1], [3], []), ([2, 3], [0, 0], []),
                  ([2, 4], [3, 1], [([1, 0], F(1, 2)),
                                    ([-1, 0], F(-1, 2))]),
                  ([2], [3], [([1], 0)])]
    for a, b, rows in boundaries:
        expected, _ = reference(a, b, rows)
        actual = solve_pooling(a, b, rows)
        assert abs(actual-float(expected)) <= 2e-5, (actual, expected)
        checked += 1
    # Removing P-row constraints at output1 creates a false positive by
    # allowing L to avoid output2 and use a forbidden source mixture.
    a, b, rows = [1, 1], [0, 10], [([0, 1], 0)]
    correct = solve_pooling(a, b, rows)
    broken = solve_pooling(a, b, rows, omit_output_one_rows=True)
    assert abs(correct) <= 1e-6 and abs(broken-10) <= 1e-5
    print(f'PASS {checked} original-model solves; negative control '
          f'correct={correct:.8g}, missing-output1-rows={broken:.8g}', flush=True)


if __name__ == '__main__':
    main()
