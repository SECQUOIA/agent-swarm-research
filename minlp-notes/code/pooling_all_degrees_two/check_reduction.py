"""Check the constant-data all-degree-two pooling reduction.

Run with the minlp-notes environment. Brute-force MIS is compared against
the original nonconvex P-formulation and, for small graphs, enumeration of
mode choices followed by an independent bipartite matching computation.
"""
from collections import Counter
from pathlib import Path
import argparse
import itertools
import random
import sys

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pooling_degree_two"))
from verify_reduction import solve_pooling


def build(n, colors, merged_lax=False):
    inputs, pools, outputs, arcs_in, arcs_out = {}, {}, {}, {}, {}
    for color, edges in enumerate(colors):
        assert sorted(v for e in edges for v in e) == list(range(n))
        for ei, (u, v) in enumerate(edges):
            resource = (color, ei)
            if color == 1:
                outputs[resource] = (0, 1)
                for w in (u, v):
                    arcs_out[w, resource] = -2
            else:
                inputs[resource] = (int(color == 2), 1)
                for w in (u, v):
                    arcs_in[resource, w] = int(color == 0)
                if color == 2 and merged_lax:
                    outputs[3, ei] = (1, 1)
                    for w in (u, v):
                        arcs_out[w, (3, ei)] = -1
    for v in range(n):
        pools[v] = 1
        if not merged_lax:
            outputs[3, v] = (1, 1)
            arcs_out[v, (3, v)] = -1
    assert set(Counter(i for i, _ in arcs_in).values()) == {2}
    assert set(Counter(v for _, v in arcs_in).values()) == {2}
    assert set(Counter(v for v, _ in arcs_out).values()) == {2}
    assert max(Counter(j for _, j in arcs_out).values()) <= 2
    if merged_lax:
        assert set(Counter(j for _, j in arcs_out).values()) == {2}
    return inputs, pools, outputs, arcs_in, arcs_out


def independent_set(n, edges):
    masks = [(1 << u) | (1 << v) for u, v in edges]
    return max(bits.bit_count() for bits in range(1 << n)
               if all(bits & edge != edge for edge in masks))


def mode_matching(n, instance):
    """Enumerate 2^n pure mode supports and use bipartite matching."""
    inputs, _, outputs, arcs_in, arcs_out = instance
    best = 0
    for modes in itertools.product((0, 1), repeat=n):
        g = nx.Graph()
        left = [("i", i) for i in inputs]
        right = [("j", j) for j in outputs]
        g.add_nodes_from(left, bipartite=0)
        g.add_nodes_from(right, bipartite=1)
        for v, mode in enumerate(modes):
            i = next(i for i, w in arcs_in if w == v and inputs[i][0] == mode)
            j = next(j for w, j in arcs_out if w == v and outputs[j][0] == mode)
            g.add_edge(("i", i), ("j", j))
        best = max(best, len(nx.bipartite.maximum_matching(g, top_nodes=left)) // 2)
    return best


def random_coloring(rng, n):
    while True:
        colors = []
        for _ in range(3):
            perm = list(range(n))
            rng.shuffle(perm)
            colors.append([tuple(sorted(perm[i:i+2])) for i in range(0, n, 2)])
        if len(set(itertools.chain.from_iterable(colors))) == 3*n//2:
            return colors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--trials", type=int, default=40)
    parser.add_argument("--merged-lax", action="store_true")
    args = parser.parse_args()
    rng = random.Random(args.seed)
    exact_count = 0
    for trial in range(args.trials):
        n = rng.choice((4, 6, 8, 10, 12))
        colors = random_coloring(rng, n)
        instance = build(n, colors, merged_lax=args.merged_lax)
        alpha = independent_set(n, list(itertools.chain.from_iterable(colors)))
        expected = n//2 + alpha
        actual = -solve_pooling(*instance)
        assert abs(actual - expected) < 1e-6, (n, colors, actual, expected)
        if n <= 8:
            exact = mode_matching(n, instance)
            assert exact == expected, (n, colors, exact, expected)
            exact_count += 1
        print(f"trial={trial} n={n} alpha={alpha} profit={actual:.9f} target={expected}", flush=True)
    print(f"PASS: {args.trials} P-formulation checks; {exact_count} exhaustive mode/matching checks; seed={args.seed}; merged_lax={args.merged_lax}")


if __name__ == "__main__":
    main()
