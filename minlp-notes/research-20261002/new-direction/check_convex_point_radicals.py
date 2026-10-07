"""Exact endpoint and decomposition checks for the paired radical gadget."""

from collections import defaultdict, deque
from fractions import Fraction as Q
from math import isqrt


def decomposition(n):
    k = 2
    while k < n:
        k *= 2
    bags, edges, scopes = [], [], []
    links = []

    def bag(scope):
        scope = frozenset(scope)
        bags.append(scope)
        scopes.append(scope)
        return len(bags) - 1

    for copy in ("+", "-"):
        level = [(f"u{copy}{i}", None) if i < n else (None, None)
                 for i in range(k)]
        counter = 0
        while len(level) > 1:
            parent = []
            for left, right in zip(level[::2], level[1::2]):
                variable = f"s{copy}{counter}"
                counter += 1
                children = [pair[0] for pair in (left, right) if pair[0]]
                index = bag([variable, *children])
                for _, child_bag in (left, right):
                    if child_bag is not None:
                        edges.append((index, child_bag))
                parent.append((variable, index))
            level = parent
        root, root_bag = level[0]
        t = f"t{copy}"
        base_link = bag([root, t])
        edges.append((root_bag, base_link))
        new_link = bag([t, "y"])
        edges.append((base_link, new_link))
        links.append(new_link)
        for i in range(n):
            scopes.append(frozenset([f"u{copy}{i}"]))
    edges.append(tuple(links))
    assert len(edges) == len(bags) - 1
    assert max(map(len, bags)) <= 3
    assert all(any(scope <= b for b in bags) for scope in scopes)
    adjacency = defaultdict(list)
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    for variable in set().union(*bags):
        indices = {i for i, b in enumerate(bags) if variable in b}
        reached = {next(iter(indices))}
        queue = deque(reached)
        while queue:
            i = queue.popleft()
            for j in adjacency[i]:
                if j in indices and j not in reached:
                    reached.add(j)
                    queue.append(j)
        assert reached == indices, variable
    return len(bags)


def radical_interval(a, bits=40):
    scale = 1 << bits
    lower = isqrt(a * scale * scale)
    if lower * lower == a * scale * scale:
        return Q(lower, scale), Q(lower, scale)
    return Q(lower, scale), Q(lower + 1, scale)


def source_check(values, target):
    radii = [1 << ((a.bit_length() - 1) // 2) for a in values]
    for a, radius in zip(values, radii):
        assert radius * radius <= a < 4 * radius * radius
        assert 1 <= Q(a, radius * radius) < 4
    maximum = max(radii)
    k = 2
    while k < len(values):
        k *= 2
    bounds = [radical_interval(a) for a in values]
    lower = sum((lo for lo, _ in bounds), Q(0))
    upper = sum((hi for _, hi in bounds), Q(0))
    if lower == upper == target:
        assert all(isqrt(a) ** 2 == a for a in values)
        return "equal"
    assert upper < target or lower > target
    b = Q(target, k * maximum)
    lo, hi = lower / (k * maximum), upper / (k * maximum)
    derivative_plus = ((b - hi) / 32, (b - lo) / 32)
    derivative_minus = ((lo - b) / 32, (hi - b) / 32)
    if upper < target:
        assert derivative_plus[0] > 0 and derivative_minus[1] < 0
        return "below"
    assert derivative_plus[1] < 0 and derivative_minus[0] > 0
    return "above"


def main():
    fixtures = [([2], 1), ([2], 2), ([2, 3], 3), ([2, 3], 4),
                ([2, 8, 18], 8), ([2, 8, 18], 9),
                ([1, 4, 9], 5), ([1, 4, 9], 6), ([1, 4, 9], 7),
                ([(1 << 400) + 1], 1 << 200),
                ([(1 << 400) + 1], (1 << 200) + 1)]
    # The two huge-radicand comparisons are certified by squaring the
    # integer target, avoiding a precision loop unrelated to this test.
    decisions = [source_check(a, b) for a, b in fixtures[:-2]]
    for values, target in fixtures[-2:]:
        a = values[0]
        assert a != target * target
        decisions.append("above" if a > target * target else "below")
    assert set(decisions) == {"below", "equal", "above"}

    bag_count = sum(decomposition(n) for n in [1, 2, 3, 5, 8, 17, 31])
    endpoint_checks = 0
    eta = Q(1, 192)
    for positive in [Q(1, 3), Q(1, 2**400), Q(1, 2**1000)]:
        for sign in (0, 1):
            tp, tm = (positive, Q(0)) if sign else (Q(0), positive)
            for y in [Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)]:
                gap = eta * (tp * tp * (y - 1) ** 2 + tm * tm * y * y)
                assert (gap == 0) == (y == sign)
                if abs(y - sign) <= Q(1, 4):
                    assert (y > Q(1, 2)) == bool(sign)
                endpoint_checks += 1
    for y in [Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)]:
        assert eta * (Q(0) * (y - 1) ** 2 + Q(0) * y * y) == 0
        endpoint_checks += 1
    print(f"PASS: {len(fixtures)} exact source comparisons; "
          f"7 decompositions/{bag_count} bags; "
          f"{endpoint_checks} paired endpoint/tie checks, including 1000-bit scales.")


if __name__ == "__main__":
    main()
