"""Exact, small-instance audit of the sparse-quadratic PSD-cover proof.

This is a reviewer check, not a claimed efficient implementation. It exhausts
supports and checks the maximum-volume branch for each nonsingular support.
"""

from itertools import combinations
import random

import sympy as sp


def subsets(n):
    return [frozenset(i for i in range(n) if mask & (1 << i))
            for mask in range(1 << n)]


def psd(matrix):
    return all(matrix.extract(rows, rows).det() >= 0
               for size in range(1, matrix.rows + 1)
               for rows in combinations(range(matrix.rows), size))


def normalize(matrix):
    lower, diagonal = matrix.LDLdecomposition(hermitian=False)
    scales = []
    for value in diagonal.diagonal():
        scale = sp.Integer(1)
        while scale * scale * value < 1:
            scale *= 2
        while scale * scale * value >= 4:
            scale /= 2
        scales.append(scale)
    return sp.diag(*scales) * lower.inv()


def check_case(U, ds, bs, costs, cardinality=False):
    U = sp.Matrix(U)
    n, r = U.shape
    dim = r + 1
    prior = sp.diag(*([1] * r + [0]))
    atoms = []
    for i in range(n):
        vector = sp.Matrix([*U.row(i), bs[i]])
        atoms.append(vector * vector.T / ds[i])
    fixed = []
    for j in range(r):
        vector = sp.eye(dim)[:, j]
        fixed.append(vector * vector.T)
    all_atoms = atoms + fixed
    epsilon = sp.Rational(3, 4)
    mesh = epsilon / (2 * dim * n)
    supports = subsets(n)
    zero = sp.zeros(dim)
    matrices = {S: prior + sum((atoms[i] for i in S), zero)
                for S in supports}
    gains = {}
    Q = sp.diag(*ds) + U * U.T
    for S in supports:
        rows = sorted(S)
        selected_b = sp.Matrix([bs[i] for i in rows])
        gain = ((selected_b.T * Q.extract(rows, rows).inv() * selected_b)[0]
                if rows else sp.Integer(0))
        K = matrices[S]
        schur = K[-1, -1] - (
            K[-1:, :-1] * K[:-1, :-1].inv() * K[:-1, -1:])[0]
        assert gain == schur
        assert 0 <= gain <= sum(bs[i] ** 2 / ds[i] for i in range(n))
        assert (K.det() > 0) == (gain > 0)
        gains[S] = gain

    branches = collisions = replacements = 0
    output_candidates = {frozenset()}
    largest_error = sp.Integer(0)
    for S in supports:
        if gains[S] == 0:
            continue
        labels = sorted(S) + list(range(n, n + r))
        candidates = []
        for basis in combinations(labels, dim):
            anchor = sum((all_atoms[j] for j in basis), zero)
            candidates.append((anchor.det(), basis, anchor))
        _, basis, anchor = max(candidates, key=lambda candidate: candidate[0])
        assert anchor.det() > 0
        inverse = anchor.inv()
        assert all(sp.trace(inverse * all_atoms[j]) <= dim for j in labels)
        transform = normalize(anchor)
        normalized_anchor = transform * anchor * transform.T
        assert psd(normalized_anchor - sp.eye(dim))
        assert all(v < 4 for v in normalized_anchor.diagonal())
        admitted = [i for i in range(n)
                    if sp.trace(inverse * atoms[i]) <= dim]
        forced = frozenset(j for j in basis if j < n)
        assert S.issubset(admitted)
        transformed = {i: transform * atoms[i] * transform.T for i in admitted}
        assert all(sp.trace(matrix) < 4 * dim for matrix in transformed.values())
        coordinates = list(combinations(range(dim), 2)) + [(j, j) for j in range(dim)]
        labels = {i: tuple(int(sp.floor(transformed[i][a, b] / mesh))
                           for a, b in coordinates) + ((1,) if cardinality else ())
                  for i in admitted}

        width = len(coordinates) + int(cardinality)
        table = {tuple(0 for _ in range(width)): (sp.Integer(0), frozenset())}
        for i in admitted:
            next_table = {} if i in forced else dict(table)
            for key, (cost, support) in table.items():
                new_key = tuple(a + b for a, b in zip(key, labels[i]))
                new_value = (cost + costs[i], support | {i})
                old = next_table.get(new_key)
                if old is not None:
                    collisions += 1
                if old is None or new_value[0] < old[0]:
                    next_table[new_key] = new_value
            table = next_table
        target_key = tuple(sum(labels[i][j] for i in S) for j in range(width))
        cost, T = table[target_key]
        output_candidates.add(T)
        assert cost <= sum(costs[i] for i in S)
        if cardinality:
            assert len(T) == len(S)
        KS = transform * matrices[S] * transform.T
        KT = transform * matrices[T] * transform.T
        assert psd(KS - sp.eye(dim)) and psd(KT - sp.eye(dim))
        assert all(abs(v) < n * mesh for v in KT - KS)
        assert psd(KT - (1 - epsilon) * KS)
        c = transform * sp.eye(dim)[:, -1]
        assert gains[S] == 1 / (c.T * KS.inv() * c)[0]
        assert gains[T] >= (1 - epsilon) * gains[S]
        if T != S:
            replacements += 1
        if gains[S] > gains[T]:
            largest_error = max(largest_error, (gains[S] - gains[T]) / gains[S])
        branches += 1
    negative = frozenset(i for i in range(n) if costs[i] < 0)
    for S in supports:
        if gains[S] == 0:
            assert sum(costs[i] for i in negative) - gains[negative] <= sum(costs[i] for i in S)
    if all(cost >= 0 for cost in costs):
        for capacity in {sum(costs[i] for i in S) for S in supports}:
            for limit in (range(n + 1) if cardinality else (n,)):
                feasible = [S for S in supports if len(S) <= limit
                            and sum(costs[i] for i in S) <= capacity]
                retained = [S for S in output_candidates if len(S) <= limit
                            and sum(costs[i] for i in S) <= capacity]
                assert max(gains[S] for S in retained) >= (
                    1 - epsilon) * max(gains[S] for S in feasible)
    return branches, collisions, replacements, largest_error


def main():
    random.seed(20260927)
    cases = []
    for r in (1, 2):
        for _ in range(3):
            n = 4
            cases.append(([[random.randint(-3, 3) for _ in range(r)] for _ in range(n)],
                          [sp.Rational(random.randint(1, 5)) for _ in range(n)],
                          [sp.Rational(random.randint(-2, 2)) for _ in range(n)],
                          [sp.Rational(random.randint(-4, 4)) for _ in range(n)]))
    cases.extend([
        ([[1], [sp.Rational(1, 2**20)], [sp.Rational(-1, 2**21)], [0]],
         [sp.Integer(1)] * 4,
         [sp.Integer(1), sp.Rational(1, 2**22), sp.Integer(0), sp.Integer(0)],
         [sp.Integer(2), sp.Integer(-1), sp.Integer(-1), sp.Integer(-3)]),
        ([[2**30, 1], [2**30 + 1, 1], [0, 0], [sp.Rational(1, 2**20), 1]],
         [sp.Rational(1, 2**25), sp.Integer(1), sp.Integer(1), sp.Integer(2)],
         [sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Rational(1, 2**30)],
         [sp.Integer(3), sp.Integer(-1), sp.Integer(-2), sp.Integer(1)]),
        ([[0], [1], [2], [3]], [sp.Integer(1)] * 4,
         [sp.Integer(0)] * 4, [sp.Integer(-1), sp.Integer(1), sp.Integer(-2), sp.Integer(2)]),
    ])
    results = [check_case(*case) for case in cases]
    budget_case = (
        [[1], [-2], [sp.Rational(1, 2**20)], [2**20]],
        [sp.Integer(1)] * 4,
        [sp.Integer(2), sp.Integer(1), sp.Integer(1), sp.Integer(-1)],
        [sp.Integer(3), sp.Rational(1, 2), sp.Integer(2**40), sp.Integer(2)],
    )
    results.extend(check_case(*budget_case, cardinality=flag) for flag in (False, True))
    print(f"cases={len(results)} nonsingular_support_branches={sum(x[0] for x in results)} "
          f"DP_key_collisions={sum(x[1] for x in results)} "
          f"target_replacements={sum(x[2] for x in results)}")
    print(f"largest_observed_relative_gain_loss={max(x[3] for x in results)}")
    print("All exact support, Schur, normalization, rounding, Loewner, cost, budget, and cardinality assertions passed.")


if __name__ == "__main__":
    main()
