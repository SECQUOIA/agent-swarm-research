#!/usr/bin/env python3
"""Check the TTSP coefficient obstruction against original-arc state-flow LPs.

The LP retains every arc in every explicit simplex state. It does not use the
derived shared-profile or subset-inequality formulation. Exact witnesses check
the independent construction without floating-point feasibility tolerances.
"""

from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog


def instance(k):
    n = k + 1
    a, c, p = F(1, 2 * n), F(1, 8 * n), F(1, 2)
    arcs = [(i, i + 1) for i in range(n) for _ in range(2)] + [(0, n)]
    allowed = [set(range(k))] + [{i, k} for i in range(k)]
    flow = []
    observed = {}
    for i in range(n):
        ai = k * a + c if i == 0 else 2 * a + (k - 1) * c
        flow.extend([ai, p - ai])
        for j in range(n):
            if j not in allowed[i]:
                observed[(2 * i, j)] = c
    flow.append(1 - p)
    free = [(0, k), (2, 1)]
    return n, a, c, p, arcs, allowed, flow, observed, free


def solve(k, u=None, v=None, objective=False):
    n, a, c, p, arcs, _, flow, observed, free = instance(k)
    ne = len(arcs)
    rows, rhs = [], []
    for j in range(n):
        for node in range(n + 1):
            row = np.zeros(ne * n)
            for e, (tail, head) in enumerate(arcs):
                row[e * n + j] = int(tail == node) - int(head == node)
            rows.append(row)
            rhs.append(float(F(1, n) if node == 0 else -F(1, n) if node == n else 0))
    for e in range(ne):
        row = np.zeros(ne * n)
        row[e * n:(e + 1) * n] = 1
        rows.append(row)
        rhs.append(float(flow[e]))
    for key, value in observed.items():
        if key in free:
            value = u if key == free[0] else v
            if value is None:
                continue
        row = np.zeros(ne * n)
        row[key[0] * n + key[1]] = 1
        rows.append(row)
        rhs.append(float(value))
    obj = np.zeros(ne * n)
    if objective:
        obj[free[0][0] * n + free[0][1]] = k - 1
        obj[free[1][0] * n + free[1][1]] = 1
    return linprog(obj, A_eq=np.array(rows), b_eq=np.array(rhs),
                   bounds=(0, float(F(1, n))), method="highs")


def exact_witness(k, s, t):
    n, a, c, p, arcs, allowed, flow, observed, free = instance(k)
    d = (k - 1) * s + t
    assert d >= 0
    w = [a + (k - 2) * s] + [a - s] * (k - 1) + [a + s]
    u, v = c + s, c + t
    fs = [[F(0) for _ in range(n)] for _ in arcs]
    for i in range(n):
        for j in range(n):
            fs[2 * i][j] = w[j] if j in allowed[i] else c
        if i == 0:
            fs[0][k] = u
        if i == 1:
            fs[2][0] -= d
            fs[2][1] = v
        for j in range(n):
            fs[2 * i + 1][j] = w[j] - fs[2 * i][j]
    for j in range(n):
        fs[-1][j] = 2 * a - w[j]
    for e in range(len(arcs)):
        assert sum(fs[e]) == flow[e]
        assert all(0 <= val <= F(1, n) for val in fs[e])
    observed[free[0]], observed[free[1]] = u, v
    assert all(fs[e][j] == val for (e, j), val in observed.items())
    for j in range(n):
        for node in range(n + 1):
            balance = sum(fs[e][j] * (int(tail == node) - int(head == node))
                          for e, (tail, head) in enumerate(arcs))
            target = F(1, n) if node == 0 else -F(1, n) if node == n else 0
            assert balance == target


def main():
    rng = np.random.default_rng(20260907)
    report = []
    for k in [3, 4, 5, 8, 12]:
        _, a, c, _, _, _, _, _, _ = instance(k)
        support = solve(k, objective=True)
        assert support.success, support.message
        assert abs(support.fun - float(k * c)) < 1e-9
        epsilon = a / (8 * k)
        feasible = infeasible = witnesses = 0
        points = [(F(0), F(0))]
        for j in range(-5, 6):
            s = j * epsilon / (10 * k)
            points.append((s, -(k - 1) * s))
        for _ in range(80):
            s = F(int(rng.integers(-99, 100)), 100) * epsilon
            t = F(int(rng.integers(-99, 100)), 100) * epsilon
            points.append((s, t))
        for s, t in points:
            expected = (k - 1) * s + t >= 0
            result = solve(k, c + s, c + t)
            assert result.success == expected, (k, s, t, result.message)
            if expected:
                feasible += 1
                exact_witness(k, s, t)
                witnesses += 1
            else:
                infeasible += 1
        report.append({"k": k, "ratio": k - 1, "support": str(k * c),
                       "feasible": feasible, "infeasible": infeasible,
                       "exact_witnesses": witnesses})
    print(json.dumps({"passed": True, "cases": report}, indent=2))


if __name__ == "__main__":
    main()
