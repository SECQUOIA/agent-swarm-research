"""Create cactus instances of hard triangles sharing vertices (instances.cactus_instance).
Usage: python make_cactus.py m seed"""
import sys
sys.path.insert(0, '.')
from instances import load_pool, cactus_instance, save_json, write_lp
m, seed = int(sys.argv[1]), int(sys.argv[2])
pool = load_pool(['../data/pool_hard3.jsonl'])
H, g, cliques = cactus_instance(m, pool, seed=seed)
tag = 'cactus_m%d_s%d' % (m, seed)
save_json('../data/%s.json' % tag, H, g, {'m': m, 'seed': seed, 'pool': 'pool_hard3.jsonl',
                                         'cliques': [list(c) for c in cliques]})
write_lp('../data/%s.lp' % tag, H, g, tag)
print(tag, 'n', len(g), 'plus diagonals', int((H.diagonal() > 0).sum()))
