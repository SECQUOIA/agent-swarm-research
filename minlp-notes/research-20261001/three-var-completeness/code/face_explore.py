"""Discovery: extreme rays of faces of P3plus defined by prescribed edge
contacts.  Default configuration T2: contacts on the monotone path
0 -x- e1 -y- e1+e2 -z- 1.  Each extreme ray of the face is an extreme ray of
P3plus; we test it for membership in the cone dual to R."""
import sys, json, time, warnings
import numpy as np
import cvxpy as cp
warnings.filterwarnings("ignore")
from cube3 import *
from sdp3 import *
from zero_pattern import pattern

def mono(k): return k
def lin_value(point):
    x = point
    return np.array([1, x[0], x[1], x[2], x[0]**2, x[1]**2, x[2]**2, x[0]*x[1], x[0]*x[2], x[1]*x[2]])
def lin_deriv(point, i):
    x = list(point); g = np.zeros(10)
    g[1 + i] = 1; g[4 + i] = 2 * x[i]
    pairs = {(0,1): 7, (0,2): 8, (1,2): 9}
    for (a, b), idx in pairs.items():
        if a == i: g[idx] = x[b]
        if b == i: g[idx] = x[a]
    return g

class FaceSep(Separation):
    def __init__(self, nrows):
        super().__init__()
        self.A = cp.Parameter((nrows, 10))
        cons = self.prob.constraints + [self.A @ self.pv == 0]
        self.prob = cp.Problem(self.prob.objective, cons)

EDGES_T2 = [((None, 0, 0), 0), ((1, None, 0), 1), ((1, 1, None), 2)]  # (point template, direction)

def contact_rows(contacts):
    rows = []
    for pt, i in contacts:
        rows.append(lin_value(pt)); rows.append(lin_deriv(pt, i))
    return np.array(rows)

if __name__ == '__main__':
    seed = int(sys.argv[1]); n = int(sys.argv[2]); per = int(sys.argv[3])
    rng = np.random.default_rng(seed)
    FS = FaceSep(6); R1 = Relaxation(use_family=True); R0 = Relaxation(use_family=False)
    found = []; allvals = []; stats = dict(feasible=0, rays=0, notd3=0, missing=0)
    t0 = time.time()
    for it in range(n):
        ts = rng.uniform(0.05, 0.95, 3)
        contacts = []
        for (tmpl, i), t in zip(EDGES_T2, ts):
            pt = [t if v is None else v for v in tmpl]
            contacts.append((pt, i))
        FS.A.value = contact_rows(contacts)
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
                found.append(dict(ts=ts.tolist(), p=p.tolist(), r1=r1, r0=r0, zeros=[(list(s), list(x)) for s, x in z]))
                print('MISSING', it, j, 'ts', np.round(ts, 3).tolist(), 'r1', r1, 'r0', r0, 'pattern', pat, flush=True)
    print(stats, 'time', time.time() - t0, flush=True)
    json.dump(dict(found=found, vals=allvals, stats=stats), open(f'../logs/face_explore_T2_{seed}.json', 'w'))
