"""Replay overhead_search.py up to a given separable instance and print the optimal
non-guillotine grid partition, its free cuts, and the instance.
Usage: python3 overhead_replay.py SEED T [knots]"""
import sys
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from nd_sep import Ftable, TOL
from search_sep2d import build, rand_params
from poly2d import Poly2
from overhead_search import dp

seed, target = int(sys.argv[1]), int(sys.argv[2])
knots = len(sys.argv) > 3 and sys.argv[3] == "knots"
rng = np.random.default_rng(seed)
for t in range(target + 1):
    G = int(rng.integers(8, 13)); g = np.linspace(0, 1, G)
    params = rand_params(rng, int(rng.integers(3, 8))); eps = 10 ** rng.uniform(-6, -2)
    if t == target:
        Is = build(params, eps)
        g1 = np.array(sorted(set(g) | set(float(x) for x in Is[0].x))) if knots else g
        g2 = np.array(sorted(set(g) | set(float(x) for x in Is[1].x))) if knots else g
        F1, F2 = Ftable(Is[0], g1), Ftable(Is[1], g2)
        V = (F1[:, :, None, None] + F2[None, None, :, :] >= -TOL).astype(np.uint8)
G1, G2 = len(g1), len(g2)
print("grid sizes", G1, G2, "eps = %.3g" % eps, "N_guill_grid =", dp(V))
boxes = [(a, b, c, d) for a in range(G1) for b in range(a + 1, G1) for c in range(G2) for d in range(c + 1, G2) if V[a, b, c, d]]
A = lil_matrix(((G1 - 1) * (G2 - 1), len(boxes)))
for k, (a, b, c, d) in enumerate(boxes):
    for i in range(a, b):
        for j in range(c, d):
            A[i * (G2 - 1) + j, k] = 1
res = milp(np.ones(len(boxes)), constraints=[LinearConstraint(A.tocsr(), 1, 1)], integrality=np.ones(len(boxes)), bounds=Bounds(0, 1))
sol = [boxes[k] for k in range(len(boxes)) if res.x[k] > 0.5]
print("N_grid_opt =", len(sol))
for (a, b, c, d) in sol:
    print(f"  x in [{g1[a]:.4f},{g1[b]:.4f}]  z in [{g2[c]:.4f},{g2[d]:.4f}]   F1={F1[a,b]:+.5f} F2={F2[c,d]:+.5f}")
free = [("x", g1[k]) for k in range(1, G1 - 1) if all(not (g1[a] < g1[k] < g1[b]) for a, b, c, d in sol)]
free += [("z", g2[k]) for k in range(1, G2 - 1) if all(not (g2[c] < g2[k] < g2[d]) for a, b, c, d in sol)]
print("free guillotine cuts of the optimal partition:", free)
for i, I in enumerate(Is):
    print(f"coordinate {i}: knots", np.round(I.x, 5).tolist(), "m at knots", np.round(I.m, 6).tolist())
