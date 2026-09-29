"""Exp 15: 1D Euclidean GCS (intervals, |x_v-x_u| lengths, general digraph with cycles) is
solved exactly by Dijkstra on (vertex, breakpoint) pairs, breakpoints = all interval endpoints.
Walks are shortcut to simple paths by the triangle inequality. Compare with path enumeration."""
import heapq, numpy as np
from gcs import *
rng = np.random.default_rng(9)

def dp(I):
    iv = {v: (S[1][0], S[1][0]) if S[0]=='point' else (S[1][0], S[2][0]) for v, S in I.sets.items()}
    B = sorted({x for a, b in iv.values() for x in (a, b)})
    cand = {v: [x for x in B if iv[v][0]-1e-12 <= x <= iv[v][1]+1e-12] for v in I.sets}
    out = {}
    for u, v in I.edges: out.setdefault(u, []).append(v)
    dist = {(I.s, x): 0.0 for x in cand[I.s]}; pq = [(0.0, I.s, x) for x in cand[I.s]]
    while pq:
        d, u, x = heapq.heappop(pq)
        if d > dist.get((u, x), np.inf) + 1e-15: continue
        if u == I.t: return d
        for v in out.get(u, []):
            for x2 in cand[v]:
                nd = d + abs(x2 - x)
                if nd < dist.get((v, x2), np.inf) - 1e-15:
                    dist[(v, x2)] = nd; heapq.heappush(pq, (nd, v, x2))
    return np.inf

worst = 0; cnt = 0
while cnt < 60:
    nv = rng.integers(4, 8)
    sets = {}
    for v in range(nv):
        c = rng.uniform(-5, 5); w = rng.uniform(0, 2.5) if rng.random() < 0.8 else 0
        sets[v] = ('box', [c - w], [c + w])
    E = [(u, v) for u in range(nv) for v in range(nv) if u != v and v != 0 and u != nv-1 and rng.random() < 0.45]
    I = Inst(sets, E, 0, nv-1, 1)
    if not all_paths(I): continue
    cnt += 1
    o = exact(I); d = dp(I)
    worst = max(worst, abs(o - d))
print("max |enumeration - breakpoint DP| over 60 cyclic 1D instances:", worst)
