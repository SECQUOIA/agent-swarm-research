"""Brute-force check of Theorem 1 (midpoint-conflict bound) and of the
'robustness' remark on small convex integer least-squares instances.

Problem: min phi(x) = ||A x - y||^2, x integer in the box [0,m]^n, K = box.
Quantities (eps = 1e-6):
  omega_mid : clique number of the midpoint-conflict graph (a~b iff phi((a+b)/2) < OPT-eps)
  chi_mid   : chromatic number of that graph                    (n = 2 only)
  chi_seg   : chromatic number of the segment graph (a~b iff min_[a,b] phi < OPT-eps) (n = 2)
  part      : min number of classes I with min_{conv I} phi >= OPT-eps (exact, n = 2)
  L_var     : exact min #leaves over variable-branching trees (x_i <= c | x_i >= c+1, any c)
  L_obbt, N_obbt : same, but every node first applies OBBT with integer rounding using the
              incumbent UB = OPT (bounds of box ∩ {phi <= UB}); leaves / nodes of the min tree.
Theorem 1 predicts omega_mid <= chi_mid <= chi_seg <= part <= L_var.
The remark claims the bound also holds with OBBT; we test L_obbt >= omega_mid and the
corrected statement N_obbt >= omega_mid / (2n+1).
"""
import itertools, functools, math, sys, json
import numpy as np
from scipy.optimize import lsq_linear

EPS = 1e-6
TOL = 1e-9


def make_instance(rng, n, m, rows):
    A = rng.standard_normal((rows, n))
    t = rng.uniform(0.3, m - 0.3, n)
    y = A @ t + 0.3 * rng.standard_normal(rows)
    return A, y


def phi(A, y, x):
    r = A @ x - y
    return float(r @ r)


def box_min(A, y, lo, hi):
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    if np.any(lo > hi):
        return math.inf
    fixed = lo == hi
    if np.all(fixed):
        return phi(A, y, lo)
    # lsq_linear needs lo < hi strictly; handle fixed coordinates by substitution
    free = ~fixed
    yy = y - A[:, fixed] @ lo[fixed]
    r = lsq_linear(A[:, free], yy, bounds=(lo[free], hi[free]), method='bvls', tol=1e-12)
    return 2 * r.cost


def seg_min(A, y, a, b):
    ra = A @ a - y; Ad = A @ (b - a)
    den = Ad @ Ad
    tau = 0.0 if den == 0 else min(1.0, max(0.0, -(ra @ Ad) / den))
    r = ra + tau * Ad
    return float(r @ r)


def max_clique(adj):
    nv = len(adj); best = [0]
    nbr = [set(j for j in range(nv) if adj[i][j]) for i in range(nv)]

    def bk(R, P, X):
        if not P and not X:
            best[0] = max(best[0], len(R)); return
        if len(R) + len(P) <= best[0]:
            return
        u = max(P | X, key=lambda w: len(nbr[w] & P))
        for v in list(P - nbr[u]):
            bk(R | {v}, P & nbr[v], X & nbr[v]); P = P - {v}; X = X | {v}
    bk(set(), set(range(nv)), set())
    return best[0]


def min_partition(nv, ok):
    """ok(mask) -> bool, hereditary. Min number of ok classes covering all."""
    okm = [False] * (1 << nv)
    for mask in range(1, 1 << nv):
        if mask & (mask - 1) == 0:
            okm[mask] = True; continue
        # hereditary pruning
        good = True
        mm = mask
        while mm:
            b = mm & -mm; mm ^= b
            if not okm[mask ^ b]:
                good = False; break
        okm[mask] = good and ok(mask)
    INF = 10 ** 9
    f = [INF] * (1 << nv); f[0] = 0
    for rem in range(1, 1 << nv):
        low = rem & -rem
        sub = rem; best = INF
        while sub:
            if sub & low and okm[sub]:
                v = f[rem ^ sub] + 1
                if v < best:
                    best = v
            sub = (sub - 1) & rem
        f[rem] = best
    return f[(1 << nv) - 1]


def in_triangle(p, a, b, c):
    def cross(o, q, r):
        return (q[0] - o[0]) * (r[1] - o[1]) - (q[1] - o[1]) * (r[0] - o[0])
    d1, d2, d3 = cross(a, b, p), cross(b, c, p), cross(c, a, p)
    neg = d1 < -1e-12 or d2 < -1e-12 or d3 < -1e-12
    pos = d1 > 1e-12 or d2 > 1e-12 or d3 > 1e-12
    return not (neg and pos)


def run_instance(seed, n, m, rows, do_part):
    rng = np.random.default_rng(seed)
    A, y = make_instance(rng, n, m, rows)
    pts = [np.array(p, float) for p in itertools.product(range(m + 1), repeat=n)]
    vals = [phi(A, y, p) for p in pts]
    OPT = min(vals); thr = OPT - EPS
    nv = len(pts)
    adj_mid = [[i != j and phi(A, y, (pts[i] + pts[j]) / 2) < thr for j in range(nv)] for i in range(nv)]
    adj_seg = [[i != j and seg_min(A, y, pts[i], pts[j]) < thr for j in range(nv)] for i in range(nv)]
    for i in range(nv):
        for j in range(nv):
            assert not adj_mid[i][j] or adj_seg[i][j]
    omega = max_clique(adj_mid)
    out = dict(seed=seed, n=n, m=m, OPT=OPT, omega_mid=omega, omega_seg=max_clique(adj_seg))

    if do_part:
        xstar = np.linalg.lstsq(A, y, rcond=None)[0]
        glob = phi(A, y, xstar)

        def indep(adj):
            def ok(mask):
                idx = [i for i in range(nv) if mask >> i & 1]
                return all(not adj[i][j] for i, j in itertools.combinations(idx, 2))
            return ok

        def adm(mask):
            idx = [i for i in range(nv) if mask >> i & 1]
            if any(adj_seg[i][j] for i, j in itertools.combinations(idx, 2)):
                return False
            if glob >= thr or len(idx) < 3:
                return True
            # x* inside conv I  <=>  inside some triangle of I (Caratheodory, n = 2)
            for a, b, c in itertools.combinations(idx, 3):
                if in_triangle(xstar, pts[a], pts[b], pts[c]):
                    return False
            return True
        out['chi_mid'] = min_partition(nv, indep(adj_mid))
        out['chi_seg'] = min_partition(nv, indep(adj_seg))
        out['part'] = min_partition(nv, adm)

    # variable-branching DP over integer sub-boxes
    UB = OPT

    @functools.lru_cache(maxsize=None)
    def bound(lo, hi):
        return box_min(A, y, lo, hi)

    @functools.lru_cache(maxsize=None)
    def T(lo, hi):
        if bound(lo, hi) >= thr - TOL:
            return 1
        best = math.inf
        for i in range(n):
            for c in range(lo[i], hi[i]):
                h1 = list(hi); h1[i] = c
                l2 = list(lo); l2[i] = c + 1
                best = min(best, T(lo, tuple(h1)) + T(tuple(l2), hi))
        return best

    def obbt(lo, hi):
        """rounded OBBT on box ∩ {phi <= UB}: smallest/largest integer c such that
        the box restricted to x_i <= c (resp. >= c) still meets {phi <= UB}."""
        lo = list(lo); hi = list(hi)
        if bound(tuple(lo), tuple(hi)) > UB + TOL:
            return None
        for i in range(n):
            c = lo[i]
            while c < hi[i]:
                h = list(hi); h[i] = c
                if bound(tuple(lo), tuple(h)) <= UB + TOL:
                    break
                c += 1
            newlo = c
            c = hi[i]
            while c > newlo:
                l = list(lo); l[i] = c
                if bound(tuple(l), tuple(hi)) <= UB + TOL:
                    break
                c -= 1
            lo[i], hi[i] = newlo, c
        return tuple(lo), tuple(hi)

    @functools.lru_cache(maxsize=None)
    def TO(lo, hi):
        """returns (leaves, nodes) of a min-leaf tree with OBBT at every node"""
        r = obbt(lo, hi)
        if r is None:
            return (1, 1)
        lo, hi = r
        if bound(lo, hi) >= thr - TOL:
            return (1, 1)
        best = (math.inf, math.inf)
        for i in range(n):
            for c in range(lo[i], hi[i]):
                h1 = list(hi); h1[i] = c
                l2 = list(lo); l2[i] = c + 1
                a = TO(lo, tuple(h1)); b = TO(tuple(l2), hi)
                cand = (a[0] + b[0], a[1] + b[1] + 1)
                best = min(best, cand)
        return best
    root = (tuple([0] * n), tuple([m] * n))
    out['L_var'] = T(*root)
    out['L_obbt'], out['N_obbt'] = TO(*root)
    return out


if __name__ == '__main__':
    results = []
    configs = [(2, 2, 3, 60, True), (2, 3, 3, 40, False), (3, 2, 4, 40, False)]
    for n, m, rows, cnt, do_part in configs:
        if n == 2 and m == 3:
            do_part = False
        viol = dict(chain=0, obbt_leaves=0, obbt_nodes=0)
        rows_out = []
        for seed in range(cnt):
            r = run_instance(1000 * n + 100 * m + seed, n, m, rows, do_part)
            rows_out.append(r); results.append(r)
            chain = [r['omega_mid']] + ([r['chi_mid'], r['chi_seg'], r['part']] if do_part else []) + [r['L_var']]
            if any(a > b for a, b in zip(chain, chain[1:])):
                viol['chain'] += 1
                print("CHAIN VIOLATION", r)
            if r['L_obbt'] < r['omega_mid']:
                viol['obbt_leaves'] += 1
            if r['N_obbt'] * (2 * n + 1) < r['omega_mid']:
                viol['obbt_nodes'] += 1
        med = lambda key: float(np.median([r[key] for r in rows_out]))
        print("n=%d box=[0,%d]^%d: %d instances; chain violations=%d; "
              "instances with L_obbt < omega_mid: %d; with N_obbt < omega_mid/(2n+1): %d"
              % (n, m, n, cnt, viol['chain'], viol['obbt_leaves'], viol['obbt_nodes']))
        keys = ['omega_mid', 'omega_seg'] + (['chi_mid', 'chi_seg', 'part'] if do_part else []) + ['L_var', 'L_obbt', 'N_obbt']
        print("   medians: " + ", ".join("%s=%g" % (k, med(k)) for k in keys))
        if do_part:
            strict = sum(r['part'] > r['chi_mid'] for r in rows_out)
            tight = sum(r['part'] == r['L_var'] for r in rows_out)
            print("   part > chi_mid in %d; part == L_var in %d; omega_seg > omega_mid in %d"
                  % (strict, tight, sum(r['omega_seg'] > r['omega_mid'] for r in rows_out)))
        ex = [r for r in rows_out if r['L_obbt'] < r['omega_mid']][:3]
        for r in ex:
            print("   example (OBBT beats leaf bound):", {k: r[k] for k in ('seed', 'omega_mid', 'L_var', 'L_obbt', 'N_obbt')})
        sys.stdout.flush()
    with open('thm1_bruteforce.jsonl', 'w') as f:
        for r in results:
            f.write(json.dumps(r) + '\n')
