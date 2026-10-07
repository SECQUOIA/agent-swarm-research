"""Khajavirad's LMIs (17) on ALL triples of a given kind for a spar instance, with shared
auxiliary moments (so the result is not covered by Lemma 3).

Builds B (dense Shor + McCormick + triangle separation to convergence, violation
> 1e-7), then adds K (8 level-3 RLT, 12 rotated cones, 6 order-3 blocks per triple) to
every triple of the chosen set and re-solves, re-separating triangles until none is
violated.  Sets: 'plus' = triples of plus coordinates (H_ii > 0); 'all' = all triples.
Usage: python kall.py spar_name plus|all out.json"""
import glob
import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from relax import Relax, read_boxqp, separate_triangles

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../sources/BoxQP_instances-master/')


def tri_loop(R, tag, log):
    for rnd in range(60):
        res = R.solve('clarabel')
        cuts, mv = separate_triangles(res['xv'], res['Y'], tol=1e-7, cap=5000)
        cuts = [c for c in cuts if c not in R.tri_added]
        log.append({'stage': tag, 'round': rnd, 'pobj': res['pobj'], 'safe': res['safe'], 'status': res['status'],
                    'pinf': res['pinf'], 't': res['time_solve'], 'newtri': len(cuts), 'size': R.size()})
        print(json.dumps(log[-1]), flush=True)
        if not cuts:
            return res
        for c in cuts:
            R.add_triangle(*c)
    return res


def main():
    name, kind, out = sys.argv[1], sys.argv[2], sys.argv[3]
    H, g = read_boxqp(glob.glob(D + '*/' + name + '.in')[0])
    n = len(g)
    R = Relax(H, g, name)
    log = []
    t0 = time.time()
    tri_loop(R, 'B', log)
    plus = [i for i in range(n) if H[i, i] > 0]
    trip = list(itertools.combinations(plus if kind == 'plus' else range(n), 3))
    for T in trip:
        R.add_K(T)
    res = tri_loop(R, 'K_' + kind, log)
    opt = None
    for line in open(D + 'README.txt'):
        t = line.split()
        if len(t) == 2 and t[0] == name:
            opt = -float(t[1])
    rec = {'name': name, 'kind': kind, 'triples': len(trip), 'opt_min': opt, 'B': log[[l['stage'] for l in log].index('K_' + kind) - 1]['pobj'],
           'B_safe': log[[l['stage'] for l in log].index('K_' + kind) - 1]['safe'], 'K': res['pobj'], 'K_safe': res['safe'],
           'status': res['status'], 'pinf': res['pinf'], 'time_total': time.time() - t0, 'log': log}
    json.dump(rec, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
