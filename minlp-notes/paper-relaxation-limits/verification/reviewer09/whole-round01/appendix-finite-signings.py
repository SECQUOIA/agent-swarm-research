from itertools import combinations
def min_range(n):
    edges = list(combinations(range(n), 2))
    free = [(i, j) for i, j in edges if i != 0]
    cuts = []
    for side in range(1 << (n - 1)):
        side <<= 1  # Vertex zero stays on side zero.
        cross = lambda i, j: ((side >> i) ^ (side >> j)) & 1
        size = sum(cross(i, j) for i, j in edges)
        mask = sum(cross(i, j) << k
                   for k, (i, j) in enumerate(free))
        cuts.append((size, mask))
    best = len(edges) + 1
    for negative in range(1 << len(free)):
        weights = [size - 2 * (negative & mask).bit_count()
                   for size, mask in cuts]
        best = min(best, max(weights) - min(weights))
    return best
result = [min_range(n) for n in range(2, 8)]
assert result == [1, 2, 4, 4, 5, 8]
print(result)
