"""Distinct regression checks for all-run scoring, including invalid results."""
import unittest

from analyze import paired, row_for, summarize


def task(name="a", arm="native"):
    return {"name": name, "kind": "public", "family": name, "arm": arm, "seed": 0,
            "key": name+"__"+arm+"__0", "time_limit": 10}


def raw(status="optimal", valid=True, incumbent=True):
    return {"process_complete": True, "process_exitcode": 0, "process_wall_seconds": 2,
            "outcome": {"status": status, "solution": [0] if incumbent else None,
                        "dual_bound": 0, "obbt": {}},
            "validation": {"valid": valid, "objective_min": 0} if incumbent else None}


class ScoringTests(unittest.TestCase):
    def test_invalid_incumbent_and_process_failure_are_not_successes(self):
        invalid = row_for(task(), raw(valid=False))
        self.assertFalse(invalid["solved"])
        self.assertTrue(invalid["invalid_incumbent"])
        self.assertEqual(invalid["par2"], 20)
        crashed = raw()
        crashed["process_exitcode"] = 1
        self.assertFalse(row_for(task(), crashed)["solved"])
        inverted = raw()
        inverted["outcome"]["dual_bound"] = 1
        self.assertTrue(row_for(task(), inverted)["inconsistent_bounds"])
        self.assertFalse(row_for(task(), inverted)["solved"])

    def test_paired_comparison_keeps_unsolved_and_missing_incumbents(self):
        rows = [row_for(task("a"), raw()),
                row_for(task("a", "adaptive"), raw("timelimit", incumbent=False)),
                row_for(task("b"), raw("timelimit", incumbent=False)),
                row_for(task("b", "adaptive"), raw())]
        p = paired(rows, "adaptive")
        self.assertEqual(p["pairs"], 2)
        self.assertEqual(len(p["new_solves"]), 1)
        self.assertEqual(len(p["lost_solves"]), 1)
        self.assertEqual(p["comparable_finite_gaps"], 0)
        s = summarize([r for r in rows if r["arm"] == "native"])
        self.assertEqual(s["runs"], 2)
        self.assertEqual(s["mean_par2_seconds"], 11)
        self.assertEqual(s["mean_gap_score"], .5)

    def test_missing_cost_is_rejected_instead_of_invented(self):
        outcome = raw()
        del outcome["process_wall_seconds"]
        with self.assertRaisesRegex(ValueError, "Missing finite observed"):
            row_for(task(), outcome)


if __name__ == "__main__":
    unittest.main()
