"""W5 front verification: exact checks of the abstract's scope sentence.

Abstract: point growth with ratio kappa = max{1, L/g} forces
  (i)  lambda_min(H_{J0J0}) >= 2 L / kappa, and
  (ii) F(x') - min F >= L |x' - x*|^2 / kappa for every x' (in particular every
       other local minimizer).
Both follow from H_{J0J0} >= 2 g I (Lemma lem:growthcert(b)), growth, and
g >= L / kappa. Checked on the block of Example ex:family (g = 1/2, L = 21/8,
kappa = 21/4, J0 = {omega}) on a rational grid, and g >= L/kappa on random
rational pairs.
"""
from fractions import Fraction as Fr
import random

def phi(u, v, w):
    return u*u + v*v - 4*u*v + Fr(1, 4)*(u + v) + (w - u/2)**2

xs = (Fr(1), Fr(1), Fr(1, 2))
OPT = phi(*xs)
g, L = Fr(1, 2), Fr(21, 8)
kappa = max(Fr(1), L / g)
assert kappa == Fr(21, 4)
# (i) J0 = {omega}; H_{omega,omega} = 2.
assert Fr(2) >= 2 * L / kappa
# (ii) on a grid of [0,1]^3, including the strict local minimizer (0,0,0)
N = 16
worst = None
for i in range(N + 1):
    for j in range(N + 1):
        for k in range(N + 1):
            x = (Fr(i, N), Fr(j, N), Fr(k, N))
            d2 = sum((a - b)**2 for a, b in zip(x, xs))
            gap = phi(*x) - OPT
            assert gap >= L * d2 / kappa, x
            if d2 > 0:
                r = gap / d2
                worst = r if worst is None else min(worst, r)
assert worst >= g
# g >= L/kappa for random rational pairs
rng = random.Random(1)
for _ in range(10000):
    L1 = Fr(rng.randint(0, 50), rng.randint(1, 50))
    g1 = Fr(rng.randint(1, 50), rng.randint(1, 50))
    k1 = max(Fr(1), L1 / g1)
    assert g1 >= L1 / k1
print("ex:family block: min ratio (F-OPT)/|x-x*|^2 on grid =", worst,
      ">= g =", g, "; L/kappa =", L / kappa)
print("front-verify scope checks passed")
