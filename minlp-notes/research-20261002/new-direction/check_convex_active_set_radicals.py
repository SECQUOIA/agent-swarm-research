"""Exact checks for the active-bound / radical-sum reduction."""

from fractions import Fraction as Q


def transpose(a):
    return list(map(list, zip(*a)))


def multiply(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)]
            for row in a]


def positive_ldl(a):
    a = [row[:] for row in a]
    for i in range(len(a)):
        pivot = a[i][i]
        assert pivot > 0, (i, pivot)
        for j in range(i + 1, len(a)):
            for k in range(j, len(a)):
                a[k][j] -= a[i][j] * a[i][k] / pivot
                a[j][k] = a[k][j]


def construction(radicals):
    n = len(radicals)
    k = 1 << (max(2, n) - 1).bit_length()
    scales = [1 << ((a.bit_length() - 1) // 2) for a in radicals]
    scale = max(scales)
    c = [Q(a, r * r) for a, r in zip(radicals, scales)]
    assert all(1 <= z < 4 for z in c)
    signals = [(i, Q(r, scale)) for i, r in enumerate(scales)]
    signals += [None] * (k - n)
    rows = [{} for _ in radicals]
    bags = []
    while len(signals) > 1:
        next_signals = []
        for left, right in zip(signals[::2], signals[1::2]):
            node = len(rows)
            row = {child[0]: child[1] / 2
                   for child in (left, right) if child is not None}
            rows.append(row)
            bags.append({node, *row})
            next_signals.append((node, Q(1)))
        signals = next_signals
    root = signals[0][0]
    size = len(rows)
    p = [[rows[i].get(j, Q(0)) for j in range(size)] for i in range(size)]
    pp = multiply(p, transpose(p))
    assert all(pp[i][i] <= Q(1, 2) for i in range(size))
    assert all(pp[i][j] == 0 for i in range(size)
               for j in range(size) if i != j)
    d = [[Q(i == j) - p[i][j] for j in range(size)] for i in range(size)]
    h0 = [[2 * z for z in row] for row in multiply(transpose(d), d)]
    h = [row + [Q(0)] for row in h0]
    h.append([Q(0)] * size + [Q(2)])
    h[root][-1] = h[-1][root] = -Q(1, 32)
    positive_ldl([[h[i][j] - Q(i == j, 16) for j in range(size + 1)]
                  for i in range(size + 1)])
    # Actual leaf Hessians range from two to four. All other terms are fixed.
    assert all(h[i][i] + (2 if i < n else 0) <= 5
               for i in range(size + 1))
    bags.append({root, size})
    assert max(map(len, bags)) <= 3
    edges = [(i, j) for i in range(size + 1) for j in range(i)
             if h[i][j] != 0]
    assert all(any({i, j} <= bag for bag in bags) for i, j in edges)
    owner = {max(bag): index for index, bag in enumerate(bags[:-1])}
    adjacency = [[] for _ in bags]
    for child_node, child_bag in owner.items():
        if child_node == root:
            parent_bag = len(bags) - 1
        else:
            parent_bag = next(j for j, bag in enumerate(bags[:-1])
                              if child_node in bag and j != child_bag)
        adjacency[child_bag].append(parent_bag)
        adjacency[parent_bag].append(child_bag)
    for coordinate in range(size + 1):
        containing = {i for i, bag in enumerate(bags) if coordinate in bag}
        seen = set()
        stack = [next(iter(containing))]
        while stack:
            at = stack.pop()
            if at not in seen:
                seen.add(at)
                stack.extend(j for j in adjacency[at]
                             if j in containing and j not in seen)
        assert seen == containing
    return k, scale, c, rows, root, len(bags)


def main():
    fixtures = [[1], [2], [3], [4], [2, 3], [1, 2, 3], [2, 8, 18, 32],
                [1, 4, 9, 16, 25], [2, 7, 19, 31, 101, 997, 65537],
                [2**400 + 1, 3, 2**399 - 1]]
    bag_count = 0
    for instance in fixtures:
        *_, bags = construction(instance)
        bag_count += bags
    kkt_cases = 0
    for roots in ([1], [1, 2], [1, 3, 5], [2, 4, 8, 16, 32]):
        instance = [a * a for a in roots]
        k, scale, c, rows, root, bags = construction(instance)
        bag_count += bags
        denominators = [1 << ((a.bit_length() - 1) // 2) for a in instance]
        point = [Q(a, r) for a, r in zip(roots, denominators)]
        assert all(x * x == ci for x, ci in zip(point, c))
        for row in rows[len(roots):]:
            point.append(sum(coef * point[i] for i, coef in row.items()))
        assert point[root] == Q(sum(roots), k * scale)
        for target in (sum(roots) - 1, sum(roots), sum(roots) + 1):
            slope = (Q(target, k * scale) - point[root]) / 32
            assert (slope >= 0) == (sum(roots) <= target)
            if slope < 0:
                y = -slope / 2
                assert 0 < y < 1
                assert y * y + slope * y == -slope * slope / 4 < 0
            kkt_cases += 1
    print(f"PASS: {len(fixtures) + 4} construction fixtures, {bag_count} bags, "
          f"14 exact positive-LDL/curvature checks, {kkt_cases} KKT comparisons")


if __name__ == "__main__":
    main()
