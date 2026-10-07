"""Random search (reviewer): uniform chains sum u(x_i) + b sum x_i x_{i+1}, u quartic, whose bond phi has an
off-diagonal minimizer (a, c) and whose even-n grid-DP optimum has a phase wall away from both ends."""
import sys
import numpy as np
G = np.linspace(-1, 1, 801)
def dp(u, b, n):
    uG = u(G); V = uG.copy(); back = []
    for i in range(1, n):
        M = V[:, None] + b * G[:, None] * G[None, :]
        j = np.argmin(M, axis=0); back.append(j)
        V = M[j, np.arange(len(G))] + uG
    kk = int(np.argmin(V)); path = [kk]
    for j in reversed(back):
        kk = int(j[kk]); path.append(kk)
    return float(V.min()), G[np.array(path[::-1])]
rng = np.random.default_rng(int(sys.argv[1]))
X, Y = np.meshgrid(G[::4], G[::4], indexing="ij")
found = 0
for trial in range(4000):
    co = np.r_[0.0, rng.uniform(-2, 2, 4)]
    b = rng.uniform(-2, 2)
    u = lambda t, co=co: np.polynomial.polynomial.polyval(t, co)
    P = 0.5 * (u(X) + u(Y)) + b * X * Y
    k = np.unravel_index(np.argmin(P), P.shape)
    a_, c_ = G[::4][k[0]], G[::4][k[1]]
    if abs(a_ - c_) < 0.3:
        continue
    # second minimum must be the mirror (c,a) only: check gap to other points
    far = (np.hypot(X - a_, Y - c_) > 0.15) & (np.hypot(X - c_, Y - a_) > 0.15)
    if P[far].min() - P[k] < 0.01:
        continue
    n = 14
    fs, xs = dp(u, b, n)
    lab = []
    for i in range(n - 1):
        d1 = np.hypot(xs[i] - a_, xs[i + 1] - c_); d2 = np.hypot(xs[i] - c_, xs[i + 1] - a_)
        ph = (0 if d1 < d2 else 1) ^ (i % 2)
        lab.append(ph if min(d1, d2) < 0.05 else -1)
    lab = np.array(lab)
    good = lab[lab >= 0]
    # wall in the middle: phase label changes between bonds 3..n-5 and both sides are clean
    left, right = lab[:4], lab[-4:]
    if np.all(left >= 0) and np.all(right >= 0) and len(set(left)) == 1 and len(set(right)) == 1 and left[0] != right[0]:
        found += 1
        print(f"coef={np.round(co, 3).tolist()} b={b:.3f} (a,c)=({a_:.2f},{c_:.2f}) f*={fs:.5f} x*={np.round(xs, 2).tolist()} labels={lab.tolist()}", flush=True)
        if found >= 6:
            break
print("found", found)
