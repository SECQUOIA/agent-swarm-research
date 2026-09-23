"""Exact finite checks of two spatial-certificate boundary calculations.

These checks support the written proofs; they do not prove universal claims.
The slab vertices are enumerated independently from their active constraints.
The half-split tree count uses a recursion, independently of its binomial form.
"""

from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import comb
from pathlib import Path
import json


def slab_vertices(n, k, delta):
    lo, hi = Q(2 * k + 1, 2) - delta, Q(2 * k + 1, 2) + delta
    vertices = set()
    for bits in product((Q(0), Q(1)), repeat=n):
        if lo <= sum(bits) <= hi:
            vertices.add(bits)
    # A non-Boolean vertex has n-1 active coordinate bounds and one active
    # demand boundary. Enumerating both boundaries also covers delta=0.
    for free in range(n):
        for bits in product((Q(0), Q(1)), repeat=n - 1):
            for boundary in (lo, hi):
                value = boundary - sum(bits)
                if 0 <= value <= 1:
                    vertices.add(bits[:free] + (value,) + bits[free:])
    return vertices


@lru_cache(None)
def terminal_counts(high, low, high_stop, low_stop):
    if high >= high_stop or low >= low_stop:
        return 1, 1
    left = terminal_counts(high + 1, low, high_stop, low_stop)
    right = terminal_counts(high, low + 1, high_stop, low_stop)
    return left[0] + right[0], 1 + left[1] + right[1]


def main():
    slab_cases = vertices_checked = tree_cases = 0
    tolerances = (Q(0), Q(1, 100), Q(1, 8), Q(1, 4), Q(49, 100))
    for n in range(2, 9):
        for k in range(1, n):
            for delta in tolerances:
                vertices = slab_vertices(n, k, delta)
                expected = Q(1, 4) - delta * delta
                assert vertices
                values = {sum(x * (1 - x) for x in v) for v in vertices}
                assert values == {expected}, (n, k, delta, values)
                assert all(abs(sum(v) - Q(2 * k + 1, 2)) == delta for v in vertices)
                slab_cases += 1
                vertices_checked += len(vertices)
    for n in range(2, 61):
        for k in range(1, n):
            leaves, nodes = terminal_counts(0, 0, k + 1, n - k)
            assert leaves == comb(n + 1, k + 1), (n, k, leaves)
            assert nodes == 2 * leaves - 1
            if k == 1:
                assert nodes == n * n + n - 1
            tree_cases += 1
            terminal_counts.cache_clear()
    # The narrow tolerance condition matters: the slab includes a Boolean
    # point at delta=1/2, and retains optimum zero for larger delta.
    for delta in (Q(1, 2), Q(3, 4), Q(1)):
        vertices = slab_vertices(4, 1, delta)
        assert min(sum(x * (1 - x) for x in v) for v in vertices) == 0
    result = dict(
        status="PASS",
        slab_cases=slab_cases,
        slab_vertices=vertices_checked,
        tree_cases=tree_cases,
        out_of_range_regressions=3,
        arithmetic="fractions.Fraction and integer counts",
        limitation="Finite corroboration; universal validity is supplied by the proofs.",
    )
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
