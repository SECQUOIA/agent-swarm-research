"""Independent saved-cut binding tests with one real SCIP mechanism solve."""
import copy
from dataclasses import asdict
from fractions import Fraction as Q
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experiments.cases import synthetic_cases
from experiments.replay import (check_run, encode, model_digest, original_rows,
                                signed_original_side, tamper_checks)
from solver.integration import Config, run_instance
from solver.support import replay_support


class SavedCutReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = next(case["instance"] for case in synthetic_cases()
                         if case["instance"].name == "star_marginal_inconsistency")
        cls.expected = encode(asdict(cls.model))
        cls.record = run_instance(cls.model, "all", time_limit=5,
                                  config=Config(max_separation_seconds=2,
                                                separation_budget_fraction=.7))
        cls.record.update(original_model=cls.expected,
                          model_sha256=model_digest(cls.expected), cut_log_complete=True)
        if not cls.record["cuts"]:
            raise AssertionError("mechanism did not produce a cut for replay review")

    def test_real_native_rows_replay_from_original_model(self):
        result = check_run(self.record, self.expected, replay_support)
        self.assertTrue(result["passed"], result)
        self.assertEqual(result["replayed_cuts"], len(self.record["cuts"]))

    def test_fourteen_distinct_tamper_controls(self):
        checks = tamper_checks(self.record, self.expected, replay_support)
        self.assertEqual(len(checks), 14)
        self.assertTrue(all(checks.values()), checks)

    def test_substitutions_and_hidden_upper_bound_rejected(self):
        for name, mutation in (
            ("unproved fixing", lambda r: r["cuts"][0]["actual_row"].__setitem__("fixed_substitutions", [1])),
            ("NaN upper side", lambda r: r["cuts"][0]["actual_row"].__setitem__("rhs", math.nan)),
            ("finite upper side", lambda r: r["cuts"][0]["actual_row"].__setitem__("rhs", 1.0)),
        ):
            record = copy.deepcopy(self.record)
            mutation(record)
            with self.subTest(name=name):
                self.assertFalse(check_run(record, self.expected, replay_support)["passed"])

    def test_original_objective_sense_is_bound(self):
        record = copy.deepcopy(self.record)
        record["cuts"][0]["signed_sides"][0]["sign"] = -1
        self.assertFalse(check_run(record, self.expected, replay_support)["passed"])

    def test_min_and_max_objective_elimination_signs(self):
        # f = 2*x + 3 + x^2. For max, the source side is -x^2-2*x+t <= 3.
        model = asdict(self.model)
        model.update(var_lb=[0], var_ub=[1], var_type=["C"], obj_const=3., obj_sense="max")
        model["rows"] = [{"lin": {0: 2.}, "quad": [(0, 0, 1.)], "nl": None,
                          "lb": -math.inf, "ub": math.inf}]
        symbols, expressions = original_rows(model)
        h, terms, rhs, identity = signed_original_side(model, symbols, expressions[0], 0, -1, True)
        self.assertEqual(h, -symbols[0]**2)
        self.assertEqual(terms, {"x0": Q(-2), "objective_epigraph": Q(1)})
        self.assertEqual(rhs, Q(3))
        self.assertEqual(identity, "row0:objective")
        model["obj_sense"] = "min"
        h, terms, rhs, _ = signed_original_side(model, symbols, expressions[0], 0, 1, True)
        self.assertEqual(h, symbols[0]**2)
        self.assertEqual(terms, {"x0": Q(2), "objective_epigraph": Q(-1)})
        self.assertEqual(rhs, Q(-3))


if __name__ == "__main__":
    unittest.main()
