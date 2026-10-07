"""Focused checks for experiment input integrity and feasibility diagnostics."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np

from models import Problem, read_problem, synthetic, write_problem

HERE = Path(__file__).resolve().parent


class ExperimentModelTests(unittest.TestCase):
    def test_synthetic_constructions_have_feasible_witnesses(self):
        for family, size in (("packing", 3), ("coupled_squares", 6),
                             ("bilinear_cycle", 5), ("indefinite_qp", 8)):
            p = synthetic(family, size, 17)
            x = np.zeros(p.n)
            if family == "bilinear_cycle":
                x[:size], x[size:] = .4, .16
            elif family == "indefinite_qp":
                x[:] = .45
            self.assertTrue(p.validation(x)["valid"], family)
            with tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "model.json"
                write_problem(p, path)
                restored = read_problem(path)
                self.assertAlmostEqual(p.fmin(x), restored.fmin(x))
                np.testing.assert_allclose(p.rows(x), restored.rows(x))

    def test_original_rows_bounds_integrality_and_finiteness_are_checked(self):
        data = {"name": "diagnostic", "names": ["b", "x"], "vtype": ["B", "C"],
                "lb": [0, -1], "ub": [1, 1], "c": [1, 2], "c0": 3, "sense": -1,
                "rlo": [0], "rhi": [0], "A": {"row": [0], "col": [0], "value": [-1]},
                "oq": [], "rq": {"0": [[1, 1, 1]]}}
        p = Problem(data)
        self.assertTrue(p.validation([1, 1])["valid"])
        self.assertEqual(p.fmin([1, 1]), -6)
        self.assertFalse(p.validation([.25, .5])["valid"])  # row holds, integrality fails
        self.assertFalse(p.validation([1, -2])["valid"])
        self.assertFalse(p.validation([0, .5])["valid"])
        self.assertFalse(p.validation([0, np.nan])["valid"])
        self.assertFalse(p.validation([0])["valid"])

    def test_nonfinite_original_evaluation_is_not_feasible(self):
        p = synthetic("indefinite_qp", 8, 17)
        p.ub[:] = np.inf
        self.assertFalse(p.validation(np.full(p.n, 1e200))["valid"])

    def test_reported_objective_survives_cancellation(self):
        p = synthetic("coupled_squares", 6, 17)
        p.c = np.array([1e16, 1, -1e16, 0, 0, 0])
        p.c0 = 0
        p.oq = {}
        self.assertEqual(p.objective_exact_float(np.ones(p.n)), 1)

    def test_frozen_public_roundtrip_matches_original_parser(self):
        sys.path.insert(0, str(HERE.parents[1] / "research-20260922/iterated-obbt/code"))
        from qcqp import QCQP
        manifest = json.loads((HERE / "frozen/manifest.json").read_text())
        rng = np.random.default_rng(42)
        for entry in manifest["models"]:
            if entry["kind"] != "public":
                continue
            original = QCQP(entry["name"])
            restored = read_problem(HERE / "frozen" / entry["model"])
            for _ in range(3):
                x = rng.uniform(-1, 1, original.n)
                self.assertAlmostEqual(original.fmin(x), restored.fmin(x), places=8)
                np.testing.assert_allclose(original.rows(x), restored.rows(x), rtol=1e-13, atol=1e-10)
                np.testing.assert_allclose(original.lb, restored.lb)
                np.testing.assert_allclose(original.ub, restored.ub)
                np.testing.assert_allclose(original.rlo, restored.rlo)
                np.testing.assert_allclose(original.rhi, restored.rhi)


if __name__ == "__main__":
    unittest.main()
