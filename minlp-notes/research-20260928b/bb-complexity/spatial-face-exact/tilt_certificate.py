"""Explicit certificates for tilt(theta) (Proposition 3.6 upper side).

f = 2|U| + U*Y,  U = (x-1/2) + theta (y-1/2),  Y = y - 1/2  on [0,1]^2 (c = 1); optimal set U = 0.
Construction: K horizontal strips of height h = 1/K; in each strip split x once, at the point where
the optimal line crosses mid-height.  2K leaves.  Each leaf is checked with the exact node bound
(HiGHS QP of face_bb.relax); the smallest valid K is found by scanning upward from the lower bound.
Lower bound (Theorem 3.5): any certificate has >= 0.5*sqrt(theta/eps) leaves.
"""
import math
import numpy as np
from face_bb import relax
import instances as I


def valid(P, K, theta, eps):
    h = 1.0 / K
    for k in range(K):
        y0, y1 = k * h, min(1.0, (k + 1) * h)
        xm = 0.5 - theta * (0.5 * (y0 + y1) - 0.5)
        for (l, u) in (([0.0, y0], [xm, y1]), ([xm, y0], [1.0, y1])):
            if relax(P, np.array(l), np.array(u))[0] < -eps:
                return False
    return True


if __name__ == "__main__":
    for theta in (0.3, 0.03, 0.003):
        P = I.tilt(theta)
        for eps in (1e-3, 1e-4, 1e-5, 1e-6):
            lbL = 0.5 * math.sqrt(theta / eps)
            K = max(1, int(lbL / 2))
            while not valid(P, K, theta, eps):
                K = int(K * 1.05) + 1
            # refine downward
            while K > 1 and valid(P, K - 1, theta, eps):
                K -= 1
            print(f"theta={theta:<6} eps={eps:.0e}: certificate leaves 2K = {2 * K:6d}   lower bound = {lbL:8.1f}   "
                  f"ratio = {2 * K / lbL:.2f}   (2K*sqrt(eps/theta) = {2 * K * math.sqrt(eps / theta):.3f})", flush=True)
