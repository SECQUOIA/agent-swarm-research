"""Independent exact diagnostics for implicit-graph KKT and tail interfaces."""

from fractions import Fraction as Q
from itertools import product


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(left, right):
    if not left:
        return []
    columns = transpose(right)
    return [[sum(a * b for a, b in zip(row, column)) for column in columns]
            for row in left]


def determinant(matrix):
    work = [list(map(Q, row)) for row in matrix]
    result = Q(1)
    for col in range(len(work)):
        pivot = next((row for row in range(col, len(work)) if work[row][col]), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            result = -result
        value = work[col][col]
        result *= value
        for row in range(col + 1, len(work)):
            ratio = work[row][col] / value
            for index in range(col + 1, len(work)):
                work[row][index] -= ratio * work[col][index]
    return result


def saddle_checks():
    count = 0
    for free, dependent, seed in product(range(4), range(1, 4), range(3)):
        diagonal = [Q(j + seed + 1, j + 2) for j in range(dependent)]
        jac_u = [[Q((i + 2 * j + seed) % 5 - 2) for i in range(free)]
                 for j in range(dependent)]
        tangent_y = [[-value / diagonal[j] for value in row]
                     for j, row in enumerate(jac_u)]
        reduced = [[Q((i + 1) * (j + 1) + (i == j)) for j in range(free)]
                   for i in range(free)]
        cross = [[Q((i + j + seed) % 3 - 1) for j in range(dependent)]
                 for i in range(free)]
        h_yy = [[Q((i + j + seed) % 4 - 2) for j in range(dependent)]
                for i in range(dependent)]
        if free:
            cross_tangent = multiply(cross, tangent_y)
            tangent_quadratic = multiply(transpose(tangent_y), multiply(h_yy, tangent_y))
            h_uu = [[reduced[i][j] - cross_tangent[i][j] - cross_tangent[j][i]
                     - tangent_quadratic[i][j] for j in range(free)] for i in range(free)]
        else:
            h_uu = []
        hessian = [h_uu[i] + cross[i] for i in range(free)]
        hessian += [[cross[i][j] for i in range(free)] + h_yy[j]
                    for j in range(dependent)]
        jacobian = [jac_u[j] + [diagonal[j] if j == k else Q(0)
                               for k in range(dependent)] for j in range(dependent)]
        kkt = [hessian[i] + [jacobian[j][i] for j in range(dependent)]
               for i in range(free + dependent)]
        kkt += [row + [Q(0)] * dependent for row in jacobian]
        target = Q((-1) ** dependent) * determinant(reduced)
        for value in diagonal:
            target *= value * value
        assert determinant(kkt) == target != 0
        count += 1
    return count


def nonlinear_active_face_checks():
    # q=y²+y-u-a²; the active anchor a=1/2 stays fixed in face stationarity.
    active, free, output, multiplier = Q(1, 2), Q(1, 2), Q(1, 2), Q(-1, 2)
    eta, free_noise = Q(1), Q(-3, 2)
    assert output * output + output - free - active * active == 0
    assert 2 * free + free_noise - multiplier == 0
    assert eta + multiplier * (2 * output + 1) == 0
    jacobian = [[Q(2), Q(0), Q(-1)], [Q(0), Q(-1), Q(2)], [Q(-1), Q(2), Q(0)]]
    assert determinant(jacobian) == -7
    assert determinant(jacobian) == -(2 * output + 1) ** 2 * Q(7, 4)
    count = 0
    for size, threshold in product([2, 4, 8, 16], [Q(0), Q(1, 8), Q(1, 2), Q(1)]):
        law = [Q(-1) + Q(2 * k, size - 1) for k in range(size)]
        active_gradients = [noise - 2 * active * multiplier for noise in law]
        probability = Q(sum(abs(value) <= threshold for value in active_gradients), size)
        assert probability <= threshold + Q(1, size)
        count += 1
    # The positive reduced Hessian hypothesis is material.
    singular = [[Q(0), Q(0), Q(-1)], [Q(0), Q(0), Q(1)], [Q(-1), Q(1), Q(0)]]
    assert determinant(singular) == 0
    return count


if __name__ == "__main__":
    saddle_count = saddle_checks()
    strip_count = nonlinear_active_face_checks()
    print(f"PASS: {saddle_count} exact KKT determinant identities, including zero free dimension")
    print(f"PASS: nonlinear active-face fixture and {strip_count} finite-law strip bounds")
    print("PASS: reduced-Hessian degeneracy gives a singular KKT example")
