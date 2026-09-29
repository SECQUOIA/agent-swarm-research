"""Direct counterexample to PWE Theorem 2 as stated (per-entry noise N(0, gamma^2), rho = lam = sqrt n):
S* is certified to be the unique optimal support (saturated witness of Prop. 2.3, or exact single-fixing
node solves), while the root relaxation value R is strictly below f(S*) = OPT.
PWE's hypothesis n > c0 (gamma^2 + ||w*||^2)/w_min^2 log d holds with c0 = n / (5.25 log p)."""
from common import ridge_on, node_primal_cvx, saturated_witness, dual_L
import numpy as np

p, k, b, gam = 50, 5, 1.0, 0.5
for n in (500, 5000):
    lam = np.sqrt(n)
    for seed in range(4):
        rng = np.random.default_rng(424242 + seed)
        X = rng.standard_normal((n, p)); S = np.sort(rng.choice(p, k, replace=False))
        beta = np.zeros(p); beta[S] = b * rng.choice([-1.0, 1.0], k)
        y = X @ beta + gam * rng.standard_normal(n)
        fS, bS, r = ridge_on(X, y, lam, S)
        a = X.T @ r; nulls = np.setdiff1d(np.arange(p), S); m0 = np.min(np.abs(a[S]))
        R = node_primal_cvx(X, y, lam, k)[0]
        best = -np.inf
        for th in np.linspace(0.5, 1.0, 51):
            al, Gam, V, _ = saturated_witness(X, y, lam, S, th * m0)
            if len(V) > n - k - 1:
                continue
            c = X.T @ al; m = np.min(np.abs(c[S])); M = np.max(np.abs(c[nulls]))
            if M <= m:
                best = max(best, (m * m - M * M) / lam - Gam)
        how = 'witness' if best > 0 else None
        if how is None:   # exact single-fixing nodes
            vals = [node_primal_cvx(X, y, lam, k, (int(i),), ())[0] for i in S] + \
                   [node_primal_cvx(X, y, lam, k, (), (int(j),))[0] for j in nulls]
            how = 'exact nodes' if min(vals) > fS * (1 + 1e-7) else 'NOT certified'
        print(f"n={n:5d} (c0={n/((gam**2+k*b*b)/b**2*np.log(p)):6.1f}) seed={seed}: PWE cert {np.max(np.abs(a[nulls]))<=m0}, "
              f"max|a_l|/m0={np.max(np.abs(a[nulls]))/m0:.2f}, (f(S*)-R)/f(S*)={(fS-R)/fS:.2e}, S* unique optimum certified by: {how}", flush=True)
