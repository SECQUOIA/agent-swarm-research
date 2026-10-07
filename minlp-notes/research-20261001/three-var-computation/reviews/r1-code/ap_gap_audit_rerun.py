# Reviewer r1 copy of code/ap_gap_audit.py with output paths moved to reviews/r1-logs/; run from code/ with PYTHONPATH=.
"""Targeted check of the sole AP-variant gap in the existing small-dense logs.

Run from code/: OMP_NUM_THREADS=1 timeout 300 python ap_gap_audit.py
No benchmark batch is rerun. Save the base point and audit all 84 triples.
"""
import copy
import json

import numpy as np

import hullsep
from driver import Runner, summarize
from relax import all_triples, triple_moment_matrices
from small_dense import box_min, build, gen
from spar_audit import family_min

Q, c = gen(9, 75, 586, 'ap')
H, g = -Q, -c
opt, _ = box_min(H, g)
R = build(H, g, '')
res = R.solve('clarabel', tol=1e-10)
T = all_triples(9)
depths = [hullsep.depth(M)[0] for M in triple_moment_matrices(res['xv'], res['Y'], T)]
fam, count = family_min(res['xv'], res['Y'], T)
rec = {'n': 9, 'dens': 75, 'seed': 586, 'variant': 'ap', 'opt': opt,
       'B': res['pobj'], 'B_safe': res['safe'], 'status': res['status'],
       'pinf': res['pinf'], 'min_depth': min(depths),
       'count_depth_lt_1e-6': sum(d < -1e-6 for d in depths),
       'family_stqp_min': fam, 'family_violated_pairs_1e-6': count}
np.savez('../reviews/r1-logs/ap_gap_audit.base.npz', x=res['xv'], Y=res['Y'], depths=depths)
with open('../reviews/r1-logs/ap_gap_audit.json', 'w') as f:
    json.dump(rec, f, indent=2)
print(json.dumps(rec, indent=2))

log = '../reviews/r1-logs/ap_gap_methods.jsonl'
open(log, 'w').close()
run = Runner(R, 'clarabel', log, max_rounds=10, time_budget=60,
             solve_kw={'tol': 1e-10})
run.emit(summarize(res, R, 0.0, 'B', 0))
done = {}
for method in ('K', 'A', 'KA', 'F', 'KAF', 'X'):
    start_R, start_res = done['KA'] if method == 'KAF' else (R, res)
    done[method] = run.run(method, copy.deepcopy(start_R), start_res)
