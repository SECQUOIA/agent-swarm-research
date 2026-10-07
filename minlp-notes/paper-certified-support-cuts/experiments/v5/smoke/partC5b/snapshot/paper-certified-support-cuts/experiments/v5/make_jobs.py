"""Create a campaign-5 output directory: frozen cases, code snapshot copy and job list.

    make_jobs.py partS5   --output DIR
    make_jobs.py partC5a  --output DIR
    make_jobs.py partC5b  --output DIR
    make_jobs.py PART --smoke --output DIR

DIR must not exist. It receives the campaign-2/3/4 layout (``cases/``,
``snapshot/`` with ``frozen-cases/``, ``source-manifest.json``, ``jobs.json``,
``build.json``) so that the archived replay and the driver run unchanged, plus
``c5-inputs/`` with copies and SHA-256 of the files the cases were checked
against. A job is one (model, phase, seed); its modes run back to back in the
order rotated by (model index + seed) mod (number of modes). Larger instances
first, full before root, seed 0, at most six workers (campaign-4 conventions).

Parts (campaign-v5-protocol.md):

- ``partS5``: the 30 star instances of ``stars.py`` (names checked to be new).
  Full (300 s soft / 360 s hard): baseline, baseline-novarlocks, baseline-extra,
  rowdir-star4, agg-star4, agg-star, gurobi; root (node limit 1, 120 s / 180 s):
  the six SCIP modes. Larger = more variables n (2k + 1). 60 jobs, 390 runs.
  Each case's witness gets the archived primal check.
- ``partC5a``: the 20 C3 and the 20 C4 cases of campaign 4 (copied from
  ``../v4/runs/partC3/cases`` and ``../v4/runs/partC4/cases``; each must equal
  its generator, ``mechanism.case`` and ``../v4/mechanism_c4.case`` with
  ``../v4/c4-references.json``, byte for byte as written here). Mode
  baseline-novarlocks, full (300 s / 360 s) and root (120 s / 180 s). Larger n
  first, C3 before C4 within n. 80 jobs, 80 runs.
- ``partC5b``: the 20 C4 cases, root (node limit 1, 300 s / 360 s): frozen-cap32,
  rowdir-cap32, frozen-cap64, rowdir-cap64. 20 jobs, 80 runs.

``--smoke`` keeps a part's modes and rules but uses its smallest instance
(partC5a: the smallest C3 and the smallest C4 instance) and 10 s soft / 30 s
hard limits.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import time

from common import (PAPER, REPO, SNAPSHOT, TOPIC_NAME, V4, digest, load_snapshot_manifest, text,
                    verify_manifest, write_new)
import mechanism
import stars

S5_SCIP_MODES = ("baseline", "baseline-novarlocks", "baseline-extra", "rowdir-star4", "agg-star4", "agg-star")
C5B_MODES = ("frozen-cap32", "rowdir-cap32", "frozen-cap64", "rowdir-cap64")
# (phase, seeds, modes, soft seconds, hard seconds, node limit)
S5_FULL = ("full", (0,), S5_SCIP_MODES + ("gurobi",), 300.0, 360.0, None)
S5_ROOT = ("root", (0,), S5_SCIP_MODES, 120.0, 180.0, 1)
C5A_FULL = ("full", (0,), ("baseline-novarlocks",), 300.0, 360.0, None)
C5A_ROOT = ("root", (0,), ("baseline-novarlocks",), 120.0, 180.0, 1)
C5B_ROOT = ("root", (0,), C5B_MODES, 300.0, 360.0, 1)
SMOKE_LIMITS = (10.0, 30.0)
MAX_WORKERS = 6
C3_SEEDS = (5, 6, 7, 8, 9)
C3_CASES = V4 / "runs/partC3/cases"
C4_CASES = V4 / "runs/partC4/cases"
C4_GENERATOR = V4 / "mechanism_c4.py"
C4_REFERENCES = V4 / "c4-references.json"


def snapshot_module_path():
    path = SNAPSHOT / TOPIC_NAME / "experiments"
    for entry in (path, SNAPSHOT / TOPIC_NAME):
        if str(entry) not in sys.path:
            sys.path.insert(0, str(entry))
    return path


def snapshot_modules():
    snapshot_module_path()
    from run_campaign import exact_json
    from worker import load_model
    from cases import check_primal
    return exact_json, load_model, check_primal


def earlier_case_names():
    """Names of every case file of campaigns 1-4 (and their smoke, scan and repair runs), and MINLPLib."""
    names = set()
    for root in [REPO / name / "experiments" for name in ("research-20261002-convexification",
                                                          "research-20261003-convexification")]:
        names |= {p.stem for p in root.glob("*/cases/*.json")}
    for path in (PAPER / "experiments").glob("v[34]*/**/cases/*.json"):
        names.add(path.stem)
    with (SNAPSHOT / "code/minlp_solver_lab/instances/instancedata.csv").open() as stream:
        names |= {row["name"] for row in csv.DictReader(stream, delimiter=";")}
    return names


def star_cases():
    """The 30 Part 5S instances; witness passes the archived primal check; names are new."""
    exact_json, load_model, check_primal = snapshot_modules()
    sweep = stars.load_sweep()
    cases = []
    for k in stars.KS:
        for n in stars.NS:
            for seed in stars.SEEDS:
                case = json.loads(json.dumps(stars.case(k, n, seed, exact_json, sweep)))
                check = check_primal(load_model(case), case["known_witness"], case["known_optimum"])
                if not check["passed"]:  # stars.instance has checked the witness exactly in rationals
                    raise SystemExit(f"star witness fails the archived primal check: {case['name']}: {check}")
                cases.append(case)
    used = earlier_case_names() & {case["name"] for case in cases}
    if used:
        raise SystemExit(f"Part 5S instance names were used before: {sorted(used)}")
    return cases


def load_c4_generator():
    references = json.loads(C4_REFERENCES.read_text())
    if references["generator_sha256"] != digest(C4_GENERATOR):
        raise SystemExit("c4-references.json was not produced by ../v4/mechanism_c4.py")
    spec = importlib.util.spec_from_file_location("mechanism_c4_readonly", C4_GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, {entry["name"]: entry for entry in references["instances"]}


def checked_copy(case, directory):
    """The campaign-4 case file must be the generated case, byte for byte as written here."""
    path = directory / (case["name"] + ".json")
    if path.read_text() != text(case):
        raise SystemExit(f"campaign-4 case file differs from its generator: {path}")
    return json.loads(path.read_text())


def c3_cases():
    exact_json, _, _ = snapshot_modules()
    return [checked_copy(json.loads(json.dumps(mechanism.case(n, seed, exact_json))), C3_CASES)
            for n in mechanism.NS for seed in C3_SEEDS]


def c4_cases():
    exact_json, load_model, check_primal = snapshot_modules()
    generator, stored = load_c4_generator()
    cases = []
    for n in generator.NS:
        for seed in generator.SEEDS:
            name = generator.case_name(n, seed)
            case = checked_copy(json.loads(json.dumps(generator.case(n, seed, exact_json, stored[name]))), C4_CASES)
            check = check_primal(load_model(case), case["known_witness"], case["known_optimum"])
            if (not check["passed"] or not stored[name]["optimum_certificate"]["certified"]
                    or case["reference_bound_ii"] > case["known_optimum"] + 1e-12):
                raise SystemExit(f"C4 witness, certificate or bound (ii) fails: {name}")
            cases.append(case)
    return cases


def jobs_for(cases, phases, order=None):
    """Declared job order: phases in the given order, seeds ascending, then cases."""
    jobs = []
    order = order or (lambda cs: cs)
    position = {case["name"]: i for i, case in enumerate(cases)}
    for phase, seeds, modes, soft, hard, nodes in phases:
        for seed in seeds:
            for case in order(cases):
                offset = (position[case["name"]] + seed) % len(modes)
                rotated = modes[offset:] + modes[:offset]
                index = len(jobs)
                jobs.append({"job_id": f"{index:03d}", "phase": phase, "name": case["name"],
                             "suite": case["suite"], "seed": seed, "time_limit": soft,
                             "worker_timeout": hard, "node_limit": nodes,
                             "runs": [{"run_id": f"{index:03d}_{case['name']}__{phase}__s{seed}__{mode}",
                                       "mode": mode, "position": k}
                                      for k, mode in enumerate(rotated)]})
    return jobs


def star_size(case):
    return case["star"]["n"] * (2 * case["star"]["k"] + 1)


def star_larger_first(cases):
    return sorted(cases, key=lambda c: (-star_size(c), c["star"]["k"], c["star"]["seed"]))


def path_larger_first(cases):
    """Path family: larger n first; C3 before C4 for equal n; then the instance seed."""
    return sorted(cases, key=lambda c: (-c["mechanism"]["n"], "coupling" in c["mechanism"], c["mechanism"]["seed"]))


def build(part, smoke):
    """(cases, jobs, input files to copy into c5-inputs/)."""
    if part == "partS5":
        cases, phases, order = star_cases(), [S5_FULL, S5_ROOT], star_larger_first
        inputs = [stars.SWEEP]
        smallest = [min(cases, key=lambda c: (star_size(c), c["star"]["seed"]))]
    elif part in ("partC5a", "partC5b"):
        c4 = c4_cases()
        cases = c3_cases() + c4 if part == "partC5a" else c4
        phases = [C5A_FULL, C5A_ROOT] if part == "partC5a" else [C5B_ROOT]
        order, inputs = path_larger_first, [C4_GENERATOR, C4_REFERENCES]
        key = lambda c: (c["mechanism"]["n"], c["mechanism"]["seed"])
        smallest = ([min(cases[:20], key=key), min(c4, key=key)] if part == "partC5a" else [min(c4, key=key)])
    else:
        raise SystemExit(f"unknown part {part}")
    if smoke:
        cases = smallest
        phases = [(phase, seeds, modes) + SMOKE_LIMITS + (nodes,) for phase, seeds, modes, soft, hard, nodes in phases]
    return cases, jobs_for(cases, phases, order), inputs


def main(args):
    code = load_snapshot_manifest()
    cases, jobs, inputs = build(args.part, args.smoke)
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    (out / "cases").mkdir()
    snapshot = out / "snapshot"
    hashes = {}
    for relative in code:
        target = snapshot / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SNAPSHOT / relative, target)
        hashes[relative] = digest(target)
    (snapshot / "frozen-cases").mkdir()
    for case in cases:
        write_new(out / "cases" / (case["name"] + ".json"), case)
        relative = f"frozen-cases/{case['name']}.json"
        shutil.copyfile(out / "cases" / (case["name"] + ".json"), snapshot / relative)
        hashes[relative] = digest(snapshot / relative)
    if verify_manifest(snapshot, hashes) or any(hashes[k] != v for k, v in code.items()):
        raise SystemExit("output snapshot does not match the code snapshot")
    (out / "c5-inputs").mkdir()
    input_hashes = {}
    for path in inputs:
        shutil.copyfile(path, out / "c5-inputs" / path.name)
        input_hashes[str(path.relative_to(PAPER))] = digest(out / "c5-inputs" / path.name)
        if input_hashes[str(path.relative_to(PAPER))] != digest(path):
            raise SystemExit(f"copy of {path} differs")
    part = args.part + ("-smoke" if args.smoke else "")
    write_new(out / "source-manifest.json", hashes)
    write_new(out / "jobs.json", {"schema": "campaign-v5-jobs-1", "part": part,
                                  "max_workers": MAX_WORKERS, "jobs": jobs})
    write_new(out / "build.json", {
        "part": part, "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "code_manifest_sha256": digest(SNAPSHOT / "source-manifest.json"),
        "inputs_sha256": input_hashes, "make_jobs_sha256": digest(Path(__file__).resolve()),
        "cases": len(cases), "jobs": len(jobs), "runs": sum(len(j["runs"]) for j in jobs),
        "max_workers": MAX_WORKERS})
    print(json.dumps({"output": str(out), "part": part, "cases": len(cases), "jobs": len(jobs),
                      "runs": sum(len(j["runs"]) for j in jobs), "max_workers": MAX_WORKERS}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("part", choices=("partS5", "partC5a", "partC5b"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smoke", action="store_true")
    main(parser.parse_args())
