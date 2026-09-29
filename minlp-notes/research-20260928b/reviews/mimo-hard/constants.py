"""Constants and ranges of Theorems 4.1 and 4.3 of
bb-complexity/binary-least-squares/certification-thresholds.md (review check).

Part A  recompute c_beta, the slack factors, rho_0 and c'_beta of Theorem 4.3.
Part B  where the Theorem 4.3 bound first becomes positive / superlinear.
Part C  exponent gap between Theorem 4.1 (upper) and Theorem 4.3 (lower).
Part D  the kappa_N loss of Theorem 4.1 is a proof artifact: the sum of the
        K most negative zeta_i is about -K a sqrt(2 log(N/K)), not
        -K a sqrt(2 log N).
Part E  midpoint-clique upper bound by first moment: largest n1 (number of
        half moves) of a ternary point with F(c) < W, compared with N^{1-c/8}.
"""
import numpy as np
from scipy.special import gammaln, logsumexp
from scipy.stats import norm

E2 = np.e ** 2
p = norm.cdf(-1) - norm.cdf(-2)
print("Part A: constants of Theorem 4.3")
print("  p = Phi(-1) - Phi(-2) = %.6f" % p)
print("  0.148 check: log(8)/7/2 = %.5f" % (np.log(8) / 7 / 2))
for beta in (1.0, 1.5, 2.0, 4.0):
    sb = np.sqrt(beta) + 1
    c_beta = beta * p / (64 * E2 * sb ** 4)
    xw = 1 / (E2 * sb ** 2)                      # bound on X/W
    # sum p_i^2 >= (3.92 - 0.5) a k / (4 rho sb^2);  lambda_1 k = sqrt(beta) k/(2 sb^2 sqrt rho)
    slack = (3.92 - 0.5) / 4 / 0.5              # ratio of the two, a = sqrt(rho beta)
    ak_over_N = beta * p / (8 * E2 * sb ** 2)    # a k / N with n' = pN/2, k = lambda_1 n'/(2e^2)
    cprime = 0.25 * ak_over_N                    # need eps' <= rho <= 0.25 a k
    # rho_0 as in the note: e^{-0.148 beta rho} <= 0.4 beta p/(64 e^2 sb^2)
    rho0_note = -np.log(0.4 * beta * p / (64 * E2 * sb ** 2)) / (0.148 * beta)
    # the requirement actually needed: 4 N e^{-0.148 beta rho} <= 0.25 a k (leading order)
    rho0_need = -np.log(0.25 * ak_over_N / 4) / (0.148 * beta)
    # k >= 1 requires lambda_1 p N/(4e^2) >= 2
    print("  beta=%.1f  c_beta=%.3e  X/W<=%.4f  slack(sum p^2 vs lambda_1 k)=%.2f  "
          "ak/N=%.3e  c'_beta~%.2e  rho_0(note)=%.1f  rho_0(needed)=%.1f"
          % (beta, c_beta, xw, slack, ak_over_N, cprime, rho0_note, rho0_need))

print()
print("Part B: first N where c_beta (N/rho) log rho - log(8N) > 0 (and > 10 log N), beta = 1")
beta = 1.0; sb = 2.0
c1 = beta * p / (64 * E2 * sb ** 4)
for name, rho_of in [("rho = 4 log N", lambda N: 4 * np.log(N)),
                     ("rho = 8 log N", lambda N: 8 * np.log(N)),
                     ("rho = 71 (fixed)", lambda N: 71.0 + 0 * N),
                     ("rho = sqrt(N)", lambda N: np.sqrt(N))]:
    Ns = np.logspace(3, 14, 2000)
    rho = rho_of(Ns)
    lb = c1 * Ns / rho * np.log(rho) - np.log(8 * Ns)
    pos = Ns[lb > 0]
    sup = Ns[lb > 10 * np.log(Ns)]
    print("  %-18s  bound > 0 from N ~ %.2e ;  bound > 10 log N from N ~ %.2e"
          % (name, pos[0] if len(pos) else np.nan, sup[0] if len(sup) else np.nan))

print()
print("Part C: exponent of Theorem 4.1 (upper) / Theorem 4.3 (lower, without -log 8N), beta = 1")
for N in (1e6, 1e8, 1e10, 1e12):
    for c in (3.0, 4.0, 8.0):
        rho = c * np.log(N)
        kN = 1 - np.sqrt(2 * np.log(N) / rho)
        up = N / (4 * kN * rho) * np.log(4 * np.e * kN * rho)
        lo = c1 * N / rho * np.log(rho)
        print("  N=%.0e c=%g  upper exponent %.3e  lower exponent %.3e  ratio %.0f"
              % (N, c, up, lo, up / lo))

print()
print("Part D: sum of the K most negative g_i versus K * max(-g_i)  (K = N/(4 rho), beta = 1)")
rng = np.random.default_rng(5)
for N in (10 ** 4, 10 ** 5, 10 ** 6):
    for c in (3.0, 4.0):
        rho = c * np.log(N)
        K = int(np.ceil(N / (4 * rho)))
        g = rng.standard_normal(N)
        topK = np.sort(-g)[-K:].sum()
        print("  N=%.0e c=%g K=%d: sum of top-K(-g)/K = %.3f, sqrt(2 log(N/K)) = %.3f, "
              "max(-g) = %.3f, sqrt(2 log N) = %.3f  ->  kappa_N = %.3f, refined 1 - sqrt(2 log(N/K)/rho) = %.3f"
              % (N, c, K, topK / K, np.sqrt(2 * np.log(N / K)), (-g).max(), np.sqrt(2 * np.log(N)),
                 1 - np.sqrt(2 * np.log(N) / rho), 1 - np.sqrt(2 * np.log(N / K) / rho)))

print()
print("Part E: midpoint-clique upper bound (first moment of Lemma 2.1), beta = 1")
print("  largest n1 with expected number of ternary c (n1 ones, any n2 twos) with F(c) < W at least 1e-3")
for N in (10 ** 4, 10 ** 5):
    M = N
    for c in (2.5, 4.0, 6.0):
        rho = c * np.log(N)
        n1s = np.arange(1, min(N, 20000) + 1)
        n2s = np.arange(0, N + 1)
        lastn1 = 0
        for n1 in n1s:
            n2 = n2s[: N - n1 + 1]
            logt = (gammaln(N + 1) - gammaln(n1 + 1) - gammaln(N - n1 + 1)
                    + gammaln(N - n1 + 1) - gammaln(n2 + 1) - gammaln(N - n1 - n2 + 1)
                    - (M / 2) * np.log1p(rho * (n1 + 4 * n2) / (4 * N)))
            if logsumexp(logt) > np.log(1e-3):
                lastn1 = n1
            elif n1 > 3 * max(lastn1, 10):
                break
        print("  N=%.0e c=%.1f: last n1 with E >= 1e-3: %d ;  N^{1-c/8} = %.1f ;  e^2 N^{1-c/8} = %.1f"
              % (N, c, lastn1, N ** (1 - c / 8), E2 * N ** (1 - c / 8)))
