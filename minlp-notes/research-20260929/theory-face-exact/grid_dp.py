"""Minimal guillotine certificates with split points restricted to a grid (n = 2, 3).

For the instance kappa = 0, c = 0 (x* = 0, f* = 0) with the exact termwise McCormick relaxation, compute
    N_grid(B) = 1 if LB(B) >= -eps, else min over grid splits of N_grid(B1) + N_grid(B2)
over all boxes with corners on the grid {0, +-2^-k (k = 0..K)} per coordinate.  N_grid(root) is an upper
bound on N_opt(eps) (it restricts the split points); it is the exact optimum over grid-guillotine trees.
Validity is decided with the certified lower bound of bb_path.certified (revision after review).
Usage: python3 grid_dp.py n K eps [kappa rel]
"""
import sys
import time
from functools import lru_cache
import numpy as np
from bb_path import Inst, relax, certified, STATS, TIE


def main():
    n, K, eps = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    kappa = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
    rel = sys.argv[5] if len(sys.argv) > 5 else "mc"
    I = Inst(n, kappa, "zero")
    pts = sorted({0.0} | {s * 2.0 ** -k for k in range(K + 1) for s in (-1, 1)})
    G = len(pts)
    nsolve = [0]

    @lru_cache(maxsize=None)
    def valid(box):
        l = np.array([pts[a] for a, _ in box])
        u = np.array([pts[b] for _, b in box])
        nsolve[0] += 1
        thr = I.fstar - eps - TIE
        xh = relax(I, rel, l, u)[1]
        return certified(I, rel, l, u, thr, xh)[0] >= thr      # certified bound (revision after review)

    sys.setrecursionlimit(100000)

    @lru_cache(maxsize=None)
    def N(box):
        if valid(box):
            return 1, None
        best, arg = 10 ** 9, None
        for i, (a, b) in enumerate(box):
            for c in range(a + 1, b):
                b1 = box[:i] + ((a, c),) + box[i + 1:]
                b2 = box[:i] + ((c, b),) + box[i + 1:]
                v = N(b1)[0] + N(b2)[0]
                if v < best:
                    best, arg = v, (i, c)
        return best, arg

    t0 = time.time()
    root = tuple((0, G - 1) for _ in range(n))
    val = N(root)[0]
    # recover leaves of one optimal tree
    leaves = []

    def collect(box):
        v, arg = N(box)
        if arg is None:
            leaves.append(box)
            return
        i, c = arg
        a, b = box[i]
        collect(box[:i] + ((a, c),) + box[i + 1:])
        collect(box[:i] + ((c, b),) + box[i + 1:])

    collect(root)
    print(f"grid DP n={n} K={K} grid points={G} eps={eps:.0e} kappa={kappa} rel={rel}: "
          f"min grid-guillotine leaves = {val} ({nsolve[0]} relaxations, {time.time()-t0:.1f}s; "
          f"refined {STATS['refined']})")
    if n == 2:
        for bx in sorted(leaves):
            print("   leaf", [(pts[a], pts[b]) for a, b in bx])


if __name__ == "__main__":
    main()
