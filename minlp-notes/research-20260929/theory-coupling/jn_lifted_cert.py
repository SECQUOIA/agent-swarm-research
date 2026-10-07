"""Exact lifted (partial-sum) certificate for J_n (Theorem 5.1(c)).

J_n: min sum_i c y_i(1-y_i) s.t. sum_i y_i = n/2, y in [0,1]^n, n odd.
Path of bags t = 1..n; bag t holds (zeta_{t-1}, y_t), zeta_t = zeta_{t-1} + y_t;
the root (bag n) imposes zeta_n = n/2. Partial-sum cells of side h, y-leaves of
side h, bag leaves = (child cell) x (y-leaf). Leaf relaxation of c y(1-y) = its
chord (convex envelope) on the y-leaf. Cell minorants: slope = chord slope of
c*phi on the cell, intercept = largest value allowed by (LC), computed exactly
(rational arithmetic) as the minimum over the vertices of the polygon
{zeta_{t-1} in child cell, y in y-leaf, zeta_t in cell}.

Prints the root bound l_r (exact), OPT = c/4, and the size (cells + leaves),
and checks the closed form 3n^2 - 3n + 2 for h = 1/2.

Usage: python3 jn_lifted_cert.py
"""
from fractions import Fraction as Fr
from math import comb, floor

C = Fr(1)


def f(y):
    return C * y * (1 - y)


def phi(s):
    fr = s - floor(s)
    return C * fr * (1 - fr)


def verts(a0, a1, b0, b1, d0, d1):
    """Vertices of {(z,y): a0<=z<=a1, b0<=y<=b1, d0<=z+y<=d1} (candidates)."""
    out = []
    for z in (a0, a1):
        for y in (b0, b1):
            if d0 <= z + y <= d1:
                out.append((z, y))
        for d in (d0, d1):
            y = d - z
            if b0 <= y <= b1:
                out.append((z, y))
    for y in (b0, b1):
        for d in (d0, d1):
            z = d - y
            if a0 <= z <= a1:
                out.append((z, y))
    return out


def cert(n, h):
    N = int(1 / h)
    ys = [(i * h, (i + 1) * h) for i in range(N)]
    chord = {Y: ((f(Y[1]) - f(Y[0])) / h, f(Y[0])) for Y in ys}  # slope, value at left end
    # stage 1: zeta_1 = y_1
    cells = []
    for j in range(N):
        lo, hi = j * h, (j + 1) * h
        lam = (phi(hi) - phi(lo)) / h
        sl, v0 = chord[(lo, hi)]
        beta = min(v0 + sl * (y - lo) - lam * y for y in (lo, hi))
        cells.append((lo, hi, lam, beta))
    size = 2 * N
    for t in range(2, n + 1):
        leaves = [(D, Y) for D in cells for Y in ys]
        size += len(leaves)
        if t == n:
            T = Fr(n, 2)
            best = None
            for (a0, a1, lp, bp), (b0, b1) in leaves:
                sl, v0 = chord[(b0, b1)]
                for z, y in verts(a0, a1, b0, b1, T, T):
                    v = v0 + sl * (y - b0) + lp * z + bp
                    best = v if best is None or v < best else best
            return best, size
        new = []
        for j in range(t * N):
            lo, hi = j * h, (j + 1) * h
            lam = (phi(hi) - phi(lo)) / h
            beta = None
            for (a0, a1, lp, bp), (b0, b1) in leaves:
                if a0 + b0 > hi or a1 + b1 < lo:
                    continue
                sl, v0 = chord[(b0, b1)]
                for z, y in verts(a0, a1, b0, b1, lo, hi):
                    v = v0 + sl * (y - b0) + lp * z + bp - lam * (z + y)
                    beta = v if beta is None or v < beta else beta
            new.append((lo, hi, lam, beta))
        size += len(new)
        cells = new


if __name__ == "__main__":
    print("n  h  l_r (exact)  OPT  size  3n^2-3n+2  C(n+1,(n+1)/2)")
    for n in [5, 9, 13, 25, 41]:
        for h in (Fr(1), Fr(1, 2)):
            lr, size = cert(n, h)
            print(n, h, lr, C / 4, size, 3 * n * n - 3 * n + 2, comb(n + 1, (n + 1) // 2), flush=True)
