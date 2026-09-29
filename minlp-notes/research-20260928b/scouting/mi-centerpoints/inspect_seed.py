import numpy as np, sys
from midepth import *
from search_random import rand_instance
for seed in map(int, sys.argv[1:]):
    rng = np.random.default_rng(seed)
    P = rand_instance(rng)
    zs, F = slice_polytope(P)
    S = MISet(F, zs, ntheta=240, nphi=121)
    val, k, y = S.best_point(refine_depth=True, starts=6)
    print("seed", seed, "zs", zs, "vols/nu", np.round(S.v / S.nu, 4), "F", val, "k", k, "y", y)
    # per-fiber best depths (centroid) for reference
    for kk, V in zip(S.z, S.F):
        c = centroid(V)
        print("  fiber", kk, "centroid depth/nu", S.depth(kk, c) / S.nu)
