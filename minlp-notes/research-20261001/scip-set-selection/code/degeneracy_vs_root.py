"""Relate per-instance degeneracy of SCIP's root corners (logs/degeneracy_root.jsonl) to the root effect of the
rules (RGC differences averaged over seeds 0, 1, 2; logs/root.json and logs/rootseeds.json).

Usage: python3 degeneracy_vs_root.py DEGEN.jsonl ROOT.json ROOTSEEDS.json
"""
import sys, os, json, csv
from collections import defaultdict
import numpy as np
from scipy.stats import spearmanr, wilcoxon

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'sources')
ref = {}
for l in open(os.path.join(SRC, 'minlplib.solu')):
    p = l.split()
    if len(p) >= 3 and p[0] in ('=opt=', '=best='):
        ref[p[1]] = float(p[2])
sense = {x['name']: x['objsense'] for x in csv.DictReader(open(os.path.join(SRC, 'instancedata.csv')), delimiter=';')}
deg = {}
for l in open(sys.argv[1]):
    d = json.loads(l)
    deg[d['inst']] = d
R = defaultdict(lambda: defaultdict(dict))
for f in sys.argv[2:]:
    for r in json.load(open(f)):
        R[r['inst']][r['setting']][r['seed']] = r


def rgc(r, i):
    if r is None or r.get('rootdual') is None or r.get('firstlp') is None or 'time limit' in (r.get('status') or ''):
        return None
    s = -1.0 if sense.get(i) == 'max' else 1.0
    den = s * (ref[i] - r['firstlp'])
    if abs(den) <= 1e-6 * max(1.0, abs(ref[i])):
        return None
    return s * (r['rootdual'] - r['firstlp']) / den


rows = []
for i, d in deg.items():
    if i not in ref or not d.get('corners'):
        continue
    diffs = {}
    for a in ('corner', 'eff', 'off'):
        v = []
        for sd in (0, 1, 2):
            ga, gs = rgc(R[i][a].get(sd), i), rgc(R[i]['scip'].get(sd), i)
            if ga is not None and gs is not None:
                v.append(ga - gs)
        diffs[a] = np.mean(v) if len(v) == 3 else None
    if None in diffs.values():
        continue
    rows.append((i, d['crit_at_zero'], d['zero_share'], d['dim2_share'], diffs['corner'], diffs['eff'], -diffs['off']))
print('instances with degeneracy data and three seeds:', len(rows))
A = np.array([r[1:] for r in rows], float)
names = ['criterion at zero-cost ray (share of corners)', 'zero-cost share of rays', 'share of corners with dim(lambda) >= 2']
print('\n| quantity | median over instances | Spearman rho with D(corner, scip) (p) | with D(eff, scip) (p) | with D(scip, off) (p) |')
print('|---|---|---|---|---|')
for k, nm in enumerate(names):
    out = []
    for col in (3, 4, 5):
        rho, p = spearmanr(A[:, k], A[:, col])
        out.append('%+.3f (%.2g)' % (rho, p))
    print('| %s | %.2f | %s |' % (nm, np.median(A[:, k]), ' | '.join(out)))
print('\nRoot effect of the rules by degeneracy class (seed-averaged RGC difference to SCIP\'s rule):\n')
print('| class | n | mean D(corner, scip) | corner better / worse (> 0.01) | Wilcoxon p | mean D(eff, scip) | eff better / worse | Wilcoxon p |')
print('|---|---|---|---|---|---|---|---|')
classes = [('criterion at a zero-cost ray in < 50% of corners', A[:, 0] < 0.5),
           ('criterion at a zero-cost ray in >= 50% of corners', A[:, 0] >= 0.5),
           ('dim(lambda) >= 2 in >= 50% of corners', A[:, 2] >= 0.5),
           ('all', np.ones(len(A), bool))]
for nm, m in classes:
    dc, de = A[m, 3], A[m, 4]
    def pv(x):
        x = x[np.abs(x) > 1e-9]
        return wilcoxon(x).pvalue if len(x) >= 10 else float('nan')
    print('| %s | %d | %+.4f | %d / %d | %.3g | %+.4f | %d / %d | %.3g |' % (
        nm, m.sum(), dc.mean(), (dc > 0.01).sum(), (dc < -0.01).sum(), pv(dc), de.mean(), (de > 0.01).sum(),
        (de < -0.01).sum(), pv(de)))
