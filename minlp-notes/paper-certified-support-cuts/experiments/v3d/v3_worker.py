"""Run one v3 case in one mode; adapted from the archived campaign-v2 worker.

Differences from ``research-20261003-convexification/experiments/worker.py``:
the mode names ``all-diag`` and ``all-diag-mech`` run the ``all`` separator
with the raised work limits of campaign-v3-protocol.md and mechanism-protocol.md;
the effective ``Config``, its overrides and the solver mode are recorded; the
archived OSiL copy is required; and the run fails unless every solver,
checker and case module was imported from the snapshot. Model loading, the
primal check and exact serialization are the archived functions, imported
from the snapshot.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import math
from pathlib import Path
import sys
import time
import traceback

ALL_DIAG = {"max_blocks": 128, "max_cuts": 200, "max_cuts_per_round": 50, "max_rounds": 10,
            "max_support_calls": 500, "max_separation_seconds": 30.0,
            "separation_budget_fraction": 0.5}
MODES = ("baseline", "all", "auto", "all-diag", "all-diag-mech", "all-diag-mech-wide")
FROZEN_PACKAGES = {"solver", "theory", "reviews", "uenv", "cases", "worker", "run_campaign"}


def mode_config(mode, case):
    """Return (run_instance mode, Config overrides) for a v3 mode name."""
    if mode in ("baseline", "all", "auto"):
        return mode, {}
    if mode == "all-diag":
        return "all", dict(ALL_DIAG)
    if mode == "all-diag-mech":
        n = case["mechanism"]["n"]
        return "all", {"max_blocks": n, "max_cuts": 4 * n, "max_cuts_per_round": n,
                       "max_rounds": 10, "max_support_calls": 20 * n,
                       "max_separation_seconds": 60.0, "separation_budget_fraction": 0.5}
    if mode == "all-diag-mech-wide":
        n = case["mechanism"]["n"]
        return "all", {"max_blocks": n, "max_cuts": 16 * n, "max_cuts_per_round": 4 * n,
                       "max_rounds": 10, "max_support_calls": 40 * n,
                       "max_separation_seconds": 60.0, "separation_budget_fraction": 0.5}
    raise ValueError(f"unknown v3 mode {mode!r}")


def main(args):
    start = time.perf_counter()
    source = args.source.resolve()
    sys.path.insert(0, str(source))
    sys.path.insert(0, str(source / "experiments"))
    from worker import load_model
    from cases import check_primal
    from run_campaign import exact_json
    from solver.integration import Config, run_instance
    preparation_start = time.perf_counter()
    case = json.loads(args.case.read_text())
    if "path" in case:
        archived = source.parent / "original-osil" / (case["name"] + ".osil")
        if not archived.is_file():
            raise FileNotFoundError(f"archived OSiL copy missing: {archived}")
        case = {**case, "path": str(archived)}
    solver_mode, overrides = mode_config(args.mode, case)
    config = Config(**overrides)
    load_start = time.perf_counter()
    model = load_model(case)
    source_read_seconds = time.perf_counter() - load_start
    encoded = exact_json(asdict(model))
    model_hash = hashlib.sha256(json.dumps(encoded, sort_keys=True).encode()).hexdigest()
    preparation_seconds = time.perf_counter() - preparation_start
    import_seconds = time.perf_counter() - start
    result = run_instance(model, solver_mode, time_limit=max(1e-6, args.time_limit - preparation_seconds),
                          seed=args.seed, node_limit=args.node_limit, config=config)
    if result.get("config") != asdict(config):
        raise RuntimeError("run_instance did not record the effective Config")
    result.update(mode=args.mode, solver_mode=solver_mode, config_overrides=overrides)
    result.setdefault("cut_log_complete", isinstance(result.get("cuts"), list))
    check_start = time.perf_counter()
    check = check_primal(model, result.get("original_values"), result.get("primal"))
    result.update(original_model=encoded, model_sha256=model_hash,
                  primal_check=check, primal_check_seconds=time.perf_counter() - check_start,
                  source_read_seconds=source_read_seconds,
                  preparation_seconds=preparation_seconds,
                  worker_import_and_load_seconds=import_seconds,
                  worker_total_seconds=time.perf_counter() - start)
    result["reference_check"] = {"checked": False, "reason": "no finite archived reference",
                                 "certifies_dual": False}
    reference = case.get("known_optimum", case.get("reference_primal"))
    if reference is not None:
        try:
            reference = float(reference)
            if not math.isfinite(reference):
                raise ValueError("nonfinite archived reference")
            tolerance = 1e-5 * max(1.0, abs(reference))
            dual, root_dual = result.get("dual"), result.get("root_dual")
            minimize = model.obj_sense == "min"
            result["reference_check"] = {
                "checked": True, "value": reference,
                "kind": "analytic optimum" if "known_optimum" in case else "archived feasible bound",
                "tolerance": tolerance,
                "dual_consistent": dual is None or (dual <= reference + tolerance if minimize
                                                     else dual >= reference - tolerance),
                "root_dual_consistent": root_dual is None or (
                    root_dual <= reference + tolerance if minimize else root_dual >= reference - tolerance),
                "certifies_dual": False}
        except (TypeError, ValueError):
            pass
    if case.get("known_witness") is not None:
        result["reference_witness_check"] = check_primal(model, case["known_witness"], case.get("known_optimum"))
    frozen = [m for name, m in list(sys.modules.items()) if name.split(".")[0] in FROZEN_PACKAGES]
    outside = [m.__file__ for m in frozen if getattr(m, "__file__", None)
               and not Path(m.__file__).resolve().is_relative_to(source.parent)]
    if outside:
        raise RuntimeError(f"modules imported from outside the snapshot: {outside}")
    result["snapshot_modules_verified"] = len(frozen)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True,
                        help="snapshot copy of research-20261003-convexification")
    parser.add_argument("--mode", required=True, choices=MODES)
    parser.add_argument("--time-limit", type=float, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--node-limit", type=int)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = main(args)
    except Exception as error:
        traceback.print_exc()
        result = {"status": "worker_error", "exception": type(error).__name__, "reason": str(error),
                  "cut_log_complete": False, "cut_count": None}
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    temporary.replace(args.output)
