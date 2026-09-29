"""Theorem 7 claim 3 on acyclic region DAGs with vertically separated lanes (forces
detours, so the region relaxation has gaps): REL_H(region) <= REL(line graph)."""
import numpy as np
from rgcs import *
import r5_ring_door as R

rng = np.random.default_rng(11)
worst = -np.inf; nviol = 0; ngapG = 0; ngapL = 0; n = 0
for it in range(80):
    if n >= 30: break
    nl = int(rng.integers(3, 5))
    regions = {}; layers = []
    for i in range(nl + 1):
        w = int(rng.integers(2, 4)) if 0 < i < nl else 1
        L = []
        for j in range(w):
            xlo = 1.6 * i - 0.3; xhi = 1.6 * i + rng.uniform(1.7, 2.4)
            c = rng.uniform(-3, 3) if 0 < i < nl else 0.0
            h = rng.uniform(0.4, 1.5) if 0 < i < nl else 3.5
            name = f"r{i}{j}"
            regions[name] = Box([xlo, c - h], [xhi, c + h]); L.append(name)
        layers.append(L)
    redges = [(u, v) for a, b in zip(layers[:-1], layers[1:]) for u in a for v in b
              if R.box_intersect(regions[u], regions[v]) is not None]
    r0, rN = layers[0][0], layers[-1][0]
    start = np.array([regions[r0].V.min(0)[0] + 0.1, rng.uniform(-1, 1)])
    goal = np.array([regions[rN].V.max(0)[0] - 0.1, rng.uniform(-1, 1)])
    g = R.region_gcs(regions, redges, start, goal, [r0], [rN])
    oR = opt(g)
    if not np.isfinite(oR):
        continue
    gl = R.door_gcs(regions, redges, start, goal, [r0], [rN], directed_line=True)
    oL = opt(gl)
    rG, rhG, rL, rhL = relax(g), relax(g, hull=True), relax(gl), relax(gl, hull=True)
    n += 1
    diff = rhG - rL; worst = max(worst, diff / max(1, rL))
    bad = diff > 1e-5 * max(1, rL) or abs(oR - oL) > 1e-5 * oR or rL > rhL + 1e-5 or rhL > oL + 1e-5
    nviol += bad; ngapG += oR > rhG + 1e-4; ngapL += oL > rhL + 1e-4
    print(f"#{it:2d} |E_G|={len(g.E):2d} OPT={oR:.5f}/{oL:.5f} REL(G)={rG:.5f} REL_H(G)={rhG:.5f} REL(L)={rL:.5f} "
          f"REL_H(L)={rhL:.5f} gapH(G)={100*(oR/rhG-1):.2f}% gap(L)={100*(oL/rL-1):.2f}%" + ("  VIOL" if bad else ""), flush=True)
print(f"{n} feasible instances; REL_H(G) gaps: {ngapG}; REL_H(L) gaps: {ngapL}; max rel (REL_H(G)-REL(L)) = {worst:.2e}; violations: {nviol}")
