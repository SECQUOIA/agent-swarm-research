"""Restricted split families: in the reduction, every violated split can be taken with
v in {0,1}^{n+2} (after flipping the signs of the basis vectors b_i), so separation over
0/1 (or 0/+-1) coefficient splits of unbounded support is NP-hard as well."""
from fractions import Fraction as F
from itertools import product
from exact_lattice import violators_pd
from check_reduction import Y_subset_sum, solutions, instances_small

mism = 0
checked = 0
for a, s in instances_small():
    n = len(a)
    Y = Y_subset_sum(a, s)
    D = [1] + [-1] * n + [1]  # Y' = D Y D  <->  basis (b0, -b_1, ..., -b_n, g)
    Yf = [[D[i] * D[j] * Y[i][j] for j in range(n + 2)] for i in range(n + 2)]
    viol = set(violators_pd(Yf))
    binary = {v for v in viol if all(x in (0, 1) for x in v)}
    expected = {(0,) + x + (1,) for x in solutions(a, s)}
    checked += 1
    if binary != expected or (bool(viol) != bool(solutions(a, s))):
        mism += 1
print(f"[0/1 splits] {checked} instances: violated 0/1 splits are exactly (0, x, 1) for subset-sum "
      f"solutions x, and no split at all is violated otherwise; mismatches: {mism}")
