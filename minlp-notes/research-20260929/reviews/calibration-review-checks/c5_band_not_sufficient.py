"""Per-separator band membership of the costate tangent planes does not imply exactness.

Path of three bags a(s1), b(s1,s2), c(s2) on [-1,1]^2 (a transcription with x_1 = s1,
x_2 = s2 as successive states): a = 10 s1^2, c = 10 s2^2,
b = -5 exp(-((s1-0.8)^2 + (s2-0.8)^2)/0.01).  f* = 0 at the origin (interior), all
data smooth, costate slopes p1 = p2 = 0 (unique by Theorem 3.1(3)).
We check on a grid: (i) the constant 0 lies in Band_1 and Band_2 (up to the pinch
constant), (ii) the affine family with the costate slopes has bound -5 + O(grid), so it
is not exact; since the slopes are forced, no exact affine calibration exists.
"""
import json
import numpy as np

s = np.linspace(-1, 1, 2001)
S1, S2 = np.meshgrid(s, s, indexing="ij")
a = 10 * s**2
c = 10 * s**2
b = -5 * np.exp(-((S1 - 0.8) ** 2 + (S2 - 0.8) ** 2) / 0.01)
F = a[:, None] + b + c[None, :]
fstar = F.min()
i, j = np.unravel_index(F.argmin(), F.shape)
# Edge 1 (separator s1): child side = bag a, other side = b + c.
U1 = a
V1 = (b + c[None, :]).min(axis=1)
L1 = fstar - V1
# Edge 2 (separator s2): child side = bag c, other side = a + b.
U2 = c
V2 = (a[:, None] + b).min(axis=0)
L2 = fstar - V2
# constant psi = U(pinch) lies in band iff L <= const <= U everywhere
k1 = U1[i]
k2 = U2[j]
in_band1 = bool(np.all(L1 <= k1 + 1e-12) and np.all(k1 <= U1 + 1e-12))
in_band2 = bool(np.all(L2 <= k2 + 1e-12) and np.all(k2 <= U2 + 1e-12))
bound = a.min() + b.min() + c.min()  # affine family with slopes 0
out = {"fstar": float(fstar), "argmin": [float(s[i]), float(s[j])],
       "const_in_band1": in_band1, "const_in_band2": in_band2,
       "affine_bound_costate_slopes": float(bound), "gap": float(fstar - bound)}
print(json.dumps(out))
json.dump(out, open("logs/c5_band_not_sufficient.json", "w"), indent=1)
