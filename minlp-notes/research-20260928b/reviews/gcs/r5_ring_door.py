"""Props 9-10 and Theorem 7 (order-1 motion planning) with the reviewer's code.

Region formulation: x_v = (a_v, b_v) in X_v^2, continuity b_u = a_v on every
edge, cost ||b_u - a_u|| charged on out-edges of u.  Door formulation: vertices
start, goal and doors X_u cap X_v; edges between vertices in a common region.

(1) Ring around a wall of half-height H: region REL, REL_H, +lifted 2-cycle
    cuts; OPT; door REL/REL_H with and without degree constraints; door aperture.
(2) Theorem 7 claim 3 on random acyclic corridors: REL_H(region DAG) <= REL(line
    graph = directed door DAG), and OPT(region) = OPT(door).
"""
import itertools
import numpy as np
import cvxpy as cp
from rgcs import *

rng = np.random.default_rng(0)


def box_intersect(A, B):
    lo = np.maximum(A.V.min(0), B.V.min(0))
    hi = np.minimum(A.V.max(0), B.V.max(0))
    if np.any(lo > hi + 1e-12):
        return None
    return Box(lo, hi)


def sq_box(Bx):
    lo, hi = Bx.V.min(0), Bx.V.max(0)
    return Box(np.r_[lo, lo], np.r_[hi, hi])


def region_gcs(regions, redges, start, goal, s_regs, t_regs):
    sets = {"s": Pt(np.r_[start, start]), "t": Pt(np.r_[goal, goal])}
    for k, Bx in regions.items():
        sets[k] = sq_box(Bx)
    E = [("s", r) for r in s_regs] + list(redges) + [(r, "t") for r in t_regs]
    k = len(start)
    Mu = np.hstack([np.zeros((k, k)), np.eye(k)])
    Mv = np.hstack([-np.eye(k), np.zeros((k, k))])
    ec = {e: (Mu, Mv, np.zeros(k)) for e in E}
    return G(sets, E, "s", "t", tailseg(k), ec)


def door_gcs(regions, redges, start, goal, s_regs, t_regs, directed_line=False):
    """If directed_line: vertices = directed region edges (line graph of the region DAG).
    Otherwise: undirected doors, edges between any two vertices in a common region."""
    sets = {"S": Pt(start), "T": Pt(goal)}
    member = {}  # region -> list of door vertices inside it
    if directed_line:
        for (u, v) in redges:
            D = box_intersect(regions[u], regions[v])
            if D is not None:
                sets[(u, v)] = D
        E = []
        for r in s_regs:
            for (u, v) in redges:
                if u == r and (u, v) in sets:
                    E.append(("S", (u, v)))
        for (a, b) in redges:
            for (c, d) in redges:
                if b == c and (a, b) in sets and (c, d) in sets:
                    E.append(((a, b), (c, d)))
        for r in t_regs:
            for (u, v) in redges:
                if v == r and (u, v) in sets:
                    E.append(((u, v), "T"))
        return G(sets, E, "S", "T", L2)
    doors = {}
    for (u, v) in redges:
        key = tuple(sorted((u, v)))
        if key not in doors:
            D = box_intersect(regions[u], regions[v])
            if D is not None:
                doors[key] = D
    for key, D in doors.items():
        sets[key] = D
        for r in key:
            member.setdefault(r, []).append(key)
    for r in s_regs:
        member.setdefault(r, []).append("S")
    for r in t_regs:
        member.setdefault(r, []).append("T")
    E = set()
    for r, vs in member.items():
        for a in vs:
            for b in vs:
                if a != b and b != "S" and a != "T":
                    E.add((a, b))
    return G(sets, sorted(E, key=str), "S", "T", L2), member


def aperture_sec(V):
    U = V / np.linalg.norm(V, axis=1, keepdims=True)
    a = cp.Variable(V.shape[1])
    t = cp.Variable()
    cp.Problem(cp.Maximize(t), [U @ a >= t, cp.norm(a, 2) <= 1]).solve(solver="CLARABEL")
    return 1.0 / t.value if t.value > 1e-12 else np.inf


if __name__ == "__main__":
    print("==== (1) ring around a wall")
    for H in [1, 2, 5, 20]:
        regions = dict(L=Box([-2, -H - 1], [-1, H + 1]), R=Box([1, -H - 1], [2, H + 1]),
                       T=Box([-2, H], [2, H + 1]), B=Box([-2, -H - 1], [2, -H]))
        start, goal = np.array([-1.5, 0.0]), np.array([1.5, 0.0])
        und = [("L", "T"), ("T", "L"), ("L", "B"), ("B", "L"), ("T", "R"), ("R", "T"), ("B", "R"), ("R", "B")]
        g = region_gcs(regions, und, start, goal, ["L"], ["R"])
        o = opt(g)
        vals = dict(REL=relax(g), REL_H=relax(g, hull=True), REL_2cyc=relax(g, lifted2=True, two_cycle=True),
                    REL_H_2cyc=relax(g, hull=True, lifted2=True, two_cycle=True))
        closed = 2 + 2 * np.sqrt(H * H + 0.25)
        gd, member = door_gcs(regions, und, start, goal, ["L"], ["R"])
        od = opt(gd)
        dvals = dict(door_REL=relax(gd), door_REL_H=relax(gd, hull=True), door_REL_H_nodeg=relax(gd, hull=True, deg=False))
        secmax = 0
        for r, vs in member.items():
            for a, b in itertools.permutations(vs, 2):
                Va, Vb = gd.sets[a].V, gd.sets[b].V
                Dv = np.array([vb - va for va in Va for vb in Vb])
                secmax = max(secmax, aperture_sec(Dv))
        print(f"H={H:2d} OPT_region={o:.5f} (closed form {closed:.5f}) " + " ".join(f"{k}={v:.5f}" for k, v in vals.items())
              + f" | OPT_door={od:.5f} " + " ".join(f"{k}={v:.5f}" for k, v in dvals.items())
              + f" | sec(theta_door)={secmax:.5f} (sqrt5/2={np.sqrt(5)/2:.5f}) ratio_region={o/vals['REL_H_2cyc']:.3f}")

    print("\n==== (2) Theorem 7 claim 3 on random acyclic corridors (directed region DAG vs its line graph)")
    worst = -np.inf
    nviol = 0
    for it in range(12):
        nl = int(rng.integers(2, 4))
        regions = {}
        layers = []
        x0 = 0.0
        for i in range(nl + 1):
            w = int(rng.integers(1, 3)) if 0 < i < nl else 1
            L = []
            for j in range(w):
                lo = np.array([x0 + rng.uniform(-0.3, 0.0), rng.uniform(-3, 1)])
                hi = lo + np.array([rng.uniform(1.5, 2.5), rng.uniform(1.0, 3.0)])
                name = f"r{i}{j}"
                regions[name] = Box(lo, hi)
                L.append(name)
            layers.append(L)
            x0 += 1.6
        redges = []
        for a, b in zip(layers[:-1], layers[1:]):
            for u in a:
                for v in b:
                    if box_intersect(regions[u], regions[v]) is not None:
                        redges.append((u, v))
        r0 = layers[0][0]
        rN = layers[-1][0]
        start = regions[r0].V.min(0) + 0.2
        goal = regions[rN].V.max(0) - 0.2
        g = region_gcs(regions, redges, start, goal, [r0], [rN])
        gl = door_gcs(regions, redges, start, goal, [r0], [rN], directed_line=True)
        oR, oL = opt(g), opt(gl)
        if not np.isfinite(oR):
            print(f"#{it} infeasible corridor, skipped")
            continue
        rhG = relax(g, hull=True)
        rG = relax(g)
        rL = relax(gl)
        rhL = relax(gl, hull=True)
        diff = rhG - rL
        worst = max(worst, diff)
        bad = diff > 1e-5 or abs(oR - oL) > 1e-5 or rL > rhL + 1e-5 or rhL > oL + 1e-5
        nviol += bad
        print(f"#{it:2d} |E_G|={len(g.E):2d} OPT_G={oR:.5f} OPT_L={oL:.5f} REL(G)={rG:.5f} REL_H(G)={rhG:.5f} "
              f"REL(L)={rL:.5f} REL_H(L)={rhL:.5f}" + ("  VIOL" if bad else ""))
    print("max REL_H(G) - REL(L):", worst, " violations:", nviol)
