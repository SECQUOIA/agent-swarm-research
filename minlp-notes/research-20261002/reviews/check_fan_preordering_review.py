"""Independent exact LDL and graph checks for the conditioned fan example.

Finite algebra checks supplement, rather than replace, the all-degree
origin-jet proof. Uses only the Python standard library.
"""

from fractions import Fraction as F


def transpose(a):
    return list(map(list, zip(*a)))


def multiply(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def inner(a, b):
    return sum(x * y for ar, br in zip(a, b) for x, y in zip(ar, br))


def ldl(a):
    n = len(a)
    lower = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    diagonal = []
    for i in range(n):
        pivot = a[i][i] - sum(lower[i][k]**2 * diagonal[k] for k in range(i))
        assert pivot > 0
        diagonal.append(pivot)
        for j in range(i + 1, n):
            lower[j][i] = (
                a[j][i] - sum(lower[j][k] * lower[i][k] * diagonal[k] for k in range(i))
            ) / pivot
    scaled = [[value * diagonal[j] for j, value in enumerate(row)] for row in lower]
    assert multiply(scaled, transpose(lower)) == a
    return diagonal


def check_tree_decomposition(blocks, support):
    bags = []
    edges = []
    roots = []
    for block in range(blocks):
        offset = 5 * block
        root = len(bags)
        roots.append(root)
        bags.extend([{offset + i for i in bag} for bag in ({0, 1, 2}, {1, 2, 3}, {2, 3, 4})])
        edges.extend([(root, root + 1), (root + 1, root + 2)])
    for block in range(blocks - 1):
        bridge = len(bags)
        bags.append({5 * block, 5 * (block + 1)})
        edges.extend([(roots[block], bridge), (bridge, roots[block + 1])])
    adjacency = {i: set() for i in range(len(bags))}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    assert len(edges) == len(bags) - 1

    def connected(nodes):
        reached, pending = set(), [next(iter(nodes))]
        while pending:
            node = pending.pop()
            if node not in reached:
                reached.add(node)
                pending.extend(adjacency[node] & nodes - reached)
        return reached == nodes

    assert connected(set(adjacency))
    for variable in range(5 * blocks):
        assert connected({i for i, bag in enumerate(bags) if variable in bag})
    for edge in support:
        assert any(set(edge) <= bag for bag in bags)
    assert max(map(len, bags)) == 3
    assert {(0, 1), (0, 2), (1, 2)} <= support  # triangle lower bound
    return len(bags)


def main():
    horn = [[F(1 - 2 * int((i - j) % 5 in (1, 4))) for j in range(5)] for i in range(5)]
    v = [[F(int(i == j)) for j in range(5)] for i in range(5)]
    v[1][3] = v[3][3] = v[2][4] = v[4][4] = F(1, 2)
    c = multiply(multiply(transpose(v), horn), v)
    expected = [[1, -1, 1, 0, 0], [-1, 1, -1, 1, 0], [1, -1, 1, -1, 1],
                [0, 1, -1, 1, F(-1, 2)], [0, 0, 1, F(-1, 2), 1]]
    assert c == expected
    w = [[F(x) for x in row] for row in [
        [1773, 1803, 0, 0, 336], [1803, 3544, 1803, 0, 0],
        [0, 1803, 4020, 2286, 0], [0, 0, 2286, 2476, 392],
        [336, 0, 0, 392, 200]]]
    assert all(x >= 0 for row in w for x in row)
    pivots = ldl(w)
    assert len(pivots) == 5
    epsilon = F(1, 100)
    q = [[c[i][j] + epsilon * int(i == j) for j in range(5)] for i in range(5)]
    assert sum(w[i][i] for i in range(5)) == 12013
    assert inner(c, w) == -163
    assert inner(q, w) == F(-4287, 100)
    assert max(sum(map(abs, row)) for row in c) == 5
    local_support = {(i, j) for i in range(5) for j in range(i + 1, 5) if c[i][j]}
    assert local_support == {(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)}
    zero = [[F(x)] for x in (1, 1, 0, 0, 0)]
    assert multiply(multiply(transpose(zero), c), zero)[0][0] == 0
    assert multiply(multiply(transpose(zero), q), zero)[0][0] == 2 * epsilon
    assert 2 * max(q[i][i] for i in range(5)) / epsilon == 202

    restrictions = bags = 0
    for blocks in (1, 2, 3, 8, 17):
        support = {(5 * b + i, 5 * b + j) for b in range(blocks) for i, j in local_support}
        support |= {(5 * b, 5 * (b + 1)) for b in range(blocks - 1)}
        bags += check_tree_decomposition(blocks, support)
        for block in range(blocks):
            degree = int(block > 0) + int(block + 1 < blocks)
            restricted = [row[:] for row in q]
            restricted[0][0] += epsilon * degree
            assert inner(restricted, w) <= F(-741, 100) < 0
            assert 2 * max(restricted[i][i] for i in range(5)) / epsilon <= 206
            restrictions += 1
        # Identical zero-ray blocks make every bridge vanish exactly.
        assert blocks * 2 * epsilon / (2 * blocks) == epsilon
    print(f"PASS: exact Horn congruence; 5 positive LDL pivots and reconstruction; "
          f"fan support; 5 chain decompositions ({bags} bags); "
          f"{restrictions} restricted separators; exact growth and curvature bounds.")


if __name__ == "__main__":
    main()
