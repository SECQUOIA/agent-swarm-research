"""Prop 2(2): REL = REL_H when every internal set is a simplex (triangles in 2D, intervals in 1D),
for nonlinear lengths (sq, l2) on dense layered DAGs; contrast with boxes (squares)."""
import sys
import numpy as np
sys.argv = ["r2", "7", "1", "1.5", "hard"]
import r2_theorem1 as T  # noqa  (runs 1 instance on import; reuses rand_set/generator)
from rgcs import *
rng = np.random.default_rng(7)

def tri(center, scale):
    P = center + rng.standard_normal((3, 2)) * scale
    cen = P.mean(0); A = []; b = []
    for i in range(3):
        p1, p2 = P[i], P[(i + 1) % 3]
        nrm = np.array([p2[1] - p1[1], -(p2[0] - p1[0])])
        if nrm @ (cen - p1) > 0: nrm = -nrm
        A.append(nrm); b.append(nrm @ p1)
    return Poly(np.array(A), np.array(b), P)

for kind in ["triangles", "intervals", "boxes"]:
    worst = 0.0; worst_box = 0.0
    for it in range(12):
        dim = 1 if kind == "intervals" else 2
        sets = {"s": Pt(np.zeros(dim))}; layers = [["s"]]
        for i in range(3):
            L = []
            for j in range(3):
                c = np.zeros(dim); c[0] = 2.0 * (i + 1)
                if dim > 1: c[1] = rng.uniform(-2, 2)
                if kind == "triangles": S = tri(c, 1.2)
                elif kind == "intervals": S = Box(c - rng.uniform(0.2, 1.5), c + rng.uniform(0.2, 1.5))
                else: S = Box(c - rng.uniform(0.3, 1.2, dim), c + rng.uniform(0.3, 1.2, dim))
                sets[f"v{i}{j}"] = S; L.append(f"v{i}{j}")
            layers.append(L)
        ct = np.zeros(dim); ct[0] = 8.0; sets["t"] = Pt(ct); layers.append(["t"])
        E = [(u, v) for A_, B_ in zip(layers[:-1], layers[1:]) for u in A_ for v in B_]
        L_ = SQ if it % 2 == 0 else L2
        g = G(sets, E, "s", "t", L_)
        r, rh = relax(g), relax(g, hull=True)
        worst = max(worst, (rh - r) / max(1, abs(rh)))
    print(f"{kind:9s}: max (REL_H - REL)/REL_H over 12 instances = {worst:.2e}")
