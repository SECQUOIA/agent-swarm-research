"""Direct checks of the Section 6.3 numbers at p = 3200, k = 5, lam = sqrt n, alpha = 3 (n = 121).
seed 1007: forced-in nodes j = 991 and j = 2714 (column generation to convergence AND the full,
unrestricted dual SOCP), |a_j|/||r||, a_j^2/(n+lam), m0^2/lam, realized tau^2, root gap.
seeds 1000, 1003: root gap and forced-in nodes of the strongest, a median and the weakest null.
usage: python3 p3200_nodes.py SEED [SEED ...]"""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import sys
import numpy as np
from scipy.stats import norm
from rc_common import make_instance, fit, solve_node, node_value_dual_socp

p, k, n = 3200, 5, 121
for seed in [int(s) for s in sys.argv[1:]]:
    X, y, lam, S = make_instance(n, p, k, seed, 'sqrtn')
    fS, bS, r = fit(X, y, lam, S)
    a = X.T @ r
    nulls = np.array([j for j in range(p) if j not in set(S)])
    m0 = lam * np.abs(bS).min()
    rn = np.linalg.norm(r)
    order = nulls[np.argsort(-np.abs(a[nulls]))]
    print("seed %d: n=%d lam=%.4f f(S*)=%.4f tau^2=%.3f m0^2/lam=%.3f" % (seed, n, lam, fS, (m0 / rn) ** 2, m0 ** 2 / lam))
    top = order[0]
    zmax = abs(a[top]) / rn
    print("  strongest null j=%d |a_j|/||r||=%.3f  a_j^2/(n+lam)=%.3f  P(max of %d |N(0,1)| >= that)=%.4f" %
          (top, zmax, a[top] ** 2 / (n + lam), len(nulls), 1 - (1 - 2 * norm.sf(zmax)) ** len(nulls)))
    root = solve_node(X, y, lam, k, W0=S, maxrounds=300)
    print("  root: lb %.4f ub %.4f  gap f(S*)-R = %.3f (%s, %d rounds)" % (root['lb'], root['ub'], fS - root['lb'], root['status'], root['rounds']))
    W0 = set(S) | set(np.nonzero(root['z'] > 1e-7)[0].tolist())
    if seed == 1007:
        js = [991, 2714]
        for j in js:
            print("  j=%d: rank %d among nulls by |a_j|, |a_j|/||r||=%.3f, a_j^2/(n+lam)=%.3f" %
                  (j, int(np.nonzero(order == j)[0][0]) + 1, abs(a[j]) / rn, a[j] ** 2 / (n + lam)))
    else:
        js = [int(order[0]), int(order[len(order) // 2]), int(order[-1])]
    for j in js:
        res = solve_node(X, y, lam, k, (), (j,), W0=W0, maxrounds=300)
        line = "  forced-in j=%d: CG lb %.4f ub %.4f (%s, %d rounds); lb - f(S*) = %.3f" % (
            j, res['lb'], res['ub'], res['status'], res['rounds'], res['lb'] - fS)
        if seed == 1007:
            dv, dlb, _ = node_value_dual_socp(X, y, lam, k, (), (j,))
            line += "; full dual SOCP value %.4f, certified lb at its a %.4f" % (dv, dlb)
        print(line, flush=True)
