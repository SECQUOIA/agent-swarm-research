#!/usr/bin/env python3
"""Finite demonstration for Theorem (balanced box quadratics without a width parameter).

The report's reference solver (research-20261002-decomposition/solver/certified_grid.py) is
imported read-only.  Its tree-DP grid oracle `grid_dp` is replaced *in memory* by an exact
minimum-cut oracle (threshold encoding of the grids, Lemma lit:lem:chaincut), and the unchanged
capped corrected-grid algorithm is run on dense balanced quadratics given with ONE bag containing
all variables (so tree DP would need prod_i |G_i| table entries).  For each instance we check, in
exact rational arithmetic,
  * certified lower <= true optimum <= certified upper, and upper = F(returned point);
  * gap <= epsilon when the run reports 'certified';
where the true optimum is computed independently by enumerating all 3^n faces and solving the
nonsingular stationarity systems (a minimum-dimensional optimal face has a nonsingular free
Hessian, so this enumeration is complete).
No research file is modified.  Finite checks support, but do not replace, the proof.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys, random, time
from fractions import Fraction as F
from itertools import product
from collections import deque

SOLVER = (_PUBLIC_REPO + '/research-20261002-decomposition/solver')
sys.path.insert(0, SOLVER)
import certified_grid as cg  # noqa: E402


def maxflow(cap, s, t):
    flow = F(0)
    while True:
        par = {s: None}
        q = deque([s])
        while q and t not in par:
            u = q.popleft()
            for v, c in cap[u].items():
                if c > 0 and v not in par:
                    par[v] = u
                    q.append(v)
        if t not in par:
            return flow, set(par)
        v, b = t, None
        while par[v] is not None:
            u = par[v]
            b = cap[u][v] if b is None else min(b, cap[u][v])
            v = u
        v = t
        while par[v] is not None:
            u = par[v]
            cap[u][v] -= b
            cap[v][u] = cap[v].get(u, F(0)) + b
            v = u
        flow += b


def balance_signs(n, pairs):
    sig = [0] * n
    adj = [[] for _ in range(n)]
    for i, j, a in pairs:
        rel = -1 if a > 0 else 1
        adj[i].append((j, rel)); adj[j].append((i, rel))
    for r in range(n):
        if sig[r]:
            continue
        sig[r] = 1
        q = [r]
        for u in q:
            for v, rel in adj[u]:
                if not sig[v]:
                    sig[v] = sig[u] * rel; q.append(v)
                elif sig[v] != sig[u] * rel:
                    raise ValueError("not balanced")
    return sig


def cut_min(unary, pairs, grids, sig):
    """min over prod grids of sum_i unary[i][k_i] + sum (i,j,a) a*y_i*y_j  (sign(a) sig_i sig_j <= 0)."""
    n = len(grids)
    order = [list(range(len(g))) if sig[i] > 0 else list(range(len(g)))[::-1] for i, g in enumerate(grids)]
    K = F(0); h = {}; w = {}
    for i in range(n):
        o = order[i]
        K += unary[i][o[0]]
        for l in range(1, len(o)):
            h[(i, l)] = h.get((i, l), F(0)) + unary[i][o[l]] - unary[i][o[l - 1]]
    for i, j, a in pairs:
        gi = [grids[i][k] for k in order[i]]; gj = [grids[j][k] for k in order[j]]
        K += a * gi[0] * gj[0]
        for l in range(1, len(gj)):
            h[(j, l)] = h.get((j, l), F(0)) + a * gi[0] * (gj[l] - gj[l - 1])
        for k in range(1, len(gi)):
            h[(i, k)] = h.get((i, k), F(0)) + a * gj[0] * (gi[k] - gi[k - 1])
            for l in range(1, len(gj)):
                c = a * (gi[k] - gi[k - 1]) * (gj[l] - gj[l - 1])
                assert c <= 0
                if c:
                    w[((i, k), (j, l))] = c
    nodes = list(h)
    p = dict(h)
    for (x, y), c in w.items():
        p[x] += c / 2; p[y] += c / 2
    cap = {x: {} for x in nodes + ['S', 'T']}
    for x in nodes:
        if p[x] > 0: cap[x]['T'] = p[x]
        elif p[x] < 0: cap['S'][x] = -p[x]
    for (x, y), c in w.items():
        cap[x][y] = cap[x].get(y, F(0)) - c / 2
        cap[y][x] = cap[y].get(x, F(0)) - c / 2
    big = 1 + sum(abs(v) for v in p.values()) + sum(abs(v) for v in w.values())
    for i in range(n):
        for l in range(1, len(grids[i]) - 1):
            cap[(i, l + 1)][(i, l)] = cap[(i, l + 1)].get((i, l), F(0)) + big
    f, src = maxflow(cap, 'S', 'T')
    idx = []
    for i in range(n):
        pos = max([l for l in range(1, len(grids[i])) if (i, l) in src], default=0)
        idx.append(order[i][pos])
    return K + sum(min(F(0), v) for v in p.values()) + f, idx


def cut_grid_dp(problem, grids, penalties, budget=None, max_table_states=None):
    n = len(grids)
    sig = balance_signs(n, problem.interactions)
    unary = [[problem.A[i][i] * x * x / 2 + problem.b[i] * x - d for x, d in zip(grids[i], penalties[i])]
             for i in range(n)]
    unary[0] = [u + problem.constant for u in unary[0]]
    pairs = list(problem.interactions)
    lower, idx = cut_min(unary, pairs, grids, sig)
    point = tuple(grids[i][k] for i, k in enumerate(idx))
    marg = []
    for i in range(n):
        row = []
        for k in range(len(grids[i])):
            g2 = [grids[j] if j != i else (grids[i][k],) for j in range(n)]
            u2 = [unary[j] if j != i else [unary[i][k]] for j in range(n)]
            v, _ = cut_min(u2, pairs, g2, sig)
            row.append(v)
        marg.append(tuple(row))
    assert min(marg[0]) == lower
    return {"lower": lower, "point": point, "marginals": marg, "messages": {},
            "table_states": sum(len(g) for g in grids)}


def true_optimum(A, b, bounds, const):
    n = len(b)
    best = None
    for pat in product(range(3), repeat=n):
        x = [None] * n
        free = []
        for i, t in enumerate(pat):
            if t == 0: x[i] = bounds[i][0]
            elif t == 1: x[i] = bounds[i][1]
            else: free.append(i)
        if free:
            M = [[A[i][j] for j in free] + [-(b[i] + sum(A[i][j] * x[j] for j in range(n) if x[j] is not None))]
                 for i in free]
            m = len(free); ok = True
            for c in range(m):
                piv = next((r for r in range(c, m) if M[r][c] != 0), None)
                if piv is None: ok = False; break
                M[c], M[piv] = M[piv], M[c]
                for r in range(m):
                    if r != c and M[r][c] != 0:
                        f = M[r][c] / M[c][c]
                        M[r] = [a - f * bb for a, bb in zip(M[r], M[c])]
            if not ok: continue
            for c, i in enumerate(free):
                x[i] = M[c][m] / M[c][c]
            if any(not (bounds[i][0] <= x[i] <= bounds[i][1]) for i in free): continue
        val = const + sum(A[i][i] * x[i] ** 2 / 2 + b[i] * x[i] for i in range(n)) + \
            sum(A[i][j] * x[i] * x[j] for i in range(n) for j in range(i + 1, n))
        best = val if best is None or val < best else best
    return best


def instance(seed, n, mode="strong"):
    random.seed(seed)
    if mode == "mild":   # larger diagonals, smaller couplings: interior optima, still indefinite
        sig = [random.choice([-1, 1]) for _ in range(n)]
        A = [[F(0)] * n for _ in range(n)]
        for i in range(n):
            A[i][i] = F(random.randint(6, 12))
            for j in range(i + 1, n):
                A[i][j] = A[j][i] = -sig[i] * sig[j] * F(random.randint(2, 9), 2)
        b = [F(random.randint(-30, 30), 4) for _ in range(n)]
        return A, b, [(F(0), F(1)) for _ in range(n)]
    sig = [random.choice([-1, 1]) for _ in range(n)]
    A = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = F(random.randint(1, 4))                     # positive diagonals: not the endpoint case
        for j in range(i + 1, n):
            A[i][j] = A[j][i] = -sig[i] * sig[j] * F(random.randint(2, 12), 2)  # dense, balanced
    b = [F(random.randint(-12, 12), 3) for _ in range(n)]
    bounds = [(F(0), F(1)) for _ in range(n)]
    return A, b, bounds


def min_eig_sign(A):
    """Smallest Hessian eigenvalue (floating point, for reporting only)."""
    import numpy as np
    return float(np.linalg.eigvalsh(np.array([[float(v) for v in row] for row in A])).min())


if __name__ == '__main__':
    cg.grid_dp = cut_grid_dp           # in-memory replacement of the oracle only
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    mode = sys.argv[3] if len(sys.argv) > 3 else "strong"
    eps = F(1, 10 ** 6)
    t0 = time.time(); done = 0
    for seed in range(N):
        A, b, bounds = instance(seed, n, mode)
        prob = cg.BoxQP(A=A, b=b, bounds=bounds, integers=(), bags=[list(range(n))], edges=[])
        cert = cg.solve(prob, epsilon=eps, max_stages=200, time_limit=60.0, convex_presolve=False,
                        polish_sweeps=0, max_table_states=10 ** 9)
        opt = true_optimum(A, b, bounds, F(0))
        lo, up = F(cert["lower"]), F(cert["upper"])
        pt = tuple(F(v) for v in cert["point"])
        assert lo <= opt <= up, (seed, lo, opt, up)
        assert prob.value(pt) == up
        if cert["status"] == "certified":
            assert up - lo <= eps
        sizes = [max(len(g) for g in st["grids"]) for st in cert["stages"]]
        print(f"[{mode}] seed {seed}: n={n} dense single bag, lambda_min={min_eig_sign(A):.2f}, status={cert['status']}, "
              f"stages={len(cert['stages'])}, max labels/coord={max(sizes)}, "
              f"product of grid sizes at last stage={__import__('math').prod(len(g) for g in cert['stages'][-1]['grids'])}, "
              f"gap={float(up - lo):.2e}, upper-opt={float(up - opt):.2e}")
        done += 1
    print(f"PASS: {done} dense balanced instances; certified enclosures contain the face-enumeration optimum "
          f"({time.time() - t0:.1f}s).")
