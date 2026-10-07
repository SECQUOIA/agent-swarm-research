"""Key table per instance size: mean fraction of the root gap closed after rounds 1, 3, 10, 20,
paired difference to SCIP's rule after rounds 3, 10, 20 (mean and 95% t-interval), wins/losses
(> 0.01), mean cuts and median seconds per instance run (wall clock on a shared machine; rough).
Usage: python3 analyze_key.py SIZE   (reads ../logs/main/main_SIZE_*.jsonl and ../logs/new/new_SIZE_*.jsonl)"""
import sys, glob, json, collections
import numpy as np
from scipy import stats

size = sys.argv[1]
R = collections.defaultdict(dict)
for f in sorted(glob.glob('../logs/main/main_%s_*.jsonl' % size)) + sorted(glob.glob('../logs/new/new_%s_*.jsonl' % size)):
    for line in open(f):
        r = json.loads(line)
        R[r['rule']][r['inst']] = r
S = R['scip']
print('size %s; instances with SCIP rule: %d' % (size, len(S)))
print('%-11s %3s  %-6s %-6s %-6s %-6s | %-24s %-24s %-24s | %-7s %-7s %6s %6s' % (
    'rule', 'n', 'r1', 'r3', 'r10', 'r20', 'r3 - scip', 'r10 - scip', 'r20 - scip', 'W/L r10', 'W/L r20', 'cuts', 'sec'))
for k in R:
    ids = sorted(set(R[k]) & set(S))
    H = np.array([R[k][i]['closed'] for i in ids])
    cells = []
    wl = []
    for s in (3, 10, 20):
        d = np.array([R[k][i]['closed'][s] - S[i]['closed'][s] for i in ids])
        h = stats.t.ppf(0.975, len(d) - 1) * d.std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else np.nan
        cells.append('%+.3f [%+.3f,%+.3f]' % (d.mean(), d.mean() - h, d.mean() + h) if k != 'scip' else '-')
        if s in (10, 20):
            wl.append('%d/%d' % (int(np.sum(d > 0.01)), int(np.sum(d < -0.01))))
    print('%-11s %3d  %.3f  %.3f  %.3f  %.3f  | %-24s %-24s %-24s | %-7s %-7s %6.1f %6.1f' % (
        k, len(ids), H[:, 1].mean(), H[:, 3].mean(), H[:, 10].mean(), H[:, 20].mean(), cells[0], cells[1], cells[2],
        wl[0], wl[1], np.mean([R[k][i]['ncuts'] for i in ids]), np.median([R[k][i]['seconds'] for i in ids])))
