"""From the same LP state, compare the vertex reached by one SCIP round and by one orbit round
(swappot records of mrloop.py): potential max_e z_K / (z_bil - z) of the new vertex, number of
normalized reduced costs <= 1e-6 and <= 1e-3, and the LP gain.  Paired over states (Wilcoxon) and
by instance (mean over states, t-interval).  Usage: python3 analyze_swappot.py 'GLOB'"""
import sys, glob, json, collections
import recio
import numpy as np
from scipy import stats
BUCK = [(0, 0), (1, 2), (3, 5), (6, 10), (11, 19)]
for f in recio.files(sys.argv[1]):
    pass
D = collections.defaultdict(lambda: [collections.defaultdict(list) for _ in BUCK])
for f in recio.files(sys.argv[1]):
    for line in recio.lines(f):
        r = json.loads(line); gap = r['zbil'] - r['zlp']
        for x in r['rounds']:
            if 'swappot_scip' not in x or 'swappot_orbit' not in x:
                continue
            ps, po = x['swappot_scip'], x['swappot_orbit']
            if ps['pot'] is None or po['pot'] is None or (r['zbil'] - x['z']) <= 1e-3 * gap:
                continue
            b = [i for i, (a, z) in enumerate(BUCK) if a <= x['r'] <= z][0]
            d = D[r['rule']][b]
            d['inst'].append(r['inst'])
            d['dpot'].append(po['pot'] - ps['pot'])
            d['pot_s'].append(ps['pot']); d['pot_o'].append(po['pot'])
            d['n3_s'].append(ps['n3']); d['n3_o'].append(po['n3'])
            d['n6_s'].append(ps['n6'] > 0); d['n6_o'].append(po['n6'] > 0)
            d['dgain'].append((x['swap_orbit'] - x['swap_scip']) / (r['zbil'] - x['z']))
for rule, B in D.items():
    print('states on the %s trajectory' % rule)
    for b, d in enumerate(B):
        if not d['dpot']:
            continue
        dp = np.array(d['dpot'])
        p = stats.wilcoxon(dp).pvalue if np.any(dp != 0) else 1.0
        # by instance
        per = collections.defaultdict(list)
        for i, v in zip(d['inst'], dp):
            per[i].append(v)
        m = np.array([np.mean(v) for v in per.values()])
        h = stats.t.ppf(0.975, len(m) - 1) * m.std(ddof=1) / np.sqrt(len(m)) if len(m) > 1 else np.nan
        print('  r%d-%d states %3d: potential after SCIP round median %.3f, after orbit round median %.3f; '
              'orbit - SCIP: state median %+.3f (Wilcoxon p %.2g), by instance mean %+.3f [%+.3f,%+.3f] (n %d) | '
              'reduced costs <= 1e-3: mean count %.2f vs %.2f | some <= 1e-6: %.2f vs %.2f | rate gain orbit - SCIP %+.4f'
              % (BUCK[b] + (len(dp), np.median(d['pot_s']), np.median(d['pot_o']), np.median(dp), p, m.mean(), m.mean() - h,
                            m.mean() + h, len(m), np.mean(d['n3_s']), np.mean(d['n3_o']), np.mean(d['n6_s']), np.mean(d['n6_o']),
                            np.mean(d['dgain']))))
