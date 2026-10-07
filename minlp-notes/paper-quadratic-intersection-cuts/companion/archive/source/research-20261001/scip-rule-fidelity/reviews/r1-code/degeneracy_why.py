"""Why are MINLPLib corners degenerate?  For sample records with a zero-cost face meeting S
(reviewer check, n_+ <= 1), report: share of zero-rate corner rays, whether one zero-rate ray alone
reaches S, and what that ray is (column of a constraint variable / of another variable / row slack).
Usage: python3 degeneracy_why.py"""
import os, sys, json, gzip, glob, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep_check import build
HERE = os.path.dirname(os.path.abspath(__file__))
mine = {}
for f in glob.glob(os.path.join(HERE, '../r1-logs/indep_check_*.jsonl')):
    for l in open(f):
        r = json.loads(l); mine[(r['inst'], r['k'])] = r
stat = collections.Counter(); share = []; per_inst = collections.Counter(); kinds = collections.Counter()
for l in gzip.open(os.path.join(HERE, '../r1-logs/sample_records.jsonl.gz'), 'rt'):
    rec = json.loads(l)
    m = mine.get((rec['inst'], rec['k']))
    if not m or not m.get('degenerate') or rec['set'] != 'minlplib':
        continue
    Q, b, c, sbar, P, w, width, nq = build(rec)
    keep = width > 1e-9
    zr = keep & (w <= 1e-9 * w[keep].max())
    share.append(zr.sum() / keep.sum())
    q0 = sbar @ Q @ sbar + b @ sbar + c
    g = 2 * Q @ sbar + b
    single = []
    for j in np.where(zr)[0]:
        L, M = g @ P[:, j], P[:, j] @ Q @ P[:, j]
        reach = (M < 0) or (L < 0 and L * L - 4 * M * q0 >= 0)
        if reach:
            single.append(j)
    stat['records'] += 1
    stat['single zero-rate ray reaches S' if single else 'only pairs'] += 1
    per_inst[rec['inst']] += 1
    names = set(rec['vars'])
    for j in single[:1]:
        lp = rec['raylppos'][j]; nm = rec['rayname'][j]
        kinds['row slack' if lp < 0 else ('column of a constraint variable' if nm in names else 'column of another variable')] += 1
print(dict(stat))
print('share of zero-rate rays among corner rays: median %.2f, quartiles %s' % (np.median(share), np.quantile(share, [.25, .75])))
print('kind of the first single zero-rate ray reaching S:', dict(kinds))
print('records per instance:', dict(per_inst))
