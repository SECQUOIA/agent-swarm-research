"""Revision check for Section C.2 of extension-adaptive.md: split the LS-versus-oracle size
difference into a slope part and an incumbent part (issue raised in the review).

  python3 check_slope_incumbent.py N EPS     # c ~ U(-0.2,0.2)^N, seeds 0 and 1

For each instance run LS from x0 = 0 (as run_ls.py random). Take the slopes lam_LS of its final
pass and the incumbent point xbest it had at the start of that pass. Then run single passes with
  A: exact slopes lam*, exact incumbent (x0 = x*)       -- the "oracle" of Section C.2
  B: lam_LS,            exact incumbent                -- slope effect only
  C: lam*,              LS incumbent (x0 = xbest)      -- incumbent effect only
  D: lam_LS,            LS incumbent                   -- must reproduce the final LS pass
  E: lam*,              x0 = 0                         -- exact slopes, no incumbent help
Sizes are reported relative to A.
"""
import sys
import time
import numpy as np
from ls_lib import run_ls, global_min, slopes

B, KAPPA = 0.8, 0.1


def main():
    n, eps = int(sys.argv[1]), float(sys.argv[2])
    for seed in (0, 1):
        c = np.random.default_rng(seed).uniform(-0.2, 0.2, n)
        xs, fs, _ = global_min(n, B, KAPPA, c)
        lams = slopes(xs, B, KAPPA, c)
        t0 = time.time()
        res, _ = run_ls(n, B, KAPPA, c, eps, np.zeros(n), pmax=30, xstar=xs, fstar=fs)
        st = res["start"]
        print("seed %d n=%d: LS size=%d pass=%d level=%d; final-pass nu=%.3e; incumbent at pass start "
              "UBD0-f*=%.3e (%.2f eps)  [%.1fs]" % (
                  seed, n, res["size"], res["p"], res["i"], np.linalg.norm(st["lam"] - lams),
                  st["UBD"] - fs, (st["UBD"] - fs) / eps, time.time() - t0), flush=True)
        base = None
        for tag, lam, x0 in (("A exact slopes, exact incumbent", lams, xs),
                             ("B LS slopes,    exact incumbent", st["lam"], xs),
                             ("C exact slopes, LS incumbent   ", lams, st["xbest"]),
                             ("D LS slopes,    LS incumbent   ", st["lam"], st["xbest"]),
                             ("E exact slopes, x0 = 0         ", lams, np.zeros(n))):
            r, _ = run_ls(n, B, KAPPA, c, eps, x0.copy(), pmax=30, fixed_lam=lam)
            base = base or r["size"]
            print("   %s: size=%7d level=%2d processed=%8d size/A=%.3f" % (
                tag, r["size"], r["i"], r["total_boxes"], r["size"] / base), flush=True)


if __name__ == "__main__":
    main()
