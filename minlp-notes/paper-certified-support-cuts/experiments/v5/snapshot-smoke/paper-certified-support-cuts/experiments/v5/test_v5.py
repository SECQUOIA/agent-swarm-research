"""Targeted tests of the campaign-5 runner and snapshot.

Fast tests: mode table (campaign-4 modes unchanged, campaign-5 modes), Config
additions, patched file, star discovery, the block direction's exact support,
instances and job specifications. Solver tests (a few seconds to about a
minute):

- with default settings (and with both additions explicitly off) the
  campaign-5 snapshot gives exactly the cuts, root bound, final bound and
  support-call count of the campaign-4 snapshot, each snapshot in its own
  process, on a campaign-4 path instance (interleaved_path_coupled_n10_s5,
  mode rowdir-wide) and a MINLPLib model (ex8_1_7, mode
  all-diag-rowdir-noaggr), and both equal the archived campaign-4 records;
- in mode agg-star on a small star instance, star blocks yield cuts certified
  by the inherited constrained-star oracle (method quadratic_star), every cut
  replays with the archived checker, and every tampering control is rejected.

Run: ``python -m unittest test_v5`` from this directory, after snapshot.py.
"""
from __future__ import annotations

from dataclasses import asdict
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import PYTHON, SNAPSHOT, THREAD_ENV, TOPIC_NAME, V4
import make_jobs
import stars
from v5_worker import CAP_MODES, SCIP_MODES_V4, SCIP_PARAMETER_SETS, STAR_MODES, mode_config

SOURCE = SNAPSHOT / TOPIC_NAME
for entry in (SOURCE, SOURCE / "experiments", SNAPSHOT / "code/univariate_envelopes"):
    sys.path.insert(0, str(entry))

RUNNER = r"""
import json, sys
root, case_path, osil, mode, overrides, params, time_limit, node_limit = sys.argv[1:9]
sys.path.insert(0, root + "/research-20261003-convexification")
sys.path.insert(0, root + "/research-20261003-convexification/experiments")
from worker import load_model
from solver.integration import Config, run_instance
case = json.load(open(case_path))
if osil:
    case["path"] = osil
inst = load_model(case)
r = run_instance(inst, mode, time_limit=float(time_limit), node_limit=int(node_limit),
                 config=Config(**json.loads(overrides)), scip_params=json.loads(params))
separation = r["separation"] or {}
print(json.dumps({"root_dual": r["root_dual"], "dual": r["dual"], "status": r["status"],
                  "cuts": r["cuts"], "certification_calls": separation.get("certification_calls")}))
"""


def run_snapshot(root, case_path, mode, overrides, params, time_limit, osil=""):
    env = {**os.environ, **THREAD_ENV, "PYTHONDONTWRITEBYTECODE": "1"}
    out = subprocess.run([str(PYTHON), "-c", RUNNER, str(root), str(case_path), str(osil), mode,
                          json.dumps(overrides), json.dumps(params), str(time_limit), "1"],
                         capture_output=True, text=True, env=env, timeout=600, check=True)
    return json.loads(out.stdout.strip().splitlines()[-1])


def load_file(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def star_model(k, n, seed):
    from run_campaign import exact_json
    from worker import load_model
    case = json.loads(json.dumps(stars.case(k, n, seed, exact_json)))
    return case, load_model(case)


class ModeTable(unittest.TestCase):
    def test_campaign4_modes_unchanged(self):
        v4 = load_file(V4 / "v4_worker.py", "v4_worker_reference")
        self.assertEqual(SCIP_MODES_V4, v4.SCIP_MODES)
        for mode in SCIP_MODES_V4:
            for case in ({}, {"mechanism": {"n": 40}}):
                try:
                    expected = v4.mode_config(mode, case)
                except KeyError:
                    with self.assertRaises(KeyError):
                        mode_config(mode, case)
                    continue
                self.assertEqual(mode_config(mode, case), expected)

    def test_campaign5_modes(self):
        case = {"star": {"n": 20, "k": 8}}
        limits = {"max_blocks": 160, "max_cuts": 640, "max_cuts_per_round": 160, "max_rounds": 10,
                  "max_support_calls": 1600, "max_separation_seconds": 60.0, "separation_budget_fraction": 0.5}
        self.assertEqual(mode_config("rowdir-star4", case), ("all", {**limits, "row_directions": True}, {}))
        self.assertEqual(mode_config("agg-star4", case),
                         ("all", {**limits, "aggregate_directions": True, "row_directions": True}, {}))
        self.assertEqual(mode_config("agg-star", case),
                         ("all", {**limits, "aggregate_directions": True, "row_directions": True,
                                  "star_leaves": 16}, {}))
        n40 = {"mechanism": {"n": 40}}
        cap = lambda cuts, per, support: {"max_blocks": 40, "max_cuts": cuts, "max_cuts_per_round": per,
                                          "max_rounds": 10, "max_support_calls": support,
                                          "max_separation_seconds": 150.0, "separation_budget_fraction": 0.5}
        self.assertEqual(mode_config("frozen-cap32", n40), ("all", cap(1280, 320, 3200), {}))
        self.assertEqual(mode_config("rowdir-cap32", n40), ("all", {**cap(1280, 320, 3200), "row_directions": True}, {}))
        self.assertEqual(mode_config("frozen-cap64", n40), ("all", cap(2560, 640, 6400), {}))
        self.assertEqual(mode_config("rowdir-cap64", n40), ("all", {**cap(2560, 640, 6400), "row_directions": True}, {}))
        for mode in STAR_MODES + CAP_MODES:
            with self.assertRaises(KeyError):
                mode_config(mode, {})
        with self.assertRaises(ValueError):
            mode_config("agg-star-noaggr", case)

    def test_snapshot_records_the_parameters(self):
        record = json.loads((SNAPSHOT / "scip-parameters.json").read_text())
        self.assertEqual({k: {p: v["value"] for p, v in s.items()} for k, s in record["sets"].items()},
                         SCIP_PARAMETER_SETS)


class SnapshotAdditions(unittest.TestCase):
    def test_config_fields(self):
        from solver.integration import Config
        self.assertIs(Config().aggregate_directions, False)
        self.assertEqual(Config().star_leaves, 0)
        self.assertEqual(Config(aggregate_directions=True, star_leaves=16).star_leaves, 16)
        for bad in (1, 0, "yes", None):
            with self.assertRaises(ValueError):
                Config(aggregate_directions=bad)
        for bad in (-1, True, 1.0, "16", None):
            with self.assertRaises(ValueError):
                Config(star_leaves=bad)
        with self.assertRaises(ValueError):  # the dimension cap of four stays for the other blocks
            Config(max_dimensions=5, star_leaves=16)
        frozen = dict(asdict(Config()))
        self.assertEqual((frozen.pop("aggregate_directions"), frozen.pop("star_leaves")), (False, 0))
        v4 = json.loads(next((V4 / "runs/partC4").glob("runs/*__baseline.json")).read_text())["config"]
        self.assertEqual(frozen, v4)  # every other default is the campaign-4 value

    def test_patched_file_differs_from_v4_only_by_the_additions(self):
        import snapshot
        relative = f"{TOPIC_NAME}/solver/integration.py"
        self.assertEqual(snapshot.patched_integration((V4 / "snapshot" / relative).read_text()),
                         (SNAPSHOT / relative).read_text())


class StarDiscovery(unittest.TestCase):
    def discover(self, inst, **overrides):
        from solver.integration import Config, discover
        from solver.model import build_model
        built = build_model(inst)
        try:
            return built, discover(inst, built, Config(**overrides))
        finally:
            built.model.freeProb()

    def test_star_blocks_first_with_their_sides_and_rows(self):
        case, inst = star_model(4, 10, 0)
        k, n = 4, 10
        _, detected = self.discover(inst, star_leaves=16, max_blocks=40)
        self.assertEqual(detected.stats["star_blocks"], n)
        for i, block in enumerate(detected.blocks[:n]):
            y = stars.indices(k, i)
            self.assertEqual(block.variables, (y,) + tuple(stars.indices(k, i, j)[0] for j in range(k)))
            self.assertEqual([s.row_index for s in block.sides], [1 + k * i + j for j in range(k)])
            self.assertEqual([r["row_index"] for r in block.domain_records], [1 + n * k + k * i + j for j in range(k)])
            self.assertTrue(block.quadratic)
        self.assertTrue(all(len(b.variables) <= 4 for b in detected.blocks[n:]))
        _, truncated = self.discover(inst, star_leaves=2, max_blocks=40)
        self.assertEqual(truncated.blocks[0].variables, (0, 1, 3))
        self.assertEqual([s.row_index for s in truncated.blocks[0].sides], [1, 2])
        self.assertEqual(len(truncated.blocks[0].rows), 2)

    def test_off_by_default(self):
        _, inst = star_model(4, 10, 0)
        _, default = self.discover(inst, max_blocks=40)
        _, explicit = self.discover(inst, max_blocks=40, star_leaves=0, aggregate_directions=False)
        self.assertNotIn("star_blocks", default.stats)
        self.assertEqual(default.stats, explicit.stats)
        self.assertEqual([(b.variables, [s.source_id for s in b.sides], b.rows) for b in default.blocks],
                         [(b.variables, [s.source_id for s in b.sides], b.rows) for b in explicit.blocks])
        self.assertTrue(all(len(b.variables) <= 4 for b in default.blocks))


class BlockDirection(unittest.TestCase):
    def test_block_direction_support_is_the_exact_star_minimum(self):
        from solver.integration import Config, RowSeparator, discover
        from solver.model import build_model
        from solver.support import certify_support
        for k, n, seed in ((4, 10, 0), (16, 10, 3)):
            case, inst = star_model(k, n, seed)
            config = Config(**mode_config("agg-star", case)[1])
            built = build_model(inst)
            try:
                detected = discover(inst, built, config)
                separator = RowSeparator(inst, built, "all", config, 60.0)
            finally:
                built.model.freeProb()
            for i in (0, n - 1):
                block = detected.blocks[i]
                query = separator._query(block, (0.0,) * len(separator.names))
                directions = list(separator._directions(block, query, time.perf_counter()))
                self.assertEqual(len(directions), 1 + k)  # block direction, then k whole-row directions
                first = directions[0]
                self.assertEqual(first[len(block.variables):], (1.0,) * k)
                leaves = [tuple(Q(v) for v in leaf) for leaf in case["star"]["leaves"][i]]
                expected_a = [sum(-2 * a1 for a1, _, _ in leaves)] + [2 * a1 * (a2 - a1) + 1 for a1, a2, _ in leaves]
                self.assertEqual([Q(v) for v in first[:len(block.variables)]], expected_a)
                result = certify_support(block.features, block.symbols, block.box, first, rows=block.rows,
                                         max_cells=config.max_cells, max_depth=config.max_depth,
                                         max_polytope_faces=config.max_faces)
                self.assertEqual(result.witness["method"], "quadratic_star")
                constant = sum((a1 * a1 for a1, _, _ in leaves), Q(0))
                self.assertEqual(Q(result.stats["exact_support"]), Q(case["star"]["star_optima"][i]) - constant)
                self.assertLessEqual(Q(result.cut.rhs), Q(case["star"]["star_optima"][i]) - constant)

    def test_four_variable_blocks_start_with_the_block_direction(self):
        from solver.integration import Config, RowSeparator, discover
        from solver.model import build_model
        case, inst = star_model(4, 10, 0)
        config = Config(**mode_config("agg-star4", case)[1])
        built = build_model(inst)
        try:
            detected = discover(inst, built, config)
            separator = RowSeparator(inst, built, "all", config, 60.0)
        finally:
            built.model.freeProb()
        block = detected.blocks[0]
        self.assertEqual(len(block.variables), 4)
        query = separator._query(block, (0.0,) * len(separator.names))
        directions = separator._directions(block, query, time.perf_counter())
        first, second = next(directions), next(directions)
        self.assertEqual(first[4:], (1.0,) * len(block.sides))
        self.assertEqual(second[4:], (1.0,) + (0.0,) * (len(block.sides) - 1))


class StarCutReplay(unittest.TestCase):
    def test_recorded_star_cut_replays_and_tampering_is_rejected(self):
        from cases import check_primal
        from run_campaign import exact_json
        from solver.integration import Config, run_instance
        from solver.support import replay_support
        archived = load_file(SOURCE / "experiments/replay.py", "archived_replay_test")
        replay = load_file(HERE / "replay_v5.py", "replay_v5_test")
        case, inst = star_model(4, 5, 0)
        solver_mode, overrides, _ = mode_config("agg-star", case)
        result = run_instance(inst, solver_mode, time_limit=60.0, node_limit=1, config=Config(**overrides))
        methods = [c["support_witness"]["method"] for c in result["cuts"]]
        self.assertIn("quadratic_star", methods)
        self.assertEqual(result["discovery"]["star_blocks"], 5)
        self.assertLessEqual(result["dual"], case["known_optimum"] + 1e-6)
        encoded = exact_json(asdict(inst))
        self.assertEqual(encoded, case["model"])
        record = {**result, "mode": "agg-star", "original_model": encoded,
                  "model_sha256": hashlib.sha256(json.dumps(encoded, sort_keys=True).encode()).hexdigest()}
        expected = archived.load_expected_model(case, SNAPSHOT)
        checked = archived.check_run(record, expected, replay_support)
        self.assertTrue(checked["passed"], checked["failures"])
        self.assertEqual(checked["replayed_cuts"], len(result["cuts"]))
        star_cut = replay.only_cut(record, methods.index("quadratic_star"))
        self.assertGreater(len(star_cut["cuts"][0]["variables"]), 4)
        self.assertTrue(archived.check_run(star_cut, expected, replay_support)["passed"])
        rejections = replay.star_tamper_checks(archived, archived.tamper_checks, star_cut, expected, replay_support)
        self.assertEqual(set(replay.STAR_MUTATIONS) - set(rejections), set())
        self.assertTrue(all(rejections.values()), rejections)
        self.assertTrue(check_primal(inst, case["known_witness"], case["known_optimum"])["passed"])


class DefaultsReproduceCampaign4(unittest.TestCase):
    def test_same_cuts_and_bounds_as_campaign4(self):
        c4 = V4 / "runs/partC4"
        b2 = V4 / "runs/partB2"
        targets = [("interleaved_path_coupled_n10_s5", c4, "rowdir-wide", 120.0, ""),
                   ("ex8_1_7", b2, "all-diag-rowdir-noaggr", 60.0, b2 / "snapshot/original-osil/ex8_1_7.osil")]
        for name, part, mode, limit, osil in targets:
            with self.subTest(case=name):
                case_path = part / "cases" / f"{name}.json"
                solver_mode, overrides, params = mode_config(mode, json.loads(case_path.read_text()))
                record = next(json.loads(line) for line in (part / "records.jsonl").read_text().splitlines()
                              if f'"{name}"' in line and json.loads(line)["mode"] == mode
                              and json.loads(line)["phase"] == "root")
                old = run_snapshot(V4 / "snapshot", case_path, solver_mode, overrides, params, limit, osil)
                new = run_snapshot(SNAPSHOT, case_path, solver_mode, overrides, params, limit, osil)
                off = run_snapshot(SNAPSHOT, case_path, solver_mode,
                                   {**overrides, "aggregate_directions": False, "star_leaves": 0}, params, limit, osil)
                self.assertGreater(len(old["cuts"]), 0)
                for result in (new, off):
                    self.assertEqual(result["cuts"], old["cuts"])
                    self.assertEqual((result["root_dual"], result["dual"], result["certification_calls"]),
                                     (old["root_dual"], old["dual"], old["certification_calls"]))
                self.assertEqual(old["root_dual"], record["root_dual"])
                self.assertEqual([c["coefficients"] for c in old["cuts"]], [c["coefficients"] for c in record["cuts"]])


class Instances(unittest.TestCase):
    def test_star_instances(self):
        cases = make_jobs.star_cases()  # archived primal check of every witness, names new
        self.assertEqual(sorted((c["star"]["k"], c["star"]["n"], c["star"]["seed"]) for c in cases),
                         [(k, n, s) for k in (4, 8, 16) for n in (10, 20) for s in range(5)])
        from run_campaign import exact_json
        sweep = stars.load_sweep()
        for case in cases[:1] + cases[-1:]:
            k, n, seed = case["star"]["k"], case["star"]["n"], case["star"]["seed"]
            self.assertEqual(case, json.loads(json.dumps(stars.case(k, n, seed, exact_json, sweep))))
            self.assertEqual(case["star"]["rng"], f"random.Random({100000 * k + 1000 * n + seed})")
            self.assertEqual(Q(case["known_optimum_exact"]), sum(Q(v) for v in case["star"]["star_optima"]))
            self.assertLessEqual(Q(case["star"]["sum_smallest_minimizers"]), Q(4 * n, 5))
            model = case["model"]
            self.assertEqual(len(model["var_lb"]), n * (2 * k + 1))
            self.assertEqual(len(model["rows"]), 2 * n * k + 2)
            for star in case["star"]["leaves"]:
                for a1, a2, d in star:
                    self.assertNotEqual(a1, a2)
                    self.assertTrue(0 <= Q(a1) * 64 <= 48 and (Q(a1) * 64).denominator == 1)
                    self.assertIn(Q(d), (Q(1, 8), Q(1, 4), Q(1, 2), Q(1)))
        first = stars.draw(4, 10, 0)[0][0]
        import random
        rng = random.Random(410000)
        m1, m2 = rng.sample(range(49), 2)
        self.assertEqual(first, (Q(m1, 64), Q(m2, 64), rng.choice(stars.SLACKS)))

    def test_path_cases_are_the_campaign4_cases(self):
        self.assertEqual(len(make_jobs.c3_cases()), 20)  # each equals its generator and the v4 file
        c4 = make_jobs.c4_cases()
        self.assertEqual(len(c4), 20)
        self.assertTrue(all("reference_bound_ii" in c for c in c4))


class Jobs(unittest.TestCase):
    def check_rotation(self, cases, jobs, phases):
        position = {c["name"]: i for i, c in enumerate(cases)}
        for job in jobs:
            declared = next(p for p in phases if p[0] == job["phase"])
            modes = tuple(r["mode"] for r in job["runs"])
            k = (position[job["name"]] + job["seed"]) % len(declared[2])
            self.assertEqual(modes, declared[2][k:] + declared[2][:k])
            self.assertEqual((job["time_limit"], job["worker_timeout"], job["node_limit"]), declared[3:])

    def test_counts_order_rotation_and_limits(self):
        cases, jobs, _ = make_jobs.build("partS5", False)
        self.assertEqual((len(jobs), sum(len(j["runs"]) for j in jobs)), (60, 390))
        self.assertEqual([j["phase"] for j in jobs[:30]], ["full"] * 30)
        self.assertEqual(jobs[0]["name"], "constrained_star_k16_n20_s0")
        self.assertEqual(jobs[29]["name"], "constrained_star_k4_n10_s4")
        self.check_rotation(cases, jobs, [make_jobs.S5_FULL, make_jobs.S5_ROOT])
        cases, jobs, _ = make_jobs.build("partC5a", False)
        self.assertEqual((len(jobs), sum(len(j["runs"]) for j in jobs)), (80, 80))
        self.assertEqual([j["phase"] for j in jobs[:40]], ["full"] * 40)
        self.assertEqual([j["name"] for j in jobs[:6]], [f"interleaved_path_n80_s{s}" for s in range(5, 10)]
                         + ["interleaved_path_coupled_n80_s5"])
        self.check_rotation(cases, jobs, [make_jobs.C5A_FULL, make_jobs.C5A_ROOT])
        cases, jobs, _ = make_jobs.build("partC5b", False)
        self.assertEqual((len(jobs), sum(len(j["runs"]) for j in jobs)), (20, 80))
        self.assertEqual(jobs[0]["name"], "interleaved_path_coupled_n80_s5")
        self.check_rotation(cases, jobs, [make_jobs.C5B_ROOT])
        for part, names in (("partS5", ["constrained_star_k4_n10_s0"]),
                            ("partC5a", ["interleaved_path_n10_s5", "interleaved_path_coupled_n10_s5"]),
                            ("partC5b", ["interleaved_path_coupled_n10_s5"])):
            cases, jobs, _ = make_jobs.build(part, True)
            self.assertEqual([c["name"] for c in cases], names)
            self.assertTrue(all((j["time_limit"], j["worker_timeout"]) == (10.0, 30.0) for j in jobs))


if __name__ == "__main__":
    unittest.main()
