"""Create the campaign-4 Part C4 output directory (campaign-v4-protocol.md, Amendment 1).

    make_jobs_c4.py --output DIR [--smoke]

Runs ``make_jobs.main`` unchanged with a C4 ``build`` (make_jobs.py itself is not edited), so DIR
gets the campaign-2/3 layout (``cases/``, snapshot copy with ``frozen-cases/``,
``source-manifest.json``, ``jobs.json``, ``build.json``) and the archived replay and the
driver run unchanged. The C4 cases come from ``mechanism_c4.case`` and the stored references
(``c4-references.json``, whose recorded generator hash must equal ``mechanism_c4.py``). Each C4
case is checked against the C3 case of ``runs/partC3/cases``: same model except for the name and
the coupling-row bound, same triples. Its witness gets the archived primal check exactly as the
worker runs it. ``mechanism_c4.py``, this file and ``c4-references.json`` are copied to
``DIR/c4-inputs/`` with their SHA-256 in ``DIR/c4-inputs/inputs.json``.

Phases: full (300 s soft / 360 s hard): baseline, frozen-wide, rowdir-wide, baseline-extra,
gurobi; root (node limit 1, 120 s / 180 s): the four SCIP modes. Seed 0, larger n first, full
before root, modes of a job rotated by (model index + seed) mod (number of modes), as in
make_jobs. 40 jobs, 180 runs. ``--smoke``: interleaved_path_coupled_n10_s5 at 10 s / 30 s.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil

from common import HERE, V3, digest, write_new
import make_jobs
import mechanism
import mechanism_c4

C4_MODES = ("baseline", "frozen-wide", "rowdir-wide", "baseline-extra")
# (phase, seeds, modes, soft seconds, hard seconds, node limit)
C4_FULL = ("full", (0,), C4_MODES + ("gurobi",), 300.0, 360.0, None)
C4_ROOT = ("root", (0,), C4_MODES, 120.0, 180.0, 1)
REFERENCES = HERE / "c4-references.json"
C3_CASES = HERE / "runs/partC3/cases"


def same_except_coupling(c4, c3, n):
    """The C4 model is the C3 model with the new name and coupling-row bound only."""
    a, b = json.loads(json.dumps(c4["model"])), json.loads(json.dumps(c3["model"]))
    if a["name"] != c4["name"] or b["name"] != c3["name"]:
        return False
    last_a, last_b = a["rows"].pop(), b["rows"].pop()
    old_ub = {"binary64": float(4 * n / 5).hex()}
    new_ub = {"binary64": float(c4["mechanism"]["coupling"]["c_binary64"]).hex()}
    if last_b["ub"] != old_ub or last_a["ub"] != new_ub:
        return False
    last_a.pop("ub"), last_b.pop("ub"), a.pop("name"), b.pop("name")
    return a == b and last_a == last_b and c4["mechanism"]["triples"] == c3["mechanism"]["triples"]


def c4_cases():
    references = json.loads(REFERENCES.read_text())
    if references["generator_sha256"] != digest(HERE / "mechanism_c4.py"):
        raise SystemExit("c4-references.json was not produced by the current mechanism_c4.py")
    stored = {entry["name"]: entry for entry in references["instances"]}
    make_jobs.snapshot_module_path()
    from run_campaign import exact_json
    from worker import load_model
    from cases import check_primal
    cases = []
    for n in mechanism_c4.NS:
        for seed in mechanism_c4.SEEDS:
            name = mechanism_c4.case_name(n, seed)
            case = json.loads(json.dumps(mechanism_c4.case(n, seed, exact_json, stored[name])))
            c3_path = C3_CASES / (mechanism.case_name(n, seed) + ".json")
            c3 = json.loads(c3_path.read_text())
            if c3 != json.loads(json.dumps(mechanism.case(n, seed, exact_json))):
                raise SystemExit(f"C3 case differs from its generator: {c3_path}")
            if not same_except_coupling(case, c3, n):
                raise SystemExit(f"C4 case differs from the C3 case beyond the coupling row: {name}")
            check = check_primal(load_model(case), case["known_witness"], case["known_optimum"])
            if not check["passed"] or not stored[name]["optimum_certificate"]["certified"]:
                raise SystemExit(f"C4 reference witness or certificate fails: {name}: {check}")
            if case["reference_bound_ii"] > case["known_optimum"] + 1e-12:
                raise SystemExit(f"bound (ii) exceeds the optimum: {name}")
            cases.append(case)
    used = ({p.stem for p in (V3 / "runs/partC/cases").glob("*.json")} | {p.stem for p in C3_CASES.glob("*.json")})
    if used & {case["name"] for case in cases}:
        raise SystemExit("a C4 instance name was used before")
    return cases


def build(part, selection, smoke):
    if part != "partC4" or selection is not None:
        raise SystemExit("make_jobs_c4 builds partC4 only, without --selection")
    cases, phases = c4_cases(), [C4_FULL, C4_ROOT]
    if smoke:
        cases = [min(cases, key=lambda c: (c["mechanism"]["n"], c["mechanism"]["seed"]))]
        phases = [(phase, seeds, modes) + make_jobs.SMOKE_LIMITS + (nodes,)
                  for phase, seeds, modes, soft, hard, nodes in phases]
    return cases, make_jobs.jobs_for(cases, phases, make_jobs.larger_first), make_jobs.MAX_WORKERS


def main(args):
    make_jobs.build = build  # make_jobs.main looks build up at call time
    make_jobs.main(argparse.Namespace(part="partC4", selection=None, smoke=args.smoke, output=args.output))
    inputs = args.output.resolve() / "c4-inputs"
    inputs.mkdir()
    hashes = {}
    for path in (HERE / "mechanism_c4.py", Path(__file__).resolve(), REFERENCES):
        shutil.copyfile(path, inputs / path.name)
        hashes[path.name] = digest(inputs / path.name)
        if hashes[path.name] != digest(path):
            raise SystemExit(f"copy of {path.name} differs")
    write_new(inputs / "inputs.json", {"sha256": hashes, "make_jobs_sha256": digest(HERE / "make_jobs.py")})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smoke", action="store_true")
    main(parser.parse_args())
