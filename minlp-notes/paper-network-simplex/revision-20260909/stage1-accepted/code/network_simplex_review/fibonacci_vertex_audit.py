"""Independent exact and path-vertex audit for Fibonacci section facets."""

from itertools import product
import json

import numpy as np
from scipy.optimize import linprog
import sympy as sp


def incidence(q):
    labels = [f"P{i}" for i in range(1, q + 1)] + ["H0"] + [f"H{i}" for i in range(3, q + 1)]
    cols = [{"H0", "P1"}, {"H0", "P2"}]
    for i in range(3, q + 1):
        cols.extend([{f"H{i}", f"P{i}"}, {f"H{i}", f"P{i-1}", f"P{i-2}"}])
    cols.append({f"P{q}", f"P{q-1}"})
    return sp.Matrix([[int(row in col) for col in cols] for row in labels])


def exact_data(q, complement=False):
    A = incidence(q)
    N = A.rows
    assert A.cols == N == 2 * q - 1
    assert sum(A) == 5 * q - 4
    assert all(0 < sum(A[i, j] for j in range(N)) < N for i in range(N))
    beta = sp.fibonacci(q + 1)
    expected = sp.Matrix([sp.fibonacci(i) for i in range(1, q + 1)] + [beta - 1] +
                         [beta - sp.fibonacci(i) for i in range(3, q + 1)])
    if complement:
        A = sp.ones(N, N) - A
        beta = sum(expected) - beta
        assert beta > 0
    inv = A.inv()
    alpha = A.T.inv() * (beta * sp.ones(N, 1))
    assert alpha == expected and all(t > 0 for t in alpha)
    r, s = q - 1, 0
    ju, jv = (N - 1, 0) if complement else (0, 1)
    assert A[r, ju] == A[s, jv] == 0
    ratio = alpha[r] / alpha[s]
    a, c = sp.Rational(1, 2 * N), sp.Rational(1, 8 * N)
    norm = max(sum(abs(inv[i, j]) for j in range(N)) for i in range(N))
    eps = a / (16 * (ratio + 1) * (norm + 1))
    return A, inv, alpha, r, s, a, c, eps, ju, jv


def exact_witness(data, du, dv):
    A, inv, alpha, r, s, a, c, eps, ju, jv = data
    N = A.rows
    delta = sp.zeros(N, 1)
    delta[r], delta[s] = du, dv
    tau = sp.zeros(N, 1)
    tau[s] = (alpha.T * delta)[0] / alpha[s]
    assert tau[s] >= 0
    profile = a * sp.ones(N, 1) + inv * (-delta + tau)
    assert sum(profile) == sp.Rational(1, 2)
    assert all(a / 2 < x < 3 * a / 2 for x in profile)
    assert tau[s] < a / 2
    for i in range(N):
        flows = []
        for j in range(N):
            val = profile[j] if A[i, j] else c
            if (i, j) == (r, ju):
                val += du
            if (i, j) == (s, jv):
                val += dv
            flows.append(val)
        if i == s:
            first_allowed = next(j for j in range(N) if A[s, j])
            flows[first_allowed] -= tau[s]
        size = sum(A[i, j] for j in range(N))
        target = size * a + (N - size) * c
        assert sum(flows) == target
        assert all(0 <= val <= profile[j] < 2 * a for j, val in enumerate(flows))
        assert all(0 <= profile[j] - val <= 2 * a for j, val in enumerate(flows))
        assert sum(profile[j] - val for j, val in enumerate(flows)) == sp.Rational(1, 2) - target
    assert all(0 <= 2 * a - val <= 2 * a for val in profile)
    assert sum(2 * a - val for val in profile) == sp.Rational(1, 2)


def vertices(data):
    A, inv, alpha, r, s, a, c, eps, ju, jv = data
    N = A.rows
    arcs = 2 * N + 1
    observed = [(i, j) for i in range(N) for j in range(N) if not A[i, j]]
    paths = []
    bypass = np.zeros(arcs)
    bypass[-1] = 1
    paths.append(bypass)
    for choices in product(range(2), repeat=N):
        path = np.zeros(arcs)
        for i, choice in enumerate(choices):
            path[2 * i + choice] = 1
        paths.append(path)
    columns = []
    for path in paths:
        for state in range(-1, N):
            y = np.array([float(state == j) for j in range(N)])
            z = np.array([path[2 * i] * y[j] for i, j in observed])
            columns.append(np.concatenate(([1], path, y, z)))
    matrix = np.array(columns).T
    x = []
    for i in range(N):
        size = sum(A[i, j] for j in range(N))
        target = float(size * a + (N - size) * c)
        x.extend([target, 0.5 - target])
    x.append(0.5)
    rhs = np.concatenate(([1], x, np.full(N, 1 / N), np.full(len(observed), float(c))))
    iu = 1 + arcs + N + observed.index((r, ju))
    iv = 1 + arcs + N + observed.index((s, jv))
    return matrix, rhs, iu, iv


def run_family(complement):
    exact_count = lp_count = 0
    ratios = {}
    for q in list(range(3, 13)) + [20, 30]:
        data = exact_data(q, complement)
        A, inv, alpha, r, s, a, c, eps, ju, jv = data
        if complement:
            assert A.rows ** 2 - sum(A) == 5 * q - 4
        R = alpha[r] / alpha[s]
        ratios[q] = int(R)
        cases = [(0, 0), (eps / (2 * R), -eps / 2), (-eps / (2 * R), eps / 2),
                 (eps / 2, eps / 2), (0, eps / 2)]
        for du, dv in cases:
            exact_witness(data, du, dv)
            exact_count += 1
        if q <= 4:
            matrix, rhs, iu, iv = vertices(data)
            keep = np.ones(len(rhs), dtype=bool)
            keep[[iu, iv]] = False
            objective = float(R) * matrix[iu] + matrix[iv]
            result = linprog(objective, A_eq=matrix[keep], b_eq=rhs[keep], bounds=(0, None), method="highs")
            assert result.success and abs(result.fun - float((R + 1) * c)) < 1e-8
            lp_count += 1
            cases += [(-eps / 2, -eps / 2), (0, -eps / 2)]
            for du, dv in cases:
                trial = rhs.copy()
                trial[iu], trial[iv] = float(c + du), float(c + dv)
                result = linprog(np.zeros(matrix.shape[1]), A_eq=matrix, b_eq=trial, bounds=(0, None), method="highs")
                expected = R * du + dv >= 0
                assert result.success == expected, (q, du, dv, result.message)
                lp_count += 1
    return {"exact_fibonacci_witnesses": exact_count, "path_vertex_lp_checks": lp_count,
            "verified_ratios": ratios, "status": "PASS"}


def main():
    print(json.dumps({"dense_observations": run_family(False),
                      "sparse_observations": run_family(True)}, indent=2))


if __name__ == "__main__":
    main()
