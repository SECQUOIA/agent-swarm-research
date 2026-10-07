#!/usr/bin/env python3
"""Targeted exact checks for the box-preordering growth obstruction.

These checks validate the finite algebraic witnesses and multiplier
coefficients. The all-degree local-jet argument is a proof in the note,
not something a finite sample can establish.
"""

from fractions import Fraction as F
from itertools import product
from math import factorial


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, length - 1):
                yield (first,) + tail


def determinant(matrix):
    a = [list(row) for row in matrix]
    result = F(1)
    for i in range(len(a)):
        if not a[i][i]:
            pivot = next(j for j in range(i + 1, len(a)) if a[j][i])
            a[i], a[pivot] = a[pivot], a[i]
            result = -result
        pivot = a[i][i]
        result *= pivot
        for j in range(i + 1, len(a)):
            ratio = a[j][i] / pivot
            for k in range(i + 1, len(a)):
                a[j][k] -= ratio * a[i][k]
    return result


def quad(matrix, x):
    return sum(matrix[i][j] * x[i] * x[j]
               for i in range(len(x)) for j in range(len(x)))


def edge(i, j):
    return (i - j) % 5 in (1, 4)


Q = [[F(6, 5) if i == j else F(-1 if edge(i, j) else 1)
      for j in range(5)] for i in range(5)]
W = [[F(13, 8) if i == j else F(int(edge(i, j)))
      for j in range(5)] for i in range(5)]

minors = [determinant([row[:k] for row in W[:k]])
          for k in range(1, 6)]
assert minors == [F(13, 8), F(105, 64), F(533, 512),
                  F(209, 4096), F(29, 32768)]
assert all(value > 0 for value in minors)
assert all(value >= 0 for row in W for value in row)
assert sum(Q[i][j] * W[i][j]
           for i in range(5) for j in range(5)) == F(-1, 4)
assert quad(Q, (1, 1, 0, 0, 0)) == F(2, 5)
assert quad(Q, (1, 1, -1, -1, 0)) < 0

# Connected block chains: exact growth equality, Hessian diagonal,
# and every single-block restriction's non-SPN separator.
chain_restrictions = 0
for blocks in range(1, 9):
    edge_vector = (F(1, 2), F(1, 2), F(0), F(0), F(0))
    objective = blocks * quad(Q, edge_vector)
    squared_norm = blocks * sum(v * v for v in edge_vector)
    assert objective == squared_norm / 5
    for block in range(blocks):
        neighbors = int(block > 0) + int(block < blocks - 1)
        diagonal = 2 * (F(6, 5) + F(neighbors, 100))
        assert diagonal <= F(61, 25)
        separator = F(-1, 4) + F(neighbors, 100) * W[0][0]
        assert separator <= F(-87, 400) < 0
        assert quad(Q, (1, 1, -1, -1, 0)) + F(neighbors, 100) < 0
        chain_restrictions += 1

# Exact growth, cycle identity, and the connected flat-set extension.
growth_cases = 0
flat_cases = 0
grid = [F(0), F(1, 4), F(1, 2), F(1)]
for x in product(grid, repeat=5):
    q = quad(Q, x)
    norm = sum(t * t for t in x)
    horn = sum(x) ** 2 - 4 * sum(x[i] * x[(i + 1) % 5]
                               for i in range(5))
    assert q == horn + norm / 5
    assert horn >= 0 and q >= norm / 5
    assert (q == 0) == (norm == 0)
    growth_cases += 1
    for y, z in product((F(0), F(1, 2), F(1)), repeat=2):
        residual = x[0] - y + z
        value = q + residual ** 2
        dist_sq = norm + (y - z) ** 2 / 2
        assert dist_sq <= 2 * norm + residual ** 2 <= 10 * value
        assert (value == 0) == (norm == 0 and y == z)
        flat_cases += 1

# Enumerate EVERY coefficient of the claimed degree-30 multiplier.
# 5Q has integral entries, so the sign numerator is checked integrally.
Q5 = [[int(5 * value) for value in row] for row in Q]
multiplier_cases = 0
minimum_numerator = None
for a in compositions(30, 5):
    numerator = quad(Q5, a) - 6 * 30
    assert numerator >= 0
    if minimum_numerator is None or numerator < minimum_numerator:
        minimum_numerator = numerator
    multiplier_cases += 1
assert multiplier_cases == 46376

# Independently expand s^(d-2)q at small degrees and compare the exact
# multinomial coefficient formula used for the degree bound.
coefficient_cases = 0
for degree in range(2, 9):
    expansion = {}
    for b in compositions(degree - 2, 5):
        multinomial = factorial(degree - 2)
        for value in b:
            multinomial //= factorial(value)
        for i in range(5):
            for j in range(5):
                a = list(b)
                a[i] += 1
                a[j] += 1
                a = tuple(a)
                expansion[a] = expansion.get(a, F(0)) + multinomial * Q[i][j]
    for a in compositions(degree, 5):
        multinomial = factorial(degree)
        denominator = 1
        for value in a:
            denominator *= factorial(value)
        multinomial //= denominator
        formula = F(multinomial, degree * (degree - 1)) * (
            quad(Q, a) - sum(Q[i][i] * a[i] for i in range(5)))
        assert expansion[a] == formula
        coefficient_cases += 1

print(f"PASS: {len(minors)} rational principal minors and the negative separator")
print(f"PASS: 8 connected block chains and {chain_restrictions} restrictions")
print(f"PASS: {growth_cases} growth identities; {flat_cases} connected-flat cases")
print(f"PASS: all {multiplier_cases} degree-30 coefficients nonnegative; "
      f"minimum integral sign numerator {minimum_numerator}")
print(f"PASS: {coefficient_cases} independently expanded coefficient identities")
