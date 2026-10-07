"""Independent adversarial checks of relaxation and certificate boundaries."""
from fractions import Fraction as F
import itertools
import math
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np
from scipy.sparse import csr_matrix

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / "solver"), str(HERE.parent / "experiments")]
from adaptive_obbt import AdaptiveOBBT, Config, Relaxation, TriggerState, dual_box_bound, solve_problem
from pyscipopt import Model
from models import Problem


def problem(lb, ub, *, oq=None, c=None, rows=None, rlo=None, rhi=None, rq=None, vtype=None, sense=1, c0=0):
    n = len(lb)
    rows = rows or []
    return Problem({"name": "independent_review", "names": [f"x{i}" for i in range(n)],
        "lb": lb, "ub": ub, "vtype": vtype or ["C"] * n,
        "c": c or [0] * n, "c0": c0, "sense": sense,
        "rlo": rlo or [-math.inf] * len(rows), "rhi": rhi or [math.inf] * len(rows),
        "oq": oq or [], "rq": rq or {},
        "A": {"row": [r for r, row in enumerate(rows) for j, a in enumerate(row) if a],
              "col": [j for row in rows for j, a in enumerate(row) if a],
              "value": [a for row in rows for a in row if a]}})


class IndependentReview(unittest.TestCase):
    def test_exact_graph_containment_with_signed_scaled_and_fixed_boxes(self):
        boxes = [(-.2, .7, -1.1, 2.2), (1e8, 1e8+1, -1e8, -1e8+2),
                 (1e-150, 3e-150, -3e-150, 2e-150), (-1e150, 1e150, .25, .75),
                 (-2., -1., 3., 4.), (.2, .2, -.7, -.7)]
        for li, ui, lj, uj in boxes:
            P = problem([li, lj], [ui, uj], oq=[[0, 0, 1], [0, 1, 1], [1, 1, 1]])
            R = Relaxation(P, P.lb, P.ub)
            xs = [F(li), (F(li) + F(ui))/2, F(ui)]
            ys = [F(lj), (F(lj) + F(uj))/2, F(uj)]
            for x, y in itertools.product(xs, ys):
                z = [x, y] + [([x, y][i] * [x, y][j]) for i, j in R.terms]
                for v, (l, u) in zip(z, R.bounds):
                    self.assertLessEqual(F(float(l)), v)
                    self.assertLessEqual(v, F(float(u)))
                for row, rhs in zip(R.rows, R.rhs):
                    self.assertLessEqual(sum((F(a)*z[k] for k, a in row.items()), F(0)), F(rhs))

    def test_dual_rounding_below_exact_arbitrary_multiplier_lagrangian(self):
        rng = np.random.default_rng(73513)
        for k in range(100):
            scale = [1e-100, 1, 1e100][k % 3]
            A = csr_matrix(rng.uniform(-2, 2, (4, 3)) * scale)
            b = rng.uniform(-2, 2, 4) * scale
            c = rng.uniform(-2, 2, 3) * scale
            marginals = rng.uniform(-5, 1, 4)
            bounds = list(zip(rng.uniform(-3, 0, 3), rng.uniform(0, 4, 3)))
            got = dual_box_bound(c, A, b, bounds, marginals)
            y = [F(min(float(v), 0)) for v in marginals]
            dense = A.toarray()
            residual = [F(float(c[j])) - sum((F(float(dense[i, j]))*y[i] for i in range(4)), F(0)) for j in range(3)]
            exact = sum((y[i]*F(float(b[i])) for i in range(4)), F(0))
            exact += sum((min(r*F(float(l)), r*F(float(u))) for r, (l, u) in zip(residual, bounds)), F(0))
            self.assertIsNotNone(got)
            self.assertLessEqual(F(got), exact)

    def test_actual_highs_signs_and_cutoff_objective_sense(self):
        for sense in (1, -1):
            P = problem([0], [2], c=[sense], c0=sense*3,
                        rows=[[0]], rlo=[1], rq={"0": [[0, 0, 1]]})
            P.sense = sense
            # Min-form objective is x+3 in both senses; cutoff gives x <= .8.
            R = Relaxation(P, P.lb, P.ub, cutoff=3.8)
            lower, _, status, _ = R.bound(0, True, 1)
            negupper, _, status2, _ = R.bound(0, False, 1)
            self.assertEqual((status, status2), (0, 0))
            self.assertLessEqual(lower, .5)
            self.assertGreater(lower, .5-1e-10)
            self.assertGreaterEqual(-negupper, .8-1e-15)
            self.assertLess(-negupper, .8+1e-10)

    def test_infeasible_or_failed_lp_never_produces_bound(self):
        P = problem([0], [1], oq=[[0, 0, 1]])
        R = Relaxation(P, P.lb, P.ub)
        for status in (1, 2, 3, 4):
            fake = SimpleNamespace(status=status, x=None, ineqlin=SimpleNamespace(marginals=None))
            with patch("adaptive_obbt.linprog", return_value=fake):
                bound, point, got_status, duration = R.bound(0, True, 1)
            self.assertIsNone(bound)
            self.assertEqual(got_status, status)

    def test_cached_witness_rechecked_in_sibling_and_new_cutoff(self):
        P = problem([0], [2], oq=[[0, 0, 1]])
        parent = Relaxation(P, [0], [2])
        point = np.array([1.5, 2.25])
        self.assertTrue(parent.witness_feasible(point))
        self.assertFalse(Relaxation(P, [0], [1]).witness_feasible(point))
        self.assertFalse(Relaxation(P, [0], [2], cutoff=1).witness_feasible(point))
        self.assertFalse(parent.witness_feasible(np.array([1.5, math.nan])))
        state = TriggerState(Config())
        state.record(1, np.array([0.]), np.array([1.]), 2.)
        self.assertEqual(state.reason(2, np.array([1.]), np.array([2.]), 2.), "first_visit")
        self.assertIsNone(state.reason(1, np.array([0.]), np.array([1.]), 2.))
        self.assertEqual(state.reason(1, np.array([0.]), np.array([1.]), 1.), "incumbent_improvement")

    def test_cutoff_preserves_exact_objective_under_catastrophic_cancellation(self):
        class IncumbentModel(Model):
            def getBestSol(self): return True
            def getSolVal(self, solution, variable): return 1.
        P = problem([1, 1], [1, 1], oq=[[0, 0, 1e16], [0, 1, 1], [1, 1, -1e16]])
        model = IncumbentModel()
        plugin = AdaptiveOBBT(P, [None, None], "fixed", Config(), 2)
        plugin.model = model
        cutoff = plugin._cutoff()
        self.assertGreaterEqual(cutoff, 1.)
        self.assertLess(cutoff, 1.001)
        relaxation = Relaxation(P, P.lb, P.ub, cutoff=cutoff)
        self.assertTrue(relaxation.witness_feasible(np.ones(5)))

    def test_callback_bounds_are_local_to_sibling_and_round_integers(self):
        class Variable:
            def __init__(self, lo, hi, integer=False):
                self.lo, self.hi, self.integer = lo, hi, integer
            def getLbLocal(self): return self.lo
            def getUbLocal(self): return self.hi

        class LocalModel(Model):
            def __init__(self, variable):
                super().__init__()
                self.variable, self.node, self.applied = variable, 1, []
            def getDepth(self): return 1
            def getCurrentNode(self): return SimpleNamespace(getNumber=lambda: self.node)
            def getTransformedVar(self, variable): return self.variable
            def getBestSol(self): return None
            def tightenVarLb(self, variable, bound):
                value = math.ceil(bound) if variable.integer else bound
                assert variable.lo <= value <= variable.hi
                variable.lo = value
                self.applied.append((self.node, "lower", value))
                return False, True
            def tightenVarUb(self, variable, bound):
                value = math.floor(bound) if variable.integer else bound
                assert variable.lo <= value <= variable.hi
                variable.hi = value
                self.applied.append((self.node, "upper", value))
                return False, True

        P = problem([-2], [2], rows=[[0]], rlo=[1], rq={"0": [[0, 0, 1]]})
        model = LocalModel(Variable(0, 2))
        plugin = AdaptiveOBBT(P, [None], "fixed", Config(time_fraction=1), 2)
        plugin.model = model
        plugin.propexec(None)
        self.assertGreater(model.variable.lo, .49)
        model.node, model.variable = 2, Variable(-2, 0)
        plugin.propexec(None)
        self.assertEqual(model.variable.lo, -2)
        self.assertLess(model.variable.hi, -.49)
        self.assertEqual([(node, direction) for node, direction, _ in model.applied],
                         [(1, "lower"), (2, "upper")])

        P = problem([0], [3], oq=[[0, 0, 1]], rows=[[1]], rlo=[1.1], vtype=["I"])
        model = LocalModel(Variable(0, 3, integer=True))
        plugin = AdaptiveOBBT(P, [None], "fixed", Config(time_fraction=1), 2)
        plugin.model = model
        plugin.propexec(None)
        self.assertEqual(model.variable.lo, 2)
        self.assertEqual(model.variable.hi, 3)

    def test_exhausted_construction_budget_never_starts_optimization(self):
        P = problem([0], [1], oq=[[0, 0, -1]])
        for policy in ("native", "fixed", "adaptive"):
            result = solve_problem(P, policy=policy, time_limit=1e-12)
            self.assertEqual(result["status"], "setup_time_limit")
            self.assertEqual(result["solving_time"], 0)
            self.assertEqual(result["nodes"], 0)
            self.assertEqual(result["obbt"]["lp_calls"], 0)
            self.assertIsNone(result["solution"])

    def test_two_integer_qcqp_known_optimum_and_original_reconstruction(self):
        P = problem([0, 0], [3, 3], oq=[[0, 1, -1]], rows=[[1, 1]],
                    rlo=[3], rhi=[3], vtype=["I", "I"])
        expected = min(-x*y for x in range(4) for y in range(4) if x+y == 3)
        for policy in ("native", "fixed", "adaptive"):
            result = solve_problem(P, policy=policy, time_limit=2,
                                   parameters={"presolving/maxrounds": 0})
            self.assertEqual(result["status"], "optimal")
            self.assertTrue(P.validation(result["solution"])["valid"])
            self.assertAlmostEqual(result["objective"], expected, places=6)
            self.assertLessEqual(result["dual_bound"], expected+1e-6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
