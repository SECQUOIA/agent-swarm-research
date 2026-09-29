"""Checks for the revision of Section 4-6 (hard side).
(1) n/n_IT for the Table 6.5 rows, n_IT = 2 k log(p/k)/log(1 + k b^2/sigma^2), b/sigma = 2, p = 10k.
(2) Detection-scale factor sqrt(alpha K(x)) with x = 2(1-gamma)/alpha, K(x) = e^{-x}(1+2x) - 1.
(3) Finite-p condition of Section 4.4 on a wider grid (lam = 0 and lam = sqrt(n log p), alpha up to 4096):
    smallest p (half-decade grid) with a certified conflicting pair (|C'| >= 2)."""
import numpy as np
from hard import rho_star, code_size_bound
from scipy.stats import norm
print("(1) Table 6.5 rows: n/n_IT")
for a in [0.35, 0.5]:
    out = []
    for k in range(3, 9):
        p = 10 * k; n = max(k + 2, int(round(a * k * np.log(p))))
        nIT = 2 * k * np.log(p / k) / np.log(1 + 4 * k)
        out.append("%.2f" % (n / nIT))
    print("  alpha=%.2f:" % a, ", ".join(out))
print("(2) detection-scale factor sqrt(alpha K(x)), x = 2(1-gamma)/alpha")
K = lambda x: np.exp(-x) * (1 + 2 * x) - 1
for g in [0.0, 0.25, 0.5, 0.75]:
    print("  gamma=%.2f:" % g, ", ".join("alpha=%g: %.2f" % (a, np.sqrt(a * max(K(2 * (1 - g) / a), 0))) for a in [2, 4, 16, 100, 1e4]))
def best_pair(p, lam_rule, alphas, ks, delta=0.05):
    for k in ks:
        for a in alphas:
            n = int(a * k * np.log(p))
            if n <= 2 * k: continue
            lam = 0.0 if lam_rule == 0 else np.sqrt(n * np.log(p))
            rs = rho_star(n, p, k, delta)
            for R in [2, 3, 4, 6, 8]:
                M = R * k
                if M >= p / 2: continue
                z = norm.isf(M / p)
                for mu in np.linspace(0.05, 1.0, 20):
                    m = max(1, int(round(mu * k)))
                    if m > k: continue
                    lc = code_size_bound(M, k, m)
                    if lc < np.log(2): continue
                    t = 2 * np.log(2) + np.log(1 / delta)      # a single pair: |C'| = 2
                    nu2 = (n - 1) + 2 * np.sqrt((n - 1) * t) + 2 * t
                    s = (k + m) * z * z
                    if s / (s + nu2 + 2 * lam) > rs:
                        return (k, a, n, R, m)
    return None
print("(3) first certified conflicting pair (finite-p condition), alpha <= 4096")
for lam_rule in [0, 1]:
    for e in [5, 5.5, 6, 6.5, 7, 7.5, 8]:
        p = int(10 ** e)
        r = best_pair(p, lam_rule, [8, 32, 128, 512, 2048, 4096], [2, 3, 4, 6, 9, 13])
        print("  lam=%s p=10^%.1f: %s" % ("0" if lam_rule == 0 else "sqrt(n log p)", e, r))
        if r: break
