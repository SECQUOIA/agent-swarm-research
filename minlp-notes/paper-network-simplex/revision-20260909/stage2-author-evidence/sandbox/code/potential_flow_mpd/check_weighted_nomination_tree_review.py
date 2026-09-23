"""Independent exact checks for the weighted-nomination comb-tree reduction."""

from fractions import Fraction as Q
from itertools import product
from random import Random


def require(condition):
    if not condition:
        raise AssertionError("independent exact check failed")


def vertices(weights, target):
    result = set()
    n = len(weights)
    for free in range(n):
        rest = [j for j in range(n) if j != free]
        for bits in product((0, 1), repeat=n - 1):
            y = [Q(0)] * n
            for j, bit in zip(rest, bits):
                y[j] = Q(bit * weights[j])
            y[free] = Q(target) - sum(y)
            if 0 <= y[free] <= weights[free]:
                result.add(tuple(y))
    return sorted(result)


def physical(weights, target, y):
    n = len(weights)
    require(sum(y) == target)
    edges = []
    potential = [Q(0)] * (2 * n)
    for j in range(n - 1):
        flow = sum(y[j + 1 :])
        edges.append((j, j + 1, Q(1), flow))
        potential[j + 1] = potential[j] - flow * abs(flow)
    for j in range(n):
        beta = Q(1, weights[j])
        edges.append((j, n + j, beta, y[j]))
        potential[n + j] = potential[j] - beta * y[j] * abs(y[j])
    balance = [Q(0)] * (2 * n)
    degree = [0] * (2 * n)
    for u, v, beta, flow in edges:
        require(flow >= 0)
        require(potential[u] - potential[v] == beta * flow * abs(flow))
        balance[u] += flow
        balance[v] -= flow
        degree[u] += 1
        degree[v] += 1
    require(balance == [Q(target)] + [Q(0)] * (n - 1) + [-v for v in y])
    require(len(edges) == 2 * n - 1 and max(degree) <= 3)
    value = sum(potential[j] - potential[n + j] for j in range(n))
    require(value == sum(v * v / w for v, w in zip(y, weights)))
    deficit = target - value
    distance = sum(min(v, w - v) for v, w in zip(y, weights))
    require(deficit >= distance / 2)
    if deficit < Q(1, 4):
        rounded = sum(w if 2 * v > w else 0 for v, w in zip(y, weights))
        require(rounded == target)
    return value


def main():
    rng = Random(20260905)
    count = states = interior = 0
    cases = [([1, 2], 1), ([2, 2], 1), ([2], 1), ([1, 1], 1)]
    for n in range(1, 8):
        for _ in range(14):
            w = [rng.randint(1, 11) for _ in range(n)]
            if sum(w) > 1:
                cases.append((w, rng.randint(1, sum(w) - 1)))
    for weights, target in cases:
        vs = vertices(weights, target)
        require(vs)
        values = [physical(weights, target, y) for y in vs]
        states += len(vs)
        optimum = max(values)
        subset = any(sum(w * bit for w, bit in zip(weights, bits)) == target
                     for bits in product((0, 1), repeat=len(weights)))
        require((optimum == target) == subset)
        require(subset or optimum <= Q(target) - Q(1, 2))
        for _ in range(20):
            a, b = rng.choice(vs), rng.choice(vs)
            t = Q(rng.randint(0, 31), 32)
            y = tuple(t * x + (1 - t) * z for x, z in zip(a, b))
            require(physical(weights, target, y) <= optimum)
            interior += 1
        count += 1
    print(f"PASS: {count} complete capped-simplex optimizations; "
          f"{states} exact vertex states; {interior} rational mixed states; "
          "physical conservation/laws, half-unit gap, and endpoint rounding.")


if __name__ == "__main__":
    main()
