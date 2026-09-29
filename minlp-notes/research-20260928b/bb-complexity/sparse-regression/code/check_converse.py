"""Check the explicit primal point of the C1 converse (forced-in node upper bound)."""
import numpy as np, sys
from core import instance, ridge, solve_node
def construction(X, y, lam, k, S, j, delta0=0.2, zeta=0.0):
    n, p = X.shape; S = list(S)
    fS, bS, r = ridge(X, y, lam, S); a = X.T @ r
    bplus = np.abs(bS).max(); kappa = lam * bplus * (1 + zeta)
    nulls = [l for l in range(p) if l not in S and l != j]
    Vp = [l for l in nulls if abs(a[l]) >= (1 + delta0) * kappa]
    if not Vp: return None
    XV = X[:, Vp]; Lop = np.linalg.norm(XV, 2) ** 2
    ex = np.abs(a[Vp]) - kappa; Q = ex @ ex
    s = min(1.0, 3 * lam * bplus ** 2 * Lop / Q)
    w = s * np.sign(a[Vp]) * ex / Lop
    t = lam * np.abs(w) / kappa; T = t.sum()
    if T > k - 1 or t.max() > 1: return ('infeasible', T, t.max())
    z = np.zeros(p); z[S] = 1 - (1 + T) / k; z[j] = 1.0; z[Vp] = t
    beta = np.zeros(p); beta[S] = bS; beta[Vp] = w
    obj = np.sum((y - X @ beta) ** 2) + lam * np.sum(beta[S] ** 2 / z[S]) + lam * np.sum(w ** 2 / t)
    bound = fS + lam * bplus ** 2 * (1 + (1 + T) ** 2 / (k - 1 - T)) - (2 * s - s * s) * Q / Lop
    return obj, bound, fS, len(Vp), T, s
for (p, k, alpha, seed) in [(400, 8, 1.0, 1000), (400, 8, 1.0, 1001), (400, 20, 0.8, 1002), (1000, 30, 0.8, 1003)]:
    n = int(round(alpha * k * np.log(p)))
    X, y, lam, S = instance(n, p, k, seed=seed, tau0=1.5)
    j = [l for l in range(p) if l not in S][0]
    res = construction(X, y, lam, k, S, j)
    LB, val, z, a = solve_node(X, y, lam, k, (), (j,))
    print(p, k, n, 'construction obj %.3f  analytic bound %.3f  f(S*) %.3f  |V\'|=%d T=%.2f s=%.2f' % res if res and res[0] != 'infeasible' else res,
          '| exact node value %.3f' % val)
