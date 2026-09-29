"""Reviewer counterexample: an aligned optimal stratum with quadratic growth in a BOX-constrained problem.

f(x,y,z) = (x-a)^2 + (x-a)(y-z) + (y-z)^2 on [0,1]^3, a = 1/3.
Split: g = (x-a)^2 + (y-z)^2 - a y + a z (convex), phi = x y - x z (termwise McCormick, c = +1, -1).
f = (X + D/2)^2 + 3 D^2 / 4 >= 0 (X = x-a, D = y-z), so argmin f = {x = a, y = z}: a segment with
tangent (0,1,1) in span(e_y, e_z); {y,z} is independent in G = {xy, xz}.  The segment is aligned
(tau = 0 for p = 1), and it lies along ker C (C (0,1,1) = 0).

Lower bound (the argument of the note's Example 3.12, applied inside the plane y = z, which is
feasible here without any constraint): on R' = {(x,y,y): |x-a| <= h}, m = (x-a)^2 <= h^2, and each
leaf C gives Gamma_C >= |c| w'_x w'_y / 2 at the centre of C ∩ R'.  Hence
N_cov >= |c| h / (h^2 + eps) = 1/(2 sqrt(eps)) at h = sqrt(eps).
So N_opt = Omega(eps^(-1/2)), contradicting "aligned strata in box-constrained problems automatically
have linear transverse growth" and Conjecture 7.1 (which predicts O(log(1/eps)) because p* = 0).

This script (i) checks f >= 0 and the optimal set on a grid, (ii) checks the key inequality
Gamma_C(centre) >= |c| w'_x w'_y/2 on random boxes, and (iii) runs a small B&B with node QPs
solved by Clarabel (own model code) for bisection and R(1,.2)-widest, comparing with the bound.
"""
import math
import random
import numpy as np
import scipy.sparse as sp
import clarabel

A = 1.0 / 3.0


def f(x, y, z):
    X, D = x - A, y - z
    return X * X + X * D + D * D


def mcc_gap(c, xi, xj, li, ui, lj, uj):
    if c > 0:
        return c * min((xi - li) * (xj - lj), (ui - xi) * (uj - xj))
    return -c * min((xi - li) * (uj - xj), (ui - xi) * (xj - lj))


def gap(box, p):
    lx, ux, ly, uy, lz, uz = box
    x, y, z = p
    return mcc_gap(1.0, x, y, lx, ux, ly, uy) + mcc_gap(-1.0, x, z, lx, ux, lz, uz)


def node_qp(box):
    lx, ux, ly, uy, lz, uz = box
    # v = (x, y, z, w1, w2); objective 1/2 v'Pv + q'v + a^2
    P = sp.csc_matrix(np.array([[2, 0, 0, 0, 0], [0, 2, -2, 0, 0], [0, -2, 2, 0, 0],
                                [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], float))
    P = sp.triu(P).tocsc()
    q = np.array([-2 * A, -A, A, 1.0, -1.0])
    rows, rhs = [], []

    def mc(iw, ix, iy, l1, u1, l2, u2):
        # w >= l2 x + l1 y - l1 l2 ; w >= u2 x + u1 y - u1 u2 ; w <= u2 x + l1 y - l1 u2 ; w <= l2 x + u1 y - u1 l2
        for (sw, cx, cy, b) in ((-1, l2, l1, l1 * l2), (-1, u2, u1, u1 * u2),
                                (1, -u2, -l1, -l1 * u2), (1, -l2, -u1, -u1 * l2)):
            r = np.zeros(5); r[iw] = sw; r[ix] = cx; r[iy] = cy
            rows.append(r); rhs.append(b)

    mc(3, 0, 1, lx, ux, ly, uy)
    mc(4, 0, 2, lx, ux, lz, uz)
    for k, (lo, hi) in enumerate(((lx, ux), (ly, uy), (lz, uz))):
        r = np.zeros(5); r[k] = 1; rows.append(r); rhs.append(hi)
        r = np.zeros(5); r[k] = -1; rows.append(r); rhs.append(-lo)
    Am = sp.csc_matrix(np.array(rows))
    s = clarabel.DefaultSettings()
    s.verbose = False
    s.tol_gap_abs = s.tol_gap_rel = s.tol_feas = 1e-10
    sol = clarabel.DefaultSolver(P, q, Am, np.array(rhs), [clarabel.NonnegativeConeT(len(rhs))], s).solve()
    v = np.array(sol.x)
    return sol.obj_val + A * A, v[:3]


def bb(eps, rule, cap=60000):
    stack = [(0.0, 1.0, 0.0, 1.0, 0.0, 1.0)]
    n = 0
    while stack:
        box = stack.pop()
        n += 1
        if n > cap:
            return None
        lb, xh = node_qp(box)
        if lb >= -eps:
            continue
        w = [box[1] - box[0], box[3] - box[2], box[5] - box[4]]
        i = int(np.argmax(w))
        l, u = box[2 * i], box[2 * i + 1]
        if rule == "bisect":
            p = 0.5 * (l + u)
        else:
            p = min(max(xh[i], l + 0.2 * (u - l)), u - 0.2 * (u - l))
        b1 = list(box); b1[2 * i + 1] = p
        b2 = list(box); b2[2 * i] = p
        stack += [tuple(b1), tuple(b2)]
    return n


if __name__ == "__main__":
    g = np.linspace(0, 1, 61)
    X, Y, Z = np.meshgrid(g, g, g, indexing="ij")
    F = f(X, Y, Z)
    print(f"[i] grid 61^3: min f = {F.min():.3e}; points with f < 1e-12 all have x = a? "
          f"{np.all(np.abs(X[F < 1e-12] - A) < 1e-9)} and y = z? {np.all(np.abs(Y[F < 1e-12] - Z[F < 1e-12]) < 1e-9)}")
    rng = random.Random(3)
    worst = float("inf")
    for _ in range(20000):
        box = []
        for _k in range(3):
            l_, u_ = sorted((rng.random(), rng.random()))
            box += [l_, u_]
        lx, ux, ly, uy, lz, uz = box
        lo, hi = max(ly, lz), min(uy, uz)
        if hi <= lo:
            continue
        xc, yc = 0.5 * (lx + ux), 0.5 * (lo + hi)
        ratio = gap(box, (xc, yc, yc)) / ((ux - lx) * (hi - lo) / 2)
        worst = min(worst, ratio)
    print(f"[ii] min over 20000 random boxes of Gamma_C(centre of C ∩ {{y=z}}) / (w'_x w'_y / 2) = {worst:.4f} (>= 1)")
    print("[iii] B&B node counts (Clarabel node QPs), proved lower bound 1/(2 sqrt(eps)) leaves -> 2LB-1 nodes")
    for eps in (1e-2, 1e-3, 1e-4):
        lbnd = 1 / (2 * math.sqrt(eps))
        nb = bb(eps, "bisect")
        nr = bb(eps, "R1")
        print(f"    eps={eps:.0e}: bound {lbnd:7.1f} leaves (>= {2 * math.ceil(lbnd) - 1} nodes); "
              f"bisect {nb}; R(1,.2)w {nr}")
