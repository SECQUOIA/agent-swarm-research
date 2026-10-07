"""Refined scan of z_K/z_1,A along the edges of the cost simplex at the Theorem 14 corner
(complements factor_scan.py).  Usage: python3 factor_edge.py OUT.jsonl"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import sys, json, warnings
import numpy as np
warnings.filterwarnings('ignore')
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260928b/sfree/code'))
import core
from orbit_lib import corner_bound
sb = np.array([-4.5, 0, 1.5])
P = np.column_stack([np.array(v) - sb for v in ([-1, -6, 18], [-5, 6, -18], [0, 2.5, 2.5])])
out = open(sys.argv[1], 'w')
eps = 1e-6
for edge in range(3):
    for t in np.linspace(0.01, 0.99, 99):
        w = np.full(3, eps)
        a, b = [k for k in range(3) if k != edge]
        w[a], w[b] = t, 1 - t
        zK, lamK = corner_bound(sb, P, w)
        c1, h1, F = core.best_orbit_bound('+', sb, P, w, zK, iters=40)
        out.write(json.dumps(dict(w=w.tolist(), zK=float(zK), z1A=float(c1), ratio=float(zK / c1) if c1 > 0 else None,
                                  lamK=np.round(lamK, 6).tolist())) + '\n'); out.flush()
