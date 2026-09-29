"""Numerical checks for the revised hard side (Theorems 4.3, 4.4; Section 4.4), own code.
(1) constants x0, 2/x0, K(x), K/(e^x-1);
(2) for x in (0, x0): the largest c' admitted by the proof, i.e. max c' subject to
    (1+mu)(1-theta) x / B(c') > e^x - 1,  B = 1 + 2 sqrt(c'x) + 2c'x,  c' < (1-mu) theta;
    and the same for the planted condition 1 + kappa_s < e^{-x}(1 + (1+mu)(1-theta)x/B) at kappa_s = K(x)/2;
(3) the two elementary GV inequalities of Step 4 on a grid, and the exact GV exponent versus
    (1-mu) theta k log(p/k);
(4) Monte Carlo of Step 5: with W = top-M |c_j| and a greedy code on W (data-dependent),
    ||X_U^perp c_U||^2 / s_U should be exactly chi^2_{n-1};
(5) the finite-p condition of Section 4.4 for a single pair at the points quoted in the revision.
usage: python3 hard_check.py"""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq
from scipy.special import gammaln
from scipy.stats import norm, chi2, kstest

K = lambda x: np.exp(-x) * (1 + 2 * x) - 1
x0 = brentq(K, 0.5, 2.0)
print("(1) x0 = %.10f, 2/x0 = %.4f, max K = K(1/2) = %.4f (2e^-1/2 - 1 = %.4f)" % (x0, 2 / x0, K(0.5), 2 * np.exp(-0.5) - 1))
for x in [0.1, 0.5, 1.0, 1.2]:
    print("    x=%.1f: K(x)=%.4f, K/(e^x-1)=%.3f, sqrt(K/x)=%.3f" % (x, K(x), K(x) / np.expm1(x), np.sqrt(K(x) / x)))

print("(2) largest c' admitted by Steps 2-6 (grid search over mu, theta)")
mus = np.linspace(0.5, 0.999, 300); ths = np.linspace(0.001, 0.5, 300)
def best_c(x, rhs):
    best = (0.0, None, None)
    for mu in mus:
        for th in ths:
            A = (1 + mu) * (1 - th) * x
            if A <= rhs: continue
            # need B(c') < A/rhs, i.e. 1 + 2 sqrt(c'x) + 2c'x < A/rhs  -> solve for sqrt(c'x)
            Bmax = A / rhs
            s = (-2 + np.sqrt(4 + 8 * (Bmax - 1))) / 4   # 2s^2 + 2s + 1 = Bmax
            c = min(s * s / x, (1 - mu) * th)
            if c > best[0]: best = (c, mu, th)
    return best
for x in [0.05, 0.2, 0.5, 0.8, 1.0, 1.2, 1.25]:
    c, mu, th = best_c(x, np.expm1(x))
    B = 1 + 2 * np.sqrt(c / 2 * x) + c * x          # eta0 evaluated at c'/2 (c'_max is a supremum)
    eta0 = np.exp(-x) - B / (B + (1 + mu) * (1 - th) * x) if c > 0 else float('nan')
    kap = K(x) / 2
    cp, _, _ = best_c(x, (1 + kap) * np.exp(x) - 1)     # planted: A/B > (1+kappa)e^x - 1
    print("    x=%.2f: c'_max ~ %.2e (mu=%.3f, theta=%.3f, eta0 at c'/2 = %.2e); planted at kappa_s=K(x)/2: c'_max ~ %.2e" %
          (x, c, mu if mu else 0, th if th else 0, eta0, cp))

print("(3) GV inequalities")
lb = lambda a, b: gammaln(a + 1) - gammaln(b + 1) - gammaln(a - b + 1)
viol = 0; cnt = 0
for k in [3, 10, 30, 100, 300]:
    for R in [2, 5, 20, 100, 1000]:
        M = R * k
        for mu in [0.1, 0.3, 0.5, 0.8, 0.95]:
            m = int(np.ceil(mu * k))
            lhs = np.logaddexp.reduce([lb(k, d) + lb(M - k, d) for d in range(m)])
            rhs = np.log(m) + k * np.log(2) + m * np.log(np.e * M / m)
            viol += lhs > rhs + 1e-12; viol += lb(M, k) < k * np.log(M / k) - 1e-12; cnt += 2
print("    %d inequality instances, %d violations" % (cnt, viol))
for k, mu, th in [(100, 0.8, 0.1), (1000, 0.8, 0.1)]:
    for L in [10, 30, 100, 1000]:          # L = log(p/k)
        M = float(np.ceil(k * np.exp(th * L))); m = int(np.ceil(mu * k))
        # exact GV log-size via log-sum-exp (terms up to d = m-1)
        # stable log C(N, d) for huge N and small d: sum_{i<d} log(N - i) - log d!
        lbs = lambda N, d: float(np.sum(np.log(N - np.arange(d)))) - gammaln(d + 1)
        ball = np.logaddexp.reduce([lb(k, d) + lbs(M - k, d) for d in range(m)])
        gv = lbs(M, k) - ball
        print("    k=%d mu=%.1f theta=%.1f log(p/k)=%d: log GV / ((1-mu) theta k log(p/k)) = %.3f" % (k, mu, th, L, gv / ((1 - mu) * th * k * L)))

print("(4) Step 5 Monte Carlo (data-dependent W and code)")
rng = np.random.default_rng(11)
n, p, k, M, m = 60, 3000, 4, 24, 3
stats = []
for rep in range(400):
    y = rng.standard_normal(n) * (1 + rng.random())
    X = rng.standard_normal((n, p))
    yh = y / np.linalg.norm(y)
    c = X.T @ yh
    W = np.argsort(-np.abs(c))[:M]
    code = []
    for S in [tuple(sorted(rng.choice(W, k, replace=False))) for _ in range(200)]:
        if all(len(set(S) - set(T)) >= m for T in code): code.append(S)
    Xp = X - np.outer(yh, yh @ X)
    for i in range(min(len(code), 4)):
        for j in range(i + 1, min(len(code), 4)):
            U = sorted(set(code[i]) | set(code[j]))
            sU = float(c[U] @ c[U])
            stats.append(float(np.sum((Xp[:, U] @ c[U]) ** 2) / sU))
ks = kstest(stats, chi2(n - 1).cdf)
print("    %d pair statistics: mean %.2f (chi2_{n-1} mean %d), KS p-value %.3f" % (len(stats), np.mean(stats), n - 1, ks.pvalue))

print("(5) finite-p condition (Section 4.4 form) for a single pair, delta = 0.05")
def rho_star(n, p, k, delta):
    q = k / n; target = (lb(p, k) + np.log(1 / delta)) * 2 / n
    d = lambda r: q * np.log(q / r) + (1 - q) * np.log((1 - q) / (1 - r))
    return brentq(lambda r: d(r) - target, q * (1 + 1e-9), 1 - 1e-15)
for e, lamrule in [(5.5, 0), (5.5, 1), (6.0, 1), (5.0, 0)]:
    p = int(10 ** e); k = 2; alpha = 2048; n = int(alpha * k * np.log(p))
    lam = 0.0 if lamrule == 0 else np.sqrt(n * np.log(p))
    rs = rho_star(n, p, k, 0.05)
    t = 2 * np.log(2) + np.log(1 / 0.05)
    nu2 = (n - 1) + 2 * np.sqrt((n - 1) * t) + 2 * t
    for M in [4, 8]:
        tM = norm.isf(M / p)
        s = (k + k) * tM ** 2       # two disjoint k-subsets of W (exist once M >= 2k; no GV bound needed)
        frac = s / (s + nu2 + 2 * lam)
        print("    p=10^%.1f lam=%s n=%d M=%d: fraction %.6e vs rho* %.6e -> %s; P(count<M) bound e^{-M/4} = %.2f" % (
            e, '0' if lamrule == 0 else 'sqrt(n log p)', n, M, frac, rs, 'pair certified' if frac > rs else 'no', np.exp(-M / 4)))
