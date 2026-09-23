"""
Check the key inequality behind the degeneracy bound on the McCormick/hull gap ratio:
for every weighted graph H (= induced subgraph G[X]) with degeneracy d,
      sum_{ij in E(H)} |a_ij|  <=  4*sqrt(d) * (mu+(H) - mu-(H))   and   <= 2*sqrt(Delta) * (mu+(H) - mu-(H)),
where mu+/mu- are the max/min weight of a cut (including the empty cut).
Also checks the stronger row-norm inequality (mu+ - mu-) >= sum_i ||a_i||_2 / 4.
Also reports the observed worst ratio  sum|a| / (mu+ - mu-)  divided by sqrt(d).
"""
import itertools, random, math
import numpy as np

def degeneracy(n, edges):
    adj = {i: set() for i in range(n)}
    for i, j in edges:
        adj[i].add(j); adj[j].add(i)
    deg = {i: len(adj[i]) for i in adj}
    removed = set(); d = 0
    for _ in range(n):
        v = min((i for i in adj if i not in removed), key=lambda i: deg[i])
        d = max(d, deg[v]); removed.add(v)
        for u in adj[v]:
            if u not in removed: deg[u] -= 1
    return d

def cut_range(n, edges, w):
    best = -math.inf; worst = math.inf
    for mask in range(1 << n):
        s = [(mask >> i) & 1 for i in range(n)]
        c = sum(w[k] for k, (i, j) in enumerate(edges) if s[i] != s[j])
        best = max(best, c); worst = min(worst, c)
    return best, worst

random.seed(0)
worst_ratio = 0.0
for trial in range(4000):
    n = random.randint(2, 9)
    p = random.choice([0.3, 0.5, 0.8, 1.0])
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if random.random() < p]
    if not edges: continue
    kind = random.choice(["pm1", "gauss", "unif"])
    if kind == "pm1": w = [random.choice([-1, 1]) for _ in edges]
    elif kind == "gauss": w = [random.gauss(0, 1) for _ in edges]
    else: w = [random.uniform(-1, 1) for _ in edges]
    d = degeneracy(n, edges)
    mp, mm = cut_range(n, edges, w)
    l1 = sum(abs(x) for x in w)
    ratio = l1 / (mp - mm)
    worst_ratio = max(worst_ratio, ratio / math.sqrt(d))
    Delta = max(sum(1 for (i, j) in edges if v in (i, j)) for v in range(n))
    row_norm_sum = sum(math.sqrt(sum(w[k] ** 2 for k, edge in enumerate(edges) if v in edge)) for v in range(n))
    assert row_norm_sum <= 4 * (mp - mm) + 1e-9, (n, edges, w)
    assert l1 <= 4 * math.sqrt(d) * (mp - mm) + 1e-9, (n, edges, w)
    assert l1 <= 2 * math.sqrt(Delta) * (mp - mm) + 1e-9, (n, edges, w)
print("all trials satisfy the inequality; worst observed (sum|a|/(mu+-mu-))/sqrt(d) =", round(worst_ratio, 4), "vs proved constant 4")
