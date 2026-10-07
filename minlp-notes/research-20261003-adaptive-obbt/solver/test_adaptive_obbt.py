"""Targeted contracts for the local OBBT integration; run with unittest."""
from fractions import Fraction
import math
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
from scipy.sparse import csr_matrix
from pyscipopt import SCIP_PARAMSETTING, SCIP_RESULT

from adaptive_obbt import (AdaptiveOBBT, Config, Relaxation, TriggerState,
                           build_model, dual_box_bound, exact_objective, solve_problem)


class Problem:
    def __init__(self, lb, ub, c, rows=(), oq=None, rq=None, integer=()):
        self.name = "obbt_contract"
        self.n = len(lb); self.m = len(rows)
        self.lb, self.ub, self.c = map(lambda x: np.array(x, dtype=float), (lb, ub, c))
        self.c0 = 0.0; self.sense = 1
        self.names = [f"x{i}" for i in range(self.n)]
        self.vtype = np.array(["I" if i in integer else "C" for i in range(self.n)])
        self.isint = self.vtype == "I"
        self.A = csr_matrix(np.array([r[0] for r in rows]).reshape(self.m, self.n))
        self.rlo = np.array([r[1] for r in rows]); self.rhi = np.array([r[2] for r in rows])
        self.oq, self.rq = oq or {}, rq or {}
        self.terms = sorted(set(self.oq).union(*(set(q) for q in self.rq.values())))
        self.nlvars = sorted({i for term in self.terms for i in term})

    def fmin(self, x):
        return self.sense * (self.c0 + self.c @ x + sum(q * x[i] * x[j] for (i, j), q in self.oq.items()))

    def violation(self, x):
        x = np.asarray(x)
        values = self.A @ x
        for row, terms in self.rq.items():
            values[row] += sum(q * x[i] * x[j] for (i, j), q in terms.items())
        return float(max(np.max(self.lb - x, initial=0), np.max(x - self.ub, initial=0),
                         np.max(self.rlo - values, initial=0), np.max(values - self.rhi, initial=0),
                         np.max(abs(x[self.isint] - np.rint(x[self.isint])), initial=0)))


class ExactLPContracts(unittest.TestCase):
    def test_cutoff_objective_evaluation_does_not_lose_cancellation(self):
        p = Problem([0, 0], [1, 1], [0, 0],
                    oq={(0, 0): 1e16, (0, 1): 1, (1, 1): -1e16})
        self.assertEqual(p.fmin(np.ones(2)), 0)
        self.assertEqual(exact_objective(p, np.ones(2)), 1)

    def test_mccormick_rows_contain_exact_graph_across_signs(self):
        for lb, ub in (([-2.3, -0.7], [1.1, 4.2]), ([0.1, 0.3], [0.8, 0.7]),
                       ([-3, -8], [-1, -2]), ([0, 0], [0, 0])):
            p = Problem(lb, ub, [0, 0], oq={(0, 0): 1, (0, 1): 1, (1, 1): 1})
            r = Relaxation(p, p.lb, p.ub)
            for a in range(5):
                for b in range(5):
                    x = [Fraction(lb[0]) + Fraction(a, 4) * (Fraction(ub[0]) - Fraction(lb[0])),
                         Fraction(lb[1]) + Fraction(b, 4) * (Fraction(ub[1]) - Fraction(lb[1]))]
                    lift = x + [x[i] * x[j] for i, j in p.terms]
                    for row, rhs in zip(r.rows, r.rhs):
                        self.assertLessEqual(sum(Fraction(v) * lift[k] for k, v in row.items()), Fraction(rhs))
                    for v, (lo, hi) in zip(lift, r.bounds):
                        self.assertLessEqual(Fraction(lo), v)
                        self.assertLessEqual(v, Fraction(hi))

    def test_residual_correction_handles_inexact_and_wrong_sign_multipliers(self):
        a = csr_matrix([[0.3, -1.2], [-0.7, 0.1]])
        b = np.array([0.8, -0.1]); c = np.array([0.1, -0.2]); box = [(-3, 4), (-2, 5)]
        for multipliers in ([0.5, -0.03], [-1.3, -7.1], [0, 0]):
            bound = dual_box_bound(c, a, b, box, multipliers)
            y = [Fraction(min(v, 0)) for v in multipliers]
            exact = sum(y[i] * Fraction(b[i]) for i in range(2))
            for j, (lo, hi) in enumerate(box):
                residual = Fraction(c[j]) - sum(y[i] * Fraction(a[i, j]) for i in range(2))
                exact += min(residual * lo, residual * hi)
            self.assertLessEqual(Fraction(bound), exact)
        self.assertIsNone(dual_box_bound(c, a, b, box, [math.nan, 0]))

    def test_direction_uses_dual_lower_bound_for_both_senses(self):
        p = Problem([0, 0], [1, 1], [0, 0], rows=[([1, 1], 1, 1)], oq={(0, 1): 1})
        r = Relaxation(p, [0, .75], [1, 1])
        lower, _, status, _ = r.bound(0, True, 1)
        upper_negative, _, status2, _ = r.bound(0, False, 1)
        self.assertEqual((status, status2), (0, 0))
        self.assertLessEqual(lower, 0)
        self.assertGreaterEqual(-upper_negative, .25)
        self.assertAlmostEqual(-upper_negative, .25, places=10)

    def test_frozen_witness_invalidated_by_cutoff_and_sibling_domain(self):
        p = Problem([0, 0], [1, 1], [1, 0], oq={(0, 1): 1})
        point = np.array([1, 0, 0])
        self.assertTrue(Relaxation(p, p.lb, p.ub, 2).witness_feasible(point))
        self.assertFalse(Relaxation(p, p.lb, p.ub, .5).witness_feasible(point))
        self.assertFalse(Relaxation(p, [0, .5], p.ub, 2).witness_feasible(point))

    def test_infeasible_lp_provides_no_domain_bound(self):
        p = Problem([0], [1], [0], rows=[([1], 2, math.inf)], oq={(0, 0): 1})
        value, point, status, _ = Relaxation(p, p.lb, p.ub).bound(0, True, 1)
        self.assertIsNone(value)
        self.assertNotEqual(status, 0)


class SchedulingContracts(unittest.TestCase):
    def test_no_incumbent_then_new_incumbent_then_tighter_cutoff(self):
        config = Config(max_calls_per_node=4)
        state = TriggerState(config)
        lo, hi = np.zeros(2), np.ones(2)
        self.assertEqual(state.reason(1, lo, hi, math.inf), "first_visit")
        state.record(1, lo, hi, math.inf)
        self.assertIsNone(state.reason(1, lo, hi, math.inf))
        self.assertEqual(state.reason(1, lo, hi, 2), "incumbent_improvement")
        state.record(1, lo, hi, 2)
        self.assertIsNone(state.reason(1, lo, hi, 1.999))
        self.assertEqual(state.reason(1, lo, hi, 1), "incumbent_improvement")

    def test_sibling_state_never_copies_parent_or_sibling_bounds(self):
        state = TriggerState(Config())
        state.record(2, np.array([0.]), np.array([.25]), 1)
        self.assertEqual(state.reason(3, np.array([.75]), np.array([1.]), 1), "first_visit")
        state.record(3, np.array([.75]), np.array([1.]), 1)
        self.assertEqual(state.nodes[2][1].tolist(), [.25])
        self.assertEqual(state.nodes[3][0].tolist(), [.75])


class SCIPIntegrationContracts(unittest.TestCase):
    def test_native_and_integrated_integer_optimum_agree(self):
        p = Problem([0, 0], [4, 1], [1, 0], rows=[([1, 0], 1.2, math.inf)],
                    oq={(0, 1): -.1}, integer=(0,))
        native = solve_problem(p, "native", 2)
        integrated = solve_problem(p, "adaptive", 2, config=Config(total_lp_budget=3))
        self.assertEqual(native["status"], "optimal")
        self.assertEqual(integrated["status"], "optimal")
        self.assertAlmostEqual(native["objective"], integrated["objective"], places=6)
        self.assertLessEqual(integrated["obbt"]["lp_calls"], 3)

    def test_actual_nonroot_bounds_and_incumbent_retrigger(self):
        # Development case, separate from frozen holdout sizes and seeds.
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
        from models import synthetic
        p = synthetic("coupled_squares", 6, 17)
        result = solve_problem(p, "fixed", 3, config=Config(total_lp_budget=40, time_fraction=.5))
        self.assertEqual(result["status"], "optimal")
        stats = result["obbt"]
        self.assertGreater(stats["nonroot_calls"], 0)
        self.assertGreater(stats["incumbent_retriggers"], 0)
        self.assertGreater(stats["tightened"], 0)
        self.assertLessEqual(stats["lp_calls"], 40)
        self.assertFalse(stats["errors"])
        self.assertTrue(any(e["depth"] > 0 and e["applications"] for e in stats["events"]))

    def test_zero_budget_and_full_log(self):
        p = Problem([0], [1], [0], oq={(0, 0): -1})
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scip.log"
            result = solve_problem(p, "adaptive", 1, config=Config(total_lp_budget=0), log_path=path)
            self.assertEqual(result["obbt"]["lp_calls"], 0)
            self.assertTrue(path.exists())

    def test_no_incumbent_callback(self):
        p = Problem([0, 0], [1, 1], [0, 0], rows=[([1, 1], 1, 1)], oq={(0, 1): -1})
        model, variables = build_model(p, 2)
        model.setPresolve(SCIP_PARAMSETTING.OFF)
        model.setHeuristics(SCIP_PARAMSETTING.OFF)
        model.setSeparating(SCIP_PARAMSETTING.OFF)
        model.setIntParam("propagating/maxrounds", 0)
        # Keep our propagator enabled by restoring propagation rounds, while
        # disabling native linear propagation that would obscure its effect.
        model.setIntParam("propagating/maxrounds", 1)
        model.setIntParam("constraints/linear/propfreq", -1)
        model.setIntParam("constraints/nonlinear/propfreq", -1)
        plugin = AdaptiveOBBT(p, variables, "fixed", Config(total_lp_budget=8, time_fraction=1), 2)
        model.includeProp(plugin, "contract_obbt", "contract test", presolpriority=0,
                          presolmaxrounds=0, proptiming=1, priority=1000000, freq=1, delay=False)
        model.optimize()
        self.assertGreater(plugin.stats["no_incumbent_calls"], 0)
        self.assertFalse(plugin.stats["errors"])
        model.freeProb()

    def test_actual_local_bound_changes_do_not_change_global_domains(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
        from models import synthetic
        p = synthetic("coupled_squares", 6, 17)
        model, variables = build_model(p, 3)
        observed = []

        class ScopeObserver(AdaptiveOBBT):
            def propexec(self, timing):
                transformed = [self.model.getTransformedVar(v) for v in self.original_vars]
                before = [(v.getLbGlobal(), v.getUbGlobal()) for v in transformed]
                count = self.stats["tightened"]
                result = super().propexec(timing)
                if self.model.getDepth() > 0 and self.stats["tightened"] > count:
                    after = [(v.getLbGlobal(), v.getUbGlobal()) for v in transformed]
                    observed.append((before, after))
                return result

        plugin = ScopeObserver(p, variables, "fixed", Config(total_lp_budget=40, time_fraction=.5), 3)
        model.includeProp(plugin, "scope_obbt", "scope contract", presolpriority=0,
                          presolmaxrounds=0, proptiming=1, priority=-1000000, freq=1, delay=False)
        model.optimize()
        self.assertGreater(len(observed), 0)
        for before, after in observed:
            self.assertEqual(before, after)
        self.assertFalse(plugin.stats["errors"])
        model.freeProb()


if __name__ == "__main__":
    unittest.main(verbosity=2)
