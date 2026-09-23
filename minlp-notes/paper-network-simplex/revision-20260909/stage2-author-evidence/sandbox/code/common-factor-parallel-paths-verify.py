"""Enumerated exact subset supports versus independent bounded-matrix LPs.

The interval matrices are more general than the proportional unobserved bounds
in the network application. This validates the cut characterization, including
negative lower bounds; graph preprocessing and separation by max-flow are not
implemented here.
"""

from fractions import Fraction as F
import random
import numpy as np
from scipy.optimize import linprog


def check(seed):
    rng = random.Random(seed)
    k, n = rng.randrange(2, 9), rng.randrange(1, 7)
    columns = []
    for j in range(n):
        col = [F(rng.randrange(-3, 4)) for i in range(k - 1)]
        columns.append(col + [-sum(col)])
    low = [[columns[j][i] - rng.randrange(4) for j in range(n)] for i in range(k)]
    high = [[columns[j][i] + rng.randrange(4) for j in range(n)] for i in range(k)]
    delta = [sum(columns[j][i] for j in range(n)) for i in range(k)]
    if seed % 2:
        a, b = rng.sample(range(k), 2)
        delta[a] += F(5, 2)
        delta[b] -= F(5, 2)
    if seed % 5 == 0:
        i, j = rng.randrange(k), rng.randrange(n)
        low[i][j] += 4
    passed = all(low[i][j] <= high[i][j] for i in range(k) for j in range(n))
    passed &= all(sum(low[i][j] for i in range(k)) <= 0 <=
                  sum(high[i][j] for i in range(k)) for j in range(n))
    if passed:
        for mask in range(1 << k):
            inside = [i for i in range(k) if mask & (1 << i)]
            outside = [i for i in range(k) if not mask & (1 << i)]
            lhs = sum(delta[i] for i in inside)
            rhs = sum(min(sum(high[i][j] for i in inside),
                          -sum(low[i][j] for i in outside)) for j in range(n))
            if lhs > rhs:
                passed = False
                break

    # Build the original d matrix LP, without shifting lower bounds or subset cuts.
    rows, rhs = [], []
    for i in range(k):
        row = np.zeros((k, n))
        row[i, :] = 1
        rows.append(row.ravel())
        rhs.append(float(delta[i]))
    for j in range(n):
        row = np.zeros((k, n))
        row[:, j] = 1
        rows.append(row.ravel())
        rhs.append(0.)
    bounds = [(float(low[i][j]), float(high[i][j])) for i in range(k) for j in range(n)]
    if any(a > b for a, b in bounds):
        result_feasible = False
    else:
        result = linprog(np.zeros(k * n), A_eq=rows, b_eq=rhs, bounds=bounds, method="highs")
        assert result.status in (0, 2), (seed, result.message)
        result_feasible = result.success
    assert passed == result_feasible, (seed, passed, result_feasible)
    return passed


if __name__ == "__main__":
    feasible = sum(check(seed) for seed in range(300))
    print(f"Passed 300 exact subset-family versus bounded-matrix LP comparisons: "
          f"{feasible} feasible and {300 - feasible} infeasible.")
