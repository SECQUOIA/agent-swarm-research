"""Exact minimal grid-guillotine certificates for n = 2, kappa = 0, c = 0 (f* = 0), termwise McCormick.

Grid {0, +-2^-k : 0 <= k <= K} per coordinate.  N(B) = 1 if LB(B) >= -eps, else min over grid splits of
N(B1) + N(B2).  LB(B) = min_B [x^2 + y^2 + b max(P, Q)] computed by enumerating all 27 faces
(x state, y state, edge state) in exact rational arithmetic (exact_bb.enum_lb).  Reports the optimum with the non-strict rule (LB >= -eps, the note's definition) and with the strict rule
(LB > -eps), the number of grid boxes with LB exactly -eps, and the number in [-eps - 1e-12, -eps).

Usage: python3 grid_dp_exact.py K k_eps      (eps = 10^-k_eps)
"""
import sys
import time
from fractions import Fraction as Fr
from functools import lru_cache

import exact_bb as E


def main():
    K, ke = int(sys.argv[1]), int(sys.argv[2])
    eps = Fr(1, 10 ** ke)
    pts = sorted({Fr(0)} | {s * Fr(1, 2 ** k) for k in range(K + 1) for s in (-1, 1)})
    G = len(pts)
    t0 = time.time()
    lbs = {}

    def lb(box):
        if box not in lbs:
            l = [pts[a] for a, _ in box]
            u = [pts[c] for _, c in box]
            lbs[box] = E.enum_lb(l, u)[0]
        return lbs[box]

    res = {}
    for strict in (False, True):
        @lru_cache(maxsize=None)
        def N(box):
            v = lb(box)
            if (v > -eps) if strict else (v >= -eps):
                return 1, None
            best, arg = 10 ** 9, None
            for i, (a, c) in enumerate(box):
                for m in range(a + 1, c):
                    b1 = box[:i] + ((a, m),) + box[i + 1:]
                    b2 = box[:i] + ((m, c),) + box[i + 1:]
                    v2 = N(b1)[0] + N(b2)[0]
                    if v2 < best:
                        best, arg = v2, (i, m)
            return best, arg
        root = ((0, G - 1), (0, G - 1))
        val = N(root)[0]
        leaves = []

        def collect(box):
            v, arg = N(box)
            if arg is None:
                leaves.append(box)
                return
            i, m = arg
            a, c = box[i]
            collect(box[:i] + ((a, m),) + box[i + 1:])
            collect(box[:i] + ((m, c),) + box[i + 1:])
        collect(root)
        res[strict] = (val, leaves)
    ties = [bx for bx, v in lbs.items() if v == -eps]
    band = [bx for bx, v in lbs.items() if -eps - Fr(1, 10 ** 12) <= v < -eps]
    print(f"EXACT grid DP n=2 K={K} eps=1e-{ke}: optimum (LB >= -eps) = {res[False][0]}, "
          f"optimum (LB > -eps) = {res[True][0]}; grid boxes evaluated = {len(lbs)}, with LB == -eps exactly: "
          f"{len(ties)}; in the note's tie band [-eps-1e-12, -eps): {len(band)}; t={time.time() - t0:.0f}s", flush=True)
    for bx in sorted(res[False][1]):
        print("   leaf", [(str(pts[a]), str(pts[c])) for a, c in bx], "LB =", lbs[bx])
    for bx in ties[:6]:
        print("   tie box", [(str(pts[a]), str(pts[c])) for a, c in bx])


if __name__ == "__main__":
    main()
