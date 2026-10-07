"""Independent exact check of Theorem 5.1(d) of theory-coupling/coupling.md.

J_n: min sum_i c y_i (1 - y_i)  s.t.  sum_i y_i = n/2,  y in [0,1]^n,  n odd.
Lifted path: bag t holds (zeta_{t-1}, y_t) (bag 1 holds y_1 only), zeta_t =
zeta_{t-1} + y_t, root = bag n imposing zeta_n = n/2. Separator of bag t < n:
Sigma_t = [0, t].

Certificate as stated in the note (side h = 1/2):
  cells of side 1/2 on [0, t]; y-pieces [0,1/2], [1/2,1]; bag leaves =
  (child cell) x (y-piece); leaf relaxation of c y(1-y) = chord on the piece;
  cell minorant = (c/2) dist(zeta, Z) restricted to the cell (must be affine
  there); child bound psi_{u,B} = the minorant of the child cell that equals
  the leaf's projection.

Checks, all in exact rational arithmetic, against [D, Definition 1.2]:
  (A) every cell minorant is affine on its cell and equals (c/2)dist there;
  (CM) psi_{u,B}(s) <= l_{u,D'}(s) for every child cell D' and every s in
       B_{S_u} cap D' (affine inequality on an interval: check endpoints);
  (LC) Rel_{t,B}(z) >= l_{t,D}(zeta_t(z)) on {z in B : zeta_t(z) in D} for
       every pair (B, D) that meets (affine on a polygon: check vertices);
  root: min over root leaves of Rel on {zeta_n = n/2} equals c/4;
  size = sum_t |L_t| + sum_{t<n} |P_t| versus 3n^2 - 3n + 2;
  validity: every minorant <= c*phi(s) = U_t(s) on its cell (spot grid).
Side 1: an LP over all affine cell minorants for the aligned construction
(slopes and intercepts free, child bound = child minorant, (CM) and (LC) as
linear constraints) maximizes l_r; the note says the result is 0.
Also checks the lattice-path identity 2 sum_{j<=m} C(m+j, j) = C(n+1,(n+1)/2)
and the comparison 3n^2 - 3n + 2 versus C(n+1,(n+1)/2).

Usage: python3 r3_jn_certificate.py
"""
from fractions import Fraction as Fr
from math import comb, floor
import itertools

import numpy as np
from scipy.optimize import linprog

c = Fr(1)
HALF = Fr(1, 2)


def dist(u):
    fl = floor(u)
    return min(u - fl, fl + 1 - u)


def f(y):
    return c * y * (1 - y)


def cphi(s):
    fr = s - floor(s)
    return c * fr * (1 - fr)


def chord(lo, hi):
    """Chord of c y(1-y) on [lo, hi] as (slope, intercept)."""
    sl = (f(hi) - f(lo)) / (hi - lo)
    return sl, f(lo) - sl * lo


def poly_vertices(a0, a1, b0, b1, d0, d1):
    """Vertices of {(z, y): a0<=z<=a1, b0<=y<=b1, d0<=z+y<=d1}."""
    pts = set()
    for z in (a0, a1):
        for y in (b0, b1):
            pts.add((z, y))
        for d in (d0, d1):
            pts.add((z, d - z))
    for y in (b0, b1):
        for d in (d0, d1):
            pts.add((d - y, y))
    return [(z, y) for (z, y) in pts
            if a0 <= z <= a1 and b0 <= y <= b1 and d0 <= z + y <= d1]


def affine_dist_on(lo, hi):
    """(slope, intercept) of (c/2) dist on [lo, hi]; None if not affine there."""
    sl = (c / 2) * (dist(hi) - dist(lo)) / (hi - lo)
    b = (c / 2) * dist(lo) - sl * lo
    for k in range(1, 8):
        s = lo + (hi - lo) * Fr(k, 8)
        if (c / 2) * dist(s) != sl * s + b:
            return None
    return sl, b


def check_half(n):
    h = HALF
    ypieces = [(Fr(0), HALF), (HALF, Fr(1))]
    ok = {"A": True, "CM": True, "LC": True, "valid": True}
    # cells[t] = list of (lo, hi, slope, intercept) for separator of bag t (t < n)
    cells = {}
    for t in range(1, n):
        lst = []
        for j in range(2 * t):
            lo, hi = j * h, (j + 1) * h
            aff = affine_dist_on(lo, hi)
            if aff is None:
                ok["A"] = False
                aff = (Fr(0), Fr(0))
            lst.append((lo, hi) + aff)
            for k in range(0, 9):
                s = lo + (hi - lo) * Fr(k, 8)
                if aff[0] * s + aff[1] > cphi(s):
                    ok["valid"] = False
        cells[t] = lst
    # leaves
    leaves = {1: [(None, Y) for Y in ypieces]}
    for t in range(2, n + 1):
        leaves[t] = [(D, Y) for D in cells[t - 1] for Y in ypieces]
    # (CM): child bound = minorant of the aligned child cell D; compare with
    # every child cell D' at the points of B_S cap D'
    for t in range(2, n + 1):
        for (D, Y) in leaves[t]:
            lo, hi, sl, b = D
            for D2 in cells[t - 1]:
                lo2, hi2, sl2, b2 = D2
                a, e = max(lo, lo2), min(hi, hi2)
                if a > e:
                    continue
                for s in {a, e}:
                    if sl * s + b > sl2 * s + b2:
                        ok["CM"] = False
    # (LC) for t < n
    npairs = 0
    for t in range(1, n):
        for (D, Y) in leaves[t]:
            ysl, yb = chord(*Y)
            for (lo, hi, sl, b) in cells[t]:
                if t == 1:
                    a0 = a1 = Fr(0)
                    psl = pb = Fr(0)
                else:
                    a0, a1, psl, pb = D
                pts = poly_vertices(a0, a1, Y[0], Y[1], lo, hi)
                if not pts:
                    continue
                npairs += 1
                for z, y in pts:
                    rel = ysl * y + yb + psl * z + pb
                    if rel < sl * (z + y) + b:
                        ok["LC"] = False
    # root
    T = Fr(n, 2)
    lr = None
    for (D, Y) in leaves[n]:
        ysl, yb = chord(*Y)
        if n == 1:
            a0 = a1 = Fr(0)
            psl = pb = Fr(0)
        else:
            a0, a1, psl, pb = D
        for z, y in poly_vertices(a0, a1, Y[0], Y[1], T, T):
            v = ysl * y + yb + psl * z + pb
            lr = v if lr is None or v < lr else lr
    size = sum(len(leaves[t]) for t in range(1, n + 1)) + sum(len(cells[t]) for t in range(1, n))
    return ok, lr, size, npairs


def lp_side(n, h):
    """Max l_r over affine minorants for the aligned construction with cells
    of side h and y-pieces of side h (floating point LP)."""
    N = int(1 / h)
    ypieces = [(i * h, (i + 1) * h) for i in range(N)]
    idx = {}
    for t in range(1, n):
        for j in range(N * t):
            idx[(t, j)] = len(idx)
    nv = 2 * len(idx) + 1  # (slope, intercept) per cell, then l_r
    A, bnd = [], []

    def cellrange(j):
        return j * h, (j + 1) * h

    def row():
        return np.zeros(nv)
    # (LC): psi(z) + chord(y) - (sl*(z+y) + b) >= 0 at polygon vertices
    for t in range(1, n + 1):
        childs = [None] if t == 1 else list(range(N * (t - 1)))
        for jc in childs:
            for Y in ypieces:
                ysl, yb = chord(*Y)
                a0, a1 = (Fr(0), Fr(0)) if jc is None else cellrange(jc)
                targets = [None] if t == n else list(range(N * t))
                for jt in targets:
                    lo, hi = (Fr(n, 2), Fr(n, 2)) if jt is None else cellrange(jt)
                    for z, y in poly_vertices(a0, a1, Y[0], Y[1], lo, hi):
                        r = row()
                        # constraint: target(z+y) - psi(z) <= chord(y)
                        if jt is None:
                            r[-1] = 1
                        else:
                            k = idx[(t, jt)]
                            r[2 * k] = float(z + y)
                            r[2 * k + 1] = 1
                        if jc is not None:
                            k = idx[(t - 1, jc)]
                            r[2 * k] -= float(z)
                            r[2 * k + 1] -= 1
                        A.append(r)
                        bnd.append(float(ysl * y + yb))
    # (CM): aligned child minorant <= neighbouring child minorants at shared points
    for t in range(1, n):
        for j in range(N * t):
            lo, hi = cellrange(j)
            for j2 in (j - 1, j + 1):
                if (t, j2) not in idx:
                    continue
                s = hi if j2 == j + 1 else lo
                r = row()
                k, k2 = idx[(t, j)], idx[(t, j2)]
                r[2 * k] += float(s)
                r[2 * k + 1] += 1
                r[2 * k2] -= float(s)
                r[2 * k2 + 1] -= 1
                A.append(r)
                bnd.append(0.0)
    obj = np.zeros(nv)
    obj[-1] = -1
    res = linprog(obj, A_ub=np.array(A), b_ub=np.array(bnd),
                  bounds=[(-50, 50)] * nv, method="highs")
    return -res.fun if res.status == 0 else None


def author_style_betas_match(n):
    """jn_lifted_cert.py uses slope = chord slope of c*phi on the cell and the
    largest intercept allowed by (LC); it does not check (CM). Recompute those
    intercepts (side 1/2) and test whether they equal the (c/2)dist ones, in
    which case the minorants are continuous and (CM) holds for that script's
    certificate too."""
    h = HALF
    ypieces = [(Fr(0), HALF), (HALF, Fr(1))]
    prev = None
    for t in range(1, n):
        cur = []
        for j in range(2 * t):
            lo, hi = j * h, (j + 1) * h
            lam = (cphi(hi) - cphi(lo)) / h
            beta = None
            src = [(None, Y) for Y in ypieces] if t == 1 else [(D, Y) for D in prev for Y in ypieces]
            for D, Y in src:
                ysl, yb = chord(*Y)
                a0, a1, psl, pb = (Fr(0), Fr(0), Fr(0), Fr(0)) if D is None else D
                for z, y in poly_vertices(a0, a1, Y[0], Y[1], lo, hi):
                    v = ysl * y + yb + psl * z + pb - lam * (z + y)
                    beta = v if beta is None or v < beta else beta
            if (lam, beta) != affine_dist_on(lo, hi):
                return False
            cur.append((lo, hi, lam, beta))
        prev = cur
    return True


def main():
    print("author-style maximal intercepts equal (c/2)dist for n = 3..15:",
          all(author_style_betas_match(n) for n in range(3, 16, 2)))
    print("Theorem 5.1(d), side 1/2, (c/2)dist construction, exact arithmetic (c = 1)")
    print(" n | affine | (CM) | (LC) | minorant<=c*phi | l_r | size | 3n^2-3n+2 | C(n+1,(n+1)/2) | (leaf,cell) pairs")
    for n in range(1, 30, 2):
        ok, lr, size, npairs = check_half(n)
        print(f"{n:2d} | {ok['A']} | {ok['CM']} | {ok['LC']} | {ok['valid']} | {lr} | {size} | "
              f"{3 * n * n - 3 * n + 2} | {comb(n + 1, (n + 1) // 2)} | {npairs}")
    print("\nnote's itemized count 2 + 2 + sum_{t=2}^{n-1}(4(t-1)+2t) + 4(n-1) (valid for n >= 2):")
    for n in (1, 3, 5, 9):
        item = 2 + 2 + sum(4 * (t - 1) + 2 * t for t in range(2, n)) + 4 * (n - 1)
        print(f"  n={n}: itemized {item}, closed form {3 * n * n - 3 * n + 2}")
    print("\nfirst odd n with 3n^2-3n+2 < C(n+1,(n+1)/2):",
          next(n for n in itertools.count(1, 2) if 3 * n * n - 3 * n + 2 < comb(n + 1, (n + 1) // 2)))
    print("comparison for n = 1, 3, 5, 7, 9:",
          [(n, 3 * n * n - 3 * n + 2, comb(n + 1, (n + 1) // 2)) for n in (1, 3, 5, 7, 9)])
    print("\nlattice-path identity 2 sum_{j<=m} C(m+j, j) = C(n+1,(n+1)/2), n = 2m+1:",
          all(2 * sum(comb(m + j, j) for j in range(m + 1)) == comb(2 * m + 2, m + 1) for m in range(0, 40)),
          "(m = 0..39)")
    print("\nLP: max l_r over all affine minorants, aligned leaves (floating point)")
    for n in (3, 5, 7, 9):
        print(f"  n={n}: side 1 -> {lp_side(n, Fr(1)):.6f}; side 1/2 -> {lp_side(n, HALF):.6f}")


if __name__ == "__main__":
    main()
