"""Experiment 4: ReLU-splitting branch and bound with triangle LP bounds on the
max-cut network f(x) = sum_{i<j} |x_i - x_j| = sum ReLU(x_i-x_j) + ReLU(x_j-x_i),
x in [0,1]^n (complete graph).  max f = floor(n^2/4).

Each node fixes the sign of some differences x_i - x_j (arcs).  A pair is resolved
when the sign is implied by the transitive closure of the arcs; resolved neurons
are modeled exactly, unresolved ones by the triangle relaxation with the exact
pre-activation bounds [-1, 1].  We certify f <= floor(n^2/4) (exact) or
f <= (1+delta) floor(n^2/4), and count nodes; we also check the lemma
LP(node) >= #unresolved pairs at every node.
"""
import itertools, sys
import numpy as np
from scipy.optimize import linprog

def closure(n, arcs):
    R = np.zeros((n, n), dtype=bool)  # R[i,j]: x_i >= x_j implied
    for i in range(n): R[i, i] = True
    for (i, j) in arcs: R[i, j] = True
    for k in range(n):
        R |= np.outer(R[:, k], R[k, :])
    return R

def node_lp(n, arcs):
    pairs = list(itertools.combinations(range(n), 2))
    R = closure(n, arcs)
    nv = n + 2 * len(pairs)
    c = np.zeros(nv); c[n:] = -1.0
    A, bvec = [], []
    def row(): return np.zeros(nv)
    for (i, j) in arcs:  # x_j - x_i <= 0
        r = row(); r[j] = 1; r[i] = -1; A.append(r); bvec.append(0)
    bounds = [(0, 1)] * n
    unresolved = 0
    for k, (i, j) in enumerate(pairs):
        p, q = n + 2 * k, n + 2 * k + 1
        if R[i, j] or R[j, i]:
            # exact: p - q = x_i - x_j, and the inactive one is 0
            if R[i, j]:
                bounds += [(None, None), (0, 0)]
                r = row(); r[p] = 1; r[i] = -1; r[j] = 1; A.append(r); bvec.append(0)
                r = row(); r[p] = -1; r[i] = 1; r[j] = -1; A.append(r); bvec.append(0)
            else:
                bounds += [(0, 0), (None, None)]
                r = row(); r[q] = 1; r[j] = -1; r[i] = 1; A.append(r); bvec.append(0)
                r = row(); r[q] = -1; r[j] = 1; r[i] = -1; A.append(r); bvec.append(0)
        else:
            unresolved += 1
            bounds += [(0, None), (0, None)]
            for var, s in ((p, 1), (q, -1)):  # t = s (x_i - x_j)
                r = row(); r[var] = -1; r[i] += s; r[j] -= s; A.append(r); bvec.append(0)  # y >= t
                r = row(); r[var] = 1; r[i] -= s / 2; r[j] += s / 2; A.append(r); bvec.append(0.5)  # y <= (t+1)/2
    res = linprog(c, A_ub=np.array(A) if A else None, b_ub=np.array(bvec) if bvec else None,
                  bounds=bounds, method="highs")
    assert res.status == 0, res.message
    return -res.fun, res.x, unresolved, R

def bab(n, theta, rule="maxgain"):
    stack = [[]]
    nodes = 0; leaves = 0; min_leaf_depth = 10**9; lemma_ok = True
    while stack:
        arcs = stack.pop(); nodes += 1
        val, x, unres, R = node_lp(n, arcs)
        if val < unres - 1e-7:
            lemma_ok = False
        if val <= theta + 1e-7:
            leaves += 1; min_leaf_depth = min(min_leaf_depth, len(arcs)); continue
        # branch: unresolved pair whose split resolves the most pairs in the worse child
        best = None
        for (i, j) in itertools.combinations(range(n), 2):
            if R[i, j] or R[j, i]:
                continue
            if rule == "maxgain":
                g1 = closure(n, arcs + [(i, j)]).sum(); g2 = closure(n, arcs + [(j, i)]).sum()
                score = min(g1, g2)
            else:
                score = -abs(x[i] - x[j])
            if best is None or score > best[0]:
                best = (score, i, j)
        _, i, j = best
        stack.append(arcs + [(i, j)]); stack.append(arcs + [(j, i)])
    return nodes, leaves, min_leaf_depth, lemma_ok

def chain_depth_bound(n, theta):
    need = n * (n - 1) // 2 - theta
    D = 0
    while D * (D + 1) // 2 < need:
        D += 1
    return D

print("n  theta  root_LP  nodes  leaves  min_leaf_depth  depth_lower_bound(2^D leaves)  lemma_LP>=unresolved")
for n in range(3, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 9):
    opt = n * n // 4
    for delta in [0.0, 0.25]:
        theta = int(np.floor((1 + delta) * opt))
        root, _, _, _ = node_lp(n, [])
        nodes, leaves, mld, ok = bab(n, theta)
        print(f"{n}  {theta:5d}  {root:7.2f}  {nodes:5d}  {leaves:6d}  {mld:14d}  {chain_depth_bound(n, theta):29d}  {ok}")
        sys.stdout.flush()
