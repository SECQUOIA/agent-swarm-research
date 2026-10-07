"""Random search for uniform chains f_n = sum u(x_i) + b sum x_i x_{i+1} on [-1,1]^n (u a quartic)
whose balanced-split per-factor envelope bound has a clear root gap, while
  (H1) phi(x,y) = (u(x)+u(y))/2 + b x y has a unique, nondegenerate, diagonal minimizer (t,t), |t|<1,
  and the minimizer of f_n (n = 6) is unique on the grid DP up to 1e-3 and interior.
Prints candidates.  Exploration only (floating point).
"""
import sys
import numpy as np
sys.path.insert(0, "..")
from robust_bb import Family, Relax  # noqa: E402
from explore_uniform import dp_fstar, G  # noqa: E402


def check(coef, b, n=6, verbose=False):
    u = lambda t: np.polynomial.polynomial.polyval(t, coef)
    X, Y = np.meshgrid(G[::4], G[::4], indexing="ij")
    P = 0.5 * (u(X) + u(Y)) + b * X * Y
    k = np.unravel_index(np.argmin(P), P.shape)
    m = P[k]
    tx, ty = G[::4][k[0]], G[::4][k[1]]
    if abs(tx - ty) > 0.02 or abs(tx) > 0.9:
        return None
    # uniqueness of phi minimizer: second best away from (t,t)
    far = (np.abs(X - tx) + np.abs(Y - ty)) > 0.2
    if np.min(P[far]) - m < 0.02:
        return None
    fs, xs = dp_fstar(u, b, n)
    if np.max(np.abs(xs)) > 0.97:
        return None
    fam = Family([list(coef) for _ in range(n)], [b] * (n - 1))
    rel = Relax(fam, "env", "balanced", K=7)
    lo, up, _ = rel.bound(np.full(n, -1.0), np.full(n, 1.0), None, maxit=60, tol=1e-9)
    return dict(m=m, t=tx, fs=fs, gap_lo=fs - up, gap_hi=fs - lo, xs=np.round(xs, 3))


if __name__ == "__main__":
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    found = 0
    for trial in range(400):
        coef = np.concatenate([[0.0], rng.uniform(-1, 1, 4)])
        coef[2] = rng.uniform(0.0, 2.0)
        b = rng.uniform(-1, 1)
        r = check(coef, b)
        if r is not None and r["gap_lo"] > 5e-3:
            found += 1
            print(f"coef={np.round(coef, 3).tolist()} b={b:.3f} {r}", flush=True)
    print("found", found)
