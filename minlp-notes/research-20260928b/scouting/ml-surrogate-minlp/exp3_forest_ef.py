"""Experiment 3: breakpoint discretization + junction-tree extended formulation for
fan-in-2 ReLU layers whose input-interaction graph is a forest (Theorem B sketch).

For each random instance:
  (a) exact arrangement vertices; check every coordinate value lies in the predicted
      set V_i (anchor values propagated along tree paths);
  (b) build the local-marginal-polytope LP (exact for forests) and compare its optimum
      with the exact maximum over the graph for random objectives.
Also reports, for cycles and ladders, the number of distinct coordinate values at
arrangement vertices (the quantity that controls the discretized formulation size).
"""
from fractions import Fraction as Fr
import random, itertools, collections
import numpy as np
from scipy.optimize import linprog
from hull_tools import arrangement_vertices, relu_layer

def random_layer(edges, n, rng, per_edge=1, unary=0):
    W, b, supp = [], [], []
    for (i, j) in edges:
        for _ in range(per_edge):
            while True:
                w = [0]*n
                w[i] = rng.choice([-3,-2,-1,1,2,3]); w[j] = rng.choice([-3,-2,-1,1,2,3])
                lo = min(0, w[i]) + min(0, w[j]); hi = max(0, w[i]) + max(0, w[j])
                bb = Fr(rng.randint(-12, 12), 4)
                if lo + bb < 0 < hi + bb:
                    break
            W.append(w); b.append(bb); supp.append((i, j))
    for _ in range(unary):
        i = rng.randrange(n); w = [0]*n; w[i] = rng.choice([-2,-1,1,2])
        bb = Fr(rng.randint(1, 3), 4) * (-w[i])  # breakpoint inside (0,1)
        W.append(w); b.append(bb); supp.append((i,))
    return W, b, supp

def predicted_values(n, W, b, supp, edges):
    """Anchor values (box bounds, unary breakpoints, parallel-neuron intersections)
    propagated along paths of the forest."""
    adj = collections.defaultdict(list)
    for idx, s in enumerate(supp):
        if len(s) == 2:
            adj[s[0]].append((s[1], idx)); adj[s[1]].append((s[0], idx))
    anchors = collections.defaultdict(set)
    for i in range(n):
        anchors[i] |= {Fr(0), Fr(1)}
    for idx, s in enumerate(supp):
        if len(s) == 1:
            i = s[0]; anchors[i].add(-Fr(b[idx]) / W[idx][i])
    # parallel neurons on the same pair: solve 2x2 systems
    bypair = collections.defaultdict(list)
    for idx, s in enumerate(supp):
        if len(s) == 2: bypair[tuple(sorted(s))].append(idx)
    for (i, j), idxs in bypair.items():
        for p, q in itertools.combinations(idxs, 2):
            a1, b1, c1 = Fr(W[p][i]), Fr(W[p][j]), Fr(b[p]); a2, b2, c2 = Fr(W[q][i]), Fr(W[q][j]), Fr(b[q])
            det = a1*b2 - a2*b1
            if det != 0:
                xi = (-c1*b2 + c2*b1)/det; xj = (-a1*c2 + a2*c1)/det
                anchors[i].add(xi); anchors[j].add(xj)
    V = collections.defaultdict(set)
    for l in range(n):
        for val in anchors[l]:
            # DFS from l propagating the value through each neuron on each edge
            stack = [(l, val, -1)]
            while stack:
                i, v, parent = stack.pop()
                if not (0 <= v <= 1):
                    continue
                V[i].add(v)
                for j, idx in adj[i]:
                    if j == parent: continue
                    a, c, bb = Fr(W[idx][i]), Fr(W[idx][j]), Fr(b[idx])
                    stack.append((j, -(a*v + bb)/c, i))
    return V

def marginal_lp_max(n, W, b, supp, edges, V, cx, dy):
    Vi = {i: sorted(V[i]) for i in range(n)}
    var = {}
    def add(key):
        var[key] = len(var)
    for i in range(n):
        for a in Vi[i]: add(('n', i, a))
    for (i, j) in edges:
        for a in Vi[i]:
            for c in Vi[j]: add(('e', i, j, a, c))
    cost = np.zeros(len(var))
    for i in range(n):
        for a in Vi[i]: cost[var[('n', i, a)]] -= float(cx[i]) * float(a)
    for idx, s in enumerate(supp):
        if len(s) == 1:
            i = s[0]
            for a in Vi[i]:
                x = [Fr(0)]*n; x[i] = a
                cost[var[('n', i, a)]] -= float(dy[idx]) * float(max(Fr(0), W[idx][i]*a + b[idx]))
        else:
            i, j = s
            e = (i, j) if (i, j) in edges else (j, i)
            for a in Vi[e[0]]:
                for c in Vi[e[1]]:
                    xi, xj = (a, c) if e == (i, j) else (c, a)
                    t = W[idx][i]*xi + W[idx][j]*xj + b[idx]
                    cost[var[('e', e[0], e[1], a, c)]] -= float(dy[idx]) * float(max(Fr(0), t))
    Aeq, beq = [], []
    for i in range(n):
        row = np.zeros(len(var))
        for a in Vi[i]: row[var[('n', i, a)]] = 1
        Aeq.append(row); beq.append(1)
    for (i, j) in edges:
        for a in Vi[i]:
            row = np.zeros(len(var)); row[var[('n', i, a)]] = -1
            for c in Vi[j]: row[var[('e', i, j, a, c)]] = 1
            Aeq.append(row); beq.append(0)
        for c in Vi[j]:
            row = np.zeros(len(var)); row[var[('n', j, c)]] = -1
            for a in Vi[i]: row[var[('e', i, j, a, c)]] = 1
            Aeq.append(row); beq.append(0)
    res = linprog(cost, A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=(0, None), method='highs')
    assert res.status == 0
    return -res.fun, len(var)

def random_tree(n, rng):
    return [(rng.randrange(i), i) for i in range(1, n)]

rng = random.Random(3)
print("== forests: coordinate-value containment and marginal-LP exactness")
worst = 0.0; checked = 0; missing = 0
for n in [3, 4, 5, 6]:
    for trial in range(8 if n < 6 else 4):
        edges = random_tree(n, rng)
        W, b, supp = random_layer(edges, n, rng, per_edge=rng.choice([1, 1, 2]), unary=rng.choice([0, 1, 2]))
        verts = arrangement_vertices(W, b, [0]*n, [1]*n)
        V = predicted_values(n, W, b, supp, edges)
        for v in verts:
            for i in range(n):
                if v[i] not in V[i]:
                    missing += 1
        gpts = [(v, relu_layer(W, b, v)) for v in verts]
        for _ in range(5):
            cx = [rng.uniform(-1, 1) for _ in range(n)]; dy = [rng.uniform(-2, 2) for _ in range(len(W))]
            true = max(sum(c*float(x) for c, x in zip(cx, v)) + sum(d*float(y) for d, y in zip(dy, yy)) for v, yy in gpts)
            lp, nv = marginal_lp_max(n, W, b, supp, edges, V, cx, dy)
            worst = max(worst, abs(lp - true)); checked += 1
    print(f"n={n}: done; max |V_i| seen so far={max(len(s) for s in V.values())}")
print(f"objectives checked={checked}, max |LP - true max| = {worst:.2e}, coordinate values missing from V = {missing}")

print("== distinct coordinate values at arrangement vertices (one neuron per edge, random weights)")
def float_vertices(W, b, n):
    H = []
    for i in range(n):
        e = np.zeros(n); e[i] = 1; H.append((e, 0.0)); H.append((e, 1.0))
    for wj, bj in zip(W, b):
        H.append((np.array([float(v) for v in wj]), -float(bj)))
    A = np.array([h[0] for h in H]); r = np.array([h[1] for h in H])
    out = set()
    for S in itertools.combinations(range(len(H)), n):
        M = A[list(S)]
        if abs(np.linalg.det(M)) < 1e-9: continue
        x = np.linalg.solve(M, r[list(S)])
        if np.all(x > -1e-9) and np.all(x < 1 + 1e-9):
            out.add(tuple(np.round(x, 9)))
    return out

def distinct_values(n, edges, trials=3):
    out = []
    for _ in range(trials):
        W, b, supp = random_layer(edges, n, rng)
        verts = float_vertices(W, b, n)
        out.append(max(len({v[i] for v in verts}) for i in range(n)))
    return max(out)

for n in [4, 5, 6, 7]:
    path = [(i, i+1) for i in range(n-1)]
    cyc = path + [(n-1, 0)]
    print(f"n={n}: path max_i|values|={distinct_values(n, path)}  cycle={distinct_values(n, cyc)}")
for L in [2, 3]:
    n = 2*L
    lad = [(2*i, 2*i+2) for i in range(L-1)] + [(2*i+1, 2*i+3) for i in range(L-1)] + [(2*i, 2*i+1) for i in range(L)]
    print(f"ladder 2x{L} (n={n}): max_i|values|={distinct_values(n, lad, trials=2)}")
