"""Exact projected inequalities versus the original auxiliary disjunctive LP.

This tests the basic fully split formulation with shared transverse auxiliaries.
The comparison LP is solved numerically; the projected inequalities use Fraction.
"""

from fractions import Fraction as F
import random
import numpy as np
from scipy.optimize import linprog


def check(seed):
    rng = random.Random(seed)
    n = rng.randrange(2, 7)
    d = F(rng.choice([3, 4, 5, 8]))
    r = F(1)
    big_u = (d + r) ** 2
    t = F(rng.randrange(-8, int(8 * (d + 1)) + 1), 8)
    w = [F(rng.randrange(-8, 9), 8) for j in range(n - 1)]
    rho2 = sum(v * v for v in w)
    predicted = rho2 <= 1 and t * t + (t - d) ** 2 + rho2 <= big_u + 1
    # Per-disjunct copies of (a,b,c_1,...,c_(n-1)), followed by two weights.
    width = n + 1
    size = 2 * width + 2
    aub, bub = [], []
    for label in range(2):
        offset = label * width
        weight_index = 2 * width + label
        for coordinate in range(width):
            row = np.zeros(size)
            row[offset + coordinate] = 1
            row[weight_index] = -float(big_u if coordinate < 2 else 1)
            aub.append(row)
            bub.append(0.)
        row = np.zeros(size)
        row[offset + label] = 1
        row[offset + 2:offset + width] = 1
        row[weight_index] = -1
        aub.append(row)
        bub.append(0.)
    values = [t * t, (t - d) ** 2] + [v * v for v in w]
    for coordinate, val in enumerate(values):
        row = np.zeros(size)
        row[coordinate] = row[width + coordinate] = -1
        aub.append(row)
        bub.append(-float(val))
    aeq = np.zeros((1, size))
    aeq[0, -2:] = 1
    result = linprog(np.zeros(size), A_ub=aub, b_ub=bub,
                     A_eq=aeq, b_eq=[1], bounds=(0, None), method="highs")
    assert result.status in (0, 2), (seed, result.message)
    assert predicted == result.success, (seed, predicted, result.message)
    return predicted


if __name__ == "__main__":
    count = sum(check(seed) for seed in range(240))
    t, w, d = F(-7, 8), F(1), F(3)
    assert t * t + w * w > 1
    assert t * t + (t - d) ** 2 + w * w <= (d + 1) ** 2 + 1
    print(f"Passed 240 projected-set versus auxiliary-hull LP comparisons: "
          f"{count} feasible, {240 - count} infeasible; rational strict witness passed.")
