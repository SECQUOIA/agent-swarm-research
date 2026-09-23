"""Run with uv run --no-sync python -m unittest discover -s lbesh/tests -p test_publication_contracts.py -v."""
import math
import shutil
import unittest
from unittest.mock import patch
import pyomo.environ as pe
from pyomo.gdp import Disjunct, Disjunction
from lbesh.solver import LBESH
from lbesh.structure import StructureError


def linear_model():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(0, 4), initialize=2)
    m.d = Disjunct([0, 1])
    m.d[0].c = pe.Constraint(expr=m.x >= 1)
    m.d[1].c = pe.Constraint(expr=m.x >= 3)
    m.dj = Disjunction(expr=[m.d[0], m.d[1]])
    m.obj = pe.Objective(expr=m.x)
    return m


def solver(m, **kw):
    return LBESH(m, threads=1, verbose=False, esh=False, lp_phase=False,
                 nlp_at_integer=False, time_limit=15, **kw)


class PublicationContracts(unittest.TestCase):
    def test_linear_no_nlp_all_variants(self):
        for formulation in ('hull', 'bigm'):
            for single_tree in (False, True):
                with self.subTest(formulation=formulation, single_tree=single_tree):
                    s = solver(linear_model(), formulation=formulation)
                    result = s.solve(single_tree=single_tree)
                    self.assertEqual(result.status, 'optimal')
                    self.assertAlmostEqual(result.obj, 1)
                    self.assertEqual(result.nlp_solves, 0)
                    self.assertEqual(result.incumbent_validation, 'numerical_within_tolerance')
                    self.assertFalse(result.rigorous_certificate)

    def test_global_logical_link_does_not_fix_both_indicators_false(self):
        m = linear_model()
        m.link = pe.Constraint(expr=m.d[0].binary_indicator_var + m.d[1].binary_indicator_var == 1)
        result = solver(m).solve()
        self.assertEqual(result.status, 'optimal')
        self.assertAlmostEqual(result.obj, 1)

    def test_original_nonlinear_objective_and_max_sense(self):
        for formulation in ('hull', 'bigm'):
            for single_tree in (False, True):
                with self.subTest(formulation=formulation, single_tree=single_tree):
                    m = linear_model(); m.obj.set_value(10 - (m.x - 2)**2); m.obj.sense = pe.maximize
                    result = solver(m, formulation=formulation).solve(single_tree=single_tree)
                    self.assertEqual(result.status, 'optimal')
                    self.assertAlmostEqual(result.obj, pe.value(m.obj), places=10)
                    self.assertAlmostEqual(result.obj, 10, places=4)
                    self.assertLessEqual(result.lb, result.obj + 1e-7)
                    self.assertGreaterEqual(result.ub, result.obj - 1e-7)

    def test_primal_validation_rejects_rows_bounds_discrete_and_nonfinite(self):
        m = linear_model(); m.n = pe.Var(domain=pe.Integers, bounds=(0, 2), initialize=0)
        m.global_row = pe.Constraint(expr=m.x + m.n <= 4)
        s = solver(m)
        good = {id(m.x): 1., id(m.n): 0., id(m.d[0].binary_indicator_var): 1., id(m.d[1].binary_indicator_var): 0.}
        self.assertIsNotNone(s._validate_primal(good))
        for var, value in ((m.x, 0), (m.x, 5), (m.x, math.nan), (m.n, .25), (m.n, 4), (m.d[1].binary_indicator_var, 1)):
            bad = dict(good); bad[id(var)] = value
            self.assertIsNone(s._validate_primal(bad))
        bad = dict(good); bad[id(m.x)] = 3; bad[id(m.n)] = 2
        self.assertIsNone(s._validate_primal(bad))
        self.assertTrue(s._update_incumbent(-10000, good)); self.assertEqual(s.ub, 1)

    def test_callback_failure_cannot_be_optimal(self):
        s = solver(linear_model())
        with patch.object(s, '_separate_point', side_effect=ValueError('injected nonfinite cut')):
            result = s.solve(single_tree=True)
        self.assertEqual(result.status, 'numerical_error')
        self.assertIn('injected nonfinite cut', result.error)

    def test_gap_is_required_and_inconsistent_bounds_fail(self):
        s = solver(linear_model()); s.ub = 2; s.lb = 1
        self.assertFalse(s._converged()); s.lb = 3
        self.assertFalse(s._converged()); s.lb = 2
        self.assertTrue(s._converged())

    def test_nonfinite_separation_fails_closed(self):
        m = linear_model(); m.nl = pe.Constraint(expr=m.x**2 <= 4)
        s = solver(m); row = s.prob.nl_rows[0]
        with patch.object(row, 'linearize', return_value=({id(m.x): math.nan}, 0.)):
            with self.assertRaisesRegex(ValueError, 'nonfinite separating cut'):
                s._esh_cuts([row], {id(m.x): 3.}, None, 'test')

    def test_infeasible_constant_disjunct_does_not_reject_feasible_branch(self):
        m = linear_model(); m.fixed = pe.Var(initialize=0); m.fixed.fix()
        m.d[0].impossible = pe.Constraint(expr=m.fixed >= 1)
        result = solver(m).solve(single_tree=True)
        self.assertEqual(result.status, 'optimal'); self.assertAlmostEqual(result.obj, 3)

    @unittest.skipUnless(shutil.which('ipopt'), 'Ipopt executable is needed for the NLP integration check')
    def test_exponential_analytic_oracle_with_nlp_all_variants(self):
        for esh in (False, True):
            for formulation in ('hull', 'bigm'):
                for single_tree in (False, True):
                    with self.subTest(esh=esh, formulation=formulation, single_tree=single_tree):
                        m = pe.ConcreteModel(); m.x = pe.Var(bounds=(-2, 2), initialize=0)
                        m.d = Disjunct([0, 1])
                        m.d[0].c = pe.Constraint(expr=pe.exp(m.x) <= 2)
                        m.d[1].c = pe.Constraint(expr=m.x <= 0)
                        m.dj = Disjunction(expr=list(m.d.values()))
                        m.obj = pe.Objective(expr=m.x, sense=pe.maximize)
                        s = LBESH(m, formulation=formulation, esh=esh, threads=1,
                                  verbose=False, time_limit=20, nlp_at_integer=True,
                                  abs_tol=1e-7, rel_tol=1e-6)
                        result = s.solve(single_tree=single_tree)
                        self.assertEqual(result.status, 'optimal')
                        self.assertLess(abs(result.obj - math.log(2)), 1e-6)
                        self.assertLessEqual(result.max_primal_violation, result.feasibility_tolerance)
                        self.assertGreater(result.nlp_solves, 0)
                        self.assertGreater(result.interior_nlps, 0)

    def test_obbt_missing_bounds_and_initialization_logging(self):
        m = pe.ConcreteModel()
        m.x = pe.Var(initialize=0); m.y = pe.Var(initialize=1)
        m.a = pe.Constraint(expr=(0, m.x + m.y, 2))
        m.b = pe.Constraint(expr=(-2, m.x - m.y, 0))
        m.nl = pe.Constraint(expr=m.x**2 <= 1)
        m.obj = pe.Objective(expr=m.x)
        s = LBESH(m, threads=1, verbose=True, nlp_at_integer=False)
        self.assertLessEqual(m.x.lb, -1)
        self.assertGreaterEqual(m.x.ub, 1)
        self.assertGreater(m.x.lb, -1.00001)
        self.assertLess(m.x.ub, 1.00001)

    def test_unused_variable_infeasible_bounds_are_not_ignored(self):
        m = linear_model(); m.unused = pe.Var(bounds=(2, 1), initialize=1)
        self.assertEqual(solver(m).solve(single_tree=True).status, 'infeasible')

    def test_unsupported_structure_refused(self):
        m = linear_model(); m.dj.xor = False
        with self.assertRaises(StructureError): solver(m)
        m = linear_model(); m.orphan = Disjunct(); m.orphan.c = pe.Constraint(expr=m.x >= 4)
        with self.assertRaises(StructureError): solver(m)
        m = linear_model(); m.d[0].eq = pe.Constraint(expr=m.x**2 == 1)
        with self.assertRaises(StructureError): solver(m)
        m = linear_model(); m.d[0].nested = Disjunct(); m.d[0].nested.c = pe.Constraint(expr=m.x >= 4)
        with self.assertRaises(StructureError): solver(m)
        with self.assertRaises(ValueError): solver(linear_model(), formulation='typo')


if __name__ == '__main__': unittest.main()
