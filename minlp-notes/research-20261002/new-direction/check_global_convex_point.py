"""Exact fixtures for interpolation, rational gradient rows, and global Jensen.

This checks the new proof ingredients, not a general convex optimizer.
Run from the repository root with python3 -B.
"""

from fractions import Fraction as F
from itertools import product
from math import comb, prod


def evaluate(coefficients, argument):
    return sum(c * argument**i for i, c in enumerate(coefficients))


def multiply(left, right):
    result = [F(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def rank(rows):
    matrix = [[F(x) for x in row] for row in rows]
    pivot = 0
    for column in range(len(matrix[0])):
        chosen = next((i for i in range(pivot, len(matrix))
                       if matrix[i][column]), None)
        if chosen is None:
            continue
        matrix[pivot], matrix[chosen] = matrix[chosen], matrix[pivot]
        divisor = matrix[pivot][column]
        matrix[pivot] = [x / divisor for x in matrix[pivot]]
        for i in range(pivot + 1, len(matrix)):
            factor = matrix[i][column]
            matrix[i] = [x - factor * y
                         for x, y in zip(matrix[i], matrix[pivot])]
        pivot += 1
    return pivot


counts = dict(interpolation=0, derivative=0, unisolvent_entries=0,
              extrapolation=0, jensen=0, row_bounds=0, zero_gap=0)
for degree in range(2, 6):
    nodes = [F(j, degree) for j in range(degree + 1)]
    constant = (degree + 1) * degree**degree
    derivative_constant = (degree + 1) * degree**(degree + 1)
    basis = []
    for j, node in enumerate(nodes):
        polynomial, denominator = [F(1)], F(1)
        for i, other in enumerate(nodes):
            if i != j:
                polynomial = multiply(polynomial, [-other, F(1)])
                denominator *= node - other
        polynomial = [c / denominator for c in polynomial]
        assert abs(polynomial[1]) <= degree**(degree + 1)
        basis.append(polynomial)
    for seed in range(1, 8):
        coefficients = [F((-1)**(seed + i) * (seed + 2 * i), i + 1)
                        for i in range(degree + 1)]
        values = [evaluate(coefficients, node) for node in nodes]
        maximum = max(map(abs, values))
        for argument in [F(-2**20), F(-7, 3), F(0), F(2, 7), F(4), F(2**20)]:
            result = evaluate(coefficients, argument)
            assert result == sum(v * evaluate(b, argument)
                                 for v, b in zip(values, basis))
            assert abs(result) <= constant * (1 + abs(argument))**degree * maximum
            counts['interpolation'] += 1
        for radius in [F(1, 17), F(1), F(2**30)]:
            scaled_values = [evaluate(coefficients, radius * node) for node in nodes]
            derivative = sum(v * b[1] for v, b in zip(scaled_values, basis)) / radius
            bound = sum(abs(c) * radius**i for i, c in enumerate(coefficients))
            assert derivative == coefficients[1]
            assert abs(derivative) <= derivative_constant * bound / radius
            counts['derivative'] += 1
    for dimension in range(1, 4):
        grid = sorted((c for c in product(range(degree), repeat=dimension)
                       if sum(c) <= degree - 1), key=lambda c: (sum(c), c))
        assert len(grid) == comb(dimension + degree - 1, degree - 1)
        for i, node in enumerate(grid):
            for j, alpha in enumerate(grid):
                value = prod(comb(c, a) if c >= a else 0
                             for c, a in zip(node, alpha))
                if j > i:
                    assert value == 0
                if j == i:
                    assert value == 1
                counts['unisolvent_entries'] += 1


def objective(point):
    x, y, z, t = point
    return (x + 2 * y)**4 + (y - z)**2 + t


def bregman(point):
    return objective(point) - point[3]


def gradient(point):
    x, y, z, _ = point
    cubic, residual = 4 * (x + 2 * y)**3, 2 * (y - z)
    return (cubic, 2 * cubic + residual, -residual, F(1))


sample_nodes = [tuple(map(F, c)) for c in product(range(4), repeat=4)
                if sum(c) <= 3]
gradient_rows = [gradient(c) for c in sample_nodes]
assert len(sample_nodes) == 35 and rank(gradient_rows) == 3
kernel = (F(-2), F(1), F(1), F(0))
assert all(sum(a * b for a, b in zip(row, kernel)) == 0 for row in gradient_rows)
degree, constant, derivative_constant = 4, 5 * 4**4, 5 * 4**5
box_radius = 9
value_bound = 81 * box_radius**4 + 4 * box_radius**2 + box_radius
gradient_bound = 324 * box_radius**3 + 8 * box_radius + 1
translated_bound = 2 * value_bound + 2 * gradient_bound * 5
wide_bound = translated_bound + 3**4 * constant
row_constant = 1 + derivative_constant * wide_bound
for scale in [F(1, 4), F(1, 8), F(1, 16)]:
    displacements = [(scale, F(0), F(0), F(0)),
                     (-2 * scale**2, scale**2, F(0), F(0)),
                     (F(0), F(0), F(0), scale**4),
                     (scale - 2 * scale**2, scale**2, scale**2, F(0))]
    for displacement in displacements:
        gap, radius = objective(displacement), 1 / scale
        assert gap == scale**4
        for theta in [F(-2), F(0), F(1, 2), F(1), radius, 2 * radius]:
            argument = tuple(2 * theta * d for d in displacement)
            assert bregman(argument) <= constant * gap * (1 + 2 * abs(theta))**4
            counts['extrapolation'] += 1
        for node, row in zip(sample_nodes, gradient_rows):
            assert abs(sum(a * b for a, b in zip(row, displacement))) <= row_constant * scale
            counts['row_bounds'] += 1
            for theta in [F(0), radius / 4, radius / 2, radius]:
                shifted = tuple(c + theta * d for c, d in zip(node, displacement))
                doubled_node = tuple(2 * c for c in node)
                doubled_line = tuple(2 * theta * d for d in displacement)
                assert 0 <= bregman(shifted) <= (bregman(doubled_node) + bregman(doubled_line)) / 2
                assert bregman(shifted) <= wide_bound
                counts['jensen'] += 1
for node in sample_nodes:
    for theta in [F(-2**20), F(-1), F(0), F(1), F(2**20)]:
        shifted = tuple(c + theta * d for c, d in zip(node, kernel))
        assert bregman(shifted) == bregman(node)
        counts['zero_gap'] += 1
print('PASS:', counts, '; rational gradient rank 3 of 4')
