"""Targeted regression tests for output distinctions and rejected false premises."""

from fractions import Fraction as Q
import unittest

from output_contracts import (ConvexityCertificate, Domain, EvenPower, Polynomial, Problem,
                              Witness, affine, error_bound, gradient_coefficient_rows,
                              minimum_norm_parameters, rank_and_kernel, regularize,
                              value_report, verify_distance_to_set, verify_minimum_norm,
                              verify_value_gap)


def problem(powers, lower, upper, linear=None, offset=0, inequalities=()):
    n = len(lower)
    certificate = ConvexityCertificate(tuple(linear or (0,) * n), offset, tuple(powers))
    return Problem(certificate.expand(n), certificate, Domain(lower, upper, inequalities))


class OutputContractsTests(unittest.TestCase):
    def test_nonunique_optimum_separates_set_and_fixed_selector(self):
        model = problem([EvenPower(1, (1, 0), 0, 2)], (-1, -1), (1, 1))
        arbitrary_optimizer = Witness((0, 1), (0, 1))
        self.assertEqual(verify_distance_to_set(model, arbitrary_optimizer, Q(1, 100)).gap_bound, 0)
        with self.assertRaisesRegex(ValueError, "objective gap"):
            verify_minimum_norm(model, arbitrary_optimizer, Q(1, 100))
        self.assertEqual(verify_minimum_norm(model, Witness((0, 0), (0, 0)), Q(1, 100)).gap_bound, 0)

    def test_tiny_gap_does_not_certify_small_point_distance(self):
        model = problem([EvenPower(Q(1, 2 ** 80), (1,), 0, 2)], (0,), (1,))
        witness = Witness((1,), (0,))
        self.assertEqual(verify_value_gap(model, witness, Q(1, 2 ** 80)).gap_bound, Q(1, 2 ** 80))
        with self.assertRaisesRegex(ValueError, "objective gap"):
            verify_distance_to_set(model, witness, Q(1, 2))
        # This fixture's optimizer is exactly zero; its candidate is distance one.
        self.assertEqual(model.objective.evaluate((0,)), 0)

    def test_tangent_bound_is_derived_and_can_have_nonfeasible_anchor(self):
        model = problem([EvenPower(1, (1,), 0, 2)], (1,), (2,))
        self.assertEqual(value_report(model, Witness((1,), (1,))).lower_bound, 1)
        outside = value_report(model, Witness((1,), (-1,)))
        self.assertEqual(outside.lower_bound, -5)
        self.assertEqual(outside.gap_bound, 6)
        with self.assertRaisesRegex(ValueError, "objective gap"):
            verify_value_gap(model, Witness((1,), (-1,)), 0)

    def test_false_convexity_and_infeasible_points_are_rejected(self):
        valid = problem([EvenPower(1, (1,), 0, 2)], (-1,), (1,))
        forged = Problem(valid.objective.scale(-1), valid.convexity, valid.domain)
        with self.assertRaisesRegex(ValueError, "does not equal"):
            value_report(forged, Witness((0,), (0,)))
        for bad_factor in [EvenPower(-1, (1,), 0, 2), EvenPower(1, (1,), 0, 3)]:
            with self.assertRaisesRegex(ValueError, "nonnegative weight"):
                problem([bad_factor], (-1,), (1,))
        with self.assertRaisesRegex(ValueError, "outside"):
            value_report(valid, Witness((2,), (0,)))
        sliced = problem([], (-1, -1), (1, 1), inequalities=(((1, 1), 0),))
        with self.assertRaisesRegex(ValueError, "polyhedral constraint"):
            value_report(sliced, Witness((1, 0), (0, 0)))

    def test_sparse_gradient_kernel_includes_affine_slope(self):
        p = affine((1, -2, 0), 3).power(4) + affine((0, 0, 1))
        rows = gradient_coefficient_rows(p)
        rank, kernel = rank_and_kernel(rows, 3)
        self.assertEqual(rank, 2)
        self.assertEqual(kernel, ((Q(2), Q(1), Q(0)),))
        for x in [(0, 0, 0), (Q(2, 3), -2, Q(1, 7))]:
            shifted = tuple(a + 5 * b for a, b in zip(x, kernel[0]))
            self.assertEqual(p.evaluate(x), p.evaluate(shifted))
        self.assertEqual(rank_and_kernel(gradient_coefficient_rows(affine((0, 0), 7)), 2),
                         (0, ((Q(1), Q(0)), (Q(0), Q(1)))))

    def test_sparse_constant_and_affine_cases_have_finite_effective_bounds(self):
        constant = problem([], (0, 0), (1, 1), offset=3)
        degree, gamma = error_bound(constant)
        self.assertEqual(degree, 2)
        self.assertGreaterEqual(gamma, 1)
        verify_minimum_norm(constant, Witness((0, 0), (0, 0)), Q(1, 10))
        linear = problem([], (0,), (1,), linear=(1,))
        verify_distance_to_set(linear, Witness((0,), (0,)), Q(1, 10))

    def test_regularized_nonzero_selector_and_rational_rounding_budget(self):
        model = problem([EvenPower(1, (1, 0), -1, 2)], (0, -1), (2, 1))
        epsilon = Q(1, 4)
        tau, eta = minimum_norm_parameters(model, epsilon)
        exact_regularized_x = 1 / (1 + tau)
        # The fixed original minimum-norm optimizer is (1,0), not the
        # regularized optimizer. An exact rational regularized point is valid.
        witness = Witness((exact_regularized_x, 0), (exact_regularized_x, 0))
        self.assertEqual(verify_minimum_norm(model, witness, epsilon).gap_bound, 0)
        self.assertLessEqual(abs(exact_regularized_x - 1), epsilon)
        # A rational perturbation is accepted only after its own tangent gap
        # is verified; no floating-point coordinate comparison substitutes.
        displacement = eta / (2 * (1 + tau))
        rounded = Witness((exact_regularized_x + displacement, 0), witness.tangent_anchor)
        report = verify_minimum_norm(model, rounded, epsilon)
        self.assertEqual(report.gap_bound, (1 + tau) * displacement ** 2)
        self.assertEqual(regularize(model, tau).objective.evaluate(witness.point), report.lower_bound)

    def test_lower_dimensional_domain_and_bound_to_model(self):
        model = problem([EvenPower(1, (1, 0), 0, 4)], (-1, -1), (1, 1),
                        inequalities=(((0, 1), 0), ((0, -1), 0)))
        verify_minimum_norm(model, Witness((0, 0), (0, 0)), Q(1, 8))
        scaled = problem([EvenPower(Q(1, 31), (1, 0), 0, 4)], (-1, -1), (1, 1))
        self.assertNotEqual(error_bound(model), error_bound(scaled))

    def test_box_tangent_rejection_does_not_disprove_optimality(self):
        model = problem([], (-1, -1), (1, 1), linear=(1, 1),
                        inequalities=(((-1, -1), -1),))
        # Every feasible point satisfies x+y>=1; (1,0) is an exact optimizer.
        # Its affine tangent over the whole box has lower bound -2.
        report = value_report(model, Witness((1, 0), (1, 0)))
        self.assertEqual(report.value, 1)
        self.assertEqual(report.lower_bound, -2)
        with self.assertRaisesRegex(ValueError, "objective gap"):
            verify_value_gap(model, Witness((1, 0), (1, 0)), Q(1, 100))

    def test_no_float_or_malformed_precision_inputs(self):
        with self.assertRaises(TypeError):
            affine((0.1,))
        with self.assertRaises(ValueError):
            Polynomial(1, (((-1,), 1),))
        model = problem([], (0,), (1,))
        for epsilon in [0, -1, 2]:
            with self.assertRaisesRegex(ValueError, "point tolerance"):
                verify_distance_to_set(model, Witness((0,), (0,)), epsilon)


if __name__ == "__main__":
    unittest.main()
