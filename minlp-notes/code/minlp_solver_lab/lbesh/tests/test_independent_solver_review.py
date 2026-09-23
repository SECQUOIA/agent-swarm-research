"""Independent adversarial checks; run only this topic's test discovery."""
import math
import shutil
import unittest
from unittest.mock import patch

import pyomo.environ as pe
from pyomo.gdp import Disjunct, Disjunction

from lbesh.solver import LBESH
from lbesh.structure import StructureError


def model():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(0, 4), initialize=2)
    m.d = Disjunct([0, 1])
    m.d[0].c = pe.Constraint(expr=m.x >= 1)
    m.d[1].c = pe.Constraint(expr=m.x >= 3)
    m.dj = Disjunction(expr=list(m.d.values()))
    m.obj = pe.Objective(expr=m.x)
    return m


def make_solver(m, **kwargs):
    opts = dict(threads=1, verbose=False, esh=False, lp_phase=False,
                nlp_at_integer=False, time_limit=15)
    opts.update(kwargs)
    return LBESH(m, **opts)


class IndependentSolverReview(unittest.TestCase):
    def test_prior_bigm_no_nlp_regression(self):
        m = model()
        result = make_solver(m, formulation='bigm').solve(single_tree=True)
        self.assertEqual(result.status, 'optimal')
        self.assertAlmostEqual(result.obj, 1)
        self.assertAlmostEqual(pe.value(m.obj), 1)

    def test_fixed_original_variable_survives_reduced_nlp_initialization(self):
        m = model()
        m.f = pe.Var(initialize=1)
        m.f.fix()
        m.obj.set_value(m.x + m.f)
        solver = make_solver(m)
        x = {id(m.x): 1., id(m.f): 2.,
             id(m.d[0].binary_indicator_var): 1.,
             id(m.d[1].binary_indicator_var): 0.}
        with patch.object(solver, '_solve_nlp_model', return_value=object()):
            obj, _ = solver.solve_reduced_nlp(x)
        self.assertEqual(m.f.value, 1)
        self.assertIn(obj, (None, 2.))

    def test_binary_projection_rechecks_amplified_row_and_stores_projected_point(self):
        m = model()
        m.x.setub(1e9)
        m.d[0].c.set_value(m.x >= 0)
        m.d[1].c.set_value(m.x >= 0)
        y0, y1 = m.d[0].binary_indicator_var, m.d[1].binary_indicator_var
        m.link = pe.Constraint(expr=m.x == 1e9 * (1 - y0))
        m.obj.set_value(1e9 * y0 + 2 * m.x)
        solver = make_solver(m)
        raw_y0 = 1 - 5e-7
        raw = {id(m.x): 1e9 * (1 - raw_y0), id(y0): raw_y0,
               id(y1): 5e-7}
        # The raw equality is satisfied, but projection moves its right side
        # by about 500. The full row check must reject that projected point.
        self.assertIsNone(solver._validate_primal(raw))
        self.assertFalse(solver._update_incumbent(0, raw))
        # With x=0, the projected point is valid. The projected indicators and
        # their recomputed objective must be the actual saved incumbent.
        raw[id(m.x)] = 0.
        self.assertTrue(solver._update_incumbent(1e9 * raw_y0, raw))
        self.assertEqual(solver.incumbent[id(y0)], 1.)
        self.assertEqual(solver.incumbent[id(y1)], 0.)
        self.assertEqual(solver.ub, 1e9)
        self.assertEqual(raw[id(y0)], raw_y0)
        result = solver.solve(single_tree=True)
        self.assertEqual(result.status, 'optimal')
        self.assertEqual(result.obj, 1e9)
        self.assertEqual(pe.value(m.obj), result.obj)
        self.assertEqual(y0.value, 1.)
        self.assertEqual(y1.value, 0.)

    def test_fixed_boolean_selects_correct_branch(self):
        for formulation in ('hull', 'bigm'):
            for single_tree in (False, True):
                with self.subTest(formulation=formulation, single_tree=single_tree):
                    m = model()
                    m.d[1].indicator_var.fix(True)
                    result = make_solver(m, formulation=formulation).solve(single_tree=single_tree)
                    self.assertEqual(result.status, 'optimal')
                    self.assertAlmostEqual(result.obj, 3)
                    self.assertTrue(m.d[1].indicator_var.value)

    def test_deactivated_branch_and_global_boolean_logic(self):
        m = model()
        m.d[0].deactivate()
        self.assertAlmostEqual(make_solver(m).solve().obj, 3)
        m = model()
        m.force = pe.LogicalConstraint(expr=m.d[1].indicator_var)
        self.assertAlmostEqual(make_solver(m).solve(single_tree=True).obj, 3)

    def test_own_indicator_inside_linear_disjunct_is_explicitly_refused(self):
        for formulation in ('hull', 'bigm'):
            m = model()
            m.d[0].c.set_value(m.x >= 2 * m.d[0].binary_indicator_var)
            with self.assertRaisesRegex(StructureError, 'GDP indicator'):
                make_solver(m, formulation=formulation)

    def test_cross_indicator_does_not_weaken_claimed_individual_hull(self):
        m = model()
        m.x.setub(2)
        m.d[1].c.set_value(m.x >= 1 - m.d[0].binary_indicator_var)
        try:
            solver = make_solver(m)
        except StructureError:
            # Explicitly refusing this extended GDP syntax is also sound.
            return
        solver.master.relax_integrality()
        solver.master.m.optimize()
        self.assertAlmostEqual(solver.master.m.ObjVal, 1)

    def test_exhausted_budget_skips_single_tree_optimization(self):
        result = make_solver(model(), time_limit=0).solve(single_tree=True)
        self.assertEqual(result.status, 'time_limit')
        self.assertEqual(result.lazy_calls, 0)
        self.assertEqual(result.nlp_solves, 0)

    def test_lp_bound_sense_and_skipped_weight_residual(self):
        m = model()
        m.obj.set_value(-m.x)
        m.obj.sense = pe.maximize
        result = make_solver(m, lp_phase=True).solve()
        self.assertEqual(result.status, 'optimal')
        self.assertAlmostEqual(result.lp_bound, -1)
        self.assertEqual(result.lp_end_reason, 'no_separating_cuts')
        m = model()
        m.d[0].c.set_value(pe.exp(-m.x) <= math.exp(-1))
        solver = make_solver(m)
        lam = 1e-8
        x = {id(m.x): 1., id(m.d[0].binary_indicator_var): lam,
             id(m.d[1].binary_indicator_var): 1 - lam}
        nu = {(0, 0, id(m.x)): 0., (0, 1, id(m.x)): 1.}
        self.assertAlmostEqual(solver._perspective_violation(x, nu),
                               lam * (1 - math.exp(-1)), places=16)

    def test_unbounded_bigm_coefficient_is_refused(self):
        m = model()
        m.x.setub(None)
        m.d[0].c.set_value(m.x <= 1)
        m.d[1].c.set_value(m.x >= 3)
        with self.assertRaisesRegex(ValueError, 'big-M needs bounds'):
            make_solver(m, formulation='bigm')

    def test_multiple_membership_and_nested_structure_refused(self):
        m = model()
        m.extra = Disjunction(expr=list(m.d.values()))
        with self.assertRaises(StructureError):
            make_solver(m)
        m = model()
        m.d[0].inner = Disjunct([0, 1])
        m.d[0].inner_dj = Disjunction(expr=list(m.d[0].inner.values()))
        with self.assertRaises(StructureError):
            make_solver(m)

    def test_cut_is_valid_at_independently_known_feasible_points(self):
        m = model()
        m.d[0].c.set_value(pe.exp(-m.x) <= math.exp(-1))
        solver = make_solver(m)
        row = solver.prob.disjunctions[0].disjuncts[0].nl_rows[0]
        for esh in (False, True):
            solver.esh = esh
            cuts = solver._esh_cuts([row], {id(m.x): 0.}, {id(m.x): 2.}, 'review')
            self.assertEqual(len(cuts), 1)
            _, coefficients, constant, _ = cuts[0]
            self.assertGreater(constant, 0)
            for x in (1., 1.1, 2., 4.):
                self.assertLessEqual(coefficients[id(m.x)] * x + constant, 1e-8)

    @unittest.skipUnless(shutil.which('ipopt'), 'Ipopt executable required')
    def test_nonquadratic_with_real_reduced_nlp(self):
        for formulation in ('hull', 'bigm'):
            for single_tree in (False, True):
                with self.subTest(formulation=formulation, single_tree=single_tree):
                    m = model()
                    m.d[0].c.set_value(pe.exp(-m.x) <= math.exp(-1))
                    m.d[1].c.set_value(pe.exp(-m.x) <= math.exp(-3))
                    result = make_solver(m, formulation=formulation, esh=True,
                                         nlp_at_integer=True,
                                         nlp_options={'max_cpu_time': 10}).solve(single_tree=single_tree)
                    self.assertEqual(result.status, 'optimal')
                    self.assertAlmostEqual(result.obj, 1, places=4)
                    self.assertGreater(result.nlp_solves, 0)
                    self.assertLessEqual(math.exp(-m.x.value) - math.exp(-1), 1e-6)
                    self.assertFalse(result.rigorous_certificate)


if __name__ == '__main__':
    unittest.main()
