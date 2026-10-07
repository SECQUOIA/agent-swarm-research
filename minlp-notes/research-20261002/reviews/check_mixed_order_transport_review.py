#!/usr/bin/env python3
"""Exact reviewer checks of mixed-order transport and certificate boundaries."""

from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


def feasible(point, edges):
    return all(0 <= x <= 1 for x in point) and all(
        point[i] <= point[j] for i, j in edges)


def same_closed_face(source, target):
    for x, y in zip(source, target):
        if x in [0, 1] and y != x:
            return False
    for i, x in enumerate(source):
        for j, y in enumerate(source):
            if x == y and target[i] != target[j]:
                return False
            if x < y and target[i] > target[j]:
                return False
    return True


def transport(point, target, bag=(0, 1)):
    source = tuple(point[i] for i in bag)
    assert same_closed_face(source, target)
    knots = [Q(0)]+sorted({x for x in source if 0 < x < 1})+[Q(1)]
    affine_knots = []
    for knot in knots:
        coefficients = [Q(0)]*len(bag)
        constant = Q(0)
        if knot == 1:
            constant = Q(1)
        elif knot != 0:
            coefficients[source.index(knot)] = Q(1)
        affine_knots.append((constant, coefficients))
    rows, images = [], []
    for x in point:
        i = next(k for k in range(len(knots)-1) if knots[k] <= x <= knots[k+1])
        weight = (x-knots[i])/(knots[i+1]-knots[i])
        left_constant, left_row = affine_knots[i]
        right_constant, right_row = affine_knots[i+1]
        row = [(1-weight)*a+weight*b for a, b in zip(left_row, right_row)]
        constant = (1-weight)*left_constant+weight*right_constant
        rows.append(row)
        images.append(constant+sum(a*b for a, b in zip(row, target)))
    assert tuple(images[i] for i in bag) == target
    assert all(all(value >= 0 for value in row) and sum(row) <= 1 for row in rows)
    return tuple(images), rows


def objective(x):
    # Absolute Hessian row sums are at most 6, so Hess F <=6I.
    # The Hessian is indefinite; the linear perturbation has all entries nonzero.
    a, b, c, z = x
    return (a*a+(b-a)**2/2+2*a*c-3*b*c
            +Q(2, 7)*a-Q(3, 5)*b+Q(4, 11)*c+Q(9, 13)*z)


def propagated_repair(raw, exact, edges, binaries):
    n = len(raw)
    reach = [[i == j or (i, j) in edges for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] |= reach[i][k] and reach[k][j]
    bounds = [(exact[i], exact[i]) if i in binaries else (Q(0), Q(1))
              for i in range(n)]
    lower = [max(bounds[k][0] for k in range(n) if reach[k][i]) for i in range(n)]
    upper = [min(bounds[k][1] for k in range(n) if reach[i][k]) for i in range(n)]
    clipped = [min(hi, max(lo, value)) for value, lo, hi in zip(raw, lower, upper)]
    return tuple(max(clipped[k] for k in range(n) if reach[k][i]) for i in range(n))


def main():
    grid = [Q(i, 4) for i in range(5)]
    graphs = [
        [(0, 2), (2, 3), (3, 1)],
        [(0, 2), (0, 3), (3, 1)],
        [(0, 2), (2, 0), (0, 3), (3, 1)],
    ]
    counts = {'feasible_sources': 0, 'endpoint_transports': 0,
              'two_sided_directions': 0, 'feasible_repairs': 0}
    h, continuous_count, H = Q(1, 4), 3, Q(6)
    for edges in graphs:
        for point in product(grid, grid, grid, [Q(0), Q(1)]):
            if not feasible(point, edges):
                continue
            counts['feasible_sources'] += 1
            source = point[:2]
            for target in product(grid, repeat=2):
                if not same_closed_face(source, target):
                    continue
                moved, rows = transport(point, target)
                assert feasible(moved, edges) and moved[3] == point[3]
                assert all(value == 0 for value in rows[3])
                counts['endpoint_transports'] += 1
            # Each free equal-coordinate group gives one disjoint 0/1 face
            # direction. Its +/-h targets may merge groups or hit endpoints.
            for level in sorted({v for v in source if 0 < v < 1}):
                direction = tuple(Q(v == level) for v in source)
                plus = tuple(v+h*d for v, d in zip(source, direction))
                minus = tuple(v-h*d for v, d in zip(source, direction))
                assert same_closed_face(source, plus) and same_closed_face(source, minus)
                moved_plus, jacobian = transport(point, plus)
                moved_minus, same_jacobian = transport(point, minus)
                assert jacobian == same_jacobian
                derivative = [sum(a*b for a, b in zip(row, direction)) for row in jacobian]
                assert all(0 <= value <= 1 for value in derivative) and derivative[3] == 0
                assert sum(value*value for value in derivative) <= continuous_count
                central = objective(moved_plus)+objective(moved_minus)-2*objective(point)
                assert central <= continuous_count*H*h*h
                counts['two_sided_directions'] += 1

    # Mixed projection need not be convex: v<=binary z<=w projects to
    # {v=0} union {w=1} inside v<=w. Its feasible midpoint can be absent.
    def projected(v, w):
        return any(v <= z <= w for z in [Q(0), Q(1)])
    assert projected(Q(0), Q(0)) and projected(Q(1), Q(1))
    assert not projected(Q(1, 2), Q(1, 2))

    # Premature LP exposure on the continuous relaxation is unsound even
    # for a convex quadratic with mixed point growth g=1.
    # Domain: 0<=x<=z<=1, z binary. F=(x-1/2)^2+10z^2-11z.
    optimum = (Q(1, 2), Q(1))
    def fixture_value(point):
        x, z = point
        return (x-Q(1, 2))**2+10*z*z-11*z
    optimum_value = fixture_value(optimum)
    assert optimum_value == -1 and fixture_value((Q(0), Q(0))) == Q(1, 4)
    for x, z in product(grid, [Q(0), Q(1)]):
        if x <= z:
            assert fixture_value((x, z))-optimum_value >= (
                (x-optimum[0])**2+(z-optimum[1])**2)
    gradient = (Q(0), Q(9))
    vertices = [(Q(0), Q(0)), (Q(0), Q(1)), (Q(1), Q(1))]
    linear_min = min(sum(a*b for a, b in zip(gradient, vertex)) for vertex in vertices)
    wrong_gap = gradient[1]-linear_min
    assert wrong_gap == 9 and optimum[0] != optimum[1]
    # Once z=1 is fixed, the continuous gradient is zero and neither
    # opposite-endpoint test has a positive gap.
    assert max(gradient[0]*x for x in [0, 1])-min(gradient[0]*x for x in [0, 1]) == 0

    # Exact binary values must be propagated before predecessor-max repair.
    edges = [(0, 1), (1, 2)]
    for binary, first, last in product([Q(0), Q(1)], grid, grid):
        exact = (first, binary, last)
        if not feasible(exact, edges):
            continue
        for first_error, last_error in product([Q(-1, 100), Q(1, 100)], repeat=2):
            raw = (first+first_error, binary, last+last_error)
            repaired = propagated_repair(raw, exact, edges, {1})
            assert repaired[1] == binary and feasible(repaired, edges)
            assert max(abs(a-b) for a, b in zip(repaired, exact)) <= max(
                abs(a-b) for a, b in zip(raw, exact))
            counts['feasible_repairs'] += 1
    assert max(Q(1, 100), Q(0)) != 0  # the unpropagated binary-zero failure

    report = {'status': 'passed', 'scope': 'finite exact reviewer diagnostics',
              'counts': counts, 'premature_relaxation_gap': str(wrong_gap),
              'nonconvex_projection_checked': True}
    Path(__file__).with_name('mixed-order-transport-review-results.json').write_text(
        json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
