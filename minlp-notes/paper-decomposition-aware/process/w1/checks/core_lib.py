"""Independent exact-arithmetic model of the cleaned core algorithm.

Per-coordinate curvature L_i = max(0, d^2F/dx_i^2), dyadic per-coordinate
meshes h_ij = eta_j * 2^{-e_i}, grading theta = 2^{-mu}, cap
K = 10 * 2^mu * ceil(log2(n_P + 2)), min-marginal filtering, restart at the
lower endpoint vector.  Everything is Fraction arithmetic.  This is a finite
check of the statements in core-proofs.tex, not a proof.
"""

from fractions import Fraction as Fr
from itertools import product
from math import prod


class Abort(Exception):
    pass


class Problem:
    """F(x) = c0 + sum_i b_i x_i + sum_{(i,j), i<=j} Q_ij x_i x_j."""

    def __init__(self, n, lo, hi, integer, c0, b, quad, bags, edges):
        self.n = n
        self.lo = [Fr(v) for v in lo]
        self.hi = [Fr(v) for v in hi]
        self.integer = set(integer)
        self.c0 = Fr(c0)
        self.b = [Fr(v) for v in b]
        self.quad = {tuple(sorted(k)): Fr(v) for k, v in quad.items() if v}
        self.bags = [tuple(bag) for bag in bags]
        self.edges = [tuple(e) for e in edges]
        for (i, j) in self.quad:
            assert any(i in bag and j in bag for bag in self.bags), (i, j)
        self.L = [max(Fr(0), 2 * self.quad.get((i, i), Fr(0))) for i in range(n)]
        self.P = [i for i in range(n) if self.L[i] > 0]
        nb = len(self.bags)
        self.nbr = [[] for _ in range(nb)]
        for u, v in self.edges:
            self.nbr[u].append(v)
            self.nbr[v].append(u)
        # rooted order
        self.parent = [-1] * nb
        order, seen = [0], {0}
        for u in order:
            for v in self.nbr[u]:
                if v not in seen:
                    seen.add(v)
                    self.parent[v] = u
                    order.append(v)
        assert len(order) == nb
        self.order = order
        self.home = [next(t for t, bag in enumerate(self.bags) if i in bag) for i in range(n)]
        self.term_home = {k: next(t for t, bag in enumerate(self.bags)
                                  if k[0] in bag and k[1] in bag) for k in self.quad}
        # running intersection check
        for i in range(n):
            cont = {t for t, bag in enumerate(self.bags) if i in bag}
            start = next(iter(cont))
            reach, stack = {start}, [start]
            while stack:
                u = stack.pop()
                for v in self.nbr[u]:
                    if v in cont and v not in reach:
                        reach.add(v)
                        stack.append(v)
            assert reach == cont, "running intersection"

    def F(self, x):
        val = self.c0 + sum(bi * xi for bi, xi in zip(self.b, x))
        for (i, j), q in self.quad.items():
            val += q * x[i] * x[j]
        return val

    def feasible(self, x, box=None):
        lo, hi = (self.lo, self.hi) if box is None else box
        return all(lo[i] <= x[i] <= hi[i] for i in range(self.n)) and all(
            x[i].denominator == 1 for i in self.integer)


def corrected_widths(grid, integer):
    out = []
    for k, v in enumerate(grid):
        adj = []
        if k > 0:
            adj.append(v - grid[k - 1])
        if k + 1 < len(grid):
            adj.append(grid[k + 1] - v)
        out.append(max((d for d in adj if not (integer and d == 1)), default=Fr(0)))
    return out


def graded_grid(lo, hi, c, h, theta, integer, cap=None):
    """Outward graded grid from center c; step h + theta*t (continuous) or
    max(1, floor(h + theta*t)) (integer), clipped at the endpoints."""
    assert lo <= c <= hi
    nodes = {c, lo, hi}
    for end, sgn in ((lo, -1), (hi, 1)):
        p = c
        while p != end:
            t = abs(p - c)
            step = h + theta * t
            if integer:
                step = Fr(max(1, int(step // 1)))
            p = p + sgn * min(step, abs(end - p))
            nodes.add(p)
            if cap is not None and len(nodes) > cap:
                raise Abort()
    return sorted(nodes)


def tree_dp(pb, grids, corr):
    """Exact min-sum DP.  Returns beta, argmin y, min-marginals m[i][k]."""
    nb = len(pb.bags)
    tables = []
    for t, bag in enumerate(pb.bags):
        tab = {}
        unary = [i for i in bag if pb.home[i] == t]
        terms = [k for k, ht in pb.term_home.items() if ht == t]
        pos = {i: a for a, i in enumerate(bag)}
        for idx in product(*(range(len(grids[i])) for i in bag)):
            val = pb.c0 if t == 0 else Fr(0)
            for i in unary:
                v = grids[i][idx[pos[i]]]
                val += pb.b[i] * v - corr[i][idx[pos[i]]]
            for (i, j) in terms:
                val += pb.quad[(i, j)] * grids[i][idx[pos[i]]] * grids[j][idx[pos[j]]]
            tab[idx] = val
        tables.append(tab)

    def sep(u, v):
        return tuple(i for i in pb.bags[u] if i in pb.bags[v])

    msg = {}

    def send(u, v):
        s = sep(u, v)
        pos = {i: a for a, i in enumerate(pb.bags[u])}
        out = {}
        for idx, val in tables[u].items():
            tot = val + sum((msg[(w, u)][tuple(idx[pos[i]] for i in sep(w, u))]
                             for w in pb.nbr[u] if w != v), Fr(0))
            key = tuple(idx[pos[i]] for i in s)
            if key not in out or tot < out[key]:
                out[key] = tot
        msg[(u, v)] = out

    for u in reversed(pb.order):
        if pb.parent[u] >= 0:
            send(u, pb.parent[u])
    for u in pb.order:
        for v in pb.nbr[u]:
            if pb.parent[v] == u:
                send(u, v)
    calib = []
    for u in range(nb):
        pos = {i: a for a, i in enumerate(pb.bags[u])}
        cal = {}
        for idx, val in tables[u].items():
            cal[idx] = val + sum((msg[(w, u)][tuple(idx[pos[i]] for i in sep(w, u))]
                                  for w in pb.nbr[u]), Fr(0))
        calib.append(cal)
    beta = min(calib[0].values())
    for cal in calib:
        assert min(cal.values()) == beta
    marg = []
    for i in range(pb.n):
        t = pb.home[i]
        a = pb.bags[t].index(i)
        row = [None] * len(grids[i])
        for idx, val in calib[t].items():
            if row[idx[a]] is None or val < row[idx[a]]:
                row[idx[a]] = val
        marg.append(row)
    # backtrack a global minimizer using calibrated tables (consistent ties)
    assign = {}
    for u in pb.order:
        bag = pb.bags[u]
        best = None
        for idx, val in calib[u].items():
            if any(i in assign and assign[i] != idx[a] for a, i in enumerate(bag)):
                continue
            if val == beta and (best is None):
                best = idx
        assert best is not None
        for a, i in enumerate(bag):
            assign[i] = best[a]
    y = [grids[i][assign[i]] for i in range(pb.n)]
    return beta, y, marg


def penalties(pb, grids):
    out = []
    for i in range(pb.n):
        w = corrected_widths(grids[i], i in pb.integer)
        out.append([pb.L[i] * wi * wi / 8 for wi in w])
    return out


def ceil_log2(m):
    """ceil(log2(m)) for integer m >= 1."""
    return (m - 1).bit_length()


def dyadic_scales(pb):
    e = {}
    for i in pb.P:
        k = 0
        while Fr(4) ** k < pb.L[i]:
            k += 1
        while Fr(4) ** (k - 1) >= pb.L[i]:
            k -= 1
        assert Fr(4) ** (k - 1) < pb.L[i] <= Fr(4) ** k
        e[i] = k
    E = None
    for i in pb.P:
        s = pb.hi[i] - pb.lo[i]
        k = -200
        while Fr(2) ** (k - e[i]) < s:
            k += 1
        E = k if E is None else max(E, k)
    return e, E


def run_schedule(pb, eps, xstar=None, kappa=None, max_mu=12, log=None,
                 table_limit=400000, use_global_U=True, fixed_mu=None, stop_early=True):
    """Capped unknown-growth schedule.  Returns dict with the certificate of
    the successful trial.  If xstar/kappa are given, checks the stage
    invariants of the admissible trial."""
    n, P = pb.n, pb.P
    nP = len(P)
    lo_vec = list(pb.lo)
    U, xhat = pb.F(lo_vec), list(lo_vec)
    if nP == 0:
        grids = [sorted({pb.lo[i], pb.hi[i]}) for i in range(n)]
        corr = [[Fr(0)] * len(g) for g in grids]
        beta, y, _ = tree_dp(pb, grids, corr)
        return {"beta": beta, "xhat": y, "U": pb.F(y), "certificate": [grids], "trials": 0}
    e, E = dyadic_scales(pb)
    eta0 = Fr(2) ** E
    J = 0
    while Fr(9, 16) * nP * eta0 ** 2 / Fr(4) ** J > eps:
        J += 1
    ell = ceil_log2(nP + 2)
    stats = {"aborted_trials": 0, "stages": 0, "max_nodes": 0, "inv_checks": 0}
    mu = 2 if fixed_mu is None else fixed_mu
    while mu <= (max_mu if fixed_mu is None else fixed_mu):
        theta = Fr(1, 2 ** mu)
        K = 10 * 2 ** mu * ell
        admissible = kappa is not None and 8 * kappa * theta ** 2 <= 1
        box = (list(pb.lo), list(pb.hi))
        c = list(lo_vec)
        if not use_global_U:
            U, xhat = pb.F(lo_vec), list(lo_vec)
        cert = []
        aborted = False
        for j in range(J + 1):
            eta = eta0 / Fr(2) ** j
            grids = []
            try:
                for i in range(n):
                    if i in P:
                        h = eta / Fr(2) ** e[i]
                        grids.append(graded_grid(box[0][i], box[1][i], c[i], h, theta,
                                                 i in pb.integer, K))
                    else:
                        grids.append(sorted({box[0][i], box[1][i]}))
            except Abort:
                aborted = True
                break
            stats["max_nodes"] = max(stats["max_nodes"], max(len(g) for g in grids))
            if sum(prod(len(grids[i]) for i in bag) for bag in pb.bags) > table_limit:
                raise RuntimeError("table limit in check")
            corr = penalties(pb, grids)
            beta, y, marg = tree_dp(pb, grids, corr)
            stats["stages"] += 1
            Fy = pb.F(y)
            D_y = sum(corr[i][grids[i].index(y[i])] for i in range(n))
            assert Fy - beta == D_y
            if Fy < U:
                U, xhat = Fy, list(y)
            cert.append([list(g) for g in grids])
            if xstar is not None:
                Fstar = pb.F(xstar)
                assert beta <= Fstar, ("lower bound invalid", beta, Fstar)
                assert pb.feasible(xstar, box), "optimizer filtered out"
            if admissible:
                a = nP * eta ** 2
                Ej = sum(pb.L[i] * (y[i] - xstar[i]) ** 2 for i in P)
                Ec = sum(pb.L[i] * (c[i] - xstar[i]) ** 2 for i in P)
                assert Ec <= 4 * kappa * a, "center invariant"
                assert Ej <= kappa * a, ("stage invariant", Ej, kappa * a)
                assert D_y <= Fr(9, 16) * a, "gap bound"
                stats["inv_checks"] += 1
            if U - beta <= eps and (stop_early or j == J):
                return {"beta": beta, "xhat": xhat, "U": U, "certificate": cert,
                        "trial_mu": mu, "J": J, "stage": j, "stats": stats, "K": K}
            # filtering
            newlo, newhi = list(box[0]), list(box[1])
            for i in P:
                g = grids[i]
                if len(g) == 1:
                    continue
                keep = [k for k in range(len(g) - 1) if min(marg[i][k], marg[i][k + 1]) <= U]
                assert keep, "empty filter"
                newlo[i], newhi[i] = g[keep[0]], g[keep[-1] + 1]
                if admissible:
                    # localization: retained hull within 8 sqrt(kappa nP) h_ij (+1 integer)
                    h = eta / Fr(2) ** e[i]
                    for endpoint in (newlo[i], newhi[i]):
                        R = abs(endpoint - y[i])
                        if i in pb.integer:
                            R = max(Fr(0), R - 1)
                        assert R ** 2 <= 64 * kappa * nP * h ** 2, ("radius", i, R, h)
            # every optimizer, incumbent and y survive
            nb = (newlo, newhi)
            assert pb.feasible(y, nb) and pb.feasible(xhat, nb)
            box = nb
            c = list(y)
        if aborted:
            stats["aborted_trials"] += 1
            assert not admissible, "admissible trial aborted"
        else:
            assert not admissible, "admissible trial failed to reach eps"
        mu += 1
    raise RuntimeError("no trial succeeded up to max_mu")


def check_certificate(pb, grids_list, beta, xhat, eps):
    """Minimal certificate: stage grids only (plus claimed beta and a
    feasible point).  No messages, marginals or intermediate incumbents."""
    n = pb.n
    if not pb.feasible(xhat):
        return False, "infeasible point"
    if pb.F(xhat) - beta > eps:
        return False, "gap too large"
    box = (list(pb.lo), list(pb.hi))
    for j, grids in enumerate(grids_list):
        for i in range(n):
            g = grids[i]
            if g != sorted(set(g)) or g[0] != box[0][i] or g[-1] != box[1][i]:
                return False, "grid does not span the stage box"
            if i in pb.integer and any(v.denominator != 1 for v in g):
                return False, "noninteger node"
        corr = penalties(pb, grids)
        b_j, _, marg = tree_dp(pb, grids, corr)
        if j + 1 == len(grids_list):
            return (b_j >= beta), "final DP bound"
        nxt = grids_list[j + 1]
        nlo = [nxt[i][0] for i in range(n)]
        nhi = [nxt[i][-1] for i in range(n)]
        for i in range(n):
            if not (box[0][i] <= nlo[i] <= nhi[i] <= box[1][i]):
                return False, "next box not nested"
            g = grids[i]
            for k in range(len(g) - 1):
                inside = nlo[i] <= g[k] and g[k + 1] <= nhi[i]
                if not inside and min(marg[i][k], marg[i][k + 1]) < beta:
                    return False, "removed interval not certified"
        box = (nlo, nhi)
    return False, "empty certificate"


def exact_box_qp_min(pb):
    """Exact global minimum of a small mixed-integer box QP by face enumeration
    (faces with nonsingular free Hessian suffice)."""
    n = pb.n
    H = [[Fr(0)] * n for _ in range(n)]
    for (i, j), q in pb.quad.items():
        if i == j:
            H[i][i] += 2 * q
        else:
            H[i][j] += q
            H[j][i] += q
    ints = sorted(pb.integer)
    conts = [i for i in range(n) if i not in pb.integer]
    best, arg = None, None
    for ival in product(*(range(int(pb.lo[i]), int(pb.hi[i]) + 1) for i in ints)):
        for face in product(*((0, 1, 2) for _ in conts)):
            x = [Fr(0)] * n
            for i, v in zip(ints, ival):
                x[i] = Fr(v)
            free = []
            for i, f in zip(conts, face):
                if f == 0:
                    x[i] = pb.lo[i]
                elif f == 1:
                    x[i] = pb.hi[i]
                else:
                    free.append(i)
            if free:
                # solve H_FF x_F = -(b_F + H_{F,A} x_A)
                m = len(free)
                A = [[H[r][cc] for cc in free] + [-(pb.b[r] + sum(H[r][k] * x[k] for k in range(n) if k not in free))]
                     for r in free]
                ok = True
                for col in range(m):
                    piv = next((r for r in range(col, m) if A[r][col] != 0), None)
                    if piv is None:
                        ok = False
                        break
                    A[col], A[piv] = A[piv], A[col]
                    pv = A[col][col]
                    A[col] = [v / pv for v in A[col]]
                    for r in range(m):
                        if r != col and A[r][col] != 0:
                            f = A[r][col]
                            A[r] = [a - f * bb for a, bb in zip(A[r], A[col])]
                if not ok:
                    continue
                for r, i in enumerate(free):
                    x[i] = A[r][m]
                if not all(pb.lo[i] <= x[i] <= pb.hi[i] for i in free):
                    continue
            v = pb.F(x)
            if best is None or v < best:
                best, arg = v, list(x)
    return best, arg
