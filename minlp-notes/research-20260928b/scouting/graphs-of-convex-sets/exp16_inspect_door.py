import numpy as np
from gcs import relax, path_cost, all_paths
from mp import MP
from door import door_inst
from exp8_mp import simply_connected
from exp9_corridor import corridor
rng = np.random.default_rng(0)
for trial in range(40):
    boxes, pts = corridor(rng, legs=rng.integers(2, 4), W=rng.uniform(0.8, 2.0))
    B = [(np.array(a), np.array(b)) for a, b in boxes]
    if not simply_connected(B): continue
    m = MP(boxes, pts[0], pts[-1], two_cycle=True)
    if not m.paths() or len(m.paths()) > 3000: continue
    if len(boxes) != 4: continue
    I = door_inst(m)
    r, sol = relax(I, return_sol=True); rh = relax(I, hull=True)
    print("start", pts[0], "goal", np.round(pts[-1], 3), "REL", r, "REL_hull", rh, "region OPT", m.exact())
    for k, S in I.sets.items(): print(" ", k, S[0], np.round(np.asarray(S[1], float), 3), np.round(np.asarray(S[2], float), 3) if S[0]=='box' else '')
    for e, v in sol['y'].items():
        if v > 1e-4: print(e, round(v, 4), 'tail', np.round(sol['z'][e]/v, 3), 'head', np.round(sol['zp'][e]/v, 3))
    ps = all_paths(I); print("door paths", len(ps))
    best = min(ps, key=lambda p: path_cost(I, p)); print("best door path", best, path_cost(I, best))
    break
