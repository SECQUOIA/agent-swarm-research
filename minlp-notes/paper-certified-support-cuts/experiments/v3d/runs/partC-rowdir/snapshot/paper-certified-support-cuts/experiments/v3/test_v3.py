"""Targeted tests of the v3 runner: instance data, mode configs, job specs."""
from __future__ import annotations

from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "research-20261003-convexification/experiments"))

import make_jobs
import mechanism
from v3_worker import mode_config


class MechanismFamily(unittest.TestCase):
    def test_proposition_example_matches_pilot_coefficients(self):
        # pilot_native.py: D = 1.25x - 0.5y + z - 0.75x^2 + 2y^2 - 0.609375z^2 - xy - 1.25yz + 0.0625
        linear, quadratic, constant = mechanism.expand((Q(1, 4), Q(3, 4)), (Q(0), Q(5, 8)))
        self.assertEqual(linear, {"x": Q(5, 4), "y": Q(-1, 2), "z": Q(1)})
        self.assertEqual(quadratic, {("x", "x"): Q(-3, 4), ("y", "y"): Q(2), ("z", "z"): Q(-39, 64),
                                     ("x", "y"): Q(-1), ("y", "z"): Q(-5, 4)})
        self.assertEqual(constant, Q(1, 16))

    def test_instances_are_exact_interleaved_and_attain_the_optimum(self):
        from cases import Instance, check_primal
        for n, seed in ((10, 0), (80, 4)):
            model, optimum, witness, records = mechanism.instance(n, seed)
            self.assertEqual(mechanism.instance(n, seed)[0], model)  # deterministic
            self.assertEqual(len(model["rows"]), n + 2)
            self.assertEqual(optimum, sum(Q(r["delta"]) ** 2 / 2 for r in records))
            for r in records:
                a, c = sorted(map(Q, r["a"])), sorted(map(Q, r["c"]))
                values = sorted(a + c)
                self.assertTrue(set(a) in ({values[0], values[2]}, {values[1], values[3]}))
                self.assertTrue(all(v.denominator <= 64 and 0 <= v <= Q(3, 4) for v in values))
            rows = [dict(row, quad=[tuple(q) for q in row["quad"]]) for row in model["rows"]]
            check = check_primal(Instance(**{**model, "rows": rows}), [float(v) for v in witness], float(optimum))
            self.assertTrue(check["passed"])
            self.assertEqual(check["max_scaled_violation"], 0.0)
            self.assertEqual(Q(check["objective"]), optimum)

    def test_case_round_trips_through_archived_loader(self):
        from run_campaign import exact_json
        from worker import load_model
        from dataclasses import asdict
        case = json.loads(json.dumps(mechanism.case(10, 1, exact_json)))
        self.assertEqual(exact_json(asdict(load_model(case))), case["model"])
        self.assertEqual(Q(case["known_optimum"]), Q(case["known_optimum_exact"]))


class Modes(unittest.TestCase):
    def test_diagnostic_configs(self):
        self.assertEqual(mode_config("all-diag", {}), ("all", {
            "max_blocks": 128, "max_cuts": 200, "max_cuts_per_round": 50, "max_rounds": 10,
            "max_support_calls": 500, "max_separation_seconds": 30.0, "separation_budget_fraction": 0.5}))
        self.assertEqual(mode_config("all-diag-mech", {"mechanism": {"n": 40}}), ("all", {
            "max_blocks": 40, "max_cuts": 160, "max_cuts_per_round": 40, "max_rounds": 10,
            "max_support_calls": 800, "max_separation_seconds": 60.0, "separation_budget_fraction": 0.5}))
        self.assertEqual(mode_config("auto", {}), ("auto", {}))
        with self.assertRaises(KeyError):
            mode_config("all-diag-mech", {})


class Jobs(unittest.TestCase):
    def test_rotation_and_counts(self):
        cases = [{"name": f"m{i}", "suite": "s"} for i in range(30)]
        jobs = make_jobs.jobs_for(cases, [make_jobs.A_FULL])
        self.assertEqual((len(jobs), sum(len(j["runs"]) for j in jobs)), (90, 270))
        for job in jobs:
            modes = [r["mode"] for r in job["runs"]]
            offset = (int(job["name"][1:]) + job["seed"]) % 3
            self.assertEqual(modes, list(make_jobs.FULL_MODES[offset:] + make_jobs.FULL_MODES[:offset]))
        ids = [r["run_id"] for j in jobs for r in j["runs"]]
        self.assertEqual(len(set(ids)), len(ids))
        root = make_jobs.jobs_for(cases, [make_jobs.AB_ROOT])
        self.assertEqual(sum(len(j["runs"]) for j in root), 120)
        self.assertTrue(all(j["node_limit"] == 1 and j["time_limit"] == 60 and j["worker_timeout"] == 90 for j in root))


if __name__ == "__main__":
    unittest.main()
