"""Self-tests of rc_common.py and a check that the mirrored generator reproduces stored instances.
usage: python3 test_rc.py"""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import json, glob
import numpy as np
from rc_common import (make_instance, fit, g_and_a, node_lb, single_fixing_lbs, solve_node,
                       node_value_dual_socp)

rng = np.random.default_rng(5)
worst = 0.0
for trial in range(4):
    n, p, k = 30, 60, 4
    X = rng.standard_normal((n, p)); y = rng.standard_normal(n); lam = 3.0 + trial
    S = sorted(rng.choice(p, k, replace=False).tolist())
    nulls = [j for j in range(p) if j not in S]
    a = rng.standard_normal(n)
    rem, frc = single_fixing_lbs(X, y, lam, k, a, S, nulls)
    rem2 = [node_lb(X, y, lam, k, a, (i,), ()) for i in S]
    frc2 = [node_lb(X, y, lam, k, a, (), (j,)) for j in nulls]
    worst = max(worst, np.max(np.abs(rem - rem2)), np.max(np.abs(frc - frc2)))
    # node values: CG vs dual SOCP (independent formulation)
    for S0, S1 in [((), ()), ((S[0],), ()), ((), (nulls[3],))]:
        res = solve_node(X, y, lam, k, S0, S1)
        dv, dlb, _ = node_value_dual_socp(X, y, lam, k, S0, S1)
        print("trial %d node S0=%s S1=%s  CG lb %.9f ub %.9f (%s)  dual SOCP %.9f (lb at its a %.9f)" %
              (trial, S0, S1, res['lb'], res['ub'], res['status'], dv, dlb))
    # f(S) three ways
    fS, bS, r = fit(X, y, lam, S)
    z = np.zeros(p); z[S] = 1
    gS, aS = g_and_a(X, y, lam, z)
    print("  f(S) p-side %.12f  n-side %.12f  |X_S'r - lam b| = %.1e" % (fS, gS, np.abs(X[:, S].T @ r - lam * bS).max()))
print("max |vectorized - loop| single-fixing bound: %.2e" % worst)

# generator check against stored instances (fS recorded by the author's runs)
base = '../../bb-complexity/sparse-regression/data/'
checked = 0; maxrel = 0.0
for fn in ['c1_sqrtn_k5.jsonl', 'c1_scaleP_k8_t1.5.jsonl', 'c1_gamma_half_full.jsonl']:
    for i, l in enumerate(open(base + fn)):
        if i % 9: continue
        r = json.loads(l)
        if r['p'] > 1600: continue
        X, y, lam, S = make_instance(r['n'], r['p'], r['k'], r['seed'], r['rule'])
        fS = fit(X, y, lam, S)[0]
        maxrel = max(maxrel, abs(fS - r['fS']) / r['fS'], abs(lam - r['lam']) / r['lam'])
        checked += 1
print("generator: %d stored instances, max relative difference in (f(S*), lam) = %.1e" % (checked, maxrel))
