"""Discovery: random extreme rays of P3plus tested for membership in the
closure of D3 + family copies (dual of R).  Numerical only."""
import sys, json, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from cube3 import *
from sdp3 import *

seed = int(sys.argv[1]); n = int(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else 'gauss'
rng = np.random.default_rng(seed)
S = Separation(); R1 = Relaxation(use_family=True); R0 = Relaxation(use_family=False)
out = []
t = time.time()
for it in range(n):
    if mode == 'gauss':
        w = rng.normal(size=10); w[0] = rng.normal()
    elif mode == 'atoms':
        # moments of a random small signed combination of cube atoms
        k = rng.integers(2, 7)
        pts = rng.random((k, 3)); pts[rng.random((k,3)) < 0.4] = np.round(pts[rng.random((k,3)) < 0.4]) if False else pts[rng.random((k,3)) < 0.4]
        wts = rng.normal(size=k)
        w = np.zeros(10)
        for x, a in zip(pts, wts):
            w += a * np.array([1, x[0], x[1], x[2], x[0]**2, x[1]**2, x[2]**2, x[0]*x[1], x[0]*x[2], x[1]*x[2]])
    val, st, p = S.solve(w)
    if p is None or st not in ('optimal', 'optimal_inaccurate'):
        continue
    p = p / np.abs(p).max()
    r1 = R1.solve(p)[0]; r0 = R0.solve(p)[0]
    cm = cube_min(p)
    out.append(dict(p=p.tolist(), r_family=r1, r_d3=r0, cube_min=cm, status=st))
    if r1 < -1e-6:
        print('MISSING', it, r1, r0, cm, np.round(p, 5).tolist(), flush=True)
print('done', len(out), 'time', time.time() - t, 'missing', sum(o['r_family'] < -1e-6 for o in out),
      'not in D3', sum(o['r_d3'] < -1e-6 for o in out))
json.dump(out, open(f'../logs/explore_random_{mode}_{seed}.json', 'w'))
