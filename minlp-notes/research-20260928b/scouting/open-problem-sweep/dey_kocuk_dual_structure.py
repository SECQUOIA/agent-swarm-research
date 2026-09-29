"""Inspect which 3x3 blocks carry dual weight in PRs3 at a PR-gap instance."""
import itertools
import numpy as np
import cvxpy as cp
from dey_kocuk_conj2_check import exact

alpha = np.array([-0.3411, -0.7205, 0.9305, 0.2946, 0.7496])
beta = np.array([0.722, 1.0, 0.3513, -0.3761, -0.0632])
n = len(alpha)
Z = cp.Variable((n + 1, n + 1), symmetric=True)
X = Z[:n, :n]; x = Z[:n, n]
cons = [Z[n, n] == 1, X >= 0, cp.sum(X, axis=1) == x, x >= 0, cp.sum(x) == 1]
blocks = {}
for i, j in itertools.combinations(range(n), 2):
    idx = [i, j, n]
    c = Z[np.ix_(idx, idx)] >> 0
    blocks[(i, j)] = c; cons.append(c)
prob = cp.Problem(cp.Minimize(alpha @ x + beta @ cp.diag(X)), cons)
prob.solve(solver="CLARABEL")
print("exact", exact(alpha, beta), "PRs3", prob.value)
print("order of alpha (ascending):", np.argsort(alpha), " beta:", beta)
print("x* =", np.round(x.value, 4))
for (i, j), c in blocks.items():
    D = c.dual_value
    ev = np.linalg.eigvalsh(D)
    if np.abs(D).max() > 1e-6:
        print((i, j), "dual trace %.4f rank~%d" % (np.trace(D), int((ev > 1e-6 * max(1, ev.max())).sum())))
