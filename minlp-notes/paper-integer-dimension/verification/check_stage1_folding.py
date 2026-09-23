"""Check the projected lower boundary of the continuous folding LP.

This numerical check exercises the relaxed internal folding inequalities,
including choices that do not follow the exact folding graph. It is not a
substitute for the backward optimization proof in the manuscript.
"""
import numpy as np
from scipy.optimize import linprog

count = 0
for depth in range(1, 8):
    weights = 4.0 ** -np.arange(1, depth + 1)
    for x in np.linspace(0.0, 1.0, 65):
        rows, rhs = [], []
        for j in range(depth):
            row = np.zeros(depth)
            row[j] = 1
            if j == 0:
                rows.append(row.copy()); rhs.append(2*x)
                rows.append(row.copy()); rhs.append(2*(1-x))
            else:
                row[j-1] = -2
                rows.append(row.copy()); rhs.append(0)
                row[j-1] = 2
                rows.append(row.copy()); rhs.append(2)
        sol = linprog(-weights, A_ub=rows, b_ub=rhs,
                      bounds=[(0, 1)] * depth, method='highs')
        assert sol.success, sol.message
        g, exact = x, 0.0
        for weight in weights:
            g = min(2*g, 2*(1-g))
            exact += weight*g
        assert abs(-sol.fun-exact) < 1e-9, (depth, x, sol.fun, exact)
        lower = x + sol.fun - 4.0**-depth/4
        assert x*x - 4.0**-depth/4 - 1e-9 <= lower <= x*x + 1e-9
        count += 1
print(f'PASS: {count} projected folding LP checks at depths 1 through 7.')
