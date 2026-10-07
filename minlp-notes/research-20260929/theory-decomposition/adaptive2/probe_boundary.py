"""Exploratory probe of hypothesis (S) (grad F(x*) = 0) of adaptive-matching.md (revision after review).

  python3 probe_boundary.py

Path family b = 0.8, kappa = 0.1 on [-1,1]^n with linear terms that put x* on the boundary:
  vertex: c_i = 3.5 for all i (x* = -1, grad F(x*) > 0 componentwise);
  face:   c_i = 3.5 (i even), 0.5 (i odd) (even coordinates at -1 with positive gradient, odd ones interior).
GR (gr_lib.run_gr, unchanged) with theta = 1/8, R = 4, eps = 1e-4, x0 = 0. x* from the grid DP plus
L-BFGS-B of dp_certificate.global_min; its KKT conditions are printed. Not covered by Theorem 2;
floating point; an illustration, not a test of a claim.
"""
import time
import numpy as np
from gr_lib import run_gr, global_min

b, kappa = 0.8, 0.1
for name, n in (("vertex", 8), ("vertex", 16), ("face", 8), ("face", 16)):
    c = np.full(n, 3.5) if name == "vertex" else np.where(np.arange(n) % 2 == 0, 3.5, 0.5)
    xs, fs, _ = global_min(n, b, kappa, c)
    g = 2 * xs - 4 * kappa * xs ** 3 + c
    g[:-1] += b * xs[1:]
    g[1:] += b * xs[:-1]
    at_lo = xs <= -1 + 1e-9
    print("%s n=%d: f* = %.8f, coordinates at -1: %d, grad there in [%.3f, %.3f], "
          "max |grad| at interior coordinates %.1e" % (
              name, n, fs, at_lo.sum(), g[at_lo].min(), g[at_lo].max(),
              np.abs(g[~at_lo]).max() if (~at_lo).any() else 0.0), flush=True)
    t0 = time.time()
    res, recs = run_gr(n, b, kappa, c, 1e-4, np.zeros(n), 1 / 8, 4.0, jmax=24, xstar=xs, fstar=fs)
    print("  done=%s stop stage=%s size=%s zloc by stage: %s  (%.0fs)" % (
        res["done"], res.get("j"), res.get("size"),
        " ".join("%.2f" % r["zloc"] for r in recs), time.time() - t0), flush=True)
