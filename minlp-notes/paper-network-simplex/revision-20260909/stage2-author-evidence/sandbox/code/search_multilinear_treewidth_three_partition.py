"""Finite search for a three-balanced-row partition at incidence width three.

A greedy elimination with fill certifies every accepted support's width upper
bound. Failure of that greedy test does not certify a width lower bound.
"""

import argparse
import itertools
import json
import random

from search_multilinear_balanced_partition import odd_holes, colorable


def width_certificate(terms, bound=3):
    graph = {}
    for index, term in enumerate(terms):
        factor = ("e", index)
        graph[factor] = {("v", i) for i in term}
        for variable in graph[factor]:
            graph.setdefault(variable, set()).add(factor)
    while graph:
        node = min(graph, key=lambda item: (len(graph[item]), item))
        neighbors = list(graph[node])
        if len(neighbors) > bound:
            return False
        for first, second in itertools.combinations(neighbors, 2):
            graph[first].add(second)
            graph[second].add(first)
        for neighbor in neighbors:
            graph[neighbor].remove(node)
        del graph[node]
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graphs", type=int, default=3000)
    args = parser.parse_args()
    rng = random.Random(411038)
    require_three = 0
    for instance in range(args.graphs):
        dimension = rng.randrange(6, 12)
        candidates = [term for size in range(2, dimension + 1)
                      for term in itertools.combinations(range(dimension), size)]
        rng.shuffle(candidates)
        terms = []
        for term in candidates:
            if width_certificate(terms + [term]):
                terms.append(term)
        clauses = odd_holes(terms)
        if not colorable(clauses, len(terms), 3):
            print(json.dumps({"counterexample": terms,
                              "clauses": [sorted(c) for c in clauses]}), flush=True)
            return
        if not colorable(clauses, len(terms), 2):
            require_three += 1
            if require_three == 1:
                print(json.dumps({"first_three_color_support": terms}), flush=True)
        if (instance + 1) % 100 == 0:
            print(json.dumps({"checked": instance + 1, "require_three": require_three}), flush=True)
    print(json.dumps({"total_checked": args.graphs, "require_three": require_three,
                      "counterexamples": 0}), flush=True)


if __name__ == "__main__":
    main()
