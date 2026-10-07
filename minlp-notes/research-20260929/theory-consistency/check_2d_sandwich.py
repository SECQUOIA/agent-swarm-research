"""Proposition 5.4(a) is special to dimension one: on the unit square,
L = max(0, x + y - 1) (convex) <= U = min(x, y) (concave), yet the affine
class has a positive band gap; with U + delta the gap stays positive for
delta < 1/2."""
import numpy as np
from consistency_lib import band_gap

t = np.linspace(0, 1, 101)
X, Y = np.meshgrid(t, t, indexing="ij")
x, y = X.ravel(), Y.ravel()
B = np.stack([np.ones_like(x), x, y], axis=1)
L = np.maximum(0, x + y - 1)
with open("logs/check_2d_sandwich.log", "w") as fh:
    for delta in [0.0, 0.1, 0.25, 0.4, 0.5, 0.6]:
        U = np.minimum(x, y) + delta
        g, *_ = band_gap(B, U, L)
        msg = f"delta={delta:.2f}: min(U-L)={np.min(U - L):.2f}, affine band gap = {g:.4f}"
        print(msg); fh.write(msg + "\n")
