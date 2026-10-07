"""Discovery: separate PSD moment points (mixtures of atoms partly outside the
cube) from H3plus; test each separating extreme ray for membership in the
cone dual to R.  Numerical only."""
import sys, json, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from cube3 import *
from sdp3 import *
from zero_pattern import pattern

seed = int(sys.argv[1]); n = int(sys.argv[2]); spread = float(sys.argv[3])
rng = np.random.default_rng(seed)
S = Separation(); R1 = Relaxation(use_family=True); R0 = Relaxation(use_family=False)
def mom(x): return np.array([1, x[0], x[1], x[2], x[0]**2, x[1]**2, x[2]**2, x[0]*x[1], x[0]*x[2], x[1]*x[2]])
out = []; t0 = time.time(); miss = 0; notd3 = 0
for it in range(n):
    k = rng.integers(3, 9)
    pts = rng.random((k, 3))
    # snap some coordinates to the boundary, push a few slightly outside
    snap = rng.random((k, 3)) < 0.5
    pts[snap] = np.round(pts[snap])
    out_mask = rng.random((k, 3)) < 0.15
    pts[out_mask] += rng.normal(0, spread, out_mask.sum())
    wts = rng.random(k) + 0.1
    w = sum(a * mom(x) for a, x in zip(wts, pts)) / wts.sum()
    try:
        sv, st, p = S.solve(w)
        if p is None: continue
        p = p / np.abs(p).max()
        r1 = R1.solve(p)[0]; r0 = R0.solve(p)[0]
    except Exception as e:
        continue
    rec = dict(p=p.tolist(), sep=sv, r1=r1, r0=r0)
    out.append(rec)
    if r0 < -1e-6: notd3 += 1
    if r1 < -1e-6:
        miss += 1
        pat, z = pattern(p, 1e-5)
        print('MISSING', it, 'r1', r1, 'r0', r0, 'pattern', pat, np.round(p, 4).tolist(), flush=True)
print('n', len(out), 'not in D3', notd3, 'missing', miss, 'time', time.time() - t0)
json.dump(out, open(f'../logs/explore_psd_{seed}_{spread}.json', 'w'))
