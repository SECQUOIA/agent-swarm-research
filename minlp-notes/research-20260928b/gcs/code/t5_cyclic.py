"""T5: cyclic graphs.

(a) Common Euclidean norm, random cyclic digraphs of boxes/points (overlaps allowed), REL_H
    WITHOUT degree constraints.  Checks
      REL_H <= OPT <= reopt(shortcut of pair-graph walk) <= walk cost <= E[round] <= sum_e y_e cav_e.
(b) Squared lengths: the path version fails even with degree constraints and the hull.
    Instance C2: s={-1}, X1=[-1/2,1/2], X2={0}, X3={0}, t={1};
      E = (s,1),(1,2),(2,1),(1,t),(s,3),(3,t).  Explicit REL_H point with value 3/2 and
      sum_e y_e cav_e = 3/2, while OPT = 2.  Shortest walk = 1.
    Instance C3: same with the 2-cycle replaced by the 3-cycle 1->2->4->1 (X4={0}); survives
      two-cycle cuts; generalized subtour cut on S={1,2,4} removes it.
Usage: python3 t5_cyclic.py [seed] [n]
"""
import sys
import numpy as np
import cvxpy as cp
from gcslib import *

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 30

viol, gaps = 0, []
cnt = 0
while cnt < N:
    nv = int(rng.integers(5, 8))
    sets = {}
    for v in range(nv):
        c = rng.uniform(-4, 4, 2)
        if v in (0, nv - 1) or rng.random() < 0.25:
            sets[v] = point(c)
        else:
            w = rng.uniform(0.2, 1.5, 2)
            sets[v] = box(c - w, c + w)
    E = [(u, v) for u in range(nv) for v in range(nv)
         if u != v and v != 0 and u != nv - 1 and rng.random() < 0.45]
    g = GCS(sets, E, 0, nv - 1, L2)
    if not all_paths(g, 1):
        continue
    cnt += 1
    rh, sol = relax(g, hull=True, degree=False, return_sol=True)
    o = opt(g)
    dp, walk, xs = pair_graph_path(g, sol)
    wc = walk_cost(g, walk, xs)
    pth, pxs = shortcut(walk, xs)
    sc = walk_cost(g, pth, pxs)
    ro = path_cost(g, pth)
    Er = expected_round(g, sol)
    jb = jensen_bound(g, sol)
    chain = [rh, o, ro, sc, wc, Er, jb]
    ok = all(chain[i] <= chain[i + 1] + 1e-5 * max(1, abs(chain[i + 1])) + 1e-6 for i in range(len(chain) - 1))
    viol += not ok
    gaps.append(o - rh)
    print(f"#{cnt:2d} |V|={nv} |E|={len(E):2d} REL_H(nodeg)={rh:.5f} OPT={o:.5f} walklen={len(walk)-1} "
          f"shortcut={sc:.5f} walk={wc:.5f} E={Er:.5f} JB={jb:.5f} {'' if ok else 'VIOLATION'}", flush=True)
print(f"(a) common l2, cyclic, no degree constraints: n={cnt} violations={viol} #gap>1e-5={np.sum(np.array(gaps)>1e-5)}")


def c_instance(three=False):
    sets = {"s": point([-1.0]), 1: box([-0.5], [0.5]), 2: point([0.0]), 3: point([0.0]), "t": point([1.0])}
    E = [("s", 1), (1, "t"), ("s", 3), (3, "t")]
    if three:
        sets[4] = point([0.0])
        E += [(1, 2), (2, 4), (4, 1)]
    else:
        E += [(1, 2), (2, 1)]
    return GCS(sets, E, "s", "t", SQ)


for three in (False, True):
    g = c_instance(three)
    name = "C3" if three else "C2"
    o = opt(g)
    rh_deg = relax(g, hull=True, degree=True)
    rh_nodeg, sol_nd = relax(g, hull=True, degree=False, return_sol=True)
    dpw, walk_nd, xs_nd = pair_graph_path(g, sol_nd)
    print(f"({'C3' if three else 'C2'}) walk version at the REL_H(nodeg) optimum: value={rh_nodeg:.6f} "
          f"pair-graph walk cost={walk_cost(g, walk_nd, xs_nd):.6f} (walk {walk_nd}) E[round]={expected_round(g, sol_nd):.6f} "
          f"sum y*cav={jensen_bound(g, sol_nd):.6f}")

    def two_cycle(g, V):
        cons = []
        y = V["y"]
        for (u, v) in g.edges:
            if (v, u) in y and v not in (g.s, g.t):
                cons.append(y[(u, v)] + y[(v, u)] <= sum(y[e] for e in g.inn[v]))
        return cons

    rh_2c = relax(g, hull=True, degree=True, extra=two_cycle)

    def gsec(g, V):
        y = V["y"]
        S = [1, 2, 4] if three else [1, 2]
        ES = [e for e in g.edges if e[0] in S and e[1] in S]
        yv = {v: sum(y[e] for e in g.inn[v]) for v in S}
        return [sum(y[e] for e in ES) <= sum(yv[v] for v in S if v != k) for k in S]

    rh_gsec = relax(g, hull=True, degree=True, extra=gsec)
    # explicit point
    y = {e: 0.5 for e in g.edges}
    z = {e: np.zeros(1) for e in g.edges}
    zp = {e: np.zeros(1) for e in g.edges}
    z[("s", 1)] = np.array([-0.5]); zp[("s", 1)] = np.array([-0.25])
    z[(1, "t")] = np.array([0.25]); zp[(1, "t")] = np.array([0.5])
    z[("s", 3)] = np.array([-0.5]); z[(3, "t")] = np.zeros(1); zp[(3, "t")] = np.array([0.5])
    first = (1, 2)
    last = (4, 1) if three else (2, 1)
    z[first] = np.array([-0.25]); zp[last] = np.array([0.25])
    val = sum(y[e] * g.cost[e].val(z[e] / y[e], zp[e] / y[e]) for e in g.edges)
    jb = jensen_bound(g, dict(y=y, z=z, zp=zp))
    print(f"({name}) OPT={o:.6f} REL_H(deg)={rh_deg:.6f} REL_H(nodeg)={rh_nodeg:.6f} REL_H(deg,2-cycle cuts)={rh_2c:.6f} "
          f"REL_H(deg,GSEC)={rh_gsec:.6f}; explicit point value={val:.6f}, sum y*cav at it={jb:.6f}")
