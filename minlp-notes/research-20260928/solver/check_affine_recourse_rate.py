"""Targeted finite checks for affine-recourse-rate-boundary.md.

Symbolic identities and rational Fourier checks are exact. Sampled positivity
and finite-grid minimax LP checks are numerical diagnostics, not proof of a
uniform approximation bound or of the infinite sequence of SDP bounds.
"""

import json
from fractions import Fraction

import numpy as np
from numpy.polynomial.chebyshev import chebval, chebvander
from scipy.optimize import linprog
import sympy as sp


x, y, z, s, p, delta = sp.symbols("x y z s p delta", real=True)
assert sp.expand((1 + x) * (p - y) / 2 + (1 - x) * (p + y) / 2
                 - (p - x * y)) == 0
assert sp.expand((1 + s) * (z - y) / 2 + (1 - s) * (z + y) / 2
                 - (z - y * s)) == 0
assert sp.expand((y*s + delta - x*y) + (z-y*s) - (-x*y+z+delta)) == 0
assert sp.expand((1 + x)**2 * (z - y) / 4
                 + (1 - x)**2 * (z + y) / 4
                 + (1 - x*x) * z / 2 - (-x*y + z)) == 0
for sign in [-1, 1]:
    assert sp.expand((1 + sign*x)**2 / 4 + (1 - x*x) / 4
                     - (1 + sign*x) / 2) == 0

lower_checks = 0
for n in range(81):
    N = n + 1 if (n + 1) % 2 == 0 else n + 2
    frequencies = {2*N: Fraction(1)}
    for j in range(1, N):
        frequencies[2*N-j] = Fraction(N-j, N)
        frequencies[2*N+j] = Fraction(N-j, N)
    assert min(frequencies) > n
    assert sum(weight for k, weight in frequencies.items() if k % 2 == 0) == N / 2
    pi_integral = sum(2*weight / (k*k-1)
                      for k, weight in frequencies.items() if k % 2 == 0)
    assert pi_integral >= Fraction(1, 9*N) >= Fraction(1, 9*(n+2))
    lower_checks += 1

kernel_rows = []
grid = np.linspace(-1, 1, 20001)
for m in [2, 3, 4, 8, 16, 32, 64]:
    b = {j: m-abs(j) for j in range(1-m, m)}
    a = {k: sum(bj*b.get(j-k, 0) for j, bj in b.items())
         for k in range(2*m-1)}
    g = {k: Fraction(ak, a[0]) for k, ak in a.items()}
    assert a[0] == (2*m**3+m)//3
    assert 1-g[1] == Fraction(3, 2*m*m+1)
    # pi*s has exact rational Chebyshev coefficients.
    scaled_s = [Fraction(0)] * (2*m-1)
    for k in range(1, 2*m-1, 2):
        scaled_s[k] = 4*g[k]*((-1)**((k-1)//2))/k
    assert scaled_s[-1] == 0 and scaled_s[-2] != 0
    assert all(scaled_s[k] == 0 for k in range(0, len(scaled_s), 2))
    values = chebval(grid, np.array([float(a)/np.pi for a in scaled_s]))
    defect = np.abs(grid)-grid*values
    bound = 2*np.sqrt(6/(2*m*m+1))
    assert np.max(np.abs(values)) <= 1+1e-12
    assert np.min(defect) >= -1e-12
    assert np.max(defect) <= bound+1e-12
    kernel_rows.append({"m": m, "sampled_max_defect": float(np.max(defect)),
                        "proved_defect_bound": float(bound)})

# The domain is sampled, so these are finite LP diagnostics only. The dual
# variables give two numerical probability measures with matching Chebyshev
# moments and discrepancy twice the sampled minimax error.
lp_rows = []
nodes = np.cos(np.linspace(0, np.pi, 8193))
h = np.abs(nodes)
for n in [2, 4, 8, 16, 32]:
    V = chebvander(nodes, n)
    objective = np.zeros(n+2)
    objective[-1] = 1
    A = np.vstack([np.column_stack([V, -np.ones(len(nodes))]),
                   np.column_stack([-V, -np.ones(len(nodes))])])
    result = linprog(objective, A_ub=A, b_ub=np.r_[h, -h],
                     bounds=[(None, None)]*(n+1)+[(0, None)], method="highs")
    assert result.success, result.message
    upper, lower = np.split(-result.ineqlin.marginals, 2)
    alpha, beta = 2*lower, 2*upper
    residual = float(np.max(np.abs(V.T @ (alpha-beta))))
    discrepancy = float(h @ (alpha-beta))
    assert abs(np.sum(alpha)-1) < 1e-7
    assert abs(np.sum(beta)-1) < 1e-7
    assert residual < 1e-7
    assert abs(discrepancy-2*result.fun) < 1e-7
    lp_rows.append({"n": n, "sampled_E_n": float(result.fun),
                    "n_times_sampled_E_n": float(n*result.fun),
                    "moment_residual": residual,
                    "measure_discrepancy": discrepancy})

print(json.dumps({"exact_polynomial_identities": 6,
                  "exact_Fourier_lower_bound_checks": lower_checks,
                  "kernel_diagnostics": kernel_rows,
                  "finite_grid_minimax_diagnostics": lp_rows}, indent=2))
