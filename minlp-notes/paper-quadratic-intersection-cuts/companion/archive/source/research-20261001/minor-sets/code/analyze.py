"""Summary tables for the minor-sets experiments (note, Section 7).  Usage: python3 analyze.py"""
import glob
import json
from math import comb
import numpy as np
from scipy import stats

FAMS = ['scip', 'bcm', 'pr', 'orbit']
ATTAIN = 1 - 1e-5


def load(pat):
    return [json.loads(l) for f in sorted(glob.glob(pat)) for l in open(f) if l.strip()]


def summ(v):
    v = np.array(v, float)
    return 'mean %.3f  median %.3f  q10 %.3f  min %.3f' % (v.mean(), np.median(v), np.quantile(v, .1), v.min())


NCOMP = 8  # paired comparisons in Section 7.2 (four families, two sizes), for the Bonferroni factor


def paired(d):
    """Mean of paired differences with a 95% percentile-bootstrap CI, median, the exact two-sided
    sign test on the differences larger than 0.01 in absolute value, and the two-sided Wilcoxon
    signed-rank test on all differences (scipy default: zero differences dropped); each p-value also
    Bonferroni-adjusted over the NCOMP comparisons, and over both tests for
    all NCOMP comparisons (so choosing the smaller p-value is also covered)."""
    rng = np.random.default_rng(0)
    bs = rng.choice(d, (10000, len(d))).mean(axis=1)
    up, dn = int((d > 0.01).sum()), int((d < -0.01).sum())
    p = min(1.0, 2 * sum(comb(up + dn, i) for i in range(min(up, dn) + 1)) / 2 ** (up + dn))
    pw = stats.wilcoxon(d).pvalue
    return ('n %d  mean %+.4f  95%% CI [%+.4f, %+.4f]  median %+.4f  better/worse %d/%d  sign test p %.3g'
            ' (x%d: %.3g, x%d: %.3g)  Wilcoxon p %.3g (x%d: %.3g, x%d: %.3g)') % (
        len(d), d.mean(), np.quantile(bs, .025), np.quantile(bs, .975), np.median(d), up, dn, p,
        NCOMP, min(1.0, NCOMP * p), 2 * NCOMP, min(1.0, 2 * NCOMP * p),
        pw, NCOMP, min(1.0, NCOMP * pw), 2 * NCOMP, min(1.0, 2 * NCOMP * pw))


print('=== Random corners (exp_random.py) ===')
for label, pat in (('N = 4', '../logs/exp_random_N4_*.jsonl'), ('N = 8', '../logs/exp_random_N8.jsonl')):
    rs = load(pat)
    fin = [r for r in rs if r.get('zK') is not None]
    print('%s: %d corners drawn with det(sbar) > 0, %d with finite z_K' % (label, len(rs), len(fin)))
    sup = np.array([len(r['support']) for r in fin])
    print('  minimizer support sizes:', {k: int((sup == k).sum()) for k in range(1, 5)})
    s2 = [r for r in fin if len(r['support']) == 2]
    if s2:
        tc = np.array([r['tangent_cos'] for r in s2])
        print('  support-2 minimizers on a tangent edge (|cos| < 1e-6): %d of %d' % ((tc < 1e-6).sum(), len(s2)))
    for fam in FAMS:
        v = [r['ratios'][fam] for r in fin]
        print('  %-5s ratio z/z_K: %s; attains z_K in %d of %d' % (fam, summ(v), sum(x >= ATTAIN for x in v), len(v)))
    for k in (1, 2):
        sub = [r for r in fin if len(r['support']) == k]
        if sub:
            fails = [r['ratios']['orbit'] for r in sub if r['ratios']['orbit'] < ATTAIN]
            print('  support %d (n = %d): orbit misses z_K in %d; their ratios %s' % (
                k, len(sub), len(fails), sorted(round(x, 4) for x in fails)))
            for fam in FAMS:
                v = [r['ratios'][fam] for r in sub]
                print('     %-5s attains in %d, mean %.3f' % (fam, sum(x >= ATTAIN for x in v), np.mean(v)))

print()
print('=== LP corners (exp_lp.py) ===')
for label, pat in (('3x3', '../logs/exp_lp_3x3.jsonl'), ('4x4', '../logs/exp_lp_4x4.jsonl')):
    rs = load(pat)
    if not rs:
        continue
    ok = [r for r in rs if 'ratios' in r]
    sk = [r for r in rs if 'skipped' in r]
    print('%s: %d LP corners with a violated minor (|det| >= 1e-4) and finite z_K > 0; %d skipped (z_K inf or 0)' % (
        label, len(ok), len(sk)))
    print('  corners with zero reduced costs among the minor-moving rays: %d' % sum(r['nzero_w'] > 0 for r in ok))
    print('  violated minors per LP vertex: mean %.1f' % np.mean([r['nviol'] for r in ok]))
    for fam in FAMS:
        v = [r['ratios'][fam] for r in ok]
        print('  %-5s ratio z/z_K: %s; attains z_K in %d of %d' % (fam, summ(v), sum(x >= ATTAIN for x in v), len(v)))
    g = [r for r in ok if r['gap'] > 1e-6 and r['lp']['scip'] is not None]
    print('  single-minor gap z_1 - z_LP > 1e-6 in %d corners (z_1 status: %s)' % (
        len(g), sorted({r['z1_status'] for r in ok})))
    print('  corner bound z_K / gap: %s' % summ([r['zK_over_gap'] for r in g]))
    nr = [r['near_ratio'] for r in ok if r.get('near_ratio') is not None]
    if nr:
        print('  orbit set nearest to SCIP\'s set: ratio z/z_K %s' % summ(nr))
    for fam in FAMS + ['orbit_near_scip', 'corner']:
        v = [r['lp'][fam] for r in g if r['lp'].get(fam) is not None]
        print('  LP re-solve with the %-6s cut: fraction of gap %s (n = %d)' % (fam, summ(v), len(v)))
    d = [r['lp']['orbit'] - r['lp']['scip'] for r in g if r['lp'].get('orbit') is not None]
    print('  orbit cut minus SCIP cut (LP re-solve): better by > 0.01 in %d, worse by > 0.01 in %d, of %d' % (
        sum(x > 0.01 for x in d), sum(x < -0.01 for x in d), len(d)))
    d = [r['lp']['orbit_near_scip'] - r['lp']['scip'] for r in g if r['lp'].get('orbit_near_scip') is not None]
    if d:
        print('  orbit-near-SCIP cut minus SCIP cut: better by > 0.01 in %d, worse by > 0.01 in %d, of %d' % (
            sum(x > 0.01 for x in d), sum(x < -0.01 for x in d), len(d)))
    print('  paired LP re-solve differences (family minus SCIP; bootstrap 10000 resamples, seed 0;'
          ' exact two-sided sign test on corners with |diff| > 0.01; two-sided Wilcoxon signed-rank test on'
          ' all differences; p-values unadjusted, in parentheses Bonferroni-adjusted over the 8 comparisons'
          ' and over both tests for all 8 comparisons, factor 16):')
    for fam in ('orbit', 'orbit_near_scip', 'bcm', 'pr'):
        d = np.array([r['lp'][fam] - r['lp']['scip'] for r in g if r['lp'].get(fam) is not None])
        print('    %-15s %s' % (fam, paired(d)))

print()
print('=== Adversarial search (adversarial.py) ===')
for tag, pat in (('margin 0.01', '../logs/adversarial_m01_s*.jsonl'), ('margin 0.05', '../logs/adversarial_m05_s*.jsonl')):
    allr = load(pat)
    rs = [r for r in allr if 'final_cert' in r]
    print('%s: %d restarts, %d invalid starts' % (tag, len(rs), sum('invalid_start' in r for r in allr)))
    for r in sorted(rs, key=lambda r: r['final_cert']):
        print('  start %3d: start ratio %.4f -> final %.4f (bisection upper %.4f), min margin %.4f, nfev %d' % (
            r['start'], r['start_ratio'], r['final_cert'], r['final_upper'], min(r['margins']), r['nfev']))
