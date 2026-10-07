"""Experiments for algorithm GR (gr_lib.py) on the path family, adaptive-matching.md Section 5.

  python3 run_gr.py zero   NMIN NMAX EPS THETA R   # c = 0 (x* = 0), x0 = 0.5*ones, n = NMIN, 2 NMIN, ..., NMAX
  python3 run_gr.py random N    EPS THETA R        # c ~ U(-0.2,0.2)^n, seeds 0 and 1, x0 = 0
  python3 run_gr.py theta  N    EPS R              # c = 0, theta = 1/4, 1/8, 1/16, 1/32 (12 stages at most)

b = 0.8, kappa = 0.1 (Theorem 4.1 of the decomposition note). Per stage the log prints the core
width W_j, partition size, root bound l_r, incumbent UBD, zloc = max_t |z^t - x*_{V_t}|_inf / W_j
(copies of the minimizing configuration), xloc / x2 = sup / Euclidean distance of its consistent
point to x* (over W_j), nu_inf = largest slope error, gviol = boxes violating the graded
invariant w <= max(W_j, theta dist_inf(box, x*)), split = leaves split per bag (max, mean),
wide = splits of boxes wider than W_j.
"""
import sys
import time
import numpy as np
from gr_lib import run_gr, global_min

B, KAPPA = 0.8, 0.1


def fmt(r):
    s = "j=%2d W=%.3e leaves=%8d cells=%6d pairs=%8d lr=% .5e UBD=% .5e" % (
        r["j"], r["W"], r["leaves"], r["cells"], r["npairs"], r["lr"], r["UBD"])
    if "zloc" in r:
        s += " zloc=%.3f xloc=%.3f x2=%.2f nu_inf/W=%.2f gviol=%d" % (
            r["zloc"], r["xloc"], r["x2"], r["nu_inf"] / r["W"], r["graded_viol"])
    if "gap" in r:
        s += " gap=%.3e gap/(n-1)W^2=%.3g" % (r["gap"], r["gap"] / (r["n"] - 1) / r["W"] ** 2)
    if "split_leaf_max" in r:
        s += " split=%d/%.1f wide=%d" % (r["split_leaf_max"], r["split_leaf_mean"], r["wide_splits"])
    return s


def run(n, c, eps, x0, theta, R, xs, fs, tag, jmax=40):
    t0 = time.time()

    def log(r):
        r["n"] = n
        print(fmt(r), flush=True)
    res, recs = run_gr(n, B, KAPPA, c, eps, x0, theta, R, jmax=jmax, xstar=xs, fstar=fs, log=log)
    sp = [r["split_leaf_max"] for r in recs if "split_leaf_max" in r]
    print("SUMMARY %s n=%d eps=%.0e theta=1/%d R=%g done=%s stages=%s size=%s leaves=%s cells=%s "
          "created=%d processed=%d size_per_bag=%.0f max_split_per_bag=%d max_zloc=%.3f "
          "max_gviol=%d wide=%d time=%.1fs" % (
              tag, n, eps, round(1 / theta), R, res["done"], res.get("j"), res.get("size"),
              res.get("leaves"), res.get("cells"), res["created"], res["processed"],
              (res.get("size") or 0) / (n - 1), max(sp) if sp else 0,
              max(r["zloc"] for r in recs), max(r["graded_viol"] for r in recs),
              sum(r.get("wide_splits", 0) for r in recs), time.time() - t0), flush=True)
    return res, recs


def main():
    mode = sys.argv[1]
    if mode == "zero":
        nmin, nmax, eps, theta, R = int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), \
            1.0 / float(sys.argv[5]), float(sys.argv[6])
        n = nmin
        while n <= nmax:
            run(n, np.zeros(n), eps, np.full(n, 0.5), theta, R, np.zeros(n), 0.0, "zero")
            n *= 2
    elif mode == "random":
        n, eps, theta, R = int(sys.argv[2]), float(sys.argv[3]), 1.0 / float(sys.argv[4]), float(sys.argv[5])
        for seed in (0, 1):
            c = np.random.default_rng(seed).uniform(-0.2, 0.2, n)
            xs, fs, _ = global_min(n, B, KAPPA, c)
            print("seed %d: f* = %.10f, |x*|_inf = %.3f" % (seed, fs, np.abs(xs).max()), flush=True)
            run(n, c, eps, np.zeros(n), theta, R, xs, fs, "random-seed%d" % seed)
    elif mode == "theta":
        n, eps, R = int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
        for m in (4, 8, 16, 32):
            run(n, np.zeros(n), eps, np.full(n, 0.5), 1.0 / m, R, np.zeros(n), 0.0, "theta", jmax=12)


if __name__ == "__main__":
    main()
