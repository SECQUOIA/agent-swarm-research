"""Discovery: random contact configurations (edge, facet and vertex zeros at
random positions); explore extreme rays of the resulting face of P3plus and
test them for membership in the cone dual to R.  Numerical only."""
import sys, json, time, warnings
import numpy as np
import cvxpy as cp
warnings.filterwarnings("ignore")
from cube3 import *
from sdp3 import *
from zero_pattern import pattern
from face_explore import lin_value, lin_deriv

class FaceSepVar(Separation):
    def __init__(self, maxrows=10):
        super().__init__()
        self.A = cp.Parameter((maxrows, 10))
        cons = self.prob.constraints + [self.A @ self.pv == 0]
        self.prob = cp.Problem(self.prob.objective, cons)

def random_config(rng, ne, nf, nv):
    rows = []; desc = []
    edges = [(i, fix) for i in range(3) for fix in product((0, 1), repeat=2)]
    for idx in rng.choice(len(edges), ne, replace=False):
        i, fix = edges[idx]; pt = [0.0] * 3; others = [j for j in range(3) if j != i]
        pt[others[0]], pt[others[1]] = fix; pt[i] = rng.uniform(0.05, 0.95)
        rows += [lin_value(pt), lin_deriv(pt, i)]; desc.append(('E', i, fix, pt[i]))
    facets = [(j, v) for j in range(3) for v in (0, 1)]
    for idx in rng.choice(6, nf, replace=False):
        j, v = facets[idx]; pt = list(rng.uniform(0.05, 0.95, 3)); pt[j] = v
        rows += [lin_value(pt)] + [lin_deriv(pt, i) for i in range(3) if i != j]; desc.append(('F', j, v, pt))
    verts = list(product((0, 1), repeat=3))
    for idx in rng.choice(8, nv, replace=False):
        rows += [lin_value(verts[idx])]; desc.append(('V', verts[idx]))
    return np.array(rows), desc

if __name__ == '__main__':
    seed = int(sys.argv[1]); n = int(sys.argv[2]); per = int(sys.argv[3])
    rng = np.random.default_rng(seed)
    FS = FaceSepVar(10); R1 = Relaxation(use_family=True); R0 = Relaxation(use_family=False)
    found = []; allvals = []; stats = dict(tried=0, feasible=0, rays=0, notd3=0, missing=0)
    t0 = time.time()
    choices = [(4,0,0),(3,0,1),(3,0,2),(2,1,0),(2,0,2),(2,0,3),(1,1,1),(1,1,2),(0,2,0),(0,2,1),(1,2,0),(3,1,0),(2,1,1),(0,1,3),(1,0,4),(4,0,1)]
    for it in range(n):
        ne, nf, nv = choices[rng.integers(len(choices))]
        A, desc = random_config(rng, ne, nf, nv)
        if A.shape[0] > 9: continue
        stats['tried'] += 1
        Ap = np.zeros((10, 10)); Ap[:A.shape[0]] = A
        FS.A.value = Ap
        for j in range(per):
            w = rng.normal(size=10)
            try:
                val, st, p = FS.solve(w)
            except Exception:
                break
            if p is None or st not in ('optimal', 'optimal_inaccurate'):
                break
            if j == 0: stats['feasible'] += 1
            p = p / np.abs(p).max(); stats['rays'] += 1
            try:
                r1 = R1.solve(p)[0]; r0 = R0.solve(p)[0]
            except Exception:
                continue
            allvals.append((float(r1), float(r0)))
            if r0 < -1e-6: stats['notd3'] += 1
            if r1 < -1e-6:
                stats['missing'] += 1
                pat, z = pattern(p, 1e-5)
                found.append(dict(desc=str(desc), p=p.tolist(), r1=r1, r0=r0, zeros=[(list(s), list(x)) for s, x in z]))
                print('MISSING', it, j, (ne, nf, nv), 'r1', r1, 'r0', r0, 'pattern', pat, np.round(p, 4).tolist(), flush=True)
    print(stats, 'time', time.time() - t0, flush=True)
    json.dump(dict(found=found, vals=allvals, stats=stats), open(f'../logs/face_explore_generic_{seed}.json', 'w'))
