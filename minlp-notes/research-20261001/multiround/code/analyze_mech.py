"""Mechanism checks of the revision after review round 1 (M3).  For every rule in diag records
(cut records with the chosen steps 'a' = 1/alpha, SCIP's steps 'a_scip' at the same corner and the
normalized reduced costs 'w'), and per round bucket:

  tie2      fraction of corners where the chosen cut has >= 2 binding rays (w_j alpha_j within
            1e-3 of z_C; rays with w_j < 1e-4 ignored), i.e. a dual degenerate corner LP
  zC/zK     mean z_C / z_K of the chosen set
  shorter   mean over corners of the fraction of rays (step finite for either set) on which the
            chosen step is shorter than SCIP's step by more than 1e-9 (relative)
  mlr       mean over corners of the mean log10(alpha_rule / alpha_scip) over rays with both steps
            finite
  cos       mean |cos| between cut normal and objective

Then, per instance, the loss (rule - scip, fraction of the root gap closed after round RD) is
correlated (Spearman) with features of the rule's own trajectory in rounds 0-4: mean 'shorter',
mean 'mlr', mean tie2, and 'degen' (share of rounds 1-5 whose vertex has a reduced cost
<= 1e-6 max), the last as a difference to SCIP's trajectory as in analyze_percase.py.
Usage: python3 analyze_mech.py 'GLOB' RD"""
import sys, collections, warnings
import numpy as np
from scipy import stats
import recio
warnings.filterwarnings("ignore")

BUCK = [(0, 0), (1, 2), (3, 5), (6, 10), (11, 19)]
RD = int(sys.argv[2])
R = collections.defaultdict(dict)
for f, r in recio.records(sys.argv[1]):
    R[r['rule']][r['inst']] = r


def cutfeat(c):
    if 'a_scip' not in c or 'w' not in c:
        return None
    a, s, w = np.array(c['a']), np.array(c['a_scip']), np.array(c['w'])
    m = (a > 0) & (w >= 1e-4)
    tie2 = None
    if m.any():
        v = w[m] / a[m]
        tie2 = float(np.sum(v <= (1 + 1e-3) * v.min()) >= 2)
    fin = (a > 0) | (s > 0)                       # a step is finite iff its inverse is > 0
    shorter = float(np.mean(a[fin] > s[fin] * (1 + 1e-9))) if fin.any() else None
    both = (a > 0) & (s > 0)
    mlr = float(np.mean(np.log10(s[both] / a[both]))) if both.any() else None
    zr = min(c['zC'] / c['zk'], 1.0) if c['zk'] and np.isfinite(c['zk']) and c['zk'] > 0 else None
    return dict(tie2=tie2, zr=zr, shorter=shorter, mlr=mlr, cos=abs(c['cosobj']))


def key(rule, c):
    return rule if rule != 'both' else 'both:' + c['set']


T = collections.defaultdict(lambda: [collections.defaultdict(list) for _ in BUCK])
for rule, D in R.items():
    for rec in D.values():
        for c in rec.get('cuts', []):
            b = [i for i, (lo, hi) in enumerate(BUCK) if lo <= c['r'] <= hi]
            ft = cutfeat(c)
            if not b or ft is None:
                continue
            for k, v in ft.items():
                if v is not None:
                    T[key(rule, c)][b[0]][k].append(v)

print('records: ' + ', '.join('%s %d' % (k, len(v)) for k, v in R.items()))
for name, lab in (('tie2', 'fraction of corners with >= 2 binding rays'), ('zr', 'mean z_C/z_K'),
                  ('shorter', 'mean fraction of rays where the step is shorter than SCIP\'s'),
                  ('mlr', 'mean log10(alpha_rule/alpha_scip) over rays with both steps finite'),
                  ('cos', 'mean |cos(cut normal, objective)|')):
    print('\n%s\n%-12s %s' % (lab, 'rule', '  '.join('%8s' % ('r%d-%d' % b) for b in BUCK)))
    for k in sorted(T):
        print('%-12s %s' % (k, '  '.join('%8.3f' % np.mean(T[k][b][name]) if T[k][b][name] else '%8s' % '-'
                                          for b in range(len(BUCK)))))


def trajfeat(rec):
    cuts = [c for c in rec.get('cuts', []) if 0 <= c['r'] <= 4]
    F = [cutfeat(c) for c in cuts]
    F = [x for x in F if x is not None]
    rd = [x for x in rec['rounds'] if 1 <= x['r'] <= 5]
    out = {}
    for k in ('shorter', 'mlr', 'tie2'):
        v = [x[k] for x in F if x[k] is not None]
        out[k] = float(np.mean(v)) if v else np.nan
    out['degen'] = float(np.mean([x['nnear'] > 0 for x in rd])) if rd else 0.0
    return out


S = R.get('scip', {})
print('\nPer-instance Spearman correlation of the loss (rule - scip after round %d) with trajectory features '
      '(rounds 0-4 for cut features, 1-5 for degen; degen as rule - scip)' % RD)
pool = collections.defaultdict(list)
for rule in R:
    if rule in ('scip', 'both'):
        continue
    ids = sorted(set(R[rule]) & set(S))
    loss = np.array([R[rule][i]['closed'][RD] - S[i]['closed'][RD] for i in ids])
    fs = [trajfeat(R[rule][i]) for i in ids]
    fsc = [trajfeat(S[i]) for i in ids]
    line = '%-10s n %2d mean loss %+.4f:' % (rule, len(ids), loss.mean())
    for k in ('shorter', 'mlr', 'tie2', 'degen'):
        v = np.array([f[k] - (g[k] if k == 'degen' else 0.0) for f, g in zip(fs, fsc)])
        m = np.isfinite(v)
        rho, p = stats.spearmanr(v[m], loss[m])
        line += '  %s %+.3f (p %.2g, mean %.3f)' % (k, rho, p, np.nanmean(v))
        if rule in ('orbit', 'pertE0.1', 'geo') and k != 'degen':
            pool[k] += list(zip(v[m], loss[m], [rule] * int(m.sum())))
    print(line)
if pool:
    print('pooled orbit, pertE0.1, geo (rank correlation within rule, then averaged by Fisher z; '
          'rules whose feature is constant, so that the correlation is undefined, are left out):')
    for k, L in pool.items():
        zs, ns, used = [], [], []
        for rule in ('orbit', 'pertE0.1', 'geo'):
            v = np.array([x for x, y, r in L if r == rule]); y = np.array([y for x, y, r in L if r == rule])
            if len(v) > 3:
                rho = stats.spearmanr(v, y)[0]
                if np.isfinite(rho):
                    zs.append(np.arctanh(rho)); ns.append(len(v)); used.append(rule)
        if zs:
            print('  %s mean within-rule Spearman %+.3f (rules: %s)' % (k, np.tanh(np.average(zs, weights=ns)), ', '.join(used)))
        else:
            print('  %s mean within-rule Spearman undefined (feature constant in every rule)' % k)
