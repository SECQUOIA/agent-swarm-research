"""From the same LP state, compare the vertex reached after one SCIP-rule round and after one
orbit-rule round: pointedness gamma of its basis cone, zero reduced costs, total violation of
the bilinear terms, and the LP gain.  Usage: python3 analyze_swapgamma.py 'GLOB'"""
import sys, glob, json, collections
import recio
import numpy as np
from scipy import stats
BUCK = [(0, 0), (1, 2), (3, 5), (6, 10), (11, 19)]
D = collections.defaultdict(lambda: [[] for _ in BUCK])
for f in recio.files(sys.argv[1]):
    for line in recio.lines(f):
        r = json.loads(line); gap = r['zbil'] - r['zlp']
        for x in r['rounds']:
            if 'swapgamma_scip' not in x or 'swapgamma_orbit' not in x:
                continue
            b = [i for i, (a, z) in enumerate(BUCK) if a <= x['r'] <= z][0]
            D[r['rule']][b].append(dict(lg=np.log10(max(x['swapgamma_orbit'], 1e-12)) - np.log10(max(x['swapgamma_scip'], 1e-12)),
                                        nz=(x['swapnzero_orbit'] > 0) - (x['swapnzero_scip'] > 0),
                                        nzo=x['swapnzero_orbit'] > 0, nzs=x['swapnzero_scip'] > 0,
                                        vi=x['swapviol_orbit'] - x['swapviol_scip'],
                                        vrel=np.log10(max(x['swapviol_orbit'], 1e-12)) - np.log10(max(x['swapviol_scip'], 1e-12)),
                                        g=(x['swap_orbit'] - x['swap_scip']) / gap))
for rule, B in D.items():
    print('states on the %s trajectory' % rule)
    for b, L in enumerate(B):
        if not L:
            continue
        lg = np.array([d['lg'] for d in L]); vr = np.array([d['vrel'] for d in L]); g = np.array([d['g'] for d in L])
        p1 = stats.wilcoxon(lg).pvalue if np.any(lg != 0) else 1.0
        p2 = stats.wilcoxon(vr).pvalue if np.any(vr != 0) else 1.0
        print('  r%d-%d n=%3d  log10 gamma(orbit)-log10 gamma(scip): mean %+.3f median %+.3f (Wilcoxon p %.2g) | '
              'zero red. cost after orbit %.2f, after scip %.2f | log10 viol ratio median %+.3f (p %.2g) | gain orbit-scip mean %+.4f'
              % (BUCK[b][0], BUCK[b][1], len(L), lg.mean(), np.median(lg), p1, np.mean([d['nzo'] for d in L]),
                 np.mean([d['nzs'] for d in L]), np.median(vr), p2, g.mean()))
