import sys, json, numpy as np, time
sys.path.insert(0, '.')
from instances import plus_instance, write_lp, ktree
from gurobi_solve import solve
from relax import Relax, separate_triangles
def base(R):
    for rnd in range(50):
        res = R.solve('clarabel')
        cuts, mv = separate_triangles(res['xv'], res['Y'], tol=1e-6, cap=2000, triples=R.triples)
        if not cuts: return res
        for c in cuts: R.add_triangle(*c)
    return res
n, k, dmax, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
H, g, edges, cliques = plus_instance(n, max(k, 2), 1.0, seed, dmax=dmax)
if k == 0:  # dense: complete graph with same diag law
    rng = np.random.default_rng(seed + 1000)
    for i in range(n):
        for j in range(i+1, n):
            H[i, j] = H[j, i] = rng.integers(-50, 51)
    cliques = None
tag = 'g_n%d_k%d_d%d_s%d' % (n, k, dmax, seed)
write_lp('../data/tmp/%s.lp' % tag, H, g, tag)
st, ub, lb, out = solve('../data/tmp/%s.lp' % tag, 120, 1)
R = Relax(H, g, tag, cliques=cliques)
res = base(R)
x = res['xv']
print(tag, 'opt', ub, lb, 'base %.4f' % res['pobj'], 'gap %.4f' % (ub - res['pobj']), 'interior', int(((x > 1e-4) & (x < 1-1e-4)).sum()), flush=True)
