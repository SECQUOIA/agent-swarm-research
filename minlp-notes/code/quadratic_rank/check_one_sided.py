"""LP checks for positive-square epigraph components and signed combinations.

The positive component has relaxed tooth auxiliaries and zero binaries;
this differs from fixing a branch of the square graph relaxation.
"""
import math
import numpy as np
from scipy.optimize import linprog


def interpolant(depth, x):
    tooth = float(x)
    val = float(x)
    for j in range(1, depth + 1):
        tooth = min(2 * tooth, 2 * (1 - tooth))
        val -= 4 ** (-j) * tooth
    return val


def positive_epigraph_boundary(depth, x):
    # Variables g_1,...,g_depth,t; g_0=x is fixed.
    rows, rhs = [], []
    for j in range(1, depth + 1):
        for sign in (-1, 1):
            row = np.zeros(depth + 1)
            row[j - 1] = 1
            if j > 1:
                row[j - 2] = 2 * sign
                bound = 0 if sign == -1 else 2
            else:
                bound = 2 * x if sign == -1 else 2 * (1 - x)
            rows.append(row)
            rhs.append(bound)
    for j in range(depth + 1):
        row = np.zeros(depth + 1)
        row[-1] = -1
        for k in range(1, j + 1):
            row[k - 1] = -4 ** (-k)
        rows.append(row)
        rhs.append(-x + 4 ** (-j) / 4)
    for bound in (0, 1 - 2 * x):
        row = np.zeros(depth + 1)
        row[-1] = -1
        rows.append(row)
        rhs.append(bound)
    objective = np.zeros(depth + 1)
    objective[-1] = 1
    out = linprog(objective, A_ub=rows, b_ub=rhs,
                  bounds=[(0, 1)] * depth + [(None, None)], method='highs')
    assert out.success
    return out.fun


for depth in range(6):
    grid = np.linspace(0, 1, 2 ** (depth + 3) + 1)
    lower_error = max(x * x - positive_epigraph_boundary(depth, x) for x in grid)
    upper_error = max(interpolant(depth, x) - x * x for x in grid)
    assert math.isclose(lower_error, 2 ** (-2 * depth - 4), abs_tol=1e-10)
    assert math.isclose(upper_error, 2 ** (-2 * depth - 2), abs_tol=1e-10)
    # f=3u^2-5v^2: the minimum relaxed epigraph output is
    # 3 times the LP positive boundary minus 5 times the hypograph upper bound.
    worst_signed_error = 3 * lower_error + 5 * upper_error
    assert worst_signed_error <= 8 * 2 ** (-2 * depth - 2) + 1e-10
    print(f'PASS depth {depth}: positive LP error={lower_error:.10g}, '
          f'negative hypograph error={upper_error:.10g}')
print('PASS: signed epigraph error allocation at every tested depth')
