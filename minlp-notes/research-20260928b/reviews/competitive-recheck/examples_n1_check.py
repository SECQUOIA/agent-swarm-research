"""Examples N1 of n-dimensional.md, exact rationals (written for this recheck), and the
sufficient direction of the radius criterion in every dimension.

alpha = 1, B = [1/2, 1] x [0, 1], c = (3/4, 1/2), |r|^2 = 5/16, m = eps + k (x - 3/10)^2.
phi_B = m - q_B with q_B(y) = |r|^2 - |y - c|^2, so min_B phi_B >= M(c) - |r|^2 always:
|r| <= rho(c) implies validity in every dimension (only the converse fails).
Usage: python3 examples_n1_check.py
"""
from fractions import Fraction as Fr

eps = Fr(1, 1000)
r2 = Fr(1, 16) + Fr(1, 4)


def xpart_min(k):
    """min over x in [1/2, 1] of k (x - 3/10)^2 - (x - 1/2)(1 - x) (convex quadratic)."""
    a = k + 1                                         # coefficient of x^2
    b = -2 * k * Fr(3, 10) - Fr(3, 2)
    xs = -b / (2 * a)
    cands = [Fr(1, 2), Fr(1)] + ([xs] if Fr(1, 2) <= xs <= 1 else [])
    g = lambda x: k * (x - Fr(3, 10)) ** 2 - (x - Fr(1, 2)) * (1 - x)
    x = min(cands, key=g)
    return g(x), x


for k in (4, 10):
    vx, x = xpart_min(k)
    vz = -Fr(1, 4)                                    # min over z of -(z)(1-z)
    minphi = eps + vx + vz
    prox_x = (Fr(3, 10) * k + Fr(3, 4)) / (k + 1)
    M = eps + Fr(k, k + 1) * Fr(9, 20) ** 2           # M(c) = eps + min_x k(x-.3)^2 + (x-.75)^2
    print(f"k={k}: x-part min {vx} at x={x}; min phi_B = eps + {vx + vz} -> {'valid' if minphi >= 0 else 'invalid'}; "
          f"proximal x = {prox_x}; M(c) = eps + {M - eps} vs |r|^2 = {r2}")
    assert minphi >= M - r2                           # sufficient direction, as an inequality
assert xpart_min(4) == (Fr(4, 25), Fr(1, 2)) and xpart_min(10) == (Fr(2, 5), Fr(1, 2))
print("k=4: invalid box whose proximal point (x = 39/100) lies outside B  -> Proposition 1(b) fails")
print("k=10: valid box with M(c) < |r|^2                                  -> 'valid => |r| <= rho(c)' fails")
print("'|r| <= rho(c) => valid' holds in every dimension (min_B phi_B >= M(c) - |r|^2)")
