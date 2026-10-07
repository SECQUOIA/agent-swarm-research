"""Per-instance association between the final loss of the orbit rule against SCIP's rule and
trajectory features (diag records).  Usage: python3 analyze_percase.py 'GLOB' ROUND"""
import sys, glob, json, collections
import recio
import numpy as np
from scipy import stats
R = collections.defaultdict(dict)
for f in recio.files(sys.argv[1]):
    for line in recio.lines(f):
        r = json.loads(line); R[r['rule']][r['inst']] = r
RD = int(sys.argv[2])


def feats(r):
    rd = [x for x in r['rounds'] if 1 <= x['r'] <= 5]
    cuts = [c for c in r['cuts'] if 0 <= c['r'] <= 4]
    g = [np.log10(max(x['gamma'], 1e-12)) for x in rd if x.get('gamma') is not None]
    return dict(loggamma=np.mean(g) if g else np.nan,
                degen=float(np.mean([x['nnear'] > 0 for x in rd])) if rd else 0.0,
                viol=float(np.median([c['viol'] for c in cuts])) if cuts else 0.0,
                cosobj=float(np.mean([abs(c['cosobj']) for c in cuts])) if cuts else np.nan,
                ncuts=float(np.mean([x['ncuts'] for x in rd])) if rd else 0.0)


common = sorted(set(R['scip']) & set(R['orbit']))
loss, F = [], collections.defaultdict(list)
for i in common:
    d = R['orbit'][i]['closed'][RD] - R['scip'][i]['closed'][RD]
    fo, fs = feats(R['orbit'][i]), feats(R['scip'][i])
    loss.append(d)
    for k in fo:
        F[k].append(fo[k] - fs[k])
loss = np.array(loss)
print('instances %d; orbit - scip at round %d: mean %+.4f, %d below -0.01, %d above +0.01' % (
    len(loss), RD, loss.mean(), int(np.sum(loss < -0.01)), int(np.sum(loss > 0.01))))
for k, v in F.items():
    v = np.array(v); m = np.isfinite(v)
    rho, p = stats.spearmanr(v[m], loss[m])
    print('  feature diff (orbit - scip) in rounds 1-5: %-8s mean %+.4f   Spearman with outcome %+.3f (p = %.3g)' % (k, np.nanmean(v), rho, p))
