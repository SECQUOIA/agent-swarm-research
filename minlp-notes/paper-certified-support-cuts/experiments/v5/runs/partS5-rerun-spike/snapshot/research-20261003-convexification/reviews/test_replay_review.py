"""Independent saved-cut binding tests with one real SCIP mechanism solve."""
import copy
from dataclasses import asdict
from fractions import Fraction as Q
import math
import hashlib
import json
from pathlib import Path
import sys
import unittest

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experiments.cases import instance, row, synthetic_cases
from experiments.replay import (check_run, encode, model_digest, original_rows,
                                signed_original_side, split_affine, tamper_checks)
from solver.integration import Config, run_instance
from solver.model import build_model
from solver.row_certificate import AffineSide, certify_row_combination
from solver.support import certify_support, replay_support


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

    def test_sparse_row_in_large_global_model(self):
        symbols = sp.symbols("x0:1400", real=True)
        expression = (sp.Rational(1, 7) + sp.Rational(3, 11)*symbols[1399]
                      - 5*symbols[31] + symbols[31]*symbols[500]
                      + sp.exp(symbols[1200]))
        h, affine, constant = split_affine(expression, symbols)
        self.assertEqual(h, symbols[31]*symbols[500]+sp.exp(symbols[1200]))
        self.assertEqual(affine, {31: -5, 1399: sp.Rational(3, 11)})
        self.assertEqual(constant, sp.Rational(1, 7))
        dense_term = sp.Mul(*symbols)
        h, affine, constant = split_affine(dense_term, symbols)
        self.assertEqual(h, dense_term)
        self.assertEqual(affine, {})
        self.assertEqual(constant, 0)

    def test_empty_infeasibility_row_has_complete_tamper_controls(self):
        # A valid support proof for x^2 >= 0 and source side x^2 <= -1
        # gives the empty row 0 >= 1. This fixture tests record composition,
        # not a claim that SCIP actually generated this synthetic row.
        model = instance("empty_cut_review", [(-1., 1.)], row(),
                         [row(quad=[(0, 0, 1.)], ub=-1.)])
        built = build_model(model)
        try:
            metadata = built.metadata
            infinity = built.model.infinity()
        finally:
            built.model.freeProb()
        x = sp.Symbol("x0", real=True)
        support = certify_support((x, x*x), (x,), [(-1, 1)], (0., 1.))
        identity = hashlib.sha256(json.dumps(support.witness, sort_keys=True,
                                             separators=(",", ":")).encode()).hexdigest()
        converted = certify_row_combination(variables=["x0"], bounds={"x0": (-1, 1)},
            linear_terms={"x0": 0.}, multipliers=[1.], support_rhs=support.cut.rhs,
            sides=[AffineSide("row1:upper", [], -1)], support_id=identity)
        cut = {"variables": [0], "symbols": ["x0"], "features": ["x0", "x0**2"],
               "box": [["-1", "1"]], "domain_rows": [], "coefficients": [0., 1.],
               "signed_sides": [{"row_index": 1, "sign": 1, "side": "upper",
                   "source_id": "row1:upper", "nonlinear": "x0**2", "affine_terms": [], "rhs": "-1"}],
               "support_witness": support.witness, "row_certificate": converted.to_dict(),
               "rhs": converted.rhs, "local": False, "column_names": ["v0"],
               "actual_row": {"columns": {}, "source_to_transformed": [], "local": False,
                   "lhs": 1., "rhs": infinity, "constant": 0., "scip_infinity": infinity}}
        expected = encode(asdict(model))
        record = {"mode": "all", "status": "infeasible", "original_model": expected,
                  "model_sha256": model_digest(expected), "model_metadata": metadata,
                  "cuts": [cut], "cut_log_complete": True}
        self.assertTrue(check_run(record, expected, replay_support)["passed"])
        controls = tamper_checks(record, expected, replay_support)
        self.assertEqual(len(controls), 14)
        self.assertTrue(all(controls.values()), controls)


if __name__ == "__main__":
    unittest.main()
