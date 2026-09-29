"""Small toolkit for a-priori integrality-gap checks of GCS shortest-path relaxations.

Notation follows research-20260928b/gcs/a-priori-gap-bounds.md.

* Sets: point, ball, box, poly (A x <= b, optional vertex list V).
* Costs: 'l2', 'sq', 'l1', 'aff', 'asym' (1D a*w^+ + b*w^-), 'zero', 'socsum'.
* relax(g, hull, degree): REL (Marcucci et al. SIOPT 2024, (5.5)) or REL_H (vertex hull,
  pair variables lambda_ef, w_ef).  Optional edge constraints in perspective form.
* opt(g): exact value by enumerating simple s-t paths and solving convex restrictions.
* Rounding from a REL_H point: closed-form expectation of the Markov-chain rounding,
  pair-graph shortest path (deterministic), Jensen bound sum_e y_e cav_e (LP over vertices).
"""
import itertools
import heapq
import numpy as np
import cvxpy as cp

SOLVER = "CLARABEL"
TOL = 1e-7


# ----------------------------------------------------------------------------- sets
class Set:
    def __init__(self, kind, **kw):
        self.kind = kind
        self.__dict__.update(kw)
        if kind == "point":
            self.c = np.atleast_1d(np.asarray(self.c, float))
            self.dim = len(self.c)
        elif kind == "ball":
            self.c = np.atleast_1d(np.asarray(self.c, float))
            self.dim = len(self.c)
        elif kind == "box":
            self.lo = np.atleast_1d(np.asarray(self.lo, float))
            self.hi = np.atleast_1d(np.asarray(self.hi, float))
            self.dim = len(self.lo)
        elif kind == "poly":
            self.A = np.asarray(self.A, float)
            self.b = np.asarray(self.b, float)
            self.dim = self.A.shape[1]
            if getattr(self, "V", None) is not None:
                self.V = np.asarray(self.V, float)
        else:
            raise ValueError(kind)

    def persp(self, z, y):
        k = self.kind
        if k == "point":
            return [z == y * self.c]
        if k == "ball":
            return [cp.norm(z - y * self.c, 2) <= self.r * y]
        if k == "box":
            return [z >= y * self.lo, z <= y * self.hi]
        return [self.A @ z <= y * self.b]

    def vertices(self):
        k = self.kind
        if k == "point":
            return self.c[None, :]
        if k == "box":
            return np.array(list(itertools.product(*zip(self.lo, self.hi))), float)
        if k == "poly":
            return getattr(self, "V", None)
        return None

    def circ(self):
        """An enclosing ball (center, radius)."""
        k = self.kind
        if k == "point":
            return self.c, 0.0
        if k == "ball":
            return self.c, float(self.r)
        if k == "box":
            return (self.lo + self.hi) / 2, float(np.linalg.norm(self.hi - self.lo) / 2)
        V = self.vertices()
        c = V.mean(0)
        return c, float(np.max(np.linalg.norm(V - c, axis=1)))

    def project(self, x):
        x = np.asarray(x, float)
        k = self.kind
        if k == "point":
            return self.c.copy()
        if k == "ball":
            d = x - self.c
            n = np.linalg.norm(d)
            return x if n <= self.r else self.c + d * (self.r / n)
        if k == "box":
            return np.clip(x, self.lo, self.hi)
        if np.all(self.A @ x <= self.b + 1e-9):
            return x
        p = cp.Variable(self.dim)
        cp.Problem(cp.Minimize(cp.sum_squares(p - x)), [self.A @ p <= self.b]).solve(solver=SOLVER)
        return p.value


def point(c):
    return Set("point", c=c)


def ball(c, r):
    return Set("ball", c=c, r=r)


def box(lo, hi):
    return Set("box", lo=lo, hi=hi)


def poly_from_vertices2d(P):
    """Convex polygon in 2D = convex hull of the given points; returns poly with A, b, V."""
    P = np.asarray(P, float)
    if len(P) > 3:
        from scipy.spatial import ConvexHull
        P = P[ConvexHull(P).vertices]
    cen = P.mean(0)
    ang = np.arctan2(P[:, 1] - cen[1], P[:, 0] - cen[0])
    P = P[np.argsort(ang)]
    A, b = [], []
    for q in range(len(P)):
        p1, p2 = P[q], P[(q + 1) % len(P)]
        nrm = np.array([p2[1] - p1[1], -(p2[0] - p1[0])])
        if nrm @ (cen - p1) > 0:
            nrm = -nrm
        A.append(nrm)
        b.append(nrm @ p1)
    return Set("poly", A=np.array(A), b=np.array(b), V=P)


# ----------------------------------------------------------------------------- costs
class Cost:
    def __init__(self, kind, **kw):
        self.kind = kind
        self.__dict__.update(kw)

    def persp(self, z, zp, y):
        k = self.kind
        if k == "l2":
            return cp.norm(zp - z, 2)
        if k == "sq":
            return cp.quad_over_lin(zp - z, y)
        if k == "l1":
            return cp.norm1(zp - z)
        if k == "aff":
            return self.c @ z + self.d @ zp + self.b0 * y
        if k == "asym":
            w = cp.sum(zp - z)
            return self.a * cp.pos(w) + self.bb * cp.neg(w)
        if k == "zero":
            return 0 * y
        if k == "socsum":
            zz = cp.hstack([z, zp])
            return sum(cp.norm(A @ zz + bvec * y, 2) for A, bvec in self.terms)
        raise ValueError(k)

    def val(self, x, xp):
        x, xp = np.atleast_1d(np.asarray(x, float)), np.atleast_1d(np.asarray(xp, float))
        k = self.kind
        if k == "l2":
            return float(np.linalg.norm(xp - x))
        if k == "sq":
            return float(np.sum((xp - x) ** 2))
        if k == "l1":
            return float(np.sum(np.abs(xp - x)))
        if k == "aff":
            return float(self.c @ x + self.d @ xp + self.b0)
        if k == "asym":
            w = float(np.sum(xp - x))
            return self.a * max(w, 0) + self.bb * max(-w, 0)
        if k == "zero":
            return 0.0
        if k == "socsum":
            xx = np.r_[x, xp]
            return float(sum(np.linalg.norm(A @ xx + bvec) for A, bvec in self.terms))
        raise ValueError(k)

    def expr(self, x, xp):
        """cvxpy expression of the cost at y=1 (for convex restrictions / Delta)."""
        return self.persp(x, xp, 1.0)


L2, SQ, L1 = Cost("l2"), Cost("sq"), Cost("l1")


# ----------------------------------------------------------------------------- graph
class GCS:
    def __init__(self, sets, edges, s, t, cost, econs=None):
        self.sets = sets
        self.edges = list(edges)
        self.s, self.t = s, t
        self.cost = cost if isinstance(cost, dict) else {e: cost for e in self.edges}
        self.econs = econs or {}
        self.V = list(sets)
        self.inn = {v: [e for e in self.edges if e[1] == v] for v in self.V}
        self.out = {v: [e for e in self.edges if e[0] == v] for v in self.V}

    def is_dag(self):
        indeg = {v: len(self.inn[v]) for v in self.V}
        q = [v for v in self.V if indeg[v] == 0]
        seen = 0
        while q:
            v = q.pop()
            seen += 1
            for (_, w) in self.out[v]:
                indeg[w] -= 1
                if indeg[w] == 0:
                    q.append(w)
        return seen == len(self.V)


def relax(g, hull=False, degree=True, return_sol=False, solver=SOLVER, extra=None):
    """REL (hull=False) or REL_H (hull=True).  extra(g, vars) -> list of constraints."""
    y = {e: cp.Variable(nonneg=True) for e in g.edges}
    z = {e: cp.Variable(g.sets[e[0]].dim) for e in g.edges}
    zp = {e: cp.Variable(g.sets[e[1]].dim) for e in g.edges}
    cons = []
    for e in g.edges:
        u, v = e
        cons += g.sets[u].persp(z[e], y[e]) + g.sets[v].persp(zp[e], y[e])
        if e in g.econs:
            cons += g.econs[e](z[e], zp[e], y[e])
    s, t = g.s, g.t
    cons.append(sum(y[e] for e in g.out[s]) == 1)
    cons.append(sum(y[e] for e in g.inn[t]) == 1)
    pair = {}
    for v in g.V:
        if v in (s, t):
            continue
        I, O = g.inn[v], g.out[v]
        if not I and not O:
            continue
        yin = sum(y[e] for e in I) if I else 0
        yout = sum(y[e] for e in O) if O else 0
        cons.append(yin == yout)
        if degree and I:
            cons.append(yin <= 1)
        n = g.sets[v].dim
        zin = sum(zp[e] for e in I) if I else np.zeros(n)
        zout = sum(z[e] for e in O) if O else np.zeros(n)
        cons.append(zin == zout)
        if hull and I and O:
            for e in I:
                for f in O:
                    lam, w = cp.Variable(nonneg=True), cp.Variable(n)
                    pair[(e, f)] = (lam, w)
                    cons += g.sets[v].persp(w, lam)
            for e in I:
                cons += [sum(pair[(e, f)][0] for f in O) == y[e], sum(pair[(e, f)][1] for f in O) == zp[e]]
            for f in O:
                cons += [sum(pair[(e, f)][0] for e in I) == y[f], sum(pair[(e, f)][1] for e in I) == z[f]]
    if extra is not None:
        cons += extra(g, dict(y=y, z=z, zp=zp, pair=pair))
    terms = []
    for e in g.edges:
        if g.cost[e].kind == "sq":
            # explicit rotated-cone epigraph |zp - z|^2 <= t_e y_e  (Clarabel can falsely report
            # infeasibility on cvxpy's quad_over_lin perspective; see reviews/gcs-review.md §7)
            te = cp.Variable(nonneg=True)
            cons.append(cp.SOC(te + y[e], cp.hstack([2 * (zp[e] - z[e]), te - y[e]])))
            terms.append(te)
        else:
            terms.append(g.cost[e].persp(z[e], zp[e], y[e]))
    obj = sum(terms)
    prob = cp.Problem(cp.Minimize(obj), cons)
    prob.solve(solver=solver)
    if prob.status not in ("optimal", "optimal_inaccurate"):
        if not return_sol:
            return np.inf if prob.status == "infeasible" else np.nan
        return (np.inf if prob.status == "infeasible" else np.nan), None
    val = prob.value
    if not np.isfinite(val):  # objective re-evaluation can divide by y_e = 0 (quad_over_lin)
        val = prob.solution.opt_val
    if not return_sol:
        return val
    sol = dict(
        y={e: float(y[e].value) for e in g.edges},
        z={e: np.array(z[e].value, float) for e in g.edges},
        zp={e: np.array(zp[e].value, float) for e in g.edges},
        pair={k: (float(l.value), np.array(w.value, float)) for k, (l, w) in pair.items()},
        status=prob.status,
    )
    return val, sol


# ----------------------------------------------------------------------------- exact
def all_paths(g, limit=None):
    res = []

    def dfs(v, path):
        if limit and len(res) >= limit:
            return
        if v == g.t:
            res.append(list(path))
            return
        for (_, w) in g.out[v]:
            if w not in path:
                path.append(w)
                dfs(w, path)
                path.pop()

    dfs(g.s, [g.s])
    return res


def path_cost(g, path, return_x=False):
    x = {v: cp.Variable(g.sets[v].dim) for v in path}
    cons = []
    for v in path:
        cons += g.sets[v].persp(x[v], 1.0)
    obj = 0
    for a, b in zip(path, path[1:]):
        e = (a, b)
        obj = obj + g.cost[e].expr(x[a], x[b])
        if e in g.econs:
            cons += g.econs[e](x[a], x[b], 1.0)
    prob = cp.Problem(cp.Minimize(obj), cons)
    prob.solve(solver=SOLVER)
    val = prob.value if prob.status in ("optimal", "optimal_inaccurate") else np.inf
    if return_x:
        return val, ({v: np.array(x[v].value, float) for v in path} if np.isfinite(val) else None)
    return val


def opt(g, return_path=False, limit=None):
    best, bp = np.inf, None
    for p in all_paths(g, limit):
        c = path_cost(g, p)
        if c < best:
            best, bp = c, p
    return (best, bp) if return_path else best


# ----------------------------------------------------------------------------- rounding
def _bar(w, lam, S):
    return S.project(w / lam)


def tail_head_states(g, sol, tol=TOL):
    """For each edge e with y_e>tol: list of (prob, tail position, tail-state key) and
    (prob, head position, head-state key); keys are pair keys or ('S',e)/('T',e)."""
    y, z, zp, pair = sol["y"], sol["z"], sol["zp"], sol["pair"]
    out = {}
    for e in g.edges:
        if y[e] <= tol:
            continue
        u, v = e
        if u == g.s:
            tails = [(1.0, g.sets[u].project(z[e] / y[e]), ("S", e))]
        else:
            tails = [(pair[(d, e)][0], _bar(pair[(d, e)][1], pair[(d, e)][0], g.sets[u]), (d, e))
                     for d in g.inn[u] if (d, e) in pair and pair[(d, e)][0] > tol]
        if v == g.t:
            heads = [(1.0, g.sets[v].project(zp[e] / y[e]), ("T", e))]
        else:
            heads = [(pair[(e, f)][0], _bar(pair[(e, f)][1], pair[(e, f)][0], g.sets[v]), (e, f))
                     for f in g.out[v] if (e, f) in pair and pair[(e, f)][0] > tol]
        st = sum(p for p, _, _ in tails)
        sh = sum(p for p, _, _ in heads)
        out[e] = ([(p / st, x, k) for p, x, k in tails], [(p / sh, x, k) for p, x, k in heads])
    return out


def expected_round(g, sol, tol=TOL):
    """Closed-form expected cost of the Markov-chain rounding (walk cost in cyclic graphs;
    edges never reached by the chain are not charged: see note)."""
    th = tail_head_states(g, sol, tol)
    E = 0.0
    for e, (tails, heads) in th.items():
        c = g.cost[e]
        E += sol["y"][e] * sum(pt * ph * c.val(xt, xh) for pt, xt, _ in tails for ph, xh, _ in heads)
    return E


def pair_graph_path(g, sol, tol=TOL):
    """Shortest path in the pair (second-order line) graph.  Returns (cost, vertex walk,
    positions list).  Uses Bellman-Ford (costs may be negative; graph acyclic) or Dijkstra."""
    th = tail_head_states(g, sol, tol)
    arcs = {}  # node -> list of (node2, cost, edge)
    pos = {}
    for e, (tails, heads) in th.items():
        for _, xt, kt in tails:
            pos[kt] = xt
            for _, xh, kh in heads:
                pos[kh] = xh
                arcs.setdefault(kt, []).append((kh, g.cost[e].val(xt, xh), e))
    starts = [k for k in pos if k[0] == "S"]
    nodes = list(pos)
    neg = any(c < -1e-12 for L in arcs.values() for _, c, _ in L)
    dist = {k: np.inf for k in nodes}
    prev = {}
    for k in starts:
        dist[k] = 0.0
    if not neg:
        pq = [(0.0, i, k) for i, k in enumerate(starts)]
        heapq.heapify(pq)
        cnt = len(pq)
        while pq:
            d, _, k = heapq.heappop(pq)
            if d > dist[k] + 1e-15:
                continue
            for k2, c, e in arcs.get(k, []):
                if d + c < dist[k2] - 1e-15:
                    dist[k2] = d + c
                    prev[k2] = (k, e)
                    cnt += 1
                    heapq.heappush(pq, (dist[k2], cnt, k2))
    else:
        for _ in range(len(nodes)):
            ch = False
            for k in nodes:
                if not np.isfinite(dist[k]):
                    continue
                for k2, c, e in arcs.get(k, []):
                    if dist[k] + c < dist[k2] - 1e-15:
                        dist[k2] = dist[k] + c
                        prev[k2] = (k, e)
                        ch = True
            if not ch:
                break
    ends = [k for k in nodes if k[0] == "T"]
    kend = min(ends, key=lambda k: dist[k])
    # reconstruct
    seq, k = [kend], kend
    while k in prev:
        k = prev[k][0]
        seq.append(k)
    seq = seq[::-1]
    walk = [g.s]
    xs = [pos[seq[0]]]
    for k in seq[1:]:
        e = k[1] if k[0] == "T" else k[0]
        walk.append(e[1])
        xs.append(pos[k])
    return dist[kend], walk, xs


def walk_cost(g, walk, xs):
    return sum(g.cost[(a, b)].val(xa, xb) for a, b, xa, xb in zip(walk, walk[1:], xs, xs[1:]))


def shortcut(walk, xs):
    """Remove closed sub-walks (keep the first visit position)."""
    walk, xs = list(walk), list(xs)
    changed = True
    while changed:
        changed = False
        seen = {}
        for i, v in enumerate(walk):
            if v in seen:
                j0 = seen[v]
                walk = walk[:j0 + 1] + walk[i + 1:]
                xs = xs[:j0 + 1] + xs[i + 1:]
                changed = True
                break
            seen[v] = i
    return walk, xs


# ----------------------------------------------------------------------------- Jensen
def cav_lp(g, e, a, b):
    """Concave envelope of l_e over K_e = X_u x X_v at (a,b), via LP over vertex pairs."""
    u, v = e
    Vu, Vv = g.sets[u].vertices(), g.sets[v].vertices()
    if Vu is None or Vv is None:
        return None
    K = np.array([np.r_[p, q] for p in Vu for q in Vv])
    nu = Vu.shape[1]
    vals = np.array([g.cost[e].val(k[:nu], k[nu:]) for k in K])
    m = np.r_[a, b]
    p = cp.Variable(len(K), nonneg=True)
    slack = cp.Variable(len(m))
    prob = cp.Problem(cp.Maximize(vals @ p - 1e4 * cp.norm1(slack)), [cp.sum(p) == 1, K.T @ p + slack == m])
    prob.solve(solver=SOLVER)
    return float(vals @ p.value)


def jensen_bound(g, sol, tol=TOL):
    tot = 0.0
    for e in g.edges:
        ye = sol["y"][e]
        if ye <= tol:
            continue
        c = cav_lp(g, e, sol["z"][e] / ye, sol["zp"][e] / ye)
        if c is None:
            return None
        tot += ye * c
    return tot


def delta_e(g, e):
    """Delta_e = max_{K_e} (cav_e - l_e) (convex program over vertex weights)."""
    u, v = e
    Vu, Vv = g.sets[u].vertices(), g.sets[v].vertices()
    K = np.array([np.r_[p, q] for p in Vu for q in Vv])
    nu = Vu.shape[1]
    vals = np.array([g.cost[e].val(k[:nu], k[nu:]) for k in K])
    p = cp.Variable(len(K), nonneg=True)
    m = K.T @ p
    prob = cp.Problem(cp.Maximize(vals @ p - g.cost[e].expr(m[:nu], m[nu:])), [cp.sum(p) == 1])
    prob.solve(solver=SOLVER)
    return max(0.0, float(prob.value))


def max_path_weight(g, w):
    """max over s-t paths of sum of edge weights w (DAG)."""
    order = []
    indeg = {v: len(g.inn[v]) for v in g.V}
    q = [v for v in g.V if indeg[v] == 0]
    while q:
        v = q.pop()
        order.append(v)
        for (_, x) in g.out[v]:
            indeg[x] -= 1
            if indeg[x] == 0:
                q.append(x)
    best = {v: -np.inf for v in g.V}
    best[g.s] = 0.0
    for v in order:
        if best[v] == -np.inf:
            continue
        for e in g.out[v]:
            best[e[1]] = max(best[e[1]], best[v] + w[e])
    return best[g.t]


# ----------------------------------------------------------------------------- kappa
def kappa_l2(Su, Sv):
    """sec(theta_e): theta_e = half-angle of narrowest circular cone containing X_v - X_u.
    Exact for polytope/point pairs (vertex differences) and for ball/point pairs;
    otherwise an upper bound from enclosing balls."""
    Vu, Vv = Su.vertices(), Sv.vertices()
    if Vu is not None and Vv is not None:
        W = np.array([q - p for p in Vu for q in Vv])
        nr = np.linalg.norm(W, axis=1)
        W = W[nr > 1e-12] / nr[nr > 1e-12, None]
        if len(W) == 0:
            return 1.0
        a, tt = cp.Variable(W.shape[1]), cp.Variable()
        cp.Problem(cp.Maximize(tt), [W @ a >= tt, cp.norm(a) <= 1]).solve(solver=SOLVER)
        return np.inf if tt.value <= 1e-9 else 1.0 / float(tt.value)
    cu, ru = Su.circ()
    cv, rv = Sv.circ()
    d = np.linalg.norm(cv - cu)
    if ru + rv >= d:
        return np.inf
    return 1.0 / np.sqrt(1 - ((ru + rv) / d) ** 2)


def kappa_sq(Su, Sv, return_cert=False):
    """kappa^sq_e = sup_{D_e} cav(|.|^2)/|.|^2 for D_e = X_v - X_u (Corollary C, exact form).

    kappa^sq = 1/(1 - tau*),  tau* = min_u max_{w in ext D} (|w|^2 |u|^2 - 2 w.u + 1),
    i.e. the best enclosing ball B(c, rho) of D with c = u/|u|^2, rho^2 = tau* |c|^2.
    Exact for point/polytope pairs (ext D within vertex differences) and for ball/point
    pairs (closed form).  For mixed ball/polytope pairs a valid upper bound is returned.
    With return_cert, also returns (mu, W): a mixture certificate (dual weights on active
    points) with sum mu|w|^2 / |sum mu w|^2 = 1/(1 - tau*)."""
    Vu, Vv = Su.vertices(), Sv.vertices()
    if Vu is not None and Vv is not None:
        W = np.array([q - p for p in Vu for q in Vv])
        nz = np.linalg.norm(W, axis=1) >= 1e-12
        if not nz.any():            # D = {0}: the edge length is identically 0, no Jensen loss
            return (1.0, None) if return_cert else 1.0
        if not nz.all():            # 0 is a vertex of D (0 in D): kappa^sq = inf (mix 0 with any w != 0)
            return (np.inf, None) if return_cert else np.inf
        u, tt, sq = cp.Variable(W.shape[1]), cp.Variable(), cp.Variable(nonneg=True)
        n2 = np.sum(W ** 2, axis=1)
        cons = [n2[i] * sq - 2 * W[i] @ u + 1 <= tt for i in range(len(W))]   # linear rows: scalar duals
        cp.Problem(cp.Minimize(tt), cons + [cp.sum_squares(u) <= sq]).solve(solver=SOLVER)
        tau = float(tt.value)
        if tau >= 1 - 1e-10:
            return (np.inf, None) if return_cert else np.inf
        k = 1.0 / (1.0 - tau)
        if return_cert:
            mu = np.array([max(0.0, float(c.dual_value)) for c in cons])
            return k, (mu / mu.sum(), W)
        return k
    if Su.kind in ("ball", "point") and Sv.kind in ("ball", "point"):
        cu, ru = Su.circ()
        cv, rv = Sv.circ()
        d2 = float(np.sum((cv - cu) ** 2))
        rho2 = (ru + rv) ** 2
        k = np.inf if rho2 >= d2 else d2 / (d2 - rho2)
        return (k, None) if return_cert else k
    cu, ru = Su.circ()
    cv, rv = Sv.circ()
    d2 = float(np.sum((cv - cu) ** 2))
    rho2 = (ru + rv) ** 2
    k = np.inf if rho2 >= d2 else d2 / (d2 - rho2)
    return (k, None) if return_cert else k
