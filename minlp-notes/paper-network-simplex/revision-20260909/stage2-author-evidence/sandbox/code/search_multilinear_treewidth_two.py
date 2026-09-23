"""Bounded numerical search; not a proof of a treewidth-two gap bound."""

import argparse
import itertools
import json

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, hstack


def width_two(terms):
    graph = {}
    for index, term in enumerate(terms):
        factor = ("e", index)
        graph[factor] = {("v", i) for i in term}
        for variable in graph[factor]:
            graph.setdefault(variable, set()).add(factor)
    while graph:
        node = min(graph, key=lambda item: len(graph[item]))
        neighbors = list(graph[node])
        if len(neighbors) > 2:
            return False
        if len(neighbors) == 2:
            first, second = neighbors
            graph[first].add(second)
            graph[second].add(first)
        for neighbor in neighbors:
            graph[neighbor].remove(node)
        del graph[node]
    return True


class Coupling:
    def __init__(self, dimension, terms):
        self.terms = terms
        codes = np.arange(2**dimension)
        self.vertices = ((codes[:, None] >> np.arange(dimension)) & 1).astype(float)
        self.products = np.array(
            [self.vertices[:, term].prod(axis=1) for term in terms]
        )
        self.eq = csr_matrix(
            np.column_stack(
                [
                    np.vstack([self.vertices.T, np.ones(2**dimension)]),
                    np.zeros(dimension + 1),
                ]
            )
        )

    def solve(self, means):
        upper = np.array([min(means[list(term)]) for term in self.terms])
        lower = np.array(
            [max(0, sum(means[list(term)]) - len(term) + 1) for term in self.terms]
        )
        gaps = upper - lower
        matrix = hstack([csr_matrix(self.products), csr_matrix(gaps[:, None])])
        objective = np.zeros(len(self.vertices) + 1)
        objective[-1] = -1
        result = linprog(
            objective,
            A_ub=matrix,
            b_ub=upper,
            A_eq=self.eq,
            b_eq=np.r_[means, 1],
            bounds=[(0, None)] * len(self.vertices) + [(0, 1)],
            method="highs",
        )
        if not result.success:
            raise RuntimeError(result.message)
        return 1 / result.x[-1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graphs", type=int, default=150)
    parser.add_argument("--points", type=int, default=12)
    args = parser.parse_args()
    rng = np.random.default_rng(410091)
    best = 0.0
    count = 0
    for iteration in range(args.graphs):
        dimension = int(rng.integers(5, 10))
        candidates = [
            term
            for size in range(2, dimension + 1)
            for term in itertools.combinations(range(dimension), size)
        ]
        rng.shuffle(candidates)
        terms = []
        for term in candidates:
            if width_two(terms + [term]):
                terms.append(term)
        solver = Coupling(dimension, terms)
        for point in range(args.points):
            means = rng.choice([0.05, 0.1, 0.2, 1 / 3, 0.5, 2 / 3, 0.8, 0.9, 0.95], dimension)
            if point % 3 == 0:
                means = np.full(dimension, 1 - 1 / dimension)
                selected = rng.choice(dimension, size=int(rng.integers(1, 3)), replace=False)
                means[selected] = rng.choice([1 / dimension, 0.1, 0.2])
            ratio = solver.solve(means)
            count += 1
            if ratio > best + 1e-8:
                best = ratio
                print(json.dumps({"checked": count, "ratio": ratio, "means": means.tolist(), "terms": terms}), flush=True)
    print(json.dumps({"total_checked": count, "largest_ratio": best}), flush=True)


if __name__ == "__main__":
    main()
