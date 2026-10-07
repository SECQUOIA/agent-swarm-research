"""Recheck of Section 9 (chordal split) and of the convexity behind the Frank-Wolfe bounds in bb_path.py.

1. Lemma 9.1: random positive definite tridiagonal H (random signs of b_i): pivots > 0, the 2x2 blocks
   [[p_i, b_i], [b_i, b_i^2/p_i]] plus p_n e_n e_n' sum to H, and each block is PSD with determinant 0.
2. Consequence A: clique-wise PSD relaxation (3x3 blocks [1 x_c'; x_c X_c] >= 0 on each edge, box on x)
   of the convex QP kappa = 0 on random sub-boxes, against the exact QP minimum.
3. Balanced split, kappa = 0.1: the largest centred cube on which every factor is convex, and the smallest
   eigenvalue of an interior factor on [-1,1]^2.
4. Convexity of the relaxations whose Frank-Wolfe bound bb_path uses (abb, kappa = 0; abbU/abbS, kappa = 0.1):
   smallest Hessian eigenvalue at random points of random boxes; and FW bound <= relaxation minimum.
Usage: python3 section9_checks.py
"""
import math
import os
import sys
import warnings

import numpy as np
import cvxpy as cp
from scipy import optimize

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../theory-face-exact"))
import bb_path  # noqa: E402

rng = np.random.default_rng(7)

# 1 ------------------------------------------------------------------------------------------
worst_rec, worst_psd, worst_det, tried = 0.0, 0.0, 0.0, 0
for trial in range(2000):
    n = int(rng.integers(2, 13))
    d = rng.uniform(0.1, 3.0, n)
    bo = rng.uniform(-2, 2, n - 1)
    H = np.diag(d) + np.diag(bo, 1) + np.diag(bo, -1)
    if np.linalg.eigvalsh(H)[0] <= 1e-6:
        continue
    tried += 1
    p = [d[0]]
    for i in range(1, n):
        p.append(d[i] - bo[i - 1] ** 2 / p[-1])
    assert min(p) > 0
    S = np.zeros((n, n))
    for i in range(n - 1):
        Bk = np.array([[p[i], bo[i]], [bo[i], bo[i] ** 2 / p[i]]])
        worst_psd = min(worst_psd, np.linalg.eigvalsh(Bk)[0] / np.abs(Bk).max())
        worst_det = max(worst_det, abs(np.linalg.det(Bk)) / np.abs(Bk).max() ** 2)
        S[i:i + 2, i:i + 2] += Bk
    S[n - 1, n - 1] += p[n - 1]
    worst_rec = max(worst_rec, np.abs(S - H).max())
print(f"1. Lemma 9.1 on {tried} random PD tridiagonal matrices (n = 2..12, mixed signs): pivots all > 0; "
      f"max |sum of blocks - H| = {worst_rec:.1e}; min relative block eigenvalue = {worst_psd:.1e}; "
      f"max relative |det| = {worst_det:.1e}")

# 2 ------------------------------------------------------------------------------------------
worst = 0.0
for trial in range(24):
    n = 4
    c = np.zeros(n) if trial % 2 == 0 else rng.uniform(-0.3, 0.3, n)
    bs = 0.8 * (rng.choice([-1, 1], n - 1) if trial % 3 == 0 else np.ones(n - 1))
    a, bb = np.sort(rng.uniform(-1, 1, (2, n)), axis=0)
    l, u = a, bb
    Hm = 2 * np.eye(n) + np.diag(bs, 1) + np.diag(bs, -1)
    x = cp.Variable(n); Xd = cp.Variable(n); Xo = cp.Variable(n - 1)
    cons = [x >= l, x <= u]
    for i in range(n - 1):
        M = cp.Variable((3, 3), symmetric=True)
        cons += [M >> 0, M[0, 0] == 1, M[0, 1] == x[i], M[0, 2] == x[i + 1], M[1, 1] == Xd[i],
                 M[2, 2] == Xd[i + 1], M[1, 2] == Xo[i]]
    pr = cp.Problem(cp.Minimize(cp.sum(Xd) + bs @ Xo + c @ x), cons)
    pr.solve(solver="CLARABEL")
    xs = cp.Variable(n)
    q = cp.Problem(cp.Minimize(0.5 * cp.quad_form(xs, Hm) + c @ xs), [xs >= l, xs <= u])
    q.solve(solver="CLARABEL")
    worst = max(worst, abs(pr.value - q.value))
print(f"2. Consequence A: clique-PSD bound vs exact QP minimum on 24 random sub-boxes (n = 4, c = 0 or random, "
      f"uniform or mixed signs of b): max |difference| = {worst:.1e}")

# 3 ------------------------------------------------------------------------------------------
kap, b = 0.1, 0.8
g2 = lambda t: 2 - 12 * kap * t * t
lmin = lambda p, q: (p + q) / 2 - math.sqrt(((p - q) / 2) ** 2 + b * b)
# interior factor [[g''(u)/2, b], [b, g''(v)/2]] on the cube |u|,|v| <= t: worst at u = v = t
t_int = optimize.brentq(lambda t: lmin(g2(t) / 2, g2(t) / 2), 0.0, 1.0)
t_end = optimize.brentq(lambda t: lmin(g2(t), g2(t) / 2), 0.0, 1.0)
print(f"3. Balanced split, kappa = 0.1: interior factor convex on the centred cube iff t <= {t_int:.6f} "
      f"(1/sqrt(3) = {1 / math.sqrt(3):.6f}); end factors iff t <= {t_end:.6f}; interior factor at (1, 1): "
      f"lambda_min = {lmin(g2(1) / 2, g2(1) / 2):.3f}; interior factor at (0.775, 0): lambda_min = "
      f"{lmin(g2(0.775) / 2, g2(0) / 2):.4f} (the convex set of a factor is not a cube)")

# 4 ------------------------------------------------------------------------------------------
res = []
for rel, kappa in (("abb", 0.0), ("abbU", 0.1), ("abbS", 0.1)):
    n = 5
    I = bb_path.Inst(n, kappa, "zero")
    worst_eig, worst_fw = math.inf, -math.inf
    for trial in range(300):
        a, c2 = np.sort(rng.uniform(-1, 1, (2, n)), axis=0)
        l, u = a, c2
        if rel == "abb":
            al = bb_path.alpha_abb(b)
            A = np.full(n, 2 * al); A[0] = A[-1] = al
        else:
            sb, ta = bb_path._split_weights(n, rel)
            gmin = 2 - 12 * kappa * np.maximum(l * l, u * u)
            p, q = sb[:-1] * gmin[:-1], ta[1:] * gmin[1:]
            lam = (p + q) / 2 - np.sqrt(((p - q) / 2) ** 2 + b * b)
            alf = np.maximum(0.0, -lam) / 2
            A = np.zeros(n); A[:-1] += alf; A[1:] += alf
        for _ in range(20):
            xx = rng.uniform(l, u)
            Hx = np.diag(2 - 12 * kappa * xx ** 2 + 2 * A) + b * (np.eye(n, k=1) + np.eye(n, k=-1))
            worst_eig = min(worst_eig, np.linalg.eigvalsh(Hx)[0])
        # FW bound from bb_path at a random point vs the minimum of the relaxation (multi-start)
        thr = -1e9
        if rel == "abb":
            lbfw, _ = bb_path.certified(I, "abb", l, u, thr, rng.uniform(l, u))
            Fx = lambda x: float(np.sum(x * x) + b * np.sum(x[:-1] * x[1:]) - np.sum(A * (x - l) * (u - x)))
        else:
            lbfw, _, _ = bb_path.relax_split(I, rel, l, u, thr)
            Fx = lambda x: float(np.sum(x * x - kappa * x ** 4) + b * np.sum(x[:-1] * x[1:])
                                 - np.sum(A * (x - l) * (u - x)))
        mn = min(optimize.minimize(Fx, rng.uniform(l, u), method="L-BFGS-B", bounds=list(zip(l, u)),
                                   options={"ftol": 1e-15, "gtol": 1e-12}).fun for _ in range(4))
        worst_fw = max(worst_fw, lbfw - mn)
    res.append(f"{rel}: min Hessian eigenvalue of the relaxation = {worst_eig:.3f}, max (FW bound - minimum) = "
               f"{worst_fw:.1e}")
print("4. Convexity / Frank-Wolfe validity on 300 random boxes, n = 5: " + "; ".join(res))
