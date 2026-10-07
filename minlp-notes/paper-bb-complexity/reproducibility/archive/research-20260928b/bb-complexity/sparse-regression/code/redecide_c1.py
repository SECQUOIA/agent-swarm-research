"""Exact re-decision of C1 at S* (no cap) for stored instances of exp_c1.py.
usage: redecide_c1.py OUT nproc FILE [FILE ...]   (decides every row whose c1 == 'capped')
"""
import os, sys, json, time
for v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]: os.environ[v] = "1"
import numpy as np
from multiprocessing import Pool
from core import instance, decide_c1_exact
def job(r):
    t = time.time()
    X, y, lam, S = (instance(r['n'], r['p'], r['k'], seed=r['seed']) if r['rule'] == 'sqrtn'
                    else instance(r['n'], r['p'], r['k'], seed=r['seed'], tau0=float(r['rule'])))
    d = decide_c1_exact(X, y, lam, r['k'], S)
    return dict(p=r['p'], k=r['k'], n=r['n'], rule=r['rule'], seed=r['seed'], old_c1=r['c1'], **d, time=time.time() - t)
if __name__ == '__main__':
    out, nproc = sys.argv[1], int(sys.argv[2])
    rows, seen = [], set()
    for fn in sys.argv[3:]:
        for l in open(fn):
            r = json.loads(l); key = (r['p'], r['k'], r['rule'], r['n'], r['seed'])
            if key in seen: continue
            seen.add(key)
            if r['c1'] == 'capped': rows.append(r)
    rows.sort(key=lambda r: r['p'])
    print(len(rows), 'rows to decide', flush=True)
    with Pool(nproc) as pool, open(out, 'w') as f:
        for res in pool.imap_unordered(job, rows):
            f.write(json.dumps(res) + '\n'); f.flush()
