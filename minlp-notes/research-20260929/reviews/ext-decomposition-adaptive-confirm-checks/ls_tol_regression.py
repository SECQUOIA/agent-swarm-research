"""Confirmation check: LS (one pass, exact slopes lam = 0, c = 0, n = 16, eps = 1e-6) with the
leaf-cell intersection test widened by 1e-12 must give the same numbers as the closed test
(extension-adaptive.md, Section E last row / Section F item 6)."""
import os
import sys
import numpy as np
AD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "theory-decomposition", "adaptive")
sys.path.insert(0, AD)
import ls_lib  # noqa: E402

orig = ls_lib.dp
for tol in (0.0, 1e-12):
    ls_lib.dp = lambda P, lam, b, kappa, c, _t=tol: orig(P, lam, b, kappa, c, tol=_t)
    n = 16
    res, recs = ls_lib.run_ls(n, 0.8, 0.1, np.zeros(n), 1e-6, np.zeros(n), pmax=30, xstar=np.zeros(n),
                              fstar=0.0, fixed_lam=np.zeros(n))
    lv = max(r["live_mean"] for r in recs)
    print("tol=%.0e size=%d level=%d lr=%.6e total=%d max split per bag=%.1f viol=%d" % (
        tol, res["size"], res["i"], res["lr"], res["total_boxes"], lv, sum(r["viol"] for r in recs)), flush=True)
