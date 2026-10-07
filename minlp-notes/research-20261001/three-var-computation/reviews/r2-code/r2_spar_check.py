"""Reviewer r2: independent checks of the revised Section 4.1 (no stream imports).

Reads raw stream records only: BoxQP .in files and README optima, the 17 original audit
JSON records, the saved audit points (*.base.npz) and depth arrays (*.depth.npz), the
strict re-audit records (author logs/strict_r1/ and reviewer reviews/r1-logs/).
Run from three-var-computation/: python reviews/r2-code/r2_spar_check.py
"""
import glob
import itertools
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
L = os.path.join(ROOT, 'logs')
SRC = os.path.join(ROOT, 'sources/BoxQP_instances-master')

opt = {}
for line in open(os.path.join(SRC, 'README.txt')):
    t = line.split()
    if len(t) == 2 and t[0].startswith('spar'):
        opt[t[0]] = -float(t[1])


def instance(name):
    tok = open(glob.glob(os.path.join(SRC, '*', name + '.in'))[0]).read().split()
    n = int(tok[0])
    v = np.array(tok[1:], float)
    return -v[n:].reshape(n, n) / 2, -v[:n]


def f_uniform(H, g):
    return np.trace(H) / 3 + (H.sum() - np.trace(H)) / 4 + g.sum() / 2


def triangle_viol(x, Y, T):
    i, j, k = T.T
    return np.stack([Y[i, j] + Y[i, k] - x[i] - Y[j, k], Y[i, j] + Y[j, k] - x[j] - Y[i, k],
                     Y[i, k] + Y[j, k] - x[k] - Y[i, j],
                     x[i] + x[j] + x[k] - Y[i, j] - Y[i, k] - Y[j, k] - 1], 1).max(1)


def gain(eps, fc, B):
    return eps * (fc - B) / (1 + eps)


print('== original audits')
recs = {}
for p in glob.glob(L + '/audit/spar*.json') + glob.glob(L + '/spar_audit/spar*.json'):
    if p.endswith('.tri.json'):
        continue
    r = json.load(open(p))
    recs[r['name']] = (r, p)
print('records:', len(recs))
rows = []
for name, (r, p) in sorted(recs.items()):
    H, g = instance(name)
    n = len(g)
    fc = f_uniform(H, g)
    gap = opt[name] - r['B_safe']
    eps = max(0.0, -r['min_depth'])
    row = dict(name=name, n=n, rel=gap / abs(opt[name]), ratio=gain(eps, fc, r['B']) / gap,
               B_minus_opt=r['B'] - opt[name], pinf=r['pinf'])
    bp, dp = p + '.base.npz', p + '.depth.npz'
    if os.path.exists(bp) and os.path.exists(dp):
        z = np.load(bp)
        d = np.load(dp)['depths']
        T = np.array(list(itertools.combinations(range(n), 3)))
        tv = triangle_viol(z['x'], z['Y'], T)
        a, b = int(np.argmin(d)), int(np.argmax(tv))
        assert d[a] == r['min_depth']
        row.update(tv_max=float(tv.max()), deepest=T[a].tolist(), most_violated=T[b].tolist(),
                   match=a == b, tv_at_deepest=float(tv[a]),
                   depth_over_minus4tv=float(d[a] / (-4 * tv[a])) if tv[a] > 0 else None,
                   # exact depth is <= -4 tv when tv > 0 (normalized triangle cut is feasible
                   # in Lemma 2); report how far stored depths exceed that exact bound
                   max_excess_over_minus4tv=float(np.max((d + 4 * tv)[tv > 0])),
                   min_depth_tri_feasible=float(d[tv <= 0].min()),
                   min_depth_tv_le_1e8=float(d[tv <= 1e-8].min()),
                   n_depth_lt_1e7=int((d < -1e-7).sum()))
    rows.append(row)
for row in sorted(rows, key=lambda r: -r['rel']):
    print(json.dumps(row))
saved = [r for r in rows if 'match' in r]
m = [r for r in saved if r['match']]
print('saved points:', len(saved), ' deepest == most violated triangle:', len(m))
print('  depth/(-4tv) on matches: %.4f .. %.4f' % (min(r['depth_over_minus4tv'] for r in m),
                                                   max(r['depth_over_minus4tv'] for r in m)))
print('  non-matching:', [(r['name'], r['tv_at_deepest'], r['tv_max']) for r in saved if not r['match']])
print('  min depth over triangle-feasible triples (all saved):',
      min(r['min_depth_tri_feasible'] for r in saved))
print('  max pinf over 17:', repr(max(r['pinf'] for r in rows)))
big = [r for r in rows if r['rel'] >= 1e-5]
print('rel gap >= 1e-5:', len(big), ' max ratio excluding spar090-075-1:',
      max((r['ratio'], r['name']) for r in big if r['name'] != 'spar090-075-1'))
for r in rows:
    if r['rel'] < 1e-5:
        print('small gap: %s rel %.3e ratio %.4f%% B-opt %r' % (r['name'], r['rel'], 100 * r['ratio'],
                                                               r['B_minus_opt']))
print('max ratio:', max((r['ratio'], r['name']) for r in rows))

print('\n== strict spar090-075-1')
name = 'spar090-075-1'
H, g = instance(name)
fc = f_uniform(H, g)
T = np.array(list(itertools.combinations(range(90), 3)))
A = json.load(open(L + '/strict_r1/%s.json' % name))
Rv = json.load(open(os.path.join(ROOT, 'reviews/r1-logs/spar090_strict.json')))
dA = np.load(L + '/strict_r1/%s.depth.npz' % name)['depths']
dR = np.load(os.path.join(ROOT, 'reviews/r1-logs/spar090_strict.depth.npz'))['depths']
print('depth arrays bit-identical:', np.array_equal(dA, dR), ' len', len(dA), ' nan', int(np.isnan(dA).sum()))
zA = np.load(L + '/strict_r1/%s.base.npz' % name)
zR = np.load(os.path.join(ROOT, 'reviews/r1-logs/spar090_strict.base.npz'))
print('base points bit-identical:', np.array_equal(zA['x'], zR['x']) and np.array_equal(zA['Y'], zR['Y']))
tv = triangle_viol(zA['x'], zA['Y'], T)
print('author strict: tri', A['tri'], 'max triangle viol', repr(float(tv.max())), 'logged',
      repr(A['max_triangle_violation']), 'pinf', A['pinf'], 'status', A['status'])
eps = max(0.0, -float(dA.min()))
gap = opt[name] - A['B_safe']
gn = gain(eps, fc, A['B'])
print('min depth', repr(float(dA.min())), 'deepest', T[int(np.argmin(dA))].tolist(),
      '#<-1e-7', int((dA < -1e-7).sum()))
print('gain %r ratio %r with margin %r' % (gn, gn / gap, (gn + A['B'] - A['B_safe']) / gap))
print('relative primal change vs original audit:',
      (A['B'] - recs[name][0]['B']) / abs(recs[name][0]['B']))
print('reviewer:', {k: Rv.get(k) for k in ('B', 'B_safe', 'min_depth', 'gain_over_gap', 'tri')})

print('\n== failed strict attempts (saved base points)')
for name in ('spar100-050-1', 'spar100-050-2'):
    z = np.load(L + '/strict_r1/%s.base.npz' % name)
    info = json.loads(str(z['info']))
    n = len(z['x'])
    T = np.array(list(itertools.combinations(range(n), 3)))
    tv = triangle_viol(z['x'], z['Y'], T)
    print(name, 'max triangle viol %r (logged %r), #>1e-8 %d, tri %d, rounds %s' % (
        float(tv.max()), info['max_triangle_violation'], int((tv > 1e-8).sum()), info['tri'],
        [(r['solve_tol'], r['B'], r['status']) for r in info['rounds']]))
    od = np.load(L + '/spar_audit/%s.json.depth.npz' % name)['depths']
    a = int(np.argmin(od))
    print('   original deepest triple', T[a].tolist(), 'original depth %.3e, its tv now %.3e' % (od[a], tv[a]))
    np.save(os.path.join(ROOT, 'reviews/r2-logs/%s_probe_triples.npy' % name),
            T[np.argsort(od)[:100]])
