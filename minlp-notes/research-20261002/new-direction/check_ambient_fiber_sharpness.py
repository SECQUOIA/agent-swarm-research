"""Targeted exact checks for the ambient fiber-volume sharpness example."""

from fractions import Fraction as F
from itertools import combinations, product
from math import ceil, floor


def integrated_probability(n, q):
    """Integrate the joint extreme density, split at range 1-q."""
    if n == 1:
        return q
    a = 1 - q
    first = q * a ** (n - 1) / (n - 1)
    second = (1 - a ** (n - 1)) / (n - 1) - (1 - a**n) / n
    return n * (n - 1) * (first + second)


def discrete_probability(n, points, q):
    """Count integer-grid extrema by their difference and midpoint."""
    powers = [j**n for j in range(points + 1)]
    count = 0
    for span in range(points):
        lo = max(0, ceil((points - 1 - span - q * (points - 1)) / 2))
        hi = min(
            points - 1 - span,
            floor((points - 1 - span + q * (points - 1)) / 2),
        )
        if hi < lo:
            continue
        endpoint_count = (
            1
            if span == 0
            else powers[span + 1] - 2 * powers[span] + powers[span - 1]
        )
        count += (hi - lo + 1) * endpoint_count
    return F(count, points**n)


def determinant(matrix):
    work = [list(row) for row in matrix]
    answer = F(1)
    for i in range(len(work)):
        pivot = next((j for j in range(i, len(work)) if work[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            work[i], work[pivot] = work[pivot], work[i]
            answer = -answer
        value = work[i][i]
        answer *= value
        for j in range(i + 1, len(work)):
            multiplier = work[j][i] / value
            for col in range(i + 1, len(work)):
                work[j][col] -= multiplier * work[i][col]
    return answer


def main():
    integral_checks = 0
    for n in range(1, 33):
        for q in (F(0), F(1, 2 * n), F(1, 7), F(1, 2), F(1)):
            assert integrated_probability(n, q) == 1 - (1 - q) ** n
            integral_checks += 1

    enumeration_checks = 0
    for n in range(1, 7):
        for points in range(2, 6):
            for q in (F(0), F(1, 4), F(1, 2), F(1)):
                hits = sum(
                    abs(min(draw) + max(draw) - points + 1) <= q * (points - 1)
                    for draw in product(range(points), repeat=n)
                )
                assert discrete_probability(n, points, q) == F(hits, points**n)
                enumeration_checks += 1

    discrepancy_checks = 0
    for n in (4, 9, 16, 25):
        for points in (33, 129, 513):
            for q in (F(1, 2 * n), F(1, 4), F(1, 2)):
                continuous = 1 - (1 - q) ** n
                discrete = discrete_probability(n, points, q)
                # Each scalar section is an interval. Replace coordinates
                # successively, paying the interval discrepancy 2/points.
                assert abs(discrete - continuous) <= F(2 * n, points)
                discrepancy_checks += 1

    minor_checks = 0
    for k in range(1, 4):
        for m in (1, 2):
            n = k * m * m
            rows = [
                [F(1, m) if j // (m * m) == i else F(0) for i in range(k)]
                for j in range(n)
            ]
            for size in range(1, k + 1):
                for selected in combinations(range(k), size):
                    total = sum(
                        abs(
                            determinant(
                                [[rows[j][i] for i in selected] for j in coords]
                            )
                        )
                        for coords in combinations(range(n), size)
                    )
                    assert total == m**size
                    minor_checks += 1

    print(
        f"PASS: {integral_checks} exact range integrals, "
        f"{enumeration_checks} discrete endpoint/enumeration comparisons, "
        f"{discrepancy_checks} finite-grid discrepancy checks, "
        f"{minor_checks} disjoint-block minor sums."
    )


if __name__ == "__main__":
    main()
