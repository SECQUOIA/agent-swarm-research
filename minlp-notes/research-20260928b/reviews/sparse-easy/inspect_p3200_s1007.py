"""Inspect the p = 3200, seed 1007 run of Table 6.3 (lam = sqrt n, k = 5, n = 121), reported as 'capped'."""
from verify_cg import author_instance, all_single_bounds, solve_node_cg
from common import ridge_on, node_primal_cvx, dual_L, saturated_witness
import numpy as np, itertools
n, p, k = 121, 3200, 5
X, y, lam, S = author_instance(n, p, k, 'sqrtn', 1007)
fS, bS, r = ridge_on(X, y, lam, S)
a = X.T @ r; nulls = np.setdiff1d(np.arange(p), S); m0 = np.min(np.abs(a[S]))
print('f(S*) =', fS, 'beta^S =', np.round(bS, 3), 'tau^2 =', (m0 / np.linalg.norm(r)) ** 2)
# weakest forced-in nodes under the root-optimal dual
stR, vR, LR, resR, _ = solve_node_cg(X, y, lam, k, (), (), None, r, S, max_rounds=80)
rem, frc = all_single_bounds(X, y, lam, k, resR, S, nulls)
order = np.argsort(frc)[:8]
print('root value', vR, 'root LB', LR)
for t in order:
    j = int(nulls[t])
    st, v, L, res, rounds = solve_node_cg(X, y, lam, k, (), (j,), fS, resR, S, max_rounds=80)
    print(f'  forced-in j={j}: |a_j|/m0={abs(a[j])/m0:.2f}, status {st}, restricted UB {v:.4f}, full-node LB {L:.4f}, f(S*)={fS:.4f}')
# full (unrestricted) solve for the first failing node, as an independent check
for t in order:
    j = int(nulls[t])
    v, z, bb, res = node_primal_cvx(X, y, lam, k, (), (j,))
    L = dual_L(X, y, lam, k, res, (), (j,))
    print(f'  FULL SOCP forced-in j={j}: value {v:.4f}, dual bound {L:.4f}, f(S*) - value = {fS - v:.4f}')
    break
# is S* optimal?  one-swap neighbourhood and greedy-from-relaxation supports
best = (fS, tuple(S))
for i in range(k):
    for j in nulls[np.argsort(-np.abs(a[nulls]))[:300]]:
        T = np.sort(np.append(np.delete(S, i), j)); fT = ridge_on(X, y, lam, T)[0]
        if fT < best[0]: best = (fT, tuple(T))
print('best one-swap support value', best[0], 'vs f(S*)', fS, 'S* =', tuple(S), 'best =', best[1])
