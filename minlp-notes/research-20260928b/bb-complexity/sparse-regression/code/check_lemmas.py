"""Numerical checks of the deterministic lemmas in phase-transition.md."""
import numpy as np
from core import instance, ridge, g_val, solve_node, dual_bound
from hard import g_mid
rng = np.random.default_rng(5)
worst = {}
def upd(key, v): worst[key] = max(worst.get(key, 0.0), abs(v))
for trial in range(30):
    n, p, k = int(rng.integers(20, 60)), int(rng.integers(30, 90)), int(rng.integers(2, 7))
    X, y, lam, S = instance(n, p, k, seed=trial, tau0=1.0)
    S = list(S); XS = X[:, S]; G = XS.T @ XS
    fS, bS, r = ridge(X, y, lam, S)
    Minv = np.linalg.inv(np.eye(n) + XS @ XS.T / lam)
    # Lemma 2.3: h(alpha,1_S) = f(S) - u^T H u, X_V^T alpha = a_V - H u
    V = [j for j in range(p) if j not in S][:int(rng.integers(1, 8))]
    XV = X[:, V]; H = XV.T @ Minv @ XV; u = rng.standard_normal(len(V))
    al = r - Minv @ XV @ u
    h = 2 * al @ y - al @ al - np.sum((XS.T @ al) ** 2) / lam
    upd('witness identity', (h - (fS - u @ H @ u)) / fS)
    upd('c_V identity', np.max(np.abs(XV.T @ al - (XV.T @ r - H @ u))))
    # beta^S = X_S^T r / lam
    upd('beta=X^T r/lam', np.max(np.abs(bS - XS.T @ r / lam)))
    # midpoint formula vs g at z=(1_S+1_T)/2, and inequality (b)
    T = list(rng.choice(p, k, replace=False))
    z = np.zeros(p); z[S] += 0.5; z[T] += 0.5
    gz, _ = g_val(X, y, lam, z)
    upd('midpoint formula', (gz - g_mid(X, y, lam, S, T)) / gz)
    fT, bT, rT = ridge(X, y, lam, T)
    bSf = np.zeros(p); bSf[S] = bS; bTf = np.zeros(p); bTf[T] = bT
    C = list(set(S) & set(T))
    rhs = (fS + fT) / 2 - np.sum((X @ (bSf - bTf)) ** 2) / 4 - lam * np.sum((bSf[C] - bTf[C]) ** 2) / 4
    worst['midpoint ineq violation'] = max(worst.get('midpoint ineq violation', 0), (gz - rhs) / fS)
    # f_{2 lam}(S u T) upper bound
    U = sorted(set(S) | set(T)); f2 = ridge(X, y, 2 * lam, U)[0]
    worst['g(mid) - f_2lam(U)'] = max(worst.get('g(mid) - f_2lam(U)', -1e9), (gz - f2) / fS)
    # dual bound validity at a random alpha for a random node
    j = [x for x in range(p) if x not in S][0]
    LB, val, zz, aa = solve_node(X, y, lam, k, (), (j,))
    a_rand = r + 0.3 * rng.standard_normal(n)
    worst['dual bound - node value (should be <=0)'] = max(worst.get('dual bound - node value (should be <=0)', -1e9),
                                                         (dual_bound(X, y, lam, k, a_rand, (), (j,)) - val) / fS)
for kk, v in worst.items(): print("%-45s %.3e" % (kk, v))
