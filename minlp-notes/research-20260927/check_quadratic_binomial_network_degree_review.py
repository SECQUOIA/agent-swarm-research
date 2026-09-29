"""Exact small graph checks for the independent binomial-network review.

Enumerate every directed multigraph with two outgoing arcs per vertex on
one through four labeled vertices. Loops and repeated neighbors are included.
This checks finite combinatorial claims, not the field or character proofs.
"""

from functools import reduce
from itertools import combinations_with_replacement, product
from math import gcd


def determinant(matrix):
    """Bareiss determinant with exact integer division and row pivoting."""
    size = len(matrix)
    if not size:
        return 1
    matrix = [row[:] for row in matrix]
    sign = 1
    denominator = 1
    for pivot_index in range(size - 1):
        if not matrix[pivot_index][pivot_index]:
            row = next(
                (i for i in range(pivot_index + 1, size) if matrix[i][pivot_index]),
                None,
            )
            if row is None:
                return 0
            matrix[pivot_index], matrix[row] = matrix[row], matrix[pivot_index]
            sign = -sign
        pivot = matrix[pivot_index][pivot_index]
        for i in range(pivot_index + 1, size):
            for j in range(pivot_index + 1, size):
                numerator = (
                    matrix[i][j] * pivot
                    - matrix[i][pivot_index] * matrix[pivot_index][j]
                )
                assert numerator % denominator == 0
                matrix[i][j] = numerator // denominator
            matrix[i][pivot_index] = 0
        denominator = pivot
    return sign * matrix[-1][-1]


def reaches_every_vertex(adjacency, reverse=False):
    seen = {0}
    pending = [0]
    while pending:
        i = pending.pop()
        for j in range(len(adjacency)):
            multiplicity = adjacency[j][i] if reverse else adjacency[i][j]
            if multiplicity and j not in seen:
                seen.add(j)
                pending.append(j)
    return len(seen) == len(adjacency)


def verify(size):
    cases = odd_cases = maximum_index = maximum_odd_index = 0
    maximum_noneulerian_index = 0
    choices = tuple(combinations_with_replacement(range(size), 2))
    for outgoing in product(choices, repeat=size):
        adjacency = [[0] * size for _ in range(size)]
        for i, (j, k) in enumerate(outgoing):
            adjacency[i][j] += 1
            adjacency[i][k] += 1
        if not reaches_every_vertex(adjacency):
            continue
        if not reaches_every_vertex(adjacency, reverse=True):
            continue
        cases += 1
        laplacian = [
            [2 * (i == j) - adjacency[i][j] for j in range(size)]
            for i in range(size)
        ]
        cofactors = [
            determinant(
                [
                    [laplacian[i][j] for j in range(size) if j != root]
                    for i in range(size)
                    if i != root
                ]
            )
            for root in range(size)
        ]
        assert min(cofactors) > 0
        assert max(cofactors) <= 2 ** (size - 1)
        index = reduce(gcd, cofactors)
        stationary = [value // index for value in cofactors]
        assert reduce(gcd, stationary) == 1
        assert all(
            sum(stationary[i] * laplacian[i][j] for i in range(size)) == 0
            for j in range(size)
        )
        signed_minors = [
            (-1) ** row
            * determinant(
                [
                    [laplacian[i][j] for j in range(1, size)]
                    for i in range(size)
                    if i != row
                ]
            )
            for row in range(size)
        ]
        assert signed_minors == cofactors
        eulerian = all(
            sum(adjacency[i][j] for i in range(size)) == 2 for j in range(size)
        )
        assert eulerian == (max(stationary) == 1)
        if not eulerian:
            assert size >= 2
            assert index <= 2 ** (size - 2)
            maximum_noneulerian_index = max(maximum_noneulerian_index, index)
        if index % 2:
            odd_cases += 1
            assert index <= (2**size - (-1) ** size) // 3
            maximum_odd_index = max(maximum_odd_index, index)
        maximum_index = max(maximum_index, index)
    return (
        cases,
        odd_cases,
        maximum_index,
        maximum_odd_index,
        maximum_noneulerian_index,
    )


if __name__ == "__main__":
    expected = {
        1: (1, 1, 1, 1, 0),
        2: (4, 3, 2, 1, 1),
        3: (65, 42, 4, 3, 2),
        4: (2325, 1296, 8, 5, 4),
    }
    for size, expected_result in expected.items():
        result = verify(size)
        assert result == expected_result
        print(f"m={size}: {result}")
    print("All exact checks passed, including loops and repeated neighbors.")
