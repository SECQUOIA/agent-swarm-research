"""Experiments for Part A of extension-adaptive.md (algorithm LS on the path family).

  python3 run_ls.py scaling  NMAX EPS   # c = 0, LS with restarts, x0 = 0.5*ones; n = 4,8,...,NMAX
  python3 run_ls.py oracle   NMAX EPS   # c = 0, one pass with the exact slopes (lam = 0), no restarts
  python3 run_ls.py random   N    EPS   # c ~ U(-0.2,0.2)^n (seeds 0,1): LS vs oracle slopes vs zero slopes
                                        # (zero slopes capped at 10 levels)

Per sublevel the log prints: pass p, sublevel i, leaves, cells, root bound l_r, incumbent UBD,
live_mean / live_max = level-i leaves per bag with min-marginal < UBD - eps (these are split),
viol = frozen boxes with min-marginal < UBD - eps (Lemma A.2 predicts 0),
dx2 / dxinf = distance of the consistent point of the minimizing configuration to x*, nu = slope error.
"""
import sys
import time
import numpy as np
from ls_lib import run_ls, global_min, slopes

B, KAPPA = 0.8, 0.1


def fmt(r):
    s = "p=%2d i=%2d leaves=%7d cells=%6d lr=% .3e UBD=% .3e live_mean=%7.1f live_max=%5d viol=%d" % (
        r["p"] if r["p"] is not None else -1, r["i"], r["leaves"], r["cells"], r["lr"], r["UBD"],
        r["live_mean"], r["live_max"], r["viol"])
    if "dx2" in r:
        s += " dx2=%.2e dxinf=%.2e" % (r["dx2"], r["dxinf"])
    if r.get("nu") is not None:
        s += " nu=%.2e" % r["nu"]
    return s


def summary(tag, n, eps, res, recs, secs):
    lv = [r["live_mean"] for r in recs if r["p"] == res.get("p") and r["live_mean"] > 0]
    print("SUMMARY %s n=%d eps=%.0e done=%s pass=%s level=%s size=%s leaves=%s cells=%s "
          "total_boxes=%d lr=%.3e UBD=%.3e max_live_mean=%.1f viol=%d time=%.1fs" % (
              tag, n, eps, res["done"], res.get("p"), res.get("i"), res.get("size"),
              res.get("leaves"), res.get("cells"), res["total_boxes"], res.get("lr", np.nan),
              res.get("UBD", np.nan), max(lv) if lv else 0.0, sum(r["viol"] for r in recs), secs),
          flush=True)


def main():
    mode = sys.argv[1]
    eps = float(sys.argv[3])
    if mode in ("scaling", "oracle"):
        nmax = int(sys.argv[2])
        n = 4
        while n <= nmax:
            c = np.zeros(n)
            t0 = time.time()
            if mode == "scaling":
                res, recs = run_ls(n, B, KAPPA, c, eps, np.full(n, 0.5), pmax=30,
                                   xstar=np.zeros(n), fstar=0.0)
            else:
                res, recs = run_ls(n, B, KAPPA, c, eps, np.zeros(n), pmax=30, xstar=np.zeros(n),
                                   fstar=0.0, fixed_lam=np.zeros(n))
            last = res.get("p")
            for r in recs:
                if r["p"] == last:
                    print(fmt(r))
            summary(mode, n, eps, res, recs, time.time() - t0)
            n *= 2
    elif mode == "random":
        n = int(sys.argv[2])
        for seed in (0, 1):
            c = np.random.default_rng(seed).uniform(-0.2, 0.2, n)
            xs, fs, _ = global_min(n, B, KAPPA, c)
            lam_star = slopes(xs, B, KAPPA, c)
            print("seed %d: f* = %.10f, |x*|_inf = %.3f, lam* in [%.3f, %.3f]" % (
                seed, fs, np.abs(xs).max(), lam_star[1:n - 1].min(), lam_star[1:n - 1].max()))
            for tag, kw in (("LS", dict(x0=np.zeros(n))),
                            ("oracle", dict(x0=xs.copy(), fixed_lam=lam_star)),
                            ("zero", dict(x0=xs.copy(), fixed_lam=np.zeros(n), pmax=10))):
                t0 = time.time()
                res, recs = run_ls(n, B, KAPPA, c, eps, kw["x0"], pmax=kw.get("pmax", 30), xstar=xs,
                                   fstar=fs, fixed_lam=kw.get("fixed_lam"))
                last = res.get("p")
                for r in recs:
                    if r["p"] == last:
                        print(fmt(r) + " gap=%.2e" % r["gap"])
                summary("%s-seed%d" % (tag, seed), n, eps, res, recs, time.time() - t0)


if __name__ == "__main__":
    main()
