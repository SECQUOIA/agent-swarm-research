"""Certified finite checks of projected-box slices for interaction rank two.

HiGHS proposes corner classifications. Every classification is verified with
exact rational exposing or convex-combination certificates. At rational total
slices, projected vertex-pair candidates are compared with independently
enumerated original margin vertices. This does not test symbolic running-time
bounds or the global stationary-point search over the total.
"""
from fractions import Fraction as F
from itertools import product, combinations
from random import Random

import numpy as np
from scipy.optimize import linprog
import sympy as sp


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def project(x, factors, additive):
    return (sum(x), dot(x, [r[0] for r in factors]),
            dot(x, [r[1] for r in factors]), dot(x, additive))


def projected_vertices(lower, upper, factors, additive, counts):
    corners = {}
    for bits in product((0, 1), repeat=len(lower)):
        x = tuple(upper[i] if bit else lower[i] for i, bit in enumerate(bits))
        corners.setdefault(project(x, factors, additive), x)
    points = list(corners)
    if len(points) == 1:
        counts['singleton_boxes'] += 1
        return [(points[0], corners[points[0]])]
    vertices = []
    for point in points:
        others = [q for q in points if q != point]
        columns = [q+(F(1),) for q in others]
        target = point+(F(1),)
        eq = np.array(columns, dtype=float).T
        trial = linprog(np.zeros(len(others)), A_eq=eq,
                        b_eq=np.array(target, dtype=float),
                        bounds=(0, None), method='highs')
        if trial.success:
            support = [i for i, v in enumerate(trial.x) if v > 1e-8]
            matrix = sp.Matrix.hstack(*(sp.Matrix(columns[i]) for i in support))
            solution, parameters = matrix.gauss_jordan_solve(sp.Matrix(target))
            assert not parameters.rows
            weights = [F(v) for v in solution]
            assert all(w >= 0 for w in weights) and sum(weights) == 1
            assert all(sum(weights[j]*columns[i][k]
                           for j, i in enumerate(support)) == target[k]
                       for k in range(5))
            counts['convex_certificates'] += 1
        else:
            assert trial.status == 2, trial.message
            differences = [[a-b for a, b in zip(q, point)] for q in others]
            separator = linprog(np.zeros(4), A_ub=np.array(differences, dtype=float),
                                b_ub=-np.ones(len(others)),
                                bounds=[(None, None)]*4, method='highs')
            assert separator.success, separator.message
            direction = [F(float(v)).limit_denominator(10**7) for v in separator.x]
            assert all(dot(direction, row) < 0 for row in differences)
            vertices.append((point, corners[point]))
            counts['exposing_certificates'] += 1
    return vertices


def pair_slice(vertices, total, lower, upper, factors, additive):
    candidates = {}
    for point, x in vertices:
        if point[0] == total:
            candidates.setdefault(point, x)
    for (p, x), (q, y) in combinations(vertices, 2):
        if p[0] == q[0]:
            continue
        weight = (total-p[0])/(q[0]-p[0])
        if 0 <= weight <= 1:
            margin = tuple((1-weight)*a+weight*b for a, b in zip(x, y))
            point = tuple((1-weight)*a+weight*b for a, b in zip(p, q))
            assert sum(margin) == total
            assert all(l <= v <= u for l, v, u in zip(lower, margin, upper))
            assert project(margin, factors, additive) == point
            candidates.setdefault(point, margin)
    return list(candidates)


def margin_vertices(lower, upper, total):
    result = set()
    for free in range(len(lower)):
        others = [i for i in range(len(lower)) if i != free]
        for bits in product((0, 1), repeat=len(others)):
            x = list(lower)
            for i, bit in zip(others, bits):
                x[i] = upper[i] if bit else lower[i]
            x[free] = total-sum(x[i] for i in others)
            if lower[free] <= x[free] <= upper[free]:
                result.add(tuple(x))
    return list(result)


def main():
    rng = Random(20260905106)
    counts = dict(instances=0, slices=0, exposing_certificates=0,
                  convex_certificates=0, singleton_boxes=0, zero_slices=0,
                  infeasible=0)
    for case in range(24):
        m, n = 3+case % 3, 3+(case//3) % 2
        while True:
            U = [[F(rng.randrange(-3, 4)) for _ in range(2)] for _ in range(m)]
            V = [[F(rng.randrange(-3, 4)) for _ in range(2)] for _ in range(n)]
            a = [F(rng.randrange(-3, 4)) for _ in range(m)]
            b = [F(rng.randrange(-3, 4)) for _ in range(n)]
            C = [[a[i]+b[j]+dot(U[i], V[j]) for j in range(n)] for i in range(m)]
            D = [[C[i][j]-C[i][0]-C[0][j]+C[0][0]
                  for j in range(n)] for i in range(m)]
            if sp.Matrix(D).rank() == 2:
                break
        lower = [F(rng.randrange(3), 2) for _ in range(m)]
        other_lower = [F(rng.randrange(3), 2) for _ in range(n)]
        upper = [v+F(rng.randrange(4), 2) for v in lower]
        other_upper = [v+F(rng.randrange(4), 2) for v in other_lower]
        if case == 0:
            lower = upper = [F(0)]*m
            other_lower = other_upper = [F(0)]*n
        elif case == 1:
            lower = upper = [F(1)]+[F(0)]*(m-1)
            other_lower = other_upper = [F(1)]+[F(0)]*(n-1)
        elif case == 2:
            # Five moving generators in at most four dimensions force
            # at least one projected corner to be redundant.
            lower, upper = [F(0)]*m, [F(1)]*m
            other_lower, other_upper = [F(0)]*n, [F(1)]*n
        lo, hi = max(sum(lower), sum(other_lower)), min(sum(upper), sum(other_upper))
        counts['instances'] += 1
        if lo > hi:
            counts['infeasible'] += 1
            continue
        X = projected_vertices(lower, upper, U, a, counts)
        Y = projected_vertices(other_lower, other_upper, V, b, counts)
        for total in sorted({lo, hi, (lo+hi)/2, (3*lo+hi)/4, (lo+3*hi)/4}):
            px = pair_slice(X, total, lower, upper, U, a)
            py = pair_slice(Y, total, other_lower, other_upper, V, b)
            mx = margin_vertices(lower, upper, total)
            my = margin_vertices(other_lower, other_upper, total)
            assert px and py and mx and my
            if total == 0:
                assert all(not any(x) for x in mx+my)
                counts['zero_slices'] += 1
            else:
                got = min(x[3]+y[3]+dot(x[1:3], y[1:3])/total for x in px for y in py)
                expected = min(sum(C[i][j]*x[i]*y[j] for i in range(m)
                                   for j in range(n))/total for x in mx for y in my)
                assert got == expected, (case, total, got, expected)
            counts['slices'] += 1
    assert counts['convex_certificates'] and counts['exposing_certificates']
    print('PASS:', counts)
    print('Every hull classification and objective comparison certified with exact rational arithmetic.')
    print('Numerical LP proposes certificates only; no tolerance is an acceptance criterion.')


if __name__ == '__main__':
    main()
