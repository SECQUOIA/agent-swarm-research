"""Driver: Krawczyk existence proof near a listed point.

Usage: python3 run_kraw.py name.pK [--act TOL] [--snap TOL] [--rho 1e-12,1e-10,1e-8]
- integer variables are rounded and fixed;
- variables within --snap (absolute, relative to max(1,|x|)) of a bound are put
  exactly on it and fixed (default: only exact equality);
- the system is all equality rows plus inequality rows within --act (relative)
  of a side, held at that side;
- rows whose variables are all fixed are checked exactly in the box check.
"""
import argparse
import json
import os
import sys
import time
from fractions import Fraction as F

import numpy as np

import ad
import evalpt
import ivl
import kraw
import osil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("point")
    ap.add_argument("--act", type=float, default=1e-7)
    ap.add_argument("--snap", type=float, default=0.0)
    ap.add_argument("--rho", default="1e-13,1e-12,1e-11,1e-10,1e-9,1e-8")
    ap.add_argument("--floor", type=float, default=1e-6, help="radius floor scale")
    a = ap.parse_args()
    name, pk = a.point.rsplit(".", 1)
    M = evalpt.model(name)
    x0, missing, _ = osil.read_sol(os.path.join(HERE, "data", f"{name}.{pk}.sol"), M)
    x = list(x0)
    fixed = set()
    for j in range(M.n):
        if M.vtype[j] in ("B", "I"):
            x[j] = F(round(x[j]))
            fixed.add(j)
            continue
        for bd in (M.lb[j], M.ub[j]):
            if bd is not None and abs(x[j] - bd) <= F(a.snap) * max(1, abs(float(bd))):
                x[j] = bd
                fixed.add(j)
    # system rows
    S, sides = [], {}
    xf = [float(v) for v in x]
    for i in range(M.m):
        vs = osil.row_vars(M, i)
        if not (vs - fixed):
            continue
        if M.clb[i] is not None and M.clb[i] == M.cub[i]:
            S.append(i)
            continue
        v = float(osil.row_iv(M, i, x).mid()) if not osil.is_algebraic(M.nl[i]) else float(osil.row_exact(M, i, x))
        _, g = ad.row(M, i, xf, ad.FloatT, set(range(M.n)) - fixed)
        if not any(v != 0 for v in g.values()):
            continue  # constant after fixing: decided in the box check
        for side, bd in (("lb", M.clb[i]), ("ub", M.cub[i])):
            if bd is not None and abs(v - float(bd)) <= a.act * max(1.0, abs(float(bd))):
                S.append(i)
                sides[i] = side
                break
    cand = [j for j in range(M.n) if j not in fixed and any(True for _ in [0])]
    used = set()
    for i in S:
        used |= osil.row_vars(M, i)
    cand = [j for j in cand if j in used]
    print(f"{a.point}: n={M.n} m={M.m} fixed={len(fixed)} system rows={len(S)} (active ineq {len(sides)}) candidates={len(cand)}")
    B, d = kraw.choose_basis(M, S, cand, x)
    sysm = kraw.System(M, x, S, B, sides)
    cB = [x[j] for j in B]
    c = kraw.newton(sysm, cB)
    res = dict(point=a.point, fixed=len(fixed), rows=len(S), active_ineq=len(sides), basis=len(B))
    for rho in [float(t) for t in a.rho.split(",")]:
        r = rho * np.maximum(np.abs(c), a.floor)
        t0 = time.time()
        ok, X, info = kraw.krawczyk(sysm, c, r)
        print(f"  rho={rho:g}: krawczyk ok={ok} {info} ({time.time()-t0:.1f}s)")
        if ok:
            bok, fails, ob = kraw.box_check(M, sysm, X)
            print(f"  box check ok={bok}; fails={fails[:5]}")
            print(f"  objective enclosure [{float(ob.lo)!r}, {float(ob.hi)!r}] width {float(ob.hi-ob.lo):.3e}")
            mv = max(abs(float(c[k]) - float(x0[j])) for k, j in enumerate(B))
            print(f"  max |center - listed| over basic vars = {mv:.3e}")
            res.update(rho=rho, krawczyk=info, box_ok=bok, fails=fails[:20],
                       obj_lo=str(ob.lo), obj_hi=str(ob.hi), obj_lo_f=float(ob.lo), obj_hi_f=float(ob.hi),
                       max_shift=mv)
            if bok:
                break
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    with open(os.path.join(HERE, "logs", f"kraw_{a.point}.json"), "w") as f:
        json.dump(res, f, indent=1, default=str)


if __name__ == "__main__":
    main()
