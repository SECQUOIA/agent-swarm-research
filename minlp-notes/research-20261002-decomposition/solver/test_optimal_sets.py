"""Behavioral tests for automatic optimal-set discovery and independent replay."""

import copy
from fractions import Fraction as F
from itertools import product
import json
import unittest

from certified_grid import BoxQP, BudgetExceeded
from optimal_sets import (diagonal_certificate, discover_diagonal_set,
                          recovery_radius, solve_endpoint_set)
from verify_optimal_sets import CertificateError, contains, verify_certificate


def tilted(offset=F(0)):
    direction = [F(1), F(-1), F(1, 2)]
    matrix = [[2 * x * y for y in direction] for x in direction]
    matrix[2][2] -= F(1, 4)
    linear = [-2 * offset * x for x in direction]
    linear[2] += F(1, 8)
    return BoxQP(matrix, linear, [(0, 1)] * 3, [], [(0, 1, 2)], [],
                 constant=offset ** 2)


def permute(problem, order):
    inverse = {old: new for new, old in enumerate(order)}
    return BoxQP([[problem.A[i][j] for j in order] for i in order],
                 [problem.b[i] for i in order], [problem.bounds[i] for i in order],
                 [inverse[i] for i in problem.integers],
                 [tuple(inverse[i] for i in reversed(bag)) for bag in problem.bags],
                 problem.edges, problem.constant)


class EndpointTests(unittest.TestCase):
    def test_branching_support_integer_interior_and_concavity(self):
        # Coupled corners have two components; a free native-integer variable
        # has a billion labels, all represented without enumerating them.
        p = BoxQP([[0, -2, 0, 0, 0], [-2, 0, -2, 0, 0],
                   [0, -2, -2, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 7]],
                  [1, 2, 2, 0, 3], [(0, 1), (0, 1), (0, 1), (0, 10**9), (2, 2)],
                  [3, 4], [(1, 0), (2, 1), (3,), (4,)], [(0, 2), (0, 1), (1, 3)])
        result = solve_endpoint_set(p)
        self.assertEqual(result["status"], "certified")
        cert = json.loads(json.dumps(result["certificate"]))
        self.assertEqual(verify_certificate(cert, p)["minimum"], 20)
        self.assertEqual(result["table_states"], 11)
        for x, y, z, integer in product([F(0), F(1, 2), F(1)], repeat=4):
            point = (x, y, z, int(integer * 10**9), F(2))
            self.assertEqual(contains(cert, point), p.value(point) == 20)
        self.assertTrue(contains(cert, [0, 0, 0, 533357, 2]))
        self.assertFalse(contains(cert, [0, 0, 0, F(1, 3), 2]))
        self.assertFalse(contains(cert, [0, 0, F(1, 2), 533357, 2]))

    def test_permutations_and_actual_subtree_messages(self):
        p = BoxQP([[0, -2, 0, 0], [-2, 0, -2, -2],
                   [0, -2, 0, 0], [0, -2, 0, 0]],
                  [1, 3, 1, 1], [(0, 1)] * 4, [],
                  [(1, 3), (0, 1), (1, 2)], [(0, 2), (2, 1)])
        for order in [(0, 1, 2, 3), (3, 1, 0, 2), (2, 0, 3, 1)]:
            model = permute(p, order)
            cert = solve_endpoint_set(model)["certificate"]
            for point in product([F(0), F(1, 2), F(1)], repeat=4):
                self.assertEqual(contains(cert, point, model), model.value(point) == 0)

    def test_certificate_mutations_and_budget(self):
        p = BoxQP([[0, -2], [-2, 0]], [1, 1], [(0, 1)] * 2, [], [(0, 1)], [])
        cert = solve_endpoint_set(p)["certificate"]
        changes = [lambda c: c["residuals"][0][1].update(value="0"),
                   lambda c: c["messages"][0][0].update(value="-1"),
                   lambda c: c.update(point=["1/2", "1/2"]),
                   lambda c: c["residuals"][0].pop(),
                   lambda c: c["messages"][0].append(c["messages"][0][0]),
                   lambda c: c["residuals"][0][0].update(value=0.0)]
        for change in changes:
            bad = copy.deepcopy(cert)
            change(bad)
            with self.assertRaises(CertificateError):
                verify_certificate(bad, p)
        other = BoxQP(p.A, [2, 2], p.bounds, [], p.bags, p.edges)
        with self.assertRaises(CertificateError):
            verify_certificate(cert, other)
        self.assertEqual(solve_endpoint_set(p, max_table_states=3)["status"], "resource_limit")
        self.assertEqual(solve_endpoint_set(p, time_limit=0)["status"], "resource_limit")


class DiagonalTests(unittest.TestCase):
    def test_tilted_disconnected_continua_full_schedule(self):
        p = tilted()
        result = discover_diagonal_set(p, early_accept=False)
        self.assertEqual(result["status"], "certified")
        self.assertEqual(result["trials"][0]["completed_stages"], result["trials"][0]["required_stages"])
        self.assertGreater(result["trials"][0]["completed_stages"], 10)
        cert = result["certificate"]
        self.assertTrue(contains(cert, [F(2, 3), F(2, 3), 0], p))
        self.assertTrue(contains(cert, [F(1, 3), F(5, 6), 1], p))
        self.assertFalse(contains(cert, [F(1, 3), F(7, 12), F(1, 2)], p))
        self.assertEqual(verify_certificate(cert)["minimum"], 0)

    def test_stationary_lp_finds_unsupplied_rational_optimum(self):
        for offset, order in [(F(1, 3), (0, 1, 2)), (F(2, 7), (2, 0, 1)),
                              (F(-1, 5), (1, 2, 0))]:
            p = permute(tilted(offset), order)
            result = discover_diagonal_set(p)
            self.assertEqual(result["status"], "certified")
            answer = verify_certificate(result["certificate"], p)
            self.assertEqual(answer["minimum"], 0)
            self.assertTrue(any(x.denominator > 1 for x in answer["point"]))

    def test_false_conditioning_does_not_accept_nonglobal_kkt(self):
        p = BoxQP([[2, -3], [-3, 2]], [F(63, 128)] * 2,
                  [(0, 1)] * 2, [], [(0, 1)], [])
        self.assertIsNone(diagonal_certificate(p, [0, 0]))
        failed = discover_diagonal_set(p, max_trials=1)
        self.assertEqual(failed["status"], "inconclusive")
        self.assertNotIn("certificate", failed)
        self.assertEqual(failed["trials"][0]["completed_stages"], failed["trials"][0]["required_stages"])
        result = discover_diagonal_set(p)
        self.assertEqual(result["status"], "certified")
        self.assertGreater(len(result["trials"]), 1)
        self.assertGreater(result["trials"][0]["rejected_candidates"], 0)
        self.assertEqual(verify_certificate(result["certificate"], p)["minimum"], F(-1, 64))

    def test_outside_class_and_resource_limits_are_inconclusive(self):
        # Triangle antiferromagnetic QP: every optimum fails the diagonal test.
        p = BoxQP([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [0] * 3,
                  [(-1, 1)] * 3, [], [(0, 1, 2)], [])
        result = discover_diagonal_set(p, max_trials=1)
        self.assertEqual(result["status"], "inconclusive")
        self.assertEqual(result["reason"], "trial_limit")
        for kwargs, reason in [({"time_limit": 0}, "time_limit"),
                               ({"max_table_states": 1}, "table_limit"),
                               ({"max_stages": 1}, "stage_limit")]:
            limited = discover_diagonal_set(p, **kwargs)
            self.assertEqual(limited["status"], "inconclusive")
            self.assertEqual(limited["reason"], reason)

    def test_fixed_substitution_narrow_bounds_and_all_fixed(self):
        # x2=1/7 shifts the optimum to 3/7; an indefinite fixed row is harmless.
        p = BoxQP([[2, 1], [1, -10]], [-1, 0], [(0, 1), (F(1, 7), F(1, 7))],
                  [], [(0, 1)], [])
        result = discover_diagonal_set(p)
        self.assertEqual(result["status"], "certified")
        self.assertEqual(verify_certificate(result["certificate"])["point"][0], F(3, 7))
        p = BoxQP([[2]], [-F(1, 10**12)], [(0, F(1, 10**12))], [], [(0,)], [])
        self.assertLess(2 * recovery_radius(p), p.bounds[0][1])
        self.assertEqual(discover_diagonal_set(p)["status"], "certified")
        p = BoxQP([[-100]], [7], [(2, 2)], [0], [(0,)], [])
        result = discover_diagonal_set(p)
        self.assertTrue(contains(result["certificate"], [2]))
        self.assertFalse(contains(result["certificate"], [3]))

    def test_psd_corruption_zero_pivot_and_numeric_inputs(self):
        p = tilted()
        cert = discover_diagonal_set(p)["certificate"]
        for change in [lambda c: c["diagonal"].__setitem__(2, "0"),
                       lambda c: c.update(active=[0, 1]),
                       lambda c: c.update(minimum="-1"),
                       lambda c: c["point"].__setitem__(0, 0.0),
                       lambda c: c["diagonal"].__setitem__(0, True)]:
            bad = copy.deepcopy(cert)
            change(bad)
            with self.assertRaises(CertificateError):
                verify_certificate(bad)
        # Zero pivot with nonzero offdiagonal must fail the PSD acceptance.
        p = BoxQP([[0, 1], [1, 0]], [0, 0], [(-1, 1)] * 2, [], [(0, 1)], [])
        self.assertIsNone(diagonal_certificate(p, [0, 0]))
        bad = {"schema": "box-qp-optimal-set-v1", "kind": "diagonal", "problem": p.to_dict(),
               "point": ["0", "0"], "minimum": "0", "active": [0, 1], "diagonal": ["0", "0"]}
        with self.assertRaises(CertificateError):
            verify_certificate(bad)

    def test_verification_cooperative_interrupt(self):
        cert = discover_diagonal_set(tilted())["certificate"]
        def stop():
            raise BudgetExceeded("test")
        with self.assertRaises(BudgetExceeded):
            verify_certificate(cert, check=stop)


if __name__ == "__main__":
    unittest.main()
