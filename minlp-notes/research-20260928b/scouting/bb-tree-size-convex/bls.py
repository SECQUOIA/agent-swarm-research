"""Binary least squares (convex MIQP):  min ||y - A x||^2,  x in {-1,1}^N,
with the natural box relaxation x in [-1,1]^N.  Random model (square/tall
Gaussian MIMO):  y = sqrt(rho/N) H x* + w.

Tools:
  * enumerate(): all 2^N objective values (N <= ~22)
  * conflict clique: midpoint-conflict graph, greedy clique lower bound on
    the number of leaves of ANY convex-piece branching tree
  * bnb(): best-first B&B with box relaxation (variable branching)
  * min_tree(): exact minimum variable-branching tree (DP, tiny N)
"""
import heapq, itertools
import numpy as np
from scipy.optimize import lsq_linear


def instance(N, M, rho, seed):
    rng = np.random.default_rng(seed)
    H = rng.standard_normal((M, N))
    A = np.sqrt(rho / N) * H
    xs = rng.choice([-1.0, 1.0], N)
    y = A @ xs + rng.standard_normal(M)
    return A, y, xs


def all_values(A, y):
    N = A.shape[1]
    G = A.T @ A
    b = A.T @ y
    c = y @ y
    idx = np.arange(2 ** N, dtype=np.int64)
    out = np.empty(2 ** N)
    chunk = 1 << 16
    for s in range(0, 2 ** N, chunk):
        ii = idx[s:s + chunk]
        X = 1.0 - 2.0 * ((ii[:, None] >> np.arange(N)) & 1)
        out[s:s + chunk] = c - 2 * X @ b + np.einsum('ij,jk,ik->i', X, G, X)
    return out


def to_vec(i, N):
    return 1.0 - 2.0 * ((i >> np.arange(N)) & 1)


def conflict_clique(A, y, vals, eps=1e-9, eta_max=None, maxcand=4000):
    """Greedy clique in the midpoint-conflict graph on near-optimal points.
    a~b  iff  (f(a)+f(b))/2 - ||A(a-b)||^2/4 < OPT - eps.
    Candidates: the maxcand best points.  Returns clique size and members."""
    N = A.shape[1]
    OPT = vals.min()
    order = np.argsort(vals)[:maxcand]
    V = np.array([to_vec(int(i), N) for i in order])
    f = vals[order]
    AV = V @ A.T
    # pairwise ||A(a-b)||^2 = |Aa|^2 + |Ab|^2 - 2 <Aa,Ab>
    sq = (AV * AV).sum(1)
    D = sq[:, None] + sq[None, :] - 2 * AV @ AV.T
    mid = 0.5 * (f[:, None] + f[None, :]) - D / 4
    adj = mid < OPT - eps
    np.fill_diagonal(adj, False)
    # greedy: grow clique in order of objective value
    best = []
    for start in range(min(50, len(f))):
        cl = [start]
        cand = adj[start].copy()
        for j in range(len(f)):
            if cand[j]:
                cl.append(j)
                cand &= adj[j]
        if len(cl) > len(best):
            best = cl
    return len(best), f[best] - OPT


def relax(A, y, fixed):
    """Box relaxation with fixings dict {i: +-1}. Returns (value, x)."""
    N = A.shape[1]
    x = np.zeros(N)
    fi = list(fixed.keys())
    for i, v in fixed.items():
        x[i] = v
    free = [i for i in range(N) if i not in fixed]
    r0 = y - A[:, fi] @ x[fi] if fi else y.copy()
    if free:
        r = lsq_linear(A[:, free], r0, bounds=(-1.0, 1.0), method='bvls', tol=1e-13)
        x[free] = np.clip(r.x, -1, 1)
    res = y - A @ x
    return float(res @ res), x


def relax_lb(A, y, fixed):
    """Relaxation value with a certified dual lower bound (FW/Lagrangian)."""
    val, x = relax(A, y, fixed)
    g = -2 * A.T @ (y - A @ x)
    free = [i for i in range(A.shape[1]) if i not in fixed]
    # min over box of g^T (x' - x) on free coords
    lb = val + sum(-abs(g[i]) - g[i] * x[i] for i in free)
    return lb, val, x


def bnb(A, y, xinit=None, rtol=1e-9, max_nodes=10**6, branch="maxfrac"):
    N = A.shape[1]
    UB, xb = np.inf, None
    for x0 in (xinit or []):
        v = float(np.sum((y - A @ x0) ** 2))
        if v < UB:
            UB, xb = v, x0.copy()
    heap = [(-np.inf, 0, {})]
    tie = 1
    nodes = 0
    while heap:
        plb, _, fx = heapq.heappop(heap)
        if plb >= UB - rtol * abs(UB):
            continue
        nodes += 1
        if nodes > max_nodes:
            return nodes, UB, False
        lb, val, x = relax_lb(A, y, fx)
        xr = np.sign(x); xr[xr == 0] = 1
        vr = float(np.sum((y - A @ xr) ** 2))
        if vr < UB:
            UB, xb = vr, xr
        if lb >= UB - rtol * abs(UB):
            continue
        free = [i for i in range(N) if i not in fx]
        if not free:
            continue
        if branch == "maxfrac":
            i = min(free, key=lambda j: abs(x[j]))
        else:
            i = free[0]
        for v in (-1.0, 1.0):
            f2 = dict(fx); f2[i] = v
            heapq.heappush(heap, (lb, tie, f2)); tie += 1
    return nodes, UB, True


def min_tree(A, y, OPT, rtol=1e-9):
    from functools import lru_cache
    N = A.shape[1]
    thr = OPT - rtol * abs(OPT)

    @lru_cache(maxsize=None)
    def T(key):
        fx = dict(key)
        lb, _, _ = relax_lb(A, y, fx)
        if lb >= thr or len(fx) == N:
            return 1
        best = None
        for i in range(N):
            if i in fx:
                continue
            a = T(tuple(sorted({**fx, i: -1.0}.items())))
            if best is not None and a >= best:
                continue
            a += T(tuple(sorted({**fx, i: 1.0}.items())))
            if best is None or a < best:
                best = a
        return 1 + best
    return T(())
