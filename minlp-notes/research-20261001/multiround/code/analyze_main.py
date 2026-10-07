"""Summaries and paired comparisons of loop runs (JSONL records of mrloop.py).
Usage: python3 analyze_main.py 'GLOB' [ROUNDS_TO_SHOW (comma)] [BASELINES (comma)]
Prints, per rule: mean / median fraction of the root gap closed at the chosen rounds, mean
number of cuts, and paired differences rule - baseline with a 95% t-interval and a 95%
percentile bootstrap interval (10000 resamples, fixed seed), plus win/loss counts (> 0.01).
"""
import sys, glob, json, collections
import recio
import numpy as np
from scipy import stats

files = recio.files(sys.argv[1])
SHOW = [int(a) for a in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1, 3, 5, 10, 20]
BASE = sys.argv[3].split(',') if len(sys.argv) > 3 else ['scip', 'orbit']
R = collections.defaultdict(dict)
for f in files:
    for line in recio.lines(f):
        r = json.loads(line)
        R[r['rule']][r['inst']] = r
rules = list(R)
common = sorted(set.intersection(*[set(R[k]) for k in rules]))
print('files %d, rules %d, instances with all rules: %d' % (len(files), len(rules), len(common)))
SHOW = [s for s in SHOW if s < len(R[rules[0]][common[0]]['closed'])]
rng = np.random.default_rng(0)


def ci(d):
    d = np.asarray(d)
    m = d.mean(); h = stats.t.ppf(0.975, len(d) - 1) * d.std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else np.nan
    bs = d[rng.integers(0, len(d), (10000, len(d)))].mean(1)
    return m, m - h, m + h, np.quantile(bs, 0.025), np.quantile(bs, 0.975)


print('\nMean fraction of root gap closed (median in brackets), mean cuts, LP failures')
print('%-11s ' % 'rule' + ' '.join('r%-13d' % s for s in SHOW) + ' cuts   fail')
for k in rules:
    H = np.array([R[k][i]['closed'] for i in common])
    print('%-11s ' % k + ' '.join('%.3f [%.3f] ' % (H[:, s].mean(), np.median(H[:, s])) for s in SHOW)
          + ' %6.1f %d' % (np.mean([R[k][i]['ncuts'] for i in common]), sum(R[k][i]['status'] != 'ok' for i in common)))
for b in BASE:
    if b not in R:
        continue
    print('\nPaired difference rule - %s: mean [95%% t-CI] {bootstrap CI} wins/losses (>0.01)' % b)
    for k in rules:
        if k == b:
            continue
        out = []
        for s in SHOW:
            d = [R[k][i]['closed'][s] - R[b][i]['closed'][s] for i in common]
            m, lo, hi, blo, bhi = ci(d)
            w = sum(x > 0.01 for x in d); l = sum(x < -0.01 for x in d)
            out.append('r%d %+.3f [%+.3f,%+.3f] {%+.3f,%+.3f} %d/%d' % (s, m, lo, hi, blo, bhi, w, l))
        print('%-11s ' % k + ' | '.join(out))
