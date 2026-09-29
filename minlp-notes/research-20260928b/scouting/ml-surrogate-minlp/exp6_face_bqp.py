"""Experiment 6: sanity check of the face construction in Theorem A (nonnegative weights).
Layer on [0,1]^n: y_ij = ReLU(x_i + x_j - 1) for i<j, u_i = ReLU(2 x_i - 1).
phi = sum_i (2 u_i - 2 x_i + 1) = sum_i |2 x_i - 1| is linear on the lifted space.
Check: max phi over graph vertices = n, attained exactly at the 2^n box vertices, and the
face (projected to (x,y)) has the facet count of the Boolean quadric polytope BQP(K_n)."""
from fractions import Fraction as Fr
from itertools import combinations
from hull_tools import graph_points, facets

for n in [3, 4]:
    pairs = list(combinations(range(n), 2))
    W, b = [], []
    for (i, j) in pairs:
        w = [0]*n; w[i] = 1; w[j] = 1; W.append(w); b.append(-1)
    for i in range(n):
        w = [0]*n; w[i] = 2; W.append(w); b.append(-1)
    pts = graph_points(W, b, [0]*n, [1]*n)
    k = len(W)
    def phi(p):
        x = p[:n]; u = p[n+len(pairs):]
        return sum(2*u[i] - 2*x[i] + 1 for i in range(n))
    vals = [phi(p) for p in pts]
    top = [p for p, v in zip(pts, vals) if v == max(vals)]
    boolean = all(all(xi in (0, 1) for xi in p[:n]) for p in top)
    F_full = facets(pts)
    face_xy = sorted({tuple(p[:n+len(pairs)]) for p in top})
    F_face = facets(face_xy)
    print(f"n={n}: layer neurons={k}, graph vertices={len(pts)}, max phi={max(vals)}, #maximizers={len(top)} (all Boolean: {boolean}), "
          f"facets of full hull={len(F_full)}, facets of face in (x,y) space={len(F_face)}")
