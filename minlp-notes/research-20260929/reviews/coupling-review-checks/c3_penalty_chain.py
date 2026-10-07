"""Independent check of Example 2.4 (penalty chain) of the coupling note.

    F(x) = sum_i c x_i(1-x_i) + M sum_i (x_i - x_{i+1})^2,  sum x = n/2,  x in [0,1]^n.

1. OPT by a grid DP over (x_i, partial sum) with the row enforced exactly on
   the grid (an upper bound on OPT; the grid contains x = 1/2 and walls).
   Independent of the author's SLSQP multistart.
2. rho(a_t) for a two-term bag and a one-term bag, by the lower convex hull
   of the bag function on a grid of [0,1]^2 (envelope value at the worst point).
3. The M threshold: the smallest M on a grid for which the DP optimum equals
   c n/4, compared with the note's sufficient M = c n (n-1) and with the
   second-order threshold c / (2 - 2 cos(pi/n)).

Usage: python3 c3_penalty_chain.py
"""
import numpy as np
from scipy.spatial import ConvexHull

c = 1.0


def dp_opt(n, M, G=41):
    """min F on grid x_i in {0, 1/(G-1), ..., 1} with sum x = n/2 exactly.
    Partial sums are integer multiples of 1/(G-1)."""
    g = np.linspace(0, 1, G)
    S = (G - 1) * n + 1
    target = (G - 1) * n // 2
    assert (G - 1) * n % 2 == 0
    INF = np.inf
    unary = c * g * (1 - g)
    pair = M * (g[:, None] - g[None, :]) ** 2  # pair[x, x']
    V = np.full((G, S), INF)
    for j in range(G):
        V[j, j] = unary[j]
    for _ in range(n - 1):
        W = np.full((G, S), INF)
        for jp in range(G):
            # W[jp, s] = unary[jp] + min_j V[j, s - jp] + pair[j, jp]
            shifted = np.full((G, S), INF)
            shifted[:, jp:] = V[:, :S - jp]
            W[jp] = unary[jp] + np.min(shifted + pair[:, jp][:, None], axis=0)
        V = W
    return float(np.min(V[:, target]))


def rho_bag(two_terms, M, G=81):
    g = np.linspace(0, 1, G)
    X, Y = np.meshgrid(g, g, indexing="ij")
    A = c * X * (1 - X) + M * (X - Y) ** 2
    if two_terms:
        A = A + c * Y * (1 - Y)
    pts = np.c_[X.ravel(), Y.ravel(), A.ravel()]
    hull = ConvexHull(pts)
    # lower facets: normal with negative z component; envelope = max over lower facets
    best = -np.inf
    env = np.full(len(pts), -np.inf)
    for eq in hull.equations:
        a, b, cz, d = eq
        if cz < -1e-12:
            # plane a x + b y + cz z + d = 0 -> z = -(a x + b y + d)/cz
            env = np.maximum(env, -(a * pts[:, 0] + b * pts[:, 1] + d) / cz)
    return float(np.max(pts[:, 2] - env))


if __name__ == "__main__":
    print("[1] OPT by exact-row grid DP (G=41) vs note")
    for n in [6, 10, 16]:
        for M in [1.0, 10.0, c * n * (n - 1)]:
            print(f"    n={n:2d} M={M:6.1f}  DP OPT={dp_opt(n, M):.6f}  c n/4={c*n/4}")
    print("[2] per-bag nonconvexity rho(a_t) (grid hull, G=81)")
    for M in [1.0, 30.0, 240.0]:
        print(f"    M={M:6.1f}  two-term bag rho={rho_bag(True, M):.4f} (claim <= c/2)"
              f"   one-term bag rho={rho_bag(False, M):.4f} (claim <= c/4)")
    print("[3] smallest M (grid of M values) with DP OPT = c n/4, vs sufficient c n(n-1) and 2nd-order c/(2-2cos(pi/n))")
    for n in [6, 10, 16]:
        Ms = np.geomspace(0.5, c * n * (n - 1), 60)
        thr = None
        for M in Ms:
            if dp_opt(n, M) >= c * n / 4 - 1e-9:
                thr = M
                break
        print(f"    n={n:2d}  empirical threshold ~{thr:.2f}   c n(n-1)={c*n*(n-1):.0f}   2nd-order {c/(2-2*np.cos(np.pi/n)):.2f}")
