"""Exact end-to-end fixture; not an implementation of the general MIQP oracle."""

from fractions import Fraction as Q

from projection_anchor_checks import penalties, source_grid


def dot(row, point):
    return sum((a * b for a, b in zip(row, point)), Q(0))


def objective(point):
    z, y, _, _ = point
    return (y - (1 + z) / 3) ** 2 + 2 * z * (1 - z)


# Original coordinates are (integer z, continuous y, w, u).
# P includes w=2y, redundant copies, and a zero row. The optimal set is
# {(0,1/3,2/3,u),(1,2/3,4/3,u): 0<=u<=1}.
ROWS = [
    (-1, 0, 0, 0), (1, 0, 0, 0),
    (0, -1, 0, 0), (0, 1, 0, 0),
    (0, 0, 0, -1), (0, 0, 0, 1),
    (0, -2, 1, 0), (0, 2, -1, 0),
    (0, -4, 2, 0), (0, 0, 0, 0),
    (0, 0, -1, 0), (0, 0, 1, 0),
]
RHS = [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 2]
A = [
    [Q(-34, 9), Q(-2, 3), Q(0), Q(0)],
    [Q(-2, 3), Q(2), Q(0), Q(0)],
    [Q(0)] * 4, [Q(0)] * 4,
]
B = [Q(20, 9), Q(-2, 3), Q(0), Q(0)]
T = (Q(6, 7), Q(1, 7), Q(0), Q(0))
ALPHA = Q(49, 9)
GROWTH = Q(1, 5)
GW = GROWTH * ALPHA / (2 * GROWTH + ALPHA)
KAPPA = ALPHA / GW
OPTIMAL_IMAGES = (Q(1, 21), Q(20, 21))


def feasible(point):
    return point[0].denominator == 1 and all(
        dot(row, point) <= rhs for row, rhs in zip(ROWS, RHS)
    )


def oracle(a):
    # The residual Hessian is diag(2/9,19/9,0,0). Enumerate the two
    # integer modes; their common continuous minimizer is explicit.
    y = min(Q(1), max(Q(0), (6 + 7 * a) / 19))
    candidates = []
    for z in (Q(0), Q(1)):
        point = (z, y, 2 * y, Q(1, 2))
        value = objective(point) + ALPHA * (a - dot(T, point)) ** 2 / 2
        candidates.append((value, point))
    value, point = min(candidates)
    assert feasible(point)
    if 0 <= a <= 1:
        exact = Q(49, 19) * min((a - v) ** 2 for v in OPTIMAL_IMAGES)
        assert value == exact
    return value, point


def main():
    n, denominator = 4, 9
    curvature_bound = max(
        [Q(1)] + [abs(denominator * v) for row in A for v in row]
        + [abs(denominator * v) for row in ROWS for v in row]
    )
    assert curvature_bound.denominator == 1
    row_bound = n * curvature_bound
    coefficient_bound = (n * curvature_bound) ** (n + 1)
    height = (n * coefficient_bound) ** n
    value_height = 2 * denominator * height ** 2
    tau = 1 / (4 * len(ROWS) * height)
    delta = tau / (2 * row_bound)
    target = min(Q(1), GROWTH * delta ** 2, 1 / (4 * value_height ** 2))
    epsilon, accuracy_bits = Q(1), 0
    while epsilon > target:
        epsilon /= 2
        accuracy_bits += 1

    theta = Q(1, 4)
    while theta * theta * KAPPA > Q(1, 8):
        theta /= 2
    radius = 0
    while radius * radius < KAPPA:
        radius += 1
    radius *= 2
    proximity = ALPHA * theta * theta / 4
    center = Q(0)
    calls = max_grid = 0
    for stage in range(accuracy_bits + 20):
        h = Q(1, 2 ** stage)
        lo, hi = max(Q(0), center - radius * h), min(Q(1), center + radius * h)
        nearest = min(OPTIMAL_IMAGES, key=lambda s: abs(s - center))
        assert lo <= nearest <= hi
        grid = source_grid(lo, hi, center, h, theta)
        correction = penalties(grid, ALPHA)
        max_grid = max(max_grid, len(grid))
        candidates = []
        for a, d in zip(grid, correction):
            value, witness = oracle(a)
            assert value >= GW * min((a - s) ** 2 for s in OPTIMAL_IMAGES)
            candidates.append((value - d + proximity * (a - center) ** 2,
                               a, value, witness))
            calls += 1
        minimum, a, value, witness = min(candidates)
        error_bound = 4 * KAPPA * h * h
        lower = minimum - proximity * ((1 + theta * theta / 2) * error_bound + h * h / 2)
        assert lower <= 0 <= objective(witness) <= value
        assert value - lower <= Q(99, 256) * ALPHA * h * h
        distance2 = min((witness[0] - z) ** 2
                        + 5 * (witness[1] - Q(1 + z, 3)) ** 2
                        for z in (0, 1))
        assert objective(witness) >= GROWTH * distance2
        assert min((a - s) ** 2 for s in OPTIMAL_IMAGES) <= KAPPA * h * h
        if value - lower <= epsilon:
            break
        center = a
    else:
        raise AssertionError("proximal refinement did not terminate")

    assert distance2 <= delta ** 2
    selected = [i for i, (row, rhs) in enumerate(zip(ROWS, RHS))
                if denominator * (rhs - dot(row, witness)) <= tau]
    z = witness[0]
    recovered = (z, (1 + z) / 3, 2 * (1 + z) / 3, Q(0))
    assert feasible(recovered) and objective(recovered) == 0
    assert all(dot(ROWS[i], recovered) == RHS[i] for i in selected)
    # Here the recovered continuous gradient is zero; the remaining
    # component is in the integer-fixing normal space. This supplies an
    # explicit solution of the final stationarity LP for this fixture.
    gradient = [dot(row, recovered) + b for row, b in zip(A, B)]
    assert all(g == 0 for g in gradient[1:])
    assert lower <= 0 <= objective(witness)
    assert objective(witness) - lower < 1 / value_height ** 2
    print("PASS: disconnected optimal segments and coupled mixed polytope")
    print("accuracy bits:", accuracy_bits, "stages:", stage + 1)
    print("exact recourse calls:", calls, "maximum grid nodes:", max_grid)
    print("selected rows:", selected, "recovered:", tuple(map(str, recovered)))


if __name__ == "__main__":
    main()
