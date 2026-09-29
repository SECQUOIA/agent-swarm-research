"""Reviewer's check of the (QG) constant in Example 7.3: on the unit sphere,
m(y) = sum_i (c_1 - c_i) y_i^2 >= c_g dist(y, M)^2 with c_g = (c_1 - c_{k+1})/2, where M is the unit
sphere of the top-k eigenspace.  Random points on S^{n-1}; reports min m/dist^2 and c_g.
Also checks the two-point constant of the unit circle (tau = 1): dist(z-y, T_y S) <= |z-y|^2/2.
Usage: python3 qg_example73.py
"""
import numpy as np
rng = np.random.default_rng(5)
for c in ([1, 1, .5], [1, .5, .25], [1, 1, 1, .3], [2, 2, 1.9, 0.1]):
    c = np.array(c, float); n = len(c); k = int(np.sum(c == c.max()))
    Y = rng.normal(size=(400000, n)); Y /= np.linalg.norm(Y, axis=1, keepdims=True)
    Y[:1000, k:] *= 1e-3; Y[:1000] /= np.linalg.norm(Y[:1000], axis=1, keepdims=True)  # near M
    m = ((c.max() - c) * Y ** 2).sum(1)
    top = Y[:, :k]; r = np.linalg.norm(top, axis=1)
    proj = np.where(r[:, None] > 0, top / np.maximum(r, 1e-300)[:, None], np.eye(k)[0])
    d2 = ((Y[:, :k] - proj) ** 2).sum(1) + (Y[:, k:] ** 2).sum(1)
    cg = (c.max() - c[k]) / 2 if k < n else float('nan')
    print(f"c={c.tolist()}: min m/dist^2 = {np.min(m / np.maximum(d2, 1e-300)):.4f}, claimed c_g = {cg:.4f}")
t = rng.uniform(0, 2 * np.pi, (200000, 2))
Yp = np.stack([np.cos(t[:, 0]), np.sin(t[:, 0])], 1); Zp = np.stack([np.cos(t[:, 1]), np.sin(t[:, 1])], 1)
T = np.stack([-np.sin(t[:, 0]), np.cos(t[:, 0])], 1)
D = Zp - Yp
perp = np.abs(D[:, 0] * T[:, 1] - D[:, 1] * T[:, 0])
print(f"circle two-point: max dist(z-y,T_yS)/(|z-y|^2/2) = {np.max(perp / ((D ** 2).sum(1) / 2)):.6f} (claimed <= 1, equality)")
