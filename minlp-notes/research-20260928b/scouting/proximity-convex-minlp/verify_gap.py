"""Independent brute-force check of the 2-D Voronoi l_inf radius used in
sublattice_gap.py: for the LP maximiser v (scaled by 0.999 into the cell
interior) check by exhaustive search that 0 is the unique Q_SS-closest lattice
point, so the constrained problem x3 = 0 with continuous optimum v has
integer optimum 0 at l_inf distance ~ rho(Q_SS)."""
import math, itertools
import numpy as np
from scipy.optimize import linprog
from voronoi import lll, gram_schmidt, short_vectors

alpha = 2 ** (1 / 3)
for e in [4, 6, 8]:
    R = 10.0 ** e
    w = np.array([1.0, -alpha])
    G = R * np.outer(w, w) + np.eye(2)
    B = lll(np.eye(2), G)
    Bs, _ = gram_schmidt(B, G)
    mu2 = 0.25 * sum(Bs[:, i] @ G @ Bs[:, i] for i in range(2))
    vecs = [B @ np.array(u) for u in short_vectors(B, G, 4 * mu2)]
    Aub = np.array([z @ G for z in vecs]); bub = np.array([0.5 * z @ G @ z for z in vecs])
    nr = np.linalg.norm(Aub, axis=1); Aub = Aub / nr[:, None]; bub = bub / nr
    best = None
    for i in range(2):
        for s in (1, -1):
            obj = np.zeros(2); obj[i] = -s
            r = linprog(obj, A_ub=Aub, b_ub=bub, bounds=[(None, None)] * 2, method="highs")
            assert r.status == 0, r.message
            if best is None or -r.fun > best[0]:
                best = (-r.fun, r.x)
    v = 0.999 * best[1]
    # brute force: all lattice points in a box of radius 3*|v|_inf + 3
    L = int(3 * np.abs(v).max()) + 3
    d0 = v @ G @ v
    closer = [(z1, z2) for z1 in range(-L, L + 1) for z2 in range(-L, L + 1)
              if (z1 or z2) and (v - (z1, z2)) @ G @ (v - (z1, z2)) < d0 - 1e-9 * d0]
    print(f"R=1e{e}: rho_LP={best[0]:.3f}, |0.999 v|_inf={np.abs(v).max():.3f}, box={L}, lattice pts strictly closer than 0: {len(closer)}")
