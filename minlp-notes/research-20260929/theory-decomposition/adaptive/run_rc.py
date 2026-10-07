"""Experiments for algorithm RC (rc_lib.py), Section A.6 of extension-adaptive.md.

  python3 run_rc.py zero   NMAX EPS [JMAX]   # c = 0, x0 = 0.5*ones, n = 4, 8, ..., NMAX, theta = 1/16
  python3 run_rc.py random N    EPS [JMAX]   # c ~ U(-0.2,0.2)^n, seeds 0 and 1, x0 = 0
  python3 run_rc.py randomlocal N EPS [JMAX] # same, with a local solve (L-BFGS-B) from each consistent point
JMAX (default 30) caps the number of rounds.

Per round: central width h, size, root bound, incumbent, cen_inf = |xhat - x*|_inf / h,
x_inf = |x_cons - x*|_inf / h and x_2 = |x_cons - x*|_2 / h for the new consistent point.
"""
import sys
import time
import numpy as np
from rc_lib import run_rc
from ls_lib import global_min

B, KAPPA = 0.8, 0.1


def fmt(r):
    s = "j=%2d h=%.2e leaves=%8d cells=%6d lr=% .3e UBD=% .3e" % (
        r["j"], r["h"], r["leaves"], r["cells"], r["lr"], r["UBD"])
    if "cen_inf" in r:
        s += " cen_inf/h=%.2f x_inf/h=%.2f x_2/h=%.2f nu=%.2e" % (r["cen_inf"], r["x_inf"], r["x_2"], r["nu"])
    if "gap" in r:
        s += " gap=%.2e" % r["gap"]
    return s


def main():
    mode, eps = sys.argv[1], float(sys.argv[3])
    jmax = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    if mode == "zero":
        n = 4
        while n <= int(sys.argv[2]):
            t0 = time.time()
            res, recs = run_rc(n, B, KAPPA, np.zeros(n), eps, np.full(n, 0.5), xstar=np.zeros(n),
                               fstar=0.0, log=lambda r: print(fmt(r), flush=True), jmax=jmax)
            print("SUMMARY rc n=%d eps=%.0e %s time=%.1fs" % (n, eps, res, time.time() - t0), flush=True)
            n *= 2
    else:
        n = int(sys.argv[2])
        for seed in (0, 1):
            c = np.random.default_rng(seed).uniform(-0.2, 0.2, n)
            xs, fs, _ = global_min(n, B, KAPPA, c)
            t0 = time.time()
            res, recs = run_rc(n, B, KAPPA, c, eps, np.zeros(n), xstar=xs, fstar=fs,
                               log=lambda r: print(fmt(r), flush=True), local=(mode == "randomlocal"),
                               jmax=jmax)
            print("SUMMARY rc-seed%d n=%d eps=%.0e %s time=%.1fs" % (seed, n, eps, res, time.time() - t0),
                  flush=True)


if __name__ == "__main__":
    main()
