"""Rigorous feasible-state enclosures Y_t, V_t for optcdeg2 (reviewer code).

Every step is computed exactly in rationals and rounded outward to the dyadic grid 2^-110;
the final boxes are rounded outward to doubles. Forward pass, then one backward pass:
  forward : Y_{t+1} = Y_t + h V_t;  V_{t+1} = g(V_t) + h U - a Y_t, g(v) = v - b v^2 (increasing
            for v < 1/(2b) = 6250, asserted), intersected with [-1, inf) for 1 <= t+1 <= N-1 and
            with {0} for t+1 = N;
  backward: Y_t &= Y_{t+1} - h V_t;  V_t &= g^{-1}(V_{t+1} - h U + a Y_t)  (t = N-1..1).
Each feasible point satisfies the recurrences exactly, so by induction it lies in the boxes.
Output: logs/vt_reviewer.npy (N+1, 2) and a comparison with the first-wave stored bounds.
"""
import json
import math
import sys
from fractions import Fraction as Fr

import numpy as np
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../.."))

N = 50000
H = Fr(4, 10000)
AY = Fr(8, 10 ** 6)
BV = Fr(8, 10 ** 5)
UL, UH = Fr(-1, 5), Fr(1, 5)
VMIN = Fr(-1)


GRID = 110           # propagate on the dyadic grid 2^-GRID (outward), not in doubles:
SC = 1 << GRID       # per-step double rounding would accumulate ~5e-12 over 50000 steps


def rdn(x):
    """largest grid point <= x (exact)"""
    return Fr((x.numerator * SC) // x.denominator, SC)


def rup(x):
    return -rdn(-x)


def fdn(x):
    f = float(x)
    while Fr(f) > x:
        f = math.nextafter(f, -math.inf)
    return f


def fup(x):
    f = float(x)
    while Fr(f) < x:
        f = math.nextafter(f, math.inf)
    return f


def g(v):
    return v - BV * v * v


def ginv_dn(w):
    """grid point v < 6250 with g(v) <= w (so v <= g^{-1}(w)); Newton-corrected from a float guess."""
    wf = float(w)
    f = Fr(2 * wf / (1 + math.sqrt(1 - 4 * float(BV) * wf)))
    f = rdn(f - (g(f) - w) / (1 - 2 * BV * f))          # one exact Newton step, then onto the grid
    step = Fr(1, SC)
    while g(f) > w:
        f -= step; step *= 2
    assert f < 6000
    return f


def ginv_up(w):
    wf = float(w)
    f = Fr(2 * wf / (1 + math.sqrt(1 - 4 * float(BV) * wf)))
    f = rup(f - (g(f) - w) / (1 - 2 * BV * f))
    step = Fr(1, SC)
    while g(f) < w:
        f += step; step *= 2
    assert f < 6000
    return f


def enclosures():
    Y = [None] * (N + 1); V = [None] * (N + 1)
    Y[0] = (Fr(10), Fr(10)); V[0] = (Fr(0), Fr(0))
    for t in range(N):
        ylo, yhi = Fr(Y[t][0]), Fr(Y[t][1]); vlo, vhi = Fr(V[t][0]), Fr(V[t][1])
        assert vhi < 6000
        Y[t + 1] = (rdn(ylo + H * vlo), rup(yhi + H * vhi))
        lo = g(vlo) + H * UL - AY * yhi
        hi = g(vhi) + H * UH - AY * ylo
        if t + 1 < N:
            lo = max(lo, VMIN)
            assert lo <= hi
            V[t + 1] = (rdn(lo), rup(hi))
        else:
            assert lo <= 0 <= hi
            V[N] = (Fr(0), Fr(0))
    for t in range(N - 1, 0, -1):
        ylo = max(Fr(Y[t][0]), Fr(Y[t + 1][0]) - H * Fr(V[t][1]))
        yhi = min(Fr(Y[t][1]), Fr(Y[t + 1][1]) - H * Fr(V[t][0]))
        assert ylo <= yhi
        Y[t] = (rdn(ylo), rup(yhi))
        wlo = Fr(V[t + 1][0]) - H * UH + AY * Fr(Y[t][0])
        whi = Fr(V[t + 1][1]) - H * UL + AY * Fr(Y[t][1])
        lo = max(Fr(V[t][0]), Fr(ginv_dn(wlo)))
        hi = min(Fr(V[t][1]), Fr(ginv_up(whi)))
        assert lo <= hi
        V[t] = (lo, hi)  # grid points already
    return Y, V


def main():
    Y, V = enclosures()
    # final outward rounding to doubles
    Va = np.array([(fdn(a), fup(b)) for a, b in V]); Ya = np.array([(fdn(a), fup(b)) for a, b in Y])
    # distance of the stored (first-wave) bounds from the exact grid enclosure, in ulps of the stored value
    vb0 = np.load(_REPO + "/research-20260929/open-instances/logs/optcdeg2_vbounds.npy")
    worst_in = Fr(0); worst_t = None
    for t in range(N + 1):
        a, b = V[t]
        for side, x, st in ((0, a, Fr(vb0[t, 0])), (1, b, Fr(vb0[t, 1]))):
            inward = (st - x) if side == 0 else (x - st)   # > 0: stored bound cuts off part of the enclosure
            if inward > worst_in:
                worst_in, worst_t = inward, (t, side)
    ulp_out = None
    if worst_t is not None:
        t, side = worst_t
        st = float(vb0[t, side]); ulp_out = float(worst_in) / (abs(math.nextafter(st, math.inf) - st) or 5e-324)
    np.save("logs/vt_reviewer.npy", Va); np.save("logs/yt_reviewer.npy", Ya)
    vb = np.load(_REPO + "/research-20260929/open-instances/logs/optcdeg2_vbounds.npy")
    # certificate domain = [nextafter down of vb_lo, nextafter up of vb_hi] (ivnp dn/up, one ulp)
    cert_lo = np.nextafter(vb[:, 0], -np.inf); cert_hi = np.nextafter(vb[:, 1], np.inf)
    out = dict(V_max=float(Va[:, 1].max()), V_min=float(Va[:, 0].min()),
               max_abs_diff_vs_stored=float(np.max(np.abs(Va - vb))),
               stages_where_reviewer_V_not_inside_stored=int(np.sum((Va[:, 0] < vb[:, 0]) | (Va[:, 1] > vb[:, 1]))),
               stages_where_reviewer_V_not_inside_cert_domain=int(np.sum((Va[:, 0] < cert_lo) | (Va[:, 1] > cert_hi))),
               width_V_max=float(np.max(Va[:, 1] - Va[:, 0])),
               max_inward_excess_of_stored_over_exact=float(worst_in), at=worst_t, in_ulps=ulp_out)
    print(json.dumps(out, indent=1))
    json.dump(out, open("logs/states_check.json", "w"), indent=1)


if __name__ == "__main__":
    sys.exit(main())
