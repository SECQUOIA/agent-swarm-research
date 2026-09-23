"""Check the support reduction against explicit Minkowski sums and SciPy LPs.

This is a small-instance check, not an implementation of quantifier elimination.
Vertex generation and all support/denominator checks use exact rationals.
"""
from itertools import combinations, product
from fractions import Fraction as F
import random
import numpy as np
from scipy.optimize import linprog
import sympy as s


t = s.Symbol("t")
rng = random.Random(20260905)


def rational(expr, value):
    return F(str(expr.subs(t, s.Rational(value.numerator, value.denominator))))


def candidates(B, b):
    result = []
    for rows in combinations(range(B.rows), B.cols):
        basis = B[list(rows), :]
        determinant = s.expand(basis.det())
        if determinant == 0:
            continue
        numerator = basis.adjugate() * b[list(rows), :]
        result.append((determinant, numerator))
    return result


def vertices(B, b, pool, value):
    evaluated_B = [[rational(B[i, j], value) for j in range(B.cols)]
                   for i in range(B.rows)]
    evaluated_b = [rational(b[i], value) for i in range(B.rows)]
    valid = {}
    for determinant, numerator in pool:
        den = rational(determinant, value)
        if not den:
            continue
        num = tuple(rational(e, value) for e in numerator)
        vertex = tuple(a / den for a in num)
        if all(sum(a * x for a, x in zip(row, vertex)) <= rhs
               for row, rhs in zip(evaluated_B, evaluated_b)):
            valid[vertex] = (num, den)
    return valid, evaluated_B, evaluated_b


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull(points):
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    halves = []
    for sequence in [points, list(reversed(points))]:
        half = []
        for point in sequence:
            while len(half) >= 2 and cross(half[-2], half[-1], point) <= 0:
                half.pop()
            half.append(point)
        halves.append(half[:-1])
    return halves[0] + halves[1]


checks = 0
for trial in range(20):
    blocks = []
    for j in range(3):
        # Bounded polytopes. Extra parameter-dependent inequalities sometimes
        # cut them down to faces or make them empty at a tested core point.
        B = s.Matrix([[1, 0], [-1, 0], [0, 1], [0, -1],
                      [1 + t, rng.choice([-1, 1])],
                      [rng.choice([-1, 1]), t]])
        b = s.Matrix([1, 0, 1, 0, rng.choice([0, 1, 2]) + t,
                      rng.choice([0, 1, 2])])
        blocks.append((B, b, candidates(B, b)))
    for value in [F(-1), F(-1, 2), F(0), F(1, 2), F(1)]:
        evaluated = [vertices(*block, value) for block in blocks]
        for valid, B, b in evaluated:
            result = linprog([0, 0], A_ub=np.array(B, dtype=float),
                             b_ub=np.array(b, dtype=float), bounds=[(None, None)] * 2,
                             method="highs")
            assert bool(valid) == result.success
        if any(not valid for valid, _, _ in evaluated):
            continue
        summed = [tuple(sum(v[i] for v in choice) for i in range(2))
                  for choice in product(*(list(e[0]) for e in evaluated))]
        boundary = hull(summed)
        directions = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(-1))]
        if len(boundary) >= 2:
            for a, b in zip(boundary, boundary[1:] + boundary[:1]):
                directions.append((b[1] - a[1], a[0] - b[0]))
        for direction in directions:
            selections = []
            for valid, B, b in evaluated:
                best = max(valid, key=lambda v: dot(direction, v))
                num, den = valid[best]
                selections.append((dot(direction, num), den))
                lp = linprog(-np.array(direction, dtype=float),
                             A_ub=np.array(B, dtype=float), b_ub=np.array(b, dtype=float),
                             bounds=[(None, None)] * 2, method="highs")
                assert abs(-lp.fun - float(dot(direction, best))) < 1e-7
            support = sum(num / den for num, den in selections)
            assert support == max(dot(direction, point) for point in summed)
            H = F(1)
            for _, den in selections:
                H *= den * den
            for target in boundary[:2] + [(F(5), F(5))]:
                direct = dot(direction, target) - support
                cleared = dot(direction, target) * H
                for j, (num, den) in enumerate(selections):
                    others = F(1)
                    for i, (_, d) in enumerate(selections):
                        if i != j:
                            others *= d * d
                    cleared -= num * den * others
                assert cleared == H * direct
                assert (cleared <= 0) == (direct <= 0)
                checks += 1

# A singleton and an empty lower-dimensional block check the active-rank case.
B = s.Matrix([[1, 0], [-1, 0], [0, 1], [0, -1]])
assert list(vertices(B, s.Matrix([0, 0, 0, 0]), candidates(B, s.Matrix([0, 0, 0, 0])), F(0))[0]) == [(F(0), F(0))]
assert not vertices(B, s.Matrix([-1, 0, 0, 0]), candidates(B, s.Matrix([-1, 0, 0, 0])), F(0))[0]
print(f"Passed {checks} exact support/denominator checks, independent LP comparisons, and degeneracy checks.")
