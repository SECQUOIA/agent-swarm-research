"""Exploratory stress test of hypothesis (S) (grad F(x*) = 0) of adaptive-matching.md, using the
authors' GR implementation (gr_lib.run_gr, unchanged) for speed: path family b = 0.8, kappa = 0.1 with a
linear term c_i = C on even and C2 on odd coordinates, so that the minimizer lies on a face (even coordinates at -1, odd ones interior) with grad F(x*) != 0
(KKT multipliers positive on the even coordinates). Not covered by Theorem 2. Prints the GR stage log and the summary."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import os
import sys
import numpy as np
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/theory-decomposition/adaptive2'))
from gr_lib import run_gr, global_min, F  # noqa: E402

C = float(sys.argv[1])
C2 = float(sys.argv[2])
theta = 1.0 / float(sys.argv[3])
R = float(sys.argv[4])
eps = float(sys.argv[5])
for n in [int(a) for a in sys.argv[6:]]:
    c = np.where(np.arange(n) % 2 == 0, C, C2)
    xs, fs, _ = global_min(n, 0.8, 0.1, c)
    g = 2 * xs - 0.4 * xs ** 3 + c
    g[:-1] += 0.8 * xs[1:]
    g[1:] += 0.8 * xs[:-1]
    print("n=%d C=%.2f C2=%.2f: x*[:4] = %s, f* = %.8f, grad F(x*) even [%.3f, %.3f], odd max|.| %.1e" % (
        n, C, C2, np.round(xs[:4], 6), fs, g[0::2].min(), g[0::2].max(), np.abs(g[1::2]).max()), flush=True)

    def log(r):
        print("j=%2d W=%.2e size=%8d lr=% .6e UBD=% .6e gap=%.2e zloc=%.3f gviol=%d split=%s wide=%s" % (
            r["j"], r["W"], r["leaves"] + r["cells"], r["lr"], r["UBD"], r["gap"], r["zloc"], r["graded_viol"],
            r.get("split_leaf_max"), r.get("wide_splits")), flush=True)
    res, recs = run_gr(n, 0.8, 0.1, c, eps, np.zeros(n), theta, R, jmax=24, xstar=xs, fstar=fs, log=log)
    print("SUMMARY n=%d done=%s stage=%s size=%s max_zloc=%.3f" % (n, res["done"], res.get("j"), res.get("size"),
                                                                 max(r["zloc"] for r in recs)), flush=True)
