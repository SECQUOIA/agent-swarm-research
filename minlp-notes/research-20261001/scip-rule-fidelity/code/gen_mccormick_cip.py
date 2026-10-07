"""Write the random bilinear instances of research-20260928b/sfree/code/exp_mccormick.py as .cip files.

The generator and the seeding are those of exp_mccormick.py: module rng reset to
default_rng(SEED), then make_instance(*SIZE) is called once per trial, so trial t here is
trial t of the earlier runs (exp_mccormick_11*.json: SEED 11, 4 4 3; exp_mccormick_12_big*.json:
SEED 12, 6 8 4). Each instance: min c^T x, A x <= b (McCormick rows of every product and nlin
random rows), bounds, and w_e = x_i x_j as nonlinear equality constraints.
Usage: python3 gen_mccormick_cip.py SEED NTRIALS OUTDIR [p npairs nlin]
"""
import os, sys, json
import numpy as np
SFREE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../research-20260928b/sfree/code')
sys.path.insert(0, SFREE)
import exp_mccormick as E
import pyscipopt as ps

seed, T, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
SIZE = tuple(int(a) for a in sys.argv[4:7]) if len(sys.argv) > 6 else (4, 4, 3)
os.makedirs(out, exist_ok=True)
E.rng = np.random.default_rng(seed)
meta = []
for t in range(T):
    I = E.make_instance(*SIZE)
    m = ps.Model(); m.hideOutput()
    n = I['n']
    names = ['x%d' % v for v in range(I['p'])] + ['w%d_%d' % pr for pr in I['pairs']]
    xs = [m.addVar(name=names[v], lb=I['lo'][v], ub=I['hi'][v]) for v in range(n)]
    for k in range(len(I['b'])):
        m.addCons(ps.quicksum(float(I['A'][k, v]) * xs[v] for v in range(n) if I['A'][k, v] != 0) <= float(I['b'][k]),
                  name='r%d' % k)
    for e, (i, j) in enumerate(I['pairs']):
        m.addCons(xs[I['p'] + e] == xs[i] * xs[j], name='bil%d' % e)
    m.setObjective(ps.quicksum(float(I['c'][v]) * xs[v] for v in range(n)))
    fn = os.path.join(out, 'mc_s%d_t%03d.cip' % (seed, t))
    m.writeProblem(fn, verbose=False)
    meta.append(dict(file=os.path.basename(fn), trial=t, n=n, pairs=[[int(a), int(b)] for a, b in I['pairs']], p=I['p']))
json.dump(dict(seed=seed, size=SIZE, instances=meta), open(os.path.join(out, 'meta_s%d.json' % seed), 'w'), indent=1)
print('wrote', len(meta), 'instances to', out)
