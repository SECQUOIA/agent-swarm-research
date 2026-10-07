"""Numerical scan of z_K(w) / z_1,A(w) over cost directions w at the Theorem 14 corner (Section
6.2 of note.md).  Since z_1,A <= z_1,B and z_1 <= z_cl, the maximum over the scanned w is a
numerical estimate of an upper bound for the closure factor sup_w z_K(w)/z_cl(w) of families
(A) and (B) (not a proof: finite grid, floating-point LMI bisection).

Grid: w on the simplex with step 1/K, each entry replaced by max(entry, eps) for eps in EPS.
Usage: python3 factor_scan.py K OUT.jsonl [--time SEC]
Writes one JSON line per direction; resumes from OUT.jsonl if it exists (skips done points).
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[7])

import sys, os, json, time, argparse, itertools, warnings
import numpy as np
warnings.filterwarnings('ignore')
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260928b/sfree/code'))
import core
from orbit_lib import corner_bound

sb = np.array([-4.5, 0, 1.5])
P = np.column_stack([np.array(v) - sb for v in ([-1, -6, 18], [-5, 6, -18], [0, 2.5, 2.5])])

ap = argparse.ArgumentParser()
ap.add_argument('K', type=int); ap.add_argument('out'); ap.add_argument('--time', type=float, default=3000)
args = ap.parse_args()
done = set()
if os.path.exists(args.out):
    for line in open(args.out):
        d = json.loads(line); done.add(tuple(d['w']))
pts = []
for i, j in itertools.product(range(args.K + 1), repeat=2):
    if i + j <= args.K:
        base = np.array([i, j, args.K - i - j], float) / args.K
        for eps in (1e-3, 1e-6):
            w = np.maximum(base, eps)
            pts.append(tuple(np.round(w / w.sum(), 12)))
pts = sorted(set(pts))
t0 = time.time()
with open(args.out, 'a') as fh:
    for w in pts:
        if w in done:
            continue
        if time.time() - t0 > args.time:
            print('time limit reached; rerun to resume', flush=True)
            break
        wv = np.array(w)
        zK, lamK = corner_bound(sb, P, wv)
        c1, h1, F = core.best_orbit_bound('+', sb, P, wv, zK, iters=40)
        rec = dict(w=list(w), zK=float(zK), z1A=float(c1), z1A_hi=float(h1), ratio=float(zK / c1) if c1 > 0 else None,
                   lamK=np.round(lamK, 6).tolist())
        fh.write(json.dumps(rec) + '\n'); fh.flush()
print('done in %.0f s' % (time.time() - t0))
