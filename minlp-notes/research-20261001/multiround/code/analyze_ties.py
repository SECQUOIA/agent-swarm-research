"""Number of near-binding rays of a cut at its corner: rays j with w_j alpha_j <= (1 + tol) z_C
(tol = 1e-3), where z_C = min_j w_j alpha_j.  Two or more binding rays mean the corner LP after the
cut has an optimal edge (dual degenerate).  Uses the normalized reduced costs stored in the diag
cut records (rounded to 1e-6; rays with w_j < 1e-4 are ignored to avoid rounding ties).
Usage: python3 analyze_ties.py 'GLOB'"""
import sys, glob, json, collections
import recio
import numpy as np
BUCK = [(0, 0), (1, 2), (3, 5), (6, 10), (11, 19)]
T = collections.defaultdict(lambda: [[] for _ in BUCK])
for f in recio.files(sys.argv[1]):
    for line in recio.lines(f):
        r = json.loads(line)
        if r['rule'] not in ('scip', 'orbit'):
            continue
        for c in r.get('cuts', []):
            if 'a_scip' not in c or 'a_orbit' not in c:
                continue
            b = [i for i, (a, z) in enumerate(BUCK) if a <= c['r'] <= z][0]
            w = np.array(c['w'])
            out = {}
            for nm in ('a_scip', 'a_orbit'):
                a = np.array(c[nm]); m = (a > 0) & (w >= 1e-4)
                if not m.any():
                    out[nm] = None; continue
                v = w[m] / a[m]; z = v.min()
                out[nm] = int(np.sum(v <= (1 + 1e-3) * z))
            if out['a_scip'] is not None and out['a_orbit'] is not None:
                T[r['rule']][b].append((out['a_scip'], out['a_orbit']))
for rule, B in T.items():
    print('corners on the %s trajectory' % rule)
    for b, L in enumerate(B):
        if not L:
            continue
        L = np.array(L)
        print('  r%d-%d corners %4d: >= 2 binding rays: SCIP set %.3f, orbit set %.3f; mean binding rays %.2f vs %.2f'
              % (BUCK[b] + (len(L), np.mean(L[:, 0] >= 2), np.mean(L[:, 1] >= 2), L[:, 0].mean(), L[:, 1].mean())))
