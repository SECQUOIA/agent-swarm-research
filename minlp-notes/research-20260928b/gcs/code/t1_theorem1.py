"""T1: Theorem 1 (acyclic, no edge constraints) on random DAGs of boxes/points/triangles
with mixed convex lengths (l2, squared l2, l1, affine).  Checks the chain

  REL <= REL_H <= OPT <= reopt(pair path) <= pair-DP cost <= E[round] <= sum_e y_e cav_e
       <= REL_H + sum_e y_e Delta_e <= REL_H + max_P sum_{e in P} Delta_e

and records violations (tolerance 1e-5 relative + 1e-6 absolute).
Usage: python3 t1_theorem1.py [seed] [n_instances] [size multiplier]
"""
import sys
import numpy as np
from gcslib import *

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 40
BIG = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0   # set-size multiplier (larger -> more gaps)


def rand_set(d, c, overlap):
    r = rng.random()
    if d == 2 and r < 0.2:
        P = c + rng.uniform(-1.0, 1.0, (3, 2)) * (1.2 if overlap else 0.6) * BIG
        return poly_from_vertices2d(P)
    if r < 0.3:
        return point(c + rng.uniform(-0.5, 0.5, d))
    w = rng.uniform(0.1, 1.2 if overlap else 0.6, d) * BIG
    return box(c - w, c + w)


def rand_cost(d):
    k = rng.choice(["l2", "sq", "l1", "aff"], p=[0.35, 0.25, 0.2, 0.2])
    if k == "aff":
        return Cost("aff", c=rng.standard_normal(d), d=rng.standard_normal(d), b0=float(rng.uniform(0, 3)))
    return Cost(k)


def make():
    d = int(rng.choice([1, 2, 3], p=[0.25, 0.5, 0.25]))
    L, k = int(rng.integers(2, 4)), int(rng.integers(2, 4))
    overlap = rng.random() < 0.5
    sets = {"s": point(np.zeros(d))}
    layers = []
    for i in range(1, L + 1):
        lay = []
        for j in range(k):
            c = np.r_[1.5 * i, rng.uniform(-2, 2, d - 1)] if d > 1 else np.array([1.5 * i + rng.uniform(-0.7, 0.7)])
            sets[f"{i}_{j}"] = rand_set(d, c, overlap)
            lay.append(f"{i}_{j}")
        layers.append(lay)
    sets["t"] = point(np.r_[1.5 * (L + 1), np.zeros(d - 1)]) if rng.random() < 0.7 else box(
        np.r_[1.5 * (L + 1) - 0.3, -0.3 * np.ones(d - 1)], np.r_[1.5 * (L + 1) + 0.3, 0.3 * np.ones(d - 1)])
    E = [("s", v) for v in layers[0]] + [(v, "t") for v in layers[-1]]
    for a, b in zip(layers, layers[1:]):
        E += [(u, v) for u in a for v in b if rng.random() < 0.85]
    for a, b in zip(layers, layers[2:]):
        E += [(u, v) for u in a for v in b if rng.random() < 0.25]
    costs = {e: rand_cost(d) for e in E}
    g = GCS(sets, E, "s", "t", costs)
    return g if all_paths(g, 1) else None


viol, rows = 0, []
cnt = 0
while cnt < N:
    g = make()
    if g is None:
        continue
    cnt += 1
    r = relax(g)
    rh, sol = relax(g, hull=True, return_sol=True)
    o = opt(g)
    dp, walk, xs = pair_graph_path(g, sol)
    ro = path_cost(g, walk)
    Er = expected_round(g, sol)
    jb = jensen_bound(g, sol)
    dl = {e: delta_e(g, e) for e in g.edges}
    sd = sum(sol["y"][e] * dl[e] for e in g.edges if sol["y"][e] > 1e-7)
    mp = max_path_weight(g, dl)
    chain = [r, rh, o, ro, dp, Er, jb, rh + sd, rh + mp]
    names = ["REL", "REL_H", "OPT", "reopt", "pairDP", "E[round]", "sum y cav", "REL_H+sum yDelta", "REL_H+maxP Delta"]
    ok = True
    for i in range(len(chain) - 1):
        a, b = chain[i], chain[i + 1]
        if a > b + 1e-5 * max(1, abs(b)) + 1e-6:
            ok = False
            print(f"  VIOLATION {names[i]}={a:.6f} > {names[i+1]}={b:.6f}")
    viol += not ok
    rows.append(chain)
    print(f"#{cnt:3d} |V|={len(g.V):2d} |E|={len(g.edges):3d} REL={r:8.4f} REL_H={rh:8.4f} OPT={o:8.4f} "
          f"pairDP={dp:8.4f} E={Er:8.4f} JB={jb:8.4f} JB+={rh+mp:8.4f}", flush=True)
rows = np.array(rows)
print(f"instances={len(rows)} violations={viol}")
print(f"#(OPT-REL>1e-5)={np.sum(rows[:,2]-rows[:,0]>1e-5)}  #(OPT-REL_H>1e-5)={np.sum(rows[:,2]-rows[:,1]>1e-5)}  "
      f"#(REL_H-REL>1e-5)={np.sum(rows[:,1]-rows[:,0]>1e-5)}  #(pairDP path suboptimal>1e-5)={np.sum(rows[:,3]-rows[:,2]>1e-5)}")
