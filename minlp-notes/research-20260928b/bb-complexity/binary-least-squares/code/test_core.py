"""Targeted checks of core.py: node values against the scout's BVLS solver,
B&B optimum against brute force, SDP bound sanity."""
import sys, itertools
import numpy as np
sys.path.insert(0, "../../../scouting/bb-tree-size-convex")
import bls  # scout code
from core import instance, node, bnb, fval_u, sdp_value, sdp_certificate_eig

rng = np.random.default_rng(7)
maxdiff = 0.0; maxgap = 0.0
for t in range(40):
    N = int(rng.integers(6, 30)); M = N if t % 2 == 0 else 2 * N
    rho = float(rng.choice([1.0, 4.0, 2 * np.log(N), 0.3 * N]))
    A, y, xs, B, w = instance(N, M, rho, int(rng.integers(1e6)))
    k = int(rng.integers(0, N // 2))
    idx = rng.choice(N, k, replace=False)
    fixed_u = {int(i): float(rng.choice([0.0, 2.0])) for i in idx}
    fixed_x = {i: xs[i] * (1.0 - u) for i, u in fixed_u.items()}
    val, lb, u, ina = node(B, w, fixed_u)
    v2, _ = bls.relax(A, y, fixed_x)
    maxdiff = max(maxdiff, abs(val - v2) / max(1.0, abs(v2)))
    maxgap = max(maxgap, (val - lb) / max(1.0, abs(val)))
    assert lb <= val + 1e-9 * max(1, abs(val))
print("node vs scout BVLS: max rel diff", maxdiff, " max (val-lb)/val", maxgap)

bad = 0
for t in range(12):
    N = 10; M = N if t % 2 else 2 * N
    rho = [1.0, 3.0, 8.0][t % 3]
    A, y, xs, B, w = instance(N, M, rho, 100 + t)
    best = min(fval_u(B, w, 2.0 * np.array(bits, float)) for bits in itertools.product([0, 1], repeat=N))
    for rule in ("maxfrac", "static"):
        r = bnb(B, w, rule=rule)
        if abs(r["OPT"] - best) > 1e-8 * best:
            bad += 1
print("B&B optimum vs brute force (N=10, 24 runs): mismatches", bad)

for t in range(3):
    N = 12
    A, y, xs, B, w = instance(N, N, 6.0, 300 + t)
    sv, slb = sdp_value(A, y)
    best = min(fval_u(B, w, 2.0 * np.array(bits, float)) for bits in itertools.product([0, 1], repeat=N))
    print("SDP value %.6f  certified lb %.6f  OPT %.6f  eig-cert %.4f" % (sv, slb, best, sdp_certificate_eig(A, xs, w)))

# active-set upper bounds versus BVLS on problems where u <= 2 binds
from scipy.optimize import lsq_linear
from core import box_min
maxd = 0.0; nact = 0
for t in range(200):
    N = int(rng.integers(10, 80)); M = N
    A, y, xs, B, w = instance(N, M, float(rng.choice([0.2, 0.5, 1.0, 2.0])), 5000 + t)
    v = w + 2 * B[:, :3].sum(axis=1)       # a node with 3 wrong fixings
    Bf = B[:, 3:]
    val, lb, u, ina = box_min(Bf, v)
    r = lsq_linear(Bf, -v, bounds=(0, 2), method="bvls", tol=1e-13)
    vb = float(np.sum((v + Bf @ np.clip(r.x, 0, 2)) ** 2))
    maxd = max(maxd, abs(val - vb) / vb); nact += (not ina)
print("active-set box solver vs BVLS: %d/200 with active upper bounds, max rel diff %.2e" % (nact, maxd))

# knapsack predictor (log-domain DP) versus brute-force enumeration
import itertools, math
from knapsack_predictor import log_tree
bad = 0
for t in range(6):
    N = 12; rho = float([4.0, 6.0, 9.0][t % 3])
    lt, dm = log_tree(N, 1.0, rho, np.random.default_rng(40 + t), bins_per_min=2000)
    if lt is None:
        continue
    r2 = np.random.default_rng(40 + t)
    W = r2.chisquare(N); g = r2.standard_normal(N); chi = r2.chisquare(N - 1, N)
    delta = 4 * (np.sqrt(rho / N) * np.sqrt(W) * g + (rho / N) * (g ** 2 + chi))
    L = W * (N - np.arange(N + 1)) / (N + np.arange(N + 1))
    tot = 1 + sum(2 * sum(1 for bits in itertools.product([0, 1], repeat=d) if np.dot(bits, delta[:d]) < L[d]) for d in range(N))
    bad += abs(math.exp(lt) - tot) > 0.5
print("knapsack DP vs brute force (N = 12, 6 instances): mismatches", bad)
