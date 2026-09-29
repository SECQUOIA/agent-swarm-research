"""Finer-grid recheck of the 'sharp x quadratic' ratios (note, Section 5 remark and Summary 3).

Instance as in the author's exp1/exp7: x: m = 2|t - 1/3| - (t - 1/3)^2 (sharp), z: knot
interpolant of (t - 29/70)^2 (knots 29/70 +- r, r shrinking by 5/4, down to 1e-8).
Grid optimum = least guillotine certificate with cuts on a candidate grid (own C DP, float with a
conservative guard), reconstructed and verified box by box in exact arithmetic.  It is an upper
bound on N_guill, so omega/grid is a LOWER bound on omega/N_guill: a smaller grid optimum is a
better bound.  Grids used here are built for strip structure: x = 1/3 +- d (d geometric,
ratio 4, from eps/4 up), z = greedy 1D breakpoints of z at the strip budgets eps + m_x(1/3 + d)
(both greedy directions), plus omega's cuts.
usage: python3 sharpquad_grid.py
"""
import ctypes
import os
import subprocess
import numpy as np
from fractions import Fraction as Fr
from sepcore import PL, run, sharp, opt_min2
from selection_check import quad_knots

HERE = os.path.dirname(os.path.abspath(__file__))
A, B = Fr(1, 3), Fr(29, 70)


def lib():
    so = os.path.join(HERE, "libgdp8.so")
    if not os.path.exists(so):
        subprocess.check_call(["gcc", "-O2", "-shared", "-fPIC", "-o", so, os.path.join(HERE, "gdp8.c")])
    L = ctypes.CDLL(so)
    L.gdp8.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double, ctypes.c_void_p]
    L.gdp8.restype = ctypes.c_int
    return L


def greedy_pts(c, b):
    """breakpoints of the left-greedy and right-greedy partitions at budget b."""
    pts = {c.L, c.U}
    a = c.L
    while a < c.U:
        a = c.maxvalid(a, b)
        pts.add(a)
    # right greedy by reflection
    rc = PL([-x for x in reversed(c.x)], list(reversed(c.Hk)))
    a = rc.L
    while a < rc.U:
        a = rc.maxvalid(a, b)
        pts.add(-a)
    return pts


def thin(pts, G, keep=()):
    pts = sorted(set(pts))
    if len(pts) <= G:
        return pts
    keep = set(keep)
    idx = sorted({round(i * (len(pts) - 1) / (G - 1)) for i in range(G)})
    return sorted({pts[i] for i in idx} | (keep & set(pts)))


def grid_opt(cx, cz, gx, gz, eps, L):
    G1, G2 = len(gx), len(gz)
    Ax = np.full((G1, G1), -1e300)
    Bz = np.full((G2, G2), -1e300)
    Fx = {}
    Fz = {}
    for a in range(G1):
        for b in range(a + 1, G1):
            Fx[a, b] = cx.node(gx[a], gx[b])[0]
            Ax[a, b] = float(Fx[a, b])
    for c in range(G2):
        for d in range(c + 1, G2):
            Fz[c, d] = cz.node(gz[c], gz[d])[0]
            Bz[c, d] = float(Fz[c, d])
    T = np.zeros(G1 * G1 * G2 * G2, dtype=np.uint8)
    thr = -float(eps) + 1e-13 * float(eps)
    r = L.gdp8(G1, G2, Ax.ctypes.data, Bz.ctypes.data, thr, T.ctypes.data)
    if r >= 255:
        return None
    T = T.reshape(G1, G1, G2, G2)
    boxes, st = [], [(0, G1 - 1, 0, G2 - 1)]
    while st:
        a, b, c, d = st.pop()
        v = int(T[a, b, c, d])
        if Ax[a, b] + Bz[c, d] >= thr:
            boxes.append((a, b, c, d))
            continue
        for k in range(a + 1, b):
            if int(T[a, k, c, d]) + int(T[k, b, c, d]) == v:
                st += [(a, k, c, d), (k, b, c, d)]
                break
        else:
            for k in range(c + 1, d):
                if int(T[a, b, c, k]) + int(T[a, b, k, d]) == v:
                    st += [(a, b, c, k), (a, b, k, d)]
                    break
            else:
                raise AssertionError("reconstruction failed")
    assert len(boxes) == r
    for a, b, c, d in boxes:   # exact verification
        assert Fx[a, b] + Fz[c, d] + eps >= 0, "invalid box"
    area = sum((gx[b] - gx[a]) * (gz[d] - gz[c]) for a, b, c, d in boxes)
    assert area == (gx[-1] - gx[0]) * (gz[-1] - gz[0])
    return r


if __name__ == "__main__":
    L = lib()
    cx, cz = sharp(A, 2, sel="knots"), quad_knots(B, 1, rmin=Fr(1, 10 ** 8), sel="knots")
    note = {3: 8, 4: 11, 5: 13, 6: 15, 7: 18, 8: 20, 9: 24, 10: 27, 11: 30}
    note_om = {3: 10, 4: 14, 5: 18, 6: 24, 7: 28, 8: 32, 9: 36, 10: 38, 11: 44}
    for k in range(3, 12):
        eps = Fr(1, 10 ** k)
        ro = run([cx, cz], eps, "omega", record=True)
        cutx = {y[0] for bx, i, ph, y in ro["internal"] if i == 0}
        cutz = {y[1] for bx, i, ph, y in ro["internal"] if i == 1}
        ds = []
        d = eps / 4
        while d < 1:
            ds.append(d)
            d *= 4
        gx = sorted({Fr(0), Fr(1), A} | {A + d for d in ds if A + d < 1} | {A - d for d in ds if A - d > 0} | cutx)
        budgets = [eps] + [eps + cx.m(A + d) for d in ds if A + d < 1]
        gzs = set(cutz) | {Fr(0), Fr(1), B}
        for bud in budgets:
            gzs |= greedy_pts(cz, bud)
        gz = thin(gzs, 190, keep=cutz | {B})
        n = grid_opt(cx, cz, gx, gz, eps, L)
        print(f"eps=1e-{k}: grid {len(gx)}x{len(gz)}; grid optimum {n} (note {note[k]}); omega leaves "
              f"{ro['leaves']} (note {note_om[k]}); omega/grid {ro['leaves'] / n:.2f} "
              f"(note {note_om[k] / note[k]:.2f})", flush=True)
