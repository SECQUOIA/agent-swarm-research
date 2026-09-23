#!/usr/bin/env python3
"""Exact Fibonacci-cover and witness checks, plus independent arc-flow LPs."""

from fractions import Fraction as F
import json
import numpy as np
import sympy as sp
from scipy.optimize import linprog


def cover(q):
    n = 2 * q - 1
    columns = [{q, 0}, {q, 1}]
    for i in range(2, q):
        h = q + i - 1
        columns.extend([{h, i}, {h, i - 1, i - 2}])
    columns.append({q - 1, q - 2})
    mat = sp.Matrix([[int(i in col) for col in columns] for i in range(n)])
    fib = [1, 1]
    for _ in range(q - 1):
        fib.append(sum(fib[-2:]))
    beta = fib[q]
    alpha = sp.Matrix(fib[:q] + [beta - 1] + [beta - fib[i] for i in range(2, q)])
    assert mat.T * alpha == beta * sp.ones(n, 1)
    assert all(val > 0 for val in alpha)
    assert mat.det() != 0
    return mat, alpha, fib[q - 1]


def setup(q):
    mat, alpha, ratio = cover(q)
    n = mat.rows
    mat = sp.ones(n, n) - mat
    balance = mat.T * alpha
    assert all(val == balance[0] > 0 for val in balance)
    assert mat.det() != 0
    a, c = F(1, 2 * n), F(1, 8 * n)
    sets = [{j for j in range(n) if mat[i, j]} for i in range(n)]
    arcs = [(i, i + 1) for i in range(n) for _ in range(2)] + [(0, n)]
    flows, obs = [], {}
    for i, allowed in enumerate(sets):
        val = len(allowed) * a + (n - len(allowed)) * c
        flows.extend([val, F(1, 2) - val])
        for j in range(n):
            if j not in allowed:
                obs[(2 * i, j)] = c
    flows.append(F(1, 2))
    free = [(2 * (q - 1), n - 1), (0, 0)]
    assert all(key in obs for key in free)
    return mat, alpha, ratio, a, c, sets, arcs, flows, obs, free


def solve(q, u=None, v=None):
    mat, alpha, ratio, a, c, sets, arcs, flows, obs, free = setup(q)
    n, ne = len(sets), len(arcs)
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
        rhs.append(float(flows[e]))
    for key, value in obs.items():
        if key in free:
            value = u if key == free[0] else v
            if value is None:
                continue
        row = np.zeros(ne * n)
        row[key[0] * n + key[1]] = 1
        rows.append(row)
        rhs.append(float(value))
    obj = np.zeros(ne * n)
    obj[free[0][0] * n + free[0][1]] = ratio
    obj[free[1][0] * n + free[1][1]] = 1
    return linprog(obj, A_eq=np.array(rows), b_eq=np.array(rhs),
                   bounds=(0, float(F(1, n))), method="highs",
                   options={"primal_feasibility_tolerance": 1e-9,
                            "dual_feasibility_tolerance": 1e-9})


def witness(q, s, t):
    mat, alpha, ratio, a, c, sets, arcs, flows, obs, free = setup(q)
    n = len(sets)
    slack = ratio * s + t
    assert slack >= 0
    delta = sp.zeros(n, 1)
    delta[q - 1], delta[0] = sp.Rational(s), sp.Rational(t)
    tau = sp.zeros(n, 1)
    tau[0] = sp.Rational(slack)
    d = mat.inv() * (-delta + tau)
    w = [a + F(val) for val in d]
    obs[free[0]], obs[free[1]] = c + s, c + t
    fs = [[F(0) for _ in range(n)] for _ in arcs]
    for i, allowed in enumerate(sets):
        for j in range(n):
            fs[2 * i][j] = w[j] if j in allowed else obs[(2 * i, j)]
        if i == 0:
            fs[0][min(allowed)] -= slack
        for j in range(n):
            fs[2 * i + 1][j] = w[j] - fs[2 * i][j]
    fs[-1] = [2 * a - val for val in w]
    assert all(sum(fs[e]) == flows[e] for e in range(len(arcs)))
    assert all(0 <= val <= 2 * a for row in fs for val in row)
    assert all(fs[e][j] == val for (e, j), val in obs.items())
    for j in range(n):
        for node in range(n + 1):
            bal = sum(fs[e][j] * (int(tail == node) - int(head == node))
                      for e, (tail, head) in enumerate(arcs))
            assert bal == (2 * a if node == 0 else -2 * a if node == n else 0)


def main():
    rng = np.random.default_rng(20260908)
    report = []
    for q in [3, 4, 5, 6, 7, 10, 14]:
        mat, alpha, ratio, a, c, _, _, _, _, _ = setup(q)
        n = mat.rows
        direction = sp.zeros(n, 1)
        direction[0], direction[q - 1] = ratio, -1
        direction = mat.inv() * direction
        maxdir = max(abs(F(v)) for v in direction)
        epsilon = a / (100 * (ratio + maxdir + 1))
        exact = feasible = infeasible = 0
        for i in range(-3, 4):
            s = i * epsilon / (10 * ratio)
            witness(q, s, -ratio * s)
            exact += 1
        if q <= 7:
            support = solve(q)
            assert support.success, support.message
            assert abs(support.fun - float((ratio + 1) * c)) < 1e-8
            for _ in range(30):
                s = F(int(rng.integers(-9, 10)), 10) * epsilon
                t = F(int(rng.integers(-9, 10)), 10) * epsilon
                expected = ratio * s + t >= 0
                result = solve(q, c + s, c + t)
                assert result.success == expected, (q, s, t, result.message)
                if expected:
                    witness(q, s, t)
                    exact += 1
                    feasible += 1
                else:
                    infeasible += 1
        report.append({"q": q, "states": n, "ratio": ratio,
                       "exact_witnesses": exact, "lp_feasible": feasible,
                       "lp_infeasible": infeasible})
    print(json.dumps({"passed": True, "cases": report}, indent=2))


if __name__ == "__main__":
    main()
