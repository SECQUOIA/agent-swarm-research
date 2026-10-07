"""Create hard-triangle instances (JSON for the relaxations, LP for Gurobi).
Usage: python make_ht.py kind n k seed   (pool: ../data/pool_hard3.jsonl; kind is only a label)"""
import sys, glob
sys.path.insert(0, '.')
from instances import load_pool, hard_triangle_instance, save_json, write_lp
kind, n, k, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
pool = load_pool(['../data/pool_hard3.jsonl'])
H, g, edges, cliques = hard_triangle_instance(n, pool, k=k, seed=seed)
tag = 'ht_%s_n%d_k%d_s%d' % (kind, n, k, seed)
save_json('../data/%s.json' % tag, H, g, {'kind': kind, 'n': n, 'k': k, 'seed': seed, 'pool_size': len(pool),
                                         'cliques': [list(c) for c in cliques]})
write_lp('../data/%s.lp' % tag, H, g, tag)
print(tag, 'pool', len(pool), 'plus diag', int((H.diagonal() > 0).sum()), 'of', n)
