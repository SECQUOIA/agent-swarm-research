"""Independent finite-law tests of Gaussian MIQP label isolation.

All label gaps and probability sums use exact fractions. A small dyadic
Gaussian-like law is enumerated completely; this is not the theorem's
much finer sampler or an implementation of its convex-MIQP oracle.
"""

from fractions import Fraction as Q
from itertools import product

import mpmath as mp


def scalar_law():
    mp.mp.dps = 80
    grid = [Q(j, 4) for j in range(-16, 17)]
    denominator = 1 << 16
    cumulative = [0]
    for a, b in zip(grid, grid[1:]):
        midpoint = (a + b) / 2
        x = mp.mpf(midpoint.numerator) / midpoint.denominator
        cdf = (1 + mp.erf(x / mp.sqrt(2))) / 2
        cumulative.append(int(mp.floor(cdf * denominator)))
    cumulative.append(denominator)
    weights = [Q(b - a, denominator) for a, b in zip(cumulative, cumulative[1:])]
    assert sum(weights) == 1 and all(w >= 0 for w in weights)
    # The loose bound follows from midpoint displacement <=1/8,
    # Gaussian density <1/2, tail outside [-4,4] <1/1000, and CDF rounding.
    delta = Q(1, 16) + Q(1, 1000) + Q(1, denominator)
    # Numerically verify the complete discrete CDF, including both sides
    # of each atom. The event sums below remain exactly rational.
    running = Q(0)
    for x, w in zip(grid, weights):
        target = (1 + mp.erf(mp.mpf(x.numerator) / x.denominator / mp.sqrt(2))) / 2
        for side in (running, running + w):
            assert abs(mp.mpf(side.numerator) / side.denominator - target) < mp.mpf(delta.numerator) / delta.denominator
        running += w
    return list(zip(grid, weights)), delta


def continuous_cost(z, gamma_y):
    # Minimize y²/2 +(z/3 + gamma_y)y + z/7 over y in [0,1].
    y = max(Q(0), min(Q(1), -Q(z, 3) - gamma_y))
    return y * y / 2 + (Q(z, 3) + gamma_y) * y + Q(z, 7)


def check():
    law, delta = scalar_law()
    thresholds = (Q(0), Q(1, 64), Q(1, 16), Q(1, 4))
    fixtures = [
        ([(0,), (1,)], [Q(0), Q(0)], 1),
        ([(0,), (2,)], [Q(0), Q(1, 8)], 2),
        ([(0, 0), (1, 1), (1, 0)], [Q(0), Q(1, 8), Q(-1, 4)], 2),
        ([(0, 0), (0, 1), (1, 0), (1, 1)], [Q(0)] * 4, 2),
    ]
    draws = ties = comparisons = 0
    for labels, costs, width_sum in fixtures:
        events = {eps: Q(0) for eps in thresholds}
        for coordinates in product(law, repeat=len(labels[0])):
            gamma = [x for x, _ in coordinates]
            mass = Q(1)
            for _, weight in coordinates:
                mass *= weight
            values = sorted(cost + sum(z * g for z, g in zip(label, gamma))
                            for label, cost in zip(labels, costs))
            gap = values[1] - values[0]
            ties += gap == 0 and mass > 0
            for eps in thresholds:
                if gap <= eps:
                    events[eps] += mass
            draws += 1
        for eps, probability in events.items():
            assert probability <= width_sum * (eps + 2 * delta)
            comparisons += 1

    # Conditioned intercepts can change with continuous-coordinate noise.
    # This fixture explicitly optimizes the continuous part for each label.
    events = {eps: Q(0) for eps in thresholds}
    for (gamma_z, mass_z), (gamma_y, mass_y) in product(law, repeat=2):
        values = sorted(continuous_cost(z, gamma_y) + gamma_z * z for z in (0, 1))
        gap = values[1] - values[0]
        ties += gap == 0 and mass_z * mass_y > 0
        for eps in thresholds:
            if gap <= eps:
                events[eps] += mass_z * mass_y
        draws += 1
    for eps, probability in events.items():
        assert probability <= eps + 2 * delta
        comparisons += 1
    assert ties > 0
    print(f"5 weighted-law fixtures; {draws} exact draws; {ties} tied draws; {comparisons} isolation bounds")
    print("33-atom scalar law: both CDF limits checked at every atom")


if __name__ == "__main__":
    check()
