"""Sup-norm localization of the minimizing configuration on the path family (c = 0), by level,
at full precision (the logs of run_ls.py print three digits). Added after the second
confirmation review (item N1).

  python3 check_localization.py NMAX_ORACLE NMAX_SCALING

Reruns the exact-slope runs of logs/oracle_eps1e-6.log (n = 4..NMAX_ORACLE, eps = 1e-6) and
the final passes of the LS runs of logs/scaling_eps1e-4.log (n = 4..NMAX_SCALING, eps = 1e-4).
Per run it prints the size (to compare with the logs), then per sublevel i of the final pass:
|x^cons - x*|_inf / s_i with s_i = 2^{1-i}, and the smallest and largest level of the leaves of
the minimizing configuration ('*' marks the stopping sublevel).
"""
import sys
import time
import numpy as np
from ls_lib import run_ls

B, KAPPA = 0.8, 0.1


def show(tag, n, eps, x0, fixed_lam):
    t0 = time.time()
    res, recs = run_ls(n, B, KAPPA, np.zeros(n), eps, x0, pmax=30, xstar=np.zeros(n),
                       fstar=0.0, fixed_lam=fixed_lam)
    last = res.get("p")
    rows = [r for r in recs if r["p"] == last]
    print("%s n=%d eps=%.0e stop pass=%s level=%s size=%s (%.1fs)" % (
        tag, n, eps, last, res.get("i"), res.get("size"), time.time() - t0))
    for r in rows:
        i = r["i"]
        print("  i=%2d  dxinf/s_i=%9.6f  config leaf levels %2d-%2d%s" % (
            i, r["dxinf"] / (2.0 * 2.0 ** (-i)), min(r["conf_lev"]), max(r["conf_lev"]),
            "  *" if i == res.get("i") else ""))
    sys.stdout.flush()


def main():
    nmax_oracle, nmax_scaling = int(sys.argv[1]), int(sys.argv[2])
    n = 4
    while n <= nmax_oracle:
        show("oracle", n, 1e-6, np.zeros(n), np.zeros(n))
        n *= 2
    n = 4
    while n <= nmax_scaling:
        show("scaling", n, 1e-4, np.full(n, 0.5), None)
        n *= 2


if __name__ == "__main__":
    main()
