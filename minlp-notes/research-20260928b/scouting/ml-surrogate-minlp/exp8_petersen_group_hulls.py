"""Experiment 8: sanity check of the multi-neuron BaB lemma on a girth-5 graph.
Petersen graph (n=10, m=15, max cut 12).  Hidden layer p_e = ReLU(x_i - x_j),
q_e = ReLU(x_j - x_i).  Node relaxation: box, split arcs, exact resolved neurons,
q_e = p_e - (x_i - x_j), and the EXACT convex hull (over [0,1]^S) of the graph of
all neurons inside S for every 4-subset S (computed exactly with hull_tools).
Lemma to check: LP(node) >= number of unresolved edges (girth 5 > 4)."""
import itertools, random, sys
import numpy as np
from scipy.optimize import linprog
from hull_tools import graph_points, facets

outer = [(i, (i + 1) % 5) for i in range(5)]
spokes = [(i, i + 5) for i in range(5)]
inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
E = outer + spokes + inner
n, m = 10, len(E)
eid = {frozenset(e): k for k, e in enumerate(E)}

# exact group hull facets for every 4-subset (in coordinates x_S, p_{E(S)})
group_cuts = []  # list of (S, ES, facet vectors)
cache = {}
for S in itertools.combinations(range(n), 4):
    ES = [k for k, (i, j) in enumerate(E) if i in S and j in S]
    if not ES:
        continue
    loc = {v: t for t, v in enumerate(S)}
    key = tuple((loc[E[k][0]], loc[E[k][1]]) for k in ES)
    if key not in cache:
        W, b = [], []
        for (a, c) in key:
            w = [0] * 4; w[a] = 1; w[c] = -1; W.append(w); b.append(0)
        pts = graph_points(W, b, [0] * 4, [1] * 4)
        cache[key] = facets(pts)
    group_cuts.append((S, ES, cache[key]))
print(f"4-subsets with edges: {len(group_cuts)}, distinct local types: {len(cache)}, "
      f"total group facets: {sum(len(f) for _, _, f in group_cuts)}")

def closure(arcs):
    R = np.eye(n, dtype=bool)
    for (i, j) in arcs: R[i, j] = True
    for k in range(n): R |= np.outer(R[:, k], R[k, :])
    return R

def node_lp(arcs):
    R = closure(arcs)
    nv = n + 2 * m
    P = lambda k: n + 2 * k; Q = lambda k: n + 2 * k + 1
    c = np.zeros(nv); c[n:] = -1.0
    Aub, bub, Aeq, beq = [], [], [], []
    for (i, j) in arcs:
        r = np.zeros(nv); r[j] = 1; r[i] = -1; Aub.append(r); bub.append(0)
    unresolved = 0
    for k, (i, j) in enumerate(E):
        r = np.zeros(nv); r[Q(k)] = 1; r[P(k)] = -1; r[i] = 1; r[j] = -1; Aeq.append(r); beq.append(0)
        if R[i, j]:
            r = np.zeros(nv); r[Q(k)] = 1; Aeq.append(r); beq.append(0)
        elif R[j, i]:
            r = np.zeros(nv); r[P(k)] = 1; Aeq.append(r); beq.append(0)
        else:
            unresolved += 1
    for S, ES, F in group_cuts:
        for f in F:  # f[0] + sum f[1+t] x_S[t] + sum f[5+s] p_{ES[s]} >= 0
            r = np.zeros(nv)
            for t, v in enumerate(S): r[v] -= f[1 + t]
            for s, k in enumerate(ES): r[P(k)] -= f[5 + s]
            Aub.append(r); bub.append(f[0])
    bounds = [(0, 1)] * n + [(0, None)] * (2 * m)
    res = linprog(c, A_ub=np.array(Aub), b_ub=np.array(bub), A_eq=np.array(Aeq), b_eq=np.array(beq),
                  bounds=bounds, method="highs")
    assert res.status == 0, res.message
    return -res.fun, unresolved

root, u = node_lp([])
print(f"root LP with all exact 4-input group hulls = {root:.4f} (m = {m}, max cut = 12)")
rng = random.Random(5)
viol = 0; worst = None
for trial in range(300):
    D = rng.randint(1, 12)
    arcs = []
    for _ in range(D):
        i, j = rng.sample(range(n), 2)
        arcs.append((i, j))
    val, un = node_lp(arcs)
    if val < un - 1e-7: viol += 1
    worst = (val - un) if worst is None else min(worst, val - un)
print(f"random nodes: 300, violations of LP >= #unresolved: {viol}, min (LP - #unresolved) = {worst:.4f}")
