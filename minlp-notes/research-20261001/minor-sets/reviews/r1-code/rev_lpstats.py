"""Reviewer r1: paired statistics for the LP re-solve comparisons of Section 7.2 (from the logged jsonl).
Mean paired difference (family - SCIP) with a 95% bootstrap CI (10000 resamples, seed 0) and an exact
two-sided sign test on corners with |difference| > 0.01.  Usage: python3 rev_lpstats.py LOGDIR"""
import json, sys
from math import comb
import numpy as np
L = sys.argv[1]
rng = np.random.default_rng(0)
for f in ('exp_lp_3x3.jsonl', 'exp_lp_4x4.jsonl'):
    R = [json.loads(l) for l in open(L + '/' + f)]
    R = [r for r in R if 'lp' in r and r['lp'].get('scip') is not None]
    for fam in ('orbit', 'orbit_near_scip', 'bcm', 'pr'):
        d = np.array([r['lp'][fam] - r['lp']['scip'] for r in R if r['lp'].get(fam) is not None])
        bs = np.array([rng.choice(d, len(d)).mean() for _ in range(10000)])
        up, dn = int((d > 0.01).sum()), int((d < -0.01).sum())
        n = up + dn; k = min(up, dn)
        p = min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)
        print('%s %-16s n=%d mean diff %+.4f  95%% bootstrap CI [%+.4f, %+.4f]; better/worse by >0.01: %d/%d, sign test p = %.3g'
              % (f, fam, len(d), d.mean(), np.quantile(bs, 0.025), np.quantile(bs, 0.975), up, dn, p))
