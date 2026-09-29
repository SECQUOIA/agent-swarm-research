"""Exact finite checks for the scalar ALD hardness constructions.

This is a targeted arithmetic check, not a verification of NP-hardness or novelty.
All arithmetic used to compare values is rational. The dual is independently
evaluated through zero-mean mixtures of at most two residuals.
"""

from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product


def dual_from_pairs(points, rho):
    """Scalar finite ALD: minimize cost among zero-mean residual mixtures."""
    zero = [F(f) for r, f in points if r == 0]
    negative = [(r, F(f) + rho * abs(r)) for r, f in points if r < 0]
    positive = [(r, F(f) + rho * abs(r)) for r, f in points if r > 0]
    candidates = zero + [
        (rp * cn - rn * cp) / (rp - rn)
        for rn, cn in negative
        for rp, cp in positive
    ]
    return min(candidates)


def check_box():
    checked = 0
    for n in range(1, 4):
        for original in combinations_with_replacement(range(1, 5), n):
            for target in range(1, sum(original) + 2):
                original_sums = {
                    sum(a * z for a, z in zip(original, bits))
                    for bits in product((0, 1), repeat=n)
                }
                weights = original + (target + 1,)
                sums = {
                    sum(a * z for a, z in zip(weights, bits))
                    for bits in product((0, 1), repeat=n + 1)
                }
                best_below = max(s for s in sums if s <= target)
                assert min(s for s in sums if s >= target + 1) == target + 1
                for k in (2, 4, 7, 16):
                    points = [(k * s - (k * target + 1) * q, -q)
                              for s in sums for q in (0, 1)]
                    assert [p for p in points if p[0] == 0] == [(0, 0)]
                    dm = k * (target - best_below) + 1
                    dp = k - 1
                    threshold = (F(1, dm) + F(1, dp)) / 2
                    if target in original_sums:
                        assert threshold == F(k, 2 * (k - 1))
                    else:
                        assert threshold <= F(k, k * k - 1)
                    for rho in (F(0), F(1, 3), threshold, 2 * threshold):
                        expected = min(F(0), -1 + rho * F(2 * dm * dp, dm + dp))
                        actual = dual_from_pairs(points, rho)
                        multiplier = rho * F(dm - dp, dm + dp)
                        lagrangian = min(F(f) + multiplier * r + rho * abs(r)
                                         for r, f in points)
                        assert actual == expected == lagrangian
                    if k == 4:
                        value = dual_from_pairs(points, F(1, 3))
                        assert value == (-F(1, 2) if target in original_sums else 0)
                    checked += 1
    return checked


def check_graphs():
    checked = 0
    for n in range(1, 5):
        possible_edges = list(combinations(range(n), 2))
        for edge_bits in product((0, 1), repeat=len(possible_edges)):
            edges = [e for e, selected in zip(possible_edges, edge_bits) if selected]
            independent = [x for x in product((0, 1), repeat=n)
                           if all(x[u] + x[v] <= 1 for u, v in edges)]
            alpha = max(map(sum, independent))
            points = []
            feasible = []
            for x in independent:
                for p, m in product((0, 1), repeat=2):
                    if p + m <= 1 and all(xv <= p + m for xv in x):
                        points.append((p - m, -sum(x)))
                        if p == m:
                            feasible.append((x, p, m))
            assert feasible == [((0,) * n, 0, 0)]
            for rho in (F(0), F(1, 3), F(alpha), F(alpha + 1)):
                assert dual_from_pairs(points, rho) == min(0, rho - alpha)
            checked += 1
    return checked


if __name__ == "__main__":
    print(f"Binary-box instances checked: {check_box()}")
    print(f"Unit-data graph instances checked: {check_graphs()}")
    print("All exact rational checks passed.")
