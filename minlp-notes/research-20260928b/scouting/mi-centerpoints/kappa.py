"""Worst ratio kappa_d = sum_j M_j / max_tau tau*ceil(N(tau)/2) over sequences with
M^{1/d} concave (d = inf: log-concave), where N(tau) = #{j : M_j >= tau}.

Family searched: M_j^{1/d} = two-slope tent with apex c, truncated to an integer window
(these are the extreme 1/d-concave profiles for this layer-cake ratio).
The line lemma gives F(S) >= g_d / kappa_d for n = 1.
"""
import numpy as np
from scipy.optimize import minimize
from multiprocessing import Pool

def ratio(M):
    M = np.sort(M[M > 0])[::-1]
    if len(M) == 0:
        return 0.0
    asc = M[::-1]
    N = len(M) - np.searchsorted(asc, M, side="left")  # #entries >= M[i]
    return M.sum() / np.max(M * np.ceil(N / 2))

J = np.arange(-600, 601).astype(float)

def seq(p, d):
    c, sp, sm, lo, hi = p
    x = J - c
    if d == np.inf:
        M = np.exp(np.where(x >= 0, -abs(sp) * x, abs(sm) * x))
    else:
        M = np.clip(np.where(x >= 0, 1 - abs(sp) * x, 1 + abs(sm) * x), 0, None) ** d
    return np.where((J >= -abs(lo)) & (J <= abs(hi)), M, 0.0)

def search(d, trials=150, seed=0):
    rng = np.random.default_rng(seed)
    best = (0.0, None)
    for _ in range(trials):
        p0 = [rng.uniform(0, 1), 10 ** rng.uniform(-2.5, 0.5), 10 ** rng.uniform(-2.5, 0.5),
              rng.uniform(0, 500), rng.uniform(0, 500)]
        r = minimize(lambda p: -ratio(seq(p, d)), p0, method="Nelder-Mead", options=dict(maxiter=300))
        if -r.fun > best[0]:
            best = (-r.fun, r.x)
    return best

if __name__ == "__main__":
    DS = [1, 2, 3, 5, 10, 20, 50, np.inf]
    with Pool(8) as pool:
        res = pool.map(search, DS)
    for d, (k, p) in zip(DS, res):
        g = (d / (d + 1)) ** d if d != np.inf else np.exp(-1)
        helly = 0.5 / (d + 1) if d != np.inf else 0.0
        print(f"d={d}: kappa~{k:.4f} -> g_d/kappa = {g / k:.4f}; Helly 1/(2(d+1)) = {helly:.4f}; params {np.round(p, 4)}")
    print("2e =", 2 * np.e, " 2(1+e) =", 2 * (1 + np.e), " 1/(2e(1+e)) =", 1 / (2 * np.e * (1 + np.e)))
