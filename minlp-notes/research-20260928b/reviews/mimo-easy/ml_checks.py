"""Reviewer checks of Section 2.1-2.2 (ML threshold).

1. Lemma 2.1 (Chernoff bound for a fixed direction): Monte Carlo of
   P(F(c) <= W - s) against e^{-s/4}(1 + rho||c||^2/(4N))^{-M/2}.
2. Direction (a) (first moment): the sum Sigma of (2.1) evaluated exactly
   (log-binomials) at rho*beta = c log N; x* is ML w.h.p. once Sigma -> 0.
3. Direction (d) (converse): given ||w||^2 = W, the N one-bit events
   E_i = {zeta_i + ||b_i||^2 < 0} are independent with probability p(W);
   P(x* has no improving one-bit neighbour | W) = (1 - p)^N, computed by
   numerical integration (g ~ N(0,1), X ~ chi^2_{M-1} independent).
Written by the reviewer.  Usage: python3 ml_checks.py > ml_checks.out
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy import stats
from scipy.special import gammaln, logsumexp


def lemma21_mc():
    rng = np.random.default_rng(5)
    print("Lemma 2.1 Monte Carlo: N M rho |c|^2 s | empirical P(F(c) <= W - s)  bound")
    for (N, M, rho, c2, s) in [(50, 50, 2.0, 4.0, 0.0), (50, 50, 2.0, 4.0, 4.0), (50, 100, 1.0, 8.0, 0.0), (20, 20, 0.5, 4.0, 0.0)]:
        T = 400000
        a = np.sqrt(rho * c2 / N)
        # F(c) - W = 2a<z,w> + a^2 ||z||^2 with z, w iid N(0, I_M); <z,w> and ||z||^2 simulated exactly
        z2 = rng.chisquare(M, T)
        zw = np.sqrt(z2) * rng.standard_normal(T)  # <z,w> | z ~ N(0, ||z||^2)
        emp = np.mean(2 * a * zw + a * a * z2 <= -s)
        bnd = np.exp(-s / 4) * (1 + rho * c2 / (4 * N)) ** (-M / 2)
        print(f"  {N} {M} {rho} {c2} {s} | {emp:.5f} {bnd:.5f} {'OK' if emp <= bnd + 3*np.sqrt(bnd/T) else 'VIOLATION'}")


def log_sigma(N, beta, rho):
    k = np.arange(1, N + 1, dtype=float)
    lc = gammaln(N + 1) - gammaln(k + 1) - gammaln(N - k + 1)
    return float(logsumexp(lc - (beta * N / 2) * np.log1p(rho * k / N)))


def one_bit_p(N, beta, rho):
    """P(E_1 | ||w||^2 = M), E_1 = {sqrt(rho/N)||w|| g + (rho/N)(g^2 + X) < 0}."""
    M = beta * N
    W = M
    q = (np.arange(4000) + 0.5) / 4000
    X = stats.chi2.ppf(q, M - 1)
    a = rho / N; b = np.sqrt(rho * W / N)
    disc = b * b - 4 * a * a * X
    ok = disc > 0
    gm = (-b - np.sqrt(np.where(ok, disc, 0))) / (2 * a)
    gp = (-b + np.sqrt(np.where(ok, disc, 0))) / (2 * a)
    pr = np.where(ok, stats.norm.cdf(gp) - stats.norm.cdf(gm), 0.0)
    return float(pr.mean())


if __name__ == "__main__":
    lemma21_mc()
    print("\nFirst-moment sum Sigma of (2.1) at rho*beta = c log N (x* unique ML w.p. >= 1 - Sigma):")
    for beta in (1.0, 2.0):
        for c in (2.2, 2.5, 3.0, 4.0):
            row = []
            for N in (10 ** 2, 10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7):
                rho = c * np.log(N) / beta
                row.append(f"N=1e{int(np.log10(N))}:{np.exp(log_sigma(N, beta, rho)):.3g}")
            print(f"  beta={beta} c={c}: " + "  ".join(row))
    print("\nConverse: E[#improving one-bit flips] = N p and P(no improving flip) = (1-p)^N at ||w||^2 = M:")
    for beta in (1.0, 2.0):
        for c in (1.0, 1.5, 1.8, 2.0, 2.2):
            row = []
            for N in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 8):
                rho = c * np.log(N) / beta
                p = one_bit_p(N, beta, rho)
                row.append(f"N=1e{int(np.log10(N))}: Np={N*p:.3g} P(none)={np.exp(N*np.log1p(-p)):.3f}")
            print(f"  beta={beta} c={c}: " + " | ".join(row))
    print("\nPapailiopoulos' boundary: N Q(sqrt(rho)) ~ 1 at rho = 2 log N - log log N + O(1)  (beta = 1):")
    for N in (10 ** 3, 10 ** 5, 10 ** 8):
        rho = 2 * np.log(N) - np.log(np.log(N))
        print(f"  N=1e{int(np.log10(N))}: rho/log N at 2logN - loglogN = {rho/np.log(N):.3f}; N p there = {N*one_bit_p(N, 1.0, rho):.3f}")
