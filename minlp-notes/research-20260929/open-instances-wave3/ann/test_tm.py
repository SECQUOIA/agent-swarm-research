"""Soundness and tightness checks of ann_tm bounds (float sampling; a violation flags a bug).

    python3 test_tm.py [nbox] [sep]
For random boxes of several sizes (around the optimum and uniformly placed): every sampled
point u in the box is evaluated in floats (ann_bb.Model.ffun); if it is feasible with margin
1e-9 its objective must be >= the rigorous box bound (up to 1e-7 relative float noise).
Also prints the fraction of boxes fathomed at UB by the old first-order bound (ann_fast) and
by the Taylor-model bound.
"""
import sys
import time

import numpy as np

import ann_tm as at

NB = int(sys.argv[1]) if len(sys.argv) > 1 else 200
M = at.SepModel() if (len(sys.argv) > 2 and sys.argv[2] == "sep") else at.TMModel()
u = np.array([370.9280572920674, 0.7863373968889928, 1.620252679906157, 0.9494678019619749, 0.734065236105183])
fstar = -3379.982394046125
rng = np.random.default_rng(0)
scale = M.hi0 - M.lo0


SIDES = [(j, s, b) for j, s, b in M.sides]


def feas_f(p):
    """float feasibility with margin 1e-9 on the sides that can bind (tanh outputs lie in [-1, 1]
    and the +-1e6 / -1e9 bounds are far from the network's range: checked by the TM ranges)."""
    f, g, X, G = M.ffun(p)
    ok = all(s * (X[j] - b) >= 1e-9 for j, s, b in SIDES)
    return ok, f


viol = 0; tot = 0; margin = INF = np.inf
for mode in ["near", "uniform"]:
    for rho in [0.3, 0.1, 0.03, 0.01, 0.003, 0.001]:
        if mode == "near":
            e = rng.standard_normal((NB, 5)); e /= np.linalg.norm(e, axis=1)[:, None]
            c = np.clip(u + rho * scale * e * rng.random((NB, 1)), M.lo_in, M.hi_in)
        else:
            c = M.lo_in + (M.hi_in - M.lo_in) * rng.random((NB, 5))
        r = 0.5 * rho * scale * (0.5 + rng.random((NB, 5)))
        lo = np.maximum(c - r, M.lo0); hi = np.minimum(c + r, M.hi0)
        t = time.time(); R = M.tmbound(lo, hi, fbbt_rounds=0); dt = time.time() - t
        rfr = np.median(R["rf"] / np.abs(R["af"]).sum(axis=1))
        R1 = M.fbound(lo, hi)
        fin = np.isfinite(R1["lb"])
        # sampling
        for k in range(NB):
            for p in lo[k] + (hi[k] - lo[k]) * rng.random((6, 5)):
                ok, fv = feas_f(p)
                if ok:
                    tot += 1
                    margin = min(margin, fv - R["lb"][k])
                    if fv < R["lb"][k] - 1e-7 * abs(fv):
                        viol += 1
        print(f"{mode:8s} rho={rho:<6}: infeasible old {np.mean(~fin):.2f} tm {np.mean(~np.isfinite(R['lb'])):.2f}; "
              f"fathomed old {np.mean(R1['lb'] >= fstar):.2f} tm {np.mean(R['lb'] >= fstar):.2f}; "
              f"median gap to f* on boxes open in both: old {np.median(fstar - R1['lb'][(R1['lb'] < fstar) & (R['lb'] < fstar)]) if np.any((R1['lb'] < fstar) & (R['lb'] < fstar)) else 0:.3g} "
              f"tm {np.median(fstar - R['lb'][(R1['lb'] < fstar) & (R['lb'] < fstar)]) if np.any((R1['lb'] < fstar) & (R['lb'] < fstar)) else 0:.3g}; "
              f"median r_f/||a_f||_1 {rfr:.3g}; {dt / NB * 1e3:.2f} ms/box", flush=True)
print(f"soundness: {viol} violations of {tot} feasible samples; smallest margin f - lb = {margin:.3g}")
