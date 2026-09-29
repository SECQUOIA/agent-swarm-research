"""Hard side: structured midpoint-conflict cliques in pure-noise / low-SNR sparse ridge regression.
Construction (Theorem H): W = M null features with largest |x_j^T y|; code = k-subsets of W with
pairwise |S \\ T| >= m.  S,T conflict iff g((1_S+1_T)/2) < OPT - eps, where
g(mid) = min_b ||y - X_U b||^2 + lam ||b_{S cap T}||^2 + 2 lam ||b_{S delta T}||^2  (exact formula)."""
import numpy as np
from scipy.special import gammaln
from scipy.optimize import brentq
from scipy.stats import norm

def g_mid(X, y, lam, S, T):
    U = sorted(set(S) | set(T)); Sc = set(S) & set(T)
    w = np.array([1.0 if u in Sc else 0.5 for u in U])
    XU = X[:, U]; bvec = XU.T @ y
    Mx = XU.T @ XU + lam * np.diag(1.0 / w)
    return float(y @ y - bvec @ np.linalg.solve(Mx, bvec))

def greedy_code(W, k, m, maxsize, rng, tries=20000):
    code = []
    for _ in range(tries):
        S = tuple(sorted(rng.choice(W, k, replace=False).tolist()))
        if all(len(set(S) - set(T)) >= m for T in code):
            code.append(S)
            if len(code) >= maxsize: break
    return code

def logbinom(a, b):
    return gammaln(a + 1) - gammaln(b + 1) - gammaln(a - b + 1)

def rho_star(n, p, k, delta):
    """Union bound: P(max_S ||P_S yhat||^2 >= rho) <= C(p,k) exp(-(n/2) d(k/n||rho)) = delta."""
    q = k / n
    target = (logbinom(p, k) + np.log(1 / delta)) * 2 / n
    d = lambda r: q * np.log(q / r) + (1 - q) * np.log((1 - q) / (1 - r))
    if d(1 - 1e-15) < target: return 1.0
    return brentq(lambda r: d(r) - target, q + 1e-12, 1 - 1e-15)

def code_size_bound(M, k, m):
    """Gilbert-Varshamov: C(M,k)/sum_{d<m} C(k,d)C(M-k,d)  (log, natural)."""
    tot = np.logaddexp.reduce([logbinom(k, d) + logbinom(M - k, d) for d in range(m)])
    return logbinom(M, k) - tot

def theorem_condition(n, p, k, lam, M, m, delta=0.05):
    """Asymptotic-free sufficient condition of Theorem H (pure noise):
    (k+m) z^2 / ((k+m) z^2 + nu^2 + 2 lam) > rho*,  z = Phibar^{-1}(M/(2p))-type quantile (conservative),
    nu = sqrt(n) + sqrt(M) + sqrt(2 log(1/delta))."""
    rs = rho_star(n, p, k, delta)
    z = norm.isf(M / p)       # P(|Z|>=z) = 2 M/p: mean count 2M, count >= M w.h.p.
    nu2 = (np.sqrt(n) + np.sqrt(M) + np.sqrt(2 * np.log(1 / delta))) ** 2
    s = (k + m) * z * z
    return s / (s + nu2 + 2 * lam), rs, code_size_bound(M, k, m)


def theorem_condition2(n, p, k, lam, M, m, logNC, delta=0.05):
    """Improved condition: nu_eff^2 = (n-1) + 2 sqrt((n-1) t) + 2 t, t = 2 logNC + log(1/delta)
    (chi-square bound, union over code pairs).  Code size N_C = exp(logNC) <= GV bound."""
    rs = rho_star(n, p, k, delta)
    z = norm.isf(M / p)
    t = 2 * logNC + np.log(1 / delta)
    nu2 = (n - 1) + 2 * np.sqrt((n - 1) * t) + 2 * t
    s = (k + m) * z * z
    return s / (s + nu2 + 2 * lam), rs
