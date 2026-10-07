"""M4: run Report A's exact star oracle (read-only import) on the overlap
objective D and on the reduced objective D~, and check the gain corollary
numbers: both pair minima zero, star minimum 1/128.
Bytecode writing is disabled so nothing is written under research-*/."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import sys
sys.dont_write_bytecode = True
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261002-convexification/theory'))
from fractions import Fraction as F
from quadratic_star import support_star

box = [(0, 1), (0, 1), (0, 1)]      # variables (x, y, z), center y = index 1
D = {(0, 2, 0): F(2), (0, 1, 0): F(-1, 2), (1, 1, 0): F(-1), (0, 1, 1): F(-5, 4),
     (1, 0, 0): F(5, 4), (2, 0, 0): F(-3, 4), (0, 0, 1): F(1), (0, 0, 2): F(-39, 64),
     (0, 0, 0): F(1, 16)}
cert = support_star(box, [], D, center=1)
assert cert["status"] == "complete"
assert F(cert["bound"]) == F(1, 128), cert["bound"]
assert [F(v) for v in cert["minimizer"]] == [F(1), F(11, 16), F(1)], cert["minimizer"]

Dt = {(0, 2, 0): F(2), (0, 1, 0): F(-1, 2), (1, 1, 0): F(-1), (0, 1, 1): F(-5, 4),
      (1, 0, 0): F(1, 2), (0, 0, 1): F(25, 64), (0, 0, 0): F(1, 16)}
cert2 = support_star(box, [], Dt, center=1)
assert F(cert2["bound"]) == F(1, 128)

# gain corollary: pair objectives D_L(x,y), D_R(y,z) on the unit square
DL = {(0, 2, 0): F(1), (0, 1, 0): F(-1, 2), (1, 1, 0): F(-1), (1, 0, 0): F(5, 4),
      (2, 0, 0): F(-3, 4), (0, 0, 0): F(1, 16)}
DR = {(0, 2, 0): F(1), (0, 1, 1): F(-5, 4), (0, 0, 1): F(1), (0, 0, 2): F(-39, 64)}
bL = F(support_star(box, [], DL, center=1)["bound"])
bR = F(support_star(box, [], DR, center=1)["bound"])
assert bL == 0 and bR == 0
assert F(cert["bound"]) - bL - bR == F(1, 128)
print("M4_star_oracle: star oracle returns 1/128 at (1,11/16,1) for D and 1/128 for D~;"
      " pair minima 0, 0; gain 1/128.")

# ---- gain Delta versus the gap of the glued pair hulls R -------------------
# Nested family member: a=0, b=3, c=1, d=1, y in [0,3]; A={0,3}, C={1,2}.
import sympy as sp
xs, ys, zs = sp.symbols("x y z")


def to_dict(expr):
    P = sp.Poly(sp.expand(expr), xs, ys, zs)
    return {m: F(int(c.p), int(c.q)) for m, c in P.terms()}


qL = (ys - 3 * xs) ** 2 + 9 * xs * (1 - xs)
qR = (ys - 1 - zs) ** 2 + zs * (1 - zs)
boxN = [(0, 1), (0, 3), (0, 1)]
bL = F(support_star(boxN, [], to_dict(qL), center=1)["bound"])
bR = F(support_star(boxN, [], to_dict(qR), center=1)["bound"])
bstar = F(support_star(boxN, [], to_dict(qL + qR), center=1)["bound"])
assert (bL, bR, bstar) == (0, 0, F(1, 2)), (bL, bR, bstar)
# Exact lower bound for the glued pair hulls R via the quadratic multiplier
# p(y) = -gam (y-m)^2 with m = 3/2, R = 1/2, r = 3/2, gam = 1/2:
m, gam = F(3, 2), F(1, 2)
k1 = min(gam / (1 + gam) * (s - m) ** 2 for s in (F(0), F(3)))    # outer set A
k2 = min(-gam / (1 - gam) * (t - m) ** 2 for t in (F(1), F(2)))   # inner set C
assert k1 + k2 == F(1, 2)
print("M4_star_oracle: nested member A={0,3}, C={1,2}: Delta = 1/2 but the glued"
      " pair hulls R already certify 1/2 (R-gap 0).")
