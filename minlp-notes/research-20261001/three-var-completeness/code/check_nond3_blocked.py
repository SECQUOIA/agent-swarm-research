"""Empirical: does every sampled ray outside D3 (numerically) have a blocked
vertex in the sense of Lemma 2.4?  Zeros are found by face enumeration."""
import json, glob, sys
import numpy as np
from itertools import combinations, product
from cube3 import *

def numeric_zeros(pvec, tol):
    p = quad_from_vector(pvec)
    sc = np.abs(pvec).max()
    out = []
    for st, x, v in face_minimizers(p, tol=1e-7):
        if abs(v) < tol * sc:
            out.append((st, x))
    return out

def in_aff(points, target, tol=1e-6):
    if not points: return False
    if len(target) == 0: return True
    P = np.array(points); t = np.array(target)
    if len(P) == 1: return np.linalg.norm(P[0] - t) < tol
    D = (P[1:] - P[0]).T; r = t - P[0]
    sol, *_ = np.linalg.lstsq(D, r, rcond=None)
    return np.linalg.norm(D @ sol - r) < tol

def blocked_vertex(pvec, zeros):
    p = quad_from_vector(pvec); sc = np.abs(pvec).max()
    res = []
    for v in product((0, 1), repeat=3):
        if peval(p, v) <= 1e-6 * sc: continue
        ok = True
        for k in range(4):
            for Fr in combinations(range(3), k):
                vis = [x for st, x in zeros if all(abs(x[j] - (1 - v[j])) > 1e-9 for j in range(3) if j not in Fr)]
                if not in_aff([[x[i] for i in Fr] for x in vis], [v[i] for i in Fr]):
                    ok = False; break
            if not ok: break
        if ok: res.append(v)
    return res

files = sys.argv[1:]
tot = 0; bl = 0; unb = []
for f in files:
    for o in json.load(open(f)):
        if o.get('r0', 1) < -1e-6:
            p = np.array(o['p']); tot += 1
            z = numeric_zeros(p, 1e-7)
            b = blocked_vertex(p, z)
            if b: bl += 1
            else: unb.append((f, o['r0'], [s for s, x in z]))
print('non-D3 rays', tot, 'with a blocked vertex', bl)
for u in unb[:10]: print('UNBLOCKED', u)
