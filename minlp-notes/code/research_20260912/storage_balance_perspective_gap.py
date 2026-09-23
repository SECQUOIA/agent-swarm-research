#!/usr/bin/env python3
"""Exact arithmetic witness: temporal storage hull plus local perspectives is weak.

Run with Python 3.11+; standard library only. The mathematical proof and
limitations are in notes/research-20260912-energy-opportunities.md.
"""

from fractions import Fraction as F
from itertools import permutations
import json
import platform


def encode(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def main():
    initial = F(1, 2)
    magnitude = F(2, 5)
    base = (magnitude, -magnitude / 2, -magnitude / 2)
    schedules = sorted(set(permutations(base)) | set(permutations(tuple(-x for x in base))))
    assert len(schedules) == 6
    records = []
    for schedule in schedules:
        levels = [initial]
        for increment in schedule:
            levels.append(levels[-1] + increment)
        assert levels[-1] == initial
        assert all(0 <= state <= 1 for state in levels)
        assert all(abs(x) <= magnitude for x in schedule)
        records.append({
            "increment": schedule,
            "state": levels,
            "charge": [max(x, 0) for x in schedule],
            "discharge": [max(-x, 0) for x in schedule],
            "mode": [int(x > 0) for x in schedule],
            "cost": sum(x * x for x in schedule),
        })
    means = {
        name: [sum(row[name][t] for row in records) / F(6) for t in range(3)]
        for name in ("charge", "discharge", "mode")
    }
    assert means["charge"] == means["discharge"] == [F(2, 15)] * 3
    assert means["mode"] == [F(1, 2)] * 3
    local_perspectives = sum(
        means["charge"][t] ** 2 / means["mode"][t]
        + means["discharge"][t] ** 2 / (1 - means["mode"][t])
        for t in range(3)
    )
    mean_throughput = sum(means["charge"]) + sum(means["discharge"])
    balance_bound = F(3, 8) * mean_throughput ** 2
    mean_cost = sum(row["cost"] for row in records) / F(6)
    assert local_perspectives == F(16, 75)
    assert balance_bound == mean_cost == F(6, 25)
    assert balance_bound / local_perspectives == F(9, 8)

    sharp_coefficients = {}
    for size in range(2, 20):
        candidate = F(size, 4 * ((size * size) // 4))
        # For p positive and q negative entries, separate Cauchy bounds give
        # (1/p + 1/q) / 4. Zero entries leave p+q <= size.
        all_sign_counts = [F(p + q, 4 * p * q)
                           for p in range(1, size)
                           for q in range(1, size - p + 1)]
        assert min(all_sign_counts) == candidate
        sharp_coefficients[str(size)] = candidate

    print(json.dumps({
        "python": platform.python_version(),
        "dependencies": "Python standard library",
        "schedules": records,
        "mean": means,
        "local_perspective_bound": local_perspectives,
        "exact_envelope_value_at_mean": mean_cost,
        "balance_throughput_cut": balance_bound,
        "ratio": balance_bound / local_perspectives,
        "sharp_zero_sum_coefficients": sharp_coefficients,
        "check": "passed",
    }, default=encode, indent=2))


if __name__ == "__main__":
    main()
