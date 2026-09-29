"""Checks of the constants and probabilistic ingredients of Section 4.

1. x0: root of e^{-x}(1+2x) = 1; 2/x0; max of K(x) = e^{-x}(1+2x) - 1.
2. Beta Chernoff bound of Lemma 4.1 vs the exact Beta tail (mpmath-free, scipy),
   on a wider grid than the author's (large n, small q = k/n, rho near q and near 1).
3. Step 1 of Theorem 4.3: -log(1 - rho*) -> x as q -> 0.
4. Relation of the Theorem 4.4 region to the information-theoretic threshold:
   K < e^{-x}(1+2x)-1  vs  K < e^x - 1  (n < n_IT  <=>  x > log(1+K)).
5. The "detection scale" sentence after Theorem 4.4:
   b / (sigma sqrt(log p / n)) < sqrt(alpha K(x)), x = 2(1-gamma)/alpha.
6. Gilbert-Varshamov exponent e(mu,R) and how the clique exponent c can be made large.
"""
import numpy as np
from scipy.optimize import brentq
from scipy.stats import beta as betad
from scipy.special import gammaln

H = lambda t: -t * np.log(t) - (1 - t) * np.log(1 - t)

# 1
K = lambda x: np.exp(-x) * (1 + 2 * x) - 1
x0 = brentq(K, 0.5, 3.0)
print("x0 = %.10f, 2/x0 = %.6f, K(1/2) = %.6f, 2e^{-1/2}-1 = %.6f" % (x0, 2 / x0, K(0.5), 2 * np.exp(-0.5) - 1))
xs = np.linspace(1e-4, x0, 200001)
print("argmax K on (0,x0): %.5f" % xs[np.argmax(K(xs))])

# 2
def d(q, r):
    return q * np.log(q / r) + (1 - q) * np.log((1 - q) / (1 - r))

worst = -np.inf; where = None
for n in [10, 30, 100, 300, 1000, 3000]:
    for k in [1, 2, 5, 10, 30, 100]:
        if k >= n:
            continue
        q = k / n
        for rho in np.concatenate([q + np.geomspace(1e-4, 1e-1, 12) * (1 - q), np.linspace(q, 1, 40)[1:-1]]):
            if rho <= q or rho >= 1:
                continue
            lb = -(n / 2) * d(q, rho)
            ex = betad.logsf(rho, k / 2, (n - k) / 2)
            if np.isfinite(ex) and ex - lb > worst:
                worst = ex - lb; where = (n, k, rho)
print("Beta Chernoff: max over grid of log(exact tail) - log(bound) = %.4f at (n,k,rho)=%s (must be <= 0)" % (worst, where))

# 3
def logbinom(a, b):
    b = int(b); i = np.arange(b, dtype=float)
    return float(b * np.log(a) + np.sum(np.log1p(-i / a)) - gammaln(b + 1))

print("Step 1: rho* vs 1-e^{-x} for fixed x = 0.8, delta = 1/k, k/n -> 0:")
for (p, k) in [(1e4, 20), (1e6, 50), (1e9, 200), (1e15, 1000), (1e30, 1e4), (1e60, 1e5)]:
    x = 0.8
    n = int(round(2 * logbinom(p, k) / x))
    q = k / n
    target = (logbinom(p, k) + np.log(k)) * 2 / n
    rs = brentq(lambda r: d(q, r) - target, q * (1 + 1e-12), 1 - 1e-15)
    print("  p=%.0e k=%d n=%d q=%.4f  rho*=%.4f  1-e^{-x}=%.4f  -log(1-rho*)=%.4f" % (p, k, n, q, rs, 1 - np.exp(-x), -np.log(1 - rs)))

# 4
xg = np.linspace(1e-3, x0 - 1e-3, 2000)
print("Theorem 4.4 region inside n < n_IT: max over x of [e^{-x}(1+2x)-1] - [e^x - 1] = %.4f (must be < 0)"
      % np.max(K(xg) - (np.exp(xg) - 1)))
print("  ratio K(x)/(e^x-1) at x = 0.1, 0.5, 1.0, 1.2: %s" % np.round(K(np.array([.1, .5, 1., 1.2])) / (np.exp(np.array([.1, .5, 1., 1.2])) - 1), 3))

# 5
print("Detection-scale factor sqrt(alpha K(x)) with x = 2(1-gamma)/alpha (claim: < 1):")
for gamma in [0.0, 0.25, 0.5]:
    row = []
    for alpha in [2, 4, 10, 30, 100, 1000]:
        x = 2 * (1 - gamma) / alpha
        row.append(np.sqrt(alpha * K(x)) if x < x0 else np.nan)
    print("  gamma=%.2f alpha=[2,4,10,30,100,1000]: %s" % (gamma, np.round(row, 3)))
print("  sup_alpha sqrt(alpha K) = sqrt(2(1-gamma)) (limit x->0); exceeds 1 iff gamma < 1/2")

# 6
def e_GV(mu, R):
    return R * H(1 / R) - (H(mu) + (R - 1) * H(mu / (R - 1)))

print("GV exponent e(mu,R) = R H(1/R) - phi_R(mu):")
for mu in [0.3, 0.5, 0.8]:
    print("  mu=%.1f: " % mu + ", ".join("R=%d: %.3f" % (R, e_GV(mu, R)) for R in [2, 3, 5, 10, 100, 1000] if mu < (R - 1) / R))
print("  large-R asymptote (1-mu) log R + 1 - mu - H(mu) + mu log mu at mu=0.5, R=1000: %.3f"
      % ((0.5) * np.log(1000) + 1 - 0.5 - H(0.5) + 0.5 * np.log(0.5)))

# smallest admissible mu for given x (condition of Step 2)
print("Smallest admissible mu(x) in Step 2 and resulting clique exponent c = e(mu,R)/2 for R = 3, 10:")
for x in [0.1, 0.3, 0.5, 0.8, 1.0, 1.2]:
    f = lambda mu: (1 + mu) * x / (1 + (1 + mu) * x) - (1 - np.exp(-x))
    mu_min = brentq(f, -0.999, 1.0)
    mu = min(mu_min + 0.02, 0.99)
    print("  x=%.1f: mu_min=%.3f  c(R=3)=%s  c(R=10)=%.3f" % (x, mu_min,
          ("%.3f" % (e_GV(mu, 3) / 2)) if mu < 2 / 3 else "n/a (mu >= 2/3)", e_GV(mu, 10) / 2))
