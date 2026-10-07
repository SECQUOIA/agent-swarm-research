"""Reviewer reproduction of the LS tables of extension-adaptive.md (Sections A.5, C.1, C.2)
with the independent implementation indep_ls.py.

  python3 run_indep_ls.py oracle  "4 8 16 32" 1e-6   # c = 0, lam = 0, x0 = 0 (as in the note)
  python3 run_indep_ls.py scaling "4 8 16"    1e-4   # c = 0, LS with restarts, x0 = 0.5*ones
  python3 run_indep_ls.py random  "8"         1e-4   # c ~ U(-0.2,0.2)^n, seeds 0,1: LS and oracle slopes
  python3 run_indep_ls.py badslope "16"       1e-4   # c = 0, fixed wrong slopes lam_t = 0.3 (-1)^t
"""
import sys
import time
import numpy as np
import indep_ls as R


def show(tag, n, eps, res, recs, secs):
    last = res.get("p")
    rs = [r for r in recs if r["p"] == last]
    for r in rs:
        s = ("  i=%2d leaves=%8d cells=%6d pairs=%8d lr=% .4e UBD=% .4e live_mean=%7.1f live_max=%5d viol=%d"
             % (r["i"], r["leaves"], r["cells"], r["npairs"], r["lr"], r["UBD"], r["live_mean"],
                r["live_max"], r["viol"]))
        if "dx2_s" in r:
            s += " dx2/s=%.2f dxinf/s=%.2f nu=%.2e" % (r["dx2_s"], r["dxinf_s"], r["nu"])
        if "gap" in r:
            s += " gap=%.2e" % r["gap"]
        s += " mmchk=%.1e conf=%.1e" % (r["mmcheck"], r["conf_err"])
        print(s)
    lv = [r["live_mean"] for r in rs if r["live_mean"] > 0]
    print("SUMMARY %s n=%d eps=%.0e done=%s pass=%s level=%s size=%s leaves=%s cells=%s pairs=%s processed=%d "
          "lr=%.4e UBD=%.4e max_live_mean=%.1f (per n %.1f) viol_total=%d time=%.1fs" % (
              tag, n, eps, res["done"], res.get("p"), res.get("i"), res.get("size"), res.get("leaves"),
              res.get("cells"), res.get("npairs"), res["processed"], res.get("lr", np.nan), res.get("UBD", np.nan),
              max(lv) if lv else 0, (max(lv) if lv else 0) / n, sum(r["viol"] for r in recs), secs), flush=True)


def main():
    mode, ns, eps = sys.argv[1], [int(v) for v in sys.argv[2].split()], float(sys.argv[3])
    for n in ns:
        if mode in ("oracle", "scaling", "badslope"):
            c = np.zeros(n)
            t0 = time.time()
            if mode == "oracle":
                res, recs = R.ls(n, c, eps, np.zeros(n), pmax=30, fixed_lam=np.zeros(n), xstar=np.zeros(n), fstar=0.0)
            elif mode == "scaling":
                res, recs = R.ls(n, c, eps, np.full(n, 0.5), pmax=30, xstar=np.zeros(n), fstar=0.0)
            else:
                lam = 0.3 * (-1.0) ** np.arange(n)
                lam[0] = lam[n - 1] = 0.0
                res, recs = R.ls(n, c, eps, np.full(n, 0.5), pmax=11, fixed_lam=lam, xstar=np.zeros(n), fstar=0.0)
            show(mode, n, eps, res, recs, time.time() - t0)
        else:
            for seed in (0, 1):
                c = np.random.default_rng(seed).uniform(-0.2, 0.2, n)
                xs, fs, gres = R.global_min_indep(n, c)
                ls_ = R.slopes(xs, c)
                print("seed %d: f* = %.10f (grad %.1e), |x*|_inf = %.3f, lam* in [%.3f, %.3f]" % (
                    seed, fs, gres, np.abs(xs).max(), ls_[1:n - 1].min(), ls_[1:n - 1].max()), flush=True)
                for tag, kw in (("LS", dict(x0=np.zeros(n))), ("oracle", dict(x0=xs.copy(), fixed_lam=ls_)),
                                ("oracleslopes-x0=0", dict(x0=np.zeros(n), fixed_lam=ls_))):
                    t0 = time.time()
                    res, recs = R.ls(n, c, eps, kw["x0"], pmax=30, fixed_lam=kw.get("fixed_lam"), xstar=xs, fstar=fs)
                    show("%s-seed%d" % (tag, seed), n, eps, res, recs, time.time() - t0)


if __name__ == "__main__":
    main()
