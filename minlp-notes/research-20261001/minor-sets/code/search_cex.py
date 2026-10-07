"""Search for rational full-dimensional tangent-edge corners where the orbit family misses z_K.

Construction (w = 1, four rays, so T* = conv{sbar, v1..v4} is a 4-simplex):
  t* = a0 b0^T (integer a0, b0), D tangent at t* ((J a0)^T D (J b0) = 0) with det D > 0,
  v1 = t* + D, v2 = t* - k D (k in {1, 2, 1/2}), sbar, v3, v4 random half-integers, det(sbar) > 0.
Kept if z_K = 1 with minimizer support {1, 2} (numerically; exact check in certify_cex.py) and the
best orbit bound is below 1.  Prints JSON lines sorted by the orbit ratio at the end.
Usage: python3 search_cex.py SEED NTRIALS
"""
import sys
import json
from fractions import Fraction as Fr
import numpy as np
from minor_core import mat, det4, zK, FamilySolver, kappa_pencil, symm
sys.path.insert(0, '.')

seed, T = int(sys.argv[1]), int(sys.argv[2])
rng = np.random.default_rng(seed)
J = np.array([[0, 1], [-1, 0]])


def kappa_sets_empty(t0, D, verts):
    """Numerical check: intersection of kappa-intervals of the other vertices is empty."""
    G0, G1 = kappa_pencil(t0, D)
    grid = np.linspace(-200, 200, 40001)
    ok = np.ones_like(grid, bool)
    for v in verts:
        A = symm(G0 @ mat(v)); B = symm(G1 @ mat(v))
        a11 = A[0, 0] + grid * B[0, 0]; a22 = A[1, 1] + grid * B[1, 1]; a12 = A[0, 1] + grid * B[0, 1]
        ok &= (a11 >= -1e-12) & (a22 >= -1e-12) & (a11 * a22 - a12 ** 2 >= -1e-12)
    return not ok.any()


found = []
nvalid = 0
for trial in range(T):
    a0 = rng.integers(-3, 4, 2); b0 = rng.integers(-3, 4, 2)
    if not a0.any() or not b0.any():
        continue
    M0 = np.outer(a0, b0).astype(float)
    ja, jb = J @ a0, J @ b0
    # tangent directions: D with ja^T D jb = 0; random integer D projected by solving for one entry
    D = rng.integers(-4, 5, (2, 2)).astype(float)
    coef = np.outer(ja, jb)                 # ja^T D jb = <coef, D>
    idx = np.argwhere(coef != 0)
    if len(idx) == 0:
        continue
    i, j = idx[rng.integers(len(idx))]
    D[i, j] = 0.0
    D[i, j] = -np.sum(coef * D) / coef[i, j]
    if abs(D[i, j] * 2 - round(D[i, j] * 2)) > 1e-12:   # keep half-integers
        continue
    if np.linalg.det(D) <= 0:
        continue
    k = [1.0, 2.0, 0.5][rng.integers(3)]
    t0 = np.array([M0[0, 0], M0[0, 1], M0[1, 0], M0[1, 1]])
    Dv = np.array([D[0, 0], D[0, 1], D[1, 0], D[1, 1]])
    v1 = t0 + Dv; v2 = t0 - k * Dv
    sbar = rng.integers(-8, 9, 4) / 2.0
    if det4(sbar) <= 0:
        continue
    v3 = rng.integers(-8, 9, 4) / 2.0
    v4 = rng.integers(-8, 9, 4) / 2.0
    P = np.stack([v1 - sbar, v2 - sbar, v3 - sbar, v4 - sbar], 1)
    if abs(np.linalg.det(P)) < 1e-6:
        continue
    w = np.ones(4)
    zk, lam = zK(sbar, P, w, return_point=True)
    if not (abs(zk - 1) < 1e-9 and lam[2] < 1e-12 and lam[3] < 1e-12 and min(lam[0], lam[1]) > 1e-6):
        continue
    nvalid += 1
    empty = kappa_sets_empty(t0, Dv, [sbar, v3, v4])
    if not empty:
        continue
    cert, hi, FT = FamilySolver('orbit', sbar, P, w).best(1.0, iters=30)
    rec = dict(trial=trial, sbar=sbar.tolist(), v1=v1.tolist(), v2=v2.tolist(), v3=v3.tolist(), v4=v4.tolist(),
               t0=t0.tolist(), D=Dv.tolist(), k=k, orbit=cert, orbit_hi=hi)
    found.append(rec)
    print(json.dumps(rec), flush=True)
print('VALID tangent-edge corners (z_K = 1, support {1,2}):', nvalid)
print('FOUND (empty kappa intersection):', len(found))
for r in sorted(found, key=lambda r: r['orbit'])[:10]:
    print('BEST', json.dumps(r))
