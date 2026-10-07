"""Exact-output contracts: rational safety, recovery, limits, and corruption."""

from copy import deepcopy
from fractions import Fraction as F
import json
import unittest
from unittest.mock import patch

from certified_grid import BoxQP, Budget, solve
from exact_output import _stationary_candidate, rational_heights, solve_exact
from verify_certificate import CertificateError, verify_certificate


def rational_face():
    # For fixed x, y -> F(x,y) is concave; compare y=0 and y=2.
    # Unique optimum (1/6,2), value -145/36, on an indefinite face.
    return BoxQP([[2, 1], [1, -2]], [F(-7, 3), 0], [(0, 1), (0, 2)],
                 [], [(0, 1)], [])


class ExactOutputTests(unittest.TestCase):
    def test_nonconvex_rational_face_recovered_without_polishing(self):
        problem = rational_face()
        certificate = solve_exact(problem, convex_presolve=False, polish_sweeps=0,
                                  time_limit=5)
        self.assertEqual(certificate['status'], 'exact')
        self.assertEqual(certificate['point'], ['1/6', '2'])
        self.assertEqual(certificate['upper'], '-145/36')
        self.assertTrue(certificate['feasible_proposals'])
        self.assertEqual(certificate['proof']['kind'], 'rational_value_separation')
        self.assertTrue(verify_certificate(json.loads(json.dumps(certificate)))['exact'])

    def test_mixed_integer_exact_fractional_optimizer(self):
        # (x-y)^2+(y-1/3)^2 with integer x.
        problem = BoxQP([[2, -2], [-2, 4]], [0, F(-2, 3)], [(-1, 1)] * 2,
                        [0], [(0, 1)], [], constant=F(1, 9))
        certificate = solve_exact(problem, time_limit=5)
        self.assertEqual(certificate['point'], ['0', '1/6'])
        self.assertEqual(certificate['lower'], '1/18')
        self.assertTrue(verify_certificate(certificate)['exact'])

    def test_direct_equality_covers_all_integer_and_tied_endpoints(self):
        for integers in ([], [0]):
            problem = BoxQP([[-2]], [1], [(0, 1)], integers, [(0,)], [])
            certificate = solve_exact(problem, convex_presolve=False)
            self.assertEqual(certificate['proof']['kind'], 'equal_bounds')
            self.assertEqual(certificate['gap'], '0')
            self.assertTrue(verify_certificate(certificate)['exact'])

    def test_rational_fixed_coordinates_enter_original_height(self):
        # Fixed endpoint denominator 7 enters free optimum x=2/21.
        problem = BoxQP([[6, -4], [-4, 0]], [0, 0], [(0, 1), (F(1, 7), F(1, 7))],
                        [], [(0, 1)], [], constant=F(1, 5))
        height = rational_heights(problem)
        certificate = solve_exact(problem, convex_presolve=False, time_limit=5)
        self.assertEqual(certificate['point'], ['2/21', '1/7'])
        self.assertEqual(height['denominator'], 35)
        self.assertLessEqual(F(certificate['upper']).denominator, height['value'])
        self.assertTrue(verify_certificate(certificate)['exact'])

    def test_singular_face_recovery_uses_bounded_linear_feasibility(self):
        # (x-y-1/3)^2; both supplied coordinates are interior, so the free
        # Hessian is singular and recovery must retain the box inequalities.
        problem = BoxQP([[2, -2], [-2, 2]], [F(-2, 3), F(2, 3)], [(-1, 1)] * 2,
                        [], [(0, 1)], [], constant=F(1, 9))
        candidate = _stationary_candidate(problem, (F(1, 2), F(1, 6)),
                                          rational_heights(problem), Budget(5), 100)
        self.assertTrue(problem.feasible(candidate))
        self.assertEqual(problem.value(candidate), 0)
        certificate = solve_exact(problem, time_limit=5)
        self.assertTrue(verify_certificate(certificate)['exact'])

    def test_nonunique_mixed_segments_return_an_exact_point(self):
        # The optimal set contains two whole diagonal segments, at z=0,1.
        # The full Hessian is indefinite; convex presolve cannot explain this.
        problem = BoxQP([[2, -2, 0], [-2, 2, 0], [0, 0, -2]], [0, 0, 1],
                        [(0, 1)] * 3, [2])
        certificate = solve_exact(problem, convex_presolve=False, polish_sweeps=0,
                                  time_limit=5)
        self.assertTrue(verify_certificate(certificate)['exact'])
        point = tuple(map(F, certificate['point']))
        self.assertEqual(point[0], point[1])
        self.assertIn(point[2], (0, 1))
        self.assertEqual(certificate['upper'], '0')

    def test_near_set_recovery_with_extra_snaps_and_fixed_rational_coordinate(self):
        # F=(x-y)^2+(z-2t)^2, integer z and fixed t=1/2. The
        # continuous optimum is a line; nearby points can select extra bounds.
        problem = BoxQP([[2, -2, 0, 0], [-2, 2, 0, 0],
                         [0, 0, 2, -4], [0, 0, -4, 8]], [0] * 4,
                        [(0, 1), (0, 1), (0, 2), (F(1, 2), F(1, 2))], [2])
        heights = rational_heights(problem)
        tau = F(1, 4 * 4 * heights['coordinate'])
        for nearby in ((tau / 4, tau / 3, F(1), F(1, 2)),
                       (1 - tau / 4, 1 - tau / 3, F(1), F(1, 2)),
                       (F(2, 5) + tau / 8, F(2, 5), F(1), F(1, 2))):
            recovered = _stationary_candidate(problem, nearby, heights, Budget(5), 100)
            self.assertTrue(problem.feasible(recovered))
            self.assertEqual(problem.value(recovered), 0)

    def test_all_limits_preserve_verified_bounds(self):
        for options, expected in (({'time_limit': 0}, 'time_limit'),
                                  ({'max_stages': 0}, 'stage_limit'),
                                  ({'max_table_states': 1}, 'table_limit'),
                                  ({'max_rounds': 1}, 'round_limit')):
            certificate = solve_exact(rational_face(), convex_presolve=False, **options)
            self.assertEqual(certificate['status'], expected)
            self.assertFalse(verify_certificate(certificate)['exact'])
            self.assertLessEqual(F(certificate['lower']), F(-145, 36))
            self.assertGreaterEqual(F(certificate['upper']), F(-145, 36))
        certificate = solve_exact(rational_face(), max_stages=7, convex_presolve=False)
        self.assertLessEqual(certificate['stats']['attempted_stages'], 7)
        self.assertTrue(verify_certificate(certificate)['valid'])

    def test_unsafe_stationary_candidate_cannot_pass_global_gate(self):
        # (1,0) is a nonglobal box KKT point of this indefinite problem.
        with patch('exact_output._candidates', return_value=iter([('bad', (F(1), F(0)))])):
            certificate = solve_exact(rational_face(), convex_presolve=False,
                                      polish_sweeps=0, max_rounds=1)
        self.assertNotEqual(certificate['status'], 'exact')
        self.assertLessEqual(F(certificate['upper']), F(-4))
        self.assertTrue(verify_certificate(certificate)['valid'])

    def test_tampered_height_candidate_problem_and_separation_fail(self):
        certificate = solve_exact(rational_face(), convex_presolve=False, time_limit=5)
        mutations = [
            lambda c: c['heights'].__setitem__('value', '1'),
            lambda c: c['proof'].__setitem__('point', ['1/7', '2']),
            lambda c: c['proof'].__setitem__('value', '-1000'),
            lambda c: c['rounds'][0]['problem'].__setitem__('constant', '1'),
            lambda c: c['proof'].__setitem__('kind', 'equal_bounds'),
            lambda c: c.__setitem__('upper', '-1000'),
            lambda c: c['rounds'].__setitem__(slice(None), c['rounds'][:1]),
        ]
        for mutate in mutations:
            corrupt = deepcopy(certificate)
            mutate(corrupt)
            with self.assertRaises(CertificateError):
                verify_certificate(corrupt)

    def test_approximate_oracle_is_not_called_by_replay(self):
        certificate = solve_exact(rational_face(), convex_presolve=False, time_limit=5)
        with patch('exact_output.solve', side_effect=AssertionError('optimizer called')):
            self.assertTrue(verify_certificate(certificate)['exact'])

    def test_invalid_accuracy_and_warm_start_are_rejected(self):
        for options in ({'max_rounds': 0}, {'max_stages': -1}, {'initial_precision': 0},
                        {'max_pivots': -1}, {'epsilon': F(1, 100)}):
            with self.assertRaises(ValueError):
                solve_exact(rational_face(), **options)
        with self.assertRaises(ValueError):
            solve(rational_face(), warm_start=[0, 3])


if __name__ == '__main__':
    unittest.main()
