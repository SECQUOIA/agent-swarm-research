"""Summarize small_dense.py logs (logs/small_dense/*.jsonl).

For each n: instances, instances with a gap of B (opt - B_safe > 1e-6 max(1,|opt|)),
and for the gap instances the fraction of the gap closed by each method, computed
with safe bounds, closed = (s_M - s_B) / (opt - s_B), and the triple-level part
(s_X - s_B)/(opt - s_B).  Also counts instances where F (resp. KAF) is below X by more
than 1e-6 relative, and where KAF improves on KA by more than 1e-6 relative.
Usage: python summarize_small.py [glob]   (default ../logs/small_dense/n*.jsonl; AP variant: '../logs/small_dense/ap_*.jsonl')"""
import glob
import json
import sys
from collections import defaultdict

import numpy as np

recs = []
for f in sorted(glob.glob(sys.argv[1] if len(sys.argv) > 1 else '../logs/small_dense/n*.jsonl')):
    for line in open(f):
        try:
            recs.append(json.loads(line))
        except ValueError:
            pass
by = defaultdict(list)
for r in recs:
    by[r['n']].append(r)
M = ['K', 'A', 'KA', 'F', 'KAF', 'X', 'KAX']
print('| n | instances | with gap | ' + ' | '.join('closed by %s (mean / median)' % m for m in M) + ' |')
print('|---|---|---|' + '---|' * len(M))
allgap = []
for n in sorted(by):
    G = [r for r in by[n] if 'X' in r]
    allgap += G
    cells = []
    for m in M:
        v = np.array([(r[m + '_safe'] - r['B_safe']) / (r['opt'] - r['B_safe']) for r in G])
        cells.append('%.3f / %.3f' % (v.mean(), np.median(v)) if len(v) else '-')
    print('| %d | %d | %d | %s |' % (n, len(by[n]), len(G), ' | '.join(cells)))
G = allgap
if not G:
    sys.exit(0)
sc = lambda r: max(1.0, abs(r['opt']))
print()
print('gap instances:', len(G))
print('relative gap of B: median %.2e max %.2e' % (np.median([(r['opt'] - r['B_safe']) / sc(r) for r in G]),
                                                  max((r['opt'] - r['B_safe']) / sc(r) for r in G)))
for m in ['F', 'KAF', 'KA', 'K', 'A']:
    below = [r for r in G if r['X'] - r[m + '_safe'] > 1e-6 * sc(r)]
    print('%s below X (X_pobj - %s_safe > 1e-6 rel): %d' % (m, m, len(below)))
imp = [r for r in G if r['KAF_safe'] - r['KA'] > 1e-6 * sc(r)]
print('KAF safe above KA pobj by > 1e-6 rel: %d' % len(imp))
impF = [r for r in G if r['F_safe'] - r['KA'] > 1e-6 * sc(r)]
print('F safe above KA pobj by > 1e-6 rel: %d' % len(impF))
xs = np.array([(r['X_safe'] - r['B_safe']) / (r['opt'] - r['B_safe']) for r in G])
print('triple-level share of the gap (X): mean %.3f median %.3f; X closes >= 0.999: %d; X closes <= 0.001: %d' % (
    xs.mean(), np.median(xs), (xs >= 0.999).sum(), (xs <= 0.001).sum()))
t = {m: np.median([r[m + '_t'] for r in G]) for m in ['B', 'KA', 'F', 'KAF', 'X']}
print('median solve times (s):', {k: round(v, 3) for k, v in t.items()})
sz = {m: np.median([r[m + '_size']['psd_svec'] + r[m + '_size']['lin'] + 3 * r[m + '_size']['soc'] for r in G]) for m in ['B', 'KA', 'F', 'KAF', 'X']}
print('median cone dimension (PSD svec + linear + 3*SOC):', sz)
