"""Exact rational objective of the DP-policy controls (double values, taken exactly), with the
exact OSIL constants; the states are the exact solution of the linear rows, so the point is
exactly feasible. Also compares with the authors' best controls.  usage: policy_exact.py N u.npy"""
import sys
import time
from fractions import Fraction as Fr

import numpy as np

import v_catmix_model as vm

N, path = int(sys.argv[1]), sys.argv[2]
m, K, strs = vm.load(N)
u = np.load(path)
assert u.shape == (N + 1,) and np.all((u >= 0) & (u <= 1))
t0 = time.time()
xs = vm.simulate_exact(K, [Fr(float(v)) for v in u])
J = xs[-1][0] + xs[-1][1] - 1
assert all(a >= 0 and b >= 0 for a, b in xs)
print("N=%d %s: exact J = %.20g  (%.0fs); free controls: %d, at 0: %d, at 1: %d" % (
    N, path, float(J), time.time() - t0, int(np.sum((u > 0) & (u < 1))), int(np.sum(u == 0)), int(np.sum(u == 1))),
    flush=True)
# 30 more digits than float(J) shows, via integer division
s = J.numerator * 10 ** 30 // J.denominator
print("  J * 1e30 (floor) =", s, flush=True)
