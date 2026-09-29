"""Numerical check of Dey-Kocuk Conjecture 2 at kappa = 2 (arXiv 2510.16595).

Compares, for random separable objectives sum_i alpha_i x_i + beta_i x_i^2
over the simplex: the exact optimum (enumeration of KKT points on faces),
PR (X >= 0, Xe = x, X_ii = y_i, y_i >= x_i^2), PRs3 (plus all 3x3 blocks),
and PRS (full PSD). Floating-point SDP; evidence only.
"""
import itertools, sys
import numpy as np
import cvxpy as cp


def exact(alpha, beta):
    n = len(alpha); best = np.inf
    for r in range(1, n + 1):
        for S in itertools.combinations(range(n), r):
            S = list(S)
            if r == 1:
                val = alpha[S[0]] + beta[S[0]]
            else:
                inv = 1.0 / (2 * beta[S])
                mu = (1 + np.sum(alpha[S] * inv)) / np.sum(inv)
                x = (mu - alpha[S]) * inv
                if np.any(x <= 0):
                    continue
                val = np.sum(alpha[S] * x + beta[S] * x * x)
            best = min(best, val)
    return best


def relax(alpha, beta, mode):
    n = len(alpha)
    Z = cp.Variable((n + 1, n + 1), symmetric=True)  # [[X, x],[x^T, 1]]
    X = Z[:n, :n]; x = Z[:n, n]
    cons = [Z[n, n] == 1, X >= 0, cp.sum(X, axis=1) == x, x >= 0, cp.sum(x) == 1]
    for i in range(n):
        cons.append(cp.bmat([[X[i, i], x[i]], [x[i], 1]]) >> 0)
    if mode == "PRs3":
        for i, j in itertools.combinations(range(n), 2):
            idx = [i, j, n]
            cons.append(Z[np.ix_(idx, idx)] >> 0)
    if mode == "PRS":
        cons.append(Z >> 0)
    obj = cp.Minimize(alpha @ x + beta @ cp.diag(X))
    prob = cp.Problem(obj, cons)
    prob.solve(solver="CLARABEL")
    return prob.value


if __name__ == "__main__":
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    worst = {"PR": 0.0, "PRs3": 0.0, "PRS": 0.0}
    for trial in range(60):
        n = int(rng.integers(3, 8))
        alpha = rng.uniform(-1, 1, n); beta = rng.uniform(-1, 1, n)
        ex = exact(alpha, beta)
        for mode in worst:
            v = relax(alpha, beta, mode)
            worst[mode] = max(worst[mode], ex - v)
    print("max (exact - relaxation) over 60 random instances, n in 3..7:")
    for k, v in worst.items():
        print(f"  {k:5s} {v:.2e}")
