"""Deterministic, scope-preserving tree decomposition heuristics.

An ordering provides an upper bound on treewidth, never a proof of minimum
width. Arbitrary factor/constraint scopes are completed to cliques before
elimination. Optional domain sizes favor smaller finite tables.
"""

from math import prod

from finite_dp import prepare_tree


def build_decomposition(n, scopes, *, weights=None, strategy="min_fill"):
    if type(n) is not int or n < 0:
        raise ValueError("invalid coordinate count")
    if strategy not in ("min_fill", "min_degree", "min_table"):
        raise ValueError("unknown decomposition strategy")
    if weights is None:
        weights = (2,) * n
    else:
        weights = tuple(weights)
        if len(weights) != n or any(type(k) is not int or k < 1 for k in weights):
            raise ValueError("weights must be positive integer domain sizes")
    scopes = tuple(tuple(scope) for scope in scopes)
    graph = [set() for _ in range(n)]
    for scope in scopes:
        if len(set(scope)) != len(scope) or any(type(i) is not int or not 0 <= i < n
                                              for i in scope):
            raise ValueError("invalid factor scope")
        for i in scope:
            graph[i].update(j for j in scope if j != i)
    if not n:
        return {"bags": [()], "edges": [], "order": [], "width": -1,
                "max_bag_size": 0, "fill_edges": 0, "strategy": strategy}
    remaining = set(range(n))
    bags, order, added = [], [], 0

    def score(i):
        neighbors = graph[i]
        degree = len(neighbors)
        if strategy == "min_degree":
            return degree, i
        table_size = weights[i] * prod(weights[j] for j in neighbors)
        fill = sum(len(neighbors - graph[j] - {j}) for j in neighbors) // 2
        if strategy == "min_table":
            return table_size, fill, degree, i
        return fill, table_size, degree, i

    while remaining:
        i = min(remaining, key=score)
        neighbors = set(graph[i])
        bags.append(tuple(sorted(neighbors | {i})))
        order.append(i)
        for j in neighbors:
            added += len(neighbors - graph[j] - {j})
        for j in neighbors:
            graph[j].update(neighbors - {j})
            graph[j].remove(i)
        remaining.remove(i)
        graph[i].clear()
    # At elimination i, all later neighbors belong to the earliest remaining
    # neighbor's bag, because fill made them a clique.
    positions = {i: t for t, i in enumerate(order)}
    edges, roots = [], []
    for t, bag in enumerate(bags):
        later = [positions[i] for i in bag if positions[i] > t]
        if later:
            edges.append((t, min(later)))
        else:
            roots.append(t)
    edges.extend(zip(roots, roots[1:]))
    prepare_tree(bags, edges, n)
    if any(not any(set(scope) <= set(bag) for bag in bags) for scope in scopes):
        raise ArithmeticError("decomposition lost a factor scope")
    return {"bags": bags, "edges": edges, "order": order,
            "width": max(map(len, bags)) - 1,
            "max_bag_size": max(map(len, bags)),
            "fill_edges": added // 2, "strategy": strategy}


def decompose_qp(A, *, weights=None, strategy="min_fill"):
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("Hessian must be square")
    if any(A[i][j] != A[j][i] for i in range(n) for j in range(i)):
        raise ValueError("Hessian must be symmetric")
    return build_decomposition(n, ((i, j) for i in range(n) for j in range(i)
                                  if A[i][j]), weights=weights, strategy=strategy)
