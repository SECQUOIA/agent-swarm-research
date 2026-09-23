"""Exact check of odd-cycle marginal-preserving coverage rounding."""

from fractions import Fraction as F
from itertools import product


for length in (3, 5, 7, 9, 11):
    edge_means = [F(0)] * length
    coverage = [F(0)] * length
    for unmatched in range(length):
        matching = {(unmatched + 1 + 2 * j) % length for j in range((length - 1) // 2)}
        for selected in (matching, set(range(length)) - matching):
            for i in range(length):
                edge_means[i] += F(i in selected, 2 * length)
                coverage[i] += F(i in selected or (i - 1) % length in selected, 2 * length)
    assert edge_means == [F(1, 2)] * length
    assert coverage == [1 - F(1, 2 * length)] * length
    for bits in product((0, 1), repeat=length):
        covered = sum(bool(bits[i] or bits[(i - 1) % length]) for i in range(length))
        assert covered <= sum(bits) + (length - 1) // 2
    print(f"L={length}: all edge means and coverage exact; sharpness inequality checked on {2**length} subsets")
