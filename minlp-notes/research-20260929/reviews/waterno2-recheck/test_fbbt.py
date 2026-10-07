"""Checks of vbb2's outward-rounded float propagation.

A. Inclusion against vbb.py's exact propagation.  For random sub-boxes, one
   pass of rows (and of monomials) is run from the same box in both codes.
   Required: float box contains exact box, and float 'empty' implies exact
   'empty'.
B. Exactly feasible rational points (first verifier, waterno2_06 periods
   0, 4, 5 at the certificate multipliers) stay inside the float FBBT box for
   random sub-boxes that contain them, and FBBT never declares such a box
   empty.
usage: python3 test_fbbt.py n_boxes
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import random
import sys
import time
from fractions import Fraction as F

import vbb2
from vbb2 import vbb

W2 = _RESEARCH + "/open-instances-wave2/waterno2/logs/"
V1 = _RESEARCH + "/reviews/waterno2-verification/logs/"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
rng = random.Random(12345)


def period(T, t):
    mult = json.load(open(W2 + f"mult_{T:02d}_w1_impl.json"))
    lam = [[float(v) for v in l] for l in mult["lam"]]
    return vbb2.PeriodF(T, t, lam, float(mult["mu"]))


def random_box(P, lo, hi, point=None, prob=0.3):
    lo, hi = list(lo), list(hi)
    for j in range(P.n):
        if rng.random() < prob and vbb.fin(lo[j]) and vbb.fin(hi[j]) and hi[j] > lo[j]:
            if P.isbin[j]:
                v = float(rng.randint(0, 1)) if point is None else float(point[j])
                lo[j] = hi[j] = v
                continue
            a, b = sorted((rng.uniform(lo[j], hi[j]), rng.uniform(lo[j], hi[j])))
            if point is not None:
                a, b = min(a, vbb2.fdn(point[j])), max(b, vbb2.fup(point[j]))
                a, b = max(a, lo[j]), min(b, hi[j])
            lo[j], hi[j] = a, b
    return lo, hi


stats = {"both_nonempty": 0, "both_empty": 0, "float_only_nonempty": 0}


def check_inclusion(P, lo, hi):
    """one pass of rows and of monomials; returns the number of violations"""
    bad = 0
    for name in ("_rows", "_mons"):
        l1, h1, l2, h2 = lo[:], hi[:], lo[:], hi[:]
        okf = getattr(vbb2.PeriodF, name)(P, l1, h1)
        oke = getattr(vbb.Period, name)(P, l2, h2)
        if not okf:
            if oke:
                print("UNSOUND: float empty, exact not", name)
                bad += 1
            else:
                stats["both_empty"] += 1
            continue
        if not oke:
            stats["float_only_nonempty"] += 1
            continue
        stats["both_nonempty"] += 1
        for j in range(P.n):
            if l1[j] > l2[j] or h1[j] < h2[j]:
                print("UNSOUND inclusion", name, j, l1[j], l2[j], h1[j], h2[j])
                bad += 1
    return bad


def inside(l, h, v):
    return (l == -vbb.INF or F(l) <= v) and (h == vbb.INF or v <= F(h))


tic = time.time()
bad = 0
cnt = 0
for (T, t) in [(9, 0), (9, 3), (18, 15), (24, 22), (24, 23)]:
    P = period(T, t)
    root = P.fbbt(P.lo0, P.hi0)
    for k in range(N):
        base = (P.lo0, P.hi0) if k % 4 == 0 else root
        lo, hi = random_box(P, *base, prob=rng.choice((0.02, 0.05, 0.1, 0.3)))
        bad += check_inclusion(P, lo, hi)
        cnt += 1
print(f"A: {cnt} random boxes x 2 passes {stats}, unsound cases: {bad} ({time.time()-tic:.0f}s)", flush=True)

# B: exactly feasible points of waterno2_06
T = 6
mult = json.load(open(W2 + "mult_06_w1_impl.json"))
lam = [[float(v) for v in l] for l in mult["lam"]]
bad_b = 0
for t in (0, 4, 5):
    pt = {k: F(v) for k, v in json.load(open(V1 + f"cert_exact_point_p{t}.json")).items()}
    P = vbb2.PeriodF(T, t, lam, float(mult["mu"]))
    z = [pt[nm] for nm in P.names]
    for (kind, x, y, w) in P.aux:
        z.append(z[x] ** 2 if kind == "sq" else z[x] ** 3 if kind == "cube" else z[x] * z[y])
    assert all(inside(P.lo0[j], P.hi0[j], z[j]) for j in range(P.n))
    nb = 0
    for k in range(N):
        lo, hi = random_box(P, P.lo0, P.hi0, z)
        assert all(inside(lo[j], hi[j], z[j]) for j in range(P.n))
        r = P.fbbt(lo, hi, 30)
        if r is None:
            print("UNSOUND: box with feasible point declared empty", t, k)
            bad_b += 1
            continue
        l2, h2 = r
        out = [j for j in range(P.n) if not inside(l2[j], h2[j], z[j])]
        if out:
            print("UNSOUND: feasible point cut off", t, k, out[:5])
            bad_b += 1
        nb += 1
    print(f"B: period {t}: {nb} boxes checked", flush=True)
print(f"B: unsound cases: {bad_b} ({time.time()-tic:.0f}s)")
print("PASS" if bad == 0 and bad_b == 0 else "FAIL")
