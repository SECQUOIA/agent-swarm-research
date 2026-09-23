"""Search for failures of a conjectured two-balanced-factor partition.

Only a finite combinatorial check; no mathematical upper bound is inferred.
"""

import argparse
import itertools
import json
import random

from search_multilinear_treewidth_two import width_two


def odd_holes(terms):
    variables = sorted(set().union(*(set(term) for term in terms)))
    offset = len(terms)
    ids = {v: offset + j for j, v in enumerate(variables)}
    graph = [set() for _ in range(offset + len(variables))]
    for e, term in enumerate(terms):
        for v in term:
            graph[e].add(ids[v])
            graph[ids[v]].add(e)
    clauses = set()

    def extend(path):
        start, last = path[0], path[-1]
        for new in graph[last]:
            if new <= start or new in path:
                continue
            previous = graph[new].intersection(path[:-1])
            if previous:
                if previous == {start} and len(path) >= 3:
                    cycle = path + [new]
                    if len(cycle) % 4 == 2:
                        clauses.add(frozenset(v for v in cycle if v < offset))
                continue
            extend(path + [new])

    for start in range(len(graph)):
        extend([start])
    return sorted(clauses, key=lambda clause: (len(clause), tuple(sorted(clause))))


def colorable(clauses, number, number_of_colors=2):
    colors = [None] * number

    def visit():
        unresolved = []
        for clause in clauses:
            used = {colors[v] for v in clause if colors[v] is not None}
            missing = [v for v in clause if colors[v] is None]
            if len(used) >= 2:
                continue
            if not missing:
                return False
            unresolved.append(missing)
        if not unresolved:
            return True
        choices = min(unresolved, key=len)
        variable = max(choices, key=lambda v: sum(v in c for c in unresolved))
        for color in range(number_of_colors):
            colors[variable] = color
            if visit():
                return True
        colors[variable] = None
        return False

    return visit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graphs", type=int, default=500)
    args = parser.parse_args()
    rng = random.Random(172092)
    for instance in range(args.graphs):
        dimension = rng.randrange(5, 11)
        candidates = [term for size in range(2, dimension + 1)
                      for term in itertools.combinations(range(dimension), size)]
        rng.shuffle(candidates)
        terms = []
        for term in candidates:
            if width_two(terms + [term]):
                terms.append(term)
        clauses = odd_holes(terms)
        if not colorable(clauses, len(terms)):
            print(json.dumps({"counterexample": terms, "clauses": [sorted(c) for c in clauses]}))
            return
        if (instance + 1) % 100 == 0:
            print(json.dumps({"checked": instance + 1}), flush=True)
    print(json.dumps({"total_checked": args.graphs, "counterexamples": 0}))


if __name__ == "__main__":
    main()
