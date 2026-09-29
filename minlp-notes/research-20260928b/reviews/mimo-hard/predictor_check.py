"""Checks of the exact-law tree predictor of Section 7.3 (heuristic model).

Part A  node-level accuracy: for random static-order nodes (depth d, wrong set
        Wr) of real instances, compare the true box-relaxation value with the
        predictor pb = f(x^Wr)(1 - (N-d)/(2M)); report the error in units of
        the cost of one wrong fixing, 4 rho beta.
Part B  predictor on the N = 256, rho = 4 log N instances whose real static
        trees hit the 1e5-node cap (so they are missing from Table 7.3b).
Uses the note's instance generator and node solver (read-only import).
"""
import sys, os
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "bb-complexity",
                                "binary-least-squares", "code"))
import numpy as np
from core import instance, node, fval_u
from predict_trees import predicted_static

rng = np.random.default_rng(3)
print("Part A: (true node value - predictor)/(4 rho beta), static-order nodes")
for beta in (1.0, 2.0):
    for N in (200, 400):
        M = int(beta * N); rho = 4 * np.log(N)
        A, y, xs, B, w = instance(N, M, rho, 77 + N)
        W = w @ w
        for d in (N // 8, N // 4, N // 2):
            errs = []; inact = 0
            for rep in range(30):
                j = int(rng.integers(0, 6))
                Wr = rng.choice(d, j, replace=False) if j else np.array([], int)
                fixed = {i: 0.0 for i in range(d)}
                for i in Wr:
                    fixed[int(i)] = 2.0
                val, lb, u, ina = node(B, w, fixed)
                uW = np.zeros(N); uW[Wr] = 2.0
                pb = fval_u(B, w, uW) * (1 - (N - d) / (2.0 * M))
                errs.append((val - pb) / (4 * rho * beta)); inact += ina
            errs = np.array(errs)
            print("  beta=%g N=%d rho=%.1f d=%d: mean %.3f  sd %.3f  min %.3f  max %.3f  (box-inactive %d/30)"
                  % (beta, N, rho, d, errs.mean(), errs.std(), errs.min(), errs.max(), inact), flush=True)

print()
print("Part B: predictor on N = 256, rho = 4 log N (beta = 1), seeds 0-3 (real static trees capped at 1e5)")
for seed in range(4):
    N = 256; rho = 4 * np.log(N)
    A, y, xs, B, w = instance(N, N, rho, seed)
    pc, ok = predicted_static(B, w, cap=5 * 10 ** 6)
    print("  seed %d: predicted static nodes %s%d" % (seed, "" if ok else ">", pc), flush=True)
