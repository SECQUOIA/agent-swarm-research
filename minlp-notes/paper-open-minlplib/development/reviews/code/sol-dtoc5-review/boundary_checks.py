"""Targeted checks of the two certificate boundaries, using copied inputs only."""
from fractions import Fraction as F
from pathlib import Path
import gzip
import os

os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
work = Path(__file__).resolve().parent
point = {}
with gzip.open(work / 'dtoc5_point.txt.gz', 'rt') as stream:
    for line in stream:
        if line.strip() and not line.startswith('#'):
            name, value = line.split()
            point[name] = F(value)
h = F(1, 50000)
T = 49999

# A tiny perturbation is an exact infeasibility, despite its small size.
delta = F('1e-60')
t = 498
row = -h * (point[f'x{2+t}'] + delta) + point[f'x{50001+t}']
row -= point[f'x{50002+t}']
row += 4 * h * point[f'x{50001+t}'] ** 2
assert row == -h * delta != 0
print('Perturb x500 by 1e-60: OSIL row e500 residual is exactly', row)

# Without the last override, the terminal slope is nonzero; its infimum on
# the free terminal coordinate is minus infinity, despite convexity.
original_last = -2 * point['x50000']
assert original_last > 0
assert 'x100000' in point
print('Without the override: positive terminal slope', original_last)
print('L(y_T=-N) tends to -infinity as N tends to infinity')

# Applying lambda=-2u to the OSIL row, instead of its negative, produces a
# negative state-square coefficient already at the first free state.
wrong_lambda = -2 * point['x3']
wrong_curvature = h + 4 * h * wrong_lambda
assert wrong_curvature < 0
print('Wrong row sign: negative coefficient on the first free state square')
print('PASS: exact infeasibility, terminal override, and row-sign checks')
