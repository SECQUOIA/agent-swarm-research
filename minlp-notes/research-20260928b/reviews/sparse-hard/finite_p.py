"""Independent evaluation of the finite-p form of Theorem 4.3 (Section 4.4).

With probability >= 1 - 2 delta - exp(-M/4), all pairs of a code C' (|C'| = e^L) of
k-subsets of the top-M correlated features, pairwise |S \\ T| >= m, conflict (eps = 0) if

    s / (s + nu^2 + 2 lam) > rho*,        s = (k+m) z_M^2,  z_M = Phibar^{-1}(M/p),
    nu^2 = (n-1) + 2 sqrt((n-1) t) + 2 t,   t = 2 L + log(1/delta),
    (n/2) d(k/n || rho*) = log C(p,k) + log(1/delta),     L <= log GV(M,k,m).

For each configuration we report the largest admissible L (-inf if none >= log 2).
Part A reproduces the note's grid. Part B searches a wider grid (any k, alpha,
lam in {0, sqrt(n log p)}, R = M/k, m) for the smallest p with a nontrivial clique.
"""
import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm
from scipy.special import gammaln


def logbinom(a, b):
    b = int(b)
    if b < 0 or b > a:
        return -np.inf
    i = np.arange(b, dtype=float)
    return float(b * np.log(a) + np.sum(np.log1p(-i / a)) - gammaln(b + 1))


def d(q, r):
    return q * np.log(q / r) + (1 - q) * np.log((1 - q) / (1 - r))


def rho_star(n, p, k, delta):
    q = k / n
    target = 2 * (logbinom(p, k) + np.log(1 / delta)) / n
    if d(q, 1 - 1e-15) < target:
        return 1.0
    return brentq(lambda r: d(q, r) - target, q * (1 + 1e-12), 1 - 1e-15)


def log_gv(M, k, m):
    terms = [logbinom(k, dd) + logbinom(M - k, dd) for dd in range(m)]
    return logbinom(M, k) - np.logaddexp.reduce(terms)


def best_L(n, p, k, lam, delta=0.05, Rs=(2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64), nm=24):
    rs = rho_star(n, p, k, delta)
    if rs >= 1:
        return -np.inf, None
    best = (-np.inf, None)
    for R in Rs:
        M = R * k
        if M >= p / 2:
            continue
        z = norm.isf(M / p)
        for m in sorted(set(np.linspace(1, k, nm).astype(int))):
            s = (k + m) * z * z
            # condition: s/(s+nu2+2lam) > rs  <=>  nu2 < s(1-rs)/rs - 2 lam
            cap = s * (1 - rs) / rs - 2 * lam
            if cap <= n - 1:
                continue
            # nu2(t) increasing in t; find largest t with nu2 <= cap
            f = lambda t: (n - 1) + 2 * np.sqrt((n - 1) * t) + 2 * t - cap
            tmax = brentq(f, 0.0, cap)
            Lmax = min((tmax - np.log(1 / delta)) / 2, log_gv(M, k, m))
            if Lmax >= np.log(2) and Lmax > best[0]:
                best = (Lmax, (R, m))
    return best


if __name__ == '__main__':
    print("Part A: the note's grid (lam = sqrt(n log p), delta = 0.05)")
    for (p, k) in [(2000, 20), (1e4, 30), (1e5, 50), (1e6, 100), (1e8, 300), (1e12, 1000)]:
        row = []
        for alpha in [2, 4, 8, 16]:
            n = int(round(alpha * k * np.log(p)))
            L, arg = best_L(n, p, k, np.sqrt(n * np.log(p)))
            row.append("a=%d: %s" % (alpha, ("L=%.1f %s" % (L, arg)) if np.isfinite(L) else "none"))
        print("  p=%.0e k=%d | %s" % (p, k, " | ".join(row)))

    print("\nPart B: smallest p with any admissible code (L >= log 2), lam in {0, sqrt(n log p)}")
    for lamrule in ['zero', 'sqrt(n log p)']:
        found = None
        for lp in np.arange(3.0, 13.01, 0.5):
            p = 10 ** lp
            bestp = (-np.inf, None)
            for k in np.unique(np.geomspace(5, min(p / 100, 3e4), 30).astype(int)):
                for alpha in [1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32, 64, 128]:
                    n = int(round(alpha * k * np.log(p)))
                    lam = 0.0 if lamrule == 'zero' else np.sqrt(n * np.log(p))
                    L, arg = best_L(n, p, k, lam)
                    if L > bestp[0]:
                        bestp = (L, (int(k), alpha, n, arg))
            print("  lam=%s p=1e%.1f: best L = %s  (k, alpha, n, (R, m)) = %s" % (lamrule, lp, "%.2f" % bestp[0], bestp[1]))
            if np.isfinite(bestp[0]) and found is None:
                found = lp
            if found is not None and lp >= found + 1.0:
                break
        print("  -> first p with a nontrivial certified clique (lam=%s): 1e%s" % (lamrule, found))
