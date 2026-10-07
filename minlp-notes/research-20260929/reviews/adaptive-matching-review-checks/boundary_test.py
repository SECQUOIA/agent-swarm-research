"""Exploratory stress test of hypothesis (S) (grad F(x*) = 0) of adaptive-matching.md, using the
authors' GR implementation (gr_lib.run_gr, unchanged) for speed: path family b = 0.8, kappa = 0.1 with a
large linear term c_i = C, so that the minimizer is the vertex x* = (-1, ..., -1) with grad F(x*) != 0
(KKT multipliers positive). Not covered by Theorem 2. Prints the GR stage log and the summary."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import os
import sys
import numpy as np
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/theory-decomposition/adaptive2'))
from gr_lib import run_gr, global_min, F  # noqa: E402

C = float(sys.argv[1])
theta = 1.0 / float(sys.argv[2])
R = float(sys.argv[3])
eps = float(sys.argv[4])
for n in [int(a) for a in sys.argv[5:]]:
    c = np.full(n, C)
    xs, fs, _ = global_min(n, 0.8, 0.1, c)
    g = np.array([2 * x - 0.4 * x ** 3 + C for x in xs])
    g[:-1] += 0.8 * xs[1:]
    g[1:] += 0.8 * xs[:-1]
    print("n=%d C=%.2f: x* = %s..., f* = %.8f, F(-1) = %.8f, grad F(x*) range [%.3f, %.3f]" % (
        n, C, np.round(xs[:3], 6), fs, F(-np.ones(n), 0.8, 0.1, c), g.min(), g.max()), flush=True)

    def log(r):
        print("j=%2d W=%.2e size=%8d lr=% .6e UBD=% .6e gap=%.2e zloc=%.3f gviol=%d split=%s wide=%s" % (
            r["j"], r["W"], r["leaves"] + r["cells"], r["lr"], r["UBD"], r["gap"], r["zloc"], r["graded_viol"],
            r.get("split_leaf_max"), r.get("wide_splits")), flush=True)
    res, recs = run_gr(n, 0.8, 0.1, c, eps, np.zeros(n), theta, R, jmax=24, xstar=xs, fstar=fs, log=log)
    print("SUMMARY n=%d done=%s stage=%s size=%s max_zloc=%.3f" % (n, res["done"], res.get("j"), res.get("size"),
                                                                 max(r["zloc"] for r in recs)), flush=True)
