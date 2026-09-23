"""Root-bound impact of single-pool single-output substructure hulls on pooling instances.

Relaxations (all contain the pq McCormick LP "PQ"):
  pq    : PQ alone.
  L1    : PQ + exact hull of the Luedtke et al. (2020) aggregated set for every
          (pool l, output j, attribute k), attributes = upper and lower specs.
  Abox  : PQ + exact hull of the aggregated multi-attribute set T^K for every (l, j),
          with the same interval data as L1 (only the shared x, z couple attributes).
  Apoly : as Abox, but pool and bypass quality sets are the polytopes spanned by
          the input quality vectors (attribute correlation kept).
  D1    : as D but one attribute per block (disaggregated single-attribute sets).
  D     : PQ + exact hull of the disaggregated single-pool single-output set
          {(x, q, w, v): w = x q, q in simplex, v >= 0, specs, capacities}.
Hull constraints are imposed by Dantzig-Wolfe column generation. Pricing is solved
globally by Gurobi (NonConvex=2), so the Lagrangian bound
  master + sum_b min(0, min reduced cost_b)
is a valid lower bound for the relaxation; the final master value is an upper
estimate (inner approximation of the hulls).
"""
import json, sys, time, itertools
from collections import defaultdict
import numpy as np
import gurobipy as gp
from gurobipy import GRB

ENV = gp.Env(params={"OutputFlag": 0, "Threads": 1})
INF = float("inf")


def cap(v):
    return INF if v is None else float(v)


class Inst:
    def __init__(self, path):
        d = json.load(open(path))
        self.name = d["name"]; self.opt = d.get("objective")
        self.I = {c["name"]: c for c in d["components"]}
        self.J = {p["name"]: p for p in d["products"]}
        self.L = dict(d["pool_size"])
        self.IL = {(a["component"], a["pool"]): a["fraction"] for a in d["component_to_pool_fraction"] if a["fraction"] is not None}
        self.LJ = {(a["pool"], a["product"]): a["bound"] for a in d["pool_to_product_bound"] if a["bound"] is not None}
        self.IJ = {(a["component"], a["product"]): a["bound"] for a in d.get("component_to_product_bound", []) if a["bound"] is not None}
        self.cIL = {(a["component"], a["pool"]): a.get("cost", 0.0) or 0.0 for a in d["component_to_pool_fraction"]}
        self.cLJ = {(a["pool"], a["product"]): a.get("cost", 0.0) or 0.0 for a in d["pool_to_product_bound"]}
        self.cIJ = {(a["component"], a["product"]): a.get("cost", 0.0) or 0.0 for a in d.get("component_to_product_bound", [])}
        self.inl = defaultdict(list)
        for (i, l) in self.IL: self.inl[l].append(i)
        self.K = list(next(iter(self.I.values()))["quality"].keys())
        # attributes per output: (k, sign) with excess gamma_ijk <= 0 required
        self.attrs = {}
        for j, p in self.J.items():
            at = []
            for k in self.K:
                if p["quality_upper"] is not None and p["quality_upper"].get(k) is not None:
                    at.append((k, "U"))
                if p["quality_lower"] is not None and p["quality_lower"].get(k) is not None:
                    at.append((k, "L"))
            self.attrs[j] = at

    def gamma(self, i, j, a):
        k, s = a
        qv = self.I[i]["quality"][k]
        return qv - self.J[j]["quality_upper"][k] if s == "U" else self.J[j]["quality_lower"][k] - qv

    def ybound(self, l, j):
        return min(cap(self.LJ[(l, j)]), cap(self.L[l]), cap(self.J[j]["upper"]),
                   sum(cap(self.I[i]["upper"]) for i in self.inl[l]))


def build_pq(P):
    m = gp.Model(env=ENV)
    q = {(i, l): m.addVar(lb=0, ub=P.IL[(i, l)]) for (i, l) in P.IL}
    y = {(l, j): m.addVar(lb=0, ub=P.ybound(l, j)) for (l, j) in P.LJ}
    z = {(i, j): m.addVar(lb=0, ub=min(cap(P.IJ[(i, j)]), cap(P.I[i]["upper"]), cap(P.J[j]["upper"]))) for (i, j) in P.IJ}
    v = {}
    for (l, j) in P.LJ:
        for i in P.inl[l]:
            v[i, l, j] = m.addVar(lb=0)
            yu, qu = P.ybound(l, j), P.IL[(i, l)]
            m.addConstr(v[i, l, j] <= yu * q[i, l]); m.addConstr(v[i, l, j] <= qu * y[l, j])
            m.addConstr(v[i, l, j] >= yu * q[i, l] + qu * y[l, j] - yu * qu)
    for l in P.L:
        m.addConstr(gp.quicksum(q[i, l] for i in P.inl[l]) == 1)
        m.addConstr(gp.quicksum(v[i, l2, j] for (i, l2, j) in v if l2 == l) <= P.L[l])
        for i in P.inl[l]:
            m.addConstr(gp.quicksum(v[i, l, j] for (l2, j) in P.LJ if l2 == l) <= P.L[l] * q[i, l])
    for (l, j) in P.LJ:
        m.addConstr(gp.quicksum(v[i, l, j] for i in P.inl[l]) == y[l, j])
    outflow = {i: gp.quicksum(v[a] for a in v if a[0] == i) + gp.quicksum(z[a] for a in z if a[0] == i) for i in P.I}
    inflow = {j: gp.quicksum(v[a] for a in v if a[2] == j) + gp.quicksum(z[a] for a in z if a[1] == j) for j in P.J}
    for i, c in P.I.items():
        if c["upper"] is not None: m.addConstr(outflow[i] <= c["upper"])
        if c["lower"]: m.addConstr(outflow[i] >= c["lower"])
    for j, p in P.J.items():
        if p["upper"] is not None: m.addConstr(inflow[j] <= p["upper"])
        if p["lower"]: m.addConstr(inflow[j] >= p["lower"])
        for a in P.attrs[j]:
            m.addConstr(gp.quicksum(P.gamma(i, j, a) * v[i, l, j2] for (i, l, j2) in v if j2 == j)
                        + gp.quicksum(P.gamma(i, j, a) * z[i, j2] for (i, j2) in z if j2 == j) <= 0)
    cpath = getattr(P, "cpath", None)
    pc = (lambda i, l, j: cpath[i, l, j]) if cpath else (lambda i, l, j: P.I[i]["price"] - P.J[j]["price"] + P.cIL[i, l] + P.cLJ[l, j])
    m.setObjective(gp.quicksum(pc(i, l, j) * v[i, l, j] for (i, l, j) in v)
                   + gp.quicksum((P.I[i]["price"] - P.J[j]["price"] + P.cIJ[i, j]) * z[i, j] for (i, j) in z), GRB.MINIMIZE)
    m.update()
    return m, q, y, z, v


class Block:
    """Local set for (pool l, output j); mode in L1 (with attribute index), Abox, Apoly, D."""

    def __init__(self, P, vars_, l, j, mode, attr=None, link=True):
        m, q, y, z, v = vars_
        self.P, self.l, self.j, self.mode = P, l, j, mode
        IL = P.inl[l]
        byp = sorted({i for (i, j2) in P.IJ if j2 == j} | {i for (i, l2, j2) in v if j2 == j and l2 != l})
        self.ok = len(byp) > 0 or True
        attrs = P.attrs[j] if attr is None else [attr]
        Gm = np.array([[P.gamma(i, j, a) for a in attrs] for i in IL])
        Gb = np.array([[P.gamma(i, j, a) for a in attrs] for i in byp]) if byp else np.zeros((0, len(attrs)))
        # linear expressions of master variables
        X = y[l, j]
        Q = [q[i, l] for i in IL]
        W = [v[i, l, j] for i in IL]
        Vb = [(z[i, j] if (i, j) in z else 0) + gp.quicksum(v[i, l2, j] for (i2, l2, j2) in v if i2 == i and j2 == j and l2 != l) for i in byp]
        Zb = gp.quicksum(Vb) if byp else gp.LinExpr(0)
        nA = len(attrs); self.nA = nA; self.Gm = Gm
        T = [gp.quicksum(Gm[a, k] * Q[a] for a in range(len(IL))) for k in range(nA)]
        U = [gp.quicksum(Gm[a, k] * W[a] for a in range(len(IL))) for k in range(nA)]
        Y = [gp.quicksum(Gb[b, k] * Vb[b] for b in range(len(byp))) for k in range(nA)] if byp else [gp.LinExpr(0)] * nA
        if mode in ("D", "D1"):
            self.coords = [X] + Q + W + Vb
        else:
            self.coords = [X, Zb] + U + Y + T
        # pricing model: an LP in which each product P = x*s is replaced by McCormick
        # rows for x in [lo, hi]; exact pricing is a 1-D branch and bound on x.
        pm = gp.Model(env=ENV); pm.Params.Threads = 1; pm.Params.Method = 1
        XU = P.ybound(l, j); Cj = cap(P.J[j]["upper"]); Dj = P.J[j]["lower"] or 0
        self.XU = XU
        x = pm.addVar(lb=0, ub=XU); self.x = x
        zb = pm.addVar(lb=0, ub=Cj if Cj < INF else GRB.INFINITY)
        pm.addConstr(x + zb <= Cj) if Cj < INF else None
        if Dj: pm.addConstr(x + zb >= Dj)
        self.mc = []

        def product(Pv, sv, sl, su):
            c1 = pm.addConstr(Pv - 0 * sv - sl * x >= 0); c2 = pm.addConstr(Pv - XU * sv - su * x >= -XU * su)
            c3 = pm.addConstr(Pv - XU * sv - sl * x <= -XU * sl); c4 = pm.addConstr(Pv - 0 * sv - su * x <= 0)
            self.mc.append((c1, c2, c3, c4, sv, sl, su))
        if mode in ("L1", "Abox"):
            tl, tu = Gm.min(0), Gm.max(0)
            t = pm.addVars(nA, lb=list(tl), ub=list(tu)); u = pm.addVars(nA, lb=-GRB.INFINITY); yy = pm.addVars(nA, lb=-GRB.INFINITY)
            for k in range(nA):
                product(u[k], t[k], tl[k], tu[k])
                if byp:
                    pm.addConstr(yy[k] >= Gb[:, k].min() * zb); pm.addConstr(yy[k] <= Gb[:, k].max() * zb)
                else:
                    pm.addConstr(yy[k] == 0); pm.addConstr(zb == 0)
                pm.addConstr(u[k] + yy[k] <= 0)
            self.pvars = [x, zb] + [u[k] for k in range(nA)] + [yy[k] for k in range(nA)] + [t[k] for k in range(nA)]
        else:
            qu = [P.IL[(i, l)] for i in IL]
            qq = pm.addVars(len(IL), lb=0, ub=qu); w = pm.addVars(len(IL), lb=0)
            vb = pm.addVars(len(byp), lb=0)
            pm.addConstr(qq.sum() == 1); pm.addConstr(vb.sum() == zb)
            if not byp: pm.addConstr(zb == 0)
            for a2 in range(len(IL)): product(w[a2], qq[a2], 0.0, qu[a2])
            pm.addConstr(w.sum() == x)
            for k in range(nA):
                pm.addConstr(gp.quicksum(Gm[a2, k] * w[a2] for a2 in range(len(IL))) + gp.quicksum(Gb[b2, k] * vb[b2] for b2 in range(len(byp))) <= 0)
            if mode in ("D", "D1"):
                self.pvars = [x] + [qq[a2] for a2 in range(len(IL))] + [w[a2] for a2 in range(len(IL))] + [vb[b2] for b2 in range(len(byp))]
            else:
                uu = [gp.quicksum(Gm[a2, k] * w[a2] for a2 in range(len(IL))) for k in range(nA)]
                yv = [gp.quicksum(Gb[b2, k] * vb[b2] for b2 in range(len(byp))) for k in range(nA)]
                tt = [gp.quicksum(Gm[a2, k] * qq[a2] for a2 in range(len(IL))) for k in range(nA)]
                self.pvars = [x, zb] + uu + yv + tt
        pm.update(); self.pm = pm
        # linking rows in master: coord - sum lam p = 0 ; sum lam = 1
        self.cols = []
        if link:
            self.link = [m.addConstr(c == 0) for c in self.coords]  # columns added below change these
            self.conv = m.addConstr(gp.LinExpr() == 1)

    def add_col(self, m, p):
        col = gp.Column([-pi for pi in p] + [1.0], self.link + [self.conv])
        lam = m.addVar(lb=0, column=col)
        self.cols.append(lam)

    def set_interval(self, lo, hi):
        self.x.LB, self.x.UB = lo, hi
        pm = self.pm
        for (c1, c2, c3, c4, sv, sl, su) in self.mc:
            pm.chgCoeff(c1, sv, -lo); c1.RHS = -lo * sl
            pm.chgCoeff(c2, sv, -hi); c2.RHS = -hi * su
            pm.chgCoeff(c3, sv, -hi); c3.RHS = -hi * sl
            pm.chgCoeff(c4, sv, -lo); c4.RHS = -lo * su

    def point(self):
        return [float(gp.LinExpr(e).getValue()) if not isinstance(e, gp.Var) else e.X for e in self.pvars]

    def solve_lp(self, lo, hi):
        self.set_interval(lo, hi); self.pm.optimize()
        if self.pm.Status != GRB.OPTIMAL:
            return INF, None, None
        return self.pm.ObjVal, self.x.X, self.point()

    def minimize(self, c, tol=1e-7, maxnodes=500):
        """Exact min of c.p over the block (1-D spatial B&B on x). Returns (ub, lb, point)."""
        import heapq
        self.pm.setObjective(gp.quicksum(c[r] * self.pvars[r] for r in range(len(c))), GRB.MINIMIZE)
        UB, best = INF, None
        lb0, xs, _ = self.solve_lp(0.0, self.XU)
        heap = [(lb0, 0.0, self.XU, xs)]; n = 0; lost = INF
        while heap and n < maxnodes:
            lb, lo, hi, xs = heapq.heappop(heap); n += 1
            if lb >= UB - tol * max(1.0, abs(UB)):
                heap = []; break
            for xc in {xs, 0.5 * (lo + hi)}:
                v, _, p = self.solve_lp(xc, xc)
                if v < UB: UB, best = v, p
            if hi - lo < 1e-12 * max(1.0, self.XU):
                lost = min(lost, lb); continue
            xm = xs if (xs is not None and lo + 1e-3 * (hi - lo) < xs < hi - 1e-3 * (hi - lo)) else 0.5 * (lo + hi)
            for a, b in ((lo, xm), (xm, hi)):
                v, xa, _ = self.solve_lp(a, b)
                if v < UB - tol * max(1.0, abs(UB)):
                    heapq.heappush(heap, (v, a, b, xa))
        # every pruned node has bound >= UB - tol*max(1,|UB|); open nodes keep their bounds
        LB = min(UB - tol * max(1.0, abs(UB)), lost)
        if heap:
            LB = min(LB, min(h[0] for h in heap))
        return UB, LB, best

    def price(self, m):
        pi = [c.Pi for c in self.link]; mu = self.conv.Pi
        sc = max(1e-12, max(abs(v) for v in pi))  # normalize the pricing objective
        ub, lb, p = self.minimize([v / sc for v in pi])
        return sc * ub - mu, sc * lb - mu, p

    def seed_points(self, m, sol):
        """Zero-flow points at each pool-quality vertex, and the projection of a feasible solution."""
        IL = self.P.inl[self.l]
        if all(self.P.IL[(i, self.l)] >= 1.0 for i in IL):
            nA = self.nA
            for a in range(len(IL)):
                if self.mode in ("D", "D1"):
                    p = [0.0] + [1.0 if b == a else 0.0 for b in range(len(IL))] + [0.0] * (len(self.coords) - 1 - len(IL))
                else:
                    p = [0.0, 0.0] + [0.0] * (2 * nA) + [float(self.Gm[a, k]) for k in range(nA)]
                self.add_col(m, p)
        if sol is not None:
            self.add_col(m, [eval_expr(c, sol) for c in self.coords])

    def seed(self, m, npts=5):
        rng = np.random.default_rng(0)
        for _ in range(npts):
            ub, lb, p = self.minimize(rng.normal(size=len(self.pvars)))
            if p is not None:
                self.add_col(m, p)


def eval_expr(e, vals):
    if isinstance(e, (int, float)):
        return float(e)
    if isinstance(e, gp.Var):
        return vals[e.index]
    e = gp.LinExpr(e)
    return e.getConstant() + sum(e.getCoeff(k) * vals[e.getVar(k).index] for k in range(e.size()))


def feasible_solution(P, tlim=60):
    """A feasible pooling solution (Gurobi on the nonconvex pq model), as master-variable values by index."""
    m, q, y, z, v = build_pq(P)
    for (i, l, j), var in v.items():
        m.addQConstr(var == q[i, l] * y[l, j])
    m.Params.NonConvex = 2; m.Params.TimeLimit = tlim
    m.optimize()
    if not m.SolCount:
        return None
    return [var.X for var in m.getVars()]


def solve_relax(P, mode, maxit=300, tlim=3600, M=1e4, log=True, rtol=1e-4, extra=None):
    vars_ = build_pq(P); m = vars_[0]
    m.optimize(); zpq = m.ObjVal
    if mode == "pq":
        return dict(mode=mode, lb=zpq, ub=zpq, it=0, blocks=0, time=0)
    t0 = time.time()
    blocks = []
    for (l, j) in P.LJ:
        if mode in ("L1", "D1"):
            for a in P.attrs[j]:
                blocks.append(Block(P, vars_, l, j, mode, a))
        else:
            blocks.append(Block(P, vars_, l, j, mode))
    # penalty slacks on linking rows (phase-1 style, keeps master feasible)
    sol = feasible_solution(P)
    for b in blocks:
        for r in b.link:
            m.addVar(lb=0, obj=M, column=gp.Column([1.0], [r])); m.addVar(lb=0, obj=M, column=gp.Column([-1.0], [r]))
        b.seed(m)
        b.seed_points(m, sol)
    if extra is not None:
        for b, pts in zip(blocks, extra):
            for p in pts:
                b.add_col(m, p)
    best_lb = -INF; it = 0
    while it < maxit and time.time() - t0 < tlim:
        it += 1
        m.optimize(); zm = m.ObjVal
        lag = zm; nadd = 0
        for b in blocks:
            rc, rcb, p = b.price(m)
            lag += min(0.0, rcb)
            if rc < -1e-6 * max(1.0, abs(zm)):
                b.add_col(m, p); nadd += 1
        best_lb = max(best_lb, lag)
        if log:
            print(f"  [{mode}] it {it} master {zm:.6f} lagr {lag:.6f} cols+ {nadd}", flush=True)
        if nadd == 0 or zm - best_lb <= rtol * max(1.0, abs(zm)):
            break
    m.optimize()
    slack = sum(abs(vv.X) for vv in m.getVars() if vv.Obj == M)
    return dict(mode=mode, lb=best_lb, ub=m.ObjVal, it=it, blocks=len(blocks), time=time.time() - t0, slack=slack, zpq=zpq)


if __name__ == "__main__":
    path = sys.argv[1]; modes = sys.argv[2].split(",") if len(sys.argv) > 2 else ["pq", "L1", "D1", "Abox", "Apoly", "D"]
    if path.endswith(".osil"):
        import spp
        P = spp.SppInst(path)
    else:
        P = Inst(path)
    res = {"name": P.name, "opt": P.opt, "K": len(P.K), "L": len(P.L), "J": len(P.J), "I": len(P.I)}
    for mode in modes:
        r = solve_relax(P, mode, log="-q" not in sys.argv)
        res[mode] = r
        print(json.dumps({"name": P.name, **r}), flush=True)
    print("RESULT", json.dumps(res), flush=True)
