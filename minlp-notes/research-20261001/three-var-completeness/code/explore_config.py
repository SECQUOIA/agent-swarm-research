"""Extreme rays of the face F(B) for a given zero configuration B (random
generic positions), tested for membership in the cone dual to R."""
import sys, json, time, warnings, ast
import numpy as np, cvxpy as cp
warnings.filterwarnings("ignore")
from cube3 import *
from sdp3 import *
from zero_pattern import pattern
from face_explore_generic import FaceSepVar
from blocking2 import rows_for

CONFIGS = {
 'C1': ((-1, 0, 0), (0, -1, 0), (0, 1, -1), (1, 0, 1)),
 'C2': ((-1, 0, 0), (0, 0, 1), (1, -1, 0), (1, 1, -1)),
 'C3': ((-1, 0, 0), (0, 1, 1), (1, -1, 0), (1, 1, -1)),
 'C5': ((-1, 0, 0), (0, -1, 1), (1, -1, 1), (1, 0, -1)),
 'C6': ((-1, 0, 0), (0, -1, 0), (0, 1, -1), (1, 1, 1)),
 'F4': ((-1, 0, 0), (0, -1, 0), (0, 1, -1), (1, 1, -1)),
}
if __name__ == '__main__':
    name = sys.argv[1]; npos = int(sys.argv[2]); per = int(sys.argv[3]); seed = int(sys.argv[4])
    B = CONFIGS[name]
    rng = np.random.default_rng(seed)
    FS = FaceSepVar(12); R1 = Relaxation(use_family=True); R0 = Relaxation(use_family=False)
    out = []; stats = dict(feasible=0, rays=0, notd3=0, missing=0)
    for it in range(npos):
        rows = rows_for(B, rng)
        A = np.zeros((12, 10)); A[:rows.shape[0]] = rows
        FS.A.value = A
        for j in range(per):
            w = rng.normal(size=10)
            try:
                val, st, p = FS.solve(w)
            except Exception:
                break
            if p is None or st not in ('optimal', 'optimal_inaccurate'): break
            if j == 0: stats['feasible'] += 1
            p = p / np.abs(p).max(); stats['rays'] += 1
            r1 = R1.solve(p)[0]; r0 = R0.solve(p)[0]
            if r0 < -1e-7: stats['notd3'] += 1
            rec = dict(p=p.tolist(), r1=r1, r0=r0, p0=p[0])
            out.append(rec)
            if r1 < -1e-7:
                stats['missing'] += 1
                pat, z = pattern(p, 1e-5)
                print('MISSING', name, it, j, 'r1 %.3e r0 %.3e p0 %.3f' % (r1, r0, p[0]), 'zeros', [(s, x) for s, x in z], flush=True)
    print(name, stats, flush=True)
    json.dump(out, open(f'../logs/explore_config_{name}_{seed}.json', 'w'))
