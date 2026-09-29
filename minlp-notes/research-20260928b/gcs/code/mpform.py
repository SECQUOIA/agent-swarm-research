"""Order-1 motion-planning formulations through overlapping boxes (Euclidean path length).

Region formulation (Marcucci et al., Science Robotics 2023 / SIOPT 2024 perspective form):
vertex = box region, variable (a_v, b_v) = segment inside the box, edge (u, v) for every
overlapping ordered pair, edge constraint b_u = a_v, cost ||b_u - a_u|| on the out-edge of u.
Options: degree constraints (always), two-cycle cuts with their perspective lift, region-level
vertex hull (pair variables per (in-edge, out-edge), no immediate backtracking).
Door formulation: GCS on doors X_u cap X_v (plus start, goal) with l2 lengths between doors
of a common region and no edge constraints (gcslib).
Adapted from research-20260928b/scouting/graphs-of-convex-sets/mp.py and door.py.
"""
import numpy as np
import cvxpy as cp
from gcslib import GCS, box, point, L2, relax as gcs_relax

SOLVER = "CLARABEL"


def overlap(B1, B2):
    return bool(np.all(np.maximum(B1[0], B2[0]) <= np.minimum(B1[1], B2[1]) + 1e-12))


def inbox(p, B):
    return bool(np.all(p >= B[0] - 1e-12) and np.all(p <= B[1] + 1e-12))


class Region:
    def __init__(self, boxes, start, goal):
        self.boxes = [(np.asarray(lo, float), np.asarray(hi, float)) for lo, hi in boxes]
        self.start, self.goal = np.asarray(start, float), np.asarray(goal, float)
        self.d = len(self.start)
        R = len(self.boxes)
        self.s, self.t = R, R + 1
        E = [(i, j) for i in range(R) for j in range(R) if i != j and overlap(self.boxes[i], self.boxes[j])]
        E += [(self.s, i) for i in range(R) if inbox(self.start, self.boxes[i])]
        E += [(i, self.t) for i in range(R) if inbox(self.goal, self.boxes[i])]
        self.E = E

    def pbox(self, i, w, y):
        lo, hi = self.boxes[i]
        return [w >= y * lo, w <= y * hi]

    def relax(self, two_cycle=False, hull=False, return_y=False):
        d, E, s, t = self.d, self.E, self.s, self.t
        y = {e: cp.Variable(nonneg=True) for e in E}
        za = {e: cp.Variable(d) for e in E}
        zb = {e: cp.Variable(d) for e in E}
        wa = {e: cp.Variable(d) for e in E}
        wb = {e: cp.Variable(d) for e in E}
        cons, obj = [], 0
        for e in E:
            u, v = e
            if u == s:
                cons += [za[e] == y[e] * self.start, zb[e] == y[e] * self.start]
            else:
                cons += self.pbox(u, za[e], y[e]) + self.pbox(u, zb[e], y[e])
                if not hull:
                    obj += cp.norm(zb[e] - za[e], 2)
            if v == t:
                cons += [wa[e] == y[e] * self.goal, wb[e] == y[e] * self.goal]
            else:
                cons += self.pbox(v, wa[e], y[e]) + self.pbox(v, wb[e], y[e])
            cons.append(zb[e] == wa[e])
        cons.append(sum(y[e] for e in E if e[0] == s) == 1)
        cons.append(sum(y[e] for e in E if e[1] == t) == 1)
        R = len(self.boxes)
        for v in range(R):
            I = [e for e in E if e[1] == v]
            O = [e for e in E if e[0] == v]
            yin = sum(y[e] for e in I) if I else 0
            yout = sum(y[e] for e in O) if O else 0
            if I or O:
                cons += [yin == yout]
            if I:
                cons += [yin <= 1]
            if I and O:
                cons += [sum(wa[e] for e in I) == sum(za[e] for e in O),
                         sum(wb[e] for e in I) == sum(zb[e] for e in O)]
            if two_cycle and I:
                for u in range(R):
                    if (u, v) in y and (v, u) in y:
                        slack = yin - y[(u, v)] - y[(v, u)]
                        cons.append(slack >= 0)
                        SA = sum(wa[e] for e in I) - wa[(u, v)] - za[(v, u)]
                        SB = sum(wb[e] for e in I) - wb[(u, v)] - zb[(v, u)]
                        cons += self.pbox(v, SA, slack) + self.pbox(v, SB, slack)
            if hull and I and O:
                P = [(e, f) for e in I for f in O if f != (e[1], e[0])]
                lam = {p: cp.Variable(nonneg=True) for p in P}
                Wa = {p: cp.Variable(d) for p in P}
                Wb = {p: cp.Variable(d) for p in P}
                for p in P:
                    cons += self.pbox(v, Wa[p], lam[p]) + self.pbox(v, Wb[p], lam[p])
                    obj += cp.norm(Wb[p] - Wa[p], 2)
                for e in I:
                    Pe = [p for p in P if p[0] == e]
                    cons += [sum(lam[p] for p in Pe) == y[e], sum(Wa[p] for p in Pe) == wa[e],
                             sum(Wb[p] for p in Pe) == wb[e]] if Pe else [y[e] == 0]
                for f in O:
                    Pf = [p for p in P if p[1] == f]
                    cons += [sum(lam[p] for p in Pf) == y[f], sum(Wa[p] for p in Pf) == za[f],
                             sum(Wb[p] for p in Pf) == zb[f]] if Pf else [y[f] == 0]
        prob = cp.Problem(cp.Minimize(obj), cons)
        prob.solve(solver=SOLVER)
        if return_y:
            return prob.value, {e: float(y[e].value) for e in E}
        return prob.value

    def paths(self, maxn=20000):
        out = {}
        for u, v in self.E:
            out.setdefault(u, []).append(v)
        res = []

        def dfs(v, path):
            if len(res) >= maxn:
                return
            if v == self.t:
                res.append(list(path))
                return
            for w in out.get(v, []):
                if w not in path:
                    path.append(w)
                    dfs(w, path)
                    path.pop()

        dfs(self.s, [self.s])
        return res

    def path_cost(self, p):
        regs = p[1:-1]
        P = [self.start] + [cp.Variable(self.d) for _ in range(len(regs) - 1)] + [self.goal]
        cons, obj = [], 0
        for k, r in enumerate(regs):
            lo, hi = self.boxes[r]
            for X in (P[k], P[k + 1]):
                if isinstance(X, cp.Variable):
                    cons += [X >= lo, X <= hi]
            obj += cp.norm(P[k + 1] - P[k], 2)
        prob = cp.Problem(cp.Minimize(obj), cons)
        prob.solve(solver=SOLVER)
        return prob.value

    def exact(self):
        return min(self.path_cost(p) for p in self.paths())


def door_gcs(m: Region):
    """Door (line-graph) GCS: vertices start, goal and doors X_u cap X_v (u<v)."""
    R = len(m.boxes)
    sets = {"s": point(m.start), "t": point(m.goal)}
    member = {"s": {i for i in range(R) if inbox(m.start, m.boxes[i])},
              "t": {i for i in range(R) if inbox(m.goal, m.boxes[i])}}
    for u in range(R):
        for v in range(u + 1, R):
            lo = np.maximum(m.boxes[u][0], m.boxes[v][0])
            hi = np.minimum(m.boxes[u][1], m.boxes[v][1])
            if np.all(lo <= hi + 1e-12):
                name = f"D{u}_{v}"
                sets[name] = box(lo, hi)
                member[name] = {u, v}
    names = list(sets)
    E = [(a, b) for a in names for b in names if a != b and a != "t" and b != "s" and member[a] & member[b]]
    return GCS(sets, E, "s", "t", L2)


def ring_wall(H, eps=0.0):
    """Free space = [-2,2] x [-H-1,H+1] minus the wall [-1,1] x [-H,H]; four boxes."""
    boxes = [([-2, -H - 1], [-1, H + 1]), ([1, -H - 1], [2, H + 1]),
             ([-2, H], [2, H + 1]), ([-2, -H - 1], [2, -H + eps])]
    return Region(boxes, [-1.5, 0.0], [1.5, 0.0])
