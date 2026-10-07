"""Review r3: independent check of the Section 7.2 paired statistics added in the round-2 revision.

Reads logs/exp_lp_{3x3,4x4}.jsonl directly (does not import the stream's code).  For each family
minus SCIP's cut (LP re-solve fraction of the single-minor gap):
  - number of zero differences and of tied |d| values;
  - Wilcoxon signed-rank: own normal approximation (zeros dropped, tie-corrected variance, no
    continuity correction), scipy default, scipy method='exact' on the nonzero differences;
  - exact sign test with own binomial sum;
  - Bonferroni with factor 8 (as in the note) and factor 16 (both tests over all eight comparisons,
    a sensitivity check for picking the better of two tests);
  - largest interval-end difference between logs/analysis.log and the two earlier reviews.
Usage: python3 r3_lpstats.py <stream logs dir> <reviews dir>
"""
import json
import re
import sys
from math import comb, erf, sqrt

import numpy as np
from scipy import stats

logs, revs = sys.argv[1], sys.argv[2]


def own_wilcoxon(d):
    d = d[d != 0]
    n = len(d)
    a = np.abs(d)
    ranks = stats.rankdata(a)
    wplus = ranks[d > 0].sum()
    mu = n * (n + 1) / 4
    _, cnt = np.unique(a, return_counts=True)
    var = n * (n + 1) * (2 * n + 1) / 24 - (cnt ** 3 - cnt).sum() / 48
    z = (wplus - mu) / sqrt(var)
    return 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2)))), n, int((cnt > 1).sum())


def sign_p(up, dn):
    n = up + dn
    return min(1.0, 2 * sum(comb(n, i) for i in range(min(up, dn) + 1)) / 2 ** n)


for size in ('3x3', '4x4'):
    rs = [json.loads(l) for l in open('%s/exp_lp_%s.jsonl' % (logs, size)) if l.strip()]
    g = [r for r in rs if 'ratios' in r and r['gap'] > 1e-6 and r['lp']['scip'] is not None]
    print('== %s: %d corners' % (size, len(g)))
    for fam in ('orbit', 'orbit_near_scip', 'bcm', 'pr'):
        d = np.array([r['lp'][fam] - r['lp']['scip'] for r in g])
        nz = int((d == 0).sum())
        pw_own, nn, nties = own_wilcoxon(d)
        pw_def = stats.wilcoxon(d).pvalue
        pw_ex = stats.wilcoxon(d[d != 0], method='exact').pvalue
        up, dn = int((d > 0.01).sum()), int((d < -0.01).sum())
        ps = sign_p(up, dn)
        zero_rows = [r['trial'] for r in g if r['lp'][fam] - r['lp']['scip'] == 0]
        print('  %-15s zeros %d (trials %s), tied |d| groups %d; Wilcoxon own-approx %.5f, scipy default %.5f,'
              ' exact %.5f (|exact - default| %.4f); x8 %.4f, x16 %.4f; sign %d/%d p %.5f, x8 %.4f, x16 %.4f'
              % (fam, nz, zero_rows, nties, pw_own, pw_def, pw_ex, abs(pw_ex - pw_def), min(1, 8 * pw_def),
                 min(1, 16 * pw_def), up, dn, ps, min(1, 8 * ps), min(1, 16 * ps)))

# interval ends: note log vs r1 and r2 logs
def grab(path, pat):
    out = {}
    size = None
    for line in open(path):
        m = re.search(r'(3x3|4x4)', line)
        if m and ('==' in line or line.startswith('exp_lp') or line[:3] in ('3x3', '4x4')):
            size = m.group(1)
        mm = re.search(pat, line)
        if mm and size:
            out[(size, mm.group(1))] = (float(mm.group(2)), float(mm.group(3)))
    return out


note = grab('%s/analysis.log' % logs, r'^\s+(orbit_near_scip|orbit|bcm|pr)\s+n \d+\s+mean \S+\s+95% CI \[(\S+), (\S+)\]')
r1 = grab('%s/r1-logs/rev_lpstats.log' % revs, r'(orbit_near_scip|orbit|bcm|pr)\s+n=\d+ .*CI \[(\S+), (\S+)\]')
r2 = grab('%s/r2-logs/r2_lpstats.log' % revs, r'(orbit_near_scip|orbit|bcm|pr)\s+n \d+ mean \S+ CI \[(\S+), (\S+)\]')
for tag, other in (('r1', r1), ('r2', r2)):
    diffs = [(max(abs(note[k][0] - other[k][0]), abs(note[k][1] - other[k][1])), k) for k in note if k in other]
    print('interval ends, note vs %s: %d comparisons matched, largest difference %.5f at %s' % (
        tag, len(diffs), max(diffs)[0], max(diffs)[1]))
