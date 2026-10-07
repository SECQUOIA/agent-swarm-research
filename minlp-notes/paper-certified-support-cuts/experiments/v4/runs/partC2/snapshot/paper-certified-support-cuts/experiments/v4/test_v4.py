"""Targeted tests of the campaign-4 runner and snapshot.

Fast tests: mode table, Config and run_instance additions, fresh instances,
job specifications. Solver tests (a few seconds to about a minute):

- with default settings the campaign-4 snapshot separator adds exactly the
  cuts of the campaign-3 snapshot (two campaign-3 smoke models, mode all,
  and one path instance in mode all-diag-mech), each snapshot in its own
  process;
- mode rowdir-wide reproduces the root bound and cut count of the v3d record
  interleaved_path_n20_s4 / all-diag-mech-wide (same code path and limits);
- mode gurobi reaches the known optimum of a path instance and its
  incumbent passes the archived primal check.

Run: ``python -m unittest test_v4`` from this directory, after snapshot.py.
"""
from __future__ import annotations

from fractions import Fraction as Q
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import PYTHON, SNAPSHOT, THREAD_ENV, TOPIC_NAME, V3, V3D
import make_jobs
import mechanism
from v4_worker import ALL_DIAG, SCIP_PARAMETER_SETS, mode_config

SOURCE = SNAPSHOT / TOPIC_NAME
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(SOURCE / "experiments"))

RUNNER = r"""
import json, sys
root, case_path, mode, overrides, time_limit, node_limit = sys.argv[1:7]
sys.path.insert(0, root + "/research-20261003-convexification")
sys.path.insert(0, root + "/research-20261003-convexification/experiments")
from worker import load_model
from solver.integration import Config, run_instance
inst = load_model(json.load(open(case_path)))
r = run_instance(inst, mode, time_limit=float(time_limit), node_limit=int(node_limit),
                 config=Config(**json.loads(overrides)))
separation = r["separation"] or {}
print(json.dumps({"root_dual": r["root_dual"], "dual": r["dual"], "status": r["status"],
                  "cuts": r["cuts"], "callback_seconds": separation.get("callback_seconds"),
                  "certification_calls": separation.get("certification_calls")}))
"""


def run_snapshot(root, case_path, mode, overrides, time_limit, node_limit=1):
    env = {**os.environ, **THREAD_ENV, "PYTHONDONTWRITEBYTECODE": "1"}
    out = subprocess.run([str(PYTHON), "-c", RUNNER, str(root), str(case_path), mode, json.dumps(overrides),
                          str(time_limit), str(node_limit)], capture_output=True, text=True, env=env,
                         timeout=600, check=True)
    return json.loads(out.stdout.strip().splitlines()[-1])


class ModeTable(unittest.TestCase):
    def test_limits_and_parameters(self):
        n40 = {"mechanism": {"n": 40}}
        mech = {"max_blocks": 40, "max_cuts": 160, "max_cuts_per_round": 40, "max_rounds": 10,
                "max_support_calls": 800, "max_separation_seconds": 60.0, "separation_budget_fraction": 0.5}
        wide = {"max_blocks": 40, "max_cuts": 640, "max_cuts_per_round": 160, "max_rounds": 10,
                "max_support_calls": 1600, "max_separation_seconds": 60.0, "separation_budget_fraction": 0.5}
        noaggr = {"presolving/donotaggr": True, "presolving/donotmultaggr": True}
        self.assertEqual(mode_config("all-diag-mech", n40), ("all", mech, {}))
        self.assertEqual(mode_config("frozen-wide", n40), ("all", wide, {}))
        self.assertEqual(mode_config("rowdir-wide", n40), ("all", {**wide, "row_directions": True}, {}))
        self.assertEqual(mode_config("all-diag-rowdir", {}), ("all", {**ALL_DIAG, "row_directions": True}, {}))
        self.assertEqual(mode_config("baseline-novarlocks", {}),
                         ("baseline", {}, {"constraints/nonlinear/checkvarlocks": "d"}))
        self.assertEqual(mode_config("baseline-extra", {}), ("baseline", {}, SCIP_PARAMETER_SETS["extra"]))
        self.assertEqual(mode_config("all-diag-rowdir-noaggr", {}),
                         ("all", {**ALL_DIAG, "row_directions": True}, noaggr))
        self.assertEqual(mode_config("baseline-noaggr", {}), ("baseline", {}, noaggr))
        self.assertEqual(mode_config("all-noaggr", {}), ("all", {}, noaggr))
        self.assertEqual(mode_config("auto", {}), ("auto", {}, {}))
        for mode in ("gurobi", "all-diag-mech-wide", "baseline-extra-noaggr"):
            with self.assertRaises(ValueError):
                mode_config(mode, n40)
        with self.assertRaises(KeyError):
            mode_config("frozen-wide", {})

    def test_snapshot_records_the_parameters(self):
        record = json.loads((SNAPSHOT / "scip-parameters.json").read_text())
        self.assertEqual(record["scip_version"], "10.0.2")
        self.assertEqual({k: {p: v["value"] for p, v in s.items()} for k, s in record["sets"].items()},
                         SCIP_PARAMETER_SETS)


class SnapshotAdditions(unittest.TestCase):
    def test_config_flag(self):
        from dataclasses import asdict
        from solver.integration import Config
        self.assertIs(Config().row_directions, False)
        self.assertIs(Config(row_directions=True).row_directions, True)
        for bad in (1, 0, "yes", None):
            with self.assertRaises(ValueError):
                Config(row_directions=bad)
        frozen = dict(asdict(Config()))
        self.assertEqual(frozen.pop("row_directions"), False)
        v3 = json.loads(next((V3 / "runs/partC").glob("runs/*baseline.json")).read_text())["config"]
        self.assertEqual(frozen, v3)  # every other default is the campaign-3 value

    def test_scip_params_are_set_and_recorded(self):
        from solver.integration import run_instance
        from cases import synthetic_cases
        inst = next(c["instance"] for c in synthetic_cases() if c["instance"].name == "simplex_product")
        params = SCIP_PARAMETER_SETS["extra"]
        result = run_instance(inst, "baseline", time_limit=10.0, scip_params=params)
        self.assertEqual(result["scip_params"], params)
        self.assertEqual(run_instance(inst, "baseline", time_limit=10.0)["scip_params"], {})
        with self.assertRaises(ValueError):
            run_instance(inst, "baseline", time_limit=10.0, scip_params={"limits/time": 1.0})
        with self.assertRaises(KeyError):
            run_instance(inst, "baseline", time_limit=10.0, scip_params={"no/such/parameter": 1})

    def test_patched_file_differs_from_v3_only_by_the_additions(self):
        import snapshot
        relative = f"{TOPIC_NAME}/solver/integration.py"
        v3 = (V3 / "snapshot" / relative).read_text()
        self.assertEqual(snapshot.patched_integration(v3), (SNAPSHOT / relative).read_text())


class Instances(unittest.TestCase):
    def test_fresh_instances_are_exact_and_new(self):
        from cases import Instance, check_primal
        cases = make_jobs.c3_cases()
        self.assertEqual(len(cases), 20)
        self.assertEqual(sorted({(c["mechanism"]["n"], c["mechanism"]["seed"]) for c in cases}),
                         [(n, s) for n in (10, 20, 40, 80) for s in range(5, 10)])
        for case in cases[:2] + cases[-2:]:
            model, optimum, witness, records = mechanism.instance(case["mechanism"]["n"], case["mechanism"]["seed"])
            self.assertEqual(Q(case["known_optimum_exact"]), optimum)
            rows = [dict(row, quad=[tuple(q) for q in row["quad"]]) for row in model["rows"]]
            check = check_primal(Instance(**{**model, "rows": rows}), [float(v) for v in witness], float(optimum))
            self.assertTrue(check["passed"])
            self.assertEqual(check["max_scaled_violation"], 0.0)

    def test_c2_cases_are_the_campaign3_cases(self):
        self.assertEqual(len(make_jobs.c2_cases()), 20)  # c2_cases compares each with campaign 3
        self.assertEqual(len(make_jobs.b2_cases()), 30)


class Jobs(unittest.TestCase):
    def test_counts_rotation_and_limits(self):
        cases = make_jobs.c3_cases()
        jobs = make_jobs.jobs_for(cases, [make_jobs.C3_FULL, make_jobs.C3_ROOT], make_jobs.larger_first)
        self.assertEqual((len(jobs), sum(len(j["runs"]) for j in jobs)), (40, 180))
        self.assertEqual([j["phase"] for j in jobs[:20]], ["full"] * 20)
        self.assertEqual(jobs[0]["name"], "interleaved_path_n80_s5")
        position = {c["name"]: i for i, c in enumerate(cases)}
        for job in jobs:
            modes = tuple(r["mode"] for r in job["runs"])
            declared = make_jobs.C3_FULL[2] if job["phase"] == "full" else make_jobs.C3_ROOT[2]
            k = position[job["name"]] % len(declared)
            self.assertEqual(modes, declared[k:] + declared[:k])
            limits = (300.0, 360.0, None) if job["phase"] == "full" else (120.0, 180.0, 1)
            self.assertEqual((job["time_limit"], job["worker_timeout"], job["node_limit"]), limits)
        c2 = make_jobs.jobs_for(make_jobs.c2_cases(), [make_jobs.C2_FULL, make_jobs.C2_ROOT])
        self.assertEqual(sum(len(j["runs"]) for j in c2), 140)
        b2 = make_jobs.jobs_for(make_jobs.b2_cases(), [make_jobs.B2_ROOT])
        self.assertEqual(sum(len(j["runs"]) for j in b2), 150)
        self.assertTrue(all(j["node_limit"] == 1 and j["time_limit"] == 60 for j in b2))
        d = [{"name": f"m{i}", "suite": "larger"} for i in range(20)]
        self.assertEqual(sum(len(j["runs"]) for j in make_jobs.jobs_for(d, [make_jobs.D_ROOT])), 100)
        self.assertEqual(sum(len(j["runs"]) for j in make_jobs.jobs_for(d, [make_jobs.D_FULL])), 80)


class SolverBehaviour(unittest.TestCase):
    def test_defaults_reproduce_campaign3_cuts(self):
        root = V3 / "runs/partA-root/cases"
        targets = [(root / "ex4_1_8.json", "all", {}), (root / "cvxnonsep_normcon20r.json", "all", {}),
                   (V3 / "runs/partC/cases/interleaved_path_n10_s0.json", "all", mode_config(
                       "all-diag-mech", {"mechanism": {"n": 10}})[1])]
        for case, mode, overrides in targets:
            with self.subTest(case=case.stem):
                old = run_snapshot(V3 / "snapshot", case, mode, overrides, 60.0)
                new = run_snapshot(SNAPSHOT, case, mode, overrides, 60.0)
                new_flag_off = run_snapshot(SNAPSHOT, case, mode, {**overrides, "row_directions": False}, 60.0)
                self.assertGreater(len(old["cuts"]), 0)
                for result in (new, new_flag_off):
                    self.assertEqual(result["cuts"], old["cuts"])
                    self.assertEqual((result["root_dual"], result["certification_calls"]),
                                     (old["root_dual"], old["certification_calls"]))

    def test_rowdir_wide_reproduces_v3d_record(self):
        name = "interleaved_path_n20_s4"
        records = [json.loads(line) for line in (V3D / "runs/partC-rowdir/records.jsonl").read_text().splitlines()]
        archived = next(r for r in records if r["name"] == name and r["phase"] == "root"
                        and r["mode"] == "all-diag-mech-wide")
        case = V3D / "runs/partC-rowdir/cases" / f"{name}.json"
        overrides = mode_config("rowdir-wide", {"mechanism": {"n": 20}})[1]
        result = run_snapshot(SNAPSHOT, case, "all", overrides, 120.0)
        self.assertEqual(result["root_dual"], archived["root_dual"])
        self.assertEqual(len(result["cuts"]), len(archived["cuts"]))
        self.assertEqual([c["coefficients"] for c in result["cuts"]], [c["coefficients"] for c in archived["cuts"]])
        frozen = run_snapshot(SNAPSHOT, case, "all", {**overrides, "row_directions": False}, 120.0)
        self.assertLess(frozen["root_dual"], result["root_dual"])

    def test_gurobi_mode_on_a_path_instance(self):
        from worker import load_model
        from cases import check_primal
        from v4_worker import run_gurobi
        case = json.loads((V3 / "runs/partC/cases/interleaved_path_n10_s0.json").read_text())
        model = load_model(case)
        result = run_gurobi(model, 60.0, 0)
        self.assertIn(result["status"], ("optimal", "gaplimit"))
        self.assertEqual(result["gurobi_params"]["Threads"], 1)
        self.assertLessEqual(abs(result["primal"] - case["known_optimum"]), 1e-4 * max(1, case["known_optimum"]))
        self.assertLessEqual(result["dual"], case["known_optimum"] + 1e-6)
        self.assertTrue(check_primal(model, result["original_values"], result["primal"])["passed"])


if __name__ == "__main__":
    unittest.main()
