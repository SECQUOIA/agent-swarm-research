import json, sys, glob
import numpy as np
files = sorted(glob.glob('../logs/n3hard/*.jsonl'))
recs = {}
for fn in files:
    for l in open(fn):
        r = json.loads(l); recs.setdefault(r['kind'], []).append(r)
for kind, R in recs.items():
    print('== kind %s: %d samples' % (kind, len(R)))
    gaps = np.array([r['X'] - r['B'] for r in R])
    print('   B gap (X - B): median %.4f min %.4f max %.4f' % (np.median(gaps), gaps.min(), gaps.max()))
    for m in ['K', 'A', 'KA', 'F', 'KAF']:
        v = np.array([(r[m] - r['B']) / (r['X'] - r['B']) for r in R])
        print('   %-4s closed: mean %.4f median %.4f min %.4f  frac>=0.9999: %.3f' % (m, v.mean(), np.median(v), v.min(), (v >= .9999).mean()))
    # safe-bound check: X_safe vs X; F_safe
    xs = np.array([r['X'] - r['X_safe'] for r in R]); print('   X pobj - safe: max %.2e' % xs.max())
    fs = np.array([r['X_safe'] - r['F'] for r in R]); print('   X_safe - F pobj: max %.2e  (positive = F below exact by more than safe slack)' % fs.max())
    nd = np.array([sum(1 for d in np.diag(r['H']) if d > 0) for r in R]); print('   positive diagonals count distribution', np.bincount(nd, minlength=4))
