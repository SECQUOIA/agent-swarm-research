"""A uniform chain with a boundary-layer gap for the balanced split (Section A.4 of robust-chains.md).

u is C^1 piecewise quadratic on [-1,1]: curvature K1 on [-1,p1] with u(t) = 0, u'(t) = -2 b t (bulk
equilibrium of the diagonal), curvature -K2 on [p1,p2], curvature K3 on [p2,1].  The chain is
f_n = sum_i u(x_i) + b sum_i x_i x_{i+1} on [-1,1]^n.

check(...) prints: the minimizer of phi(x,y) = (u(x)+u(y))/2 + b x y on a grid (hypothesis (H1) asks
for a unique diagonal minimizer (t,t)), the quadratic-growth constant kappa of psi = phi - min phi
around (t,t) on the grid, x* and f* by grid DP + L-BFGS-B, and the root gap of the balanced-split
per-factor envelope bound (column generation of robust_bb.Relax with class 'env').
Floating point.
"""
import sys
import numpy as np
from scipy import optimize
sys.path.insert(0, "..")
from robust_bb import PW, Family, Relax  # noqa: E402

G = np.linspace(-1, 1, 2001)


def make_pw(t, b, K1, p1, K2, p2, K3):
    """C^1 piecewise quadratic, coefficient arrays in powers of x."""
    # piece 1: u = 0 + s1 (x-t) + K1/2 (x-t)^2, s1 = -2 b t
    s1 = -2 * b * t
    def quad(x0, v0, d0, k):  # v0 + d0 (x-x0) + k/2 (x-x0)^2 in powers of x
        return np.array([v0 - d0 * x0 + 0.5 * k * x0 * x0, d0 - k * x0, 0.5 * k])
    c1 = quad(t, 0.0, s1, K1)
    v1 = np.polynomial.polynomial.polyval(p1, c1); d1 = s1 + K1 * (p1 - t)
    c2 = quad(p1, v1, d1, -K2)
    v2 = np.polynomial.polynomial.polyval(p2, c2); d2 = d1 - K2 * (p2 - p1)
    c3 = quad(p2, v2, d2, K3)
    return PW([-1.0, p1, p2, 1.0], [c1, c2, c3])


def dp_fstar(u, b, n):
    uG = u(G)
    V = uG.copy(); back = []
    for _ in range(1, n):
        M = V[:, None] + b * G[:, None] * G[None, :]
        j = np.argmin(M, axis=0); back.append(j)
        V = M[j, np.arange(len(G))] + uG
    k = int(np.argmin(V)); path = [k]
    for j in reversed(back):
        k = int(j[k]); path.append(k)
    x0 = G[np.array(path[::-1])]
    f = lambda x: float(np.sum(u(x)) + b * np.sum(x[:-1] * x[1:]))
    r = optimize.minimize(f, x0, bounds=[(-1, 1)] * n, method="L-BFGS-B", options={"ftol": 1e-15, "gtol": 1e-12})
    # second-best local configuration: DP value of the best path whose first coordinate is far from x*_1
    return min(r.fun, f(x0)), r.x


def check(params, b, ns=(3, 4, 6, 8), verbose=True):
    u = make_pw(*params[:1], b, *params[1:])
    g = G[::4]
    X, Y = np.meshgrid(g, g, indexing="ij")
    Pm = 0.5 * (u(X) + u(Y)) + b * X * Y
    k = np.unravel_index(np.argmin(Pm), Pm.shape)
    m = Pm[k]; t = params[0]
    mt = u(t) + b * t * t
    psi = Pm - mt
    d2 = (X - t) ** 2 + (Y - t) ** 2
    mask = d2 > 1e-12
    kappa = float(np.min(psi[mask] / d2[mask]))
    out = dict(phi_argmin=(round(g[k[0]], 4), round(g[k[1]], 4)), min_phi=m, phi_tt=mt, kappa=kappa)
    if verbose:
        print(out, flush=True)
    res = []
    for n in ns:
        fs, xs = dp_fstar(u, b, n)
        fam = Family([u] * n, [b] * (n - 1))
        rel = Relax(fam, "env", "balanced", K=7)
        lo, up, _ = rel.bound(np.full(n, -1.0), np.full(n, 1.0), None, maxit=80, tol=1e-10)
        res.append((n, fs, fs - up, fs - lo, np.round(xs, 3)))
        if verbose:
            print(f"  n={n} f*={fs:.6f} gap_bal in [{fs-up:.3e}, {fs-lo:.3e}] x*={np.round(xs, 3)}", flush=True)
    return out, res


if __name__ == "__main__":
    b = 0.6
    for params in [(0.2, 6.0, 0.3, 3.0, 0.6, 4.0), (0.2, 8.0, 0.28, 4.0, 0.55, 5.0), (0.2, 8.0, 0.3, 5.0, 0.5, 6.0),
                   (0.25, 6.0, 0.35, 4.0, 0.6, 5.0)]:
        print("params (t,K1,p1,K2,p2,K3) =", params, "b =", b)
        check(params, b)
