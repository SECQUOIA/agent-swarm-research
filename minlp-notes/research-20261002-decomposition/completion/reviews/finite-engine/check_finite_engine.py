"""Independent review checks for exact finite tree computations.

The reference oracle optimizes original bag factors by full enumeration.
For each directed message it removes the corresponding edge, collects the
source component, and enumerates that component independently. It does not
reuse the implementation's message recurrence or projection tables.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
from random import Random
import sys
import unittest

SOLVER = Path(__file__).resolve().parents[3] / "solver"
sys.path.insert(0, str(SOLVER))
from decomposition import build_decomposition, decompose_qp
from finite_dp import prepare_tree, solve_tree


def exhaustive(bags, tables, sizes, selected, fixed):
    variables = sorted({i for u in selected for i in bags[u]})
    free = [i for i in variables if i not in fixed]
    values = {}
    for assignment in product(*(range(sizes[i]) for i in free)):
        point = dict(fixed)
        point.update(zip(free, assignment))
        terms = [tables[u][tuple(point[i] for i in bags[u])] for u in selected]
        if all(term is not None for term in terms):
            values[tuple(point[i] for i in variables)] = sum(terms, F(0))
    return min(values.values(), default=None), values


def side_of_edge(bag_count, edges, source, target):
    remaining = [edge for edge in edges if set(edge) != {source, target}]
    component = {source}
    while True:
        expanded = component | {v for edge in remaining for v in edge
                                if component.intersection(edge)}
        if expanded == component:
            return sorted(component)
        component = expanded


class FiniteEngineReview(unittest.TestCase):
    def assert_reference(self, bags, edges, sizes, tables, home=None):
        result = solve_tree(bags, edges, sizes, tables, home=home)
        expected, values = exhaustive(bags, tables, sizes, range(len(bags)), {})
        self.assertEqual(result["lower"], expected)
        if expected is None:
            self.assertIsNone(result["point_indices"])
        else:
            self.assertEqual(values[result["point_indices"]], expected)
        for i, size in enumerate(sizes):
            margins = tuple(exhaustive(bags, tables, sizes, range(len(bags)),
                                       {i: index})[0] for index in range(size))
            self.assertEqual(result["marginals"][i], margins)
        for edge in edges:
            for source, target in (edge, edge[::-1]):
                component = side_of_edge(len(bags), edges, source, target)
                separator = sorted(set(bags[source]).intersection(bags[target]))
                expected_message = {}
                for assignment in product(*(range(sizes[i]) for i in separator)):
                    expected_message[assignment] = exhaustive(
                        bags, tables, sizes, component,
                        dict(zip(separator, assignment)))[0]
                self.assertEqual(result["messages"][source, target], expected_message)
        self.assertEqual(result["table_states"], sum(map(len, tables)))
        return result

    def test_star_all_roots_homes_and_directed_messages(self):
        # Two-coordinate separators in deliberately different coordinate order;
        # central and leaf factors both forbid states. Some leaves are fixed.
        bags = [(1, 0)] + [(i, 0, 1) for i in range(2, 7)]
        edges = [(0, i) for i in range(1, len(bags))]
        sizes = [2, 3, 1, 2, 2, 1, 2]
        tables = []
        for u, bag in enumerate(bags):
            table = {}
            for state in product(*(range(sizes[i]) for i in bag)):
                x = dict(zip(bag, state))
                invalid = (u == 0 and x[0] == 0 and x[1] == 0)
                invalid |= (u == 1 and x[1] == 2)
                invalid |= (u == 3 and x[0] == 1 and x[4] == 1)
                table[state] = None if invalid else F(
                    sum((i - 3) * (index + 1) for i, index in x.items()), u + 2)
            tables.append(table)
        for root in range(len(bags)):
            order = [root] + [u for u in range(len(bags)) if u != root]
            inverse = {old: new for new, old in enumerate(order)}
            rebags = [bags[u] for u in order]
            reedges = [(inverse[a], inverse[b]) for a, b in reversed(edges)]
            retables = [tables[u] for u in order]
            home = [max(u for u, bag in enumerate(rebags) if i in bag)
                    for i in range(len(sizes))]
            with self.subTest(root=root):
                self.assert_reference(rebags, reedges, sizes, retables, home)

    def test_empty_separator_components_and_empty_factor(self):
        bags = [(), (1, 0), (2,), (3, 2), ()]
        edges = [(0, 1), (0, 2), (2, 3), (0, 4)]
        sizes = [1, 2, 3, 2]
        tables = [{(): F(-3, 7)}, {(0, 0): F(5), (1, 0): F(-1)},
                  {(0,): None, (1,): F(1, 2), (2,): F(-1, 2)},
                  {(x, y): (None if x + y == 2 else F(x - 2 * y, 3))
                   for x, y in product(range(2), range(3))}, {(): F(2, 11)}]
        self.assert_reference(bags, edges, sizes, tables)
        # An infeasible variable-free factor makes the full problem infeasible,
        # but messages directed toward it still describe feasible components.
        tables[4] = {(): None}
        result = self.assert_reference(bags, edges, sizes, tables)
        self.assertIsNotNone(result["messages"][0, 4][()])
        self.assertIsNone(result["messages"][4, 0][()])

    def test_all_global_states_infeasible_two_independent_causes(self):
        bags, edges = [(0,), (0, 1), (2, 0), (0,)], [(0, 1), (0, 2), (0, 3)]
        sizes = [3, 2, 1]
        tables = [{(a,): F(0) for a in range(3)},
                  {(a, b): F(-b, 3) if a == 0 else None
                   for a, b in product(range(3), range(2))},
                  {(0, a): F(2, 3) if a == 1 else None for a in range(3)},
                  {(a,): None if a == 2 else F(1, 5) for a in range(3)}]
        result = self.assert_reference(bags, edges, sizes, tables)
        self.assertTrue(all(value is None for row in result["marginals"] for value in row))
        # Excluding one invalid input can restore feasibility, but two invalid
        # inputs must not cancel each other or turn into a numerical bound.
        self.assertEqual(result["messages"][0, 1][(1,)], F(13, 15))
        self.assertIsNone(result["messages"][0, 1][(2,)])

    def test_zero_variables_and_one_bag(self):
        self.assert_reference([(), (), ()], [(0, 1), (0, 2)], [],
                              [{(): F(-4)}, {(): F(1, 3)}, {(): F(6)}])
        self.assert_reference([(1, 0)], [], [1, 1], [{(0, 0): None}])

    def test_random_intersections_against_edge_deletion_oracle(self):
        rng = Random(907231)
        for trial in range(40):
            bags, edges = [(0,)], []
            for coordinate in range(1, 7):
                parent = rng.randrange(coordinate)
                # A new variable and a subset of its parent's bag preserve
                # connected occurrences without assuming a path or full overlap.
                bag = [i for i in bags[parent] if rng.randrange(3)] + [coordinate]
                rng.shuffle(bag)
                bags.append(tuple(bag))
                edges.append((parent, coordinate))
            sizes = [rng.randrange(1, 4)] + [rng.randrange(1, 3) for _ in range(6)]
            tables = [{state: (None if rng.randrange(7) < 2 else
                              F(rng.randrange(-15, 16), rng.randrange(1, 8)))
                       for state in product(*(range(sizes[i]) for i in bag))}
                      for bag in bags]
            home = [rng.choice([u for u, bag in enumerate(bags) if i in bag])
                    for i in range(len(sizes))]
            with self.subTest(trial=trial):
                self.assert_reference(bags, edges, sizes, tables, home)

    def test_bad_tables_domains_homes_and_reused_layout(self):
        valid = {(0,): F(1), (1,): F(2)}
        bad_tables = [{(0,): F(1)}, {(0,): F(1), (2,): F(2)},
                      {(0, 0): F(1), (1, 0): F(2)},
                      {(False,): F(1), (1,): F(2)},
                      {(0,): F(1), (1,): float("inf")},
                      {(0,): F(1), (1,): True}]
        for table in bad_tables:
            with self.subTest(table=table), self.assertRaises(ValueError):
                solve_tree([(0,)], [], [2], [table])
        for sizes in ([0], [True], [F(2)], [-1]):
            with self.subTest(sizes=sizes), self.assertRaises(ValueError):
                solve_tree([(0,)], [], sizes, [valid])
        with self.assertRaises(ValueError):
            solve_tree([(0,), ()], [(0, 1)], [2], [valid, {(): F(0)}], home=[1])
        with self.assertRaises(ValueError):
            solve_tree([(0,)], [], [2], [valid], layout=prepare_tree([(0,), ()], [(0, 1)], 1))
        with self.assertRaises(ValueError):
            solve_tree([(0,)], [], [2], [valid], home=[False])

    def test_invalid_tree_structures_and_scopes(self):
        examples = [([(0,), (1,), (0,)], [(0, 1), (1, 2)], 2),
                    ([(0,), (1,)], [(0, 0)], 2),
                    ([(0,), (1,), (2,)], [(0, 1), (1, 0)], 3),
                    ([(0,), (1,), (2,), (3,)], [(0, 1), (1, 2), (2, 0)], 4),
                    ([(0, 0)], [], 1), ([(0,)], [], 2)]
        for bags, edges, n in examples:
            with self.subTest(bags=bags, edges=edges), self.assertRaises(ValueError):
                prepare_tree(bags, edges, n)
        for strategy in ("min_fill", "min_degree", "min_table"):
            scopes = [(0, 3, 5), (3, 4), (1,), (), (7, 6), (0, 5)]
            result = build_decomposition(9, scopes, weights=[1, 2, 9, 1, 4, 2, 1, 3, 1],
                                         strategy=strategy)
            # Independent running-intersection check by graph reachability.
            for coordinate in range(9):
                containing = {u for u, bag in enumerate(result["bags"]) if coordinate in bag}
                reached = {next(iter(containing))}
                while True:
                    updated = reached | {v for edge in result["edges"]
                                         if reached.intersection(edge)
                                         for v in edge if v in containing}
                    if updated == reached:
                        break
                    reached = updated
                self.assertEqual(reached, containing)
            self.assertTrue(all(any(set(scope) <= set(bag) for bag in result["bags"])
                                for scope in scopes))
        for scope in [(True,), (0, 0), (9,), (-1,)]:
            with self.subTest(scope=scope), self.assertRaises(ValueError):
                build_decomposition(9, [scope])
        with self.assertRaises(ValueError):
            decompose_qp([[1, 2], [3, 4]])

    def test_check_hook_propagates_abort(self):
        class StopReview(Exception):
            pass
        calls = 0
        def check():
            nonlocal calls
            calls += 1
            if calls == 5:
                raise StopReview()
        with self.assertRaises(StopReview):
            solve_tree([(0,), (0, 1)], [(0, 1)], [2, 2],
                       [{(0,): 0, (1,): 0},
                        {state: 0 for state in product(range(2), repeat=2)}], check=check)
        self.assertEqual(calls, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
