"""Dual degeneracy of dumped root corners: fraction of rays with zero reduced cost, and fraction of corners whose
single-cut criterion min_j wt_j alpha_j (wt = reduced costs floored at 1e-6 max) is attained at a ray with zero
reduced cost (then the criterion is set by the floor, not by the objective).
Usage: python3 degeneracy.py DUMP...
"""
import sys, gzip, json
import numpy as np
print('| dump | corners | mean share of zero-cost rays | corners with all rays zero-cost | corners whose criterion is attained at a zero-cost ray |')
print('|---|---|---|---|---|')
tot = [0, 0, 0]
for f in sys.argv[1:]:
    fr = []; allz = 0; att = 0; n = 0
    for l in gzip.open(f, 'rt'):
        d = json.loads(l.replace('-nan', 'NaN').replace('nan', 'NaN'))
        if d['type'] != 'corner' or not d['w']:
            continue
        w = np.array(d['w']); a = np.array(d['alpha0'], float); a[a < 0] = np.inf
        zero = w <= 1e-9 * max(w.max(), 1e-300)
        wt = np.maximum(w, 1e-6 * max(w.max(), 1e-9))
        v = np.where(np.isfinite(a), wt * a, np.inf)
        n += 1; fr.append(zero.mean()); allz += zero.all()
        if np.isfinite(v.min()) and zero[int(np.argmin(v))]:
            att += 1
    tot[0] += n; tot[1] += allz; tot[2] += att
    print('| %s | %d | %.2f | %d | %d |' % (f.split('/')[-1].replace('.jsonl.gz', ''), n, np.mean(fr), allz, att))
print('| total | %d | | %d | %d |' % tuple(tot))
