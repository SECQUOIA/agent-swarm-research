"""Frequency of triple-level gaps for random three-variable objectives (logs/n3).
A gap is counted when X_safe - B > thr * max(1, |X|): the exact value is at least
X_safe (safe dual bound of the exact lift) and B is the base primal objective."""
import json, glob, sys
import numpy as np
from collections import defaultdict
stats = defaultdict(list)
for fn in sorted(glob.glob('../logs/n3/*.jsonl')):
    for line in open(fn):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue   # last line of a stopped run may be truncated
        stats[r['dist']].append(r)
for d, R in sorted(stats.items()):
    rel = np.array([(r['X_safe'] - r['B']) / max(1, abs(r['X'])) for r in R])
    out = '%-20s samples %6d  max rel %.2e  count(rel>1e-6) %d  count(rel>1e-5) %d  count(rel>1e-4) %d' % (
        d, len(R), rel.max(), (rel > 1e-6).sum(), (rel > 1e-5).sum(), (rel > 1e-4).sum())
    print(out)
    for r, v in zip(R, rel):
        if v > 1e-4:
            gap = r['X'] - r['B']
            print('    sample', r['seed'], r['s'], 'rel %.2e' % v, {m: round((r[m] - r['B']) / gap, 4) for m in ['K', 'A', 'KA', 'F', 'KAF'] if m in r})
