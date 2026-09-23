"""Root box for probe C: SCIP root node (presolve + FBBT + cuts), OBBT off, no objective limit."""
import sys, json, os
from multiprocessing import Pool
from common import solve, global_bounds
def job(n):
    try:
        m, o = solve(n, {'limits/nodes': 1, 'limits/time': 30, 'propagating/obbt/freq': -1})
        json.dump(global_bounds(m), open('bounds/%s.json' % n, 'w'))
    except Exception as e:
        print(n, e)
if __name__ == '__main__':
    with Pool(int(sys.argv[2]), maxtasksperchild=1) as p:
        p.map(job, open(sys.argv[1]).read().split(), chunksize=1)
