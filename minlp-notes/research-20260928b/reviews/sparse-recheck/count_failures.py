"""Count ALL failing single fixings at S* for one instance (no early stop), with exact node solves.
Uses the dual-vector pool of rc_common to skip nodes already certified above f(S*).
usage: python3 count_failures.py p k n rule seed"""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import sys
import numpy as np
from rc_common import make_instance, fit, solve_node, single_fixing_lbs

p, k, n, rule, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5])
X, y, lam, S = make_instance(n, p, k, seed, rule)
fS, bS, r = fit(X, y, lam, S)
a0 = X.T @ r
rn = np.linalg.norm(r)
nulls = np.array([j for j in range(p) if j not in set(S)])
rank = {int(j): i + 1 for i, j in enumerate(nulls[np.argsort(-np.abs(a0[nulls]))])}
rem = np.full(k, -np.inf); frc = np.full(len(nulls), -np.inf)
def absorb(a):
    rr, ff = single_fixing_lbs(X, y, lam, k, a, S, nulls)
    np.maximum(rem, rr, out=rem); np.maximum(frc, ff, out=frc)
absorb(r)
root = solve_node(X, y, lam, k, W0=S, maxrounds=300)
absorb(root['a'])
W0 = set(S) | set(np.nonzero(root['z'] > 1e-7)[0].tolist())
done = np.zeros(k + len(nulls), bool)
fails, passes = [], 0
while True:
    allb = np.concatenate([rem, frc]); allb[done] = np.inf
    idx = int(np.argmin(allb))
    if allb[idx] >= fS * (1 + 1e-9):
        break
    S0, S1 = ((S[idx],), ()) if idx < k else ((), (int(nulls[idx - k]),))
    res = solve_node(X, y, lam, k, S0, S1, W0=W0, maxrounds=300)   # to convergence
    absorb(res['a']); done[idx] = True
    if res['ub'] < fS * (1 - 1e-7):
        j = (S0 + S1)[0]
        fails.append((('remove' if S0 else 'force-in'), j, rank.get(j, 0), abs(a0[j]) / rn, res['lb'] - fS, res['ub'] - fS))
    else:
        passes += 1
print("p=%d k=%d n=%d rule=%s seed=%d: f(S*)=%.4f, root gap %.3f, tau^2 %.3f, #nulls with |a_l|>m0: %d" % (
    p, k, n, rule, seed, fS, fS - root['lb'], (lam * np.abs(bS).min() / rn) ** 2,
    int((np.abs(a0[nulls]) > lam * np.abs(bS).min()).sum())))
print("exactly solved nodes: %d passing, %d failing" % (passes, len(fails)))
for f in sorted(fails, key=lambda t: t[4]):
    print("  fail: %s j=%d (null rank %d by |a_j|, |a_j|/||r||=%.3f): node value - f(S*) in [%.4f, %.4f]" % f)
