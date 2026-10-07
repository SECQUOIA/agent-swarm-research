"""Pooled paired comparison with SCIP's rule over all four sizes (220 instances), for the rules
run on every size.  Columns: mean difference (rule - scip) of the fraction of the root gap closed
after rounds 1, 3, 10, 20 and of the mean over rounds 1..10 ("AUC"), with 95% t-intervals; Holm-
adjusted p-values (paired t-test) for round 10 and AUC across the listed rules.
Usage: python3 analyze_pooled.py"""
import glob, json, collections
import numpy as np
from scipy import stats

R = collections.defaultdict(dict)
for size in ('4x4', '6x8', '8x12', '10x20'):
    for f in sorted(glob.glob('../logs/main/main_%s_*.jsonl' % size)) + sorted(glob.glob('../logs/new/new_%s_*.jsonl' % size)):
        for line in open(f):
            r = json.loads(line)
            R[r['rule']][(size, r['inst'])] = np.array(r['closed'])
S = R['scip']
rules = [k for k in R if k != 'scip' and set(S) <= set(R[k])]
rows, praw = [], {}
for k in rules:
    ids = sorted(S)
    cells = []
    for name, f in (('r1', lambda h: h[1]), ('r3', lambda h: h[3]), ('r10', lambda h: h[10]), ('r20', lambda h: h[20]),
                    ('AUC', lambda h: h[1:11].mean())):
        d = np.array([f(R[k][i]) - f(S[i]) for i in ids])
        h = stats.t.ppf(0.975, len(d) - 1) * d.std(ddof=1) / np.sqrt(len(d))
        cells.append('%+.4f [%+.4f,%+.4f]' % (d.mean(), d.mean() - h, d.mean() + h))
        if name in ('r10', 'AUC'):
            praw[(k, name)] = stats.ttest_1samp(d, 0.0).pvalue
    rows.append((k, cells))


def holm(keys):
    ps = sorted((praw[k], k) for k in keys)
    m = len(ps); out = {}; run = 0.0
    for i, (p, k) in enumerate(ps):
        run = max(run, min(1.0, (m - i) * p)); out[k] = run
    return out


H10 = holm([(k, 'r10') for k in rules]); HA = holm([(k, 'AUC') for k in rules])
print('pooled over %d instances (4x4: 60, 6x8: 60, 8x12: 50, 10x20: 50)' % len(S))
print('%-11s %-24s %-24s %-24s %-24s %-24s %s' % ('rule', 'r1', 'r3', 'r10', 'r20', 'AUC r1-10', 'Holm p (r10, AUC)'))
for k, c in rows:
    print('%-11s %-24s %-24s %-24s %-24s %-24s %.3g, %.3g' % ((k,) + tuple(c) + (H10[(k, 'r10')], HA[(k, 'AUC')])))
