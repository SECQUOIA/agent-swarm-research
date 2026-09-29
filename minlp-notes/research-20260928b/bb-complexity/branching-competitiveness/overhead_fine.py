"""Fine-grid guillotine DP for the pinwheel instance (overhead_search seed 2, t = 149).
Usage: python3 overhead_fine.py"""
import numpy as np
from nd_sep import Ftable, TOL
from search_sep2d import build, rand_params
from overhead_search import dp

rng = np.random.default_rng(2)
for t in range(150):
    G = int(rng.integers(8, 13)); g = np.linspace(0, 1, G)
    params = rand_params(rng, int(rng.integers(3, 8))); eps = 10 ** rng.uniform(-6, -2)
Is = build(params, eps)
for G in (12, 23, 45, 67, 89):
    g1 = np.array(sorted(set(np.linspace(0, 1, G)) | set(float(x) for x in Is[0].x)))
    g2 = np.array(sorted(set(np.linspace(0, 1, G)) | set(float(x) for x in Is[1].x)))
    F1, F2 = Ftable(Is[0], g1), Ftable(Is[1], g2)
    V = (F1[:, :, None, None] + F2[None, None, :, :] >= -TOL).astype(np.uint8)
    print(f"uniform G={G:3d} (+knots): grid sizes {len(g1)},{len(g2)}  N_guill_grid = {dp(V)}", flush=True)
