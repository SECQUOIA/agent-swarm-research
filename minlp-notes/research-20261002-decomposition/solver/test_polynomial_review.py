"""Independent adversarial checks for explicit-factor polynomial certificates."""

from copy import deepcopy
from fractions import Fraction as F
from itertools import product
from math import comb
from random import Random
import unittest
from unittest.mock import patch

import polynomial_grid as producer
from certified_grid import BudgetExceeded
from polynomial_grid import (PolynomialBox, PolynomialFactor, integer_value_denominator,
                             polynomial_grid_dp, solve)
from verify_certificate import CertificateError
from verify_polynomial import polynomial_interval, verify_polynomial


def shifted_power(a, degree):
    return [(F(comb(degree, p)) * (-a) ** (degree - p), (p,))
            for p in range(degree + 1)]


class PolynomialIndependentReview(unittest.TestCase):
    def test_brute_force_corrected_dp_and_all_marginals(self):
        rng = Random(60403)
        for case in range(24):
            factors = []
            for i in range(4):
                factors.append(PolynomialFactor((i,), [
                    (F(rng.randint(-4, 4), 3), (degree,)) for degree in range(5)]))
            for i in range(3):
                factors.append(PolynomialFactor((i, i + 1), [
                    (F(rng.randint(-4, 4), 5), powers)
                    for powers in ((1, 1), (2, 1), (1, 2), (2, 2))]))
            problem = PolynomialBox([(-1, 2)] * 4, factors, integers=(1,),
                                    bags=((0, 1), (1, 2), (2, 3)), edges=((0, 1), (1, 2)))
            grids = ((F(-1), F(0), F(2)),) * 4
            penalties = tuple(tuple(F(rng.randrange(5), 7) for _ in row) for row in grids)
            result = polynomial_grid_dp(problem, grids, penalties)
            costs = {state: problem.value(tuple(grids[i][k] for i, k in enumerate(state)))
                     - sum(penalties[i][k] for i, k in enumerate(state))
                     for state in product(range(3), repeat=4)}
            self.assertEqual(result['lower'], min(costs.values()), case)
            for i, row in enumerate(result['marginals']):
                for k, value in enumerate(row):
                    self.assertEqual(value, min(v for s, v in costs.items() if s[i] == k))

    def test_exact_intervals_enclose_manual_derivatives(self):
        # -3 x^4 y^3 + 5 x^2 y - 7 y^2 + 11, with an interval crossing zero.
        problem = PolynomialBox([(-2, 1), (-1, 3)], [PolynomialFactor((0, 1), [
            (-3, (4, 3)), (5, (2, 1)), (-7, (0, 2)), (11, (0, 0))])])
        formulas = {(): lambda x, y: -3*x**4*y**3 + 5*x*x*y - 7*y*y + 11,
                    (0,): lambda x, y: -12*x**3*y**3 + 10*x*y,
                    (1,): lambda x, y: -9*x**4*y*y + 5*x*x - 14*y,
                    (0, 0): lambda x, y: -36*x*x*y**3 + 10*y,
                    (0, 1): lambda x, y: -36*x**3*y*y + 10*x,
                    (1, 1): lambda x, y: -18*x**4*y - 14}
        for indices, formula in formulas.items():
            lo, hi = problem.derivative_bounds(indices)
            self.assertEqual((lo, hi), polynomial_interval(problem, problem.bounds, indices))
            for x, y in product((F(k, 4) for k in range(-8, 5)),
                                (F(k, 4) for k in range(-4, 13))):
                self.assertLessEqual(lo, formula(x, y))
                self.assertLessEqual(formula(x, y), hi)

    def test_known_mixed_polynomial_optimum_survives_all_filters(self):
        optimum = (F(1, 3), F(1), F(-1, 2))
        factors = [PolynomialFactor((i,), shifted_power(a, 2) + shifted_power(a, 4))
                   for i, a in enumerate(optimum)]
        for i in range(2):
            terms = [(c*d/F(10), (p[0], q[0]))
                     for c, p in shifted_power(optimum[i], 2)
                     for d, q in shifted_power(optimum[i+1], 2)]
            factors.append(PolynomialFactor((i, i+1), terms))
        problem = PolynomialBox([(-1, 2)] * 3, factors, integers=(1,))
        self.assertEqual(problem.value(optimum), 0)
        cert = solve(problem, F(1, 10000), max_stages=10, max_table_states=10000, time_limit=30)
        self.assertGreaterEqual(len(cert['stages']), 3)
        self.assertTrue(verify_polynomial(cert)['valid'])
        self.assertLessEqual(F(cert['lower']), 0)
        self.assertGreaterEqual(F(cert['upper']), 0)
        for stage in cert['stages']:
            self.assertTrue(all(F(lo) <= x <= F(hi)
                                for x, (lo, hi) in zip(optimum, stage['next_bounds'])))

    def test_zero_cap_endpoint_reduction_matches_dense_corner_oracle(self):
        # Negative quartics/quadratics and bilinear terms are concave in each
        # coordinate, including on native integer coordinates.
        rng = Random(6001)
        for _ in range(10):
            factors = [PolynomialFactor((i,), [(-i-1, (4,)), (-1, (2,))]) for i in range(4)]
            factors += [PolynomialFactor((i,j), [(rng.randrange(-3,4), (1,1))])
                        for i in range(4) for j in range(i+1,4)]
            problem = PolynomialBox([(-1, 2)]*4, factors, integers=(1,3))
            cert = solve(problem, F(1,100), max_stages=2, time_limit=10)
            expected = min(problem.value(x) for x in product((F(-1), F(2)), repeat=4))
            self.assertEqual(F(cert['lower']), expected)
            self.assertEqual(F(cert['upper']), expected)
            self.assertEqual(cert['status'], 'exact')
            self.assertEqual(cert['curvature']['caps'], ['0']*4)
            self.assertTrue(verify_polynomial(cert)['valid'])

    def test_native_integer_complete_grid_matches_enumeration(self):
        problem = PolynomialBox([(-2, 3), (-1, 2)], [
            PolynomialFactor((0,), [(1,(4,)), (-2,(2,)), (-1,(1,))]),
            PolynomialFactor((1,), [(1,(4,)), (2,(1,))]),
            PolynomialFactor((0,1), [(1,(1,1))])], integers=(0,1))
        cert = solve(problem, 0, max_stages=12, time_limit=20)
        expected = min(problem.value(x) for x in product(range(-2,4), range(-1,3)))
        self.assertEqual(cert['status'], 'exact')
        self.assertEqual(F(cert['lower']), expected)
        self.assertEqual(F(cert['upper']), expected)
        self.assertTrue(verify_polynomial(cert)['valid'])

    def test_shifted_skipped_integer_intervals_retain_interior_optimum(self):
        problem = PolynomialBox([(F(-5,2), F(19,2))], [PolynomialFactor(
            (0,), shifted_power(F(4), 4) + shifted_power(F(4), 2))], integers=(0,))
        self.assertEqual(problem.bounds, ((F(-2), F(9)),))
        cert = solve(problem, F(1,10**6), max_stages=6, time_limit=10)
        first_grid = tuple(map(F, cert['stages'][0]['grids'][0]))
        self.assertNotIn(F(4), first_grid)
        self.assertTrue(any(a < 4 < b and b-a > 1 for a,b in zip(first_grid,first_grid[1:])))
        for stage in cert['stages']:
            lo, hi = map(F, stage['next_bounds'][0])
            self.assertLessEqual(lo, 4)
            self.assertLessEqual(4, hi)
        self.assertTrue(verify_polynomial(cert)['valid'])

    def test_flat_zero_cap_coordinate_keeps_full_unknown_optimal_set(self):
        problem = PolynomialBox([(0,1), (-7,13)], [PolynomialFactor(
            (0,), shifted_power(F(1,3), 2))], integers=(1,))
        cert = solve(problem, F(1,10**6), max_stages=5, time_limit=10)
        self.assertGreater(len(cert['stages']), 1)
        for stage in cert['stages']:
            self.assertEqual(stage['grids'][1], ['-7','13'])
            self.assertEqual(stage['next_bounds'][1], ['-7','13'])
        self.assertTrue(verify_polynomial(cert)['valid'])

    def test_integer_value_lattice_substitutes_fixed_rationals(self):
        # A normal geometric solve reaches a gap smaller than its rational
        # value spacing before the corrected-grid lower bound becomes exact.
        coefficients = [(-3,(0,0)), (-3,(0,1)), (3,(0,2)),
                        (7,(1,0)), (-2,(1,1)), (-5,(2,0))]
        problem = PolynomialBox([(-3,6), (-2,7), (F(1,3),F(1,3))], [PolynomialFactor(
            (0,1,2), [(F(c,2), powers+(2,)) for c,powers in coefficients])], integers=(0,1))
        self.assertEqual(integer_value_denominator(problem), 18)
        cert = solve(problem, 0, max_stages=6, time_limit=10)
        self.assertEqual(len(cert['stages']), 2)
        self.assertEqual(cert['integer_lattice'], {'denominator':18, 'lower_before':'-71/8'})
        self.assertEqual(cert['status'], 'exact')
        self.assertEqual(cert['lower'], '-53/6')
        expected = min(problem.value((F(x), F(y), F(1,3)))
                       for x,y in product(range(-3,7),range(-2,8)))
        self.assertEqual(F(cert['lower']), expected)
        self.assertTrue(verify_polynomial(cert, expected_problem=problem)['valid'])
        for key, value in (('denominator',9), ('denominator',True), ('lower_before','0')):
            forged = deepcopy(cert)
            forged['integer_lattice'][key] = value
            with self.assertRaises(CertificateError):
                verify_polynomial(forged)

    def test_lattice_requires_strict_separation_and_no_varying_continuous_coordinate(self):
        integer_problem = PolynomialBox([(0,1)], [PolynomialFactor(
            (0,), [(1,(2,)),(-1,(1,))])], integers=(0,))
        cert = solve(integer_problem, 0, max_stages=0)
        self.assertEqual(cert['lower'], '-1')
        self.assertEqual(cert['upper'], '0')
        self.assertNotIn('integer_lattice', cert)
        forged = deepcopy(cert)
        forged.update(integer_lattice={'denominator':1, 'lower_before':'-1'},
                      lower='0', gap='0', status='exact')
        with self.assertRaises(CertificateError):
            verify_polynomial(forged)
        continuous_problem = PolynomialBox([(0,1)], [PolynomialFactor(
            (0,), [(1,(2,)),(-F(2,3),(1,))])])
        self.assertIsNone(integer_value_denominator(continuous_problem))
        forged = solve(continuous_problem, 0, max_stages=0)
        forged.update(integer_lattice={'denominator':1, 'lower_before':forged['lower']},
                      lower=forged['upper'], gap='0', status='exact')
        with self.assertRaises(CertificateError):
            verify_polynomial(forged)

    def test_limits_and_interrupted_trial_restart_keep_last_verified_box(self):
        problem = PolynomialBox([(0,1)], [PolynomialFactor((0,), [(1,(2,)), (-F(2,3),(1,))])])
        for options, expected in (({'max_stages':0}, 'stage_limit'),
                                  ({'time_limit':0}, 'time_limit'),
                                  ({'max_table_states':1}, 'table_limit')):
            cert = solve(problem, F(1,10**6), **options)
            self.assertEqual(cert['status'], expected)
            self.assertTrue(verify_polynomial(cert)['valid'])
        original, calls = producer.coordinate_grid, 0
        def interrupt(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 4:
                raise BudgetExceeded('trial_grid_limit')
            if calls == 5:
                raise BudgetExceeded('time_limit')
            return original(*args, **kwargs)
        with patch.object(producer, 'coordinate_grid', interrupt):
            cert = solve(problem, F(1,10**6), max_stages=10, time_limit=10)
        self.assertEqual(cert['status'], 'time_limit')
        self.assertEqual(len(cert['stages']), 3)
        self.assertEqual(cert['retained_bounds'], [['0', '1/2']])
        self.assertTrue(verify_polynomial(cert)['valid'])

    def test_malformed_certificates_are_rejected(self):
        problem = PolynomialBox([(0,1)]*2, [
            PolynomialFactor((0,), [(1,(4,)), (-F(2,3),(1,))]),
            PolynomialFactor((1,), [(1,(2,)), (-F(1,5),(1,))])],
            bags=((0,), (1,)), edges=((0,1),))
        cert = solve(problem, F(1,10**6), max_stages=4, time_limit=10)
        self.assertTrue(verify_polynomial(cert)['valid'])
        mutations = [
            lambda c: c['curvature']['caps'].__setitem__(0, '0'),
            lambda c: c['curvature']['diagonal_bounds'][0].__setitem__(1, '0'),
            lambda c: c['initial'].__setitem__('lower', '100'),
            lambda c: c['stages'][0]['grids'][0].__setitem__(0, '1/10'),
            lambda c: c['stages'][0]['messages'][0]['rows'][0].__setitem__('value','100'),
            lambda c: c['stages'][0]['min_marginals'][0].__setitem__(0, '100'),
            lambda c: c['stages'][0].__setitem__('grid_lower', '100'),
            lambda c: c['stages'][0].__setitem__('grid_point', ['7','7']),
            lambda c: c['stages'][0].__setitem__('next_bounds', [['0','0'],['0','0']]),
            lambda c: c.__setitem__('retained_bounds', [['0','0'],['0','0']]),
            lambda c: c.__setitem__('status', 'exact'),
            lambda c: c.__setitem__('point', ['7','7']),
            lambda c: c['options'].__setitem__('pruning', 1),
        ]
        for number, mutate in enumerate(mutations):
            changed = deepcopy(cert)
            mutate(changed)
            with self.assertRaises(CertificateError, msg=f'mutation {number}'):
                verify_polynomial(changed)


if __name__ == '__main__':
    unittest.main()
