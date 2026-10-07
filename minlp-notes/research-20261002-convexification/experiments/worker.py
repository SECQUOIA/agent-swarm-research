"""Run a single frozen case and independently evaluate its original incumbent."""
from __future__ import annotations

import argparse
from dataclasses import asdict, fields
import hashlib
import json
from pathlib import Path
import sys
import time
import traceback


def decode(value):
    if isinstance(value, dict):
        if set(value) == {"binary64"}:
            return float.fromhex(value["binary64"])
        return {k: decode(v) for k, v in value.items()}
    if isinstance(value, list):
        return [decode(v) for v in value]
    return value


def tuples(tree):
    return tuple(tuples(v) if isinstance(v, list) else v for v in tree)


def load_model(case):
    from cases import Instance
    from uenv.osil import read_osil
    if "path" in case:
        path = Path(case["path"])
        if hashlib.sha256(path.read_bytes()).hexdigest() != case["source_sha256"]:
            raise ValueError("cached OSiL source changed after protocol freeze")
        return read_osil(str(path))
    data = decode(case["model"])
    for row in data["rows"]:
        row["lin"] = {int(k): v for k, v in row["lin"].items()}
        row["quad"] = [tuple(q) for q in row["quad"]]
        if row["nl"] is not None:
            row["nl"] = tuples(row["nl"])
    return Instance(**data)


def main(args):
    start = time.perf_counter()
    sys.path.insert(0, str(args.source))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from cases import check_primal
    from run_campaign import exact_json
    from solver.integration import Config, run_instance
    case = json.loads(args.case.read_text())
    if "path" in case:
        archived = args.source.parent / "original-osil" / (case["name"] + ".osil")
        if archived.exists():
            case = {**case, "path": str(archived)}
    load_start = time.perf_counter()
    model = load_model(case)
    source_read_seconds = time.perf_counter() - load_start
    encoded = exact_json(asdict(model))
    model_hash = hashlib.sha256(json.dumps(encoded, sort_keys=True).encode()).hexdigest()
    options = {}
    if args.no_cache:
        available = {f.name for f in fields(Config)}
        option = next((name for name in ("cache", "use_cache", "cache_samples") if name in available), None)
        if option is None:
            return {"status": "ablation_unavailable", "reason": "integration has no caching toggle",
                    "model_sha256": model_hash}
        options[option] = False
    if args.no_merge_stars:
        options["merge_stars"] = False
    import_seconds = time.perf_counter() - start
    result = run_instance(model, args.mode, time_limit=max(1e-6, args.time_limit - source_read_seconds), seed=args.seed,
                          node_limit=args.node_limit, config=Config(**options))
    check_start = time.perf_counter()
    check = check_primal(model, result.get("original_values"), result.get("primal"))
    result.update(original_model=encoded, model_sha256=model_hash,
                  primal_check=check, primal_check_seconds=time.perf_counter() - check_start,
                  source_read_seconds=source_read_seconds,
                  worker_import_and_load_seconds=import_seconds,
                  worker_total_seconds=time.perf_counter() - start)
    reference = case.get("known_optimum", case.get("reference_primal"))
    if reference is not None:
        try:
            reference = float(reference)
            tolerance = 1e-5 * max(1.0, abs(reference))
            dual = result.get("dual")
            root_dual = result.get("root_dual")
            result["reference_check"] = {
                "value": reference, "kind": "analytic optimum" if "known_optimum" in case else "archived feasible bound",
                "tolerance": tolerance,
                "dual_consistent": dual is None or (dual <= reference + tolerance if model.obj_sense == "min"
                                                     else dual >= reference - tolerance),
                "root_dual_consistent": root_dual is None or (
                    root_dual <= reference + tolerance if model.obj_sense == "min"
                    else root_dual >= reference - tolerance),
                "certifies_dual": False}
        except (TypeError, ValueError):
            pass
    if case.get("known_witness") is not None:
        result["reference_witness_check"] = check_primal(model, case["known_witness"], case.get("known_optimum"))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--mode", required=True)
    parser.add_argument("--time-limit", type=float, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--node-limit", type=int)
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--no-merge-stars", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = main(args)
    except Exception as error:
        traceback.print_exc()
        result = {"status": "worker_error", "exception": type(error).__name__, "reason": str(error)}
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    temporary.replace(args.output)
