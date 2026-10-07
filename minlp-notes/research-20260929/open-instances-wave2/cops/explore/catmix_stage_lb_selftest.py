"""Self-test of the rigorous per-stage bound: for random chord data (concave-ish plus noise,
and deliberately non-concave) and random rays, the rigorous stage bound must not exceed
the minimum of W(M(u) r) over a dense u sample (float)."""
import sys, numpy as np
sys.path.insert(0, '..')
import catmix_bound as cb, catmix_model as cmx
rng = np.random.default_rng(5)
N = 100
m, K = cmx.extract(N); maps = cb.Maps(K)
worst = -np.inf
for trial in range(6):
    th = np.unique(np.round(np.concatenate([[0, 1], rng.uniform(0, 1, 50), rng.uniform(0.05, 0.08, 400)]) * 2.0 ** 40) / 2.0 ** 40)
    w = 1 - 0.3 * th + 0.2 * th * (1 - th) + (1e-6 if trial % 2 else 1e-3) * rng.standard_normal(len(th))
    ch = cb.Chord(1 - th, th, w)
    rt = np.unique(np.round(rng.uniform(0, 0.1, 300) * 2.0 ** 40) / 2.0 ** 40)
    lb, inc, st = cb.stage_lb(maps.stage, 1 - rt, rt, ch, 1e-14)
    us = np.linspace(0, 1, 20001)
    dense = np.full(len(rt), np.inf)
    for uu in us:
        z1, z2 = cb.float_eval_map(maps.stage, 1 - rt, rt, np.full(len(rt), uu))
        dense = np.minimum(dense, ch.float_W(z1, z2))
    worst = max(worst, np.max(lb - dense))
    print('trial', trial, 'max(lb - dense_min) = %.3e' % np.max(lb - dense), 'min(dense_min - lb) = %.3e' % np.min(dense - lb), st['rounds'])
print('overall max(lb - dense sampled min):', worst, '(must be <= ~1e-15)')
