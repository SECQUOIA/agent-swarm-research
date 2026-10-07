"""Spatial branch and bound with SDP-Lagrangian node bounds for the power-flow
relaxation R (pf_model).  Branching variable: the angle of W_pq = V_p conj(V_q)
for a line (p, q).  A node restricts, for some pairs, the angle of W_pq to a cone
given by two exact rational directions:
    u1 = (c1, s1), u2 = (c2, s2):  s1*w_R - c1*w_I <= 0  (angle >= dir u1)
                                   c2*w_I - s2*w_R <= 0  (angle <= dir u2)
with w_R = e_p e_q + f_p f_q, w_I = f_p e_q - e_p f_q.  Children split a cone at a
rational direction, so the two children cover the parent exactly (the halfplanes
through the split direction are complementary).  The root cone of a pair is the
whole plane; its first split is w_I >= 0 / w_I <= 0.  Every node bound is the
rigorous Lagrangian certificate of pf_cert applied to R plus the node rows.

    python3 pf_bb.py <name> <time_limit_s> [rel_tol]
"""
import heapq
import json
import math
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

import pf_cert as pc
import pf_model as pm
import pf_sdp as ps


def wRI(p, q):
    def qadd(Q, i, j, c):
        if i > j:
            i, j = j, i
        Q[(i, j)] = Q.get((i, j), Fr(0)) + c
    E = lambda k: 2 * k
    F = lambda k: 2 * k + 1
    WR, WI = {}, {}
    qadd(WR, E(p), E(q), Fr(1)); qadd(WR, F(p), F(q), Fr(1))
    qadd(WI, F(p), E(q), Fr(1)); qadd(WI, E(p), F(q), Fr(-1))
    return WR, WI


def half_row(p, q, a, b, name):
    """row  a*w_R + b*w_I <= 0"""
    WR, WI = wRI(p, q)
    Q = {k: a * WR.get(k, 0) + b * WI.get(k, 0) for k in set(WR) | set(WI)}
    Q = {k: v for k, v in Q.items() if v != 0}
    return dict(name=name, lin={}, Q=Q, qy={}, lb=None, ub=Fr(0), kind="branch")


def rat_dir(phi):
    """exact rational direction (c, s) close to (cos phi, sin phi)"""
    return Fr(math.cos(phi)).limit_denominator(10**12), Fr(math.sin(phi)).limit_denominator(10**12)


def node_rows(cones):
    rows = []
    for (p, q), (lo, hi) in cones.items():
        # lo, hi: angles (floats) with rational directions stored alongside
        (phi1, d1), (phi2, d2) = lo, hi
        if d1 is not None:   # angle >= phi1:  s1 w_R - c1 w_I <= 0
            c1, s1 = d1
            rows.append(half_row(p, q, s1, -c1, f"B{p}_{q}lo"))
        if d2 is not None:   # angle <= phi2:  c2 w_I - s2 w_R <= 0
            c2, s2 = d2
            rows.append(half_row(p, q, -s2, c2, f"B{p}_{q}hi"))
    return rows


def lines_of(M):
    pairs = set()
    for r in M["rows"]:
        if r["kind"] == "flow":
            ks = {i // 2 for (i, j) in r["Q"] for i in (i, j)}
            ks2 = set()
            for (i, j) in r["Q"]:
                ks2 |= {i // 2, j // 2}
            if len(ks2) == 2:
                pairs.add(tuple(sorted(ks2)))
    return sorted(pairs)


def solve_node(M0, cones, log):
    M = dict(M0)
    M["rows"] = [r for r in M0["rows"] if r["kind"] != "angle"] + node_rows(cones)
    best = None
    for kw in (dict(chordal_decomposition_enable=False),):   # (chordal decomposition hangs on the 39-bus case)
        try:
            val, st, raw = ps.solve_dual_vec(M, **kw)
        except Exception as e:
            log(f"    solver failed ({kw}): {e.__class__.__name__}")
            continue
        W = ps.solve_dual_vec.W
        res = pc.certify(M, raw, log=lambda s: None)
        if res is None:
            continue
        b = res[0]
        if best is None or b > best[0]:
            best = (b, W, val, st)
        if st == "optimal":
            break
    return best


def choose_branch(M, W, pairs):
    best, arg = -1, None
    for (p, q) in pairs:
        Wpp = W[2 * p, 2 * p] + W[2 * p + 1, 2 * p + 1]
        Wqq = W[2 * q, 2 * q] + W[2 * q + 1, 2 * q + 1]
        wr = W[2 * p, 2 * q] + W[2 * p + 1, 2 * q + 1]
        wi = W[2 * p + 1, 2 * q] - W[2 * p, 2 * q + 1]
        viol = (Wpp * Wqq - (wr * wr + wi * wi)) / max(Wpp * Wqq, 1e-12)
        if viol > best:
            best, arg = viol, (p, q, math.atan2(wi, wr))
    return best, arg


def run(name, tlim, rel_tol=1e-6, UB=None, log=print):
    t0 = time.time()
    M0 = pm.decode(name)
    pairs = lines_of(M0)
    # angle limits of the polar model give the root cones: a <= theta_p - theta_q <= b with |a|, |b| < pi/2
    # is implied by  w_I >= ta w_R  and  w_I <= tb w_R  (directions (1, ta), (1, tb)); these rows are
    # exactly the pf_model angle rows, which solve_node drops and replaces by the cones.
    root = {}
    for (p_, q_), (A0, B0, ta, tb) in M0["angle"].items():
        root[(p_, q_)] = ((float(A0), (Fr(1), ta)), (float(B0), (Fr(1), tb)))
    heap = []
    cnt = 0
    res = solve_node(M0, root, log)
    b, W, val, st = res
    log(f"root: bound {float(b)!r} (numeric {val!r}, {st})  UB {UB}")
    heapq.heappush(heap, (float(b), cnt, dict(root), b, W))
    closed = []      # certified bounds of fathomed leaves
    nodes = 1
    while heap and time.time() - t0 < tlim:
        fb, _, cones, b, W = heapq.heappop(heap)
        if UB is not None and fb >= UB - rel_tol * abs(UB):
            closed.append(b)
            continue
        viol, arg = choose_branch(M0, W, pairs)
        p, q, phi = arg
        lo, hi = cones.get((p, q), ((-math.pi, None), (math.pi, None)))
        a1, a2 = lo[0], hi[0]
        if lo[1] is None and hi[1] is None:
            mid = 0.0 if not (a1 < phi < a2) else phi
            mid = 0.0
        else:
            mid = 0.5 * (a1 + a2)
        dmid = rat_dir(mid)
        kids = [dict(cones), dict(cones)]
        kids[0][(p, q)] = (lo, (mid, dmid))
        kids[1][(p, q)] = ((mid, dmid), hi)
        for kc in kids:
            # a cone wider than pi cannot be written with the two halfplanes; the root split
            # (at angle 0 from the full circle) gives [-pi, 0] and [0, pi], which are fine.
            r = solve_node(M0, kc, log)
            nodes += 1
            if r is None:
                log("    node failed: keeping parent bound")
                r = (b, W, None, None)
            cb, cW, cval, cst = r
            cb = max(cb, b)
            cnt += 1
            heapq.heappush(heap, (float(cb), cnt, kc, cb, cW))
        glb = min([h[0] for h in heap] + [float(x) for x in closed]) if heap or closed else float(b)
        log(f"  nodes {nodes}: split line {p}-{q} at {mid:.4f} (viol {viol:.2e}); LB {glb!r} open {len(heap)} t {time.time()-t0:.0f}s")
    allb = [h[3] for h in heap] + closed
    LB = min(allb)
    return LB, nodes, len(heap)


if __name__ == "__main__":
    name = sys.argv[1]
    tl = float(sys.argv[2])
    UB = float(sys.argv[3]) if len(sys.argv) > 3 else None
    LB, nodes, nopen = run(name, tl, UB=UB)
    print(f"FINAL {name}: certified LB {float(LB)!r} (exact {LB}) nodes {nodes} open {nopen}")
