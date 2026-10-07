"""Size-dependent conditioning of the test families of adaptive-matching.md, Sections 8.3-8.4
(revision after review).

  python3 cg_by_size.py

Families with c = 0 (x* = 0, f* = 0): F(x) = sum_v (x_v^2 - 0.1 x_v^4) + b sum_{edges} x_u x_v on
[-1,1]^m, for the path graph on n vertices and the complete binary tree on m vertices.
  lower bound on c_g:  0.9 - |b| rho(A)/2   (x^2 - 0.1 x^4 >= 0.9 x^2 on [-1,1]; rho = spectral radius
                                             of the adjacency matrix A);
  local constant:      1 - |b| rho(A)/2     (half the smallest Hessian eigenvalue at x* = 0; an upper
                                             bound on c_g);
  upper bound on c_g:  min of F(x)/|x|^2 over a few feasible points (the bottom eigenvector scaled to
                       sup norm 1, then L-BFGS-B on the ratio from there); any feasible point gives a
                       valid upper bound.
Families with random c (b = 0.55 trees, seed 0; b = 0.8 paths, seeds 0, 1): half the smallest
eigenvalue of the Hessian at the computed x* (an upper bound on c_g when x* is interior).
Also prints the couplings b that hold 0.9 - |b| rho(A)/2 fixed across sizes (used by run_fixed_cg.py).
Double precision throughout.
"""
import os
import sys
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def adj_path(n):
    A = np.zeros((n, n))
    i = np.arange(n - 1)
    A[i, i + 1] = A[i + 1, i] = 1
    return A


def adj_tree(m):
    A = np.zeros((m, m))
    v = np.arange(1, m)
    p = (v - 1) // 2
    A[p, v] = A[v, p] = 1
    return A


def F0(x, A, b):
    return float(np.sum(x * x - 0.1 * x ** 4) + 0.5 * b * x @ A @ x)


def cg_bounds(A, b):
    ev, V = np.linalg.eigh(A)
    rho = ev[-1]
    lo = 0.9 - abs(b) * rho / 2
    loc = 1 - abs(b) * rho / 2
    v = V[:, 0] if b > 0 else V[:, -1]          # minimizes b x^T A x / 2
    x0 = v / np.abs(v).max()
    best = F0(x0, A, b) / (x0 @ x0)

    def ratio(x):
        return F0(x, A, b) / (x @ x)
    r = minimize(ratio, x0, bounds=[(-1, 1)] * len(x0), method="L-BFGS-B")
    if np.linalg.norm(r.x) > 1e-3:
        best = min(best, ratio(r.x))
    return rho, lo, loc, best


def main():
    print("c = 0 families: c_g in [lower, upper]; local = half the smallest Hessian eigenvalue at 0")
    rows = [("path", b, n, adj_path(n)) for b in (0.8,) for n in (8, 64, 256)]
    rows += [("path", 0.88, n, adj_path(n)) for n in (8, 16, 32, 64)]
    rows += [("tree", b, m, adj_tree(m)) for b in (0.55, 0.62) for m in (7, 15, 31, 63, 127)]
    # instances of run_fixed_cg.py (0.9 - b rho/2 held fixed)
    rows += [("path", b, n, adj_path(n)) for n, b in ((16, 0.841253), (32, 0.830691), (64, 0.827896),
                                                      (8, 0.920531))]
    rows += [("tree", b, m, adj_tree(m)) for m, b in ((7, 0.759342), (15, 0.663689), (63, 0.595954))]
    for fam, b, n, A in rows:
        rho, lo, loc, up = cg_bounds(A, b)
        print("  %s b=%.4f size=%3d  rho(A)=%.4f  c_g in [%.4f, %.4f]  local=%.4f" % (fam, b, n, rho, lo, up, loc))

    print("random c: half the smallest Hessian eigenvalue at the computed x*")
    import tree_gr as TG
    for m in (7, 15, 31, 63, 127):
        c = np.random.default_rng(0).uniform(-0.2, 0.2, m)
        xs, fs = TG.global_min_tree(m, 0.55, 0.1, c)
        H = np.diag(2 - 1.2 * xs ** 2) + 0.55 * adj_tree(m)
        print("  tree b=0.55 seed 0 m=%3d  |x*|_inf=%.3f  lambda_min(H)/2=%.4f" % (
            m, np.abs(xs).max(), np.linalg.eigvalsh(H)[0] / 2))
    from dp_certificate import global_min
    for n in (8, 16, 32):
        for seed in (0, 1):
            c = np.random.default_rng(seed).uniform(-0.2, 0.2, n)
            xs, fs, _ = global_min(n, 0.8, 0.1, c)
            H = np.diag(2 - 1.2 * xs ** 2) + 0.8 * adj_path(n)
            print("  path b=0.80 seed %d n=%3d  |x*|_inf=%.3f  lambda_min(H)/2=%.4f" % (
                seed, n, np.abs(xs).max(), np.linalg.eigvalsh(H)[0] / 2))

    print("couplings b with 0.9 - b rho(A)/2 = target (fixed conditioning across sizes)")
    for fam, target, sizes in (("path", 0.9 - 0.88 * np.cos(np.pi / 9), (8, 16, 32, 64)),
                               ("path", 0.9 - 0.88 * np.cos(np.pi / 17), (8, 16, 32)),
                               ("tree", None, (7, 15, 31, 63))):
        if fam == "tree":
            target = 0.9 - 0.62 * np.linalg.eigvalsh(adj_tree(31))[-1] / 2
        for n in sizes:
            A = adj_path(n) if fam == "path" else adj_tree(n)
            rho = np.linalg.eigvalsh(A)[-1]
            print("  %s target %.4f size=%3d  b=%.6f" % (fam, target, n, 2 * (0.9 - target) / rho))


if __name__ == "__main__":
    main()
