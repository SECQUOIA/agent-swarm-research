"""Bounded TU-row-partition search using the Ghouila-Houri criterion.

The oracle enumerates every subset of columns and every signing (up to global
sign). A failed signing problem supplies a row obstruction for exact coloring.
This is feasible only in small column dimension; it is not a general TU test.
"""

import argparse
import itertools
import json
import random

import numpy as np

from search_multilinear_balanced_partition import odd_holes
from search_multilinear_treewidth_three_partition import width_certificate


def coloring(clauses, count, colors):
    assignment = [None] * count

    def visit():
        unresolved = []
        for clause in clauses:
            used = {assignment[v] for v in clause if assignment[v] is not None}
            if len(used) >= 2:
                continue
            missing = [v for v in clause if assignment[v] is None]
            if not missing:
                return False
            unresolved.append(missing)
        if not unresolved:
            return True
        smallest = min(unresolved, key=len)
        variable = max(smallest, key=lambda v: sum(v in c for c in unresolved))
        for color in range(colors):
            assignment[variable] = color
            if visit():
                return True
        assignment[variable] = None
        return False

    return [0 if c is None else c for c in assignment] if visit() else None


class TUOracle:
    def __init__(self, terms, dimension):
        if len(terms) > 63:
            raise ValueError("The bounded oracle uses a 63-bit row set")
        matrix = np.zeros((len(terms), dimension), dtype=np.int16)
        for row, term in enumerate(terms):
            matrix[row, list(term)] = 1
        row_bits = np.left_shift(np.uint64(1), np.arange(len(terms), dtype=np.uint64))
        self.groups = []
        for size in range(3, dimension + 1):
            codes = np.arange(2 ** (size - 1))
            signs = np.ones((len(codes), size), dtype=np.int16)
            signs[:, 1:] -= 2 * ((codes[:, None] >> np.arange(size - 1)) & 1)
            for columns in itertools.combinations(range(dimension), size):
                violated = np.abs(signs @ matrix[:, columns].T) > 1
                masks = tuple(int(v) for v in (violated * row_bits).sum(axis=1))
                self.groups.append((columns, masks))

    def obstruction(self, selected):
        row_mask = sum(1 << row for row in selected)
        for columns, masks in self.groups:
            if any(row_mask & mask == 0 for mask in masks):
                continue
            minimal = list(selected)
            for row in selected:
                trial = row_mask ^ (1 << row)
                if all(trial & mask for mask in masks):
                    row_mask = trial
                    minimal.remove(row)
            return frozenset(minimal), columns
        return None


def partition(terms, dimension, colors):
    clauses = list(odd_holes(terms))
    oracle = TUOracle(terms, dimension)
    extra = []
    while True:
        candidate = coloring(clauses, len(terms), colors)
        if candidate is None:
            return None, extra
        added = False
        for color in range(colors):
            selected = [row for row, label in enumerate(candidate) if label == color]
            obstruction = oracle.obstruction(selected)
            if obstruction is not None:
                rows, columns = obstruction
                clauses.append(rows)
                extra.append({"rows": sorted(rows), "columns": columns})
                added = True
        if not added:
            return candidate, extra


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graphs", type=int, default=300)
    parser.add_argument("--width", type=int, default=3)
    parser.add_argument("--colors", type=int, default=3)
    args = parser.parse_args()
    rng = random.Random(941081)
    additional = 0
    for instance in range(args.graphs):
        dimension = rng.randrange(5, 10)
        candidates = [term for size in range(2, dimension + 1)
                      for term in itertools.combinations(range(dimension), size)]
        rng.shuffle(candidates)
        terms = []
        for term in candidates:
            if width_certificate(terms + [term], args.width):
                terms.append(term)
        answer, extra = partition(terms, dimension, args.colors)
        additional += len(extra)
        if answer is None:
            print(json.dumps({"counterexample": terms, "dimension": dimension,
                              "tu_obstructions": extra}), flush=True)
            return
        if (instance + 1) % 25 == 0:
            print(json.dumps({"checked": instance + 1, "tu_obstructions_added": additional}), flush=True)
    print(json.dumps({"total_checked": args.graphs, "counterexamples": 0,
                      "tu_obstructions_added": additional}), flush=True)


if __name__ == "__main__":
    main()
