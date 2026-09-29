"""Order-1 motion-planning GCS (polygonal paths through overlapping boxes).
Vertex v = box region; vertex variable x_v = (a_v, b_v) (segment inside the box);
edge (u,v) for every overlapping pair, edge constraint b_u = a_v, edge cost ||b_u - a_u||
(u's segment charged on its out-edge copy). s and t are point regions.
Relaxation = perspective formulation of Marcucci et al. SIOPT 2024 eq. (5.5).
"""
import itertools
import numpy as np
import cvxpy as cp

SOLVER = "CLARABEL"


def overlap(B1, B2):
    return np.all(np.maximum(B1[0], B2[0]) <= np.minimum(B1[1], B2[1]) + 1e-12)


class MP:
    def __init__(self, boxes, start, goal, two_cycle=False):
        self.boxes = [(np.asarray(lo, float), np.asarray(hi, float)) for lo, hi in boxes]
        self.start, self.goal = np.asarray(start, float), np.asarray(goal, float)
        self.d = len(start)
        R = len(self.boxes)
        self.s, self.t = R, R + 1
        E = [(i, j) for i in range(R) for j in range(R) if i != j and overlap(self.boxes[i], self.boxes[j])]
        inb = lambda p, B: np.all(p >= B[0] - 1e-12) and np.all(p <= B[1] + 1e-12)
        E += [(self.s, i) for i in range(R) if inb(self.start, self.boxes[i])]
        E += [(i, self.t) for i in range(R) if inb(self.goal, self.boxes[i])]
        self.E = E
        self.two_cycle = two_cycle

    def persp_box(self, i, w, y):
        lo, hi = self.boxes[i]
        return [w >= y * lo, w <= y * hi]

    def relax(self):
        d, E, s, t = self.d, self.E, self.s, self.t
        y = {e: cp.Variable(nonneg=True) for e in E}
        # copies of u's variable (a,b) on out-edge e=(u,v): za[e], zb[e]
        za = {e: cp.Variable(d) for e in E}
        zb = {e: cp.Variable(d) for e in E}
        # copies of v's variable on in-edge e=(u,v): wa[e], wb[e]
        wa = {e: cp.Variable(d) for e in E}
        wb = {e: cp.Variable(d) for e in E}
        cons, obj = [], 0
        for e in E:
            u, v = e
            if u == s:
                cons += [za[e] == y[e] * self.start, zb[e] == y[e] * self.start]
            else:
                cons += self.persp_box(u, za[e], y[e]) + self.persp_box(u, zb[e], y[e])
                obj += cp.norm(zb[e] - za[e], 2)
            if v == t:
                cons += [wa[e] == y[e] * self.goal, wb[e] == y[e] * self.goal]
            else:
                cons += self.persp_box(v, wa[e], y[e]) + self.persp_box(v, wb[e], y[e])
            cons.append(zb[e] == wa[e])  # continuity b_u = a_v (perspective of linear eq.)
        V = range(len(self.boxes))
        cons.append(sum(y[e] for e in E if e[0] == s) == 1)
        cons.append(sum(y[e] for e in E if e[1] == t) == 1)
        for v in V:
            I = [e for e in E if e[1] == v]
            O = [e for e in E if e[0] == v]
            yin = sum(y[e] for e in I) if I else 0
            yout = sum(y[e] for e in O) if O else 0
            cons += [yin == yout, yin <= 1]
            if I and O:
                cons.append(sum(wa[e] for e in I) == sum(za[e] for e in O))
                cons.append(sum(wb[e] for e in I) == sum(zb[e] for e in O))
            if self.two_cycle:
                for u in V:
                    if (u, v) in y and (v, u) in y:
                        # linear two-cycle cut y_uv + y_vu <= y_v and its Lemma-5.4 lift
                        slack = yin - y[(u, v)] - y[(v, u)]
                        cons.append(slack >= 0)
                        if I:
                            SA = sum(wa[e] for e in I) - wa[(u, v)] - za[(v, u)]
                            SB = sum(wb[e] for e in I) - wb[(u, v)] - zb[(v, u)]
                            cons += self.persp_box(v, SA, slack) + self.persp_box(v, SB, slack)
        prob = cp.Problem(cp.Minimize(obj), cons)
        prob.solve(solver=SOLVER)
        return prob.value, {e: float(y[e].value) for e in E}

    def paths(self, maxlen=None):
        out = {}
        for u, v in self.E:
            out.setdefault(u, []).append(v)
        res = []

        def dfs(v, path):
            if v == self.t:
                res.append(list(path))
                return
            if maxlen and len(path) > maxlen:
                return
            for w in out.get(v, []):
                if w not in path:
                    path.append(w)
                    dfs(w, path)
                    path.pop()

        dfs(self.s, [self.s])
        return res

    def path_cost(self, p):
        # region k carries the segment P[k] -> P[k+1]; interior P's are door points
        regs = p[1:-1]
        d = self.d
        cons = []
        P = [self.start] + [cp.Variable(d) for _ in range(len(regs) - 1)] + [self.goal]
        obj = 0
        for k, r in enumerate(regs):
            A, B = P[k], P[k + 1]
            lo, hi = self.boxes[r]
            for X in (A, B):
                if isinstance(X, cp.Variable):
                    cons += [X >= lo, X <= hi]
            obj += cp.norm(B - A, 2)
        prob = cp.Problem(cp.Minimize(obj), cons)
        prob.solve(solver=SOLVER)
        return prob.value

    def exact(self, maxlen=None):
        best = np.inf
        for p in self.paths(maxlen):
            best = min(best, self.path_cost(p))
        return best


def relax_hull(m, pair_cost=True, forbid_backtrack=True):
    """Vertex-hull strengthening for the MP-GCS: pair variables (lambda_ef, W_ef) per
    (in-edge e, out-edge f) at each region v, with W_ef in lambda_ef * X_v^2.
    forbid_backtrack drops pairs with f = reverse(e) (immediate return u->v->u).
    pair_cost charges v's segment length per pair (Jensen-stronger than per out-edge)."""
    d, E, s, t = m.d, m.E, m.s, m.t
    y = {e: cp.Variable(nonneg=True) for e in E}
    za = {e: cp.Variable(d) for e in E}; zb = {e: cp.Variable(d) for e in E}
    wa = {e: cp.Variable(d) for e in E}; wb = {e: cp.Variable(d) for e in E}
    cons, obj = [], 0
    for e in E:
        u, v = e
        if u == s:
            cons += [za[e] == y[e] * m.start, zb[e] == y[e] * m.start]
        else:
            cons += m.persp_box(u, za[e], y[e]) + m.persp_box(u, zb[e], y[e])
            if not pair_cost:
                obj += cp.norm(zb[e] - za[e], 2)
        if v == t:
            cons += [wa[e] == y[e] * m.goal, wb[e] == y[e] * m.goal]
        else:
            cons += m.persp_box(v, wa[e], y[e]) + m.persp_box(v, wb[e], y[e])
        cons.append(zb[e] == wa[e])
    cons.append(sum(y[e] for e in E if e[0] == s) == 1)
    cons.append(sum(y[e] for e in E if e[1] == t) == 1)
    for v in range(len(m.boxes)):
        I = [e for e in E if e[1] == v]; O = [e for e in E if e[0] == v]
        yin = sum(y[e] for e in I) if I else 0
        yout = sum(y[e] for e in O) if O else 0
        cons += [yin == yout, yin <= 1]
        if not (I and O):
            continue
        P = [(e, f) for e in I for f in O if not (forbid_backtrack and f == (e[1], e[0]))]
        lam = {p: cp.Variable(nonneg=True) for p in P}
        Wa = {p: cp.Variable(d) for p in P}; Wb = {p: cp.Variable(d) for p in P}
        for p in P:
            cons += m.persp_box(v, Wa[p], lam[p]) + m.persp_box(v, Wb[p], lam[p])
            if pair_cost:
                obj += cp.norm(Wb[p] - Wa[p], 2)
        for e in I:
            Pe = [p for p in P if p[0] == e]
            cons += [sum(lam[p] for p in Pe) == y[e] if Pe else y[e] == 0]
            if Pe:
                cons += [sum(Wa[p] for p in Pe) == wa[e], sum(Wb[p] for p in Pe) == wb[e]]
        for f in O:
            Pf = [p for p in P if p[1] == f]
            cons += [sum(lam[p] for p in Pf) == y[f] if Pf else y[f] == 0]
            if Pf:
                cons += [sum(Wa[p] for p in Pf) == za[f], sum(Wb[p] for p in Pf) == zb[f]]
    prob = cp.Problem(cp.Minimize(obj), cons)
    prob.solve(solver=SOLVER)
    return prob.value, {e: float(y[e].value) for e in E}
