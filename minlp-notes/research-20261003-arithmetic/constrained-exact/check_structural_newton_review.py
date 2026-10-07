"""Exact checks of the comparison vector and Pang--Han box-QP interface.

These finite checks do not prove the structural Newton complexity theorem.
The random seed and all arithmetic are exact and reproducible.
"""

import random
from itertools import combinations

import sympy as sp


def box_qp(hessian, cost, upper, vector):
    """Transcribe Algorithm I with full principal-system solves."""
    dimension = hessian.rows
    free = []
    lower = list(range(dimension))
    at_upper = []
    pivots = 0

    while True:
        reduced_cost = (
            cost + hessian[:, at_upper] * upper[at_upper, :]
            if at_upper
            else cost.copy()
        )
        reduced_vector = vector.copy()
        if free:
            inverse = hessian.extract(free, free).inv()
            free_cost = inverse * reduced_cost[free, :]
            free_vector = inverse * vector[free, :]
            reduced_cost -= hessian[:, free] * free_cost
            reduced_vector -= hessian[:, free] * free_vector
            for index, coordinate in enumerate(free):
                reduced_cost[coordinate] = free_cost[index]
                reduced_vector[coordinate] = free_vector[index]

        candidates = [(sp.Integer(0), -1)]
        candidates.extend(
            (-reduced_cost[i] / reduced_vector[i], i)
            for i in lower
            if reduced_vector[i] > 0
        )
        candidates.extend(
            (-(upper[i] + reduced_cost[i]) / reduced_vector[i], i)
            for i in free
            if reduced_vector[i] > 0
        )
        parameter, coordinate = max(
            candidates, key=lambda item: (item[0], -item[1])
        )
        if parameter == 0:
            point = sp.zeros(dimension, 1)
            for i in free:
                point[i] = -reduced_cost[i]
            for i in at_upper:
                point[i] = upper[i]
            return point, pivots

        if coordinate in lower:
            lower.remove(coordinate)
            free.append(coordinate)
            free.sort()
        else:
            free.remove(coordinate)
            at_upper.append(coordinate)
            at_upper.sort()
        pivots += 1
        assert pivots <= 2 * dimension


def main():
    rng = random.Random(103)
    qp_cases = 0
    principal_subsets = 0

    for dimension in range(2, 7):
        for _ in range(6):
            lower_factor = sp.eye(dimension)
            for i in range(1, dimension):
                lower_factor[i, i - 1] = rng.choice([-3, -2, -1, 1, 2, 3])
            diagonal = sp.diag(*[rng.randint(1, 5) for _ in range(dimension)])
            hessian = lower_factor * diagonal * lower_factor.T
            comparison = sp.Matrix(
                dimension,
                dimension,
                lambda i, j: hessian[i, j] if i == j else -abs(hessian[i, j]),
            )
            scaling = comparison.inv() * sp.ones(dimension, 1)
            vector = (hessian + comparison) * scaling / 2
            assert all(value > 0 for value in scaling)
            assert all(value > 0 for value in vector)

            for size in range(1, dimension + 1):
                for subset in combinations(range(dimension), size):
                    solution = (
                        hessian.extract(subset, subset).inv()
                        * vector[list(subset), :]
                    )
                    assert all(value >= 0 for value in solution)
                    principal_subsets += 1

            upper = sp.Matrix([rng.randint(1, 3) for _ in range(dimension)])
            boundary_point = sp.Matrix(
                [upper[i] if i % 2 else 0 for i in range(dimension)]
            )
            costs = [
                sp.Matrix([rng.randint(-8, 8) for _ in range(dimension)]),
                -hessian * boundary_point,
                sp.zeros(dimension, 1),
            ]
            for cost in costs:
                point, pivots = box_qp(hessian, cost, upper, vector)
                gradient = hessian * point + cost
                assert all(0 <= point[i] <= upper[i] for i in range(dimension))
                assert all(
                    gradient[i] >= 0
                    if point[i] == 0
                    else gradient[i] <= 0
                    if point[i] == upper[i]
                    else gradient[i] == 0
                    for i in range(dimension)
                )
                assert pivots <= 2 * dimension
                qp_cases += 1

    print(
        f"PASS: {qp_cases} exact bounded-QP KKT checks; "
        f"{principal_subsets} exact principal n-step checks; "
        "all pivot counts <=2n; boundary zero-multiplier cases included"
    )
    check_boundary_newton()


def check_boundary_newton():
    """Exercise quartic refinement near a boundary point with zero multiplier."""
    first, second = sp.symbols("first second")
    minimizer = sp.Matrix([0, sp.Rational(1, 2)])
    coordinates = sp.Matrix([first, second])
    displacement = coordinates - minimizer
    difference = displacement[0] - displacement[1]
    objective = displacement.dot(displacement) / 2 + difference**4
    gradient = sp.Matrix([sp.diff(objective, variable) for variable in coordinates])
    hessian = sp.hessian(objective, coordinates)
    edge = sp.Matrix([1, -1])
    assert (hessian - sp.eye(2) - 12 * difference**2 * edge * edge.T).applyfunc(
        sp.expand
    ) == sp.zeros(2)
    assert gradient.subs(dict(zip(coordinates, minimizer))) == sp.zeros(2, 1)

    # On [0,1]^2, |difference| <= 3/2. Since ||edge||_2 <= 2 and
    # ||edge edge'||_2 = 2, 144 bounds the Hessian Lipschitz constant.
    # Thus mu=1 and K=72 satisfy the theorem's hypotheses.
    constant = sp.Integer(72)
    point = sp.Matrix([sp.Rational(1, 512), sp.Rational(1, 2)])
    error_squared = (point - minimizer).dot(point - minimizer)
    assert error_squared <= 1 / (4 * constant**2)
    for _ in range(4):
        substitution = dict(zip(coordinates, point))
        current_hessian = hessian.subs(substitution)
        current_gradient = gradient.subs(substitution)
        following, _ = box_qp(
            current_hessian,
            current_gradient - current_hessian * point,
            sp.ones(2, 1),
            sp.ones(2, 1),
        )
        next_error_squared = (following - minimizer).dot(following - minimizer)
        assert next_error_squared <= constant**2 * error_squared**2
        assert 0 < following[0] < 1
        assert 0 < following[1] < 1
        point, error_squared = following, next_error_squared
    print(
        "PASS: four exact quartic Newton steps satisfy the squared error bound; "
        "the true optimizer has an active lower bound with zero multiplier, "
        "while every computed iterate is interior"
    )


if __name__ == "__main__":
    main()
