"""T8: edge constraints.

(a) Negative (Prop. E1): 1D, acyclic, pairwise-disjoint sets, translation constraints x_v = x_u + 10
    on every edge, zero lengths: the MICP is infeasible but REL = REL_H = 0; adding a direct
    s->t edge of constant length 1 gives OPT = 1, REL = REL_H = 0.
(b) Positive (Thm E2): cubic Bezier segments with C^1 continuity (p3^u = p0^v, p3^u - p2^u = p1^v - p0^v),
    control points in the region, cost = control-polygon length, on DAGs of boxes.  The line-graph
    ("door") reformulation with door variables sigma_e = (P_e, d_e) has no edge constraints,
    the same optimum, and Theorem 1 applies to it.  Compare REL/REL_H of both formulations and
    check OPT <= E[round] from REL_H of the line-graph formulation.
Usage: python3 t8_edge.py [seed] [n_random]
"""
import sys
import numpy as np
import cvxpy as cp
from gcslib import *

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
NR = int(sys.argv[2]) if len(sys.argv) > 2 else 8

# (a)
S = {"s": point([0.0]), "A": box([9.0], [11.0]), "P": point([21.0]), "M": point([19.0]),
     "B": box([29.0], [31.0]), "t": point([40.0])}
E = [("s", "A"), ("A", "P"), ("A", "M"), ("P", "B"), ("M", "B"), ("B", "t")]
tr = {e: (lambda z, zp, y: [zp == z + 10.0 * y]) for e in E}
g = GCS(S, E, "s", "t", Cost("zero"), econs=tr)
print(f"(a) translation constraints: REL={relax(g):.6f} REL_H={relax(g, hull=True):.6f} OPT={opt(g)}")
g2 = GCS(S, E + [("s", "t")], "s", "t", {**{e: Cost("zero") for e in E}, ("s", "t"): Cost("aff", c=np.zeros(1), d=np.zeros(1), b0=1.0)}, econs=tr)
print(f"(a') with bypass edge of length 1: REL={relax(g2):.6f} REL_H={relax(g2, hull=True):.6f} OPT={opt(g2):.6f}")


# (b)
def sel(i, n=8):
    M = np.zeros((2, n))
    M[:, 2 * i:2 * i + 2] = np.eye(2)
    return M


def region_formulation(boxes, E, start, goal):
    """GCS with vertex = region (4 control points in R^8), edge constraints = C^1 continuity."""
    sets = {"s": point(start), "t": point(goal)}
    for v, (lo, hi) in boxes.items():
        sets[v] = box(np.tile(lo, 4), np.tile(hi, 4))
    # cost of u's curve on out-edge (u, v): sum_k |p_{k+1} - p_k| (acts on the first 8 of 16 coordinates)
    seglen = Cost("socsum", terms=[(np.hstack([sel(k + 1) - sel(k), np.zeros((2, 8))]), np.zeros(2)) for k in range(3)])
    seglen_t = Cost("socsum", terms=[(np.hstack([sel(k + 1) - sel(k), np.zeros((2, 2))]), np.zeros(2)) for k in range(3)])
    costs, econs = {}, {}
    for (u, v) in E:
        if u == "s":
            costs[(u, v)] = Cost("zero")
            econs[(u, v)] = lambda z, zp, y: [zp[0:2] == z, zp[2:4] == z]
        elif v == "t":
            costs[(u, v)] = seglen_t
            econs[(u, v)] = lambda z, zp, y: [z[6:8] == zp, z[4:6] == zp]
        else:
            costs[(u, v)] = seglen
            econs[(u, v)] = lambda z, zp, y: [z[6:8] == zp[0:2], z[6:8] - z[4:6] == zp[2:4] - zp[0:2]]
    return GCS(sets, E, "s", "t", costs, econs)


def line_formulation(boxes, E, start, goal):
    """Line-graph GCS: vertex = region edge e with sigma_e = (P, d) in R^4; no edge constraints."""
    sets = {"S'": point(np.r_[start, 0, 0]), "T'": point(np.r_[goal, 0, 0])}
    for (u, v) in E:
        if u == "s":
            sets[(u, v)] = point(np.r_[start, 0.0, 0.0])
        elif v == "t":
            sets[(u, v)] = point(np.r_[goal, 0.0, 0.0])
        else:
            (lu, hu), (lv, hv) = boxes[u], boxes[v]
            I2, Z2 = np.eye(2), np.zeros((2, 2))
            A = np.vstack([np.hstack([I2, Z2]), -np.hstack([I2, Z2]),       # P in X_u cap X_v
                           np.hstack([I2, -I2]), -np.hstack([I2, -I2]),     # P - d in X_u
                           np.hstack([I2, I2]), -np.hstack([I2, I2])])      # P + d in X_v
            b = np.r_[np.minimum(hu, hv), -np.maximum(lu, lv), hu, -lu, hv, -lv]
            sets[(u, v)] = Set("poly", A=A, b=b)
    cv = Cost("socsum", terms=[(np.hstack([np.zeros((2, 2)), np.eye(2), np.zeros((2, 4))]), np.zeros(2)),
                               (np.hstack([-np.eye(2), -np.eye(2), np.eye(2), -np.eye(2)]), np.zeros(2)),
                               (np.hstack([np.zeros((2, 6)), np.eye(2)]), np.zeros(2))])
    LE, costs = [], {}
    for e in E:
        if e[0] == "s":
            LE.append(("S'", e))
            costs[("S'", e)] = Cost("zero")
        if e[1] == "t":
            LE.append((e, "T'"))
            costs[(e, "T'")] = Cost("zero")
        for f in E:
            if e[1] == f[0] and e[1] not in ("s", "t"):
                LE.append((e, f))
                costs[(e, f)] = cv
    return GCS(sets, LE, "S'", "T'", costs)


def lanes_instance():
    boxes = {0: ([0, 0], [2, 2]), 1: ([1.5, 1.2], [4, 3]), 2: ([1.5, -1], [4, 0.8]), 3: ([3.5, 0], [6, 2])}
    boxes = {k: (np.array(a, float), np.array(b, float)) for k, (a, b) in boxes.items()}
    E = [("s", 0), (0, 1), (0, 2), (1, 3), (2, 3), (3, "t")]
    return boxes, E, np.array([0.5, 1.0]), np.array([5.5, 1.0])


def random_instance():
    # corridor of K columns, each with 2 overlapping or separated lanes; DAG left -> right
    K = int(rng.integers(2, 4))
    boxes, cols = {}, []
    idx = 0
    y0 = 0.0
    for k in range(K + 2):
        col = []
        if k in (0, K + 1):
            boxes[idx] = (np.array([2.0 * k, -1.0]), np.array([2.0 * k + 2.5, 1.0]))
            col.append(idx)
            idx += 1
        else:
            gap = rng.uniform(-0.3, 0.3)
            boxes[idx] = (np.array([2.0 * k, gap + 0.05]), np.array([2.0 * k + 2.5, rng.uniform(1.0, 2.0)]))
            boxes[idx + 1] = (np.array([2.0 * k, -rng.uniform(1.0, 2.0)]), np.array([2.0 * k + 2.5, gap - 0.05]))
            col += [idx, idx + 1]
            idx += 2
        cols.append(col)
    E = [("s", cols[0][0])]
    for a, b in zip(cols, cols[1:]):
        for u in a:
            for v in b:
                lo = np.maximum(boxes[u][0], boxes[v][0])
                hi = np.minimum(boxes[u][1], boxes[v][1])
                if np.all(lo <= hi):
                    E.append((u, v))
    E.append((cols[-1][0], "t"))
    start = np.array([0.3, rng.uniform(-0.8, 0.8)])
    goal = np.array([2.0 * (K + 1) + 2.2, rng.uniform(-0.8, 0.8)])
    return boxes, E, start, goal


insts = [lanes_instance()] + [random_instance() for _ in range(NR)]
viol = 0
for i, (boxes, E, st, gl) in enumerate(insts):
    gR = region_formulation(boxes, E, st, gl)
    gL = line_formulation(boxes, E, st, gl)
    oR, oL = opt(gR), opt(gL)
    rR, rRH = relax(gR), relax(gR, hull=True)
    rL = relax(gL)
    rLH, sol = relax(gL, hull=True, return_sol=True)
    Er = expected_round(gL, sol)
    dp, walk, xs = pair_graph_path(gL, sol)
    ok = abs(oR - oL) < 1e-5 * max(1, oR) and oL <= Er + 1e-5 * max(1, oL) and dp <= Er + 1e-5 * max(1, Er) and rLH <= oL + 1e-6
    viol += not ok
    print(f"(b) inst {i}: regions={len(boxes)} OPT_region={oR:.5f} OPT_line={oL:.5f} | REL_region={rR:.5f} "
          f"REL_H,region={rRH:.5f} REL_line={rL:.5f} REL_H,line={rLH:.5f} E[round]={Er:.5f} pairDP={dp:.5f} "
          f"{'' if ok else 'VIOLATION'}", flush=True)
print(f"(b) n={len(insts)} violations={viol}")

# (c) ring around a wall with a DAG of regions L -> {T, B} -> R and cubic Bezier C^1 segments
for H in [1.0, 5.0, 20.0]:
    boxes = {"L": ([-2, -H - 1], [-1, H + 1]), "R": ([1, -H - 1], [2, H + 1]), "T": ([-2, H], [2, H + 1]), "B": ([-2, -H - 1], [2, -H])}
    boxes = {k: (np.array(a, float), np.array(b, float)) for k, (a, b) in boxes.items()}
    E = [("s", "L"), ("L", "T"), ("L", "B"), ("T", "R"), ("B", "R"), ("R", "t")]
    st, gl = np.array([-1.5, 0.0]), np.array([1.5, 0.0])
    gR, gL = region_formulation(boxes, E, st, gl), line_formulation(boxes, E, st, gl)
    oR, oL = opt(gR), opt(gL)
    rR, rRH, rL = relax(gR), relax(gR, hull=True), relax(gL)
    rLH, sol = relax(gL, hull=True, return_sol=True)
    print(f"(c) ring-wall H={H:4}: OPT_region={oR:.5f} OPT_line={oL:.5f} REL_region={rR:.5f} REL_H,region={rRH:.5f} "
          f"REL_line={rL:.5f} REL_H,line={rLH:.5f} E[round]={expected_round(gL, sol):.5f}", flush=True)
