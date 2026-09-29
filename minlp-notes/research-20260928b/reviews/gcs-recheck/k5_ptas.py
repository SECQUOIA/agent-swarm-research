"""Sanity check of Proposition 11 (grid (1+eps)-approximation, fixed dimension, separated sets).

Sets are axis-aligned boxes (projection = clipping), Euclidean lengths, random digraphs with cycles.
Net: cell-centred grid of spacing eps*delta/sqrt(n) over each box, clipped onto the box (an h-net
with h = eps*delta/2; at most (1 + D sqrt(n)/(eps delta))^n points).  Dijkstra on (vertex, net point),
then shortcut repeated vertices; compare with exact OPT (simple-path enumeration)."""
import heapq
import itertools
import numpy as np
from rc import box, pt, G, opt_exact, path_cost

rng = np.random.default_rng(0)


def box_dist(a, b):
    gap = np.maximum(0, np.maximum(a[0] - b[1], b[0] - a[1]))
    return float(np.linalg.norm(gap))


def net(lo, hi, s):
    axes = []
    for l, h in zip(lo, hi):
        k = max(1, int(np.ceil((h - l) / s - 1e-12)))
        axes.append(np.clip(l + (np.arange(k) + 0.5) * s, l, h))
    return np.array(list(itertools.product(*axes)))


worst = 0.0
count_ok = cover_ok = True
rows = 0
for it in range(12):
    n = 2
    k = int(rng.integers(4, 7))
    B = {}
    cen = rng.uniform(0, 8, size=(k, n))
    for i in range(k):
        half = rng.uniform(0.1, 0.8, n)
        B[str(i)] = (cen[i] - half, cen[i] + half)
    B["s"] = (np.array([-1.0, 4.0]),) * 2
    B["t"] = (np.array([9.0, 4.0]),) * 2
    names = list(B)
    E = [(a, b) for a in names for b in names if a != b and a != "t" and b != "s" and rng.random() < 0.5]
    E = [e for e in E if box_dist(B[e[0]], B[e[1]]) > 0.05 and e != ("s", "t")]
    g = G({v: (pt(*B[v][0]) if v in "st" else box(*B[v])) for v in names}, E, "s", "t", "l2")
    try:
        opt = opt_exact(g)[0]
    except Exception:
        continue
    if not np.isfinite(opt):
        continue
    delta = min(box_dist(B[u], B[v]) for u, v in E)
    D = max(float(np.linalg.norm(B[v][1] - B[v][0])) for v in names)
    for eps in (1.0, 0.5, 0.25):
        s = eps * delta / np.sqrt(n)
        h = eps * delta / 2
        nets = {v: net(B[v][0], B[v][1], s) for v in names}
        bound = (1 + D * np.sqrt(n) / (eps * delta)) ** n
        count_ok &= all(len(P) <= bound for P in nets.values())
        for v in names:  # covering radius
            X = B[v][0] + rng.random((200, n)) * (B[v][1] - B[v][0])
            d = np.min(np.linalg.norm(X[:, None, :] - nets[v][None, :, :], axis=2), axis=1)
            cover_ok &= bool(np.max(d) <= h + 1e-12)
        # Dijkstra on product graph
        dist = {("s", 0): 0.0}
        prev = {}
        pq = [(0.0, "s", 0)]
        while pq:
            dcur, v, i = heapq.heappop(pq)
            if dcur > dist.get((v, i), np.inf):
                continue
            for (_, w) in g.out[v]:
                L = np.linalg.norm(nets[w] - nets[v][i], axis=1)
                for j, l in enumerate(L):
                    if dcur + l < dist.get((w, j), np.inf):
                        dist[(w, j)] = dcur + l
                        prev[(w, j)] = (v, i)
                        heapq.heappush(pq, (dcur + l, w, j))
        walk_cost = dist[("t", 0)]
        # recover walk and shortcut repeated vertices (triangle inequality)
        node, walk = ("t", 0), []
        while node in prev:
            walk.append(node)
            node = prev[node]
        walk.append(node)
        walk = walk[::-1]
        out = []
        for v, i in walk:
            if any(v == u for u, _ in out):
                while out[-1][0] != v:
                    out.pop()
                continue
            out.append((v, i))
        pc = sum(np.linalg.norm(nets[b][j] - nets[a][i]) for (a, i), (b, j) in zip(out[:-1], out[1:]))
        ratio = pc / opt
        worst = max(worst, (ratio - 1) / eps)
        rows += 1
        print(f"inst {it} eps={eps:4.2f} delta={delta:.3f} D={D:.3f} net sizes<= {max(len(P) for P in nets.values())} (bound {bound:.0f})"
              f" walk={walk_cost:.5f} path={pc:.5f} OPT={opt:.5f} ratio={ratio:.5f} <= 1+eps: {ratio <= 1 + eps + 1e-9}")
print(f"rows={rows} counts within bound: {count_ok}; covering radius <= h: {cover_ok}; max (ratio-1)/eps = {worst:.4f}")
