"""Adversarial search (n=1, d=2) for small Oertel radius F(S) among instances whose
fibers all carry at least a fraction `share` of the mixed-integer volume.

Instance = point cloud in R^3 (z in {0..m} plus optional off-level points); fibers are
integer slices of its convex hull.  (1+lambda) evolution strategy, parallel.
"""
import numpy as np, sys, time
from multiprocessing import Pool
from midepth import *

m = int(sys.argv[1]); share = float(sys.argv[2]); seed = int(sys.argv[3]); rounds = int(sys.argv[4])
PER = 4  # points per level

def build(theta):
    P = theta.reshape(-1, 2)
    pts = []
    for j in range(m + 1):
        for i in range(PER):
            pts.append([j, *P[j * PER + i]])
    return np.array(pts)

def F_of(theta, fine=False):
    try:
        zs, F = slice_polytope(build(theta))
    except Exception:
        return 1.0
    if len(F) != m + 1:
        return 1.0
    S = MISet(F, zs, ntheta=240 if fine else 72, nphi=121 if fine else 33)
    if (S.v / S.nu).min() < share:
        return 1.0 + (share - (S.v / S.nu).min())
    val, k, y = S.best_point(refine_depth=fine, starts=4 if fine else 2)
    return val

if __name__ == "__main__":
    rng = np.random.default_rng(seed)
    best, bestv = None, 9
    with Pool(34) as pool:
        # random init
        cands = [rng.normal(size=(m + 1) * PER * 2) for _ in range(68)]
        vals = pool.map(F_of, cands)
        i = int(np.argmin(vals)); best, bestv = cands[i], vals[i]
        sigma = 0.3
        for r in range(rounds):
            cands = [best + sigma * rng.normal(size=best.shape) * (rng.random(best.shape) < 0.5) for _ in range(34)]
            vals = pool.map(F_of, cands)
            i = int(np.argmin(vals))
            if vals[i] < bestv:
                best, bestv = cands[i], vals[i]; sigma *= 1.1
            else:
                sigma *= 0.8
            print(f"round {r} best {bestv:.5f} sigma {sigma:.3f}", flush=True)
    fine = F_of(best, fine=True)
    zs, F = slice_polytope(build(best))
    S = MISet(F, zs)
    print("final coarse", bestv, "fine", fine, "shares", np.round(S.v / S.nu, 4))
    np.save(f"adv_m{m}_s{share}_seed{seed}.npy", best)
