"""Exact arithmetic certificate for the five-variable star counterexample."""

from fractions import Fraction as F


A = [
    [625, -600, 527, -600, -175, 625],
    [-600, 625, -600, 527, 625, -175],
    [527, -600, 625, 0, 0, 0],
    [-600, 527, 0, 625, 0, 0],
    [-175, 625, 0, 0, 625, 0],
    [625, -175, 0, 0, 0, 625],
]
R = [
    [1000000, 799266, 291861, 478567, 69800, 786],
    [799266, 1202068, 562307, 124777, 4, 3138],
    [291861, 562307, 293721, 4, 4, 2857],
    [478567, 124777, 4, 354219, 67082, 4],
    [69800, 4, 4, 67082, 19549, 678],
    [786, 3138, 2857, 4, 678, 99],
]


def transpose(matrix):
    return list(map(list, zip(*matrix)))


def multiply(left, right):
    return [
        [sum(a * b for a, b in zip(row, col)) for col in transpose(right)]
        for row in left
    ]


def determinant(matrix):
    work = [[F(value) for value in row] for row in matrix]
    result = F(1)
    for k in range(len(work)):
        pivot = next((j for j in range(k, len(work)) if work[j][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            work[k], work[pivot] = work[pivot], work[k]
            result = -result
        value = work[k][k]
        result *= value
        for j in range(k + 1, len(work)):
            scale = work[j][k] / value
            for ell in range(k + 1, len(work)):
                work[j][ell] -= scale * work[k][ell]
    return result


def pairing(left, right):
    return sum(a * b for row, other in zip(left, right) for a, b in zip(row, other))


def mc_slacks(moment, upper):
    return [
        slack
        for i in range(1, 6)
        for j in range(1, 6)
        for slack in (
            moment[i][j],
            upper * moment[0][i] - moment[i][j],
            upper * moment[0][j] - moment[i][j],
            moment[i][j] - upper * (moment[0][i] + moment[0][j]) + upper**2,
        )
    ]


def evaluate(coefficients, point):
    return sum(value * point**power for power, value in enumerate(coefficients))


def check_reduced_pieces():
    # Each leaf polynomial is 625*y^2 + (constant+slope*t)*y.
    leaf_linear = [(1054, -1200), (-1200, 1054), (-350, 1250), (1250, -350)]
    breaks = [F(0), F(7, 25), F(527, 600), F(600, 527), F(25, 7), F(4)]
    expected = [
        [0, F(289 * 350, 625), -F(289 * 961, 625)],
        [49, -F(49 * 2400, 625), F(49 * 2304, 625)],
        [-F(20592 * 12, 625), F(20592 * 25, 625), -F(20592 * 12, 625)],
        [F(49 * 2304, 625), -F(49 * 2400, 625), 49],
        [-F(289 * 961, 625), F(289 * 350, 625), 0],
    ]
    minima = []
    for lo, hi, target in zip(breaks, breaks[1:], expected):
        mid = (lo + hi) / 2
        polynomial = list(map(F, [625, -1200, 625]))
        for constant, slope in leaf_linear:
            # No leaf's upper bound is active anywhere on the whole box.
            assert max(-F(constant, 1250), -F(constant + 4 * slope, 1250)) < 4
            if constant + slope * mid < 0:
                square = [constant**2, 2 * constant * slope, slope**2]
                polynomial = [p - F(s, 2500) for p, s in zip(polynomial, square)]
        assert polynomial == target, (polynomial, target)
        candidates = [lo, hi]
        if polynomial[2] > 0:
            vertex = -polynomial[1] / (2 * polynomial[2])
            if lo <= vertex <= hi:
                candidates.append(vertex)
        minimum = min(evaluate(polynomial, t) for t in candidates)
        assert minimum >= 0
        minima.append(minimum)
    zero = [F(1), F(48, 25), F(1), F(0), F(0), F(0)]
    assert sum(zero[i] * A[i][j] * zero[j] for i in range(6) for j in range(6)) == 0
    return minima


def main():
    assert R == transpose(R) and A == transpose(A)
    minors = [determinant([row[:k] for row in R[:k]]) for k in range(1, 7)]
    assert all(value > 0 for value in minors)
    Y = [[F(value, 10**6) for value in row] for row in R]
    assert Y[0][0] == 1
    assert min(mc_slacks(Y, F(4))) == F(4, 10**6)
    assert pairing(A, Y) == -F(9337, 250000)

    # old coordinates = D * (1,u); new coordinates = H * old coordinates.
    D = [[0] * 6 for _ in range(6)]
    H = [[F(0)] * 6 for _ in range(6)]
    D[0][0] = H[0][0] = 1
    for i in range(1, 6):
        D[i][i], H[i][i] = 4, F(1, 4)
    for i in (3, 4):
        D[i][0], D[i][i] = 4, -4
        H[i][0], H[i][i] = 1, -F(1, 4)
    assert multiply(H, D) == [[int(i == j) for j in range(6)] for i in range(6)]
    transformed_A = multiply(multiply(transpose(D), A), D)
    transformed_Y = multiply(multiply(H, Y), transpose(H))
    assert transformed_A[0][0] == 14425
    assert [2 * transformed_A[0][i] for i in range(1, 6)] == [32064, 4216, -15200, -18600, 5000]
    assert [transformed_A[i][i] for i in range(1, 6)] == [10000] * 5
    assert [2 * transformed_A[1][i] for i in range(2, 6)] == [-19200, -16864, -20000, -5600]
    assert all(transformed_A[i][j] == 0 for i in range(2, 6) for j in range(i + 1, 6))
    assert min(mc_slacks(transformed_Y, F(1))) > 0
    assert pairing(transformed_A, transformed_Y) == -F(9337, 250000)

    minima = check_reduced_pieces()
    print("Positive leading principal minors:", ", ".join(map(str, minors)))
    print("Minimum [0,4] McCormick slack:", min(mc_slacks(Y, F(4))))
    print("Minimum unit-cube McCormick slack:", min(mc_slacks(transformed_Y, F(1))))
    print("Reduced-piece minima:", ", ".join(map(str, minima)))
    print("True minimum: 0; feasible SDP–RLT value:", pairing(A, Y))
    print("All exact certificate checks passed.")


if __name__ == "__main__":
    main()
