"""Exp 8: order-1 motion-planning GCS with overlapping boxes.
(a) ring around a square obstacle (a hole), symmetric and perturbed;
(b) random box unions, classified simply-connected vs with holes (grid test)."""
import numpy as np
from mp import MP

def ring(eps):
    # obstacle [-1,1]^2; free ring of width 1 made of 4 boxes
    boxes = [([-2, -2], [-1, 2]), ([1, -2], [2, 2]), ([-2, 1], [2, 2]), ([-2, -2], [2, -1 + eps])]
    return MP(boxes, [-1.5, 0.0], [1.5, 0.0])

def simply_connected(boxes, res=200):
    lo = np.min([b[0] for b in boxes], 0) - 0.5; hi = np.max([b[1] for b in boxes], 0) + 0.5
    xs = np.linspace(lo[0], hi[0], res); ys = np.linspace(lo[1], hi[1], res)
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    free = np.zeros_like(X, bool)
    for b in boxes:
        free |= (X >= b[0][0]) & (X <= b[1][0]) & (Y >= b[0][1]) & (Y <= b[1][1])
    # flood fill complement from border
    from collections import deque
    seen = np.zeros_like(free); q = deque()
    for i in range(res):
        for j in (0, res-1):
            for (a, c) in ((i, j), (j, i)):
                if not free[a, c] and not seen[a, c]: seen[a, c] = True; q.append((a, c))
    while q:
        a, c = q.popleft()
        for da, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            na, nc = a+da, c+dc
            if 0 <= na < res and 0 <= nc < res and not free[na, nc] and not seen[na, nc]:
                seen[na, nc] = True; q.append((na, nc))
    holes = (~free) & (~seen)
    return holes.sum() == 0

if __name__ == "__main__":
    for eps in [0.0, 0.05, 0.2]:
        m = ring(eps); r, y = m.relax(); o = m.exact()
        print(f"ring eps={eps}: REL={r:.4f} OPT={o:.4f} gap={(o-r)/o:.3%}")

    rng = np.random.default_rng(5)
    stats = {True: [], False: []}
    tries = 0
    while min(len(stats[True]), len(stats[False])) < 25 and tries < 3000:
        tries += 1
        R = rng.integers(4, 8)
        boxes = []
        for _ in range(R):
            c = rng.uniform(0, 6, 2); w = rng.uniform(0.3, 2.0, 2)
            boxes.append((c - w, c + w))
        B = [(np.array(a), np.array(b)) for a, b in boxes]
        # start/goal inside random boxes
        i, j = rng.choice(R, 2, replace=False)
        st = rng.uniform(B[i][0], B[i][1]); gl = rng.uniform(B[j][0], B[j][1])
        m = MP(boxes, st, gl)
        if not m.paths(): continue
        sc = simply_connected(B)
        if len(stats[sc]) >= 25: continue
        r, y = m.relax(); o = m.exact()
        stats[sc].append((o - r)/max(o, 1e-9))
    for sc in (True, False):
        g = np.array(stats[sc])
        print(f"simply_connected={sc}: n={len(g)} #gap>1e-4: {(g>1e-4).sum()} max rel gap={g.max():.3%}")
