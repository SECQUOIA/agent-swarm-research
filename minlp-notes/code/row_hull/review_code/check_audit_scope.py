"""Exact small witnesses for the 2026-09-22 row-hull statement corrections.

These check the scope errors in Corollary 1' and Remark 7, not the full
theorems or the floating-point implementation.
"""
from fractions import Fraction as F


# A concave tent is not strictly concave, but the singleton P={1/2} has a
# positive vertex gap. Checking only strictly concave items is insufficient.
x = F(1, 2)
assert min(x, 1 - x) == F(1, 2)

# A slack strictly inside its interval does not prevent hull improvement.
z, slack, residual = F(3, 5), F(3, 10), F(1, 2)
assert 2 * z + slack == F(3, 2) and 0 < slack < F(3, 2)
lhs = 2 * min(z / residual, (1 - z) / (1 - residual), F(0))
rhs = (2 * z - 1) / residual
assert lhs == 0 and rhs == F(2, 5)

# A full item with width 1 and dual coefficient 2 contributes -2, even when
# every subset considered has the same cardinality.
assert residual * (1 - residual) - 2 == F(-7, 4)

print("3 exact rational scope checks passed")
