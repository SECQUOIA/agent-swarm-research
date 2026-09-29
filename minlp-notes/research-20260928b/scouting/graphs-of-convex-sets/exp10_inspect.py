import numpy as np
from mp import MP
from exp9_corridor import corridor
from exp8_mp import simply_connected
rng = np.random.default_rng(0)
for trial in range(40):
    boxes, pts = corridor(rng, legs=rng.integers(2, 4), W=rng.uniform(0.8, 2.0))
    B = [(np.array(a), np.array(b)) for a, b in boxes]
    if not simply_connected(B): continue
    m = MP(boxes, pts[0], pts[-1], two_cycle=True)
    if not m.paths() or len(m.paths()) > 3000: continue
    if len(boxes) == 4:
        r, y = m.relax(); o = m.exact()
        print("start", pts[0], "goal", pts[-1], "REL", r, "OPT", o)
        for i, b in enumerate(boxes): print(i, np.round(b[0], 3), np.round(b[1], 3))
        for e, v in y.items():
            if v > 1e-4: print(e, round(v, 4))
        best = min(m.paths(), key=m.path_cost); print("best path", best, m.path_cost(best))
        break
