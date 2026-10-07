"""Audit the final point of the selective family method F on a chain instance.

Runs B and then F (family blocks by separation) with Clarabel, as in driver.py,
then computes the QPB3 depth of every triangle at the final F point y_F.  With
eps = max(0, -min depth), the point (y_F + eps*y_c)/(1+eps), y_c the uniform
moments on the cube, is feasible for B, for the added family blocks (convex
combination of feasible points) and has every triangle moment matrix in QPB3.
Hence the exact lift X on ALL triangles (added to B + F) can raise the bound by
at most eps*(f(y_c) - f(y_F))/(1+eps), up to the solver accuracy of y_F.
Usage: python chain_audit.py instance.json out.json"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, '.')
from driver import Runner
from relax import Relax, triple_moment_matrices, separate_family
from instances import load_json
import hullsep


def main():
    path, out = sys.argv[1], sys.argv[2]
    H, g, meta = load_json(path)
    R = Relax(H, g, path, cliques=meta['cliques'])
    run = Runner(R, 'clarabel', out + '.runlog.jsonl', max_rounds=25)
    open(out + '.runlog.jsonl', 'w').close()
    Rb, resb = run.base()
    RF, resF = run.run('F', Rb, resb)
    x, Y = resF['xv'], resF['Y']
    T = R.triples
    t0 = time.time()
    M = triple_moment_matrices(x, Y, T)
    depths = np.array([hullsep.depth(Mi)[0] for Mi in M])
    fam = separate_family(x, Y, T, tol=-np.inf)
    fam_min = min(v[2] for v in fam)
    f_F = resF['pobj']
    n = len(g)
    # uniform moments: E x_i = 1/2, E x_i^2 = 1/3, E x_i x_j = 1/4
    f_c = float(np.trace(H) / 3 + (H.sum() - np.trace(H)) / 4 + g.sum() / 2)
    eps = max(0.0, -float(depths.min()))
    rec = {'instance': path, 'n': n, 'triangles': len(T), 'F_pobj': f_F, 'F_safe': resF['safe'],
           'F_status': resF['status'], 'F_pinf': resF['pinf'], 'F_blocks': len(RF.F_added),
           'min_depth': float(depths.min()), 'count_depth_lt_1e-6': int((depths < -1e-6).sum()),
           'count_depth_lt_1e-5': int((depths < -1e-5).sum()), 'family_stqp_min': fam_min,
           'f_uniform': f_c, 'eps': eps, 'max_X_improvement': eps * (f_c - f_F) / (1 + eps),
           'time_hull_tests': time.time() - t0}
    # diagnostics for the five deepest triples (added 2026-10-02 by the second author)
    worst = []
    for i in np.argsort(depths)[:5]:
        Ti = T[i:i + 1]
        fmin = min(float(v[2]) for v in separate_family(x, Y, Ti, tol=-np.inf))
        Mi = M[i]
        xi = Mi[0, 1:]
        Yi = Mi[1:, 1:]
        tri = max(Yi[0, 1] + Yi[0, 2] - xi[0] - Yi[1, 2], Yi[0, 1] + Yi[1, 2] - xi[1] - Yi[0, 2],
                  Yi[0, 2] + Yi[1, 2] - xi[2] - Yi[0, 1], xi.sum() - Yi[0, 1] - Yi[0, 2] - Yi[1, 2] - 1)
        worst.append({'triple': [int(t) for t in T[i]], 'depth': float(depths[i]), 'family_min': fmin,
                      'max_triangle_violation': float(tri), 'min_eig_M': float(np.linalg.eigvalsh(Mi)[0]),
                      'M': Mi.tolist()})
    rec['worst'] = worst
    np.savez(out + '.F.npz', x=x, Y=np.nan_to_num(Y))
    json.dump(rec, open(out, 'w'), indent=1)
    print(json.dumps(rec))


if __name__ == '__main__':
    main()
