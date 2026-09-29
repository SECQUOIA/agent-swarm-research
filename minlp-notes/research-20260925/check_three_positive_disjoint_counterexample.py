"""Exact arithmetic for the three-positive disjoint-affine-SOS obstruction."""

from fractions import Fraction as F
from itertools import combinations, product


Q = ((F(1), F(3), F(-6)), (F(3), F(1), F(-6)), (F(-6), F(-6), F(9)))
LINEAR = (F(-1), F(-1), F(9))
CONSTANT = F(1, 4)
ZEROS = (
    (F(1, 2), F(0), F(0)),
    (F(0), F(1, 2), F(0)),
    (F(1), F(0), F(1, 6)),
    (F(0), F(1), F(1, 6)),
    (F(1), F(1), F(5, 6)),
)


def value(point):
    return CONSTANT + sum(a * x for a, x in zip(LINEAR, point)) + sum(
        Q[i][j] * point[i] * point[j] for i in range(3) for j in range(3)
    )


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    return sum(
        (-1) ** j * matrix[0][j] * determinant(
            [row[:j] + row[j + 1:] for row in matrix[1:]]
        )
        for j in range(len(matrix))
    )


def rank(matrix):
    matrix = [list(row) for row in matrix]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((i for i in range(pivot_row, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for i in range(pivot_row + 1, len(matrix)):
            scale = matrix[i][column]
            matrix[i] = [a - scale * b for a, b in zip(matrix[i], matrix[pivot_row])]
        pivot_row += 1
    return pivot_row


def main():
    minors = [Q[i][i] * Q[j][j] - Q[i][j] ** 2 for i, j in combinations(range(3), 2)]
    assert minors == [F(-8), F(-27), F(-27)]
    assert all(Q[i][i] > 0 for i in range(3))

    edge_minima = []
    edge_zeros = set()
    for free in range(3):
        fixed = [i for i in range(3) if i != free]
        for bits in product((F(0), F(1)), repeat=2):
            point = [F(0)] * 3
            for index, bit in zip(fixed, bits):
                point[index] = bit
            slope = LINEAR[free] + 2 * sum(Q[free][j] * point[j] for j in fixed)
            stationary = -slope / (2 * Q[free][free])
            point[free] = min(F(1), max(F(0), stationary))
            minimum = value(point)
            assert minimum >= 0
            edge_minima.append(minimum)
            if minimum == 0:
                edge_zeros.add(tuple(point))
    assert len(edge_minima) == 12
    assert edge_minima.count(F(0)) == 5
    assert edge_minima.count(F(1, 4)) == 5
    assert edge_minima.count(F(25, 4)) == 2
    assert edge_zeros == set(ZEROS)
    assert all(value(point) == 0 for point in ZEROS)
    assert value((F(0), F(0), F(0))) == F(1, 4)

    augmented = [[F(1), *ZEROS[i]] for i in (0, 1, 2, 4)]
    assert determinant(augmented) == F(-1, 12)

    # Normalize the affine factor's nonzero origin value to one. Vanishing
    # at the first three selected zeros forces these remaining coefficients.
    coefficients = (F(1), F(-2), F(-2), F(6))
    residuals = [sum(a * b for a, b in zip(coefficients, row)) for row in augmented]
    assert residuals == [F(0), F(0), F(0), F(2)]

    # Every term has degree at most four in each variable. Equality on this
    # tensor grid therefore verifies the polynomial identity exactly.
    for x, y, z in product(map(F, (-2, -1, 0, 1, 2)), repeat=3):
        certificate = (x * y + x + y - 3 * z - F(1, 2)) ** 2
        certificate += 6 * z * (1 - x) * (1 - y)
        certificate += 3 * x * y * (1 - x) + 2 * x * y * (1 - y)
        certificate += x * x * y * (1 - y)
        assert certificate == value((x, y, z))

    # Columns are 1, x, y, z, x², y², z², xy, xz, yz. Values and
    # tangential derivatives at the five zeros give rank nine.
    contact_rows = []
    for (x, y, z), free in zip(ZEROS, (0, 1, 2, 2, 2)):
        contact_rows.append([F(1), x, y, z, x * x, y * y, z * z, x * y, x * z, y * z])
        derivatives = (
            [F(0), F(1), F(0), F(0), 2 * x, F(0), F(0), y, z, F(0)],
            [F(0), F(0), F(1), F(0), F(0), 2 * y, F(0), x, F(0), z],
            [F(0), F(0), F(0), F(1), F(0), F(0), 2 * z, F(0), x, y],
        )
        contact_rows.append(derivatives[free])
    assert rank(contact_rows) == 9
    target_coefficients = (F(1, 4), F(-1), F(-1), F(9), F(1), F(1), F(9), F(6), F(-12), F(-12))
    assert all(sum(a * b for a, b in zip(row, target_coefficients)) == 0 for row in contact_rows)
    print("PASS: exact minors, 12 edge minima, 5 zeros, affine span, exclusion, quartic identity, and exposed-ray rank")


if __name__ == "__main__":
    main()
