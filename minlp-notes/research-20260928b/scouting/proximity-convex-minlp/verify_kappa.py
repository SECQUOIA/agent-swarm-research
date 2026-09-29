"""Brute-force check of the 2-D sqrt(kappa) family: Q = R w w^T + I,
w = (1, -1/(2K)).  Take the LP maximiser v of the Voronoi cell (scaled by
0.999), confirm by exhaustive search that 0 is the unique Q-closest lattice
point, and report |v|_inf against sqrt(kappa)."""
import numpy as np
from scipy.optimize import linprog
from voronoi import lll, gram_schmidt, short_vectors

for R, K in [(1e4, 47), (1e6, 477)]:
    w = np.array([1.0, -1.0 / (2 * K)])
    G = R * np.outer(w, w) + np.eye(2)
    ev = np.linalg.eigvalsh(G)
    B = lll(np.eye(2), G)
    Bs, _ = gram_schmidt(B, G)
    mu2 = 0.25 * sum(Bs[:, i] @ G @ Bs[:, i] for i in range(2))
    vecs = [B @ np.array(u) for u in short_vectors(B, G, 4 * mu2)]
    Aub = np.array([z @ G for z in vecs]); bub = np.array([0.5 * z @ G @ z for z in vecs])
    nr = np.linalg.norm(Aub, axis=1); Aub, bub = Aub / nr[:, None], bub / nr
    best = None
    for i in range(2):
        for s in (1, -1):
            obj = np.zeros(2); obj[i] = -s
            r = linprog(obj, A_ub=Aub, b_ub=bub, bounds=[(None, None)] * 2, method="highs")
            assert r.status == 0
            if best is None or -r.fun > best[0]:
                best = (-r.fun, r.x)
    v = 0.999 * best[1]
    L = int(np.abs(v).max()) * 2 + 5
    d0 = v @ G @ v
    closer = 0
    for z1 in range(-L, L + 1):
        for z2 in range(-L, L + 1):
            if (z1 or z2):
                d = v - (z1, z2)
                if d @ G @ d < d0 * (1 - 1e-12):
                    closer += 1
    print(f"R={R:.0e} K={K}: kappa={ev[1]/ev[0]:.3e} |v|_inf={np.abs(v).max():.1f} sqrt(kappa)={np.sqrt(ev[1]/ev[0]):.1f} "
          f"box={L} closer lattice points={closer}")
