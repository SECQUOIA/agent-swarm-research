"""Create a v3 output directory: frozen cases, code snapshot copy and job list.

    make_jobs.py partA-full --output DIR
    make_jobs.py partA-root --output DIR
    make_jobs.py partC      --output DIR
    make_jobs.py partB      --output DIR --selection scan/partB-selection.json
    make_jobs.py smoke      --output DIR

DIR must not exist. It receives the layout of campaign v2 (``cases/``,
``snapshot/`` with ``frozen-cases/`` and ``original-osil/``,
``source-manifest.json``) so that the archived replay runs unchanged, plus
``jobs.json``. A job is one (model, phase, seed); its modes run in the
rotated order (model index + seed) mod (number of modes).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

from common import (OSIL_CACHE, SNAPSHOT, TOPIC_NAME, digest, load_snapshot_manifest,
                    verify_manifest, write_new)
import mechanism

FULL_MODES = ("baseline", "all", "auto")
ROOT_MODES = ("baseline", "all", "auto", "all-diag")
MECH_MODES = ("baseline", "all-diag-mech", "all-diag-mech-wide")
# (phase, seeds, modes, soft seconds, hard seconds, node limit)
A_FULL = ("full", (0, 1, 2), FULL_MODES, 300.0, 360.0, None)
AB_ROOT = ("root", (0,), ROOT_MODES, 60.0, 90.0, 1)
B_FULL = ("full", (0, 1), FULL_MODES, 300.0, 360.0, None)
C_ROOT = ("root", (0,), MECH_MODES, 120.0, 180.0, 1)
C_FULL = ("full", (0,), MECH_MODES, 300.0, 360.0, None)
SMOKE_MODELS = ("cvxnonsep_normcon20r", "ex4_1_8")
SMOKE_FULL = ("full", (0, 1), FULL_MODES, 5.0, 20.0, None)
SMOKE_ROOT = ("root", (0,), ROOT_MODES, 5.0, 20.0, 1)
SMOKE_MECH = ((10, 0), (10, 1))
STRUCTURE_PREFIX = "convexification-structure-v3:"
PART_B_SIZE = 30


def snapshot_module_path():
    path = SNAPSHOT / TOPIC_NAME / "experiments"
    sys.path.insert(0, str(path))
    return path


def holdout():
    return json.loads((SNAPSHOT / TOPIC_NAME / "experiments/holdout-selection.json").read_text())


def metadata():
    with (SNAPSHOT / "code/minlp_solver_lab/instances/instancedata.csv").open() as stream:
        return {row["name"]: row for row in csv.DictReader(stream, delimiter=";")}


def osil_case(name, suite, source, sha256, reference_primal, reference_dual, stratum):
    source = Path(source)
    if digest(source) != sha256:
        raise SystemExit(f"OSiL file changed after selection: {source}")
    return {"name": name, "suite": suite, "stratum": stratum, "path": str(source),
            "source_sha256": sha256, "reference_primal": reference_primal,
            "reference_dual": reference_dual}


def holdout_cases(names=None):
    selected = holdout()["selected"]
    return [osil_case(r["name"], "holdout", OSIL_CACHE / f"{r['name']}.osil", r["sha256"],
                      r.get("reference_primal"), r.get("reference_dual"), r["stratum"])
            for r in selected if names is None or r["name"] in names]


def structure_cases(selection_path):
    selection = json.loads(Path(selection_path).read_text())
    frozen = holdout()
    excluded = {r["name"] for r in frozen["selected"]}
    pool = [n for n in frozen["eligible_names_in_rank_order"] if n not in excluded]
    entries = selection["selected"]
    names = [e["name"] for e in entries]
    rank = lambda n: hashlib.sha256((STRUCTURE_PREFIX + n).encode()).hexdigest()
    if len(set(names)) != len(names) or not set(names) <= set(pool):
        raise SystemExit("Part B selection contains duplicates or names outside the Part S pool")
    if names != sorted(names, key=rank) or len(names) > PART_B_SIZE:
        raise SystemExit("Part B selection is not in structure-hash rank order or exceeds 30 models")
    qualifying = selection.get("qualifying_names_in_rank_order")
    if qualifying is not None and names != qualifying[:PART_B_SIZE]:
        raise SystemExit("Part B selection differs from the first 30 qualifying models")
    reference = metadata()
    return [osil_case(e["name"], "structure", e["path"], e["osil_sha256"],
                      reference.get(e["name"], {}).get("primalbound"),
                      reference.get(e["name"], {}).get("dualbound"), e.get("stratum"))
            for e in entries]


def mechanism_cases(pairs):
    snapshot_module_path()
    from run_campaign import exact_json
    return [mechanism.case(n, seed, exact_json) for n, seed in pairs]


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


def build(part, selection):
    if part == "partA-full":
        cases = holdout_cases()
        return cases, jobs_for(cases, [A_FULL]), 6
    if part == "partA-root":
        cases = holdout_cases()
        return cases, jobs_for(cases, [AB_ROOT]), 6
    if part == "partB":
        if selection is None:
            raise SystemExit("partB requires --selection")
        cases = structure_cases(selection)
        return cases, jobs_for(cases, [B_FULL, AB_ROOT]), 6
    if part == "partC":
        cases = mechanism_cases([(n, s) for n in mechanism.NS for s in mechanism.SEEDS])
        # Larger instances first within each phase, to shorten the parallel makespan.
        larger_first = lambda cs: sorted(cs, key=lambda c: (-c["mechanism"]["n"], c["mechanism"]["seed"]))
        return cases, jobs_for(cases, [C_FULL, C_ROOT], larger_first), 4
    if part == "smoke":
        models = holdout_cases(SMOKE_MODELS)
        mech = mechanism_cases(SMOKE_MECH)
        jobs = jobs_for(models, [SMOKE_FULL, SMOKE_ROOT]) + jobs_for(mech, [C_ROOT, C_FULL])
        for index, job in enumerate(jobs):
            job["job_id"] = f"{index:03d}"
            for run in job["runs"]:
                run["run_id"] = f"{index:03d}" + run["run_id"][3:]
        return models + mech, jobs, 4
    raise SystemExit(f"unknown part {part}")


def main(args):
    code = load_snapshot_manifest()
    cases, jobs, max_workers = build(args.part, args.selection)
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
    for case in cases:
        write_new(out / "cases" / (case["name"] + ".json"), case)
        relative = f"frozen-cases/{case['name']}.json"
        (snapshot / "frozen-cases").mkdir(exist_ok=True)
        shutil.copyfile(out / "cases" / (case["name"] + ".json"), snapshot / relative)
        hashes[relative] = digest(snapshot / relative)
        if "path" in case:
            relative = f"original-osil/{case['name']}.osil"
            (snapshot / "original-osil").mkdir(exist_ok=True)
            shutil.copyfile(case["path"], snapshot / relative)
            hashes[relative] = digest(snapshot / relative)
            if hashes[relative] != case["source_sha256"]:
                raise SystemExit(f"OSiL copy differs from the pinned hash: {case['name']}")
    if verify_manifest(snapshot, hashes) or any(hashes[k] != v for k, v in code.items()):
        raise SystemExit("output snapshot does not match the code snapshot")
    write_new(out / "source-manifest.json", hashes)
    write_new(out / "jobs.json", {"schema": "campaign-v3-jobs-1", "part": args.part,
                                  "max_workers": max_workers, "jobs": jobs})
    write_new(out / "build.json", {
        "part": args.part, "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "code_manifest_sha256": digest(SNAPSHOT / "source-manifest.json"),
        "selection": str(Path(args.selection).resolve()) if args.selection else None,
        "selection_sha256": digest(args.selection) if args.selection else None,
        "cases": len(cases), "jobs": len(jobs), "runs": sum(len(j["runs"]) for j in jobs),
        "max_workers": max_workers})
    print(json.dumps({"output": str(out), "cases": len(cases), "jobs": len(jobs),
                      "runs": sum(len(j["runs"]) for j in jobs), "max_workers": max_workers}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("part", choices=("partA-full", "partA-root", "partB", "partC", "smoke"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--selection", type=Path)
    main(parser.parse_args())
