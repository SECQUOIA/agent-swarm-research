#!/usr/bin/env python3
"""Exact checks for conditional-moment-gap.md; uses only the standard library."""

from fractions import Fraction as Q
from itertools import product
import json
import random


ZERO = (0, 0, 0, 0)


def scalar(value):
    return {ZERO: Q(value)} if value else {}


def variable(index):
    exponent = [0] * 4
    exponent[index] = 1
    return {tuple(exponent): Q(1)}


def add(*terms):
    result = {}
    for term in terms:
        for powers, coefficient in term.items():
            result[powers] = result.get(powers, Q(0)) + coefficient
    return {powers: value for powers, value in result.items() if value}


def scale(value, term):
    return {powers: Q(value) * coefficient for powers, coefficient in term.items()}


def multiply(left, right):
    result = {}
    for a, ca in left.items():
        for b, cb in right.items():
            powers = tuple(x + y for x, y in zip(a, b))
            result[powers] = result.get(powers, Q(0)) + ca * cb
    return {powers: value for powers, value in result.items() if value}


def square(term):
    return multiply(term, term)


def evaluate(poly, point):
    return sum(
        coefficient * prod(value**power for value, power in zip(point, powers))
        for powers, coefficient in poly.items()
    )


def prod(values):
    result = Q(1)
    for value in values:
        result *= value
    return result


def outer(left, right):
    return [[x * y for y in right] for x in left]


def moments(measure):
    dimension = len(measure[0][1])
    mean = [sum(weight * point[i] for weight, point in measure) for i in range(dimension)]
    second = [
        [sum(weight * point[i] * point[j] for weight, point in measure) for j in range(dimension)]
        for i in range(dimension)
    ]
    assert sum(weight for weight, _ in measure) == 1
    return mean, second


def hessian(poly):
    result = [[Q(0) for _ in range(4)] for _ in range(4)]
    for powers, coefficient in poly.items():
        assert sum(powers) <= 2
        if sum(powers) != 2:
            continue
        indices = [i for i, power in enumerate(powers) for _ in range(power)]
        i, j = indices
        result[i][j] += coefficient * (2 if i == j else 1)
        if i != j:
            result[j][i] += coefficient
    return result


def lifted_value(poly, mean, second):
    result = Q(0)
    for powers, coefficient in poly.items():
        indices = [i for i, power in enumerate(powers) for _ in range(power)]
        if not indices:
            value = Q(1)
        elif len(indices) == 1:
            value = mean[indices[0]]
        else:
            assert len(indices) == 2
            value = second[indices[0]][indices[1]]
        result += coefficient * value
    return result


def run():
    s, u1, u2, v = [variable(i) for i in range(4)]
    one = scalar(1)
    controls = [u1, u2, v]
    tau = Q(1, 16)
    randomizer = random.Random(20261002)
    records = []
    rational_points = 0
    rlt_checks = 0
    for exponent in [1, 2, 3, 4, 5, 6, 7, 8, 16, 64, 256]:
        h = Q(1, 2**exponent)
        t = scale(1 / h, s)
        residual_left = add(t, scale(-Q(1, 2), add(u1, u2)))
        residual_right = add(t, scalar(-Q(1, 4)), scale(-Q(1, 2), v))
        objective = add(
            scale(8, square(residual_left)),
            scale(8, square(residual_right)),
            *(multiply(control, add(one, scale(-1, control))) for control in controls),
            scale(tau, add(*controls)),
        )
        delta = add(t, scalar(-Q(1, 8)), scale(-Q(1, 4), add(*controls)))
        nonnegative = add(
            multiply(add(one, scale(-1, v)), multiply(u1, u2)),
            multiply(v, multiply(add(one, scale(-1, u1)), add(one, scale(-1, u2)))),
        )
        identity = add(scalar(Q(1, 4)), scale(16, square(delta)), scale(2, nonnegative), scale(tau, add(*controls)))
        assert objective == identity
        optimum = [h / 8, Q(0), Q(0), Q(0)]
        assert evaluate(objective, optimum) == Q(1, 4)

        # Separate interior points, boundary points, and the far s=1 face.
        points = [[Q(randomizer.randrange(65), 64) for _ in range(4)] for _ in range(100)]
        points += [[h * Q(randomizer.randrange(65), 64)] + [Q(randomizer.randrange(65), 64) for _ in range(3)] for _ in range(100)]
        points += [[Q(a), Q(b), Q(c), Q(d)] for a, b, c, d in product([0, 1], repeat=4)]
        points += [[h * (Q(1, 8) + sum(w) / 4)] + list(w) for w in product([Q(0), Q(1, 2), Q(1)], repeat=3)]
        for point in points:
            gap = evaluate(objective, point) - Q(1, 4)
            distance = sum((x - y) ** 2 for x, y in zip(point, optimum))
            assert gap >= distance / 22
            assert gap > 0 or point == optimum
            rational_points += 1

        matrix = hessian(objective)
        r1 = [1 / h, -Q(1, 2), -Q(1, 2), Q(0)]
        r2 = [1 / h, Q(0), Q(0), -Q(1, 2)]
        for i, j in product(range(4), repeat=2):
            assert matrix[i][j] == 16 * (r1[i] * r1[j] + r2[i] * r2[j]) - (2 if i == j and i > 0 else 0)
        negative_vector = [Q(0), Q(1), Q(-1), Q(0)]
        assert [sum(matrix[i][j] * negative_vector[j] for j in range(4)) for i in range(4)] == [-2 * entry for entry in negative_vector]
        assert max(matrix[i][i] for i in range(4)) == 32 / h**2

        left = [
            (Q(1, 8), [Q(0), Q(0), Q(0)]),
            (Q(3, 8), [h / 2, Q(1), Q(0)]),
            (Q(3, 8), [h / 2, Q(0), Q(1)]),
            (Q(1, 8), [h, Q(1), Q(1)]),
        ]
        right = [(Q(1, 2), [h / 4, Q(0)]), (Q(1, 2), [3 * h / 4, Q(1)])]
        left_mean, left_second = moments(left)
        right_mean, right_second = moments(right)
        for degree in range(4):
            assert sum(weight * point[0] ** degree for weight, point in left) == sum(weight * point[0] ** degree for weight, point in right)
        assert sum(weight * point[0] ** 4 for weight, point in left) == Q(11, 64) * h**4
        assert sum(weight * point[0] ** 4 for weight, point in right) == Q(41, 256) * h**4

        for _, point in left:
            assert 0 <= point[0] < 2 * h
            assert point[0] / h == (point[1] + point[2]) / 2
            assert all(x in [0, 1] for x in point[1:])
        for _, point in right:
            assert 0 <= point[0] < 2 * h
            assert point[0] / h == Q(1, 4) + point[1] / 2
            assert point[1] in [0, 1]

        mean = [h / 2, Q(1, 2), Q(1, 2), Q(1, 2)]
        a, b = [h, Q(1), Q(1), Q(2)], [Q(0), Q(1), Q(-1), Q(0)]
        covariance = [[a[i] * a[j] / 16 + 3 * b[i] * b[j] / 16 for j in range(4)] for i in range(4)]
        second = [[mean[i] * mean[j] + covariance[i][j] for j in range(4)] for i in range(4)]
        for indices, bag_mean, bag_second in [([0, 1, 2], left_mean, left_second), ([0, 3], right_mean, right_second)]:
            assert [mean[i] for i in indices] == bag_mean
            assert [[second[i][j] for j in indices] for i in indices] == bag_second
        upper = [2 * h, Q(1), Q(1), Q(1)]
        for i, j in product(range(4), repeat=2):
            assert second[i][j] >= 0
            assert second[i][j] >= upper[i] * mean[j] + upper[j] * mean[i] - upper[i] * upper[j]
            assert second[i][j] <= upper[i] * mean[j]
            assert second[i][j] <= upper[j] * mean[i]
            rlt_checks += 4
        assert lifted_value(square(residual_left), mean, second) == 0
        assert lifted_value(square(residual_right), mean, second) == 0
        assert lifted_value(objective, mean, second) == Q(3, 32)
        assert Q(1, 4) - lifted_value(objective, mean, second) == Q(5, 32)
        assert lifted_value(nonnegative, mean, second) == -Q(1, 8)
        assert sum(covariance[i][i] for i in range(4)) == Q(3, 4) + h**2 / 16
        # Equation (1) remains valid; small within-cell width cannot replace its trace.
        assert lifted_value(objective, mean, second) >= evaluate(objective, mean) - sum(covariance[i][i] for i in range(4))
        records.append({
            "h_exponent": exponent,
            "optimum": "1/4",
            "local_measure_value": "3/32",
            "gap": "5/32",
            "negative_curvature": "2",
            "valid_growth": "1/22",
            "gap_over_nu_sum_widths_squared": str(Q(5, 32) / (32 * h**2)),
        })

    return {
        "status": "passed",
        "family_parameters": len(records),
        "symbolic_polynomial_identities": len(records),
        "exact_growth_point_checks": rational_points,
        "global_mccormick_inequality_checks": rlt_checks,
        "moment_orders_matched": [0, 1, 2, 3],
        "scope": "Exact finite diagnostics plus symbolic identities; not a general solver or complexity lower bound.",
        "records": records,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
