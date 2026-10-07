"""Independent mpmath-interval recheck of the optcdeg2 partial-Lagrangian bound
(optcdeg2_head.py computes the same quantity with outward-rounded numpy intervals).

Recomputes, in mpmath interval arithmetic at 30 digits:
  - the global state bounds (forward-backward propagation, optcdeg2_bound.state_bounds);
  - the head reachable intervals for all u in [-0.2,0.2]^m, the interval adjoint and the
    monotonicity check p_v(t+1) > 0 for t < m;
  - J at the corner u = -0.2 by interval simulation;
  - all separable terms for t > m (y, v) and t >= m (u).
"""
import json
import sys
import time

import mpmath as mp
import numpy as np

from optcdeg2_bound import state_bounds
from optcdeg2_common import N

iv = mp.iv


def main(m):
    t0 = time.time()
    Yg, Vg = state_bounds(passes=1)
    iv.dps = 30
    mu = np.load("logs/optcdeg2_mu.npy"); lam = np.load("logs/optcdeg2_lam.npy")
    M = [iv.mpf(float(v)) for v in mu]; L = [iv.mpf(float(v)) for v in lam]
    h = iv.mpf("0.0004"); c002 = iv.mpf("0.02"); c02 = iv.mpf("0.2"); half = iv.mpf("0.5")
    U = iv.mpf(["-0.2", "0.2"])
    cy = -M[m] + c002 * h * L[m]
    cv = -h * M[m] - L[m]
    av = c02 * h * L[m]
    # head reachable intervals (all controls in the box)
    Y, V = [iv.mpf(10)], [iv.mpf(0)]
    for t in range(m):
        Y.append(Y[t] + h * V[t])
        V.append(V[t] + h * (U - c002 * Y[t] - c02 * V[t] ** 2))
    py = h * Y[m] + cy
    pv = cv + 2 * av * V[m]
    minpv = mp.inf
    for t in range(m - 1, -1, -1):
        minpv = min(minpv, mp.mpf(pv.a))
        py, pv = (h * Y[t] if t >= 1 else iv.mpf(0)) + py - c002 * h * pv, h * py + (1 - iv.mpf("0.4") * h * V[t]) * pv
    # J at the corner
    y, v = iv.mpf(10), iv.mpf(0)
    J = half * h * y ** 2
    u = iv.mpf("-0.2")
    for t in range(m):
        y, v = y + h * v, v + h * (u - c002 * y - c02 * v ** 2)
        if t < m - 1:
            J += half * h * y ** 2
    J += half * h * y ** 2 + cy * y + cv * v + av * v ** 2
    # separable rest
    rest = iv.mpf(0)
    for t in range(m + 1, N):
        b = M[t - 1] - M[t] + c002 * h * L[t]
        rest -= b ** 2 / (2 * h)
    rest -= M[N - 1] ** 2 / (2 * h)
    for t in range(m, N):
        rest -= c02 * h * abs(L[t])
    for t in range(m + 1, N):
        A = c02 * h * L[t]
        B = L[t - 1] - L[t] - h * M[t]
        lo, hi = Vg[t].a, Vg[t].b
        cands = [A * lo ** 2 + B * lo, A * hi ** 2 + B * hi]
        if mp.mpf(A.a) > 0:
            s = -B / (2 * A)
            if mp.mpf(s.b) >= mp.mpf(lo) and mp.mpf(s.a) <= mp.mpf(hi):
                cands.append(-(B ** 2) / (4 * iv.mpf(A.a)))
        rest += iv.mpf(min(mp.mpf(c.a) for c in cands))
    total = J + rest
    rec = dict(m=m, monotone=bool(minpv > 0), min_pv_lower=float(minpv), J_corner=float(mp.mpf(J.a)),
               rest=float(mp.mpf(rest.a)), dual_bound=float(mp.mpf(total.a)) if minpv > 0 else None,
               seconds=time.time() - t0)
    print(json.dumps(rec), flush=True)
    with open("logs/optcdeg2_verify.json", "w") as f:
        json.dump(rec, f, indent=1)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3080)
