"""Independent reviewer toolkit for GCS shortest-path relaxations.

Written from scratch for the review of gcs/a-priori-gap-bounds.md; it does not
import the author's code.

Sets:    Poly(A, b, V)  (H-rep plus vertex list), Ball(c, r), Pt(c).
Lengths: Len('l2'|'sq'|'l1'|'aff'|'zero', ...) with value and perspective.
Model:   G(sets, edges, s, t, lengths, econs) with optional linear edge
         equalities  Mu x_u + Mv x_v = m  (perspective: Mu z + Mv z' = m y).
relax(G, hull=..., deg=..., cuts=...)  -> REL (SIOPT (5.5)) or REL_H.
opt(G)   -> exact SPP value by enumerating simple s-t paths.
Rounding helpers from a REL_H point: pair-graph shortest path, closed-form
chain expectation, Jensen bound sum_e y_e cav_e (LP over vertices of K_e).
"""
import itertools
import heapq
import numpy as np
import cvxpy as cp

SOLVERS = ("CLARABEL", "SCS")


def solve(prob):
    for s in SOLVERS:
        try:
            if s == "CLARABEL":
                prob.solve(solver=s, tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
            else:
                prob.solve(solver=s)
            if prob.status in ("optimal", "optimal_inaccurate"):
                return prob.value
        except Exception:
            pass
    return None


# ------------------------------------------------------------------ sets
class Poly:
    def __init__(self, A, b, V):
        self.A = np.atleast_2d(np.asarray(A, float))
        self.b = np.asarray(b, float)
        self.V = np.atleast_2d(np.asarray(V, float))
        self.dim = self.V.shape[1]

    def persp(self, z, y):
        return [self.A @ z <= self.b * y]


class Pt:
    def __init__(self, c):
        self.c = np.atleast_1d(np.asarray(c, float))
        self.V = self.c[None, :]
        self.dim = len(self.c)

    def persp(self, z, y):
        return [z == self.c * y]


class Ball:
    def __init__(self, c, r):
        self.c = np.atleast_1d(np.asarray(c, float))
        self.r = float(r)
        self.V = None
        self.dim = len(self.c)

    def persp(self, z, y):
        return [cp.norm(z - self.c * y, 2) <= self.r * y]


def Box(lo, hi):
    lo = np.atleast_1d(np.asarray(lo, float))
    hi = np.atleast_1d(np.asarray(hi, float))
    n = len(lo)
    A = np.vstack([np.eye(n), -np.eye(n)])
    b = np.r_[hi, -lo]
    V = np.array(list(itertools.product(*zip(lo, hi))), float)
    V = np.unique(V, axis=0)
    return Poly(A, b, V)


def Seg(p, q):
    """Segment in R^n as a Poly (vertex list plus H-rep via affine hull)."""
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    n = len(p)
    d = q - p
    # H-rep: x = p + t d, 0<=t<=1 -> use orthogonal complement equalities
    U, S, Vt = np.linalg.svd(d[None, :])
    N = Vt[1:]  # rows orthogonal to d
    A = np.vstack([N, -N, d[None, :], -d[None, :]])
    b = np.r_[N @ p, -(N @ p), d @ q, -(d @ p)]
    return Poly(A, b, np.vstack([p, q]))


# ------------------------------------------------------------------ lengths
class Len:
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
        if k == "zero":
            return 0 * y
        raise ValueError(k)

    def val(self, x, xp):
        x = np.atleast_1d(np.asarray(x, float))
        xp = np.atleast_1d(np.asarray(xp, float))
        k = self.kind
        if k == "l2":
            return float(np.linalg.norm(xp - x))
        if k == "sq":
            return float(np.sum((xp - x) ** 2))
        if k == "l1":
            return float(np.sum(np.abs(xp - x)))
        if k == "aff":
            return float(self.c @ x + self.d @ xp + self.b0)
        if k == "zero":
            return 0.0
        raise ValueError(k)


L2, SQ, L1, ZERO = Len("l2"), Len("sq"), Len("l1"), Len("zero")


class FnLen(Len):
    """Length given by a perspective builder pf(z, zp, y) and a value function vf(x, xp)."""

    def __init__(self, pf, vf):
        super().__init__("fn")
        self.pf, self.vf = pf, vf

    def persp(self, z, zp, y):
        return self.pf(z, zp, y)

    def val(self, x, xp):
        return float(self.vf(np.atleast_1d(np.asarray(x, float)), np.atleast_1d(np.asarray(xp, float))))


def tailseg(k):
    """Order-1 region formulation: x = (a, b) in R^{2k}; length of edge = ||b_u - a_u|| (tail segment)."""
    return FnLen(lambda z, zp, y: cp.norm(z[k:] - z[:k], 2),
                 lambda x, xp: np.linalg.norm(x[k:] - x[:k]))


# ------------------------------------------------------------------ graph
class G:
    def __init__(self, sets, edges, s, t, lens, econs=None):
        self.sets = sets
        self.E = list(edges)
        self.s, self.t = s, t
        self.len = lens if isinstance(lens, dict) else {e: lens for e in self.E}
        self.econs = econs or {}
        self.inn = {v: [e for e in self.E if e[1] == v] for v in sets}
        self.out = {v: [e for e in self.E if e[0] == v] for v in sets}
        assert not self.inn[s] and not self.out[t]

    def paths(self):
        res = []

        def dfs(v, path, seen):
            if v == self.t:
                res.append(list(path))
                return
            for e in self.out[v]:
                w = e[1]
                if w not in seen:
                    seen.add(w)
                    path.append(e)
                    dfs(w, path, seen)
                    path.pop()
                    seen.remove(w)

        dfs(self.s, [], {self.s})
        return res


def restriction(g, path, return_x=False):
    """Convex restriction on a fixed path (edge list)."""
    verts = [path[0][0]] + [e[1] for e in path]
    X = {v: cp.Variable(g.sets[v].dim) for v in verts}
    cons = []
    one = 1.0
    for v in verts:
        cons += g.sets[v].persp(X[v], one)
    obj = 0
    for e in path:
        u, v = e
        obj = obj + g.len[e].persp(X[u], X[v], one)
        if e in g.econs:
            Mu, Mv, m = g.econs[e]
            cons.append(Mu @ X[u] + Mv @ X[v] == m)
    prob = cp.Problem(cp.Minimize(obj), cons)
    val = solve(prob)
    if val is None:
        return (np.inf, None) if return_x else np.inf
    if return_x:
        return val, {v: X[v].value for v in verts}
    return val


def opt(g, return_path=False):
    best, bp = np.inf, None
    for p in g.paths():
        v = restriction(g, p)
        if v < best:
            best, bp = v, p
    return (best, bp) if return_path else best


def relax(g, hull=False, deg=True, two_cycle=False, gsec=(), return_vars=False, lifted2=False):
    E = g.E
    y = {e: cp.Variable(nonneg=True) for e in E}
    z = {e: cp.Variable(g.sets[e[0]].dim) for e in E}
    zp = {e: cp.Variable(g.sets[e[1]].dim) for e in E}
    cons = []
    s, t = g.s, g.t
    cons.append(sum(y[e] for e in g.out[s]) == 1)
    cons.append(sum(y[e] for e in g.inn[t]) == 1)
    lam, w = {}, {}
    for v in g.sets:
        if v in (s, t):
            continue
        ins, outs = g.inn[v], g.out[v]
        fin = sum(y[e] for e in ins) if ins else 0
        fout = sum(y[e] for e in outs) if outs else 0
        cons.append(fin == fout)
        if deg and ins:
            cons.append(fin <= 1)
        if hull and ins and outs:
            for e in ins:
                for f in outs:
                    lam[e, f] = cp.Variable(nonneg=True)
                    w[e, f] = cp.Variable(g.sets[v].dim)
                    cons += g.sets[v].persp(w[e, f], lam[e, f])
            for e in ins:
                cons.append(sum(lam[e, f] for f in outs) == y[e])
                cons.append(sum(w[e, f] for f in outs) == zp[e])
            for f in outs:
                cons.append(sum(lam[e, f] for e in ins) == y[f])
                cons.append(sum(w[e, f] for e in ins) == z[f])
        else:
            if ins and outs:
                cons.append(sum(zp[e] for e in ins) == sum(z[f] for f in outs))
            elif ins:
                for e in ins:
                    cons.append(y[e] == 0)
            elif outs:
                for f in outs:
                    cons.append(y[f] == 0)
    for e in E:
        u, v = e
        cons += g.sets[u].persp(z[e], y[e])
        cons += g.sets[v].persp(zp[e], y[e])
        if e in g.econs:
            Mu, Mv, m = g.econs[e]
            cons.append(Mu @ z[e] + Mv @ zp[e] == m * y[e])
    if two_cycle:
        for e in E:
            u, v = e
            if (v, u) in y and v not in (s, t):
                yv = sum(y[f] for f in g.inn[v])
                cons.append(y[e] + y[(v, u)] <= yv)
    if lifted2:  # Science Robotics App. A.1 cuts lifted with Lemma 5.4 (SIOPT)
        for (i, j) in E:
            if (j, i) in y and i not in (s, t):
                yi = sum(y[f] for f in g.inn[i])
                zi = sum(zp[f] for f in g.inn[i])
                cons += g.sets[i].persp(zi - z[(i, j)] - zp[(j, i)], yi - y[(i, j)] - y[(j, i)])
                cons.append(yi - y[(i, j)] - y[(j, i)] >= 0)
    for S in gsec:  # sum_{e in S} y_e <= sum_{v in S minus k} y_v for all k
        inside = [e for e in E if e[0] in S and e[1] in S]
        yv = {v: sum(y[f] for f in g.inn[v]) for v in S}
        for k in S:
            cons.append(sum(y[e] for e in inside) <= sum(yv[v] for v in S if v != k))
    obj = 0
    for e in E:
        if g.len[e].kind == "sq":
            # explicit epigraph of the perspective of ||.||^2:  t*y >= ||w||^2, t,y >= 0
            te = cp.Variable(nonneg=True)
            dlt = zp[e] - z[e]
            cons.append(cp.SOC(te + y[e], cp.hstack([2 * dlt, te - y[e]])))
            obj = obj + te
        else:
            obj = obj + g.len[e].persp(z[e], zp[e], y[e])
    prob = cp.Problem(cp.Minimize(obj), cons)
    val = solve(prob)
    if not return_vars:
        return val
    sol = dict(
        y={e: float(y[e].value) for e in E},
        z={e: np.asarray(z[e].value, float) for e in E},
        zp={e: np.asarray(zp[e].value, float) for e in E},
        lam={k: float(lam[k].value) for k in lam},
        w={k: np.asarray(w[k].value, float) for k in w},
    )
    return val, sol


# ------------------------------------------------------------------ rounding tools
def project(S, x):
    x = np.atleast_1d(np.asarray(x, float))
    if isinstance(S, Pt):
        return S.c.copy()
    if isinstance(S, Ball):
        d = x - S.c
        n = np.linalg.norm(d)
        return x if n <= S.r else S.c + d * (S.r / n)
    if np.all(S.A @ x <= S.b + 1e-10):
        return x
    p = cp.Variable(S.dim)
    cp.Problem(cp.Minimize(cp.sum_squares(p - x)), [S.A @ p <= S.b]).solve(solver="CLARABEL")
    return np.asarray(p.value, float)


def pair_positions(g, sol, tol=1e-6):
    """Return dict: pair (d,e) -> (prob lambda, position of shared vertex), after
    cleaning: flows/pairs below tol are dropped and barycenters are projected onto
    their sets (removes solver-tolerance noise).  Boundary pairs ('*', e) for
    e in out(s), (e, '*') for e in in(t)."""
    y, z, zp, lam, w = sol["y"], sol["z"], sol["zp"], sol["lam"], sol["w"]
    P = {}
    for e in g.out[g.s]:
        if y[e] > tol:
            P[("*", e)] = (y[e], project(g.sets[g.s], z[e] / y[e]))
    for e in g.inn[g.t]:
        if y[e] > tol:
            P[(e, "*")] = (y[e], project(g.sets[g.t], zp[e] / y[e]))
    for (d, e), l in lam.items():
        if l > tol and y[d] > tol and y[e] > tol:
            P[(d, e)] = (l, project(g.sets[d[1]], w[d, e] / l))
    return P


def chain_stats(g, sol, tol=1e-6):
    """Closed-form expected cost of the Markov-chain rounding and the Jensen
    right-hand side pieces; returns (E_cost, dict e -> list of (prob, xu, xv))."""
    y = sol["y"]
    P = pair_positions(g, sol, tol)
    into = {}
    outof = {}
    for (d, e), (l, x) in P.items():
        if e != "*":
            into.setdefault(e, []).append((d, l, x))
        if d != "*":
            outof.setdefault(d, []).append((e, l, x))
    Ecost = 0.0
    mix = {}
    for e in g.E:
        if y[e] <= tol:
            continue
        A = into.get(e, [])
        B = outof.get(e, [])
        sa = sum(l for _, l, _ in A)
        sb = sum(l for _, l, _ in B)
        lst = []
        for (_, la, xa) in A:
            for (_, lb, xb) in B:
                p = (la / sa) * (lb / sb)
                lst.append((p, xa, xb))
                Ecost += y[e] * p * g.len[e].val(xa, xb)
        mix[e] = lst
    return Ecost, mix


def pair_graph_sp(g, sol, tol=1e-6):
    """Dijkstra over pair nodes (costs assumed >= 0 or DAG); returns cost and
    list of (vertex, position) along the chosen walk."""
    P = pair_positions(g, sol, tol)
    succ = {}
    for (d, e) in P:
        if d != "*":
            pass
    by_first = {}
    for (d, e) in P:
        by_first.setdefault(d, []).append((d, e))
    # arcs (d,e) -> (e,f) with cost len_e(pos(d,e), pos(e,f))
    starts = [k for k in P if k[0] == "*"]
    dist = {k: 0.0 for k in starts}
    prev = {}
    pq = [(0.0, i, k) for i, k in enumerate(starts)]
    heapq.heapify(pq)
    cnt = len(pq)
    done = set()
    best_end, best_val = None, np.inf
    # Bellman-Ford style if negative costs: use simple label-correcting
    while pq:
        dv, _, k = heapq.heappop(pq)
        if k in done:
            continue
        done.add(k)
        d, e = k
        if e == "*":
            if dv < best_val:
                best_val, best_end = dv, k
            continue
        for k2 in by_first.get(e, []):
            c = g.len[e].val(P[k][1], P[k2][1])
            nd = dv + c
            if nd < dist.get(k2, np.inf) - 1e-15:
                dist[k2] = nd
                prev[k2] = k
                cnt += 1
                heapq.heappush(pq, (nd, cnt, k2))
    return best_val


def cav_lp(len_e, Vu, Vv, xbar, xbarp):
    """cav_e at (xbar, xbarp) over K_e = conv(Vu) x conv(Vv) for convex len_e:
    LP over product vertices."""
    pts = [(a, b) for a in Vu for b in Vv]
    vals = np.array([len_e.val(a, b) for a, b in pts])
    p = cp.Variable(len(pts), nonneg=True)
    M1 = np.array([a for a, _ in pts]).T
    M2 = np.array([b for _, b in pts]).T
    # small slack absorbs solver-tolerance infeasibility of the barycenters
    s1 = cp.Variable(len(xbar))
    s2 = cp.Variable(len(xbarp))
    cons = [cp.sum(p) == 1, M1 @ p == xbar + s1, M2 @ p == xbarp + s2]
    prob = cp.Problem(cp.Maximize(vals @ p - 1e3 * (cp.norm1(s1) + cp.norm1(s2))), cons)
    v = solve(prob)
    return v


def delta_max(len_e, Vu, Vv):
    """Maximal Jensen defect over K_e (polytopes): max_p sum p_i l(k_i) - l(sum p_i k_i)."""
    pts = [(a, b) for a in Vu for b in Vv]
    vals = np.array([len_e.val(a, b) for a, b in pts])
    p = cp.Variable(len(pts), nonneg=True)
    M1 = np.array([a for a, _ in pts]).T
    M2 = np.array([b for _, b in pts]).T
    x = M1 @ p
    xp = M2 @ p
    obj = vals @ p - len_e.persp(x, xp, 1.0)
    prob = cp.Problem(cp.Maximize(obj), [cp.sum(p) == 1])
    return solve(prob)
