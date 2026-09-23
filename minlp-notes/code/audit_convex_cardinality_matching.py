"""Exact small-instance audit of the convex degree-cost matching reduction.

Compare exhaustive binary minimization with a separately enumerated unconstrained
matching gadget. All arithmetic is integer. This validates the reduction, not a
polynomial-time matching implementation.
"""

from functools import lru_cache
import random


def check_instance(edges, phi, linear):
    degree = [sum(v in edge for edge in edges) for v in range(len(phi))]
    next_node = 2 * len(edges)
    slots = []
    for count in degree:
        slots.append(list(range(next_node, next_node + count)))
        next_node += count
    gadget = []
    for e, (u, v) in enumerate(edges):
        gadget.append((2 * e, 2 * e + 1, 0))
        for k, slot in enumerate(slots[u]):
            gadget.append((2 * e, slot, phi[u][k + 1] - phi[u][k] + linear[e]))
        for k, slot in enumerate(slots[v]):
            gadget.append((2 * e + 1, slot, phi[v][k + 1] - phi[v][k]))
    mandatory_count = 2 * len(edges)
    bonus = 2 * sum(abs(cost) for _, _, cost in gadget) + 1
    adjacency = [[] for _ in range(next_node)]
    for u, v, cost in gadget:
        adjusted = cost - bonus * ((u < mandatory_count) + (v < mandatory_count))
        adjacency[u].append((v, adjusted))
        adjacency[v].append((u, adjusted))

    @lru_cache(None)
    def minimum_matching(mask):
        if not mask:
            return 0, ()
        first_bit = mask & -mask
        u = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        best = minimum_matching(remainder)  # Leaving a node unmatched is allowed.
        for v, cost in adjacency[u]:
            if remainder & (1 << v):
                tail_cost, tail_edges = minimum_matching(remainder ^ (1 << v))
                candidate = cost + tail_cost, ((u, v),) + tail_edges
                if candidate[0] < best[0]:
                    best = candidate
        return best

    matching_cost, matching = minimum_matching((1 << next_node) - 1)
    covered = {v for edge in matching for v in edge}
    assert set(range(mandatory_count)) <= covered
    unmodified = matching_cost + mandatory_count * bonus
    gadget_value = unmodified + sum(sequence[0] for sequence in phi)
    exhaustive = min(
        sum(sequence[sum(bool(mask & (1 << e)) for e, edge in enumerate(edges) if v in edge)]
            for v, sequence in enumerate(phi))
        + sum(linear[e] for e in range(len(edges)) if mask & (1 << e))
        for mask in range(1 << len(edges))
    )
    assert gadget_value == exhaustive, (edges, phi, linear, gadget_value, exhaustive)


def main():
    rng = random.Random(2026090407)
    samples = 100
    for _ in range(samples):
        factors = rng.randrange(2, 5)
        node_count = factors
        edges = []
        for _ in range(rng.randrange(1, 6)):
            u = rng.randrange(factors)
            if rng.random() < 0.3:
                v = node_count
                node_count += 1
            else:
                v = rng.choice([j for j in range(factors) if j != u])
            edges.append((u, v))
        phi = []
        for v in range(node_count):
            degree = sum(v in edge for edge in edges)
            if v >= factors:
                phi.append([0] * (degree + 1))
                continue
            slopes = sorted(rng.randrange(-8, 9) for _ in range(degree))
            sequence = [rng.randrange(-10, 11)]
            for slope in slopes:
                sequence.append(sequence[-1] + slope)
            phi.append(sequence)
        linear = [rng.randrange(-10, 11) for _ in edges]
        check_instance(edges, phi, linear)
    print(f"Passed {samples} exact exhaustive matching versus binary-minimization checks.")
    print("Cases include signed convex costs, negative edge costs, private and parallel edges.")


if __name__ == "__main__":
    main()
