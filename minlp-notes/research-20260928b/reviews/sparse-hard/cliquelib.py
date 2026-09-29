"""Shared routines for the exact conflict-clique experiments (independent of the author's code).

- all_f: f(S) for all k-subsets (batched ridge, p-side).
- all_midpoints: g((1_S+1_T)/2) for all pairs, via the identity
      g(mid) = min_{b1,b2} ||y - X_S b1 - X_T b2||^2 + 2 lam (||b1||^2 + ||b2||^2)
             = y'y - v'(Z'Z + 2 lam I)^{-1} v,   Z = [X_S, X_T],  v = Z'y,
  which follows from g(z) = y'(I + X diag(z) X'/lam)^{-1} y with
  X diag(z) X' = (X_S X_S' + X_T X_T')/2 (push-through identity). A shared
  feature appears twice with penalty 2 lam each, i.e. effective penalty lam, as
  in Lemma 1.5. This is a different computation from the author's g_mid.
- max_clique: exact maximum clique (bitset branch and bound with greedy
  colouring bound, Tomita-style), tested against brute force in selftest().
- node_bound: certified node relaxation bound r(S0,S1) via cvxpy/Clarabel and
  the dual bound of Lemma 1.1 (own implementation).
"""
import itertools
import numpy as np


def instance_author(n, p, k, b=1.0, sigma=0.5, seed=0):
    """Replicates core.instance of the note's code (same RNG sequence)."""
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    S = np.sort(rng.choice(p, k, replace=False))
    beta = np.zeros(p)
    if b > 0:
        beta[S] = b * rng.choice([-1.0, 1.0], k)
    y = X @ beta + sigma * rng.standard_normal(n)
    return X, y, tuple(S.tolist())


def all_f(X, y, lam, k):
    p = X.shape[1]
    G = X.T @ X; bv = X.T @ y; yy = float(y @ y)
    sups = np.array(list(itertools.combinations(range(p), k)), dtype=np.int64)
    A = G[sups[:, :, None], sups[:, None, :]] + lam * np.eye(k)
    v = bv[sups]
    sol = np.linalg.solve(A, v[:, :, None])[:, :, 0]
    f = yy - np.einsum('ij,ij->i', v, sol)
    return sups, f


def midpoints_for_pairs(G, bv, yy, lam, sups, I, J):
    idx = np.concatenate([sups[I], sups[J]], axis=1)
    m = idx.shape[1]
    A = G[idx[:, :, None], idx[:, None, :]] + 2 * lam * np.eye(m)
    v = bv[idx]
    sol = np.linalg.solve(A, v[:, :, None])[:, :, 0]
    return yy - np.einsum('ij,ij->i', v, sol)


def conflict_edges(X, y, lam, sups, thresh, cand=None, chunk=200000):
    """Return list of (i,j) (indices into sups) with g(mid) < thresh, over all pairs of cand."""
    G = X.T @ X; bv = X.T @ y; yy = float(y @ y)
    cand = np.arange(len(sups)) if cand is None else np.asarray(cand)
    N = len(cand)
    iu = np.triu_indices(N, 1)
    I_all, J_all = iu
    edges = []
    gmin = np.inf
    for s in range(0, len(I_all), chunk):
        I = cand[I_all[s:s + chunk]]; J = cand[J_all[s:s + chunk]]
        gm = midpoints_for_pairs(G, bv, yy, lam, sups, I, J)
        gmin = min(gmin, gm.min())
        sel = gm < thresh
        edges.extend(zip(I[sel].tolist(), J[sel].tolist()))
    return edges, gmin


def max_clique(nv, edges):
    """Exact maximum clique. Vertices 0..nv-1. Returns list of vertices."""
    nbr = [set() for _ in range(nv)]
    for a, b in edges:
        nbr[a].add(b); nbr[b].add(a)
    verts = [v for v in range(nv) if nbr[v]]
    if not verts:
        return [0] if nv > 0 else []
    # degeneracy-type order: sort by degree descending, relabel
    verts.sort(key=lambda v: -len(nbr[v]))
    pos = {v: i for i, v in enumerate(verts)}
    adj = [0] * len(verts)
    for v in verts:
        m = 0
        for u in nbr[v]:
            m |= 1 << pos[u]
        adj[pos[v]] = m
    best = [[]]

    def expand(R, P):
        # greedy colouring of P
        order = []; bnd = []
        U = P; col = 0
        while U:
            col += 1
            Q = U
            while Q:
                low = Q & -Q
                v = low.bit_length() - 1
                Q &= ~low; Q &= ~adj[v]
                U &= ~low
                order.append(v); bnd.append(col)
        for t in range(len(order) - 1, -1, -1):
            if len(R) + bnd[t] <= len(best[0]):
                return
            v = order[t]
            newP = P & adj[v]
            R.append(v)
            if newP:
                expand(R, newP)
            elif len(R) > len(best[0]):
                best[0] = list(R)
            R.pop()
            P &= ~(1 << v)

    expand([], (1 << len(verts)) - 1)
    return [verts[i] for i in best[0]]


def greedy_clique(nv, edges, starts=60):
    nbr = [set() for _ in range(nv)]
    for a, b in edges:
        nbr[a].add(b); nbr[b].add(a)
    order = sorted(range(nv), key=lambda v: -len(nbr[v]))
    best = []
    for s in order[:starts]:
        cl = [s]; cand = set(nbr[s])
        for v in order:
            if v in cand:
                cl.append(v); cand &= nbr[v]
        if len(cl) > len(best):
            best = cl
    return best


def selftest(seed=0):
    rng = np.random.default_rng(seed)
    for trial in range(200):
        nv = int(rng.integers(1, 13)); pr = rng.uniform(0.1, 0.9)
        edges = [(a, b) for a in range(nv) for b in range(a + 1, nv) if rng.random() < pr]
        E = set(edges)
        bestbf = 1 if nv else 0
        for r in range(2, nv + 1):
            for c in itertools.combinations(range(nv), r):
                if all((a, b) in E for a, b in itertools.combinations(c, 2)):
                    bestbf = max(bestbf, r)
        mc = max_clique(nv, edges)
        assert len(mc) == bestbf, (nv, edges, mc, bestbf)
        assert all((min(a, b), max(a, b)) in E for a, b in itertools.combinations(mc, 2))
    return True


def dual_bound(X, y, lam, k, a, S0=(), S1=()):
    c2 = (X.T @ a) ** 2
    p = X.shape[1]
    free = np.ones(p, bool); free[list(S0)] = False; free[list(S1)] = False
    kp = k - len(S1)
    top = np.sort(c2[free])[::-1][:kp].sum() if kp > 0 else 0.0
    return float(2 * a @ y - a @ a - (c2[list(S1)].sum() + top) / lam)


def g_nside(X, y, lam, z):
    n = X.shape[0]
    return float(y @ np.linalg.solve(np.eye(n) + (X * z) @ X.T / lam, y))


def node_bound(X, y, lam, k, S0=(), S1=()):
    """Returns (certified lower bound, primal value at the computed z)."""
    import cvxpy as cp
    n, p = X.shape
    beta = cp.Variable(p); z = cp.Variable(p); t = cp.Variable(p)
    cons = [z >= 0, z <= 1, cp.sum(z) <= k,
            cp.SOC(t + z, cp.vstack([2 * beta, t - z]), axis=0)]
    if S0:
        cons.append(z[list(S0)] == 0)
    if S1:
        cons.append(z[list(S1)] == 1)
    prob = cp.Problem(cp.Minimize(cp.sum_squares(y - X @ beta) + lam * cp.sum(t)), cons)
    prob.solve(solver=cp.CLARABEL)
    zz = np.clip(z.value, 0, 1)
    a1 = y - X @ beta.value
    a2 = np.linalg.solve(np.eye(n) + (X * zz) @ X.T / lam, y)
    LB = max(dual_bound(X, y, lam, k, a1, S0, S1), dual_bound(X, y, lam, k, a2, S0, S1))
    return LB, g_nside(X, y, lam, zz)
