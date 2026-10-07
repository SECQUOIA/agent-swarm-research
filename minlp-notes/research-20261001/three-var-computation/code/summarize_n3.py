import json, sys, glob
import numpy as np
from collections import defaultdict
files = sys.argv[1:] or glob.glob('../logs/n3/*.jsonl')
c = defaultdict(int); g = defaultdict(list)
for fn in files:
    for l in open(fn):
        r = json.loads(l); d = r['dist']; c[d] += 1
        gap = r['X'] - r['B']
        if 'KAF' in r:
            g[d].append({m: (r[m] - r['B']) / gap for m in ['K', 'A', 'KA', 'F', 'KAF']} | {'gap': gap, 'rel': gap / max(1, abs(r['X']))})
for d in sorted(c):
    G = g[d]
    print('%-22s samples %6d  with gap>1e-7: %5d' % (d, c[d], len(G)))
    if not G: continue
    for m in ['K', 'A', 'KA', 'F', 'KAF']:
        v = np.array([x[m] for x in G])
        print('    %-4s closed: mean %.3f median %.3f  frac>=0.999: %.3f  frac<=0.001: %.3f' % (m, v.mean(), np.median(v), (v >= .999).mean(), (v <= .001).mean()))
    ka = np.array([x['KA'] for x in G]); kaf = np.array([x['KAF'] for x in G])
    print('    KAF-KA: mean %.3f, frac(KAF-KA>0.01) %.3f, frac(KAF-KA>0.1) %.3f' % ((kaf - ka).mean(), ((kaf - ka) > .01).mean(), ((kaf - ka) > .1).mean()))
    rel = np.array([x['rel'] for x in G]); print('    rel gap median %.2e max %.2e' % (np.median(rel), rel.max()))
