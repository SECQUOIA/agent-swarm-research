"""Exact independent checks of the pooling capacity support-function step."""

from fractions import Fraction
from itertools import product
from random import Random


def run():
    random = Random(20260905)
    cases = subsets = flow_points = interpolations = 0
    for case in range(128):
        n = random.choice((2, 3, 4, 5, 6))
        edges = [(i, i + 1) for i in range(n - 1)]
        if case % 3 == 0 and n % 2 == 0 and n >= 4:
            edges.append((n - 1, 0))
        elif case % 3 == 1:
            edges.pop(random.randrange(len(edges)))
        # Every edge is directed from its even (input) endpoint.
        edges = [(u, v) if u % 2 == 0 else (v, u) for u, v in edges]
        lower = [random.randrange(-3, 2) for _ in edges]
        upper = [l + random.randrange(4) for l in lower]

        def divergence(flow):
            answer = [0] * n
            for (u, v), amount in zip(edges, flow):
                answer[u] += amount
                answer[v] -= amount
            return tuple(answer)

        all_flows = list(product(*(range(l, u + 1) for l, u in zip(lower, upper))))
        reference = divergence(random.choice(all_flows))
        alpha = [d - random.randrange(3) for d in reference]
        beta = [d + random.randrange(3) for d in reference]
        feasible = {}
        for flow in all_flows:
            d = divergence(flow)
            if all(l <= x <= u for l, x, u in zip(alpha, d, beta)):
                feasible.setdefault(d, flow)
        assert feasible
        # The incidence system with integer data is integral. Enumeration
        # therefore gives its true support values, not just sampled points.
        masks = range(1 << n)

        def member(mask, vertex):
            return bool(mask & (1 << vertex))

        cut = []
        for mask in masks:
            cut.append(sum(
                u if member(mask, a) and not member(mask, b)
                else -l if member(mask, b) and not member(mask, a)
                else 0
                for (a, b), l, u in zip(edges, lower, upper)
            ))
        rank = []
        for s in masks:
            rank.append(min(
                cut[t] + sum(
                    beta[v] if member(s, v) and not member(t, v)
                    else -alpha[v] if member(t, v) and not member(s, v)
                    else 0 for v in range(n)
                ) for t in masks
            ))
            assert rank[s] == max(sum(d[v] for v in range(n) if member(s, v)) for d in feasible)
            subsets += 1
        assert rank[0] == rank[-1] == 0
        q = Fraction(1, 3)
        quality = [Fraction(random.randrange(-3, 4)) for _ in range(n)]
        cost = [1 / (quality[v] - q) if v % 2 == 0 else Fraction(0) for v in range(n)]
        extrema = []
        for sign in (1, -1):
            order = sorted(range(n), key=lambda v: sign * cost[v], reverse=True)
            greedy = [0] * n
            prefix = 0
            for v in order:
                previous = prefix
                prefix |= 1 << v
                greedy[v] = rank[prefix] - rank[previous]
            greedy = tuple(greedy)
            assert greedy in feasible
            value = sum(c * d for c, d in zip(cost, greedy))
            assert sign * value == max(sign * sum(c * d for c, d in zip(cost, x)) for x in feasible)
            extrema.append((value, feasible[greedy]))
        (maximum, max_flow), (minimum, min_flow) = extrema
        for weight in (Fraction(0), Fraction(1, 7), Fraction(1, 2), Fraction(1)):
            flow = [(1 - weight) * a + weight * b for a, b in zip(min_flow, max_flow)]
            d = divergence(flow)
            assert all(l <= w <= u for l, w, u in zip(lower, flow, upper))
            assert all(l <= x <= u for l, x, u in zip(alpha, d, beta))
            assert sum(c * x for c, x in zip(cost, d)) == (1 - weight) * minimum + weight * maximum
            interpolations += 1
        cases += 1
        flow_points += len(all_flows)
    print(f"PASS: {cases} signed path/cycle systems; {subsets} exact rank values; "
          f"{flow_points} integer arc assignments; {2 * cases} greedy extrema; "
          f"{interpolations} recovered interpolations")


if __name__ == "__main__":
    run()
