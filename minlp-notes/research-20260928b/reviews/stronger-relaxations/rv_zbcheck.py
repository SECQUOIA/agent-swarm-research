"""Check 8: the pure-noise run k = 6, alpha = 2, seed 3002, whose stored zb (SCS, eps 1e-6) exceeds OPT by 3.3e-5
relative and is counted "exact" in Table 7.3.  Re-solve zb (vectorized model) with Clarabel at two tolerance
settings and report solver status, so that the sign of OPT - zb can be judged."""
import os as _os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    _os.environ[_v] = "1"
import os, json
import numpy as np
import cvxpy as cp
import rv_common
from rv_common import gen_core

HERE = os.path.dirname(os.path.abspath(__file__))
k, alpha, seed = 6, 2.0, 3002
row = None
for l in open(os.path.join(HERE, '..', '..', 'bb-complexity', 'sparse-regression', 'data', 'hard_k3-8.jsonl')):
    r = json.loads(l)
    if r['b'] == 0.0 and r['k'] == k and float(r['alpha']) == alpha and r['seed'] == seed:
        row = r
X, y, _, _ = gen_core(row['n'], row['p'], k, b=0.0, sigma=0.5, seed=seed, lam=row['lam'])
OPT = row['opt']
for label, opts in [('clarabel default', {}), ('clarabel 1e-10', dict(tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10, max_iter=1000))]:
    captured = {}
    orig = cp.Problem.solve

    def solve(self, *a, **kw):
        kw = dict(solver=cp.CLARABEL, **opts)
        out = orig(self, **kw)
        captured['status'] = self.status
        captured['iters'] = self.solver_stats.num_iters
        return out
    cp.Problem.solve = solve
    v = rv_common.zb_vec(X, y, row['lam'], k)
    cp.Problem.solve = orig
    print(json.dumps(dict(setting=label, zb=v, OPT=OPT, relgap=(OPT - v) / OPT, **captured)), flush=True)
