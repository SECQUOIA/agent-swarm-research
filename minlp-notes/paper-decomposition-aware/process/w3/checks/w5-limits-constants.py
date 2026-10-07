"""Checks for the W5 edits in Section 10 / Appendix G (limits group).

1. (1+log2 k)^2 <= 4k for k >= 1, hence f(p,k) <= 4 c0 (c1 p)^p k^(p/2+2).
   h(t) = 4*2^t - (1+t)^2, t = log2 k >= 0: h(0) = 3 and h'(t) > 0 (checked
   at the minimizer of h' and on a fine grid).
2. (I+2)^5 <= 3^5 I^5 for integers I >= 1.
3. DK two-item instance with c = 2^k: ell = ceil(log2(2c)) = k+1, 5*ell+2 = 5k+7
   variables, 80*ell*c^2 = 80(k+1)4^k.
4. Oracle barrier: (1/(2 sqrt(6 eps)) - 1)^n - 1 >= (1/(4 sqrt(6 eps)))^n - 1 for
   eps <= 1/96, i.e. Omega(eps^{-n/2}).
"""
from fractions import Fraction as Fr
import math

# 1
ln2 = math.log(2)
t_star = math.log2(1 / (2 * ln2 ** 2))           # minimizer of h'
hp = lambda t: 4 * ln2 * 2 ** t - 2 * (1 + t)
assert hp(t_star) > 0.7 and hp(0) > 0
assert all(4 * 2 ** (j / 1000) - (1 + j / 1000) ** 2 > 0 for j in range(0, 200001))
for k in [Fr(1), Fr(3, 2), Fr(2), Fr(10), Fr(10**6)]:
    assert (1 + math.log2(k)) ** 2 <= 4 * k
# 2
assert all((I + 2) ** 5 <= 3 ** 5 * I ** 5 for I in range(1, 10000))
# 3
for k in range(1, 60):
    c = 2 ** k
    ell = math.ceil(math.log2(2 * c))
    assert ell == k + 1 and 5 * ell + 2 == 5 * k + 7 and 80 * ell * c * c == 80 * (k + 1) * 4 ** k
# 4: 1/(2 sqrt(6 eps)) - 1 >= 1/(4 sqrt(6 eps)) iff sqrt(6 eps) <= 1/4 iff eps <= 1/96
for e in [Fr(1, 96), Fr(1, 1000), Fr(1, 10**8)]:
    r = 1 / (2 * math.sqrt(6 * e))
    assert r - 1 >= r / 2 - 1e-12
print('PASS')
