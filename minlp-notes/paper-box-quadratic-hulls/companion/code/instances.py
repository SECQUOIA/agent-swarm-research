"""Instance generation and file writers.

Random sparse 'plus' instances (min form  x'Hx + g'x  over [0,1]^n):
  graph  random k-tree: start from a (k+1)-clique, then attach each new node to
         a uniformly random existing k-clique (k = 2 gives a 2-tree in which every
         edge lies in a triangle and every maximal clique is a triangle).
  H_ii   integer uniform in [1, dmax] with probability pplus (a 'plus loop' in
         Khajavirad's terminology: positive diagonal in the minimization form),
         otherwise integer uniform in [-dmax, -1].
  H_ij   for edges, integer uniform in [-omax, omax] (zero allowed, as in spar).
  g_i    integer uniform in [-50, 50].
All data are integers, so instances are exactly reproducible from (n, k, pplus, seed).
"""

import itertools
import json
import numpy as np


def ktree(n, k, rng):
    edges = set()
    cliques = [tuple(range(k + 1))]
    for a, b in itertools.combinations(range(k + 1), 2):
        edges.add((a, b))
    kcliques = [c for c in itertools.combinations(range(k + 1), k)]
    for v in range(k + 1, n):
        base = kcliques[rng.integers(len(kcliques))]
        for u in base:
            edges.add((min(u, v), max(u, v)))
        cliques.append(tuple(sorted(base + (v,))))
        for sub in itertools.combinations(base, k - 1):
            kcliques.append(tuple(sorted(sub + (v,))))
    return sorted(edges), cliques


def plus_instance(n, k=2, pplus=1.0, seed=0, dmax=50, omax=50):
    rng = np.random.default_rng(seed)
    edges, cliques = ktree(n, k, rng)
    H = np.zeros((n, n))
    for i in range(n):
        if rng.random() < pplus:
            H[i, i] = rng.integers(1, dmax + 1)
        else:
            H[i, i] = -rng.integers(1, dmax + 1)
    for (i, j) in edges:
        H[i, j] = H[j, i] = rng.integers(-omax, omax + 1)
    g = rng.integers(-50, 51, size=n).astype(float)
    return H, g, edges, cliques


def write_lp(path, H, g, name='boxqp'):
    """Gurobi/SCIP LP format, min x'Hx + g'x, 0 <= x <= 1."""
    n = len(g)
    lin = ' '.join('%+.17g x%d' % (g[i], i) for i in range(n) if g[i])
    quad = []
    for i in range(n):
        if H[i, i]:
            quad.append('%+.17g x%d ^ 2' % (2 * H[i, i], i))
        for j in range(i + 1, n):
            if H[i, j]:
                quad.append('%+.17g x%d * x%d' % (4 * H[i, j], i, j))
    with open(path, 'w') as f:
        f.write('\\ %s\nMinimize\n obj: %s + [ %s ] / 2\nSubject To\nBounds\n' % (name, lin or '0 x0', ' '.join(quad)))
        for i in range(n):
            f.write(' 0 <= x%d <= 1\n' % i)
        f.write('End\n')


def save_json(path, H, g, meta):
    n = len(g)
    I, J = np.nonzero(np.triu(H))   # same entries and order as the former double loop
    data = {'n': n, 'g': [float(v) for v in g],
            'H': [[int(i), int(j), float(H[i, j])] for i, j in zip(I, J)], 'meta': meta}
    json.dump(data, open(path, 'w'))


def load_json(path):
    d = json.load(open(path))
    n = d['n']
    H = np.zeros((n, n))
    for i, j, v in d['H']:
        H[i, j] = H[j, i] = v
    return H, np.array(d['g']), d['meta']


def load_pool(paths, kind=None):
    """Hard three-variable objectives (H, g) from n3_hard.py logs."""
    pool = []
    for p in paths:
        for line in open(p):
            r = json.loads(line)
            if kind and r['kind'] != kind:
                continue
            pool.append((np.array(r['H']), np.array(r['g'])))
    return pool


def hard_triangle_instance(n, pool, k=2, seed=0, noise=0.02):
    """Random k-tree; every triangle inside a maximal clique receives a randomly
    weighted (w ~ U[0.5,1.5]) and randomly permuted hard objective from the pool;
    then Gaussian noise of relative size `noise` is added to every edge, diagonal
    and linear coefficient (the support stays inside the k-tree)."""
    rng = np.random.default_rng(seed)
    edges, cliques = ktree(n, k, rng)
    H = np.zeros((n, n))
    g = np.zeros(n)
    tris = sorted({t for c in cliques for t in itertools.combinations(sorted(c), 3)})
    for T in tris:
        Hp, gp = pool[rng.integers(len(pool))]
        perm = rng.permutation(3)
        w = rng.uniform(0.5, 1.5)
        idx = [T[p] for p in perm]
        for a in range(3):
            g[idx[a]] += w * gp[a]
            for b in range(3):
                H[idx[a], idx[b]] += w * Hp[a, b]
    scale = np.abs(H).max()
    for (i, j) in edges:
        e = noise * scale * rng.normal()
        H[i, j] += e
        H[j, i] += e
    H[np.diag_indices(n)] += noise * scale * rng.normal(size=n)
    g += noise * scale * rng.normal(size=n)
    # round to 6 significant decimals so that the LP file and the relaxation use identical data
    H = np.round(H, 6)
    g = np.round(g, 6)
    return H, g, edges, cliques


def chain_instance(m, pool, eta=0.1, nu=0.01, seed=0, tree='path'):
    """m disjoint triangles (n = 3m), triangle t on nodes 3t..3t+2 carries a randomly
    weighted (w ~ U[0.5,1.5]) and permuted pool objective with relative coefficient
    noise nu; consecutive triangles (tree='path') or a random tree of triangles
    (tree='random') are joined by one bridge edge between random end nodes with
    weight eta * s * N(0,1), where s is the mean absolute off-diagonal pool coefficient.
    The graph is chordal; maximal cliques are the triangles and the bridges."""
    rng = np.random.default_rng(seed)
    n = 3 * m
    H = np.zeros((n, n))
    g = np.zeros(n)
    s = np.mean([np.abs(Hp[np.triu_indices(3, 1)]).mean() for Hp, _ in pool])
    cliques = []
    for t in range(m):
        Hp, gp = pool[rng.integers(len(pool))]
        perm = rng.permutation(3)
        w = rng.uniform(0.5, 1.5)
        idx = [3 * t + p for p in perm]
        for a in range(3):
            g[idx[a]] += w * gp[a] * (1 + nu * rng.normal())
            for b in range(a, 3):
                v = w * Hp[a, b] * (1 + nu * rng.normal())
                H[idx[a], idx[b]] += v
                if a != b:
                    H[idx[b], idx[a]] += v
        cliques.append((3 * t, 3 * t + 1, 3 * t + 2))
    for t in range(1, m):
        parent = t - 1 if tree == 'path' else int(rng.integers(t))
        u = 3 * parent + int(rng.integers(3))
        v = 3 * t + int(rng.integers(3))
        e = eta * s * rng.normal()
        H[u, v] += e
        H[v, u] += e
        cliques.append((min(u, v), max(u, v)))
    H = np.round(H, 6)
    g = np.round(g, 6)
    return H, g, cliques


def cactus_instance(m, pool, nu=0.01, seed=0):
    """m hard triangles that share vertices: triangle 0 is on nodes 0,1,2; triangle t >= 1
    consists of one node of a uniformly random earlier triangle and two new nodes
    (n = 2m + 1).  Each triangle carries a randomly weighted (w ~ U[0.5,1.5]) and permuted
    pool objective with relative coefficient noise nu; objectives add on shared nodes.
    The graph is chordal (a cactus of triangles); its maximal cliques are the triangles."""
    rng = np.random.default_rng(seed)
    n = 2 * m + 1
    H = np.zeros((n, n))
    g = np.zeros(n)
    cliques = [(0, 1, 2)]
    nxt = 3
    for t in range(1, m):
        par = cliques[int(rng.integers(t))]
        cliques.append((int(par[int(rng.integers(3))]), nxt, nxt + 1))
        nxt += 2
    for c in cliques:
        Hp, gp = pool[rng.integers(len(pool))]
        perm = rng.permutation(3)
        w = rng.uniform(0.5, 1.5)
        idx = [c[p] for p in perm]
        for a in range(3):
            g[idx[a]] += w * gp[a] * (1 + nu * rng.normal())
            for b in range(a, 3):
                v = w * Hp[a, b] * (1 + nu * rng.normal())
                H[idx[a], idx[b]] += v
                if a != b:
                    H[idx[b], idx[a]] += v
    H = np.round(H, 6)
    g = np.round(g, 6)
    return H, g, [tuple(sorted(c)) for c in cliques]
