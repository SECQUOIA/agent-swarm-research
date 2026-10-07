"""Create random sparse 'plus' instances (instances.plus_instance; all data integer).
Usage: python make_plus.py n k pplus dmax seed"""
import sys
sys.path.insert(0, '.')
from instances import plus_instance, save_json, write_lp
n, k, pplus, dmax, seed = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
H, g, edges, cliques = plus_instance(n, k, pplus, seed, dmax=dmax)
tag = 'plus_n%d_k%d_pp%g_d%d_s%d' % (n, k, pplus, dmax, seed)
save_json('../data/%s.json' % tag, H, g, {'n': n, 'k': k, 'pplus': pplus, 'dmax': dmax, 'seed': seed,
                                         'cliques': [list(c) for c in cliques]})
write_lp('../data/%s.lp' % tag, H, g, tag)
print(tag, 'plus diag', int((H.diagonal() > 0).sum()), 'of', n)
