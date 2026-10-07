"""Penalty chain: one coupling row, per-bag nonconvexity c/4, duality gap c n/4.

    min  sum_i c x_i (1 - x_i) + M sum_i (x_i - x_{i+1})^2
    s.t. sum_i x_i = n/2,  x in [0,1]^n.

Claims (Example 3.4): D = 0 (mix all-0 and all-1), OPT = c n/4 when
M >= c n (n-1). This script checks OPT numerically by multistart SLSQP and
evaluates the Lagrangian dual by a grid DP along the path (a check, not a
certificate), for several M.

Usage: python3 penalty_chain.py
"""
import numpy as np
from scipy.optimize import minimize


def F(x, c, M):
    return c * np.sum(x * (1 - x)) + M * np.sum(np.diff(x) ** 2)


def opt_multistart(n, c, M, starts=40, seed=0):
    rng = np.random.default_rng(seed)
    cons = [{"type": "eq", "fun": lambda x: np.sum(x) - n / 2}]
    best = np.inf
    for s in range(starts):
        if s == 0:
            x0 = np.full(n, 0.5)
        elif s == 1:
            x0 = np.r_[np.zeros(n // 2), np.ones(n - n // 2)]
        else:
            x0 = rng.random(n)
        r = minimize(F, x0, args=(c, M), bounds=[(0, 1)] * n, constraints=cons,
                     method="SLSQP", options={"maxiter": 500, "ftol": 1e-12})
        if r.success and abs(np.sum(r.x) - n / 2) < 1e-7:
            best = min(best, r.fun)
    return best


def lagrangian_grid(n, c, M, mu, G=401):
    """min_x F + mu (sum x - n/2) by DP on a grid of G points (upper estimate
    of the inner minimum; the exact inner minimum is <= this value)."""
    g = np.linspace(0, 1, G)
    unary = c * g * (1 - g) + mu * g
    pair = M * (g[:, None] - g[None, :]) ** 2
    V = unary.copy()
    for _ in range(n - 1):
        V = unary + np.min(V[:, None] + pair, axis=0)
    return np.min(V) - mu * n / 2


if __name__ == "__main__":
    c = 1.0
    print("n  M  OPT(multistart)  c*n/4  max_mu L(mu) (grid)")
    for n in [6, 10, 16]:
        for M in [1.0, 10.0, c * n * (n - 1)]:
            o = opt_multistart(n, c, M)
            mus = np.linspace(-2, 2, 81)
            d = max(lagrangian_grid(n, c, M, mu) for mu in mus)
            print(f"{n:3d}  {M:7.1f}  {o:.6f}  {c*n/4:.4f}  {d:.6f}")
