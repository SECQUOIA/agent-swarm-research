"""Negative controls for the own Krawczyk code (kraw.py).

For ghg_3veh.p2 and glider100.p2 (same setup as run_kraw.py):
 1. the unperturbed test passes (positive control);
 2. a center moved by 1e-9 (relative) with radius 1e-13 fails;
 3. a system whose first row right-hand side is shifted by 1e-8 fails with the
    original center;
 4. the box check fails when an upper bound of a basic variable is lowered to
    its center value.
"""
import copy
import sys
from fractions import Fraction as F

import numpy as np

import ad
import evalpt
import kraw
import osil


def setup(name, pk, snap=0.0, act=1e-7):
    M = evalpt.model(name)
    x0, _, _ = osil.read_sol(f"data/{name}.{pk}.sol", M)
    x = list(x0)
    fixed = set()
    for j in range(M.n):
        if M.vtype[j] in ("B", "I"):
            x[j] = F(round(x[j]))
            fixed.add(j)
            continue
        for bd in (M.lb[j], M.ub[j]):
            if bd is not None and abs(x[j] - bd) <= F(snap) * max(1, abs(float(bd))):
                x[j] = bd
                fixed.add(j)
    S, sides = [], {}
    xf = [float(v) for v in x]
    for i in range(M.m):
        if not (osil.row_vars(M, i) - fixed):
            continue
        if M.clb[i] is not None and M.clb[i] == M.cub[i]:
            S.append(i)
            continue
        _, g = ad.row(M, i, xf, ad.FloatT, set(range(M.n)) - fixed)
        if not any(v != 0 for v in g.values()):
            continue
        v = float(osil.row_iv(M, i, x).mid())
        for side, bd in (("lb", M.clb[i]), ("ub", M.cub[i])):
            if bd is not None and abs(v - float(bd)) <= act * max(1.0, abs(float(bd))):
                S.append(i)
                sides[i] = side
                break
    used = set()
    for i in S:
        used |= osil.row_vars(M, i)
    cand = [j for j in range(M.n) if j not in fixed and j in used]
    B, _ = kraw.choose_basis(M, S, cand, x, log=lambda *a: None)
    return M, x, S, B, sides


def run(name, pk):
    M, x, S, B, sides = setup(name, pk)
    sysm = kraw.System(M, x, S, B, sides)
    c = kraw.newton(sysm, [x[j] for j in B], log=lambda *a: None)
    r = 1e-13 * np.maximum(np.abs(c), 1e-6)
    ok, X, info = kraw.krawczyk(sysm, c, r)
    print(f"{name}.{pk} 1 positive control: ok={ok} ratio={info['max_ratio']:.3e}")
    c2 = c * (1 + 1e-9)
    ok2, _, info2 = kraw.krawczyk(sysm, c2, r)
    print(f"{name}.{pk} 2 center moved 1e-9 rel: ok={ok2} (expected False) ratio={info2['max_ratio']:.3e}")
    M3 = copy.copy(M)
    M3.clb = list(M.clb)
    M3.cub = list(M.cub)
    i0 = S[0]
    shift = F(1, 10 ** 8) * max(1, abs(M.cub[i0] if M.cub[i0] is not None else M.clb[i0]))
    if M3.clb[i0] is not None:
        M3.clb[i0] += shift
    if M3.cub[i0] is not None:
        M3.cub[i0] += shift
    sys3 = kraw.System(M3, x, S, B, sides)
    ok3, _, info3 = kraw.krawczyk(sys3, c, r)
    print(f"{name}.{pk} 3 row {M.cname[i0]} rhs shifted by {float(shift):.1e}: ok={ok3} (expected False) ratio={info3['max_ratio']:.3e}")
    M4 = copy.copy(M)
    M4.ub = list(M.ub)
    j = B[int(np.argmax(np.abs(c)))]
    M4.ub[j] = F(float(c[B.index(j)]))
    sys4 = kraw.System(M4, x, S, B, sides)
    bok, fails, _ = kraw.box_check(M4, sys4, X)
    print(f"{name}.{pk} 4 ub of {M.vname[j]} lowered to its center: box ok={bok} (expected False) fails={fails[:2]}")
    return ok and not ok2 and not ok3 and not bok


if __name__ == "__main__":
    allok = True
    for arg in sys.argv[1:] or ["ghg_3veh.p2", "glider100.p2"]:
        n, p = arg.rsplit(".", 1)
        allok &= run(n, p)
    print("ALL CONTROLS AS EXPECTED" if allok else "SOME CONTROL FAILED")
