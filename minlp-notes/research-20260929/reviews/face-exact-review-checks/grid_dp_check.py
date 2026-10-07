"""Referee: rerun of theory-face-exact/grid_dp.py (kappa = 0, c = 0, termwise McCormick) with the independent
Clarabel bound (adversarial_boxes.Inst.LB) instead of bb_path.relax, to see whether HiGHS bound errors
changed the grid-optimal certificate sizes.  Same grid, same recursion.
Usage: python3 grid_dp_check.py n K eps
"""
import sys
import time
from functools import lru_cache
import numpy as np
from adversarial_boxes import Inst

n, K, eps = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
I = Inst(n, [0.8] * (n - 1), 0.0, np.zeros(n), eps, 1.0, "grid")
pts = sorted({0.0} | {s * 2.0 ** -k for k in range(K + 1) for s in (-1, 1)})
G = len(pts)
sys.setrecursionlimit(100000)


@lru_cache(maxsize=None)
def valid(box):
    l = np.array([pts[a] for a, _ in box]); u = np.array([pts[b] for _, b in box])
    return I.LB(l, u) >= I.fs - eps


@lru_cache(maxsize=None)
def N(box):
    if valid(box):
        return 1
    best = 10 ** 9
    for i, (a, b) in enumerate(box):
        for c in range(a + 1, b):
            best = min(best, N(box[:i] + ((a, c),) + box[i + 1:]) + N(box[:i] + ((c, b),) + box[i + 1:]))
    return best


t0 = time.time()
print(f"grid DP (independent bound) n={n} K={K} eps={eps:.0e}: min grid-guillotine leaves = {N(tuple((0, G - 1) for _ in range(n)))} "
      f"({time.time() - t0:.1f}s)", flush=True)
