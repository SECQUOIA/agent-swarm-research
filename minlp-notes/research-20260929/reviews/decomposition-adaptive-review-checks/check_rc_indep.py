"""Reviewer re-run of the re-centering heuristic RC (Section A.5 of extension-adaptive.md) with the
reviewer's DP (indep_ls.dp) and the shell partition of [D] (dp_certificate.shells, reviewed earlier).

Round j: h_j = 2^{1-j}, theta = 1/16, leaves Pi(xhat_{V_t}; h_j, theta), cells Pi(xhat_t; h_j, theta),
slopes lam(xhat_j), DP; next centre = consistent point of the minimizing configuration.
Also reports the stop test that an exact incumbent (UBD = f*) would give: gap = f* - l_r <= eps.

  python3 check_rc_indep.py zero 8 1e-6 17
  python3 check_rc_indep.py random 16 1e-4 12      # seed 0
"""
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "theory-decomposition"))
import indep_ls as R  # noqa: E402
from dp_certificate import shells  # noqa: E402


def shell_part(n, xhat, h, mu=4):
    P = R.Part(n)
    for t in range(n - 1):
        L, U = shells(xhat[t:t + 2], h, mu, 2)
        o = np.lexsort((L[:, 1], L[:, 0]))
        L, U = L[o], U[o]
        P.L[t] = dict(l1=L[:, 0].copy(), u1=U[:, 0].copy(), l2=L[:, 1].copy(), u2=U[:, 1].copy(),
                      lev=np.zeros(len(L), int))
        if t >= 1:
            Lc, Uc = shells(xhat[t:t + 1], h, mu, 1)
            o = np.argsort(Lc[:, 0])
            P.C[t] = dict(lo=Lc[o, 0].copy(), hi=Uc[o, 0].copy(), lev=np.zeros(len(Lc), int))
    return P


def main():
    mode, n, eps, jmax = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
    if mode == "zero":
        c = np.zeros(n)
        xs, fs = np.zeros(n), 0.0
        x0 = np.full(n, 0.5)
    else:
        c = np.random.default_rng(0).uniform(-0.2, 0.2, n)
        xs, fs, _ = R.global_min_indep(n, c)
        x0 = np.zeros(n)
    UBD = R.Fval(x0, c)
    xhat = x0.copy()
    for j in range(jmax + 1):
        t0 = time.time()
        h = 2.0 * 2.0 ** (-j)
        lam = R.slopes(xhat, c)
        P = shell_part(n, xhat, h)
        nl, nc = P.counts()
        res = R.dp(P, lam, c)
        UBD = min(UBD, R.Fval(res["x"], c))
        print("j=%2d h=%.2e size=%8d lr=% .4e UBD=% .4e gap=%.3e stop=%s exact-inc-stop=%s "
              "cen_inf/h=%.2f x_inf/h=%.2f [%.1fs]" % (
                  j, h, nl + nc, res["lr"], UBD, fs - res["lr"], res["lr"] >= UBD - eps,
                  fs - res["lr"] <= eps, np.abs(xhat - xs).max() / h, np.abs(res["x"] - xs).max() / h,
                  time.time() - t0), flush=True)
        if res["lr"] >= UBD - eps:
            print("stopped at round %d" % j)
            break
        xhat = res["x"]


if __name__ == "__main__":
    main()
