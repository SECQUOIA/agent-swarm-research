"""Checks for the revision after review (face-exact-exponential.md, Section 9).

1. Theorem 2 base: exp(-Psi_J(sigma, mu)) optimised over (sigma, mu) with the n-independent part only.
2. Chordal split of H = 2I + 0.8A (path): Cholesky pivots, and the balanced split 1/2 : 1/2; 2x2 blocks PSD.
   For the PROGRAM family (kappa = 0.1) with the balanced split, the factor Hessians
   [[s g''(u), b], [b, t g''(v)]] are PSD on |u|, |v| <= 0.577 (checked on a grid).
3. Clique-wise PSD relaxation (3x3 blocks [1 x_i x_j; x_i X_ii X_ij; x_j X_ij X_jj] >= 0, as in SCIP's
   minor separator) of the convex QP kappa = 0 on the root box: its bound equals f* (chordal argument).
Usage: python3 chordal_checks.py
"""
import math
import numpy as np
import cvxpy as cp
from scipy import optimize
from bounds import k_env, upper_max

D, b = 2.0, 0.8

# 1
best = (math.inf, None, None)
for sg in np.linspace(0.30, 0.50, 201):
    kf = k_env(D, b, sg)
    r = optimize.minimize_scalar(lambda mu: upper_max(lambda s: kf(s, mu), N=100001), bounds=(0.5, 2.0),
                                 method="bounded", options={"xatol": 1e-7})
    if r.fun < best[0]:
        best = (r.fun, sg, r.x)
psi, sg, mu = best
psi_fine = upper_max(lambda s: k_env(D, b, sg)(s, mu), N=2000001)
print(f"1. Theorem 2: best sigma={sg:.4f}, mu={mu:.4f}, exp(-Psi_J) = {math.exp(-psi_fine):.4f} "
      f"(per-variable base as n -> inf; the note's 1.2021 includes the mu b sigma/n term at n = 200)")

# 2
n = 12
H = 2 * np.eye(n) + b * (np.eye(n, k=1) + np.eye(n, k=-1))
piv = [2.0]
for i in range(1, n):
    piv.append(2.0 - b * b / piv[-1])
print("2. Cholesky pivots of 2I + 0.8A:", np.round(piv, 4), " min eig(H) =", round(np.linalg.eigvalsh(H)[0], 4))
blk = np.array([[1.0, b], [b, 1.0]])
print("   balanced block [[1, .8], [.8, 1]] eigenvalues:", np.linalg.eigvalsh(blk))
kap = 0.1
g2 = lambda t: 2 - 12 * kap * t * t
t = np.linspace(-0.5774, 0.5774, 401)
U, V = np.meshgrid(t, t)
mins = []
for s, tt in ((0.5, 0.5), (1.0, 0.5), (0.5, 1.0)):
    p, q = s * g2(U), tt * g2(V)
    lam = (p + q) / 2 - np.sqrt(((p - q) / 2) ** 2 + b * b)
    mins.append(lam.min())
print(f"   kappa = 0.1, balanced split: min over |u|,|v| <= 0.5774 of lambda_min(factor Hessian) = "
      f"{min(mins):.2e} (interior, first, last factor: {', '.join(f'{m:.2e}' for m in mins)})")
t2 = np.linspace(-1, 1, 401); U2, V2 = np.meshgrid(t2, t2)
p, q = 0.5 * g2(U2), 0.5 * g2(V2)
print(f"   on the whole square [-1,1]^2 the interior factor has min lambda_min = "
      f"{((p + q) / 2 - np.sqrt(((p - q) / 2) ** 2 + b * b)).min():.3f} (nonconvex near the corners)")

# 3
for n, seed in ((6, None), (8, None), (6, 0), (8, 0)):
    c = np.zeros(n) if seed is None else np.random.default_rng(seed).uniform(-0.3, 0.3, n)
    x = cp.Variable(n); Xd = cp.Variable(n); Xo = cp.Variable(n - 1)
    cons = [x >= -1, x <= 1]
    for i in range(n - 1):
        M = cp.bmat([[np.ones((1, 1)), cp.reshape(x[i], (1, 1)), cp.reshape(x[i + 1], (1, 1))],
                     [cp.reshape(x[i], (1, 1)), cp.reshape(Xd[i], (1, 1)), cp.reshape(Xo[i], (1, 1))],
                     [cp.reshape(x[i + 1], (1, 1)), cp.reshape(Xo[i], (1, 1)), cp.reshape(Xd[i + 1], (1, 1))]])
        cons.append((M + M.T) / 2 >> 0)
    pr = cp.Problem(cp.Minimize(cp.sum(Xd) + c @ x + b * cp.sum(Xo)), cons)
    pr.solve(solver="CLARABEL")
    xs = cp.Variable(n)
    fq = cp.Problem(cp.Minimize(cp.quad_form(xs, H[:n, :n] / 2 * 2 / 2) + c @ xs), [xs >= -1, xs <= 1])
    Q = 2 * np.eye(n) + b * (np.eye(n, k=1) + np.eye(n, k=-1))
    fq = cp.Problem(cp.Minimize(0.5 * cp.quad_form(xs, Q) + c @ xs), [xs >= -1, xs <= 1]); fq.solve(solver="CLARABEL")
    print(f"3. kappa = 0, {'c = 0' if seed is None else 'seed 0'}, n = {n}: clique-PSD bound on the root box = "
          f"{pr.value:.9f}, f* = {fq.value:.9f}, difference {fq.value - pr.value:.1e}")
