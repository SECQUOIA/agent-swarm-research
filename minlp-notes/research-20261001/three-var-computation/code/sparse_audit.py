"""Triple-level audit of the base relaxation B on a sparse (chordal-pattern) JSON instance.

B = Shor on each maximal clique + McCormick on pattern pairs + Y_ii <= x_i +
triangle inequalities on clique triples (separated, violation > 1e-7, until none).
Then for every clique triple T: QPB3 depth delta_T (hullsep.depth) and the
family minimum over the 24 orientations.  With eps = max(0, -min delta_T),
Lemma 3 of note.md bounds the gain of any constraints valid for QPB3 on clique
triples (per-triple auxiliaries) by eps * (f(y_c) - f(y*)) / (1 + eps), where
y_c are the uniform moments restricted to the pattern.
The B solution is saved to <out>.base.npz (key 'x' is used by ub_local.py).
Usage: python sparse_audit.py instance.json out.json"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from relax import Relax, separate_triangles, triple_moment_matrices
from instances import load_json
from spar_audit import family_min
import hullsep


def main():
    path, out = sys.argv[1], sys.argv[2]
    H, g, meta = load_json(path)
    t0 = time.time()
    R = Relax(H, g, path, cliques=meta['cliques'])
    rounds = []
    for rnd in range(100):
        res = R.solve('clarabel')
        cuts, mv = separate_triangles(res['xv'], res['Y'], tol=1e-7, cap=None, triples=R.triples)
        cuts = [c for c in cuts if c not in R.tri_added]
        rounds.append({'pobj': res['pobj'], 'safe': res['safe'], 'status': res['status'], 't': res['time_solve'],
                       'newtri': len(cuts)})
        if not cuts:
            break
        for c in cuts:
            R.add_triangle(*c)
    t_base = time.time() - t0
    x, Y = res['xv'], res['Y']
    np.savez(out + '.base.npz', x=x, Y=np.nan_to_num(Y))
    T = R.triples
    t1 = time.time()
    M = triple_moment_matrices(x, Y, T)
    depths = np.array([hullsep.depth(Mi)[0] for Mi in M])
    t_hull = time.time() - t1
    fam_min, fam_nviol = family_min(x, Y, T)
    n = len(g)
    f_c = float(np.trace(H) / 3 + (H.sum() - np.trace(H)) / 4 + g.sum() / 2)
    eps = max(0.0, -float(depths.min()))
    rec = {'instance': path, 'n': n, 'cliques': len(meta['cliques']), 'triples': len(T),
           'plus_diag': int((np.diag(H) > 0).sum()), 'B': res['pobj'], 'B_safe': res['safe'],
           'status': res['status'], 'pinf': res['pinf'], 'tri': len(R.tri_added), 'rounds': len(rounds),
           'time_base': t_base, 'size': R.size(), 'min_depth': float(depths.min()),
           'count_depth_lt_1e-6': int((depths < -1e-6).sum()), 'count_depth_lt_1e-5': int((depths < -1e-5).sum()),
           'family_stqp_min': fam_min, 'family_violated_pairs_1e-6': fam_nviol, 'f_uniform': f_c, 'eps': eps,
           'max_triple_level_improvement': eps * (f_c - res['pobj']) / (1 + eps), 'time_hull_tests': t_hull,
           'interior': int(((x > 1e-6) & (x < 1 - 1e-6)).sum())}
    json.dump(rec, open(out, 'w'), indent=1)
    print(json.dumps({k: v for k, v in rec.items() if k != 'size'}), flush=True)


if __name__ == '__main__':
    main()
