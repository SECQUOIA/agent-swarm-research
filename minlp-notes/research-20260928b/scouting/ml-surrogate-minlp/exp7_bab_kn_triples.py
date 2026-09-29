"""Experiment 7: same BaB as experiment 4, but every node LP also contains the
3-input multi-neuron inequalities d_ij + d_jk + d_ik <= 2 and d_ij <= d_ik + d_kj
(d_ij = p_ij + q_ij), which are valid on the graph of the hidden layer."""
import itertools, sys
import numpy as np
from scipy.optimize import linprog

def closure(n, arcs):
    R = np.zeros((n, n), dtype=bool)
    for i in range(n): R[i, i] = True
    for (i, j) in arcs: R[i, j] = True
    for k in range(n):
        R |= np.outer(R[:, k], R[k, :])
    return R

def node_lp_metric(n, arcs):
    pairs = list(itertools.combinations(range(n), 2)); pid = {p: k for k, p in enumerate(pairs)}
    R = closure(n, arcs)
    nv = n + 2 * len(pairs)
    c = np.zeros(nv); c[n:] = -1.0
    A, bvec = [], []
    def row(): return np.zeros(nv)
    for (i, j) in arcs:
        r = row(); r[j] = 1; r[i] = -1; A.append(r); bvec.append(0)
    bounds = [(0, 1)] * n
    for k, (i, j) in enumerate(pairs):
        p, q = n + 2 * k, n + 2 * k + 1
        if R[i, j]:
            bounds += [(None, None), (0, 0)]
            for s in (1, -1):
                r = row(); r[p] = s; r[i] = -s; r[j] = s; A.append(r); bvec.append(0)
        elif R[j, i]:
            bounds += [(0, 0), (None, None)]
            for s in (1, -1):
                r = row(); r[q] = s; r[j] = -s; r[i] = s; A.append(r); bvec.append(0)
        else:
            bounds += [(0, None), (0, None)]
            for var, s in ((p, 1), (q, -1)):
                r = row(); r[var] = -1; r[i] += s; r[j] -= s; A.append(r); bvec.append(0)
                r = row(); r[var] = 1; r[i] -= s / 2; r[j] += s / 2; A.append(r); bvec.append(0.5)
    def d(r, a, b, coef):
        k = pid[(min(a, b), max(a, b))]; r[n + 2 * k] += coef; r[n + 2 * k + 1] += coef
    for (i, j, k) in itertools.combinations(range(n), 3):
        r = row(); d(r, i, j, 1); d(r, j, k, 1); d(r, i, k, 1); A.append(r); bvec.append(2)
        for (a, b, m) in ((i, j, k), (j, k, i), (i, k, j)):
            r = row(); d(r, a, b, 1); d(r, a, m, -1); d(r, m, b, -1); A.append(r); bvec.append(0)
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(bvec), bounds=bounds, method="highs")
    assert res.status == 0, res.message
    return -res.fun, R

def bab(n, theta):
    stack = [[]]; nodes = leaves = 0
    while stack:
        arcs = stack.pop(); nodes += 1
        val, R = node_lp_metric(n, arcs)
        if val <= theta + 1e-7:
            leaves += 1; continue
        best = None
        for (i, j) in itertools.combinations(range(n), 2):
            if R[i, j] or R[j, i]: continue
            score = min(closure(n, arcs + [(i, j)]).sum(), closure(n, arcs + [(j, i)]).sum())
            if best is None or score > best[0]: best = (score, i, j)
        _, i, j = best
        stack.append(arcs + [(i, j)]); stack.append(arcs + [(j, i)])
    return nodes, leaves

print("n  theta=OPT  root_LP(triangle+3-input cuts)  nodes  leaves")
for n in range(3, int(sys.argv[1]) + 1):
    opt = n * n // 4
    root, _ = node_lp_metric(n, [])
    nodes, leaves = bab(n, opt)
    print(f"{n}  {opt:9d}  {root:30.3f}  {nodes:5d}  {leaves:6d}"); sys.stdout.flush()
