"""Exact primal certificate for the three-positive-variable disjoint SDP gap.

Uses only Python's standard library. This verifies all 27 localizing matrices
and their strictly negative objective. Cube nonnegativity of the objective is
proved separately in three-positive-disjoint-counterexample.md.
"""

from fractions import Fraction
from itertools import permutations, product


NUMERATORS = {
    (0, 0, 0): 10000,
    (0, 0, 1): 1377,
    (0, 0, 2): 681,
    (0, 1, 0): 4041,
    (0, 1, 1): 1025,
    (0, 1, 2): 629,
    (0, 2, 0): 3392,
    (0, 2, 1): 1222,
    (1, 0, 0): 4041,
    (1, 0, 1): 1025,
    (1, 0, 2): 629,
    (1, 1, 0): 771,
    (1, 1, 1): 674,
    (1, 1, 2): 590,
    (1, 2, 0): 770,
    (1, 2, 1): 598,
    (2, 0, 0): 3392,
    (2, 0, 1): 1222,
    (2, 1, 0): 770,
    (2, 1, 1): 598,
}
MOMENTS = {power: Fraction(value, 10000) for power, value in NUMERATORS.items()}


def localizing_matrix(status):
    """-1 means a free affine variable; 0/1 mean (1-x_i)/x_i factors."""
    free = [i for i, value in enumerate(status) if value == -1]
    fixed = {i: value for i, value in enumerate(status) if value != -1}
    powers = [(0, 0, 0)] + [
        tuple(int(j == i) for j in range(3)) for i in free
    ]

    def entry(left, right):
        terms = {tuple(a + b for a, b in zip(left, right)): 1}
        for index, literal in fixed.items():
            expanded = {}
            for power, coefficient in terms.items():
                raised = list(power)
                raised[index] += 1
                raised = tuple(raised)
                expanded[raised] = expanded.get(raised, 0) + (
                    coefficient if literal else -coefficient
                )
                if literal == 0:
                    expanded[power] = expanded.get(power, 0) + coefficient
            terms = expanded
        return sum(coefficient * MOMENTS[power] for power, coefficient in terms.items())

    return [[entry(left, right) for right in powers] for left in powers]


def positive_leading_minors(matrix):
    """Exact symmetric elimination: positive pivots prove positive definiteness."""
    residual = [row[:] for row in matrix]
    determinant = Fraction(1)
    minors = []
    for index in range(len(residual)):
        pivot = residual[index][index]
        assert pivot > 0, (index, pivot, matrix)
        determinant *= pivot
        minors.append(determinant)
        for row in range(index + 1, len(residual)):
            for column in range(index + 1, len(residual)):
                residual[row][column] -= (
                    residual[row][index] * residual[index][column] / pivot
                )
    return minors


def switched_product(indices, switches):
    """Moment of a product of variables, with optional x_i -> 1-x_i."""
    terms = {(0, 0, 0): 1}
    for index in indices:
        expanded = {}
        for power, coefficient in terms.items():
            raised = list(power)
            raised[index] += 1
            raised = tuple(raised)
            expanded[raised] = expanded.get(raised, 0) + (
                -coefficient if switches[index] else coefficient
            )
            if switches[index]:
                expanded[power] = expanded.get(power, 0) + coefficient
        terms = expanded
    return sum(coefficient * MOMENTS[power] for power, coefficient in terms.items())


def main():
    expected = {power for power in product(range(3), repeat=3) if power.count(2) <= 1}
    assert set(MOMENTS) == expected
    assert MOMENTS[(0, 0, 0)] == 1
    smallest = {}
    dimensions = {}
    for status in product((-1, 0, 1), repeat=3):
        matrix = localizing_matrix(status)
        dimensions[len(matrix)] = dimensions.get(len(matrix), 0) + 1
        for order, determinant in enumerate(positive_leading_minors(matrix), 1):
            smallest[order] = min(smallest.get(order, determinant), determinant)

    objective_coefficients = {
        (2, 0, 0): 1,
        (0, 2, 0): 1,
        (0, 0, 2): 9,
        (1, 1, 0): 6,
        (1, 0, 1): -12,
        (0, 1, 1): -12,
        (1, 0, 0): -1,
        (0, 1, 0): -1,
        (0, 0, 1): 9,
        (0, 0, 0): Fraction(1, 4),
    }
    objective = sum(
        coefficient * MOMENTS[power]
        for power, coefficient in objective_coefficients.items()
    )
    assert objective == Fraction(-1, 40)

    # Anstreicher-Puges (arXiv:2501.09150v1), equations (15) and (16).
    soc15_slacks = []
    soc16_slacks = []
    for switches in product((0, 1), repeat=3):
        triple = switched_product((0, 1, 2), switches)
        for i in range(3):
            j, k = [index for index in range(3) if index != i]
            soc15_slacks.append(
                switched_product((i, i), switches)
                * switched_product((j, k), switches) - triple**2
            )
        for i, j, k in permutations(range(3)):
            soc16_slacks.append(
                switched_product((i, i), switches)
                * (switched_product((j, j), switches)
                   + 3 * switched_product((j, k), switches))
                - (switched_product((i, j), switches) + triple)**2
            )
    assert min(soc15_slacks) > 0
    assert min(soc16_slacks) > 0
    for i in range(3):
        assert switched_product((i, i), (0, 0, 0)) <= switched_product((i,), (0, 0, 0))
    print("PASS: all 27 localizing matrices are positive definite.")
    print("Matrix counts by order:", dict(sorted(dimensions.items())))
    print("Smallest leading determinant by order:", {
        order: str(value) for order, value in sorted(smallest.items())
    })
    print("Exact relaxation objective:", objective)
    print("Anstreicher-Puges SOC (15): 24 strict inequalities; minimum slack", min(soc15_slacks))
    print("Anstreicher-Puges SOC (16): 48 strict inequalities; minimum slack", min(soc16_slacks))


if __name__ == "__main__":
    main()
