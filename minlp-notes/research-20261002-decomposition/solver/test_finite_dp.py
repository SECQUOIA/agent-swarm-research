from fractions import Fraction as F
from itertools import product
from random import Random
import unittest

from decomposition import build_decomposition, decompose_qp
from finite_dp import prepare_tree, solve_tree


class TreeComputationTests(unittest.TestCase):
    def check_reference(self, bags, edges, sizes, tables):
        result = solve_tree(bags, edges, sizes, tables)
        values = {}
        for state in product(*(range(k) for k in sizes)):
            local = [table[tuple(state[i] for i in bag)]
                     for bag, table in zip(bags, tables)]
            if all(x is not None for x in local):
                values[state] = sum(local, F(0))
        self.assertEqual(result["lower"], min(values.values()) if values else None)
        if values:
            self.assertEqual(values[result["point_indices"]], result["lower"])
        else:
            self.assertIsNone(result["point_indices"])
        for i, k in enumerate(sizes):
            expected = tuple(min((v for s, v in values.items() if s[i] == j),
                                 default=None) for j in range(k))
            self.assertEqual(result["marginals"][i], expected)
        return result

    def test_branching_feasible_and_infeasible_marginals(self):
        bags = [(0, 1), (0, 2), (0, 3), (3, 4)]
        edges = [(0, 1), (0, 2), (2, 3)]
        sizes = [3, 2, 2, 3, 2]
        rng = Random(817)
        for _ in range(16):
            tables = [{s: (None if rng.randrange(4) == 0 else
                           F(rng.randrange(-9, 10), rng.randrange(1, 5)))
                       for s in product(*(range(sizes[i]) for i in bag))}
                      for bag in bags]
            self.check_reference(bags, edges, sizes, tables)

    def test_excluding_infeasible_incoming_message(self):
        # Each leaf forbids a different root value, so the whole tree is
        # infeasible. Excluding a leaf must remove its infinity correctly.
        bags, edges = [(0,), (0, 1), (0, 2)], [(0, 1), (0, 2)]
        tables = [{(0,): F(0), (1,): F(0)},
                  {(a, b): F(b) if a == 0 else None for a, b in product(range(2), repeat=2)},
                  {(a, b): F(b) if a == 1 else None for a, b in product(range(2), repeat=2)}]
        result = self.check_reference(bags, edges, [2, 2, 2], tables)
        self.assertEqual(result["messages"][0, 1], {(0,): None, (1,): F(0)})
        self.assertEqual(result["messages"][0, 2], {(0,): F(0), (1,): None})

    def test_empty_separators_and_fixed_coordinates(self):
        self.check_reference([(0,), (1,), (2,)], [(0, 1), (0, 2)], [1, 2, 2],
                             [{(0,): F(3)}, {(0,): F(-2), (1,): F(4)},
                              {(0,): None, (1,): F(1, 7)}])
        self.check_reference([()], [], [], [{(): F(2, 3)}])

    def test_invalid_structures_and_inexact_cost(self):
        with self.assertRaises(ValueError):
            prepare_tree([(0,), (1,), (0,)], [(0, 1), (1, 2)], 2)
        with self.assertRaises(ValueError):
            solve_tree([(0,)], [], [2], [{(0,): F(1)}])
        with self.assertRaises(ValueError):
            solve_tree([(0,)], [], [1], [{(0,): 0.1}])
        with self.assertRaises(ValueError):
            solve_tree([(0,)], [], [1], [{(0,): True}])

    def test_decomposition_scopes_and_permutations(self):
        rng = Random(913)
        for n in (1, 5, 10, 18):
            scopes = [tuple(sorted(rng.sample(range(n), min(3, n)))) for _ in range(n)]
            for strategy in ("min_fill", "min_degree", "min_table"):
                result = build_decomposition(n, scopes, weights=[1 + i % 4 for i in range(n)],
                                             strategy=strategy)
                prepare_tree(result["bags"], result["edges"], n)
                self.assertTrue(all(any(set(s) <= set(b) for b in result["bags"])
                                    for s in scopes))
                self.assertEqual(len(result["order"]), n)

    def test_path_and_disconnected_decompositions(self):
        A = [[int(abs(i-j) == 1) for j in range(40)] for i in range(40)]
        self.assertEqual(decompose_qp(A)["width"], 1)
        self.assertEqual(build_decomposition(8, [()])["width"], 0)
        self.assertEqual(build_decomposition(0, [()])["bags"], [()])
        with self.assertRaises(ValueError):
            build_decomposition(3, [(0, 4)])


if __name__ == "__main__":
    unittest.main()
