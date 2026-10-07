"""Revision after review round 2 (issue n1): recovery of the switching rules oKs (orbit in rounds
0..K-1, then SCIP; first_orbit = o1s) and of the orbit rule on 6x8 and 10x20.
For each rule, d(r) = (fraction of the root gap closed by the rule after r rounds) - (same for SCIP),
per instance.  Prints d(r) for r = 3, 5, 10, 20 and the paired changes d(20) - d(3), d(20) - d(5)
and d(20) - d(10) (mean [95% t-interval], t-test p), over the same span for every rule.  A positive
change means that the rule's deficit shrinks (recovery).  After 5 rounds every oKs rule with
K <= 5 has stopped using the orbit set, so the last two spans contain SCIP rounds only (except for
orbit); the span 3..20 contains SCIP rounds only for o1s, o2s and o3s.
Reads logs/main, logs/new, logs/rev1.  Usage: python3 analyze_rev2.py"""
import collections, glob
import numpy as np
from scipy import stats
import recio

SIZES = ('6x8', '10x20')
RULES = ('first_orbit', 'o2s', 'o3s', 'o5s', 'orbit')


def ci(d):
    d = np.asarray(d, float)
    h = stats.t.ppf(0.975, len(d) - 1) * d.std(ddof=1) / np.sqrt(len(d))
    p = stats.ttest_1samp(d, 0.0).pvalue if d.std() > 0 else 1.0
    return '%+.4f [%+.4f, %+.4f] p %.2g' % (d.mean(), d.mean() - h, d.mean() + h, p)


R = collections.defaultdict(dict)
for size in SIZES:
    for pat in ('../logs/main/main_%s_*.jsonl', '../logs/new/new_%s_*.jsonl', '../logs/rev1/rev1_%s_*.jsonl',
                '../logs/rev1/rev1b_%s_*.jsonl'):
        if not glob.glob(pat % size) and not glob.glob(pat % size + '.gz'):
            continue
        for f, r in recio.records(pat % size):
            assert r['status'] == 'ok', (f, r['inst'], r['rule'])
            if r['rule'] in RULES + ('scip',):
                R[r['rule']][(size, r['inst'])] = np.array(r['closed'])

S = R['scip']
for label, sizes in (('6x8', ('6x8',)), ('10x20', ('10x20',)), ('pooled 6x8 + 10x20', SIZES)):
    keys = sorted(i for i in S if i[0] in sizes)
    print('-- %s (n %d)' % (label, len(keys)))
    for k in RULES:
        ids = [i for i in keys if i in R[k]]
        assert len(ids) == len(keys), (k, label, len(ids))
        d = {s: np.array([R[k][i][s] - S[i][s] for i in ids]) for s in (3, 5, 10, 20)}
        print('%-11s d3 %+.4f d5 %+.4f d10 %+.4f d20 %+.4f | d20-d3 %s | d20-d5 %s | d20-d10 %s' % (
            k, d[3].mean(), d[5].mean(), d[10].mean(), d[20].mean(), ci(d[20] - d[3]), ci(d[20] - d[5]),
            ci(d[20] - d[10])))
