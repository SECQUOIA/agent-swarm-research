"""Independent full-control LP and original-discrepancy checks of grid minimax.

The comparison LP retains every mode and every interval rate. It does not
import the proposed region builder or its three-type/three-phase compression.
Numerical LP comparisons support, but do not replace, the mathematical review.
"""
from fractions import Fraction as Q
from itertools import product
from random import Random

import numpy as np
from scipy.optimize import linprog

from finite_grid_research import minimax_lp, witness_matrix
from minimax import minimax


def direct_error(matrix, grid):
    """Enumerate schedules using absolute cumulative errors, not identity (1)."""
    n, N = len(matrix), len(grid) - 1
    best = grid[-1]
    for p, q, switch in product(range(n), range(n), range(N + 1)):
        err = [Q(0)] * n
        peak = Q(0)
        for k in range(N):
            active = p if k < switch else q
            dt = grid[k + 1] - grid[k]
            for i in range(n):
                err[i] += dt * (matrix[i][k] - (active == i))
                peak = max(peak, abs(err[i]))
        best = min(best, peak)
    return best


def uncompressed(n, grid):
    N = len(grid) - 1
    dim = n * N + 1
    T = grid[-1]
    dt = [grid[k + 1] - grid[k] for k in range(N)]
    error = np.zeros(dim)
    error[-1] = 1

    def cum(i, end):
        x = np.zeros(dim)
        for k in range(end):
            x[i * N + k] = dt[k]
        return x

    totals = [cum(i, N) for i in range(n)]
    eq = []
    for k in range(N):
        row = np.zeros(dim)
        row[k:n * N:N] = 1
        eq.append(row)
    best = 0.
    for a in range(1, N + 1):
        for b in range(a, N + 1):
            for high in (False, True):
                rows, rhs = [], []

                def at_most(row, bound):
                    rows.append(row)
                    rhs.append(float(bound))

                for i in range(n - 1):
                    at_most(totals[i + 1] - totals[i], 0)
                at_most(-error, -T / 3)
                for i, end in ((0, a), (1, b)):
                    at_most(-error - totals[i], grid[end] - T)
                    at_most(error + totals[i], T - grid[end - 1])
                at_most(cum(0, b) + error, grid[b])
                initials = [1] if high else range(1, n)
                for i in initials:
                    at_most(cum(i, a) + error, grid[a])
                if high:
                    at_most(error - totals[1], 0)
                result = linprog(-error, A_ub=rows, b_ub=rhs,
                                 A_eq=eq, b_eq=np.ones(N),
                                 bounds=[(0, 1)] * (n * N) + [(0, None)],
                                 method="highs")
                assert result.success or result.status == 2, result.message
                if result.success:
                    best = max(best, result.x[-1])
    return best


def main():
    rng = Random(7341)
    cases = [(n, list(map(Q, range(N + 1))))
             for n in (3, 4, 5, 7) for N in (1, 2, 3, 4, 5)]
    cases += [(5, list(map(Q, range(10))))]
    for n in (3, 4, 5, 8):
        for N in (2, 4, 6):
            grid = [Q(0)]
            for _ in range(N):
                grid.append(grid[-1] + Q(rng.randint(1, 11), rng.randint(1, 7)))
            cases.append((n, grid))
    for n, grid in cases:
        value, winner = minimax(n, grid)
        assert minimax_lp(n, grid)[0] == value
        assert abs(float(value) - uncompressed(n, grid)) < 1e-7
        if winner is not None:
            matrix = witness_matrix(n, grid, winner)
            assert all(sum(matrix[i][k] for i in range(n)) == 1
                       for k in range(len(grid) - 1))
            assert all(0 <= x <= 1 for row in matrix for x in row)
            assert direct_error(matrix, grid) == value
    old = [[Q(x, 10) for x in row] for row in
           [[5, 7, 4, 0, 0, 10, 0, 0, 0], [5, 0, 0, 1, 10, 0, 0, 0, 0],
            [0, 0, 6, 0, 0, 0, 0, 10, 0], [0, 0, 0, 6, 0, 0, 10, 0, 0],
            [0, 3, 0, 3, 0, 0, 0, 0, 10]]]
    new = [[Q(2, 5)] * 4 + [Q(0)] + [Q(1, 4)] * 4,
           [Q(3, 20)] * 4 + [Q(1)] + [Q(0)] * 4]
    new += [[Q(3, 20)] * 4 + [Q(0)] + [Q(1, 4)] * 4 for _ in range(3)]
    assert direct_error(old, list(map(Q, range(10)))) == Q(17, 5)
    assert direct_error(new, list(map(Q, range(10)))) == Q(17, 5)
    print(f"Passed {len(cases)} exact formula/compressed LP/full-control LP comparisons;")
    print("all returned witnesses pass original exact cumulative-error enumeration;")
    print("both old and three-phase N=9,n=5 witnesses have exact error 17/5.")


if __name__ == "__main__":
    main()
