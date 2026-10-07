"""Review r2: independent paired statistics of the LP re-solve fractions (note Section 7.2).
Own bootstrap (seed 12345, 20000 resamples), scipy exact binomial sign test, Wilcoxon signed-rank,
and the share of the total loss carried by the worst corners.  Usage: python3 r2_lpstats.py LOGDIR"""
import sys, json
import numpy as np
from scipy import stats

for size in ('3x3', '4x4'):
    rs = [json.loads(l) for l in open('%s/exp_lp_%s.jsonl' % (sys.argv[1], size))]
    rs = [r for r in rs if r.get('lp') and r['lp'].get('scip') is not None]
    print('== %s: %d corners' % (size, len(rs)))
    for fam in ('orbit', 'orbit_near_scip', 'bcm', 'pr'):
        d = np.array([r['lp'][fam] - r['lp']['scip'] for r in rs if r['lp'].get(fam) is not None])
        rng = np.random.default_rng(12345)
        bs = d[rng.integers(0, len(d), (20000, len(d)))].mean(1)
        up, dn = int((d > 0.01).sum()), int((d < -0.01).sum())
        p = stats.binomtest(up, up + dn, 0.5).pvalue
        pw = stats.wilcoxon(d).pvalue
        neg = np.sort(d[d < 0])
        share5 = neg[:5].sum() / d.sum() if d.sum() != 0 else float('nan')
        k10 = max(1, int(round(0.1 * len(d))))
        srt = np.sort(d)
        print('  %-15s n %d mean %+.6f CI [%+.6f, %+.6f] median %+.6f up/dn %d/%d sign p %.4g (x8 = %.3g) wilcoxon p %.3g'
              % (fam, len(d), d.mean(), np.quantile(bs, .025), np.quantile(bs, .975), np.median(d), up, dn, p, min(1, 8 * p), pw))
        print('  %-15s worst 10%% (%d corners) sum %+.4f of total %+.4f; mean without them %+.5f; #diff < -0.1: %d, > +0.1: %d'
              % ('', k10, srt[:k10].sum(), d.sum(), srt[k10:].mean(), int((d < -0.1).sum()), int((d > 0.1).sum())))
