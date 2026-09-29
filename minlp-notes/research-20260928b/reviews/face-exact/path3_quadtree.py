"""Reviewer check of Proposition 4.7 (two centres) and an O(1/eps) upper construction.

f = |X1 - X2| + (X1 - X2) y on [0,1]^3, X_k = x_k - a_k, a1 = 1/3, a2 = sqrt2 - 1,
termwise McCormick on x1*y (c=+1) and -x2*y (c=-1).  Node bound by LP (scipy/HiGHS), own model code.

[1] optimal set: f >= 0 on a grid; zeros are {X1 = X2} and additionally {y = 1, X1 <= X2}.
[2] the four orthant boxes around (a1, a2) (full y range): LP bounds.
[3] upper bound: quadtree in (x1,x2) with full y-range; a square Q of side h is a leaf when
    h <= 2 eps (then sup Gamma <= h/2 <= eps) or min_Q |D| >= 2h (then Gamma <= 2h * (1-y or y) <= m).
    Every leaf's LP bound is checked >= -eps.  Leaves * eps should stay bounded (O(1/eps)).
"""
import math
import numpy as np
from scipy.optimize import linprog

A1, A2 = 1.0 / 3.0, math.sqrt(2.0) - 1.0
DEL = A1 - A2


def f(x1, x2, y):
    D = (x1 - A1) - (x2 - A2)
    return np.abs(D) + D * y


def lp_bound(l1, u1, l2, u2, ly=0.0, uy=1.0):
    # vars: x1, x2, y, w1(=x1 y), w2(=x2 y), s(>=|x1-x2-DEL|); objective s + w1 - w2 - DEL*y
    c = np.array([0, 0, -DEL, 1, -1, 1.0])
    Aub, bub = [], []

    def row(coefs, rhs):
        r = np.zeros(6)
        for k, v in coefs.items():
            r[k] += v
        Aub.append(r); bub.append(rhs)

    row({0: 1, 1: -1, 5: -1}, DEL)          # x1 - x2 - DEL <= s
    row({0: -1, 1: 1, 5: -1}, -DEL)         # -(x1 - x2 - DEL) <= s
    for (iw, ix, lx, ux) in ((3, 0, l1, u1), (4, 1, l2, u2)):
        row({iw: -1, ix: ly, 2: lx}, lx * ly)
        row({iw: -1, ix: uy, 2: ux}, ux * uy)
        row({iw: 1, ix: -uy, 2: -lx}, -lx * uy)
        row({iw: 1, ix: -ly, 2: -ux}, -ux * ly)
    bounds = [(l1, u1), (l2, u2), (ly, uy), (None, None), (None, None), (0, None)]
    r = linprog(c, A_ub=np.array(Aub), b_ub=np.array(bub), bounds=bounds, method="highs")
    assert r.status == 0
    return r.fun


def quadtree(eps):
    leaves, worst = 0, float("inf")
    stack = [(0.0, 1.0, 0.0, 1.0)]
    while stack:
        l1, u1, l2, u2 = stack.pop()
        h = u1 - l1
        # D = x1 - x2 - DEL ranges over [l1 - u2 - DEL, u1 - l2 - DEL]
        dlo, dhi = l1 - u2 - DEL, u1 - l2 - DEL
        mind = 0.0 if dlo <= 0 <= dhi else min(abs(dlo), abs(dhi))
        if h <= 2 * eps or mind >= 2 * h:
            leaves += 1
            worst = min(worst, lp_bound(l1, u1, l2, u2) + eps)
            continue
        m1, m2 = 0.5 * (l1 + u1), 0.5 * (l2 + u2)
        stack += [(l1, m1, l2, m2), (m1, u1, l2, m2), (l1, m1, m2, u2), (m1, u1, m2, u2)]
    return leaves, worst


if __name__ == "__main__":
    g = np.linspace(0, 1, 101)
    X1, X2, Y = np.meshgrid(g, g, g, indexing="ij")
    F = f(X1, X2, Y)
    D = (X1 - A1) - (X2 - A2)
    extra = (np.abs(Y - 1) < 1e-12) & (D < -1e-3)
    print(f"[1] min f on 101^3 grid = {F.min():.2e}; max f on {{y=1, D<-1e-3}} = {F[extra].max():.2e} "
          f"(so the optimal set also contains the region y = 1, X1 <= X2)")
    b = [lp_bound(0, A1, 0, A2), lp_bound(A1, 1, 0, A2), lp_bound(0, A1, A2, 1), lp_bound(A1, 1, A2, 1)]
    print("[2] orthant boxes (x1<=a1,x2<=a2), (x1>=a1,x2<=a2), (x1<=a1,x2>=a2), (x1>=a1,x2>=a2): "
          + ", ".join(f"{v:.4f}" for v in b))
    for eps in (1e-1, 3e-2, 1e-2, 3e-3, 1e-3):
        n, worst = quadtree(eps)
        print(f"[3] eps={eps:.0e}: quadtree leaves {n:6d}, leaves*eps = {n * eps:.2f}, "
              f"min over leaves of (LB + eps) = {worst:.2e} (>= 0 means valid); "
              f"Prop 4.7 lower bound 0.102/eps = {0.102 / eps:.0f}")
