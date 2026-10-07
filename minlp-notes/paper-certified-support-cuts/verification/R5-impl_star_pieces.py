"""R5-impl: the implemented star oracle splits at all pairwise intersections
of a leaf's bound lines, so its certificate can have more pieces than the
2m+4k+1 intervals of Theorem 5.4 (redundant rows below the leaf bound)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import sys
from fractions import Fraction as F
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261002-convexification/theory'))
from quadratic_star import support_star

# center y = index 0 in [0,1], one leaf x = index 1 in [0,1].
# Redundant lower rows x >= s*y - 2 - s/2 (always below 0 on [0,1]),
# written as  s*y - x <= 2 + s/2, pairwise intersecting inside (0,1) when
# the intercepts are perturbed.
# Redundant lower rows: tangents of y^2 - 5 at t_j, x >= 2 t_j y - t_j^2 - 5,
# i.e. 2 t_j y - x <= t_j^2 + 5. Pairwise intersections (t_i+t_j)/2 lie in (0,1).
ts = [F(1, 13), F(2, 11), F(3, 10), F(2, 5), F(1, 2), F(7, 12), F(2, 3), F(3, 4), F(5, 6), F(10, 11)]
rows = [((2 * t, F(-1)), t * t + 5) for t in ts]
coefficients = {(0, 2): F(-1), (1, 1): F(1), (1, 0): F(1, 3)}   # -x^2 + xy + y/3
cert = support_star(((F(0), F(1)), (F(0), F(1))), rows, coefficients, center=0)
m, k = len(rows), 1
print("status", cert["status"], "pieces", len(cert["pieces"]), "theorem bound 2m+4k+1 =", 2 * m + 4 * k + 1)
