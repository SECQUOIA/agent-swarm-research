"""Where does the forced-in half start failing at n = 800?  Same conditional simulation as c1_large.py,
but lower tau^2 and the restricted forced-in relaxation over S + top-400 nulls (upper bound on r(0,{j}))."""
import os, sys, json
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"):
    os.environ[v] = "1"
import numpy as np
import c1_large as C
C.MR = 400

def job(args):
    return C.instance(*args)

if __name__ == '__main__':
    from multiprocessing import Pool
    n, k = 800, 10; jobs = []
    for p in (10 ** 6, 10 ** 9):
        for lam in (np.sqrt(n), 90.0):
            c1 = 2 * np.log(p * lam / n)
            for d in (-20, -16, -12, -8):
                if c1 + d <= 1: continue
                for s in range(5):
                    jobs.append((n, p, k, lam, round(c1 + d, 2), 55555 + 1000 * s + int(10 * (c1 + d))))
    with Pool(5) as pool, open(sys.argv[1], 'w') as f:
        for res in pool.imap_unordered(job, jobs):
            if res is not None:
                f.write(json.dumps(res) + '\n'); f.flush()
