#!/usr/bin/env python3
"""Small exact diagnostics for TU convex recourse, dual charts, and proximity.

All native labels, small minors, dual bases, and unit circuits are enumerated
here as independent diagnostics. This is not a production TU/oracle routine.
"""

from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product


def rank(matrix):
    if not matrix:
        return 0
    work = [[F(x) for x in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(pivot_row, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [x / scale for x in work[pivot_row]]
        for i in range(pivot_row + 1, len(work)):
            scale = work[i][column]
            work[i] = [a - scale * b for a, b in zip(work[i], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


@lru_cache(None)
def inverse(matrix):
    n = len(matrix)
    work = [[F(x) for x in row] + [F(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    determinant = F(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if work[i][j]), None)
        if pivot is None:
            return None
        if pivot != j:
            work[j], work[pivot] = work[pivot], work[j]
            determinant = -determinant
        scale = work[j][j]
        determinant *= scale
        work[j] = [x / scale for x in work[j]]
        for i in range(n):
            if i != j:
                scale = work[i][j]
                work[i] = [a - scale * b for a, b in zip(work[i], work[j])]
    return tuple(tuple(row[n:]) for row in work), determinant


def check_tu(matrix, counts):
    m, r = len(matrix), len(matrix[0]) if matrix else 0
    for size in range(1, min(m, r) + 1):
        for rows in combinations(range(m), size):
            for columns in combinations(range(r), size):
                minor = tuple(tuple(matrix[i][j] for j in columns) for i in rows)
                result = inverse(minor)
                determinant = F(0) if result is None else result[1]
                assert determinant in (-1, 0, 1)
                counts["exact TU minors"] += 1


def matvec(matrix, x):
    return tuple(sum(a * b for a, b in zip(row, x)) for row in matrix)


def polynomial(coefficients, v):
    return coefficients[0] + coefficients[1] * v + coefficients[2] * v * v


def cost(model, v, t):
    a, b, c, d = model
    return a * t * t + (b + c * v + d * v * v) * t


def marginal_chart(model, t):
    a, b, c, d = model
    return (a * (2 * t + 1) + b, c, d)


def feasible_labels(matrix, rhs, bounds):
    return tuple(z for z in product(*(range(lo, hi + 1) for lo, hi in bounds))
                 if matvec(matrix, z) == tuple(rhs))


def preprocess(matrix, rhs, bounds):
    fixed = {i: lo for i, (lo, hi) in enumerate(bounds) if lo == hi}
    remaining = [i for i in range(len(bounds)) if i not in fixed]
    reduced = [tuple(row[i] for i in remaining) for row in matrix]
    adjusted = [b - sum(row[i] * value for i, value in fixed.items())
                for row, b in zip(matrix, rhs)]
    if rank([row + (b,) for row, b in zip(reduced, adjusted)]) > rank(reduced):
        raise ValueError("inconsistent dependent equality")
    selected, selected_rhs = [], []
    for row, b in zip(reduced, adjusted):
        if rank(selected + [row]) > len(selected):
            selected.append(row)
            selected_rhs.append(b)
    return tuple(selected), tuple(selected_rhs), tuple(bounds[i] for i in remaining), remaining, fixed


def unit_circuits(matrix, r):
    circuits = []
    for x in product((-1, 0, 1), repeat=r):
        support = [i for i, value in enumerate(x) if value]
        if not support or any(matvec(matrix, x)):
            continue
        restricted = [tuple(row[i] for i in support) for row in matrix]
        if rank(restricted) == len(support) - 1:
            circuits.append(x)
    return tuple(circuits)


def interval_violation(z, intervals):
    return sum(max(lo - t, 0, t - hi) for t, (lo, hi) in zip(z, intervals))


def check_proximity(labels, tight, intervals, circuits, counts):
    r = len(intervals)
    for z in labels:
        distance, nearest = min((sum(abs(a - b) for a, b in zip(z, y)), y) for y in tight)
        violation = interval_violation(z, intervals)
        assert distance <= r * violation
        counts["nearest-tight-label inequalities"] += 1
        difference = [a - b for a, b in zip(z, nearest)]
        reconstructed = [0] * r
        charges = [0] * r
        while any(difference):
            candidates = [c for c in circuits if all(not value or value * difference[i] > 0
                                                      for i, value in enumerate(c))]
            assert candidates
            circuit = candidates[0]
            multiple = min(abs(difference[i]) for i, value in enumerate(circuit) if value)
            assert sum(abs(value) for value in circuit) <= r
            blockers = [i for i, (lo, hi) in enumerate(intervals)
                        if not lo <= nearest[i] + circuit[i] <= hi]
            assert blockers
            blocker = blockers[0]
            lo, hi = intervals[blocker]
            assert abs(z[blocker] - nearest[blocker]) == max(lo - z[blocker], 0, z[blocker] - hi)
            charges[blocker] += multiple
            for i, value in enumerate(circuit):
                difference[i] -= multiple * value
                reconstructed[i] += multiple * value
            counts["conformal circuit steps"] += 1
        assert tuple(reconstructed) == tuple(a - b for a, b in zip(z, nearest))
        assert all(charge <= max(lo - t, 0, t - hi)
                   for charge, t, (lo, hi) in zip(charges, z, intervals))


def dual_constraints(matrix, bounds, models, z0):
    constraints = []
    for i, ((lo, hi), model, z) in enumerate(zip(bounds, models, z0)):
        column = tuple(row[i] for row in matrix)
        if z > lo:
            constraints.append((tuple(-a for a in column), tuple(-a for a in marginal_chart(model, z - 1)), "native"))
        if z < hi:
            constraints.append((column, marginal_chart(model, z), "native"))
    return constraints


def vertices(constraints, m, query, counts):
    answer = {}
    for basis in combinations(range(len(constraints)), m):
        matrix = tuple(constraints[i][0] for i in basis)
        result = inverse(matrix)
        if result is None:
            continue
        inv, determinant = result
        assert determinant in (-1, 1)
        assert all(value in (-1, 0, 1) for row in inv for value in row)
        chart = tuple(tuple(sum(inv[i][j] * constraints[basis[j]][1][degree] for j in range(m))
                            for degree in range(3)) for i in range(m))
        point = tuple(polynomial(row, query) for row in chart)
        if all(sum(a * x for a, x in zip(normal, point)) <= polynomial(rhs, query)
               for normal, rhs, _ in constraints):
            counts["feasible nonsingular dual bases"] += 1
            answer.setdefault(point, (basis, chart))
    return answer


def run_model(name, matrix, rhs, bounds, models, counts):
    m, r = len(matrix), len(bounds)
    assert rank(matrix) == m
    assert all(lo < hi for lo, hi in bounds)
    assert all(model[0] >= 0 for model in models)
    labels = feasible_labels(matrix, rhs, bounds)
    assert labels
    circuits = unit_circuits(matrix, r)
    counts["enumerated signed unit circuits"] += len(circuits)
    V = max([F(1)] + [sum(abs(a) for a in marginal_chart(model, t))
                      for model, (lo, hi) in zip(models, bounds) for t in range(lo, hi)])
    radius = m * V + 1
    for query in (F(0), F(1, 3), F(1, 2), F(1)):
        objective = {z: sum(cost(model, query, t) for model, t in zip(models, z)) for z in labels}
        minimum = min(objective.values())
        optimum = tuple(z for z in labels if objective[z] == minimum)
        z0 = optimum[0]
        constraints = dual_constraints(matrix, bounds, models, z0)
        counts["endpoint-only scalar slope systems"] += sum(z in (lo, hi) for z, (lo, hi) in zip(z0, bounds))
        unbounded_vertices = vertices(constraints, m, query, counts)
        assert unbounded_vertices
        assert all(all(abs(x) <= m * V for x in point) for point in unbounded_vertices)
        counts["compact dual vertices"] += len(unbounded_vertices)
        bounded = list(constraints)
        for i in range(m):
            for sign in (-1, 1):
                bounded.append((tuple(F(sign if j == i else 0) for j in range(m)), (radius, F(0), F(0)), "box"))
        bounded_vertices = vertices(bounded, m, query, counts)
        assert bounded_vertices
        selected = min(bounded_vertices)
        assert all(abs(x) <= radius for x in selected)
        selected_basis = bounded_vertices[selected][0]
        if any(bounded[i][2] == "box" for i in selected_basis):
            counts["selected multiplier-box-active bases"] += 1
        counts["bounded dual vertices"] += len(bounded_vertices)
        for multiplier, (basis, chart) in bounded_vertices.items():
            intervals = []
            adjusted_coefficients = tuple(sum(matrix[j][i] * multiplier[j] for j in range(m)) for i in range(r))
            for i, ((lo, hi), model) in enumerate(zip(bounds, models)):
                adjusted = {t: cost(model, query, t) - adjusted_coefficients[i] * t for t in range(lo, hi + 1)}
                scalar_minimum = min(adjusted.values())
                winners = [t for t in range(lo, hi + 1) if adjusted[t] == scalar_minimum]
                assert winners == list(range(winners[0], winners[-1] + 1))
                assert z0[i] in winners
                intervals.append((winners[0], winners[-1]))
            tight = tuple(z for z in labels if interval_violation(z, intervals) == 0)
            assert tight == optimum
            counts["optimal-interval set equalities"] += 1
            check_proximity(labels, tight, intervals, circuits, counts)
            assert tuple(polynomial(row, query) for row in chart) == multiplier
            if all(model[3] == 0 for model in models):
                assert all(row[2] == 0 for row in chart)
            elif any(row[2] for row in chart):
                counts["genuinely quadratic basis charts"] += 1
            for probe in (F(0), F(1, 5), F(3, 4), F(1)):
                point = tuple(polynomial(row, probe) for row in chart)
                for index in basis:
                    normal, rhs_chart, _ = bounded[index]
                    assert sum(a * x for a, x in zip(normal, point)) == polynomial(rhs_chart, probe)
                for i, ((lo, hi), model) in enumerate(zip(bounds, models)):
                    for t in range(lo, hi):
                        adjusted_chart = tuple(marginal_chart(model, t)[degree]
                                               - sum(matrix[j][i] * chart[j][degree] for j in range(m))
                                               for degree in range(3))
                        direct = cost(model, probe, t + 1) - cost(model, probe, t)
                        direct -= sum(matrix[j][i] * point[j] for j in range(m))
                        assert polynomial(adjusted_chart, probe) == direct
                        counts["symbolic adjusted-marginal evaluations"] += 1
                if any(sum(a * x for a, x in zip(normal, point)) > polynomial(rhs_chart, probe)
                       for normal, rhs_chart, _ in bounded):
                    counts["charts infeasible away from their query"] += 1
        if len(optimum) > 1:
            counts["queries with persistent optimal ties"] += 1
        counts["exact recourse queries"] += 1
    if name == "endpoint poly chart":
        assert selected == tuple(-radius for _ in range(m))
    counts["cost-system fixtures"] += 1


def main():
    counts = Counter()
    interval = ((1, 0, 0, 1, 0, 1), (0, 1, 0, 1, 1, 1), (0, 0, 1, 0, 1, 1))
    bounds = ((0, 2),) * 6
    assert any(sum(bool(row[i]) for row in interval) == 3 for i in range(6))
    row_signs, column_signs = (-1, 1, -1), (1, -1, 1, -1, 1, -1)
    signed = tuple(tuple(row_signs[i] * a * column_signs[j] for j, a in enumerate(row))
                   for i, row in enumerate(interval))
    signed_bounds = tuple((0, 2) if sign == 1 else (-2, 0) for sign in column_signs)
    raw = tuple(row + (row[3],) for row in interval)
    raw += (raw[0],)
    raw_rhs, raw_bounds = (3, 3, 2, 3), bounds + ((1, 1),)
    for matrix in (interval, signed, raw):
        check_tu(matrix, counts)
    reduced, rhs, new_bounds, remaining, fixed = preprocess(raw, raw_rhs, raw_bounds)
    assert reduced == interval and rhs == (2, 2, 2) and new_bounds == bounds
    original_labels = feasible_labels(raw, raw_rhs, raw_bounds)
    reduced_labels = feasible_labels(reduced, rhs, new_bounds)
    assert tuple(tuple(z[i] for i in remaining) for z in original_labels) == reduced_labels
    assert fixed == {6: 1}
    counts["preprocessed feasible-label correspondences"] += len(original_labels)
    try:
        preprocess(raw, (3, 3, 2, 4), raw_bounds)
    except ValueError:
        counts["inconsistent redundant-row guards"] += 1
    else:
        raise AssertionError("inconsistent duplicate equality accepted")

    base_lambda, slope_lambda = (F(1, 3), F(-2, 5), F(1, 7)), (F(1, 2), F(0), F(-1, 3))
    linear = tuple((F(0), sum(interval[j][i] * base_lambda[j] for j in range(3)),
                    sum(interval[j][i] * slope_lambda[j] for j in range(3)), F(0)) for i in range(6))
    run_model("affine persistent ties", interval, (2, 2, 2), bounds, linear, counts)
    tie_quadratics = ((F(1), F(-1), F(0), F(0)),) * 6
    run_model("quadratic native ties", interval, (2, 2, 2), bounds, tie_quadratics, counts)
    reference = (1, 0, 1, 1, 1, 0)
    quadratic = tuple((F(1), F(-2 * reference[i]), F(i - 2, 3), F((-1)**i, 5)) for i in range(6))
    run_model("quadratic core charts", interval, (2, 2, 2), bounds, quadratic, counts)
    signed_models = tuple((a, b * sign, c * sign, d * sign)
                          for (a, b, c, d), sign in zip(quadratic, column_signs))
    run_model("signed interval matrix", signed, tuple(2 * sign for sign in row_signs),
              signed_bounds, signed_models, counts)
    endpoint_models = ((F(0), F(1), F(1), F(1)),) * 6
    run_model("endpoint poly chart", interval, (0, 0, 0), bounds, endpoint_models, counts)
    run_model("rank-zero scalar recourse", (), (), ((0, 2), (0, 2)),
              ((F(1), F(-1), F(0), F(0)), (F(0), F(0), F(0), F(0))), counts)
    assert counts["selected multiplier-box-active bases"] > 0
    assert counts["genuinely quadratic basis charts"] > 0
    assert counts["conformal circuit steps"] > 0
    assert counts["charts infeasible away from their query"] > 0
    print("PASS: " + "; ".join(f"{value} {name}" for name, value in counts.items()))
    print("Scope: small enumerated TU systems, native labels, dual bases and circuits; no production convex oracle, TU recognizer, interval binary search, or large-domain complexity test.")


if __name__ == "__main__":
    main()
