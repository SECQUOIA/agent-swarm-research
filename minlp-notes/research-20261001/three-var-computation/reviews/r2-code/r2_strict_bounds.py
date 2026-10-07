"""Reviewer r2: exact upper bounds on hull depth at the strict spar090-075-1 point.

For every triple, delta <= -4 * (triangle residual) and delta <= -6 * (diagonal-cap residual
Y_ii - x_i), because the normalized triangle and cap quadratics are feasible C in Lemma 2
(uniform means 1/4 and 1/6). Also McCormick residuals (uniform mean 1/4). Compares these exact
bounds with the stored (approximate) depths, and recomputes the Lemma 3 ratio with the most
negative exact bound in place of the stored minimum depth.
Run from three-var-computation/: python reviews/r2-code/r2_strict_bounds.py
"""
import glob
import itertools
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
name = 'spar090-075-1'
z = np.load(os.path.join(ROOT, 'logs/strict_r1', name + '.base.npz'))
info = json.loads(str(z['info']))
d = np.load(os.path.join(ROOT, 'logs/strict_r1', name + '.depth.npz'))['depths']
x, Y = z['x'], z['Y']
n = len(x)
T = np.array(list(itertools.combinations(range(n), 3)))
i, j, k = T.T
tv = np.stack([Y[i, j] + Y[i, k] - x[i] - Y[j, k], Y[i, j] + Y[j, k] - x[j] - Y[i, k],
               Y[i, k] + Y[j, k] - x[k] - Y[i, j], x[i] + x[j] + x[k] - Y[i, j] - Y[i, k] - Y[j, k] - 1], 1).max(1)
cap = np.diag(Y) - x
capT = np.maximum(np.maximum(cap[i], cap[j]), cap[k])
P = np.array(list(itertools.combinations(range(n), 2)))
a, b = P.T
mc = np.stack([-Y[a, b], Y[a, b] - x[a], Y[a, b] - x[b], x[a] + x[b] - 1 - Y[a, b]], 1).max(1)
bound = np.minimum(-4 * np.maximum(tv, 0), -6 * np.maximum(capT, 0))
print('max cap residual %.3e (#>0: %d of %d); max triangle residual %.3e; max McCormick residual %.3e; min x %.2e max x %.6f'
      % (cap.max(), (cap > 0).sum(), n, tv.max(), mc.max(), x.min(), x.max()))
print('stored min depth %r; most negative exact bound %r (triple %s)' % (float(d.min()), float(bound.min()),
      T[int(np.argmin(bound))].tolist()))
print('stored depth above exact bound by up to %.3e; #triples with stored depth > exact bound + 1e-9: %d'
      % (float(np.max(d - bound)), int((d > bound + 1e-9).sum())))
srcH = glob.glob(os.path.join(ROOT, 'sources/BoxQP_instances-master/*/%s.in' % name))[0]
tok = open(srcH).read().split()
v = np.array(tok[1:], float)
H, g = -v[n:].reshape(n, n) / 2, -v[:n]
fc = np.trace(H) / 3 + (H.sum() - np.trace(H)) / 4 + g.sum() / 2
opt = -6267.45
gap = opt - info['B_safe']
for label, eps in (('stored', -float(d.min())), ('exact-bound', -float(min(d.min(), bound.min())))):
    gain = eps * (fc - info['B']) / (1 + eps)
    print('%-12s eps %.3e gain/gap %.6f  (+margin %.6f)' % (label, eps, gain / gap,
          (gain + info['B'] - info['B_safe']) / gap))
