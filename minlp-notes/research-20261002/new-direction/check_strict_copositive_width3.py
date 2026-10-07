#!/usr/bin/env python3
"""Targeted exact checks of the width-three SUBSET SUM construction.

The zero-set equivalence is a mathematical argument; finite tests below
check its formulas, rational witnesses, graph decomposition, and curvature
certificate. They do not establish a uniform positive growth margin.
"""

from fractions import Fraction as F
from itertools import product
from random import Random


def indices(n):
    return 0, list(range(1, n + 1)), list(range(n + 1, 2 * n + 1)), list(
        range(2 * n + 1, 3 * n + 2)
    )


def construction(weights, target):
    n = len(weights)
    assert n and all(isinstance(a, int) and a > 0 for a in weights)
    assert isinstance(target, int) and target >= 0
    size = 3 * n + 2
    t, z, w, y = indices(n)

    def form(entries):
        row = [F(0)] * size
        for index, coefficient in entries:
            row[index] += coefficient
        return row

    forms = [form([(y[0], 1)]), form([(y[-1], 1), (t, -target)])]
    for i, weight in enumerate(weights):
        forms.append(form([(z[i], 1), (w[i], 1), (t, -1)]))
        forms.append(form([(y[i + 1], 1), (y[i], -1), (z[i], -weight)]))
    matrix = [[sum(row[i] * row[j] for row in forms)
               for j in range(size)] for i in range(size)]
    for zi, wi in zip(z, w):
        matrix[zi][wi] += F(1, 2)
        matrix[wi][zi] += F(1, 2)
    return matrix, forms


def quad(matrix, x):
    return sum(x[i] * matrix[i][j] * x[j]
               for i in range(len(x)) for j in range(len(x)))


def direct_value(weights, target, x):
    t, z, w, y = indices(len(weights))
    return (
        x[y[0]] ** 2
        + (x[y[-1]] - target * x[t]) ** 2
        + sum((x[zi] + x[wi] - x[t]) ** 2 for zi, wi in zip(z, w))
        + sum((x[y[i + 1]] - x[y[i]] - a * x[z[i]]) ** 2
              for i, a in enumerate(weights))
        + sum(x[zi] * x[wi] for zi, wi in zip(z, w))
    )


def subset_point(weights, bits, scale):
    t, z, w, y = indices(len(weights))
    x = [F(0)] * (3 * len(weights) + 2)
    x[t] = scale
    for i, (a, bit) in enumerate(zip(weights, bits)):
        x[z[i]] = scale * bit
        x[w[i]] = scale * (1 - bit)
        x[y[i + 1]] = x[y[i]] + a * x[z[i]]
    return x


def check_decomposition(matrix, n):
    t, z, w, y = indices(n)
    bags = [{t, y[i], y[i + 1], z[i]} for i in range(n)]
    bags += [{t, z[i], w[i]} for i in range(n)]
    edges = [(i, i + 1) for i in range(n - 1)]
    edges += [(i, n + i) for i in range(n)]
    adjacency = [set() for _ in bags]
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    assert len(edges) == len(bags) - 1
    assert max(map(len, bags)) == 4
    for vertex in range(len(matrix)):
        containing = {i for i, bag in enumerate(bags) if vertex in bag}
        assert containing
        reached = {min(containing)}
        todo = list(reached)
        while todo:
            for neighbor in adjacency[todo.pop()] & containing - reached:
                reached.add(neighbor)
                todo.append(neighbor)
        assert reached == containing
    for i in range(len(matrix)):
        for j in range(i):
            if matrix[i][j]:
                assert any({i, j} <= bag for bag in bags)
    return len(bags)


def check_curvature_shift(matrix, forms, n):
    """Verify an exact Gram decomposition of Hessian(q) + I."""
    size = len(matrix)
    t, z, w, y = indices(n)
    certificate = [[2 * sum(row[i] * row[j] for row in forms)
                    for j in range(size)] for i in range(size)]
    for zi, wi in zip(z, w):
        for i in (zi, wi):
            for j in (zi, wi):
                certificate[i][j] += 1
    for i in [t] + y:
        certificate[i][i] += 1
    assert certificate == [[2 * matrix[i][j] + int(i == j)
                            for j in range(size)] for i in range(size)]


def positive_ldl(matrix):
    """Return and verify an exact positive LDL certificate, with no pivots."""
    size = len(matrix)
    lower = [[F(i == j) for j in range(size)] for i in range(size)]
    diagonal = []
    for j in range(size):
        pivot = matrix[j][j] - sum(lower[j][k] ** 2 * diagonal[k]
                                  for k in range(j))
        assert pivot > 0
        diagonal.append(pivot)
        for i in range(j + 1, size):
            lower[i][j] = (
                matrix[i][j]
                - sum(lower[i][k] * lower[j][k] * diagonal[k]
                      for k in range(j))
            ) / pivot
    assert matrix == [[sum(lower[i][k] * diagonal[k] * lower[j][k]
                           for k in range(size))
                       for j in range(size)] for i in range(size)]
    return diagonal


def main():
    large = (2**20 + 1, 2**20 + 3, 2**21 + 5)
    families = [
        ((1,), range(3)),
        ((2,), range(4)),
        ((3,), range(5)),
        ((2, 3), range(7)),
        ((1, 2, 4), range(9)),
        ((2, 2, 2), range(8)),
        ((3, 7, 11, 13), (0, 1, 10, 14, 21, 34, 35)),
        (large, (0, 1, large[0], large[0] + large[1], sum(large), sum(large) + 1)),
    ]
    rng = Random(26100233)
    instances = bags = expansion_checks = subset_checks = box_witnesses = 0
    yes_instances = no_instances = 0
    for weights, targets in families:
        for target in targets:
            n = len(weights)
            matrix, forms = construction(weights, target)
            instances += 1
            bags += check_decomposition(matrix, n)
            check_curvature_shift(matrix, forms, n)
            for signed in (False, True):
                for _ in range(16):
                    x = [F(rng.randrange(-8 if signed else 0, 9), 8)
                         for _ in matrix]
                    assert quad(matrix, x) == direct_value(weights, target, x)
                    if not signed:
                        assert quad(matrix, x) >= 0
                    expansion_checks += 1
            solutions = []
            for bits in product((0, 1), repeat=n):
                difference = sum(a * b for a, b in zip(weights, bits)) - target
                if not difference:
                    solutions.append(bits)
                for scale in (F(0), F(1, 3), F(1)):
                    x = subset_point(weights, bits, scale)
                    assert quad(matrix, x) == scale**2 * difference**2
                    assert (quad(matrix, x) == 0) == (not scale or not difference)
                    subset_checks += 1
            if solutions:
                yes_instances += 1
                for bits in solutions:
                    scale = F(1, 1 + sum(weights) + target)
                    x = subset_point(weights, bits, scale)
                    assert all(0 <= v <= 1 for v in x) and any(x)
                    assert quad(matrix, x) == 0
                    t, z, w, y = indices(n)
                    assert tuple(x[zi] / x[t] for zi in z) == bits
                    box_witnesses += 1
            else:
                no_instances += 1
            assert direct_value(weights, target, [F(0)] * len(matrix)) == 0

    # An independent, explicit strict-positive certificate for one NO case:
    # weights=(3), target=1. Q-I/100 is positive definite even off the orthant.
    matrix, _ = construction((3,), 1)
    shifted = [[matrix[i][j] - (F(1, 100) if i == j else 0)
                for j in range(5)] for i in range(5)]
    pivots = positive_ldl(shifted)
    assert len(pivots) == 5
    assert [sum(3 * bit for bit in bits) for bits in product((0, 1), repeat=1)] == [0, 3]

    print(
        f"PASS: {instances} constructions ({yes_instances} YES, {no_instances} NO), "
        f"{bags} decomposition bags, {instances} exact PSD Hessian shifts, "
        f"{expansion_checks} expansion checks, {subset_checks} scaled subset checks, "
        f"{box_witnesses} unit-box zero witnesses, one 5-pivot strict-positive LDL certificate"
    )


if __name__ == "__main__":
    main()
