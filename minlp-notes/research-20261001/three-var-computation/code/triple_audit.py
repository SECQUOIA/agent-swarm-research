"""Triple-level audit of the base relaxation B on a BoxQP instance.

Solves B = Shor + RLT + TRI (triangle separation to convergence), then for every
triple T computes the QPB3 depth delta_T (hullsep.depth) and the family StQP
minimum over the 24 orientations.  With eps = max_T max(0, -delta_T), the point
    y_eps = (y* + eps*y_c) / (1 + eps),
where y* is the B solution and y_c the moments of the uniform distribution on
[0,1]^n, is feasible for B (convex combination of B-feasible points) and every
triple moment matrix of y_eps lies in QPB3.  Hence adding ANY constraints that
are valid for QPB3 on all triples (with per-triple auxiliaries: X, F, A, and K
with unshared auxiliaries) can raise the bound by at most
    eps * (f(y_c) - f(y*)) / (1 + eps).
Usage: python triple_audit.py spar_name out.json"""
import glob
import json
import sys
import time

import numpy as np

sys.path.insert(0, '.')
from relax import Relax, read_boxqp, separate_triangles, separate_family, triple_moment_matrices, all_triples
import hullsep

D = '../sources/BoxQP_instances-master/'


def main():
    name, out = sys.argv[1], sys.argv[2]
    H, g = read_boxqp(glob.glob(D + '*/' + name + '.in')[0])
    n = len(g)
    R = Relax(H, g, name)
    for rnd in range(60):
        res = R.solve('clarabel')
        cuts, mv = separate_triangles(res['xv'], res['Y'], tol=1e-7, cap=5000)
        if not cuts:
            break
        for c in cuts:
            R.add_triangle(*c)
    x, Y = res['xv'], res['Y']
    T = all_triples(n)
    t0 = time.time()
    M = triple_moment_matrices(x, Y, T)
    depths = np.array([hullsep.depth(Mi)[0] for Mi in M])
    t_hull = time.time() - t0
    fam = separate_family(x, Y, T, tol=-np.inf)   # tol=-inf: record the minimum over all
    fam_min = min(v[2] for v in fam) if fam else 0.0
    f_star = res['pobj']
    f_c = float(np.trace(H) / 3 + (H.sum() - np.trace(H)) / 4 + g.sum() / 2)
    eps = max(0.0, -depths.min())
    rec = {'name': name, 'n': n, 'B': f_star, 'B_safe': res['safe'], 'status': res['status'],
           'pinf': res['pinf'], 'triples': len(T), 'min_depth': float(depths.min()),
           'count_depth_lt_1e-6': int((depths < -1e-6).sum()), 'count_depth_lt_1e-8': int((depths < -1e-8).sum()),
           'family_stqp_min': fam_min, 'f_uniform': f_c, 'eps': eps,
           'max_triple_level_improvement': eps * (f_c - f_star) / (1 + eps), 'time_hull_tests': t_hull,
           'interior': int(((x > 1e-6) & (x < 1 - 1e-6)).sum())}
    json.dump(rec, open(out, 'w'), indent=1)
    print(json.dumps(rec))


if __name__ == '__main__':
    main()
