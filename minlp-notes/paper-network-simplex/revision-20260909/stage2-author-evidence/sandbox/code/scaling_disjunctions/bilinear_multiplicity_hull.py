"""
Hull of  F = {(n, X, T, W): n in {0,...,N}, X = sum_i xi_i, xi_i in [l,u], T in [lT,uT] shared, W = X*T}
(n identical units with per-unit extensive load xi_i and a shared intensive variable T).
Claim: conv(F) = conv( F_0 ∪ F_N ) = conv of six points
   (0,0,lT,0), (0,0,uT,0), (N, N l, lT, N l lT), (N, N l, uT, N l uT), (N, N u, lT, N u lT), (N, N u, uT, N u uT).
We (1) compute the facets of this 6-point polytope with qhull, (2) check by random sampling that
every point of F (any n, any split of X among units, any T) satisfies them, and (3) compare with the
naive 'McCormick with n-scaled bounds' relaxation, which is bilinear in (n,T) and therefore not usable
as a convex relaxation; we instead compare with the McCormick relaxation of W = X*T over the global box
X in [0, N u], T in [lT,uT] plus X in [n l, n u], and show the hull is strictly tighter.
"""
import numpy as np, itertools, random
from scipy.spatial import ConvexHull
from fractions import Fraction

N, l, u, lT, uT = 3, 1.0, 2.0, 0.5, 1.5
P = np.array([[0,0,lT,0],[0,0,uT,0],
              [N,N*l,lT,N*l*lT],[N,N*l,uT,N*l*uT],[N,N*u,lT,N*u*lT],[N,N*u,uT,N*u*uT]])
hull = ConvexHull(P)
# unique facets (qhull may triangulate)
eqs = np.unique(np.round(hull.equations, 9), axis=0)
print("facets (a.(n,X,T,W) + b <= 0):")
for e in eqs: print("  ", e)

random.seed(0)
viol = 0
for _ in range(20000):
    n = random.randint(0, N); T = random.uniform(lT, uT)
    X = sum(random.uniform(l, u) for _ in range(n)); W = X*T
    p = np.array([n, X, T, W])
    if np.any(eqs[:, :4] @ p + eqs[:, 4] > 1e-9): viol += 1
print("violations of the 6-point hull by points of F:", viol)

# strictness: point in McCormick-of-global-box ∩ {X in [n l, n u]} but outside the 6-point hull
# take n = 1.5, X = 1.5*u (max), T = uT: W must equal X*T in F; McCormick global upper bound allows W <= ...
def in_hull(p): return np.all(eqs[:, :4] @ p + eqs[:, 4] <= 1e-9)
def mccormick_global(X, T, W):
    XL, XU = 0.0, N*u
    return (W >= lT*X + XL*T - XL*lT - 1e-9 and W >= uT*X + XU*T - XU*uT - 1e-9 and
            W <= uT*X + XL*T - XL*uT + 1e-9 and W <= lT*X + XU*T - XU*lT + 1e-9)
cnt = 0; tot = 0
for _ in range(20000):
    n = random.uniform(0, N); X = random.uniform(n*l, n*u); T = random.uniform(lT, uT)
    # W range allowed by global McCormick
    Wlo = max(lT*X, uT*X + N*u*T - N*u*uT); Whi = min(uT*X, lT*X + N*u*T - N*u*lT)
    for W in np.linspace(Wlo, Whi, 5):
        tot += 1
        if mccormick_global(X, T, W) and not in_hull(np.array([n, X, T, W])): cnt += 1
print(f"points feasible for global McCormick ∩ {{X in [n l, n u]}} but cut off by the hull: {cnt}/{tot}")
