"""Random stress test of Lemma 3.2 (projection to a face) for
m = x(1-x) + sum_{i>=2} y_i^4 on [0,0.9] x [-0.4,0.5]^(n-1), n = 2, 4.
Gradient Lipschitz constant (Euclidean) M = max(2, 12 * 0.5^2) = 3.
Checks m(z) <= (1+d)(1+n-d) m(y) + [(1+d)(n-d)+d] M s^2 on Q_F(y', s), sampling corners and random points."""
import itertools

import numpy as np

rng = np.random.default_rng(1)
M = 3.0
worst = 0.0
for n in (2, 4):
    lo = np.array([0.0] + [-0.4] * (n - 1))
    s0 = 0.9
    hi = lo + s0
    m = lambda Y: Y[..., 0] * (1 - Y[..., 0]) + np.sum(Y[..., 1:] ** 4, axis=-1)
    for trial in range(20000):
        # bias samples toward the boundary and the minimiser
        y = lo + s0 * rng.random(n) ** rng.choice([1, 3, 6])
        s = s0 / 2 * rng.random() ** rng.choice([1, 2, 4])
        dl, du = y - lo, hi - y
        I = np.minimum(dl, du) < s
        b = np.where(dl <= du, lo, hi)
        yp = np.where(I, b, y)
        d = n - int(I.sum())
        free = np.where(~I)[0]
        Z = [yp.copy()]
        for signs in itertools.product([-1, 0, 1], repeat=d):
            z = yp.copy(); z[free] += s * np.array(signs); Z.append(z)
        for _ in range(20):
            z = yp.copy(); z[free] += s * (2 * rng.random(d) - 1); Z.append(z)
        Z = np.array(Z)
        assert np.all(Z >= lo - 1e-12) and np.all(Z <= hi + 1e-12)
        bound = (1 + d) * (1 + n - d) * m(y) + ((1 + d) * (n - d) + d) * M * s * s
        worst = max(worst, float(np.max(m(Z)) / bound))
print(f"max over samples of m(z)/bound = {worst:.4f} (Lemma 3.2 requires <= 1)")
