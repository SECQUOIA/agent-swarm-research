"""Confirmation check: one LS pass with the exact slopes lam(x*) but x0 = 0 (column E of the
slope/incumbent table in Section C.2 of extension-adaptive.md), n = 16, eps = 1e-4, seeds 0, 1."""
import os
import sys
import numpy as np
AD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "theory-decomposition", "adaptive")
sys.path.insert(0, AD)
from ls_lib import run_ls, global_min, slopes  # noqa: E402

n, eps = 16, 1e-4
for seed in (0, 1):
    c = np.random.default_rng(seed).uniform(-0.2, 0.2, n)
    xs, fs, _ = global_min(n, 0.8, 0.1, c)
    r, _ = run_ls(n, 0.8, 0.1, c, eps, np.zeros(n), pmax=30, fixed_lam=slopes(xs, 0.8, 0.1, c))
    print("seed %d: exact slopes, x0 = 0: size=%d level=%d processed=%d" % (seed, r["size"], r["i"], r["total_boxes"]), flush=True)
