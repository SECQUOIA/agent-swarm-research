import sys, json, numpy as np
sys.path.insert(0, '.')
from instances import plus_instance, write_lp, save_json
from gurobi_solve import solve
import subprocess
n, k, pplus, dmax, seed = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
tag = 'p%d_k%d_pp%g_d%d_s%d' % (n, k, pplus, dmax, seed)
H, g, edges, cliques = plus_instance(n, k, pplus, seed, dmax=dmax)
save_json('../data/tmp/%s.json' % tag, H, g, {'n': n, 'k': k, 'pplus': pplus, 'dmax': dmax, 'seed': seed, 'cliques': [list(c) for c in cliques]})
write_lp('../data/tmp/%s.lp' % tag, H, g, tag)
st, ub, lb, out = solve('../data/tmp/%s.lp' % tag, 300, 1)
print(tag, 'gurobi', st, ub, lb, flush=True)
subprocess.run(['python', 'driver.py', '--json', '../data/tmp/%s.json' % tag, '--methods', sys.argv[6] if len(sys.argv) > 6 else 'X',
                '--log', '../data/tmp/%s.log' % tag, '--max_rounds', '8'])
