"""Check for Section A.5 of extension-adaptive.md (added after the confirmation review): the RC run
at n = 8, c = 0, eps = 1e-6 (as in `run_rc.py zero 8 1e-6`, widened intersection test). The loop
repeats rc_lib.run_rc step by step so that the centres can be printed.

  python3 check_rc_cycle.py [JMAX]      # default JMAX = 19

Per round j: f* - l_r, UBD, the centre error |xhat_j - x*|_inf (absolute and in units of h_j), and
|xhat_j - xhat_{j-2}|_inf (zero when the centres repeat with period 2).
"""
import sys
import numpy as np
from ls_lib import dp, slopes, F
from rc_lib import shell_partition, PAIR_TOL

B, KAPPA, MU, N, EPS = 0.8, 0.1, 4, 8, 1e-6


def main():
    jmax = int(sys.argv[1]) if len(sys.argv) > 1 else 19
    c = np.zeros(N)
    x0 = np.full(N, 0.5)
    UBD = F(x0, B, KAPPA, c)
    xhat = x0.copy()
    centres = []
    for j in range(jmax + 1):
        h = 2.0 * 2.0 ** -j
        P = shell_partition(N, xhat, h, MU)
        R = dp(P, slopes(xhat, B, KAPPA, c), B, KAPPA, c, tol=PAIR_TOL)
        UBD = min(UBD, F(R["x"], B, KAPPA, c))
        centres.append(xhat.copy())
        err = float(np.abs(xhat).max())
        rep = float(np.abs(xhat - centres[j - 2]).max()) if j >= 2 else float("nan")
        print("j=%2d gap=%.4e UBD=%.4e centre err=%.4e (%.2f h) |xhat_j - xhat_{j-2}|_inf=%.3e" % (
            j, -R["lr"], UBD, err, err / h, rep), flush=True)
        if R["lr"] >= UBD - EPS:
            print("stopped at round %d" % j)
            return
        xhat = R["x"]
    print("centres of the last two rounds:")
    for x in centres[-2:]:
        print("  " + " ".join("% .6e" % v for v in x))


if __name__ == "__main__":
    main()
