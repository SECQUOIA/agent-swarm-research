"""T7: overlapping sets.

(a) 1D fork-merge family (Prop. O1): REL = REL_H = delta, OPT = 2 - delta; additive bound
    OPT - REL_H <= max_P sum_{e in P} Delta_e (Theorem 1) and Delta_e <= R_u + R_v.
(b) random overlapping 2D box DAGs, l2: Delta_e <= R_u + R_v (circumradii) and
    OPT - REL_H <= max_P sum Delta_e <= max_P sum (R_u + R_v).
(c) ring around a wall of half-height H (region formulation, order 1): REL = |t - s| = 3 for all H
    (also with two-cycle cuts and with the region-level hull), OPT = 2 + 2 sqrt(H^2 + 1/4)
    (detour bound OPT/REL <= d_F/|t-s| is attained); door formulation: kappa_door and REL_H,door.
Usage: python3 t7_overlap.py [seed]
"""
import sys
import numpy as np
from gcslib import *
from mpform import Region, door_gcs, ring_wall

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)

# (a)
for delta in [0.0, 0.01, 0.1, 0.5, 1.0]:
    S = {"s": point([0.0]), "A": box([-1.0], [1.0]), "P": point([1.0]), "M": point([-1.0]),
         "B": box([-1.0], [1.0]), "t": point([delta])}
    E = [("s", "A"), ("A", "P"), ("A", "M"), ("P", "B"), ("M", "B"), ("B", "t")]
    g = GCS(S, E, "s", "t", L2)
    dl = {e: delta_e(g, e) for e in E}
    rad = {e: S[e[0]].circ()[1] + S[e[1]].circ()[1] for e in E}
    print(f"(a) delta={delta:4}: REL={relax(g):.6f} REL_H={relax(g, hull=True):.6f} OPT={opt(g):.6f} "
          f"maxP sum Delta={max_path_weight(g, dl):.6f} (2-delta^2={2-delta**2:.6f}) maxP sum(R_u+R_v)={max_path_weight(g, rad):.3f}")

# (b)
bad_rad, bad_add, cnt, gaps = 0, 0, 0, 0
while cnt < 25:
    L, k = int(rng.integers(2, 4)), int(rng.integers(2, 4))
    sets = {"s": point([0.0, 0.0])}
    layers = []
    for i in range(1, L + 1):
        lay = []
        for j in range(k):
            c = np.array([1.2 * i, rng.uniform(-1.5, 1.5)])
            w = rng.uniform(0.3, 1.2, 2)
            sets[f"{i}_{j}"] = box(c - w, c + w)
            lay.append(f"{i}_{j}")
        layers.append(lay)
    sets["t"] = point([1.2 * (L + 1), 0.0])
    E = [("s", v) for v in layers[0]] + [(v, "t") for v in layers[-1]]
    for a, b in zip(layers, layers[1:]):
        E += [(u, v) for u in a for v in b]
    g = GCS(sets, E, "s", "t", L2)
    cnt += 1
    rh, o = relax(g, hull=True), opt(g)
    dl = {e: delta_e(g, e) for e in E}
    rad = {e: sets[e[0]].circ()[1] + sets[e[1]].circ()[1] for e in E}
    bad_rad += any(dl[e] > rad[e] + 1e-6 for e in E)
    mpD, mpR = max_path_weight(g, dl), max_path_weight(g, rad)
    bad_add += not (o - rh <= mpD + 1e-6 and mpD <= mpR + 1e-6)
    gaps += o - rh > 1e-5
    print(f"(b) |E|={len(E):2d} OPT-REL_H={o-rh:.5f} maxP sum Delta={mpD:.4f} maxP sum(R_u+R_v)={mpR:.4f}", flush=True)
print(f"(b) n={cnt} #gaps={gaps} violations: Delta>R_u+R_v: {bad_rad}, additive chain: {bad_add}")

# (c)
for H in [0.25, 0.5, 1, 2, 5, 10, 20]:
    m = ring_wall(H)
    o = m.exact()
    r = m.relax()
    r2 = m.relax(two_cycle=True)
    rh = m.relax(hull=True)
    gd = door_gcs(m)
    od = opt(gd)
    rd = relax(gd)
    rdh = relax(gd, hull=True, degree=False)
    kd = max(kappa_l2(gd.sets[u], gd.sets[v]) for u, v in gd.edges)
    print(f"(c) H={H:5}: OPT={o:.5f} (2+2sqrt(H^2+1/4)={2+2*np.sqrt(H*H+0.25):.5f}) REL={r:.5f} "
          f"REL(2-cycle cuts)={r2:.5f} REL(region hull)={rh:.5f} OPT/REL={o/r:.4f}; door: OPT={od:.5f} "
          f"REL={rd:.5f} REL_H(no deg)={rdh:.5f} kappa_door={kd:.4f}", flush=True)

# (d) region formulation lower bound REL >= |goal - start| on random box unions (any topology)
bad = 0
for trial in range(15):
    R = int(rng.integers(4, 8))
    boxes = []
    for _ in range(R):
        c = rng.uniform(0, 6, 2)
        w = rng.uniform(0.3, 2.0, 2)
        boxes.append((c - w, c + w))
    i, j = rng.choice(R, 2, replace=False)
    st = rng.uniform(boxes[i][0], boxes[i][1])
    gl = rng.uniform(boxes[j][0], boxes[j][1])
    m = Region(boxes, st, gl)
    if not m.paths(maxn=1):
        continue
    r = m.relax()
    bad += r < np.linalg.norm(gl - st) - 1e-6
    print(f"(d) R={R} REL={r:.5f} |goal-start|={np.linalg.norm(gl-st):.5f}", flush=True)
print(f"(d) violations of REL >= |goal-start|: {bad}")
