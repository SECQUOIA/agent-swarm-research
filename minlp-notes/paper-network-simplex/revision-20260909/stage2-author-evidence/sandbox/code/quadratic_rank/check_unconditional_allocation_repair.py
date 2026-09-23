"""Exact rational feasibility and high-precision hypograph repair checks.

This checks the explicit repair at a known log-product optimum, not an
implementation of the imported GLS weak-optimization algorithm.
"""

import random

import mpmath as mp
import sympy as sp

mp.mp.dps = 100
rng = random.Random(2026090555)
cases = 0
for rank in range(1, 7):
    for outputs in range(1, 5):
        raw = sp.Matrix(outputs, rank, lambda i, j: rng.randint(-3, 3))
        matrix = raw / (1 + 4 * sum(abs(value) for value in raw))
        # K is the Euclidean unit ball. p*=1 is feasible and has optimum
        # product one, while signed C also exercises the general oracle.
        optimum = sp.ones(rank, 1)
        assert (matrix * optimum).dot(matrix * optimum) <= 1
        bound = 1 + sum(abs(value) for value in matrix)
        exponent = 0
        delta = sp.Integer(1)
        while delta * rank * bound > sp.Rational(1, 4):
            exponent += 1
            delta /= 2
        lower = delta ** rank / 4
        box_height = rank * (rank * exponent + 2) + 4
        p_center = sp.ones(rank, 1) * delta / 2
        t_center = -rank * (exponent + 1) - 2
        sigma = min(delta / (16 * rank), 1 / (8 * bound), sp.Rational(1, 4))
        nu = sp.Rational(1, 8)
        rho = nu * sigma / (4 * (box_height + sigma + 1))
        # A rational weak optimizer outside both the coordinate cap and
        # log-product hypograph, at distance <=rho from (1,0).
        p_weak = optimum.copy()
        p_weak[0] += rho / 2
        t_weak = rho / 2
        assert (p_weak - optimum).dot(p_weak - optimum) + t_weak ** 2 <= rho ** 2
        p_fixed = (sigma * p_weak + rho * p_center) / (sigma + rho)
        t_fixed = (sigma * t_weak + rho * t_center) / (sigma + rho)
        assert all(lower <= value <= 1 for value in p_fixed)
        assert (matrix * p_fixed).dot(matrix * p_fixed) <= 1
        assert -box_height <= t_fixed <= 0
        assert -t_fixed <= nu
        logarithm = sum(mp.log(mp.mpf(str(sp.numer(value))) / mp.mpf(str(sp.denom(value)))) for value in p_fixed)
        t_value = mp.mpf(str(sp.numer(t_fixed))) / mp.mpf(str(sp.denom(t_fixed)))
        assert t_value <= logarithm + mp.mpf('1e-90')
        assert logarithm >= -float(nu) - mp.mpf('1e-90')
        cases += 1

print(f'PASS: {cases} rational central-ball repairs at a known optimum; '
      'exact coordinate/body/objective bounds and 100-digit log hypographs')
