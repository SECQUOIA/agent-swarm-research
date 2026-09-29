"""Independent exact checks of the three-positive disjoint-SDP gap.

Checks all 27 source LMIs by Fraction LDL elimination, the objective gap,
the 12 edge minima, and the five reported zeros. No optimizer is used.
"""

from fractions import Fraction as F
from itertools import combinations, product


NUMERATORS = {
    (0, 0, 0): 10000, (0, 0, 1): 1377, (0, 0, 2): 681,
    (0, 1, 0): 4041, (0, 1, 1): 1025, (0, 1, 2): 629,
    (0, 2, 0): 3392, (0, 2, 1): 1222,
    (1, 0, 0): 4041, (1, 0, 1): 1025, (1, 0, 2): 629,
    (1, 1, 0): 771, (1, 1, 1): 674, (1, 1, 2): 590,
    (1, 2, 0): 770, (1, 2, 1): 598,
    (2, 0, 0): 3392, (2, 0, 1): 1222,
    (2, 1, 0): 770, (2, 1, 1): 598,
}
MOMENTS = {power: F(numerator, 10000) for power, numerator in NUMERATORS.items()}
Q = [[F(1), F(3), F(-6)], [F(3), F(1), F(-6)], [F(-6), F(-6), F(9)]]
C = [F(-1), F(-1), F(9)]


def p(point):
    return F(1, 4) + sum(C[i] * point[i] for i in range(3)) + sum(
        Q[i][j] * point[i] * point[j] for i in range(3) for j in range(3)
    )


def subsets(items):
    for size in range(len(items) + 1):
        yield from combinations(items, size)


def local_entry(i, j, ones, zeros):
    value = F(0)
    for chosen in subsets(zeros):
        power = [0, 0, 0]
        for k in (*ones, *chosen):
            power[k] += 1
        if i is not None:
            power[i] += 1
        if j is not None:
            power[j] += 1
        value += (-1) ** len(chosen) * MOMENTS[tuple(power)]
    return value


def check_pd(matrix):
    a = [row[:] for row in matrix]
    pivots = []
    for k in range(len(a)):
        pivot = a[k][k]
        assert pivot > 0, (k, matrix, pivot)
        pivots.append(pivot)
        for i in range(k + 1, len(a)):
            for j in range(i, len(a)):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
    return min(pivots)


def main():
    assert len(MOMENTS) == 20
    smallest_pivot = F(1)
    matrices = 0
    for status in product(range(3), repeat=3):
        ones = [i for i in range(3) if status[i] == 1]
        zeros = [i for i in range(3) if status[i] == 2]
        rows = [None] + [i for i in range(3) if status[i] == 0]
        matrix = [[local_entry(i, j, ones, zeros) for j in rows] for i in rows]
        smallest_pivot = min(smallest_pivot, check_pd(matrix))
        matrices += 1
    objective = F(1, 4)
    for i in range(3):
        power = [0, 0, 0]
        power[i] = 1
        objective += C[i] * MOMENTS[tuple(power)]
        for j in range(3):
            power = [0, 0, 0]
            power[i] += 1
            power[j] += 1
            objective += Q[i][j] * MOMENTS[tuple(power)]
    assert objective == F(-1, 40)
    minors = [Q[i][i] * Q[j][j] - Q[i][j] ** 2 for i, j in combinations(range(3), 2)]
    assert minors == [F(-8), F(-27), F(-27)]
    minima = []
    for free in range(3):
        other = [i for i in range(3) if i != free]
        for fixed_values in product((F(0), F(1)), repeat=2):
            point = [F(0)] * 3
            for i, value in zip(other, fixed_values):
                point[i] = value
            a = Q[free][free]
            b = C[free] + 2 * sum(Q[free][j] * point[j] for j in other)
            point[free] = max(F(0), min(F(1), -b / (2 * a)))
            minimum = p(point)
            assert minimum >= 0
            minima.append(minimum)
    zeros = [
        (F(1, 2), F(0), F(0)), (F(0), F(1, 2), F(0)),
        (F(1), F(0), F(1, 6)), (F(0), F(1), F(1, 6)),
        (F(1), F(1), F(5, 6)),
    ]
    assert all(p(point) == 0 for point in zeros)
    print(f"Passed {matrices} exact strict-PD localizing-matrix checks.")
    print(f"Minimum LDL pivot: {smallest_pivot}")
    print(f"Exact relaxed objective: {objective}")
    print(f"Two-coordinate quadratic principal minors: {minors}")
    print(f"Exact edge minima: {minima}")
    print("All five stated zeros checked exactly.")


if __name__ == "__main__":
    main()
