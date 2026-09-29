"""Branch-and-bound with the perspective (Boolean) relaxation for
cardinality-constrained ridge regression

    OPT = min_{|S| <= k} min_beta ||y - X_S beta||^2 + lam ||beta||^2
        = min_{|S| <= k} g(1_S),   g(z) = y^T (I + X diag(z) X^T / lam)^{-1} y.

The perspective relaxation at a node (S0 fixed to 0, S1 fixed to 1, F free)
is  min { g(z) : z_S0 = 0, z_S1 = 1, z_F in [0,1], sum_F z <= k - |S1| }.
g is convex (matrix fractional).  We minimise it by accelerated projected
gradient and report the Frank-Wolfe / Lagrangian dual bound

    LB = g(z) + min_{z' feasible} grad g(z)^T (z' - z)   (valid lower bound),

so every pruning decision is certified up to floating point.
"""
import heapq
import numpy as np


def exact_value(X, y, lam, S):
    S = list(S)
    if len(S) == 0:
        return float(y @ y)
    XS = X[:, S]
    G = XS.T @ XS + lam * np.eye(len(S))
    b = XS.T @ y
    return float(y @ y - b @ np.linalg.solve(G, b))


def _proj_capped(v, cap):
    """Project v onto {u in [0,1]^m : sum u <= cap}."""
    u = np.clip(v, 0.0, 1.0)
    if u.sum() <= cap + 1e-15:
        return u
    lo, hi = 0.0, float(v.max())
    for _ in range(60):
        tau = 0.5 * (lo + hi)
        if np.clip(v - tau, 0.0, 1.0).sum() > cap:
            lo = tau
        else:
            hi = tau
    return np.clip(v - hi, 0.0, 1.0)


class Relaxation:
    def __init__(self, X, y, lam, k):
        self.X, self.y, self.lam, self.k = X, y, lam, k
        self.n, self.p = X.shape
        self.nsolves = 0

    def g_grad(self, z):
        X, y, lam = self.X, self.y, self.lam
        P = np.nonzero(z > 0)[0]
        A = np.eye(self.n)
        if len(P):
            XP = X[:, P]
            A = A + (XP * (z[P] / lam)) @ XP.T
        a = np.linalg.solve(A, y)
        c = X.T @ a
        return float(y @ a), -(c * c) / lam


    def solve_ipm(self, S0, S1, z0=None):
        """Interior-point (Clarabel) solve + certified Frank-Wolfe dual bound."""
        import scipy.sparse as sp, clarabel
        self.nsolves += 1
        X, y, lam, k = self.X, self.y, self.lam, self.k
        n, p = X.shape
        S0s = set(S0); S1 = list(S1)
        kp = k - len(S1)
        if kp < 0:
            return np.inf, np.inf, None
        F = [i for i in range(p) if i not in S0s and i not in S1]
        z = np.zeros(p); z[S1] = 1.0
        if len(F) <= kp or kp == 0:
            if kp > 0:
                z[F] = 1.0
            v, _ = self.g_grad(z)
            return v, v, z
        A = S1 + F; na = len(A); nf = len(F)
        XA = X[:, A]
        N = na + 2 * nf
        P = np.zeros((N, N))
        P[:na, :na] = 2 * (XA.T @ XA)
        P[np.arange(len(S1)), np.arange(len(S1))] += 2 * lam
        q = np.zeros(N); q[:na] = -2 * XA.T @ y; q[na + nf:] = lam
        jj = np.arange(nf)
        # nonneg rows: -z<=0, z<=1, sum z<=k'
        r1 = np.concatenate([jj, nf + jj, np.full(nf, 2 * nf)])
        c1 = np.concatenate([na + jj, na + jj, na + jj])
        v1 = np.concatenate([-np.ones(nf), np.ones(nf), np.ones(nf)])
        b1 = np.concatenate([np.zeros(nf), np.ones(nf), [kp]])
        # SOC rows (t+z, 2beta, t-z)
        base = 2 * nf + 1
        r2 = np.concatenate([base + 3 * jj, base + 3 * jj, base + 3 * jj + 1, base + 3 * jj + 2, base + 3 * jj + 2])
        c2 = np.concatenate([na + nf + jj, na + jj, len(S1) + jj, na + nf + jj, na + jj])
        v2 = np.concatenate([-np.ones(nf), -np.ones(nf), -2 * np.ones(nf), -np.ones(nf), np.ones(nf)])
        Am = sp.csc_matrix((np.concatenate([v1, v2]), (np.concatenate([r1, r2]), np.concatenate([c1, c2]))),
                           shape=(base + 3 * nf, N))
        bv = np.concatenate([b1, np.zeros(3 * nf)])
        cones = [clarabel.NonnegativeConeT(base)] + [clarabel.SecondOrderConeT(3)] * nf
        s = clarabel.DefaultSettings(); s.verbose = False
        s.tol_gap_abs = 1e-10; s.tol_gap_rel = 1e-10; s.tol_feas = 1e-10
        sol = clarabel.DefaultSolver(sp.triu(sp.csc_matrix(P)).tocsc(), q, Am, bv, cones, s).solve()
        x = np.array(sol.x)
        z[F] = np.clip(x[na:na + nf], 0.0, 1.0)
        f, gr = self.g_grad(z)
        gF = gr[F]
        m = min(kp, nf)
        idx = np.argpartition(gF, m - 1)[:m] if m < nf else np.arange(nf)
        LB = f + np.minimum(gF[idx], 0.0).sum() - gF @ z[F]
        return LB, f, z

    def solve(self, S0, S1, z0=None, tol=1e-9, maxit=3000):
        """Return (LB, g(z), z).  LB is a valid lower bound."""
        self.nsolves += 1
        p, k = self.p, self.k
        kp = k - len(S1)
        if kp < 0:
            return np.inf, np.inf, None
        free = np.ones(p, bool)
        free[list(S0)] = False
        free[list(S1)] = False
        F = np.nonzero(free)[0]
        z = np.zeros(p)
        z[list(S1)] = 1.0
        if len(F) <= kp:  # all free can be one: exact
            z[F] = 1.0
            v, _ = self.g_grad(z)
            return v, v, z
        if kp == 0:
            v, _ = self.g_grad(z)
            return v, v, z
        # accelerated projected gradient on z_F
        if z0 is not None:
            zF = _proj_capped(z0[F], kp)
        else:
            zF = np.full(len(F), min(1.0, kp / len(F)))
        z[F] = zF
        f, gr = self.g_grad(z)
        L = 1.0
        yF, t = zF.copy(), 1.0
        best = (f, z.copy(), gr)
        LB = -np.inf
        for it in range(maxit):
            z[F] = yF
            fy, gy = self.g_grad(z)
            while True:
                zn = _proj_capped(yF - gy[F] / L, kp)
                z[F] = zn
                fn, gn = self.g_grad(z)
                d = zn - yF
                if fn <= fy + gy[F] @ d + 0.5 * L * (d @ d) + 1e-14 * abs(fy):
                    break
                L *= 2.0
            # dual (Frank-Wolfe) bound at zn
            gF = gn[F]
            m = min(kp, len(F))
            idx = np.argpartition(gF, m - 1)[:m] if m < len(F) else np.arange(len(F))
            lmo = np.minimum(gF[idx], 0.0).sum()
            LB = max(LB, fn + lmo - gF @ zn)
            if fn < best[0]:
                best = (fn, z.copy(), gn)
            if best[0] - LB <= tol * max(1.0, abs(best[0])):
                break
            # FISTA momentum with adaptive restart
            tn = 0.5 * (1 + np.sqrt(1 + 4 * t * t))
            if fn > fy:  # restart
                yF, t = zn.copy(), 1.0
            else:
                yF = zn + ((t - 1) / tn) * (zn - zF)
                t = tn
            zF = zn
            L *= 0.9
        return LB, best[0], best[1]


def bnb(X, y, lam, k, S_init=(), rtol=1e-6, branch="maxfrac", max_nodes=10**6,
        node_limit_is_error=False, ipm=True, pool=None):
    """Best-first B&B. Returns dict with nodes, opt, support."""
    rel = Relaxation(X, y, lam, k)
    p = X.shape[1]
    UB, best_S = np.inf, None
    for S in S_init:
        v = exact_value(X, y, lam, S)
        if v < UB:
            UB, best_S = v, tuple(sorted(S))
    cnt = 0
    heap = [(-np.inf, 0, (), (), None)]
    tie = 1
    nodes = 0
    root_LB = None
    while heap:
        plb, _, S0, S1, zpar = heapq.heappop(heap)
        if plb >= UB - rtol * UB:
            continue
        nodes += 1
        if nodes > max_nodes:
            return dict(nodes=nodes, opt=UB, support=best_S, done=False, root_LB=root_LB)
        LB, val, z = (rel.solve_ipm(S0, S1) if ipm else rel.solve(S0, S1, zpar))
        if root_LB is None:
            root_LB = LB
        if z is None:
            continue
        # heuristic incumbent: S1 plus top free entries of z
        kp = k - len(S1)
        free = np.ones(p, bool); free[list(S0)] = False; free[list(S1)] = False
        F = np.nonzero(free)[0]
        order = F[np.argsort(-z[F])][:kp]
        S = tuple(sorted(set(S1) | set(order.tolist())))
        v = exact_value(X, y, lam, S)
        if pool is not None:
            pool[S] = v
            # also one-swap neighbours of the node's candidate, for a richer pool
            if len(pool) < 20000:
                for a in S:
                    if a in S1:
                        continue
                    for b in F[np.argsort(-z[F])][kp:kp + 3]:
                        T = tuple(sorted((set(S) - {a}) | {int(b)}))
                        if T not in pool:
                            pool[T] = exact_value(X, y, lam, T)
        if v < UB:
            UB, best_S = v, S
        if LB >= UB - rtol * UB:
            continue
        zF = z[F]
        frac = np.minimum(zF, 1 - zF)
        if frac.max() <= 1e-6:
            # relaxation integral up to tolerance: its value is attained by S
            continue
        if branch == "maxfrac":
            i = int(F[np.argmax(frac)])
        elif branch == "maxz":
            cand = F[frac > 1e-7]
            i = int(cand[np.argmax(z[cand])])
        else:
            raise ValueError(branch)
        heapq.heappush(heap, (LB, tie, S0 + (i,), S1, z)); tie += 1
        heapq.heappush(heap, (LB, tie, S0, S1 + (i,), z)); tie += 1
    return dict(nodes=nodes, opt=UB, support=best_S, done=True, root_LB=root_LB,
                solves=rel.nsolves)


def instance(n, p, k, snr=None, sigma=1.0, b=1.0, seed=0, lam=None):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    Sstar = np.sort(rng.choice(p, k, replace=False))
    beta = np.zeros(p)
    beta[Sstar] = b * rng.choice([-1.0, 1.0], k)
    y = X @ beta + sigma * rng.standard_normal(n)
    if lam is None:
        lam = np.sqrt(n)
    return X, y, lam, tuple(Sstar.tolist())


def forward_greedy(X, y, lam, k):
    S = []
    for _ in range(k):
        best = None
        for j in range(X.shape[1]):
            if j in S:
                continue
            v = exact_value(X, y, lam, S + [j])
            if best is None or v < best[0]:
                best = (v, j)
        S.append(best[1])
    return tuple(sorted(S))
