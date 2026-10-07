"""Targeted exact-rational checks for projection-anchors.md."""

from fractions import Fraction as Q
from itertools import product


def source_grid(lo, hi, center, h, theta, integer=False):
    values = {center}
    for direction, endpoint in ((-1, lo), (1, hi)):
        distance = Q(0)
        span = abs(endpoint - center)
        while distance < span:
            step = h + theta * distance
            if integer:
                step = Q(max(1, step.numerator // step.denominator))
            distance = min(span, distance + step)
            values.add(center + direction * distance)
    return sorted(values)


def penalties(grid, curvature, integer=False):
    lengths = [right - left for left, right in zip(grid, grid[1:])]
    if integer:
        lengths = [length if length > 1 else Q(0) for length in lengths]
    return [
        curvature * max(left, right) ** 2 / 8
        for left, right in zip([Q(0)] + lengths, lengths + [Q(0)])
    ]


def run_one_dimensional(lo, hi, center, objective, optima, curvature,
                        growth, epsilon, theta, integer=False):
    h = Q(1)
    while 4 * curvature * h * h > epsilon:
        h /= 2
    assert theta * theta <= growth / (4 * curvature)
    anchors = {center}
    grid = []
    failures = 0
    for _ in range(100):
        grid = sorted(set(grid).union(*[
            source_grid(lo, hi, anchor, h, theta, integer)
            for anchor in anchors
        ]))
        d = penalties(grid, curvature, integer)
        for node, correction in zip(grid, d):
            distance = min(abs(node - anchor) for anchor in anchors)
            assert correction <= curvature * (h + theta * distance) ** 2 / 8
        index = min(range(len(grid)), key=lambda i: objective(grid[i]) - d[i])
        y, correction = grid[index], d[index]
        lower = objective(y) - correction
        assert lower <= 0
        assert objective(y) >= 0
        if correction <= epsilon:
            if integer:
                assert correction == 0 and y in optima and lower == 0
            return failures, len(grid)

        nearest = min(optima, key=lambda value: abs(value - y))
        old_distance = min(abs(nearest - anchor) for anchor in anchors)
        new_distance = min(old_distance, abs(nearest - y))
        # The stronger vector-level contraction is exact in one dimension.
        assert 4 * new_distance * new_distance < old_distance * old_distance
        assert y not in anchors
        anchors.add(y)
        failures += 1
    raise AssertionError("iteration cap reached")


def check_diagonal_obstruction():
    first_grids = [
        [Q(0), Q(1)],
        [Q(0), Q(1, 5), Q(3, 5), Q(1)],
        [Q(i, 7) for i in range(8)],
    ]
    second_grids = [
        [Q(0), Q(1, 2), Q(1)],
        [Q(i, 11) for i in range(12)],
    ]
    checked = 0
    for left, right in product(first_grids, second_grids):
        dl = penalties(left, Q(2))
        dr = penalties(right, Q(2))
        lower = min(
            (x - y) ** 2 - dx - dy
            for (x, dx), (y, dy) in product(zip(left, dl), zip(right, dr))
        )
        assert all(lower <= -correction for correction in dl + dr)
        checked += 1
    return checked


def main():
    results = []
    for epsilon, center in product(
        (Q(1, 4), Q(1, 64), Q(1, 1024)), (Q(-1), Q(0), Q(1, 3))
    ):
        failures, states = run_one_dimensional(
            Q(-1), Q(1), center, lambda x: (x * x - 1) ** 2,
            (Q(-1), Q(1)), Q(8), Q(1), epsilon, Q(1, 8),
        )
        results.append((str(epsilon), str(center), failures, states))
    integer_result = run_one_dimensional(
        Q(-1024), Q(1024), Q(0), lambda x: (x * x - 512 ** 2) ** 2,
        (Q(-512), Q(512)), Q(11534336), Q(262144), Q(2883584),
        Q(1, 16), True,
    )
    print("continuous double-well runs:", len(results))
    print("maximum failed solves:", max(row[2] for row in results))
    print("maximum final states:", max(row[3] for row in results))
    print("integer double-well (failures, final states):", integer_result)
    print("diagonal obstruction grid pairs:", check_diagonal_obstruction())


if __name__ == "__main__":
    main()
