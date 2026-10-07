"""Confirmation check d6: multipliers (gradients) on the bang stages of the
saved N = 100 KKT point, 2-D COPS form (gradient code of d1).  Strict
complementarity on the bang stages is what lets a float KKT point with a
tiny Newton step stand for an exact KKT point with the same active set."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import mpmath as mp
import numpy as np
import d1_audit_2d as d1

base = (_PUBLIC_REPO + '/research-20260929/theory-bangbang/singular/logs/')
for N, f in ((100, "catmix100_smooth_u.npy"), (200, "catmix200_smooth_u.npy")):
    uf = np.load(base + f)
    J, g = d1.grad([mp.mpf(float(v)) for v in uf], mp.mpf(1) / N)
    gf = np.array([float(v) for v in g])
    up = [j for j in range(N + 1) if uf[j] >= 1 - 1e-9]
    lo = [j for j in range(N + 1) if uf[j] <= 1e-9]
    ku = min(up, key=lambda j: abs(gf[j]))
    kl = min(lo, key=lambda j: abs(gf[j]))
    print("N=%d: u=1 stages %d..%d, min |g| = %.2e at stage %d (sign %s, needs <= 0); u=0 stages: %d of them, "
          "min |g| = %.2e at stage %d (g = %.2e, needs >= 0)"
          % (N, up[0], up[-1], abs(gf[ku]), ku, "-" if gf[ku] < 0 else "+", len(lo), abs(gf[kl]), kl, gf[kl]))
