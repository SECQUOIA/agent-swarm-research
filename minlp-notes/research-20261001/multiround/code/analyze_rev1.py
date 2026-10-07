"""Paired statistics for the revision after review round 1.

Part M1: orbit - orbit_core (corrected versus bug-affected cap of the orbit bisection), on the 10
original 6x8 instances of exp_loop.py (logs/fid2_exploop_6x8.jsonl) and on the 220 main-run
instances, after rounds 1, 3, 10, 20.
Part M2: switching rules (orbit in rounds 0..K-1 then SCIP: first_orbit = o1s, o2s, o3s, o5s;
SCIP in rounds 0..K-1 then orbit: s1o, s3o, s5o), maj2 and rnd0.33, difference to SCIP's rule after rounds
1, 3, 5, 10, 20 per size and pooled; the share of the orbit rule's own mean difference.
Reads logs/main, logs/new, logs/rev1 (plain or .gz).  Usage: python3 analyze_rev1.py"""
import collections, glob
import numpy as np
from scipy import stats
import recio

SIZES = ('4x4', '6x8', '8x12', '10x20')


def ci(d):
    d = np.asarray(d, float)
    h = stats.t.ppf(0.975, len(d) - 1) * d.std(ddof=1) / np.sqrt(len(d))
    p = stats.ttest_1samp(d, 0.0).pvalue if d.std() > 0 else 1.0
    return '%+.4f [%+.4f, %+.4f] p %.2g n %d' % (d.mean(), d.mean() - h, d.mean() + h, p, len(d))


R = collections.defaultdict(dict)
for size in SIZES:
    for pat in ('../logs/main/main_%s_*.jsonl', '../logs/new/new_%s_*.jsonl', '../logs/rev1/rev1_%s_*.jsonl',
                '../logs/rev1/rev1b_%s_*.jsonl'):
        if not glob.glob(pat % size) and not glob.glob(pat % size + '.gz'):
            continue
        for f, r in recio.records(pat % size):
            assert r['status'] == 'ok', (f, r['inst'], r['rule'])
            R[r['rule']][(size, r['inst'])] = np.array(r['closed'])

print('== M1: orbit - orbit_core')
F = collections.defaultdict(dict)
for f, r in recio.records('../logs/fid2_exploop_6x8.jsonl'):
    F[r['rule']][r['inst']] = np.array(r['closed'])
ids = sorted(F['orbit'])
for s in (1, 3, 10):
    print('10 original 6x8 instances, round %2d: %s' % (s, ci([F['orbit'][i][s] - F['orbit_core'][i][s] for i in ids])))
print('  per-instance differences after round 10:', ' '.join('%+.3f' % (F['orbit'][i][10] - F['orbit_core'][i][10]) for i in ids))
print('  means after round 10: scip %.3f orbit %.3f orbit_core %.3f' % tuple(np.mean([F[k][i][10] for i in ids]) for k in ('scip', 'orbit', 'orbit_core')))
ids = sorted(set(R['orbit']) & set(R['orbit_core']))
for s in (1, 3, 10, 20):
    print('220 main instances, round %2d: %s' % (s, ci([R['orbit'][i][s] - R['orbit_core'][i][s] for i in ids])))
for size in SIZES:
    ii = [i for i in ids if i[0] == size]
    print('  %-5s round 10: %s' % (size, ci([R['orbit'][i][10] - R['orbit_core'][i][10] for i in ii])))

print('\n== M2: switching rules and maj2, difference to scip')
RULES = ('first_orbit', 'o2s', 'o3s', 'o5s', 'orbit', 's1o', 's3o', 's5o', 'maj2', 'rnd0.33')
ROUNDS = (1, 3, 5, 10, 20)
S = R['scip']


def block(label, keys):
    print('-- %s' % label)
    base = {s: np.mean([R['orbit'][i][s] - S[i][s] for i in keys]) for s in ROUNDS}
    for k in RULES:
        ids = sorted(set(R[k]) & set(keys))
        if len(ids) < len(keys):
            print('%-11s not run on all instances of this block (%d of %d)' % (k, len(ids), len(keys)))
            continue
        cells, means = [], {}
        for s in ROUNDS:
            d = np.array([R[k][i][s] - S[i][s] for i in ids])
            means[s] = d.mean()
            cells.append('r%d %s' % (s, ci(d)))
        d10 = np.array([R[k][i][10] - S[i][10] for i in ids])
        print('%-11s %s | W/L r10 %d/%d' % (k, ' | '.join(cells), int(np.sum(d10 > 0.01)), int(np.sum(d10 < -0.01))))
        if k != 'orbit':
            print('%-11s share of the orbit rule\'s mean difference: %s' % (
                '', ' '.join('r%d %.2f' % (s, means[s] / base[s]) if abs(base[s]) > 1e-4 else 'r%d -' % s for s in ROUNDS)))


def contrast(label, keys, k1, k2):
    ids = sorted(set(R[k1]) & set(R[k2]) & set(keys))
    print('-- %s: %s - %s  %s' % (label, k1, k2, ' | '.join('r%d %s' % (s, ci([R[k1][i][s] - R[k2][i][s] for i in ids]))
                                                     for s in (3, 10, 20))))


for size in SIZES:
    block(size, [i for i in S if i[0] == size])
block('pooled 4x4 + 6x8', [i for i in S if i[0] in ('4x4', '6x8')])
block('pooled 6x8 + 10x20', [i for i in S if i[0] in ('6x8', '10x20')])
block('pooled all sizes', list(S))
print()
for size in SIZES:
    contrast(size, [i for i in S if i[0] == size], 'maj2', 'rnd0.33')
contrast('pooled all sizes', list(S), 'maj2', 'rnd0.33')
contrast('pooled all sizes', list(S), 'first_orbit', 'orbit')

print('\n== maj2 and rnd0.33: share of cuts taken from the orbit set')
for size in SIZES:
    tot = collections.defaultdict(collections.Counter)
    for pat in ('../logs/rev1/rev1_%s_*.jsonl', '../logs/rev1/rev1b_%s_*.jsonl'):
        if glob.glob(pat % size):
            for f, r in recio.records(pat % size):
                tot[r['rule']].update(r.get('sets', {}))
    for k in ('maj2', 'rnd0.33'):
        n = sum(tot[k].values())
        print('  %-5s %-8s cuts %5d, orbit share %.3f' % (size, k, n, tot[k]['orbit'] / n if n else float('nan')))
