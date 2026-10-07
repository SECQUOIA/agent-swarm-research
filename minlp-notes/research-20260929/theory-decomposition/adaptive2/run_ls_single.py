"""Algorithm LS of extension-adaptive.md (../adaptive/ls_lib.py, unchanged) for one n, for comparison
with GR (adaptive-matching.md, Section 5.2).

  python3 run_ls_single.py scaling N EPS   # c = 0, LS with restarts and learned slopes, x0 = 0.5*ones
  python3 run_ls_single.py oracle  N EPS   # c = 0, one pass with the exact slopes (lam = 0), x0 = x* = 0
"""
import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "adaptive"))
from ls_lib import run_ls  # noqa: E402

B, KAPPA = 0.8, 0.1


def main():
    mode, n, eps = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    t0 = time.time()
    if mode == "scaling":
        res, recs = run_ls(n, B, KAPPA, np.zeros(n), eps, np.full(n, 0.5), pmax=30,
                           xstar=np.zeros(n), fstar=0.0)
    else:
        res, recs = run_ls(n, B, KAPPA, np.zeros(n), eps, np.zeros(n), pmax=30, xstar=np.zeros(n),
                           fstar=0.0, fixed_lam=np.zeros(n))
    last = res.get("p")
    for r in recs:
        if r["p"] == last:
            print("p=%s i=%2d leaves=%8d cells=%6d lr=% .4e UBD=% .4e live_mean=%8.1f live_max=%6d viol=%d dxinf/s_i=%.2f" % (
                r["p"], r["i"], r["leaves"], r["cells"], r["lr"], r["UBD"], r["live_mean"], r["live_max"],
                r["viol"], r["dxinf"] / (2.0 * 2.0 ** (-r["i"]))), flush=True)
    lv = [r["live_mean"] for r in recs if r["p"] == last and r["live_mean"] > 0]
    print("SUMMARY LS-%s n=%d eps=%.0e done=%s pass=%s level=%s size=%s total_boxes=%d "
          "max_live_mean=%.1f (%.1f n) viol=%d time=%.1fs" % (
              mode, n, eps, res["done"], res.get("p"), res.get("i"), res.get("size"), res["total_boxes"],
              max(lv), max(lv) / n, sum(r["viol"] for r in recs), time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
