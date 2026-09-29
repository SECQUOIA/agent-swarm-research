"""Absorption of boundary lattice points in an index set with an irrational
recession ray (d = 2).

Index set I = conv(sail vertices) + R_+ (1, alpha), where the sail vertices are
the upper-hull vertices of {(q, floor(alpha q)) : q >= 1} (best lower rational
approximations of alpha).  I has infinitely many extreme lattice points.

For a lattice point z of I we compute
    lam(z, T) = min { gauge_D(y - z) : y lattice point in int(I), y != z, x(y) <= T },
    D = conv({z} U W_T) - z,  W_T = lattice points of I with x <= T.
If y - z = sum_i mu_i (w_i - z) with w_i in W_T and sum mu_i = lam, then
y = (1 - lam) z + sum mu_i w_i, so any MICP fiber satisfies
A_y  contains  (1 - lam) A_z + sum mu_i A_{w_i}.
lam(z, T) -> 0 means A_z lies in the closure of the union of interior fibers.
Exact rational arithmetic is not needed: this is an illustration, not a proof.
"""
import math
import numpy as np
from scipy.spatial import ConvexHull


def sail_vertices(alpha, qmax):
    pts = [(q, math.floor(alpha * q)) for q in range(1, qmax + 1)]
    hull = []  # upper hull, left to right
    for p in pts:
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            # keep only right turns for the upper hull
            if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) >= 0:
                hull.pop()
            else:
                break
        hull.append(p)
    return hull


def chain_value(verts, x):
    for (x1, y1), (x2, y2) in zip(verts, verts[1:]):
        if x1 <= x <= x2:
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    return None


def lattice_points(alpha, verts, T):
    x0, y0 = verts[0]
    pts, interior = [], []
    for x in range(x0, T + 1):
        lo = y0 + alpha * (x - x0)          # ray from v0 in direction (1, alpha)
        hi = chain_value(verts, x)
        if hi is None:
            break
        for y in range(math.ceil(lo - 1e-12), math.floor(hi + 1e-12) + 1):
            pts.append((x, y))
            if lo + 1e-9 < y < hi - 1e-9:
                interior.append((x, y))
    return pts, interior


def best_absorption(z, pts, interior):
    P = np.array(pts + [z], dtype=float) - np.array(z, dtype=float)
    hull = ConvexHull(P)
    A = hull.equations[:, :2]
    b = -hull.equations[:, 2]          # facets: A v <= b
    best = (math.inf, None)
    for y in interior:
        v = np.array(y, dtype=float) - np.array(z, dtype=float)
        if not v.any():
            continue
        g = 0.0
        ok = True
        for a, bb in zip(A, b):
            av = a @ v
            if bb <= 1e-9:
                if av > 1e-9:
                    ok = False
                    break
            else:
                g = max(g, av / bb)
        if ok and g < best[0]:
            best = (g, y)
    return best


if __name__ == "__main__":
    for name, alpha in [("golden", (math.sqrt(5) - 1) / 2), ("sqrt2-1", math.sqrt(2) - 1)]:
        Tmax = 20000
        verts = sail_vertices(alpha, Tmax)
        print(f"alpha={name}: first sail vertices {verts[:7]}")
        for k in [0, 2, 4]:
            z = verts[k]
            row = []
            for T in [200, 2000, 20000]:
                pts, interior = lattice_points(alpha, verts, T)
                lam, y = best_absorption(z, pts, interior)
                row.append(f"T={T}: lam={lam:.4f} (lam*sqrt(T)={lam*math.sqrt(T):.2f}) y={y}")
            print(f"  z=v{k}={z}: " + "; ".join(row))
