"""Checks of the constants in Proposition 5.2 of the coupling note.

- Hadamard rows: |a_j|_2 = gamma, |a_j|_1 = 1/2, A A^T = gamma^2 I.
- Feasibility of (x(s), s) on S_0 = [-1/(2k), 1/(2k)]^k: max_i |x_i(s)| <= 1
  (checked at the vertices of S_0, where the max of a convex function is).
- Quadratic growth on the feasible set and lambda = 0.8 m.
- h'' >= -beta on [-1, 1]; alpha/lambda' and the per-row base.
- Extension (referee): the tightest termwise relaxation, the convex
  envelope of h on a box, still has gap >= ((beta - 12)/2) q_B because
  h'' <= -(beta - 12) on [-1, 1]; base with that alpha.
- The exact bound 2 (2k alpha/(pi lambda'))^{k/2} Gamma(k/2)^{-1} J_k(T)
  for some (k, eps), with J_k by quadrature.

Usage: python3 c5_prop52.py
"""
import itertools
import numpy as np
from math import gamma as Gamma, pi, e, sqrt
from scipy.linalg import hadamard
from scipy.integrate import quad

for m, k in [(4, 1), (4, 4), (8, 3), (16, 16), (64, 10)]:
    H = hadamard(m)
    g = 1 / (2 * sqrt(m))
    A = g * H[:k] / sqrt(m)
    n2 = np.linalg.norm(A, axis=1)
    n1 = np.abs(A).sum(axis=1)
    gram_err = np.abs(A @ A.T - g ** 2 * np.eye(k)).max()
    r = 1 / (2 * k)
    worst = 0.0
    for sgn in itertools.product([-1, 1], repeat=k):
        s = r * np.array(sgn)
        x = A.T @ s / g ** 2
        worst = max(worst, np.abs(x).max())
    beta = 0.8 / g ** 2
    lam = 1 / g ** 2 - beta
    ss = np.linspace(-1, 1, 2001)
    hpp = -beta + 12 * ss ** 2
    alpha = beta / 2
    lamp = lam + 1 / (2 * k ** 2)
    base = sqrt(4 * e * alpha / (pi * lamp))
    alpha_env = (beta - 12) / 2
    base_env = sqrt(4 * e * alpha_env / (pi * lamp)) if alpha_env > 0 else float("nan")
    print(f"m={m:3d} k={k:2d}: |a|_2={n2.min():.4f}..{n2.max():.4f} (gamma={g:.4f}) |a|_1={n1.min():.3f}..{n1.max():.3f} "
          f"gram_err={gram_err:.1e} max|x(s)|={worst:.3f} lambda/m={lam/m:.2f} min h''+beta={hpp.min()+beta:.2f} "
          f"alpha/lambda'={alpha/lamp:.3f} base={base:.3f} | envelope alpha'={alpha_env:.1f} base'={base_env:.3f}")

print("\nexact bound N >= 2 (2k alpha/(pi lambda'))^{k/2} / Gamma(k/2) * J_k(sqrt(lambda'/(8 k^2 eps))), m = max(4, k rounded up to 2^j)")
for k in [1, 2, 4, 8, 16]:
    m = 4
    while m < k:
        m *= 2
    g = 1 / (2 * sqrt(m)); beta = 0.8 / g ** 2; lam = 1 / g ** 2 - beta
    alpha = beta / 2; lamp = lam + 1 / (2 * k ** 2)
    for eps in [0.1 / k ** 2, 1e-6]:
        T = sqrt(lamp / (8 * k ** 2 * eps))
        J = quad(lambda t: t ** (k - 1) * (1 + t * t) ** (-k / 2), 0, T, limit=200)[0]
        N = 2 * (2 * k * alpha / (pi * lamp)) ** (k / 2) / Gamma(k / 2) * J
        print(f"  k={k:2d} m={m:3d} eps={eps:.1e}: T={T:.2f} J_k={J:.3f} N>={N:.3e}")
