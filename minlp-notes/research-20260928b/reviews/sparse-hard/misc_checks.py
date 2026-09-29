"""Misc checks: (1) n / n_IT for the rows of Table 6.5 (first-order n_IT = 2k log(p/k)/log(1+k b^2/sigma^2));
(2) whether Table 6.4's b=0 and b=1 runs share the noise vector w (the note says 'same X and w');
(3) Psi(t) = E(|Z|-t)_+^2 vs 4 phi(t)/t^3 (Heuristic 3.8)."""
import numpy as np
from scipy.stats import norm
from cliquelib import instance_author
print("(1) Table 6.5: b=1, sigma=0.5, p=10k, n = round(alpha k log p)")
for alpha in (0.35, 0.5):
    out = []
    for k in range(3, 9):
        p = 10 * k; n = max(k + 2, int(round(alpha * k * np.log(p))))
        nit = 2 * k * np.log(p / k) / np.log(1 + k * 4.0)
        out.append("k=%d n=%d n_IT=%.1f ratio=%.2f" % (k, n, nit, n / nit))
    print("  alpha=%.2f: %s" % (alpha, "; ".join(out)))
print("(2) same w?")
for seed in range(3000, 3004):
    X0, y0, S0 = instance_author(41, 30, 3, b=0.0, sigma=0.5, seed=seed)
    X1, y1, S1 = instance_author(41, 30, 3, b=1.0, sigma=0.5, seed=seed)
    # recover beta of the planted instance: signs drawn after S
    rng = np.random.default_rng(seed); rng.standard_normal((41, 30)); rng.choice(30, 3, replace=False)
    signs = rng.choice([-1.0, 1.0], 3); beta = np.zeros(30); beta[list(S1)] = signs
    w0 = y0 / 0.5; w1 = (y1 - X1 @ beta) / 0.5
    print("  seed %d: X equal %s, S* equal %s, max|w0-w1| = %.3f, corr(w0,w1) = %.3f" % (
        seed, np.array_equal(X0, X1), S0 == S1, np.max(np.abs(w0 - w1)), np.corrcoef(w0, w1)[0, 1]))
print("(3) Psi(t) exact vs 4 phi/t^3:")
for t in (1.5, 2, 3, 4, 5):
    psi = 2 * ((1 + t * t) * norm.sf(t) - t * norm.pdf(t))
    print("  t=%.1f Psi=%.4e  4phi/t^3=%.4e  ratio=%.3f" % (t, psi, 4 * norm.pdf(t) / t ** 3, psi / (4 * norm.pdf(t) / t ** 3)))
