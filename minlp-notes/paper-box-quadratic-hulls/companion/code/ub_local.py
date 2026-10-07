"""Heuristic upper bounds (feasible points) for sparse box QPs given with clique lists.

Block coordinate descent over three-variable blocks: each block subproblem (three
variables, others fixed) is a box QP in three variables, solved exactly by
enumerating stationary points on all 27 faces of the cube.  Multi-start from random
points (and optionally from a relaxation point).  The best value is a valid upper
bound on the global minimum: it is f evaluated in floating point at a feasible point
(re-evaluated from scratch at the end of every start).
Blocks: the triangle cliques in file order, then all 3-subsets of larger cliques.
Version 2 (2026-10-02, second author): H is stored as a sparse matrix and the
product Hx is updated incrementally, so a sweep costs O(nnz) instead of O(n^2) per
block; the best value so far is printed after every start.  Same search as version 1
(same random numbers, same acceptance rule up to floating-point rounding of the
value differences).
Usage: python ub_local.py instance.json nstarts seed [start.npz]
(start 0 uses the relaxation point 'x' from start.npz when given)"""
import itertools
import json
import sys

import numpy as np
import scipy.sparse as sp

sys.path.insert(0, '.')

FACES = list(itertools.product((-1, 0, 1), repeat=3))   # -1 free, 0/1 fixed


def box3_min(Hb, gb):
    """Exact min of v'Hb v + gb'v over [0,1]^3 (Hb symmetric 3x3)."""
    best, bestv = np.inf, None
    for face in FACES:
        free = [i for i in range(3) if face[i] == -1]
        v = np.array([0.0 if f == -1 else float(f) for f in face])
        if free:
            fixed = [i for i in range(3) if face[i] != -1]
            A = 2 * Hb[np.ix_(free, free)]
            rhs = -(gb[free] + 2 * Hb[np.ix_(free, fixed)] @ v[fixed])
            if abs(np.linalg.det(A)) < 1e-12:
                continue
            sol = np.linalg.solve(A, rhs)
            if (sol < -1e-12).any() or (sol > 1 + 1e-12).any():
                continue
            v[free] = np.clip(sol, 0, 1)
        val = v @ Hb @ v + gb @ v
        if val < best:
            best, bestv = val, v.copy()
    return best, bestv


def load(path):
    d = json.load(open(path))
    n = d['n']
    I, J, V = [], [], []
    for i, j, v in d['H']:
        I.append(i); J.append(j); V.append(v)
        if i != j:
            I.append(j); J.append(i); V.append(v)
    H = sp.csr_matrix((V, (I, J)), shape=(n, n))
    return H, np.array(d['g']), d['meta']


def f(H, g, x):
    return float(x @ (H @ x) + g @ x)


def bcd(H, Hc, g, blocks, Hbs, x, rng, sweeps=200):
    Hx = H @ x
    for _ in range(sweeps):
        improved = False
        for b in rng.permutation(len(blocks)):
            idx = blocks[b]
            Hb = Hbs[b]
            old = x[idx].copy()
            gb = g[idx] + 2 * (Hx[idx] - Hb @ old)
            val, v = box3_min(Hb, gb)
            oldval = old @ Hb @ old + gb @ old
            if val < oldval - 1e-12:
                x[idx] = v
                Hx += Hc[:, idx] @ (v - old)
                improved = True
        if not improved:
            break
    return f(H, g, x), x


def main():
    path, ns, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    H, g, meta = load(path)
    Hc = H.tocsc()
    blocks = [tuple(c) for c in meta['cliques'] if len(c) == 3]
    blocks += sorted({t for c in meta['cliques'] if len(c) > 3 for t in itertools.combinations(sorted(c), 3)})
    blocks = [list(b) for b in blocks]
    Hbs = [H[b][:, b].toarray() for b in blocks]
    x0 = None
    if len(sys.argv) > 4:
        x0 = np.clip(np.load(sys.argv[4])['x'], 0, 1)
    rng = np.random.default_rng(seed)
    best = np.inf
    for s in range(ns):
        x = rng.random(len(g)) if s % 2 == 0 else rng.integers(0, 2, len(g)).astype(float)
        if x0 is not None and s == 0:
            x = x0.copy()
        val, x = bcd(H, Hc, g, blocks, Hbs, x, rng)
        best = min(best, val)
        print(json.dumps({'instance': path, 'starts': s + 1, 'seed': seed, 'ub': best}), flush=True)


if __name__ == '__main__':
    main()
