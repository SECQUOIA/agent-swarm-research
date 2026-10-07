"""Evaluate the snapped catmix primal rigorously (writes logs/catmixN_primal_snap.{json,txt}).

This is the step that produced logs/catmix800_primal_snap.json/.txt in wave 2. It was run
as an inline python snippet and is saved here so that it can be rerun. Run from explore/
after catmix_primal_snap.py:  python3 catmix_primal_snap_eval.py 800
"""
import json
import sys

import mpmath as mp
import numpy as np

sys.path.insert(0, '..')
import catmix_model as cmx
import catmix_primal as cp

N = int(sys.argv[1])
m, K = cmx.extract(N)
u = np.load('../logs/catmix%d_u_snap.npy' % N)
Jiv = cp.exact_objective_enclosure(K, u)
X, obj_d, viol_d, bviol = cp.double_vector_check(N, m, K, u)
out = dict(N=N, source='catmix%d_u_snap.npy (catmix%d_u.npy with controls < 2e-3 set to 0, then L-BFGS-B)' % (N, N),
           exact_point_objective_enclosure=[mp.nstr(Jiv.a, 20), mp.nstr(Jiv.b, 20)], double_vector_objective=obj_d,
           double_vector_max_row_violation=viol_d, double_vector_bound_violation=bviol)
print(json.dumps(out, indent=1))
json.dump(out, open('../logs/catmix%d_primal_snap.json' % N, 'w'), indent=1)
open('../logs/catmix%d_primal_snap.txt' % N, 'w').write('\n'.join(repr(v) for v in X) + '\n')
