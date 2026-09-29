"""Reviewer's check of Theorem 5.7 on a natural constraint-gap instance.
min |y - c|^2, c = (0.3, 0.1), s.t. |y|^2 >= 1, y in X0 = [-1.2, 1.3]^2.  Objective kept exact (alpha = 0);
the reverse-convex constraint is relaxed by its secant, sum_i ((l_i+u_i) y_i - l_i u_i) >= 1, whose margin is
exactly q_B, so the scheme satisfies the tube hypothesis T_{0,1} and (U^q_1).  z* = c/|c| is a KKT point
with multiplier > 0, LICQ, active stratum = circle (d = 1).  Theorem 5.7 predicts N_opt >= c log(1/eps).
Node bound: exact convex QP via 1-D dual (bisection on the multiplier).  Also checks the tube dichotomy
(D) on all leaves at grid points z with f(z) < f* - eps:  q_C(z) < v(z) = max(0, 1 - |z|^2).
Usage: python3 reverse_convex_tube.py
"""
import math
import numpy as np
C = np.array([0.3, 0.1]); LO, HI = -1.2, 1.3
FSTAR = (1 - np.linalg.norm(C)) ** 2

def lb(l, u):
    b = l + u; r = 1 + np.sum(l * u)
    y = lambda lam: np.clip(C + lam * b / 2, l, u)
    if b @ np.clip(np.where(b > 0, u, l), l, u) < r - 1e-15:   # max of b.y over box < r
        return math.inf
    if b @ y(0.0) >= r:
        return float(np.sum((y(0.0) - C) ** 2))
    lo, hi = 0.0, 1.0
    while b @ y(hi) < r: hi *= 2
    for _ in range(200):
        m = 0.5 * (lo + hi)
        if b @ y(m) < r: lo = m
        else: hi = m
    lam = hi; yy = y(lam)
    return float(np.sum((yy - C) ** 2) - lam * (b @ yy - r))   # dual value, valid lower bound

def run(eps):
    stack, nodes, leaves = [(np.array([LO, LO]), np.array([HI, HI]))], 0, []
    while stack:
        l, u = stack.pop(); nodes += 1
        if lb(l, u) >= FSTAR - eps:
            leaves.append((l, u)); continue
        i = int(np.argmax(u - l)); s = 0.5 * (l[i] + u[i])
        u1 = u.copy(); u1[i] = s; l2 = l.copy(); l2[i] = s
        stack += [(l, u1), (l2, u)]
    viol = 0
    for l, u in leaves:
        g = [np.linspace(l[k], u[k], 7) for k in range(2)]
        X, Y = np.meshgrid(*g, indexing="ij")
        f = (X - C[0]) ** 2 + (Y - C[1]) ** 2
        v = np.maximum(0, 1 - X * X - Y * Y)
        q = (X - l[0]) * (u[0] - X) + (Y - l[1]) * (u[1] - Y)
        viol += int(np.sum((f < FSTAR - eps) & ~(q < v + 1e-14)))
    return nodes, viol

prev = None
for k in range(1, 10):
    eps = 10.0 ** -k
    n, viol = run(eps)
    print(f"eps={eps:.0e} nodes={n:6d}" + ("" if prev is None else f"  (+{n - prev} per decade)") + f"  (D)-violations on leaves: {viol}")
    prev = n
