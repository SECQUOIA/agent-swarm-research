"""Revision check for Sections A.5 / C.3 of extension-adaptive.md: sensitivity of algorithm RC
(rc_lib.py) to tiny changes of the centre (issue raised in the review).

  python3 check_rc_sensitivity.py [N] [SEED]      # default N = 16, SEED = 0, c ~ U(-0.2,0.2)^N

Round 0 of RC from x0 = 0 gives a consistent point x1. Round 1 builds shell partitions around x1
(h = 1, theta = 1/16) with slopes lam(x1). For each coordinate i, move x1_i by 1e-9 towards 0, and
move x1_6 by several amounts; recompute the round-1 root bound l_r and the number of (leaf, cell)
pairs. This is done twice: with the closed intersection test on rounded edges (tol = 0, as in the
original RC runs) and with the test widened by 1e-12 (tol = PAIR_TOL, which keeps the pairs that
touch in exact arithmetic).
"""
import sys
import numpy as np
from ls_lib import dp, slopes, global_min, F
from rc_lib import shell_partition, PAIR_TOL

B, KAPPA, MU = 0.8, 0.1, 4


def round_lr(n, c, xhat, h, tol):
    P = shell_partition(n, xhat, h, MU)
    R = dp(P, slopes(xhat, B, KAPPA, c), B, KAPPA, c, tol=tol)
    return R["lr"], R["npairs"]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    c = np.random.default_rng(seed).uniform(-0.2, 0.2, n)
    xs, fs, _ = global_min(n, B, KAPPA, c)
    P0 = shell_partition(n, np.zeros(n), 2.0, MU)
    R0 = dp(P0, slopes(np.zeros(n), B, KAPPA, c), B, KAPPA, c)
    x1 = R0["x"]
    print("n=%d seed=%d f*=%.6f; round 0: l_r=%.6f F(x1)=%.6f" % (n, seed, fs, R0["lr"], F(x1, B, KAPPA, c)))
    print("x1 = " + " ".join("%.4f" % v for v in x1))
    for tol in (0.0, PAIR_TOL):
        base, bp = round_lr(n, c, x1, 1.0, tol)
        print("tol=%.0e: round 1 at x1: l_r=%.6f pairs=%d" % (tol, base, bp))
        lrs = []
        for i in range(n):
            xp = x1.copy()
            xp[i] -= 1e-9 * np.sign(xp[i])
            lr, npairs = round_lr(n, c, xp, 1.0, tol)
            lrs.append(lr)
            print("   move x1_%-2d (=% .4f) by 1e-9 towards 0: l_r=%.6f pairs=%d change=% .2e" % (
                i, x1[i], lr, npairs, lr - base))
        for d in (1e-12, 1e-10, 1e-8, 1e-6, 1e-4, -1e-4, 1e-3):
            xp = x1.copy()
            xp[6] += d
            lr, npairs = round_lr(n, c, xp, 1.0, tol)
            print("   move x1_6 by %+.0e: l_r=%.6f pairs=%d change=% .2e" % (d, lr, npairs, lr - base))
        on_bd = np.abs(np.abs(x1) - 1) < 1e-12
        ch = np.abs(np.array(lrs) - base)
        print("   tol=%.0e: %d coordinates at +-1; largest |change| of l_r under 1e-9 moves: %.2e at +-1, "
              "%.2e at interior coordinates" % (tol, on_bd.sum(), ch[on_bd].max(), ch[~on_bd].max()))


if __name__ == "__main__":
    main()
