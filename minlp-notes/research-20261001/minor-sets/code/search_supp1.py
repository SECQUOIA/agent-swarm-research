"""Search for rational full-dimensional corners whose corner minimizer has support one (all edges of
T* at the contact point transversal) and where the orbit family still misses z_K.

Construction (w = 1, four rays): t* = a0 b0^T, v1 = t*, g = gradient of det at t*;
v_j = t* + D_j + eps_j h (j = 2, 3, 4) with g . D_j = 0 and g . h = 1, so g . v_j = eps_j > 0
(strictly positive KKT multipliers); sbar random with det(sbar) > 0 and g . sbar > 0.
Kept if z_K = 1 with minimizer e_1 (numerically) and the orbit bound is below 1 - 1e-4.
Usage: python3 search_supp1.py SEED NTRIALS
"""
import sys
import json
import numpy as np
from minor_core import det4, zK, FamilySolver, precondition

seed, T = int(sys.argv[1]), int(sys.argv[2])
rng = np.random.default_rng(seed)
found = []
nvalid = 0
for trial in range(T):
    a0 = rng.integers(-3, 4, 2); b0 = rng.integers(-3, 4, 2)
    if not a0.any() or not b0.any():
        continue
    t0 = np.array([a0[0] * b0[0], a0[0] * b0[1], a0[1] * b0[0], a0[1] * b0[1]], float)
    g = np.array([t0[3], -t0[2], -t0[1], t0[0]])
    kk = int(np.argmax(np.abs(g)))
    h = np.zeros(4); h[kk] = 1.0 / g[kk]
    verts = []
    for j in range(3):
        D = rng.integers(-6, 7, 4) / 2.0
        D[kk] = 0.0
        D[kk] = -(g @ D) / g[kk]
        eps = [1 / 8, 1 / 4, 1 / 2, 1, 2][rng.integers(5)]
        verts.append(t0 + D + eps * h)
    sbar = rng.integers(-8, 9, 4) / 2.0
    if det4(sbar) <= 0 or g @ sbar <= 0:
        continue
    V = [t0] + verts
    P = np.stack([v - sbar for v in V], 1)
    if abs(np.linalg.det(P)) < 1e-6:
        continue
    w = np.ones(4)
    zk, lam = zK(sbar, P, w, return_point=True)
    if not (abs(zk - 1) < 1e-9 and abs(lam[0] - 1) < 1e-9 and np.all(lam[1:] < 1e-12)):
        continue
    nvalid += 1
    sbI, PI = precondition(sbar, P)
    cert, hi, FT = FamilySolver('orbit', sbI, PI, w).best(1.0, iters=30)
    if hi < 1 - 1e-4:
        rec = dict(trial=trial, sbar=sbar.tolist(), v1=t0.tolist(), v2=verts[0].tolist(), v3=verts[1].tolist(),
                   v4=verts[2].tolist(), orbit=cert, orbit_hi=hi,
                   edge_cos=[float(g @ (v - t0) / (np.linalg.norm(g) * np.linalg.norm(v - t0))) for v in [sbar] + verts])
        found.append(rec)
        print(json.dumps(rec), flush=True)
print('VALID support-one corners (z_K = 1, minimizer e_1):', nvalid)
print('FOUND (orbit < 1 - 1e-4):', len(found))
for r in sorted(found, key=lambda r: r['orbit'])[:10]:
    print('BEST', json.dumps(r))
