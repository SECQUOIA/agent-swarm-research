"""Review r4 (multiround): independent recomputation of the round-3 control contrasts.

Reads the raw .jsonl / .jsonl.gz records under logs/{main,new,rev1,rev2,diag} directly (no stream
code). For each size (6x8, 10x20) and instance it collects the 'closed' trajectories of scip,
orbit, first_orbit (= o1s), o2s, o3s, o5s; duplicates across files must agree on their common
prefix. Then, with e(r) = rule(r) - orbit(r) (fraction of the root gap closed after r rounds):
  contrast(start) = e(20) - e(start), start in {3, 5, 10};
paired 95% t-intervals and two-sided t p-values (own formulas, scipy only for the t cdf/ppf),
Wilcoxon signed-rank p-values as a robustness check, and Holm adjustments over the 12 tests of a
span, over all 36, and over the 33 distinct tests (o5s 3->20 and 5->20 coincide).
Also: closed[0] == 0, oKs == orbit through state K, SCIP remaining gap, deficit changes vs SCIP,
and rule - SCIP at round 20.
"""
import glob
import gzip
import json
import math
import os
import sys
from collections import defaultdict

import numpy as np
from scipy import stats

ROOT = sys.argv[1]  # multiround/logs
RULES = ['first_orbit', 'o2s', 'o3s', 'o5s']
NAME = {'first_orbit': 'o1s', 'o2s': 'o2s', 'o3s': 'o3s', 'o5s': 'o5s'}
K = {'first_orbit': 1, 'o2s': 2, 'o3s': 3, 'o5s': 5}
WANT = set(RULES) | {'scip', 'orbit'}

traj = defaultdict(dict)  # (size, inst) -> rule -> closed
nfile = nrec = ndup = 0
for sub in ('main', 'new', 'rev1', 'rev2', 'diag'):
    for path in sorted(glob.glob(os.path.join(ROOT, sub, '*.jsonl*'))):
        base = os.path.basename(path)
        size = '6x8' if '_6x8' in base else '10x20' if '_10x20' in base else None
        if size is None:
            continue
        nfile += 1
        op = gzip.open if path.endswith('.gz') else open
        with op(path, 'rt') as f:
            for line in f:
                r = json.loads(line)
                nrec += 1
                if r.get('rule') not in WANT:
                    continue
                assert r['status'] == 'ok', (path, r['inst'], r['rule'])
                c = r['closed']
                key = (size, r['inst'])
                old = traj[key].get(r['rule'])
                if old is not None:
                    ndup += 1
                    m = min(len(old), len(c))
                    assert old[:m] == c[:m], ('duplicate differs', path, key, r['rule'])
                    if len(c) > len(old):
                        traj[key][r['rule']] = c
                else:
                    traj[key][r['rule']] = c
print('files %d, records %d, duplicate selected trajectories %d (all identical on common prefix)'
      % (nfile, nrec, ndup))

keys = {s: sorted(k for k, v in traj.items() if k[0] == s and 'scip' in v) for s in ('6x8', '10x20')}
for s in keys:
    for k in keys[s]:
        assert set(traj[k]) >= WANT, (k, sorted(traj[k]))
        for rule in WANT:
            assert len(traj[k][rule]) == 21 and traj[k][rule][0] == 0.0, (k, rule)
        for rule in RULES:
            assert traj[k][rule][:K[rule] + 1] == traj[k]['orbit'][:K[rule] + 1], (k, rule)
            assert traj[k][rule][K[rule] + 1] != traj[k]['orbit'][K[rule] + 1] or True
    print('%s: %d instances with all six rules; closed[0] = 0; each oKs equals orbit through state K'
          % (s, len(keys[s])))
groups = [('6x8', keys['6x8']), ('10x20', keys['10x20']), ('pooled', keys['6x8'] + keys['10x20'])]


def tstat(x):
    x = np.asarray(x, float)
    n = len(x)
    m = x.mean()
    se = math.sqrt(((x - m) ** 2).sum() / (n - 1) / n)
    h = stats.t.ppf(0.975, n - 1) * se
    p = 2 * stats.t.sf(abs(m / se), n - 1) if se > 0 else float(m != 0) * 0 + (1.0 if m == 0 else 0.0)
    return m, m - h, m + h, p


def holm(ps):
    order = sorted(ps, key=lambda k: ps[k])
    out, run = {}, 0.0
    for i, k in enumerate(order):
        run = max(run, min(1.0, (len(order) - i) * ps[k]))
        out[k] = run
    return out


for label, ks in groups:
    sc = np.array([traj[k]['scip'] for k in ks])
    print('\n== %s (n %d): SCIP mean remaining gap r3 %.7f r20 %.7f' % (label, len(ks), 1 - sc[:, 3].mean(),
                                                                         1 - sc[:, 20].mean()))
    for rule in RULES + ['orbit']:
        R = np.array([traj[k][rule] for k in ks])
        d = R - sc
        m, lo, hi, p = tstat(d[:, 20] - d[:, 3])
        m2, lo2, hi2, p2 = tstat(d[:, 20])
        print('  %-5s deficit change 3->20 %+.7f [%+.7f, %+.7f] p %.4f | rule - SCIP at r20 %+.4f [%+.4f, %+.4f]'
              % (NAME.get(rule, rule), m, lo, hi, p, m2, lo2, hi2))

res, wil = {}, {}
for start in (3, 5, 10):
    for label, ks in groups:
        O = np.array([traj[k]['orbit'] for k in ks])
        for rule in RULES:
            R = np.array([traj[k][rule] for k in ks])
            e = R - O
            x = e[:, 20] - e[:, start]
            res[(start, label, rule)] = tstat(x)
            nz = x[x != 0]
            wil[(start, label, rule)] = stats.wilcoxon(nz).pvalue if len(nz) > 0 else 1.0
h36 = holm({k: v[3] for k, v in res.items()})
distinct = {k: v[3] for k, v in res.items() if not (k[2] == 'o5s' and k[0] == 5)}
h33 = holm(distinct)
for start in (3, 5, 10):
    h12 = holm({k: v[3] for k, v in res.items() if k[0] == start})
    print('\n== control contrast %d->20: e(20) - e(%d), e = rule - orbit' % (start, start))
    for label, _ in groups:
        for rule in RULES:
            k = (start, label, rule)
            m, lo, hi, p = res[k]
            print('  %-6s %s %+.7f [%+.7f, %+.7f] p %.7f Holm12 %.4f Holm36 %.4f Holm33 %s Wilcoxon p %.4f'
                  % (label, NAME[rule], m, lo, hi, p, h12[k], h36[k],
                     ('%.4f' % h33[k]) if k in h33 else '(dup)', wil[k]))
for label, _ in groups:
    a, b = res[(3, label, 'o5s')], res[(5, label, 'o5s')]
    print('o5s %s: 3->20 and 5->20 identical: %s' % (label, a == b))
best = sorted(res, key=lambda k: res[k][3])[:4]
print('\nsmallest raw p over the 36:', [(k, round(res[k][3], 6)) for k in best])
print('DONE')
