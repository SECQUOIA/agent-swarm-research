#!/usr/bin/env python3
"""Exact finite check for the lit-ext development: a balanced (switch-submodular)
quadratic restricted to arbitrary finite coordinate grids, plus arbitrary unary
terms (e.g. the negative interpolation corrections), is minimized exactly by one
s-t minimum cut on the threshold (chain) encoding.

For random small instances we compare
  * brute-force minimum over the grid product, and
  * K + sum_a min(0,p_a) + mincut  (identity of the paper's cut construction),
and we check that the cut assignment decodes to a grid point with that value.
We also check min-marginals (fixing one coordinate) the same way.
All arithmetic is exact (fractions.Fraction).  Finite checks support, but do
not replace, the proof in lit-ext-proofs.tex.
"""
from fractions import Fraction as Fr
from itertools import product
from collections import deque
import random, sys

def maxflow(cap, s, t):
    """Edmonds-Karp on dict-of-dict residual capacities (exact). Returns (value, source-side set)."""
    flow = Fr(0)
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
        # bottleneck
        v, b = t, None
        while par[v] is not None:
            u = par[v]
            b = cap[u][v] if b is None else min(b, cap[u][v])
            v = u
        v = t
        while par[v] is not None:
            u = par[v]
            cap[u][v] -= b
            cap[v].setdefault(u, Fr(0))
            cap[v][u] += b
            v = u
        flow += b

def build_and_solve(Q, c, grids, s, unary_extra, fixed=None):
    """Minimize F(x)=x'Qx+c'x+sum_i unary_extra[i][x_i] over prod grids (x_i fixed if given)."""
    n = len(grids)
    chains = []
    for i in range(n):
        g = sorted(grids[i]) if s[i] > 0 else sorted(grids[i], reverse=True)
        if fixed is not None and i in fixed:
            g = [fixed[i]]
        chains.append(g)
    phi = lambda i, v: Q[i][i] * v * v + c[i] * v + unary_extra[i][v]
    K = Fr(0)
    h = {}      # linear coefficients of y-variables
    w = {}      # pair coefficients (a,b) with a<b
    for i in range(n):
        g = chains[i]
        K += phi(i, g[0])
        for k in range(1, len(g)):
            h[(i, k)] = h.get((i, k), Fr(0)) + phi(i, g[k]) - phi(i, g[k - 1])
    for i in range(n):
        for j in range(i + 1, n):
            if Q[i][j] == 0:
                continue
            a, b = chains[i], chains[j]
            coef = 2 * Q[i][j]
            K += coef * a[0] * b[0]
            for l in range(1, len(b)):
                h[(j, l)] = h.get((j, l), Fr(0)) + coef * a[0] * (b[l] - b[l - 1])
            for k in range(1, len(a)):
                h[(i, k)] = h.get((i, k), Fr(0)) + coef * b[0] * (a[k] - a[k - 1])
            for k in range(1, len(a)):
                for l in range(1, len(b)):
                    wkl = coef * (a[k] - a[k - 1]) * (b[l] - b[l - 1])
                    assert wkl <= 0, "balance violated"
                    w[((i, k), (j, l))] = wkl
    nodes = list(h.keys())
    p = {a: h[a] for a in nodes}
    for (a, b), val in w.items():
        p[a] += val / 2
        p[b] += val / 2
    cap = {x: {} for x in nodes + ['S', 'T']}
    for a in nodes:
        if p[a] > 0:
            cap[a]['T'] = cap[a].get('T', Fr(0)) + p[a]
        elif p[a] < 0:
            cap['S'][a] = cap['S'].get(a, Fr(0)) - p[a]
    for (a, b), val in w.items():
        r = -val / 2
        cap[a][b] = cap[a].get(b, Fr(0)) + r
        cap[b][a] = cap[b].get(a, Fr(0)) + r
    big = 1 + sum(abs(v) for v in p.values()) + sum(abs(v) for v in w.values())
    for i in range(n):
        for k in range(1, len(chains[i]) - 1):
            # y_{i,k+1} <= y_{i,k}: arc (i,k+1)->(i,k) of "infinite" capacity
            cap[(i, k + 1)][(i, k)] = cap[(i, k + 1)].get((i, k), Fr(0)) + big
    const = K + sum(min(Fr(0), v) for v in p.values())
    f, src = maxflow(cap, 'S', 'T')
    # decode: y_a = 1 iff a on source side
    x = []
    for i in range(n):
        pos = 0
        for k in range(1, len(chains[i])):
            if (i, k) in src:
                pos = k
        # monotonicity check of decoded y
        ys = [(i, k) in src for k in range(1, len(chains[i]))]
        assert all(ys[k] >= ys[k + 1] for k in range(len(ys) - 1)), "nonmonotone cut"
        x.append(chains[i][pos])
    return const + f, x

def F(Q, c, unary_extra, x):
    n = len(x)
    return sum(Q[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) + \
        sum(c[i] * x[i] for i in range(n)) + sum(unary_extra[i][x[i]] for i in range(n))

def rand_frac(lo, hi, den=6):
    return Fr(random.randint(lo * den, hi * den), den)

def trial(rng_seed):
    random.seed(rng_seed)
    n = random.randint(2, 5)
    s = [random.choice([-1, 1]) for _ in range(n)]
    Q = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        Q[i][i] = rand_frac(-3, 3)
        for j in range(i + 1, n):
            if random.random() < 0.7:
                mag = Fr(random.randint(1, 12), 4)
                Q[i][j] = Q[j][i] = -s[i] * s[j] * mag   # balanced: s_i s_j Q_ij <= 0
    c = [rand_frac(-4, 4) for _ in range(n)]
    grids, unary = [], []
    for i in range(n):
        lo = Fr(random.randint(-4, 0), 2)
        hi = lo + Fr(random.randint(1, 6), 2)
        pts = {lo, hi} | {lo + (hi - lo) * Fr(random.randint(1, 11), 12) for _ in range(random.randint(0, 3))}
        grids.append(sorted(pts))
        unary.append({v: rand_frac(-2, 0, 8) for v in pts})   # arbitrary unary, e.g. -corrections
    brute = min(F(Q, c, unary, list(x)) for x in product(*grids))
    val, x = build_and_solve(Q, c, grids, s, unary)
    assert val == brute, (rng_seed, val, brute)
    assert F(Q, c, unary, x) == brute, (rng_seed, x)
    # min-marginals of one random coordinate
    i = random.randrange(n)
    for v in grids[i]:
        bm = min(F(Q, c, unary, list(x)) for x in product(*grids) if x[i] == v)
        vm, xm = build_and_solve(Q, c, grids, s, unary, fixed={i: v})
        assert vm == bm and F(Q, c, unary, xm) == bm and xm[i] == v, (rng_seed, i, v)
    return n, sum(len(g) for g in grids)

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    tot = 0
    for seed in range(N):
        n, m = trial(seed)
        tot += m
    print(f"PASS: {N} random balanced instances (n<=5, nonuniform grids, arbitrary unary terms); "
          f"grid minimum and all min-marginals of one coordinate per instance equal brute force; "
          f"total grid labels {tot}.")
