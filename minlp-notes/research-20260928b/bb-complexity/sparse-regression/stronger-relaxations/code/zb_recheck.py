"""Re-solve zb with Clarabel on the disputed pure-noise instance of Table 7.3 (k = 6, alpha = 2, seed 3002)
and report status and relative gap to the stored OPT; the stored value was from SCS (eps 1e-6)."""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import json, time
import cvxpy as cp
import relax
from relax import instance

r = [json.loads(l) for l in open('../data/hardzb.jsonl') if json.loads(l)['k'] == 6 and json.loads(l)['alpha'] == 2.0 and json.loads(l)['seed'] == 3002][0]
X, y, _, S = instance(r['n'], r['p'], r['k'], b=0.0, sigma=0.5, seed=r['seed'], lam=r['lam'])
orig = relax._solve
status = {}
def spy(prob, solver="CLARABEL"):
    v = orig(prob, solver); status['s'] = prob.status; return v
relax._solve = spy
t = time.time(); v = relax.zb(X, y, r['lam'], r['k'])
print(json.dumps(dict(k=6, alpha=2.0, seed=3002, OPT=r['opt'], zb_scs=r['zb'], rel_scs=(r['opt'] - r['zb']) / r['opt'],
                      zb_clarabel=v, rel_clarabel=(r['opt'] - v) / r['opt'], status=status.get('s'), time=time.time() - t)))
