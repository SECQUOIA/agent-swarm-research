"""Default SCIP pass on the candidate pool (120 s, 1 thread) to pick probe instances."""
import sys, json, pandas as pd
from multiprocessing import Pool
from common import solve

def job(name):
    try:
        _, o = solve(name, {'limits/time': 120})
    except Exception as e:
        o = dict(name=name, status='error:' + str(e)[:80])
    print(json.dumps(o), flush=True)
    return o

if __name__ == '__main__':
    names = list(pd.read_csv('pool.csv').name)
    with Pool(34, maxtasksperchild=1) as p:
        res = p.map(job, names, chunksize=1)
    pd.DataFrame(res).to_csv('pass0.csv', index=False)
