"""Reviewer r1: recompute Section 4.1 numbers from raw spar logs (no stream imports).

Reads published optima from the BoxQP README, the 99 spar_base records, the 17 audit
records, and (where present) the saved audit points (base.npz) and depths (depth.npz).
For every audit point it recomputes the largest triangle violation over all triples
and checks whether the deepest triple is the triple of the most violated triangle.
Run from three-var-computation/: python reviews/r1-code/spar_recompute.py
"""
import glob
import itertools
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
L = os.path.join(ROOT, 'logs')

opt = {}
for line in open(os.path.join(ROOT, 'sources/BoxQP_instances-master/README.txt')):
    t = line.split()
    if len(t) == 2 and t[0].startswith('spar'):
        opt[t[0]] = -float(t[1])


def read_inst(name):
    p = glob.glob(os.path.join(ROOT, 'sources/BoxQP_instances-master/*/%s.in' % name))[0]
    tok = open(p).read().split()
    n = int(tok[0])
    v = np.array(tok[1:], float)
    c = v[:n]
    Q = v[n:].reshape(n, n)
    return -Q / 2, -c


# ---- 99 base runs
base = {}
for p in glob.glob(L + '/spar_base/*.json'):
    r = json.load(open(p))
    base[r['name']] = r
rel = {k: (opt[k] - r['B_safe']) / abs(opt[k]) for k, r in base.items()}
print('spar_base records:', len(base), ' published optima:', len(opt))
print('rel gap < 1e-6:', sum(v < 1e-6 for v in rel.values()), ' < 1e-5:', sum(v < 1e-5 for v in rel.values()))
big = sorted([k for k, v in rel.items() if v >= 1e-5], key=lambda k: -rel[k])
print('rel gap >= 1e-5 (%d):' % len(big), ', '.join('%s %.2e' % (k, rel[k]) for k in big))
mid = sorted([k for k, v in rel.items() if 1e-6 <= v < 1e-5])
print('1e-6 <= rel gap < 1e-5:', ', '.join('%s %.2e' % (k, rel[k]) for k in mid))
print('min n among big:', min(base[k]['n'] for k in big))
neg = [(k, opt[k] - base[k]['B']) for k in base if opt[k] - base[k]['B'] < 0]
print('base runs whose B primal is above the published optimum:', len(neg), sorted(neg, key=lambda t: t[1])[:5])

# ---- 17 audits
recs = {}
for p in glob.glob(L + '/audit/spar*.json') + glob.glob(L + '/spar_audit/*.json'):
    if p.endswith('.tri.json'):
        continue
    r = json.load(open(p))
    r['_path'] = p
    recs[r['name']] = r
print('\naudits:', len(recs))
rows = []
for k, r in recs.items():
    gap = opt[k] - r['B_safe']
    H, g = read_inst(k)
    n = len(g)
    fc = np.trace(H) / 3 + (H.sum() - np.trace(H)) / 4 + g.sum() / 2
    eps = max(0.0, -r['min_depth'])
    gain = eps * (fc - r['B']) / (1 + eps)
    row = dict(name=k, n=n, gap=gap, rel=gap / abs(opt[k]), md=r['min_depth'], gain=gain,
               ratio=gain / gap, ratio_margin=(gain + r['B'] - r['B_safe']) / gap,
               fc_ok=abs(fc - r['f_uniform']) < 1e-9 * max(1, abs(fc)),
               gain_ok=abs(gain - r['max_triple_level_improvement']) <= 1e-9 * max(1e-12, gain),
               B_minus_opt=r['B'] - opt[k], margin=r['B'] - r['B_safe'],
               base_rel=rel[k], tv_logged=r.get('max_triangle_violation'))
    bp = r['_path'] + '.base.npz'
    dp = r['_path'] + '.depth.npz'
    if os.path.exists(bp) and os.path.exists(dp):
        z = np.load(bp)
        x, Y = z['x'], z['Y']
        d = np.load(dp)['depths']
        T = np.array(list(itertools.combinations(range(n), 3)))
        i, j, kk = T[:, 0], T[:, 1], T[:, 2]
        V = np.stack([Y[i, j] + Y[i, kk] - x[i] - Y[j, kk], Y[i, j] + Y[j, kk] - x[j] - Y[i, kk],
                      Y[i, kk] + Y[j, kk] - x[kk] - Y[i, j], x[i] + x[j] + x[kk] - Y[i, j] - Y[i, kk] - Y[j, kk] - 1], 1)
        tv = V.max(1)
        a = int(np.argmin(d))
        row.update(tv_recomputed=float(tv.max()), argmin_depth_triple=T[a].tolist(), tv_at_argmin=float(tv[a]),
                   depth_over_4tv=float(-d[a] / (4 * tv[a])) if tv[a] > 0 else None,
                   argmax_tv_triple=T[int(np.argmax(tv))].tolist(),
                   second_min_depth=float(np.sort(d)[1]),
                   min_depth_on_triangle_feasible=float(d[tv <= 0].min()),
                   n_tri_viol_gt_1e7=int((tv > 1e-7).sum()), n_tri_viol_gt_0=int((tv > 0).sum()),
                   md_check=abs(d.min() - r['min_depth']) < 1e-15)
        # Lemma 3 ratio if the deepest triple were excluded (NOT a valid bound; diagnostic only)
        eps2 = max(0.0, -row['second_min_depth'])
        row['ratio_without_argmin'] = eps2 * (fc - r['B']) / (1 + eps2) / gap
    rows.append(row)
rows.sort(key=lambda r: -r['rel'])
for r in rows:
    print(json.dumps(r, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
print('\nmin depth range:', min(r['md'] for r in rows), max(r['md'] for r in rows))
mx = max(rows, key=lambda r: r['ratio'])
print('max ratio:', mx['name'], repr(mx['ratio']), 'gain', repr(mx['gain']), 'gap', repr(mx['gap']))
b14 = [r for r in rows if r['base_rel'] >= 1e-5]
print('instances with base rel gap >= 1e-5:', len(b14))
o13 = [r for r in b14 if r['name'] != 'spar090-075-1']
m13 = max(o13, key=lambda r: r['ratio'])
print('max ratio over the other 13:', m13['name'], repr(m13['ratio']))
sm = [r for r in rows if r['base_rel'] < 1e-5]
print('small-gap instances:', [(r['name'], round(100 * r['ratio'], 2), '%.2e' % r['rel']) for r in sm])
print('max ratio incl. primal-safe margin:', max((r['ratio_margin'], r['name']) for r in rows))
print('spar090-075-1 ratio incl. margin:', [r['ratio_margin'] for r in rows if r['name'] == 'spar090-075-1'])
print('max pinf:', max(recs[k]['pinf'] for k in recs))
