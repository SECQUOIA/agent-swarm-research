"""Independent original-model binding and saved-cut tamper regressions."""
import copy
from dataclasses import asdict
import math
from pathlib import Path
import sys
import unittest

TOPIC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOPIC))
sys.path.insert(0, str(TOPIC / "experiments"))

from cases import synthetic_cases
from replay import check_run, encode, model_digest, tamper_checks
from solver.certified import replay_support
from solver.integration import run_instance


class ReplayReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = next(case["instance"] for case in synthetic_cases()
                         if case["instance"].name == "simplex_quadratic_vector")
        cls.expected = encode(asdict(cls.model))
        # A single real solve supplies actual emitted rows and proof objects.
        cls.record = run_instance(cls.model, "all", time_limit=3.0)
        cls.record.update(original_model=cls.expected,
                          model_sha256=model_digest(cls.expected), run_id="review_fixture")
        if not cls.record["cuts"]:
            raise AssertionError("mechanism regression generated no added rows")

    def check(self, record):
        return check_run(record, self.expected, replay_support)

    def test_real_saved_rows_replay_and_original_graph_activity(self):
        result = self.check(self.record)
        self.assertTrue(result["passed"], result)
        self.assertEqual(result["replayed_cuts"], len(self.record["cuts"]))
        # Independent direct product evaluation in original coordinates. This
        # checks sign/orientation separately from the support witness replay.
        for cut in self.record["cuts"]:
            for i in range(17):
                for j in range(17 - i):
                    point = [i / 16, j / 16]
                    graph = [point[k] for k in cut["variables"]]
                    for atom_id in cut["atoms"]:
                        tree = self.record["detected_atoms"][atom_id]["tree"]
                        self.assertEqual(tree[0], "times")
                        graph.append(point[tree[1][1]] * point[tree[2][1]])
                    activity = math.fsum(coef * value for coef, value in zip(cut["coefficients"], graph))
                    self.assertGreaterEqual(activity + 1e-12, cut["rhs"])

    def test_distinct_cut_and_model_tampers_fail(self):
        result = tamper_checks(self.record, self.expected, replay_support)
        self.assertGreaterEqual(len(result), 12)
        self.assertTrue(all(result.values()), result)

    def test_recomputed_model_hash_does_not_replace_original_model(self):
        changed = copy.deepcopy(self.record)
        changed["original_model"]["var_ub"][0] = {"binary64": (2.0).hex()}
        changed["model_sha256"] = model_digest(changed["original_model"])
        self.assertFalse(self.check(changed)["passed"])

    def test_source_tree_and_quadratic_map_corruption_fail(self):
        for mutate in (
            lambda result: result["detected_atoms"][0].__setitem__("tree", ["square", ["var", 1]]),
            lambda result: result["quadratic_atoms"][0].__setitem__(2, result["quadratic_atoms"][1][2]),
            lambda result: result["rewritten_rows"].__setitem__(0, ["num", 0.0]),
        ):
            changed = copy.deepcopy(self.record)
            mutate(changed)
            self.assertFalse(self.check(changed)["passed"])

    def test_missing_proof_never_counts_as_certified(self):
        changed = copy.deepcopy(self.record)
        del changed["cuts"][0]["certificate"]
        result = self.check(changed)
        self.assertFalse(result["passed"])
        self.assertEqual(result["replayed_cuts"], len(changed["cuts"]) - 1)


if __name__ == "__main__":
    unittest.main()
