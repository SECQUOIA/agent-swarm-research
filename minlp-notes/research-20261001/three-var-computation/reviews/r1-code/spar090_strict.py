"""Reviewer r1: re-audit spar090-075-1 with the triangle inequalities enforced strictly.

The stream's audit point violates one triangle by 3.15e-6 and the deepest triple is that
triple. Here B is re-solved, starting from the stream's checkpointed triangles, adding
every triangle violated by more than 1e-8 until none is (at most 8 rounds); then the
QPB3 depth of every triple and the Lemma 3 gain term are recomputed. Uses the stream's
model builder (relax.Relax) and depth routine (hullsep.depth) because this re-runs the
stream's check with one change; the deepest triples are re-checked independently by
reviews/r1-code/lift_depth.py.
Run from three-var-computation/: python reviews/r1-code/spar090_strict.py
"""
import glob
import json
import os
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'code'))
from relax import Relax, read_boxqp, separate_triangles, triple_moment_matrices, all_triples  # noqa: E402
import hullsep  # noqa: E402

name = 'spar090-075-1'
OUT = os.path.join(ROOT, 'reviews/r1-logs/spar090_strict')
H, g = read_boxqp(glob.glob(os.path.join(ROOT, 'sources/BoxQP_instances-master/*/%s.in' % name))[0])
n = len(g)
opt = None
for line in open(os.path.join(ROOT, 'sources/BoxQP_instances-master/README.txt')):
    t = line.split()
    if len(t) == 2 and t[0] == name:
        opt = -float(t[1])
t0 = time.time()
if os.path.exists(OUT + '.base.npz'):
    z = np.load(OUT + '.base.npz')
    x, Y, info = z['x'], z['Y'], json.loads(str(z['info']))
else:
    R = Relax(H, g, name)
    for c in json.load(open(os.path.join(ROOT, 'logs/spar_audit/%s.json.tri.json' % name))):
        R.add_triangle(*c)
    rounds = []
    for rnd in range(8):
        res = R.solve('clarabel')
        cuts, mv = separate_triangles(res['xv'], res['Y'], tol=1e-8, cap=None)
        cuts = [c for c in cuts if c not in R.tri_added]
        rounds.append({'pobj': res['pobj'], 'safe': res['safe'], 'status': res['status'], 'pinf': res['pinf'],
                       't': res['time_solve'], 'newtri': len(cuts), 'maxviol': mv})
        print(rounds[-1], flush=True)
        if not cuts:
            break
        for c in cuts:
            R.add_triangle(*c)
    x, Y = res['xv'], res['Y']
    info = {'B': res['pobj'], 'B_safe': res['safe'], 'status': res['status'], 'pinf': res['pinf'],
            'max_triangle_violation': rounds[-1]['maxviol'], 'tri': len(R.tri_added), 'rounds': rounds}
    np.savez(OUT + '.base.npz', x=x, Y=Y, info=json.dumps(info))
T = all_triples(n)
M = triple_moment_matrices(x, Y, T)
t1 = time.time()
d = np.array([hullsep.depth(Mi)[0] for Mi in M])
np.savez(OUT + '.depth.npz', depths=d)
fc = float(np.trace(H) / 3 + (H.sum() - np.trace(H)) / 4 + g.sum() / 2)
eps = max(0.0, -float(d.min()))
gain = eps * (fc - info['B']) / (1 + eps)
gap = opt - info['B_safe']
order = np.argsort(d)[:5]
rec = dict(info, name=name, opt=opt, gap_safe=gap, min_depth=float(d.min()),
           deepest=[(T[i].tolist(), float(d[i])) for i in order],
           count_depth_lt_1e_6=int((d < -1e-6).sum()), count_depth_lt_1e_7=int((d < -1e-7).sum()),
           gain_term=gain, gain_over_gap=gain / gap, gain_plus_margin_over_gap=(gain + info['B'] - info['B_safe']) / gap,
           time_depth=time.time() - t1, time_total=time.time() - t0)
rec.pop('rounds', None)
json.dump(rec, open(OUT + '.json', 'w'), indent=1)
print(json.dumps(rec, indent=1))
