"""A lifted (partial-sum) box certificate for the Jeroslow-type instance J_n
of Theorem 5.1, in the certificate model of Section 4.2 of the coupling note
(cells with affine minorants on the partial-sum separators, leaves = boxes
with convex relaxations, (CM)/(LC) semantics), to compare with the B&B leaf
count C(n+1, (n+1)/2) in a common model.

Path of bags t = 1..n, root = bag n. Bag t holds (zeta_{t-1}, y_t); its own
partial sum is zeta_t = zeta_{t-1} + y_t. The row closes at the root:
zeta_n = n/2 (a linear constraint in the root's convex programs).
Grid of side h = 1/N for cells (zeta) and leaves (zeta_{t-1} x y_t); leaves
are aligned with child cells. Relaxation of c y(1-y) on a leaf: its chord
(the convex envelope). Minorant on cell D: slope = chord slope of the true
value function c*phi on D, intercept = largest value allowed by (LC)
(minimum of an affine function over a polygon, at a vertex).

Output: l_r versus OPT = c/4, and certificate size (cells + leaves).

Usage: python3 c8_lifted_jn.py
"""
from math import comb, floor

c = 1.0


def fy(y):
    return c * y * (1 - y)


def phi(s):
    fr = s - floor(s)
    return c * fr * (1 - fr)


def polygon_vertices(a0, a1, b0, b1, d0, d1):
    """Vertices of {(z, y): a0<=z<=a1, b0<=y<=b1, d0<=z+y<=d1}."""
    pts = []
    for z in (a0, a1):
        for y in (b0, b1):
            if d0 - 1e-12 <= z + y <= d1 + 1e-12:
                pts.append((z, y))
    for d in (d0, d1):
        for z in (a0, a1):
            y = d - z
            if b0 - 1e-12 <= y <= b1 + 1e-12:
                pts.append((z, y))
        for y in (b0, b1):
            z = d - y
            if a0 - 1e-12 <= z <= a1 + 1e-12:
                pts.append((z, y))
    return pts


def certificate(n, N):
    h = 1.0 / N
    T = n / 2
    # stage 1: cells on zeta_1 = y_1 in [0,1]; leaves = y intervals
    prev = []  # list of (lo, hi, slope, intercept) for cells of zeta_{t-1}
    size = 0
    for j in range(N):
        lo, hi = j * h, (j + 1) * h
        lam = (phi(hi) - phi(lo)) / h
        # leaf = same interval; Rel(y) = chord of fy on [lo,hi]; zeta_1 = y
        sl = (fy(hi) - fy(lo)) / h
        beta = min(fy(lo) + sl * (y - lo) - lam * y for y in (lo, hi))
        prev.append((lo, hi, lam, beta))
    size += 2 * N  # N leaves + N cells
    for t in range(2, n + 1):
        ycells = [(i * h, (i + 1) * h) for i in range(N)]
        leaves = [(D, Y) for D in prev for Y in ycells]
        size += len(leaves)
        if t == n:
            best = float("inf")
            for (a0, a1, lp, bp), (b0, b1) in leaves:
                sl = (fy(b1) - fy(b0)) / h
                for z, y in polygon_vertices(a0, a1, b0, b1, T, T):
                    best = min(best, fy(b0) + sl * (y - b0) + lp * z + bp)
            return best, size
        cells = []
        for j in range(t * N):
            lo, hi = j * h, (j + 1) * h
            lam = (phi(hi) - phi(lo)) / h
            beta = float("inf")
            for (a0, a1, lp, bp), (b0, b1) in leaves:
                if a0 + b0 > hi + 1e-12 or a1 + b1 < lo - 1e-12:
                    continue
                sl = (fy(b1) - fy(b0)) / h
                for z, y in polygon_vertices(a0, a1, b0, b1, lo, hi):
                    beta = min(beta, fy(b0) + sl * (y - b0) + lp * z + bp - lam * (z + y))
            cells.append((lo, hi, lam, beta))
        size += len(cells)
        prev = cells


if __name__ == "__main__":
    print("n  C(n+1,(n+1)/2)  | smallest N=2^j with l_r >= c/4 - eps (eps=c/8), size, l_r | same for eps=c/40")
    for n in [5, 9, 13, 17, 21, 25]:
        out = []
        for eps in (c / 8, c / 40):
            N = 1
            while True:
                lr, size = certificate(n, N)
                if lr >= c / 4 - eps - 1e-12 or N > 64:
                    break
                N *= 2
            out.append(f"N={N} size={size} l_r={lr:.4f}")
        print(f"{n:2d}  {comb(n + 1, (n + 1) // 2):8d}  | {out[0]} | {out[1]}", flush=True)
