"""Reviewer check of Theorem A.5(b) (localization of split leaves) on the path family, c = 0:
largest sup-distance from x*_{V_t} of a leaf split at level i, in units of s_i, versus sqrt(n).
One pass with exact slopes (oracle, as in the note's C.1) and LS with restarts (last pass)."""
import sys
import numpy as np
import indep_ls as R

eps = float(sys.argv[2])
for n in [int(v) for v in sys.argv[1].split()]:
    for tag in ("oracle", "LS"):
        if tag == "oracle":
            res, recs = R.ls(n, np.zeros(n), eps, np.zeros(n), pmax=30, fixed_lam=np.zeros(n), xstar=np.zeros(n))
        else:
            res, recs = R.ls(n, np.zeros(n), eps, np.full(n, 0.5), pmax=30, xstar=np.zeros(n))
        rs = [r for r in recs if r["p"] == res["p"] and r["live_mean"] > 0]
        far = [r["far_s"] for r in rs]
        mid = [r["far_s"] for r in rs if 4 <= r["i"] <= res["i"] - 2]
        print("n=%3d %-6s levels=%d  max far/s over levels=%.2f  median over middle levels=%.2f  "
              "(max far/s)/sqrt(n)=%.2f  per level: %s" % (
                  n, tag, res["i"], max(far), float(np.median(mid)) if mid else float("nan"),
                  max(far) / np.sqrt(n), " ".join("%.1f" % v for v in far)), flush=True)
