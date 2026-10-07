import sys, time, numpy as np
sys.path.insert(0, '.')
from relax import Relax, separate_triangles, separate_family, triple_moment_matrices
from instances import plus_instance
import hullsep
n, k, pplus, seed = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
H, g, edges, cliques = plus_instance(n, k, pplus, seed)
R = Relax(H, g, 'plus', cliques=cliques)
for rnd in range(30):
    res = R.solve('clarabel')
    cuts, mv = separate_triangles(res['xv'], res['Y'], tol=1e-6, cap=2000, triples=R.triples)
    print(rnd, res['status'], 'obj %.6f safe %.6f' % (res['pobj'], res['safe']), 'iters', res['iters'],
          'tsolve %.2f' % res['time_solve'], 'newtri', len(cuts), flush=True)
    if not cuts: break
    for c in cuts: R.add_triangle(*c)
x, Y = res['xv'], res['Y']
fam = separate_family(x, Y, R.triples)
print('triples', len(R.triples), 'family-violated (triple,orient) pairs', len(fam), 'triples', len(set(f[0] for f in fam)))
M = triple_moment_matrices(x, Y, R.triples)
t = time.time()
d = [hullsep.depth(Mi)[0] for Mi in M]
print('hull test time %.2f' % (time.time() - t), 'violated', sum(1 for v in d if v < -1e-6), 'min depth', min(d))
