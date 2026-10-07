"""Discovery: for valid quadratics p (family members, products, squares),
take the central optimal point y* of min_R <p,y> and separate it exactly from
H3plus.  A negative separation value exhibits a missing valid quadratic."""
import sys, json, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from cube3 import *
from sdp3 import *

seed = int(sys.argv[1]); n = int(sys.argv[2]); kind = sys.argv[3]
rng = np.random.default_rng(seed)
S = Separation(); R = Relaxation(use_family=True)
found = []
t0 = time.time()
for it in range(n):
    if kind == 'family':
        d1, d2 = rng.uniform(0.3, 2, 2); h = rng.uniform(0.05, 0.95) * min(d1, d2)
        k = rng.uniform(0.05, 2); D = d1 + d2 - h; d3 = (D + k) * rng.uniform(1.05, 3)
        p = family_member(h, d1, d2, d3, k)
        g = GROUP[rng.integers(48)]
        p = compose(p, g)
    elif kind == 'familyany':
        h = rng.normal(); d1, d2, d3, k = rng.exponential(1, 4)
        p = compose(family_member(h, d1, d2, d3, k), GROUP[rng.integers(48)])
    elif kind == 'mix':
        # family member plus a small random element of D3-type structure
        d1, d2 = rng.uniform(0.3, 2, 2); h = rng.uniform(0.05, 0.95) * min(d1, d2)
        k = rng.uniform(0.05, 2); D = d1 + d2 - h; d3 = (D + k) * rng.uniform(1.05, 3)
        p = family_member(h, d1, d2, d3, k)
        L = {(0,0,0): rng.normal(), (1,0,0): rng.normal(), (0,1,0): rng.normal(), (0,0,1): rng.normal()}
        p = padd(p, pscale(pmul(L, L), 0.05 * rng.random()))
        p = compose(p, GROUP[rng.integers(48)])
    pv = vector_from_quad(p); pv = pv / np.abs(pv).max()
    try:
        rv, rst, y = R.solve(pv)
        yq = np.array([y[MINDEX[kk]] for kk in QKEYS])
        sv, sst, q = S.solve(yq)
    except Exception as e:
        print('solver error', e); continue
    if sv < -1e-6:
        q = q / np.abs(q).max()
        found.append(dict(it=it, p=pv.tolist(), y=yq.tolist(), sep=sv, q=q.tolist(), rmin_p=rv))
        print('FOUND', it, 'Rmin(p)', rv, 'sep', sv, np.round(q, 4).tolist(), flush=True)
print('n', n, 'found', len(found), 'time', time.time() - t0, flush=True)
json.dump(found, open(f'../logs/face_probe_{kind}_{seed}.json', 'w'))
