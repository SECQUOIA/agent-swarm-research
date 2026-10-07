"""Discovery: points y0 in R0 (D3 only) outside the hull, obtained by
minimizing a family member over R0, are projected onto R (D3 + family);
the projection is separated exactly from H3plus."""
import sys, json, time, warnings
import numpy as np, cvxpy as cp
warnings.filterwarnings("ignore")
from cube3 import *
from sdp3 import *

seed = int(sys.argv[1]); n = int(sys.argv[2]); metric = sys.argv[3]; PERT = float(sys.argv[4])
rng = np.random.default_rng(seed)
R0 = Relaxation(use_family=False); S = Separation()
y, cons = relaxation_constraints(True, True)
y0 = cp.Parameter(10)
yq = cp.hstack([y[MINDEX[k]] for k in QKEYS])
W = cp.Parameter(10, nonneg=True)
obj = cp.sum_squares(cp.multiply(W, yq - y0)) if metric == 'l2' else cp.norm1(cp.multiply(W, yq - y0))
proj = cp.Problem(cp.Minimize(obj), cons)
found = []; t0 = time.time()
for it in range(n):
    d1, d2 = rng.uniform(0.3, 2, 2); h = rng.uniform(0.05, 0.95) * min(d1, d2)
    k = rng.uniform(0.05, 2); D = d1 + d2 - h; d3 = (D + k) * rng.uniform(1.05, 3)
    q = compose(family_member(h, d1, d2, d3, k), GROUP[rng.integers(48)])
    qv = vector_from_quad(q); qv /= np.abs(qv).max()
    # perturb the objective so that y0 is a generic point of R0 outside the hull
    qv2 = qv + PERT * rng.normal(size=10) * np.abs(qv).mean(); qv2[4:7] = np.abs(qv2[4:7])
    try:
        v0, st0, yy = R0.solve(qv2)
        y0.value = np.array([yy[MINDEX[k]] for k in QKEYS])
        W.value = rng.uniform(0.2, 1.0, 10); W.value[0] = 1
        proj.solve(**SOLVER_OPTS)
        ys = np.array(yq.value)
        sv, sst, p = S.solve(ys)
        s0, _, _ = S.solve(y0.value)
    except Exception as e:
        continue
    if sv < -1e-6:
        p = p / np.abs(p).max()
        found.append(dict(it=it, sep=sv, sep_y0=s0, p=p.tolist(), y=ys.tolist()))
        print('FOUND', it, 'sep(y*)', sv, 'sep(y0)', s0, np.round(p, 4).tolist(), flush=True)
    if it % 50 == 0: print('progress', it, 'last sep(y0)', s0, 'sep(y*)', sv, flush=True)
print('n', n, 'found', len(found), 'time', time.time() - t0)
json.dump(found, open(f'../logs/project_probe_{metric}_{seed}_{PERT}.json', 'w'))
