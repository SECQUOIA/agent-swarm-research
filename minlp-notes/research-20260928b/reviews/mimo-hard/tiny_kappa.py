"""Exact class numbers on tiny instances (review check).

For y = A x* + w, A = sqrt(rho/N) H, P = {-1,1}^N, box relaxation, tau = OPT - eps:
  kappa      exact minimum number of admissible classes (r(conv I) >= tau),
             by an exact partition search with a min-norm-point oracle;
  omega_mid  clique number of the midpoint graph;
  omega_seg, chi_seg  clique and chromatic number of the segment graph;
  L_var      minimum number of leaves of a variable-branching certificate
             (exact DP over all 3^N subcubes, any adaptive rule);
  L_static   leaves of the static-order (x_1, x_2, ...) certificate.
Checks the chain omega_mid <= omega_seg <= chi_seg <= kappa <= L_var <= L_static
and counts instances with an edgeless midpoint graph but kappa >= 2, and with
chi_seg < kappa (the class number strictly above every pairwise bound).
Independent code (own generator, own min-norm-point and box-QP solvers).
Usage: python3 tiny_kappa.py N [seeds] > log
"""
import sys, itertools, json
import numpy as np
from scipy.optimize import lsq_linear

EPS = 1e-7          # certificate tolerance eps'
BUDGET = 200000     # admissibility tests in the exact partition search
BORDER = 1e-10      # relative: decisions with |r - tau| < BORDER (1 + OPT) are reported


def mnp_value(Z, tol=1e-12, maxit=500):
    """min ||z||^2 over conv(rows of Z) by Wolfe's algorithm."""
    n = Z.shape[0]
    norms = np.einsum("ij,ij->i", Z, Z)
    S = [int(np.argmin(norms))]
    lam = np.array([1.0])
    x = Z[S[0]].copy()
    scale = norms.max() + 1.0
    for _ in range(maxit):
        dots = Z @ x
        j = int(np.argmin(dots))
        if x @ x - dots[j] <= tol * scale or j in S:
            break
        S.append(j); lam = np.append(lam, 0.0)
        while True:
            P = Z[S]
            k = len(S)
            G = np.zeros((k + 1, k + 1)); G[:k, :k] = P @ P.T; G[:k, k] = 1; G[k, :k] = 1
            rhs = np.zeros(k + 1); rhs[k] = 1
            sol = np.linalg.lstsq(G, rhs, rcond=None)[0]
            mu = sol[:k]
            if np.all(mu > 1e-14):
                lam = mu; x = mu @ P
                break
            idx = mu <= 1e-14
            theta = np.min(lam[idx] / (lam[idx] - mu[idx]))
            lam = theta * mu + (1 - theta) * lam
            keep = lam > 1e-14
            S = [s for s, kp in zip(S, keep) if kp]
            lam = lam[keep]; lam = lam / lam.sum()
            x = lam @ Z[S]
    return float(x @ x)


def box_value(B, w, fixed):
    """min ||w + B u||^2, u in [0,2]^N with u_i fixed for i in fixed (dict)."""
    N = B.shape[1]
    free = [i for i in range(N) if i not in fixed]
    v = w + sum(B[:, i] * fixed[i] for i in fixed) if fixed else w.copy()
    if not free:
        return float(v @ v)
    r = lsq_linear(B[:, free], -v, bounds=(0.0, 2.0), method="bvls", tol=1e-14)
    res = v + B[:, free] @ r.x
    return float(res @ res)


def seg_min(za, zb):
    d = zb - za
    dd = d @ d
    t = 0.0 if dd == 0 else min(1.0, max(0.0, -(za @ d) / dd))
    z = za + t * d
    return float(z @ z)


def max_clique(adj):
    n = len(adj); best = [0]
    def rec(R, Pset):
        if not Pset:
            best[0] = max(best[0], len(R)); return
        if len(R) + len(Pset) <= best[0]:
            return
        for v in list(Pset):
            rec(R + [v], [u for u in Pset if adj[v][u] and u > v])
    rec([], list(range(n)))
    return best[0]


def chromatic(adj, lb):
    n = len(adj)
    order = sorted(range(n), key=lambda v: -sum(adj[v]))
    for K in range(max(lb, 1), n + 1):
        col = [-1] * n
        def rec(i, used):
            if i == n:
                return True
            v = order[i]
            for c in range(min(used + 1, K)):
                if all(not (adj[v][u] and col[u] == c) for u in range(n)):
                    col[v] = c
                    if rec(i + 1, max(used, c + 1)):
                        return True
                    col[v] = -1
            return False
        if rec(0, 0):
            return K
    return n


def analyse(N, beta, rho, seed):
    rng = np.random.default_rng(seed)
    M = int(round(beta * N))
    H = rng.standard_normal((M, N))
    w = rng.standard_normal(M)
    B = np.sqrt(rho / N) * H                         # x* = 1 WLOG (signed columns)
    pts = np.array(list(itertools.product([0.0, 2.0], repeat=N)))   # u-coordinates
    Z = w[None, :] + pts @ B.T                       # residuals of all vertices
    fv = np.einsum("ij,ij->i", Z, Z)
    OPT = fv.min(); W = float(w @ w)
    tau = OPT - EPS
    n = len(pts)
    border = [0]
    cache = {}

    def admissible(mask_list):
        key = frozenset(mask_list)
        if key in cache:
            return cache[key]
        val = mnp_value(Z[list(key)])
        if abs(val - tau) < BORDER * (1 + OPT):
            border[0] += 1
        cache[key] = val >= tau
        return cache[key]

    mid = [[False] * n for _ in range(n)]
    seg = [[False] * n for _ in range(n)]
    for a in range(n):
        for b in range(a + 1, n):
            zm = (Z[a] + Z[b]) / 2
            mid[a][b] = mid[b][a] = (zm @ zm) < tau
            seg[a][b] = seg[b][a] = seg_min(Z[a], Z[b]) < tau
    om_mid = max_clique(mid); om_seg = max_clique(seg)
    chi_seg = chromatic(seg, om_seg)
    mid_edges = sum(mid[a][b] for a in range(n) for b in range(a + 1, n))

    # exact minimum partition into admissible classes (hereditary => = cover)
    order = sorted(range(n), key=lambda v: (-sum(seg[v]), fv[v]))
    best = [n + 1]; best_part = [None]
    # greedy upper bound
    classes = []
    for v in order:
        for C in classes:
            if not any(seg[v][u] for u in C) and admissible(C + [v]):
                C.append(v); break
        else:
            classes.append([v])
    best[0] = len(classes); best_part[0] = [list(C) for C in classes]
    calls = [0]

    class Budget(Exception):
        pass

    def rec(i, classes):
        if calls[0] > BUDGET:
            raise Budget
        if len(classes) >= best[0]:
            return
        if i == n:
            best[0] = len(classes); best_part[0] = [list(C) for C in classes]; return
        v = order[i]
        for C in classes:
            if any(seg[v][u] for u in C):
                continue
            calls[0] += 1
            if admissible(C + [v]):
                C.append(v); rec(i + 1, classes); C.pop()
                if best[0] <= chi_seg:
                    return
        if len(classes) + 1 < best[0]:
            classes.append([v]); rec(i + 1, classes); classes.pop()

    exact = True
    if best[0] > chi_seg:
        try:
            rec(0, [])
        except Budget:
            exact = False
    kappa_search = best[0]

    # variable branching: exact DP over subcubes
    memo = {}
    def leaves(fixed_items):
        if fixed_items in memo:
            return memo[fixed_items]
        fixed = dict(fixed_items)
        if box_value(B, w, fixed) >= tau or len(fixed) == N:
            memo[fixed_items] = 1; return 1
        bestv = None
        for i in range(N):
            if i in fixed:
                continue
            tot = sum(leaves(tuple(sorted(list(fixed_items) + [(i, val)]))) for val in (0.0, 2.0))
            bestv = tot if bestv is None else min(bestv, tot)
        memo[fixed_items] = bestv
        return bestv
    L_var = leaves(tuple())

    def static(fixed_items, d):
        fixed = dict(fixed_items)
        if box_value(B, w, fixed) >= tau or d == N:
            return 1
        return sum(static(fixed_items + ((d, val),), d + 1) for val in (0.0, 2.0))
    L_static = static(tuple(), 0)
    R = box_value(B, w, {})
    # if the search was cut, kappa lies in [chi_seg, min(kappa_search, L_var)]
    kappa = kappa_search if exact else None
    return dict(N=N, beta=beta, rho=rho, seed=seed, xstar_opt=bool(abs(OPT - W) < 1e-9),
                root_gap=(OPT - R) / OPT, mid_edges=int(mid_edges), omega_mid=om_mid,
                omega_seg=om_seg, chi_seg=chi_seg, kappa=kappa, kappa_exact=exact,
                kappa_search=kappa_search, kappa_ub=min(kappa_search, L_var),
                L_var=L_var, L_static=L_static,
                qp_calls=len(cache), border=border[0],
                classes=[len(C) for C in best_part[0]])


if __name__ == "__main__":
    N = int(sys.argv[1]); seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    rhos = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [1, 2, 4, 8, 16, 32]
    betas = [float(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else [1.0, 2.0]
    for beta in betas:
        for rho in rhos:
            for s in range(seeds):
                r = analyse(N, beta, rho, 7919 * s + int(100 * rho) + int(10 * beta) + N)
                if r["kappa_exact"]:
                    chain = (r["omega_mid"] <= r["omega_seg"] <= r["chi_seg"] <= r["kappa"]
                             <= r["L_var"] <= r["L_static"])
                else:
                    chain = (r["omega_mid"] <= r["omega_seg"] <= r["chi_seg"] <= r["kappa_ub"]
                             <= r["L_var"] <= r["L_static"])
                r["chain_ok"] = bool(chain)
                print(json.dumps(r), flush=True)
