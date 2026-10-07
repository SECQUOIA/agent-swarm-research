"""Validity of the c8 lifted certificate: every cell minorant l_D is below the
true partial-sum value function U_t = c*phi on D (checked at cell endpoints;
l_D - U_t is convex on D because U_t is concave on each [j, j+1] and the
cells of side 1/2 do not straddle integers), and the jump of adjacent
minorants at shared endpoints (strict (CM) of [D, Definition 1.2] needs
l_{D''}(e) <= l_{D'}(e) at a shared endpoint e).

Usage: python3 c8b_validity.py
"""
import c8_lifted_jn as C

def cells_all(n, N):
    h = 1.0 / N
    out = {}
    prev = []
    for j in range(N):
        lo, hi = j * h, (j + 1) * h
        lam = (C.phi(hi) - C.phi(lo)) / h
        sl = (C.fy(hi) - C.fy(lo)) / h
        beta = min(C.fy(lo) + sl * (y - lo) - lam * y for y in (lo, hi))
        prev.append((lo, hi, lam, beta))
    out[1] = prev
    for t in range(2, n):
        ycells = [(i * h, (i + 1) * h) for i in range(N)]
        leaves = [(D, Y) for D in prev for Y in ycells]
        cells = []
        for j in range(t * N):
            lo, hi = j * h, (j + 1) * h
            lam = (C.phi(hi) - C.phi(lo)) / h
            beta = float("inf")
            for (a0, a1, lp, bp), (b0, b1) in leaves:
                if a0 + b0 > hi + 1e-12 or a1 + b1 < lo - 1e-12:
                    continue
                sl = (C.fy(b1) - C.fy(b0)) / h
                for z, y in C.polygon_vertices(a0, a1, b0, b1, lo, hi):
                    beta = min(beta, C.fy(b0) + sl * (y - b0) + lp * z + bp - lam * (z + y))
            cells.append((lo, hi, lam, beta))
        out[t] = cells
        prev = cells
    return out

for n in [9, 25]:
    allc = cells_all(n, 2)
    viol = max(lam * s + beta - C.phi(s) for cells in allc.values() for (lo, hi, lam, beta) in cells for s in (lo, hi))
    jump = max(abs((c1[2] * c1[1] + c1[3]) - (c2[2] * c2[0] + c2[3])) for cells in allc.values() for c1, c2 in zip(cells, cells[1:]))
    exact = max(abs(lam * s + beta - C.phi(s)) for cells in allc.values() for (lo, hi, lam, beta) in cells for s in (lo, hi))
    print(f"n={n} N=2: max (l_D - U_t) at endpoints = {viol:.2e} (<= 0 means valid); max jump at shared endpoints = {jump:.2e}; max |l_D - U_t| at endpoints = {exact:.2e}")
