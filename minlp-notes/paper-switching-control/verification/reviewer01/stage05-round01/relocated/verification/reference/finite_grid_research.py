"""Exact one-switch finite-grid minimax by a rational max/min formula.

The default algorithm uses only standard-library exact rational arithmetic.
The optional independent LP audit uses SciPy to discover primal/dual solutions;
Fraction arithmetic validates every certificate it accepts. That audit fails
closed if its bounded-denominator reconstruction cannot recover a certificate.
The proof is documented in notes/cia-reopened-finite-grid.md.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from itertools import product
import json

def rational(x):
    return Q(float(x)).limit_denominator(10**7)


def region(n, grid, a, b, kind):
    """Variables: u[0:3], v[3:6], m[6:9], E[9]."""
    T, ta, tb = grid[-1], grid[a], grid[b]
    ub, rhs, eq, erhs = [], [], [], []

    def add(terms, bound, equality=False):
        row = [Q(0)] * 10
        for index, value in terms.items():
            row[index] = Q(value)
        (eq if equality else ub).append(row)
        (erhs if equality else rhs).append(Q(bound))

    for offset, total in ((0, ta), (3, tb), (6, T)):
        add({offset: 1, offset + 1: 1, offset + 2: n - 2}, total, True)
    for j in range(3):
        add({j: -1}, 0)
        add({j: 1, j + 3: -1}, 0)
        add({j + 3: 1, j + 6: -1}, 0)
    add({7: 1, 6: -1}, 0)
    add({8: 1, 7: -1}, 0)
    add({9: -1}, -T / 3)
    for j, k in ((6, a), (7, b)):
        add({9: -1, j: -1}, grid[k] - T)
        add({9: 1, j: 1}, T - grid[k - 1])
    add({3: 1, 9: 1}, tb)
    add({1: 1, 9: 1}, ta)
    if kind == "low":
        add({2: 1, 9: 1}, ta)
    else:
        add({9: 1, 7: -1}, 0)
    return ub, rhs, eq, erhs


def solve_certified(data, objective):
    import numpy as np
    from scipy.optimize import linprog

    ub, rhs, eq, erhs = data
    c = [Q(0)] * 10
    c[objective] = -1
    res = linprog(np.array(c, dtype=float), A_ub=np.array(ub, dtype=float),
                  b_ub=np.array(rhs, dtype=float), A_eq=np.array(eq, dtype=float),
                  b_eq=np.array(erhs, dtype=float), bounds=[(None, None)] * 10,
                  method="highs")
    if res.status == 2:
        # Infeasibility is not used as a mathematical certificate here: these
        # regions are included in the separate universal upper-bound audit.
        return None
    if not res.success:
        raise RuntimeError(res.message)
    x = list(map(rational, res.x))
    y = list(map(rational, res.ineqlin.marginals))
    z = list(map(rational, res.eqlin.marginals))
    dot = lambda p, q: sum(a * b for a, b in zip(p, q))
    assert all(dot(row, x) <= bound for row, bound in zip(ub, rhs))
    assert all(dot(row, x) == bound for row, bound in zip(eq, erhs))
    assert all(value <= 0 for value in y)
    for j in range(10):
        assert sum(y[i] * ub[i][j] for i in range(len(ub))) + sum(
            z[i] * eq[i][j] for i in range(len(eq))) == c[j]
    assert dot(c, x) == dot(y, rhs) + dot(z, erhs)
    return x[objective], x


def certify_region_upper(data, bound):
    """Farkas certificate that this closed region has E <= bound.

    Works also for infeasible regions; thus no numerical status is trusted
    when certifying the universal bound.
    """
    import numpy as np
    from scipy.optimize import linprog

    ub, rhs, eq, erhs = data
    # Nonnegative multipliers on inequalities, free on equalities.
    # Their weighted row sum is the E unit vector, and weighted RHS <= bound.
    Aeq = np.concatenate((np.array(ub, dtype=float).T,
                           np.array(eq, dtype=float).T), axis=1)
    target = np.zeros(10)
    target[9] = 1
    objective = np.array(rhs + erhs, dtype=float)
    # Bounded feasibility avoids an unbounded objective on an empty region.
    result = linprog(np.zeros(len(objective)), A_ub=[objective],
                     b_ub=[float(bound)], A_eq=Aeq, b_eq=target,
                     bounds=[(0, None)] * len(rhs) + [(None, None)] * len(erhs),
                     method="highs")
    if not result.success:
        return False
    mul = list(map(rational, result.x))
    y, z = mul[:len(rhs)], mul[len(rhs):]
    assert all(v >= 0 for v in y)
    for j in range(10):
        assert sum(y[i] * ub[i][j] for i in range(len(ub))) + sum(
            z[i] * eq[i][j] for i in range(len(eq))) == (j == 9)
    assert sum(v * r for v, r in zip(mul, rhs + erhs)) <= bound
    return True


def minimax_lp(n, grid):
    grid = list(map(Q, grid))
    assert n >= 3 and grid[0] == 0
    assert all(a < b for a, b in zip(grid, grid[1:]))
    N = len(grid) - 1
    best, winner = grid[-1] / 3, None
    regions = []
    for a in range(1, N + 1):
        for b in range(a, N + 1):
            for kind in ("low", "high"):
                data = region(n, grid, a, b, kind)
                regions.append(data)
                solution = solve_certified(data, 9)
                if solution is None or solution[0] < best or (solution[0] == best and winner is not None):
                    continue
                best = solution[0]
                winner = (a, b, kind, solution[1])
    # Certify all regions, including those reported numerically infeasible.
    assert all(certify_region_upper(data, best) for data in regions), (
        "Could not certify a region upper bound")
    return best, winner



def witness_matrix(n, grid, winner):
    a, b, _, x = winner
    knots = [Q(0), Q(grid[a]), Q(grid[b]), Q(grid[-1])]
    states = [[Q(0)] * 3, x[:3], x[3:6], x[6:9]]
    matrix = []
    for g in [0, 1] + [2] * (n - 2):
        row = []
        for left, right in zip(grid, grid[1:]):
            block = 0 if right <= knots[1] else 1 if right <= knots[2] else 2
            row.append((states[block + 1][g] - states[block][g]) /
                       (knots[block + 1] - knots[block]))
        matrix.append(row)
    return matrix


def exact_schedule_error(matrix, grid):
    n = len(matrix)
    totals = [sum(a * (r - l) for a, l, r in zip(row, grid, grid[1:]))
              for row in matrix]
    best = grid[-1]
    for p, q in product(range(n), repeat=2):
        if p == q:
            continue
        cumulative = Q(0)
        omitted = max(totals[i] for i in range(n) if i not in (p, q))
        for k, time in enumerate(grid):
            if k:
                cumulative += matrix[p][k - 1] * (grid[k] - grid[k - 1])
            best = min(best, max(omitted, time - cumulative,
                                 grid[-1] - totals[q] - time))
    return best


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--modes", type=int, default=5)
    parser.add_argument("--intervals", type=int, default=9)
    parser.add_argument("--grid", help="Comma-separated rational grid endpoints")
    parser.add_argument("--audit-lp", action="store_true",
                        help="Also compare the independent rational-certified LP formulation")
    args = parser.parse_args()
    times = ([Q(s) for s in args.grid.split(",")] if args.grid else
             list(map(Q, range(args.intervals + 1))))
    from minimax import minimax

    value, witness = minimax(args.modes, times)
    if args.audit_lp:
        assert minimax_lp(args.modes, times)[0] == value
    print("Exact minimax:", value)
    if witness:
        matrix = witness_matrix(args.modes, times, witness)
        assert exact_schedule_error(matrix, times) == value
        print("Region:", witness[:3])
        print("Relaxed rows:", json.dumps([[str(q) for q in row] for row in matrix]))
