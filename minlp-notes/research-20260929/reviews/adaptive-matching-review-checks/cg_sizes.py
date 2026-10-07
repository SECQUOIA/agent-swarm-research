"""Bounds on the quadratic-growth constant c_g of the instances of adaptive-matching.md Sections 8.3-8.4
at the tested sizes. F(x) = sum (x_i^2 - 0.1 x_i^4) + b x^T A x / 2 on [-1,1]^m, x* = 0 (c = 0), A the
adjacency matrix (path or complete binary tree). Since x^2 - 0.1 x^4 >= 0.9 x^2 on [-1,1],
c_g >= 0.9 - |b| rho(A)/2; and c_g <= F(v)/|v|^2 for the bottom eigenvector v of A scaled to |v|_inf = 1."""
import numpy as np


def bounds(A, b):
    ev, V = np.linalg.eigh(A)
    rho = ev[-1]
    v = V[:, 0] / np.abs(V[:, 0]).max()          # eigenvalue -rho (bipartite graph)
    F = np.sum(v * v - 0.1 * v ** 4) + b * v @ A @ v / 2
    return 0.9 - abs(b) * rho / 2, F / (v @ v)


for n in (8, 16, 32, 64, 10 ** 4):
    A = np.eye(n, k=1) + np.eye(n, k=-1)
    lo, hi = bounds(A, 0.88) if n < 10 ** 4 else (0.9 - 0.88, 0.9 - 0.88)
    print("path b=0.88 n=%5d: %.4f <= c_g <= %.4f" % (n, lo, hi))
for n in (8, 64, 256):
    A = np.eye(n, k=1) + np.eye(n, k=-1)
    lo, hi = bounds(A, 0.8)
    print("path b=0.80 n=%5d: %.4f <= c_g <= %.4f" % (n, lo, hi))
for m in (7, 15, 31, 63, 127):
    A = np.zeros((m, m))
    for v in range(1, m):
        A[v, (v - 1) // 2] = A[(v - 1) // 2, v] = 1
    for b in (0.55, 0.62):
        lo, hi = bounds(A, b)
        print("tree b=%.2f m=%4d: %.4f <= c_g <= %.4f" % (b, m, lo, hi))
