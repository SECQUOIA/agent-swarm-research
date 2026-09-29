"""Exact small graph checks for the component-elimination research note.

No external graph package is used. The treewidth routine exhausts elimination
orders, with memoization; it is intended only for the small graphs below.
"""

from functools import lru_cache
from itertools import combinations


def graph(vertices, edges):
    result = {v: set() for v in vertices}
    for u, v in edges:
        result[u].add(v)
        result[v].add(u)
    return result


def torso(g, removed):
    kept = set(g) - removed
    h = {v: g[v] & kept for v in kept}
    pending = set(removed)
    while pending:
        component = {pending.pop()}
        frontier = list(component)
        while frontier:
            u = frontier.pop()
            new = g[u] & pending
            component.update(new)
            pending.difference_update(new)
            frontier.extend(new)
        boundary = set().union(*(g[u] for u in component)) & kept
        for u in boundary:
            h[u].update(boundary - {u})
    return h


def exact_treewidth(g):
    vertices = list(g)
    index = {v: i for i, v in enumerate(vertices)}
    adjacency = tuple(sum(1 << index[w] for w in g[v]) for v in vertices)

    @lru_cache(None)
    def solve(alive, adj):
        if not alive:
            return -1
        candidates = [i for i in range(len(vertices)) if alive & (1 << i)]
        best = len(candidates) - 1
        for v in sorted(candidates, key=lambda i: adj[i].bit_count()):
            neighbors = adj[v]
            degree = neighbors.bit_count()
            if degree >= best:
                continue
            updated = list(adj)
            updated[v] = 0
            for u in candidates:
                if neighbors & (1 << u):
                    updated[u] = (adj[u] | neighbors) & ~(1 << u) & ~(1 << v)
            width = max(degree, solve(alive & ~(1 << v), tuple(updated)))
            best = min(best, width)
        return best

    return solve((1 << len(vertices)) - 1, adjacency)


def subdivision_complete(k):
    original = set(range(k))
    pairs = list(combinations(range(k), 2))
    g = graph(list(original) + pairs, [(v, e) for e in pairs for v in e])
    line = graph(pairs, [(e, f) for e, f in combinations(pairs, 2) if set(e) & set(f)])
    return g, original, line


def main():
    g = graph(range(5), [(u, v) for u in (0, 1) for v in (2, 3, 4)])
    h = torso(g, {0})
    assert all(len(h[v]) == 3 for v in h)
    assert (exact_treewidth(g), exact_treewidth(h)) == (2, 3)
    print("K2,3 singleton elimination: input treewidth 2, torso K4 treewidth 3")

    for k in range(3, 9):
        g, original, line = subdivision_complete(k)
        assert torso(g, original) == line
        if k <= 4:
            input_width, torso_width = exact_treewidth(g), exact_treewidth(line)
            expected = ((k - 1) ** 2) // 4 + k - 2
            assert input_width == k - 1
            assert torso_width == expected
            print(f"S(K{k}): input treewidth {input_width}, torso treewidth {torso_width}")
    print("S(Kk) torso equals L(Kk) for k=3,...,8")


if __name__ == "__main__":
    main()
