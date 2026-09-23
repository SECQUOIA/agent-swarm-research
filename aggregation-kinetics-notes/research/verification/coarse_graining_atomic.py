"""Exact arithmetic checks for coarse-graining.md; not a proof substitute.

Run from any working directory with Python 3. No external packages are needed.
"""

from collections import defaultdict
from fractions import Fraction as F
import json


def rank(rows):
    """Compute matrix rank by rational elimination."""
    matrix = [[F(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (i for i in range(pivot_row, len(matrix)) if matrix[i][column]), None
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for i in range(pivot_row + 1, len(matrix)):
            scale = matrix[i][column]
            matrix[i] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(matrix[i], matrix[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def total_size_kernel(z, other):
    return 1 + z / (1 + z) * other / (1 + other)


def projected_coagulation_of_atom(x):
    z = sum(x)
    coefficient = total_size_kernel(z, z) / 2
    return {z: -2 * coefficient, 2 * z: coefficient}


def projected_fragmentation_of_atom(x, fractions):
    z = sum(x)
    daughter = sum(fraction * value for fraction, value in zip(fractions, x))
    result = defaultdict(F)
    result[daughter] += 1
    result[z - daughter] += 1
    result[z] -= 1
    return dict(result)


def verify():
    results = {}
    for fractions in [
        [F(1, 5), F(2, 5), F(3, 5), F(4, 5)],
        [F(1, 4), F(1, 4), F(3, 4), F(3, 4)],
        [F(1, 2)] * 4,
    ]:
        matrix = [[fraction**power for fraction in fractions] for power in range(4)]
        actual_rank = rank(matrix)
        assert actual_rank == len(set(fractions))
        results["split_fractions_" + "_".join(map(str, fractions))] = actual_rank

    # Gradients of product(x_i), at points with one coordinate equal to two.
    # The gradient of product/(1+product) differs by a positive scalar.
    for dimension in range(2, 7):
        gradients = [
            [F(1) if i == j else F(2) for j in range(dimension)]
            for i in range(dimension)
        ]
        assert rank(gradients) == dimension
    results["bounded_rank_two_kernel_gradient_ranks"] = "full rank in dimensions 2–6"

    x = (F(1), F(1))
    other = (F(1, 2), F(3, 2))
    fractions = (F(1, 4), F(3, 4))
    assert projected_coagulation_of_atom(x) == projected_coagulation_of_atom(other)
    difference = defaultdict(F)
    for atom, value in projected_fragmentation_of_atom(x, fractions).items():
        difference[atom] += value
    for atom, value in projected_fragmentation_of_atom(other, fractions).items():
        difference[atom] -= value
    difference = {atom: value for atom, value in difference.items() if value}
    assert difference == {F(1): F(2), F(3, 4): F(-1), F(5, 4): F(-1)}
    assert sum(difference.values()) == 0
    assert sum(atom * value for atom, value in difference.items()) == 0

    # phi(z)=min(|z−1|,1) has sup norm and Lipschitz constant at most one.
    witnessed_gap = abs(
        sum(min(abs(atom - 1), F(1)) * value for atom, value in difference.items())
    )
    # Matching each off-center atom to 1 gives a BL upper bound by transport.
    transport_bound = abs(F(3, 4) - 1) + abs(F(5, 4) - 1)
    assert witnessed_gap == transport_bound == F(1, 2)
    results["atomic_projected_coagulation"] = {
        str(atom): str(value) for atom, value in projected_coagulation_of_atom(x).items()
    }
    results["fragmentation_derivative_difference_per_unit_rate"] = {
        str(atom): str(value) for atom, value in sorted(difference.items())
    }
    results["exact_BL_derivative_gap_per_unit_rate"] = str(witnessed_gap)
    results["short_time_minimax_lower_coefficient"] = str(witnessed_gap / 4)
    return results


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
