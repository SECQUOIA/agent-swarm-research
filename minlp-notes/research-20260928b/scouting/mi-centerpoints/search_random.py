import numpy as np, sys, time
from multiprocessing import Pool
from midepth import *

def rand_instance(rng):
    m = rng.integers(2, 5)   # levels 0..m -> m+1 fibers (3..5)
    pts = []
    for j in range(m + 1):
        c = rng.normal(size=2) * rng.uniform(0, 1.5)
        M = rng.normal(size=(2, 2))
        s = rng.uniform(0.2, 1.5) if rng.random() < 0.8 else rng.uniform(0.01, 0.2)
        npts = rng.integers(3, 6)
        for _ in range(npts):
            u = rng.normal(size=2); u /= np.linalg.norm(u)
            pts.append([j, *(c + s * (M @ u))])
    # optional off-level points
    for _ in range(rng.integers(0, 4)):
        z = rng.uniform(0, m)
        pts.append([z, *(rng.normal(size=2) * rng.uniform(0, 2))])
    return np.array(pts)

def run(seed):
    rng = np.random.default_rng(seed)
    P = rand_instance(rng)
    try:
        zs, F = slice_polytope(P)
    except Exception:
        return None
    if len(F) < 3:
        return None
    S = MISet(F, zs, ntheta=90, nphi=41)
    val, k, y = S.best_point(refine_depth=False, starts=2)
    return (val, seed, len(F))

if __name__ == "__main__":
    N = int(sys.argv[1]); off = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    t = time.time()
    with Pool(34) as p:
        res = [r for r in p.map(run, range(off, off + N)) if r is not None]
    res.sort()
    print("time", time.time() - t, "n", len(res))
    for r in res[:15]:
        print(r)
    vals = np.array([r[0] for r in res])
    print("quantiles", np.quantile(vals, [0, 0.01, 0.1, 0.5]))
