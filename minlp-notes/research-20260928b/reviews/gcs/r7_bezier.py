"""Cubic Bezier C^1 region formulation on the ring (Prop 9 remark, t8 claims) and its
line-graph reformulation (Theorem 7).

Region vertex v: control points r0..r3 in X_v (x in R^8); start/goal vertices fix all
four control points at the start/goal point.  Edge (u,v) constraints: r_{v,0} = r_{u,3},
r_{v,1} - r_{v,0} = r_{u,3} - r_{u,2}.  Cost of region u charged on its out-edges:
sum_k ||r_{u,k+1} - r_{u,k}|| (control-polygon length, Science Robotics (10)).

Line graph L (Theorem 7): vertex e=(u,v) carries sigma_e = (r_{u,2}, r_{u,3}) in
Sigma_e = {p2, p3 in X_u, p3 in X_v, 2 p3 - p2 in X_v}; edge (e,f) through v has length
||r1-r0|| + ||r2-r1|| + ||r3-r2|| with r0 = p3^e, r1 = 2 p3^e - p2^e, (r2, r3) = sigma_f.
"""
import numpy as np
import cvxpy as cp
from rgcs import *


def region4(Bx):
    lo, hi = Bx.V.min(0), Bx.V.max(0)
    return Box(np.tile(lo, 4), np.tile(hi, 4))


def cp_len(z):  # control polygon length of x = (r0,r1,r2,r3) in R^8 (works for y-scaled copies)
    return sum(cp.norm(z[2 * k + 2:2 * k + 4] - z[2 * k:2 * k + 2], 2) for k in range(3))


def np_len(x):
    return sum(np.linalg.norm(x[2 * k + 2:2 * k + 4] - x[2 * k:2 * k + 2]) for k in range(3))


def region_bezier(regions, redges, start, goal, s_regs, t_regs):
    sets = {"s": Pt(np.tile(start, 4)), "t": Pt(np.tile(goal, 4))}
    for k, Bx in regions.items():
        sets[k] = region4(Bx)
    E = [("s", r) for r in s_regs] + list(redges) + [(r, "t") for r in t_regs]
    I2 = np.eye(2)
    Z2 = np.zeros((2, 2))
    # rows: r_{v,0} - r_{u,3} = 0 ; r_{v,1} - r_{v,0} - r_{u,3} + r_{u,2} = 0
    Mu = np.block([[Z2, Z2, Z2, -I2], [Z2, Z2, I2, -I2]])
    Mv = np.block([[I2, Z2, Z2, Z2], [-I2, I2, Z2, Z2]])
    ec = {e: (Mu, Mv, np.zeros(4)) for e in E}
    lens = FnLen(lambda z, zp, y: cp_len(z), lambda x, xp: np_len(x))
    return G(sets, E, "s", "t", lens, ec)


class SigmaSet:
    """Sigma_e = {(p2,p3): p2,p3 in X_u, p3 in X_v, 2p3-p2 in X_v} as a Poly-like object."""

    def __init__(self, Xu, Xv):
        lou, hiu = Xu.V.min(0), Xu.V.max(0)
        lov, hiv = Xv.V.min(0), Xv.V.max(0)
        I = np.eye(2)
        Z = np.zeros((2, 2))
        rows, rhs = [], []
        for (A, lo, hi) in [(np.hstack([I, Z]), lou, hiu), (np.hstack([Z, I]), lou, hiu),
                            (np.hstack([Z, I]), lov, hiv), (np.hstack([-I, 2 * I]), lov, hiv)]:
            rows += [A, -A]
            rhs += [hi, -lo]
        self.A = np.vstack(rows)
        self.b = np.concatenate(rhs)
        self.dim = 4
        self.V = None

    def persp(self, z, y):
        return [self.A @ z <= self.b * y]

    def nonempty(self):
        x = cp.Variable(4)
        p = cp.Problem(cp.Minimize(0), [self.A @ x <= self.b])
        p.solve(solver="CLARABEL")
        return p.status == "optimal"


def line_bezier(regions, redges, start, goal, s_regs, t_regs):
    sets = {"S": Pt(np.r_[start, start]), "T": Pt(np.r_[goal, goal])}
    for (u, v) in redges:
        Sg = SigmaSet(regions[u], regions[v])
        if Sg.nonempty():
            sets[(u, v)] = Sg
    # start pseudo-edge sigma = (start, start); goal pseudo-edge sigma = (goal, goal)

    def through(z, zp):  # z = sigma_e (p2,p3), zp = sigma_f (r2, r3) -> length through the middle region
        r0 = z[2:4]
        r1 = 2 * z[2:4] - z[0:2]
        return cp.norm(r1 - r0, 2) + cp.norm(zp[0:2] - r1, 2) + cp.norm(zp[2:4] - zp[0:2], 2)

    def through_np(x, xp):
        r0 = x[2:4]
        r1 = 2 * x[2:4] - x[0:2]
        return np.linalg.norm(r1 - r0) + np.linalg.norm(xp[0:2] - r1) + np.linalg.norm(xp[2:4] - xp[0:2])

    lens = FnLen(lambda z, zp, y: through(z, zp), through_np)
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
    # region constraints for the middle region of each L-edge: r1 = 2p3 - p2 must lie in the middle region
    # (r0 = p3 lies in X_v and (r2, r3) in X_v by Sigma definitions); encode as edge constraints on L.
    g = G(sets, E, "S", "T", lens)
    return g




if __name__ == "__main__":
    for H in [1, 5, 20]:
        regions = dict(L=Box([-2, -H - 1], [-1, H + 1]), R=Box([1, -H - 1], [2, H + 1]),
                       T=Box([-2, H], [2, H + 1]), B=Box([-2, -H - 1], [2, -H]))
        start, goal = np.array([-1.5, 0.0]), np.array([1.5, 0.0])
        dag = [("L", "T"), ("L", "B"), ("T", "R"), ("B", "R")]
        g = region_bezier(regions, dag, start, goal, ["L"], ["R"])
        oR = opt(g)
        rR, rhR = relax(g), relax(g, hull=True)
        gl = line_bezier(regions, dag, start, goal, ["L"], ["R"])
        oL = opt(gl)
        rL, rhL = relax(gl), relax(gl, hull=True)
        print(f"H={H:2d} Bezier C1 DAG ring: OPT_region={oR:.5f} REL_region={rR:.5f} REL_H,region={rhR:.5f} | "
              f"OPT_line={oL:.5f} REL_line={rL:.5f} REL_H,line={rhL:.5f}  (order-1 OPT {2+2*np.sqrt(H*H+0.25):.5f})",
              flush=True)
