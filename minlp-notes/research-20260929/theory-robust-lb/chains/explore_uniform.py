"""Exploration: bulk structure of the balanced split on uniform chains
f_n = sum_i u(x_i) + b sum_i x_i x_{i+1} on [-1,1]^n, u(t) = t^2 - kappa t^4 + c t.

Prints, for a few parameter sets:
  * argmin of phi(x,y) = (u(x)+u(y))/2 + b x y over [-1,1]^2 (grid + refinement) and m = min phi;
  * f*_n by min-plus DP on a grid (an upper bound on f*_n, refined by L-BFGS-B from the DP point);
  * balanced-split root bound  sum_e min factor_e  and the class-(a) root bound (column generation).
Floating point; exploration only.
"""
import sys
import numpy as np
from scipy import optimize
sys.path.insert(0, "..")
from robust_bb import Family, Relax, PW  # noqa: E402

G = np.linspace(-1, 1, 2001)


def make_u(kappa, c):
    return lambda t: t * t - kappa * t ** 4 + c * t


def phi_min(u, b):
    X, Y = np.meshgrid(G, G, indexing="ij")
    P = 0.5 * (u(X) + u(Y)) + b * X * Y
    k = np.unravel_index(np.argmin(P), P.shape)
    r = optimize.minimize(lambda z: 0.5 * (u(z[0]) + u(z[1])) + b * z[0] * z[1], [G[k[0]], G[k[1]]],
                          bounds=[(-1, 1)] * 2, method="L-BFGS-B", options={"ftol": 1e-15, "gtol": 1e-12})
    return r.fun, r.x


def dp_fstar(u, b, n):
    """Min-plus DP on the grid; returns value and argmin path, refined by L-BFGS-B."""
    uG = u(G)
    V = uG.copy()
    back = []
    for i in range(1, n):
        M = V[:, None] + b * G[:, None] * G[None, :]
        j = np.argmin(M, axis=0)
        back.append(j)
        V = M[j, np.arange(len(G))] + uG
    k = int(np.argmin(V)); path = [k]
    for j in reversed(back):
        k = int(j[k]); path.append(k)
    x0 = G[np.array(path[::-1])]
    f = lambda x: float(np.sum(u(x)) + b * np.sum(x[:-1] * x[1:]))
    r = optimize.minimize(f, x0, bounds=[(-1, 1)] * n, method="L-BFGS-B", options={"ftol": 1e-15, "gtol": 1e-12})
    return min(r.fun, f(x0)), r.x


def fam_uniform(kappa, c, b, n):
    return Family([[0.0, c, 1.0, 0.0, -kappa] for _ in range(n)], [b] * (n - 1))


if __name__ == "__main__":
    for (kappa, c, b) in [(0.1, 0.0, 0.8), (0.1, 0.3, 0.8), (0.1, -0.3, 0.8), (0.4, 0.3, 0.5), (0.6, 0.2, 0.4), (0.6, 0.2, -0.4)]:
        u = make_u(kappa, c)
        m, am = phi_min(u, b)
        print(f"kappa={kappa} c={c} b={b}: min phi = {m:.6f} at {np.round(am, 4)}")
        for n in [2, 3, 4, 6, 8, 12]:
            fs, xs = dp_fstar(u, b, n)
            fam = fam_uniform(kappa, c, b, n)
            rel = Relax(fam, "env", "balanced", K=7)
            lo_b, up_b, _ = rel.bound(np.full(n, -1.0), np.full(n, 1.0), None, maxit=60, tol=1e-10)
            if n >= 3:
                rel = Relax(fam, "a", "balanced", K=7)
                lo_a, up_a, _ = rel.bound(np.full(n, -1.0), np.full(n, 1.0), None, maxit=80, tol=1e-10)
            else:
                lo_a = up_a = float("nan")
            print(f"  n={n:2d} f*={fs:.6f} (n-1)m={((n-1)*m):.6f} gap_bal=[{fs-up_b:.2e},{fs-lo_b:.2e}]"
                  f" gap_a=[{fs-up_a:.2e},{fs-lo_a:.2e}] x*={np.round(xs, 3)}", flush=True)
