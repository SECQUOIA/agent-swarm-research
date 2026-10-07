"""Existence proof for exactly feasible points of topopt-cantilever_60x40_50 near
listed points p4/p5 (own method, different from the audit's basis choice).

Model (asserted from the OSIL file):
  min sum_e c_e,  c_e >= 0
  sum_k w_{e,k}^2 - c_e * b_e <= 0        (one quadratic row per element e)
  A w = f                                 (4920 linear equality rows in w only)
  linear rows in the binaries b only.

Method. Keep b (exact 0/1). Void elements (b_e = 0): w_e := 0 exactly (their
cone row then reads 0 <= 0). Let A_s be the equality rows restricted to the
solid-element w's, w0 the listed solid w's, r = f - A_s w0 (exact rational).
Rows with no solid w must have f_i = 0 (checked exactly). We look for
w = w0 + A_s^T y with G y = r, G = A_s A_s^T (exact rational, sparse). A
Krawczyk test for the linear system G y = r (floating point with a-priori
error bounds, see kraw.py) proves that a box Y contains a solution y*. Then
w* = w0 + A_s^T y* satisfies A w* = f exactly, and w* lies in the interval
vector W = w0 + A_s^T Y. Set c_e := upper endpoint of the interval enclosure of
sum_k W_{e,k}^2 (a rational), so every cone row holds; c_e := 0 on void
elements. All binary-only rows are checked exactly. The objective sum c_e is
then an exact rational upper bound for the objective of the proven point
(w*, b, c).
"""
import os
import sys
import time
from collections import defaultdict
from fractions import Fraction as F

import numpy as np

import evalpt
import ivl
import kraw
import osil

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "topopt-cantilever_60x40_50"


def main(pk):
    t0 = time.time()
    M = evalpt.model(NAME)
    x0, missing, _ = osil.read_sol(os.path.join(HERE, "data", f"{NAME}.{pk}.sol"), M)
    assert M.sense == "min" and M.obj_const == 0 and not M.obj_quad and M.obj_nl is None
    cvars = sorted(M.obj_lin)
    assert all(M.obj_lin[j] == 1 and M.lb[j] == 0 and M.ub[j] is None for j in cvars)
    bins = [j for j in range(M.n) if M.vtype[j] == "B"]
    assert all(x0[j] in (0, 1) for j in bins)
    cset = set(cvars)
    wset = set(j for j in range(M.n) if M.vtype[j] == "C") - cset
    assert all(M.lb[j] is None and M.ub[j] is None for j in wset)
    # cone rows: sum w^2 - c*b <= 0
    elem = {}  # c var -> (b var, [w vars], row)
    for i in range(M.m):
        if not M.quad[i]:
            continue
        assert not M.lin[i] and M.nl[i] is None and M.clb[i] is None and M.cub[i] == 0 and M.cconst[i] == 0
        sq = [a for a, b, c in M.quad[i] if a == b]
        assert all(c == 1 for a, b, c in M.quad[i] if a == b)
        cb = [(a, b, c) for a, b, c in M.quad[i] if a != b]
        assert len(cb) == 1 and cb[0][2] == -1
        a, b, _ = cb[0]
        cj, bj = (a, b) if a in cset else (b, a)
        assert cj in cset and M.vtype[bj] == "B" and set(sq) <= wset
        elem[cj] = (bj, sq, i)
    assert len(elem) == len(cvars)
    eqrows = [i for i in range(M.m) if M.clb[i] is not None and M.clb[i] == M.cub[i]]
    assert all(set(M.lin[i]) <= wset and not M.quad[i] and M.nl[i] is None for i in eqrows)
    binrows = [i for i in range(M.m) if not M.quad[i] and i not in set(eqrows)]
    assert all(all(M.vtype[j] == "B" for j in M.lin[i]) for i in binrows)
    x = list(x0)
    solid_w = set()
    nvoid_nonzero = 0
    for cj, (bj, ws, i) in elem.items():
        if x[bj] == 0:
            for j in ws:
                if x[j] != 0:
                    nvoid_nonzero += 1
                x[j] = F(0)
        else:
            solid_w |= set(ws)
    print(f"{pk}: elements {len(elem)}, solid {sum(1 for c in elem.values() if x[c[0]] == 1)}, "
          f"void w listed nonzero: {nvoid_nonzero}")
    # binary rows exactly
    bad = []
    for i in binrows:
        v = osil.row_exact(M, i, x)
        if (M.clb[i] is not None and v < M.clb[i]) or (M.cub[i] is not None and v > M.cub[i]):
            bad.append(M.cname[i])
    print(f"binary-only rows: {len(binrows)}, violated exactly: {bad[:5]}")
    assert not bad
    # equality rows
    act = [i for i in eqrows if set(M.lin[i]) & solid_w]
    for i in eqrows:
        if i not in set(act):
            assert osil.row_exact(M, i, x) == M.cub[i], M.cname[i]
    cols = sorted(set().union(*[set(M.lin[i]) & solid_w for i in act]))
    print(f"equality rows with solid w: {len(act)} of {len(eqrows)}; solid w in them: {len(cols)}")
    r = [M.cub[i] - osil.row_exact(M, i, x) for i in act]
    print("max |residual| of listed point on these rows:", float(max(abs(v) for v in r)))
    # G = A_s A_s^T exactly
    rows_of = defaultdict(list)
    for k, i in enumerate(act):
        for j, c in M.lin[i].items():
            if j in solid_w:
                rows_of[j].append((k, c))
    G = defaultdict(F)
    for j, lst in rows_of.items():
        for (k1, c1) in lst:
            for (k2, c2) in lst:
                G[(k1, k2)] += c1 * c2
    n = len(act)
    Gm = np.zeros((n, n))
    Gr = np.zeros((n, n))
    for (k1, k2), v in G.items():
        f = float(v)
        Gm[k1, k2] = f
        Gr[k1, k2] = kraw.fup(abs(v - F(f)))
    print(f"G: n={n}, nnz={len(G)} ({time.time()-t0:.1f}s)")

    def Gy_minus_r(y):  # exact, y floats
        out = [-v for v in r]
        yF = [F(float(v)) for v in y]
        for (k1, k2), v in G.items():
            out[k1] += v * yF[k2]
        return out

    rf = np.array([float(v) for v in r])
    y = np.linalg.solve(Gm, rf)
    for it in range(3):
        res = Gy_minus_r(y)
        y = y - np.linalg.solve(Gm, np.array([float(v) for v in res]))
    res = Gy_minus_r(y)
    Fm = np.array([float(v) for v in res])
    Fr = np.array([kraw.fup(abs(v - F(float(v)))) for v in res])
    R = np.linalg.inv(Gm)
    aR = np.abs(R)
    P3, E3 = kraw.mm(R, Gm)
    Cabs = np.abs(np.eye(n) - P3) * (1 + 4 * kraw.U) + E3
    ok = False
    for kappa in (1e-8, 1e-6, 1e-4, 1e-2):
        rho = kappa * np.maximum(np.abs(y), np.max(np.abs(y)) * 1e-3)
        P1, E1 = kraw.mm(R, Fm[:, None])
        t1 = np.abs(P1[:, 0]) + E1[:, 0]
        t2 = kraw.mm_nonneg_up(aR, Fr[:, None])[:, 0]
        t3 = kraw.mm_nonneg_up(Cabs, rho[:, None])[:, 0]
        t4 = kraw.mm_nonneg_up(aR, kraw.mm_nonneg_up(Gr, rho[:, None]))[:, 0]
        T = (t1 + t2 + t3 + t4) * (1 + 1e-12)
        ok = bool(np.all(T < rho))
        print(f"  kappa={kappa:g}: Krawczyk ok={ok}, max ratio {np.max(T/rho):.3e} "
              f"(residual term {np.max(t1/rho):.2e}, contraction {np.max((t3+t4)/rho):.2e})")
        if ok:
            break
    assert ok
    Y = [ivl.I(F(float(y[k])) - F(float(rho[k])), F(float(y[k])) + F(float(rho[k]))) for k in range(n)]
    W = {}
    for j in solid_w:
        d = ivl.I(0)
        for (k, c) in rows_of.get(j, []):
            d = d + ivl.I(c) * Y[k]
        W[j] = ivl.I(x[j]) + d
    maxw = max(float(W[j].hi - W[j].lo) for j in W)
    shift = max(float(max(abs(W[j].lo - x0[j]), abs(W[j].hi - x0[j]))) for j in W)
    print(f"  box W: max width {maxw:.3e}; max distance from listed w {shift:.3e}")
    # sanity: equality rows evaluated over W contain f
    for i in act:
        v = ivl.I(M.cconst[i])
        for j, c in M.lin[i].items():
            v = v + ivl.I(c) * (W[j] if j in W else ivl.I(x[j]))
        assert v.lo <= M.cub[i] <= v.hi
    obj = F(0)
    for cj, (bj, ws, i) in elem.items():
        if x[bj] == 1:
            s = ivl.I(0)
            for j in ws:
                s = s + W[j].sqr()
            x[cj] = s.hi
        else:
            x[cj] = F(0)
        obj += x[cj]
    listed = osil.obj_exact(M, x0)
    print(f"  objective of proven point <= {float(obj)!r} (exact rational upper bound); listed point {float(listed)!r}")
    print(f"  LINDO 35.35267044 - bound = {float(F('35.35267044') - obj):.6f}; "
          f"GUROBI 8.88779974 - bound = {float(F('8.88779974') - obj):.6f}  ({time.time()-t0:.0f}s)")
    return obj


if __name__ == "__main__":
    for pk in sys.argv[1:] or ["p5", "p4"]:
        main(pk)
