"""Create chain instances of hard triangles.  Usage: python make_chain.py m eta seed [tree]"""
import sys
sys.path.insert(0, '.')
from instances import load_pool, chain_instance, save_json, write_lp
m, eta, seed = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
tree = sys.argv[4] if len(sys.argv) > 4 else 'path'
pool = load_pool(['../data/pool_hard3.jsonl'])
H, g, cliques = chain_instance(m, pool, eta=eta, seed=seed, tree=tree)
tag = 'chain_m%d_e%g_s%d%s' % (m, eta, seed, '' if tree == 'path' else '_' + tree)
save_json('../data/%s.json' % tag, H, g, {'m': m, 'eta': eta, 'seed': seed, 'tree': tree, 'pool': 'pool_hard3.jsonl',
                                         'cliques': [list(c) for c in cliques]})
write_lp('../data/%s.lp' % tag, H, g, tag)
print(tag, 'n', 3 * m, 'plus diagonals', int((H.diagonal() > 0).sum()))
