"""Checks of the curve-hull separator.
1. Validity: every returned cut holds at 20,000 random curve points (float evaluation, with a
   relative tolerance 1e-12) for several function families.
2. Exactness for (t, t^2, t^3): the separator finds a cut (violation > 1e-6 scaled) exactly when the
   point violates the two rotated cones of the moment hull (checked on random points near the hull).
python test_curvehull.py"""
import math
import sys
import time

import numpy as np
import sympy as sp

from curvehull import T, Curve, moment3_in_hull

rng = np.random.default_rng(1)

FAMILIES = [
    ("x^2,x^3 on [0,10]", [T**2, T**3], 0, 10),
    ("x^2,x^3 on [-2,3]", [T**2, T**3], -2, 3),
    ("exp,x^2 on [-1,4]", [sp.exp(T), T**2], -1, 4),
    ("sin,cos on [-3,5]", [sp.sin(T), sp.cos(T)], -3, 5),
    ("sin,cos on [0,1]", [sp.sin(T), sp.cos(T)], 0, 1),
    ("xlogx,log on [0.01,5]", [T * sp.log(T), sp.log(T)], 0.01, 5),
    ("sqrt,x^1.852 on [0,20]", [sp.sqrt(T), T**sp.Float(1.852)], 0, 20),
    ("1/x,x^2 on [660,680]", [1 / T, T**2], 660, 680),
    ("x^3,x^6 on [-1,2]", [T**3, T**6], -1, 2),
    ("exp(-x),x*exp(-x),x^2 on [0,8]", [sp.exp(-T), T * sp.exp(-T), T**2], 0, 8),
]


def random_hull_point(C, spread=0.3):
    """Convex combination of 3 curve points plus a perturbation in scaled space."""
    ts = rng.uniform(C.l, C.u, 3)
    w = rng.dirichlet(np.ones(3))
    p = C.phi(ts) @ w
    return p + rng.normal(0, spread, p.shape) * C.wid * rng.uniform(0, 1)


def validity():
    worst = 0.0
    for name, fs, l, u in FAMILIES:
        t0 = time.time()
        C = Curve(fs, l, u)
        tt = np.concatenate([rng.uniform(l, u, 20000), [l, u]])
        P = C.phi(tt)
        ncut, shifts = 0, []
        for _ in range(60):
            cut = C.separate(random_hull_point(C))
            if cut is None:
                continue
            ncut += 1
            val = cut["c0"] + cut["c"] @ P
            scale = 1 + np.abs(cut["c"]) @ np.abs(P)
            rel = float((val / scale).min())
            worst = min(worst, rel)
            fmin = C.float_min(cut["c"])[1]
            shifts.append((cut["c0"] + fmin) / (1 + np.abs(cut["c"]) @ np.maximum(np.abs(C.rlo), np.abs(C.rhi))))
            assert rel > -1e-12, (name, rel)
        print(f"{name:34s} cuts {ncut:2d}  min rel slack on curve {min(0, worst):.1e}  "
              f"certification shift (rel) max {max(shifts) if shifts else 0:.1e}  {time.time() - t0:.1f}s")
    return worst


def moment_crosscheck(l, u, n=400):
    C = Curve([T**2, T**3], l, u)
    agree = disagree = 0
    rows = []
    for _ in range(n):
        p = random_hull_point(C, spread=0.05)
        s = moment3_in_hull(p, l, u)
        cut = C.separate(p, min_viol=1e-7)
        inside = s >= 0
        if inside == (cut is None):
            agree += 1
        else:
            disagree += 1
            rows.append((s, None if cut is None else cut["viol_scaled"]))
    print(f"moment cross-check [{l},{u}]: agree {agree}, disagree {disagree}; "
          f"disagreements (cone slack, cut violation): {rows[:5]}")
    return disagree, rows


if __name__ == "__main__":
    validity()
    bad = 0
    for l, u in [(0, 1), (0, 10), (-2, 3), (1, 2)]:
        d, rows = moment_crosscheck(l, u)
        # borderline disagreements are expected only within tolerance
        bad += sum(1 for s, v in rows if abs(s) > 1e-5 and (v is None or v > 1e-5))
    print("non-borderline disagreements:", bad)
    sys.exit(1 if bad else 0)
