"""Independent LP checks of the shared-expansion graph formulation.

Checks projected fibers, including every binary assignment for each small
case, against exact graph inclusion and componentwise McCormick error.
Also checks finite accuracy allocation LPs on seeded random graphs.
This is a numerical verification aid, not a proof of the lower bound.
"""
from itertools import product
from math import ceil, log2

import numpy as np
from scipy.optimize import linprog


def allocation(n, edges, demand):
    if not edges:
        return np.zeros(n)
    mat = np.zeros((len(edges), n))
    for row, (i, j) in enumerate(edges):
        mat[row, i] = mat[row, j] = -1
    ans = linprog(np.ones(n), A_ub=mat, b_ub=-np.asarray(demand),
                  bounds=(0, None), method="highs")
    assert ans.success, ans.message
    return ans.x


def projected_fiber(x, edges, depths, bits):
    """Explicit four-row product system with x and binary coordinates fixed."""
    n = len(x)
    h = np.exp2(-np.asarray(depths, dtype=float))
    offsets = []
    pos = 0
    for depth in depths:
        offsets.append(sum(bits[pos + k] * 2.0 ** (-k - 1)
                           for k in range(depth)))
        pos += depth
    residual = np.asarray(x) - offsets
    if min(residual) < -1e-10 or max(residual - h) > 1e-10:
        return None

    bounds = [(0, None) for _ in edges]  # w coordinates first
    inequalities, rhs, equalities = [], [], []

    def variable(upper):
        index = len(bounds)
        bounds.append((0, upper))
        return index

    def leq(terms, bound):
        inequalities.append(terms)
        rhs.append(bound)

    starts = np.cumsum([0] + list(depths))
    for e, (i, j) in enumerate(edges):
        expr = {e: 1.0}
        for vertex, value, upper in [(i, x[j], 1.0), (j, residual[i], h[i])]:
            for k in range(depths[vertex]):
                beta = bits[starts[vertex] + k]
                aux = variable(upper)
                leq({aux: 1}, upper * beta)
                leq({aux: 1}, value)
                leq({aux: -1}, -value + upper * (1 - beta))
                expr[aux] = -2.0 ** (-k - 1)
        q = variable(h[i] * h[j])
        # McCormick for q=r_i r_j, with residual coordinates fixed.
        leq({q: -1}, -h[i] * residual[j] - h[j] * residual[i] + h[i] * h[j])
        leq({q: 1}, h[i] * residual[j])
        leq({q: 1}, h[j] * residual[i])
        expr[q] = -1
        equalities.append(expr)

    def dense(rows):
        arr = np.zeros((len(rows), len(bounds)))
        for k, row in enumerate(rows):
            for index, coefficient in row.items():
                arr[k, index] = coefficient
        return arr

    aub, aeq = dense(inequalities), dense(equalities)
    answer = []
    for e in range(len(edges)):
        cost = np.zeros(len(bounds))
        cost[e] = 1
        low = linprog(cost, A_ub=aub, b_ub=rhs, A_eq=aeq,
                      b_eq=np.zeros(len(edges)), bounds=bounds, method="highs")
        high = linprog(-cost, A_ub=aub, b_ub=rhs, A_eq=aeq,
                       b_eq=np.zeros(len(edges)), bounds=bounds, method="highs")
        assert low.success and high.success
        answer.append((low.fun, -high.fun))
    return answer


def main():
    rng = np.random.default_rng(20260905)
    allocation_checks = 0
    for n in range(2, 12):
        for _ in range(25):
            edges = [(i, j) for i in range(n) for j in range(i + 1, n)
                     if rng.random() < 0.4]
            if not edges:
                continue
            epsilon = np.exp2(-rng.uniform(0, 30, len(edges)))
            d4 = np.maximum(0, -np.log2(4 * epsilon))
            d20 = np.maximum(0, -np.log2(20 * epsilon))
            s4, s20 = allocation(n, edges, d4), allocation(n, edges, d20)
            cover = allocation(n, edges, np.ones(len(edges)))
            rounded = allocation(n, edges, np.ceil(d4))
            assert sum(s4) <= sum(s20) + sum(cover) * log2(5) + 1e-7
            assert sum(rounded) <= sum(s4) + sum(cover) + 1e-7
            depths = np.ceil(rounded - 1e-9).astype(int)
            for e, (i, j) in enumerate(edges):
                assert 2.0 ** (-int(depths[i] + depths[j])) / 4 <= epsilon[e] + 1e-12
            allocation_checks += 1

    cases = [
        (3, [(0, 1), (1, 2), (0, 2)], [2, 1, 1]),
        (4, [(0, 1), (0, 2), (0, 3)], [3, 0, 0, 0]),
        (4, [(0, 1), (1, 2), (2, 3)], [0, 2, 2, 0]),
        (2, [(0, 1)], [0, 0]),
    ]
    lp_checks = 0
    for n, edges, depths in cases:
        points = [np.zeros(n), np.ones(n), np.full(n, 0.5)]
        points.extend(rng.random((8, n)))
        # Includes a cell midpoint where local maximal error is attained.
        points.append(np.exp2(-np.asarray(depths, dtype=float)) / 2)
        worst = np.zeros(len(edges))
        for x in points:
            covered = False
            for bits in product((0, 1), repeat=sum(depths)):
                interval = projected_fiber(x, edges, depths, bits)
                if interval is None:
                    continue
                covered = True
                for e, (i, j) in enumerate(edges):
                    value = x[i] * x[j]
                    low, high = interval[e]
                    error = max(value - low, high - value)
                    assert low <= value + 1e-9 and high >= value - 1e-9
                    bound = 2.0 ** (-depths[i] - depths[j]) / 4
                    assert error <= bound + 1e-9
                    worst[e] = max(worst[e], error)
                    lp_checks += 2
            assert covered
        for e, (i, j) in enumerate(edges):
            assert abs(worst[e] - 2.0 ** (-depths[i] - depths[j]) / 4) < 1e-9

    print(f"PASS: {allocation_checks} weighted allocation cases; {lp_checks} projected LP extrema")


if __name__ == "__main__":
    main()
