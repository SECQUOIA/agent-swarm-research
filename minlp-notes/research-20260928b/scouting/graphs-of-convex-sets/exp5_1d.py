"""Exp 5: 1D random DAGs, Euclidean |.| lengths.
(a) disjoint intervals (every edge joins disjoint intervals) -> expect REL == OPT;
(b) overlapping intervals -> gaps possible; also check REL == REL_hull (intervals are simplices)."""
import numpy as np
from gcs import *
rng = np.random.default_rng(3)

def rand_dag(nv, p):
    E = []
    for i in range(nv):
        for j in range(i+1, nv):
            if rng.random() < p: E.append((i, j))
    return E

def build(overlap):
    nv = rng.integers(5, 9)
    sets = {}
    for v in range(nv):
        if v in (0, nv-1):
            sets[v] = ('point', [rng.uniform(-5, 5)])
        else:
            c = rng.uniform(-5, 5); w = rng.uniform(0.1, 2.0 if overlap else 0.6)
            sets[v] = ('box', [c - w], [c + w])
    E = rand_dag(nv, 0.6)
    if not overlap:
        def iv(S): return (S[1][0], S[1][0]) if S[0]=='point' else (S[1][0], S[2][0])
        E = [(u,v) for (u,v) in E if iv(sets[u])[1] < iv(sets[v])[0] or iv(sets[v])[1] < iv(sets[u])[0]]
    I = Inst(sets, E, 0, nv-1, 1)
    if not all_paths(I): return None
    return I

for overlap in [False, True]:
    gaps, hulldiff, cnt = [], [], 0
    while cnt < 80:
        I = build(overlap)
        if I is None: continue
        cnt += 1
        r = relax(I); rh = relax(I, hull=True); o = exact(I)
        gaps.append(o - r); hulldiff.append(rh - r)
    gaps, hulldiff = np.array(gaps), np.array(hulldiff)
    print(f"overlap={overlap}: n=80 max(OPT-REL)={gaps.max():.2e} #gap>1e-5: {(gaps>1e-5).sum()}  max|REL_hull-REL|={np.abs(hulldiff).max():.2e}")
