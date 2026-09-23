"""Independent checks using path/simplex hull vertices, not state-flow LPs.

Run: python code/network_simplex_review/series_parallel_vertex_audit.py
"""

from fractions import Fraction as Q
from itertools import product
import json

import numpy as np
from scipy.optimize import linprog


def vertex_section(k):
    n = k + 1
    arcs = 2 * (k + 1) + 1
    sets = [set(range(k))] + [{i, k} for i in range(k)]
    observed = [(2 * i, j) for i in range(k + 1) for j in range(n) if j not in sets[i]]
    u, v = observed.index((0, k)), observed.index((2, 1))
    paths = []
    bypass = np.zeros(arcs)
    bypass[-1] = 1
    paths.append(bypass)
    for choices in product(range(2), repeat=k + 1):
        path = np.zeros(arcs)
        for i, choice in enumerate(choices):
            path[2 * i + choice] = 1
        paths.append(path)
    columns = []
    for path in paths:
        for state in range(-1, n):  # Include the original residual simplex vertex.
            y = np.array([float(state == j) for j in range(n)])
            z = np.array([path[e] * y[j] for e, j in observed])
            columns.append(np.concatenate(([1], path, y, z)))
    matrix = np.array(columns).T
    a = 1 / (2 * n)
    c = a / 4
    x = np.array([val for i in range(k + 1)
                  for val in ((k * a + c if i == 0 else 2 * a + (k - 1) * c),
                              (0.5 - k * a - c if i == 0 else 0.5 - 2 * a - (k - 1) * c))] + [0.5])
    rhs = np.concatenate(([1], x, np.full(n, 1 / n), np.full(len(observed), c)))
    iu = 1 + arcs + n + u
    iv = 1 + arcs + n + v
    return matrix, rhs, iu, iv, a, c


def exact_witness(k, s, t):
    n = k + 1
    a, c = Q(1, 2 * n), Q(1, 8 * n)
    w = [a + (k - 2) * s] + [a - s] * (k - 1) + [a + s]
    d = (k - 1) * s + t
    assert d >= 0 and sum(w) == Q(1, 2)
    gadgets = []
    for i in range(k + 1):
        ai = [c] * n
        if i == 0:
            ai = w[:k] + [c + s]
        elif i == 1:
            ai[0], ai[-1], ai[1] = w[0] - d, w[-1], c + t
        else:
            ai[i - 1], ai[-1] = w[i - 1], w[-1]
        bi = [wj - aj for wj, aj in zip(w, ai)]
        assert all(0 <= f <= 2 * a for f in ai + bi)
        assert all(aj + bj == wj for aj, bj, wj in zip(ai, bi, w))
        target = k * a + c if i == 0 else 2 * a + (k - 1) * c
        assert sum(ai) == target and sum(bi) == Q(1, 2) - target
        allowed = set(range(k)) if i == 0 else {i - 1, k}
        for j in range(n):
            if j not in allowed:
                expected = c + s if (i, j) == (0, k) else c + t if (i, j) == (1, 1) else c
                assert ai[j] == expected
        gadgets.append((ai, bi))
    bypass = [2 * a - wj for wj in w]
    assert all(0 <= f <= 2 * a for f in bypass)
    assert sum(bypass) == Q(1, 2)
    assert all(wj + hj == 2 * a for wj, hj in zip(w, bypass))


def main():
    rng = np.random.default_rng(823410)
    lp_count, exact_count = 0, 0
    for k in range(3, 7):
        matrix, rhs, iu, iv, a, c = vertex_section(k)
        keep = np.ones(len(rhs), dtype=bool)
        keep[[iu, iv]] = False
        objective = (k - 1) * matrix[iu] + matrix[iv]
        result = linprog(objective, A_eq=matrix[keep], b_eq=rhs[keep], bounds=(0, None), method="highs")
        assert result.success and abs(result.fun - k * c) < 1e-8
        lp_count += 1
        eps = a / (8 * k)
        points = [(0.0, 0.0)]
        for s in [-eps / (2 * k), eps / (2 * k)]:
            points.append((s, -(k - 1) * s))
        points.extend(tuple(rng.uniform(-0.95 * eps, 0.95 * eps, 2)) for _ in range(40))
        for s, t in points:
            test_rhs = rhs.copy()
            test_rhs[iu], test_rhs[iv] = c + s, c + t
            result = linprog(np.zeros(matrix.shape[1]), A_eq=matrix, b_eq=test_rhs, bounds=(0, None), method="highs")
            expected = (k - 1) * s + t >= -1e-12
            assert result.success == expected, (k, s, t, result.message)
            lp_count += 1
    for k in list(range(3, 30)) + [50, 100, 1000]:
        eps = Q(1, 16 * k * (k + 1))
        # Rational boundary and strictly interior points, including both slope directions.
        points = [(Q(0), Q(0)), (eps / (2 * k), -(k - 1) * eps / (2 * k)),
                  (-eps / (2 * k), (k - 1) * eps / (2 * k)),
                  (eps / 2, eps / 2), (Q(0), eps / 2)]
        for s, t in points:
            exact_witness(k, s, t)
            exact_count += 1
    print(json.dumps({"path_vertex_lp_checks": lp_count, "exact_fraction_witnesses": exact_count,
                      "status": "PASS"}, indent=2))


if __name__ == "__main__":
    main()
