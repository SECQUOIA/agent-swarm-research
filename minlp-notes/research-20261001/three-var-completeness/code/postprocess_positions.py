"""Post-process blocking_positions output: at the best positions, maximize
p(0) under the hard contact constraints; for clearly feasible cases, test
the resulting quadratic (and extreme rays of the face) against R."""
import sys, json, glob, warnings
import numpy as np, cvxpy as cp
warnings.filterwarnings("ignore")
from cube3 import *
from sdp3 import *
from blocking_positions import rows_theta
from face_explore_generic import FaceSepVar
from zero_pattern import zeros

S = Separation()
A = cp.Parameter((12, 10))
prob = cp.Problem(cp.Maximize(S.pv[0]), S.prob.constraints + [A @ S.pv == 0])
FS = FaceSepVar(12)
R1 = Relaxation(use_family=True); R0 = Relaxation(use_family=False)
rng = np.random.default_rng(7)
import ast, re
recs = []
for f in sorted(glob.glob('../logs/blocking_positions_*.txt')):
    for line in open(f):
        m = re.match(r'^(\S+) (family-sub|NEW) (\(\(.*\)\)) (\[.*\]) elapsed', line)
        if not m:
            continue
        recs.append(dict(resid=float(m.group(1)), family_sub=(m.group(2) == 'family-sub'),
                         config=ast.literal_eval(m.group(3)), theta=ast.literal_eval(m.group(4))))
print('records', len(recs))
import os
CKPT = '../logs/postprocess_positions.jsonl'
done = set()
if os.path.exists(CKPT):
    for ln in open(CKPT):
        done.add(json.loads(ln)['key'])


def safe(fn, *a):
    try:
        return fn(*a)
    except BaseException as e:  # Clarabel panics derive from BaseException
        if isinstance(e, KeyboardInterrupt):
            raise
        return None


summary = []
for r in recs:
    B = tuple(tuple(s) for s in r['config'])
    if r['resid'] > 1e-6 or r['theta'] is None:
        continue
    key = repr((B, r['theta']))
    if key in done:
        continue
    th = np.array(r['theta'])
    Rm = rows_theta(B, th); Ap = np.zeros((12, 10)); Ap[:Rm.shape[0]] = Rm
    A.value = Ap
    try:
        prob.solve(solver='CLARABEL')
        p0 = prob.value if prob.status in ('optimal', 'optimal_inaccurate') else None
    except BaseException as e:
        if isinstance(e, KeyboardInterrupt):
            raise
        p0 = None
    line = dict(config=B, theta=th.tolist(), resid=r['resid'], maxp0=p0, family_sub=r['family_sub'])
    if p0 is not None and p0 > 1e-4:
        FS.A.value = Ap
        worst = np.inf; worst_d3 = np.inf
        for j in range(6):
            res = safe(FS.solve, rng.normal(size=10))
            if res is None or res[2] is None: continue
            p = res[2] / np.abs(res[2]).max()
            a1 = safe(R1.solve, p); a0 = safe(R0.solve, p)
            if a1 is None or a0 is None: continue
            worst = min(worst, a1[0]); worst_d3 = min(worst_d3, a0[0])
        line.update(min_r1=worst, min_r0=worst_d3)
    summary.append(line)
    with open(CKPT, 'a') as fh:
        fh.write(json.dumps(dict(key=key, **line), default=str) + '\n')
    print(('%.2e' % r['resid']), 'maxp0', None if p0 is None else '%.3g' % p0,
          'min_r1 %.2e' % line.get('min_r1', np.nan), 'min_r0 %.2e' % line.get('min_r0', np.nan),
          'family-sub' if r['family_sub'] else 'NEW', B, np.round(th, 3).tolist(), flush=True)
json.dump(summary, open('../logs/postprocess_positions.json', 'w'), default=str)
