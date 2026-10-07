"""Replay saved cut evidence against the frozen original models in a campaign.

Run this in a fresh process.  It does not import the solver integration or trust
its symbolic features, rewritten rows, domain restrictions, or auxiliary map.
The support checker itself is imported from the verified campaign snapshot.
The result certifies added rows, never SCIP's numerical primal or dual bounds.
"""
from __future__ import annotations

import argparse
import copy
from dataclasses import asdict
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import sympy as sp


TOPIC_NAME = "research-20261002-convexification"


def decode(value):
    if isinstance(value, dict):
        if set(value) == {"binary64"}:
            return float.fromhex(value["binary64"])
        return {key: decode(item) for key, item in value.items()}
    if isinstance(value, list):
        return [decode(item) for item in value]
    return value


def encode(value):
    if isinstance(value, float):
        return {"binary64": value.hex()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    if isinstance(value, dict):
        return {str(key): encode(item) for key, item in value.items()}
    return value


def model_digest(encoded):
    return hashlib.sha256(json.dumps(encoded, sort_keys=True).encode()).hexdigest()


def tree_tuple(tree):
    if not isinstance(tree, (list, tuple)) or not tree:
        raise ValueError("invalid source expression tree")
    return tuple(tree_tuple(item) if isinstance(item, (list, tuple)) else item for item in tree)


def source_variables(tree):
    if tree[0] == "var":
        if type(tree[1]) is not int or len(tree) != 2:
            raise ValueError("invalid source variable")
        return {tree[1]}
    if tree[0] == "num":
        if len(tree) != 2 or not math.isfinite(tree[1]):
            raise ValueError("invalid source scalar")
        return set()
    return set().union(*(source_variables(child) for child in tree[1:]))


def source_expression(tree, symbols):
    """Independently interpret the original source tree, never feature strings."""
    tag = tree[0]
    if tag == "num":
        return sp.Rational(float(tree[1]))
    if tag == "var":
        return symbols[tree[1]]
    arguments = [source_expression(child, symbols) for child in tree[1:]]
    if tag == "sum":
        return sp.Add(*arguments)
    if tag == "times":
        return sp.Mul(*arguments)
    if tag == "negate":
        return -arguments[0]
    if tag == "divide":
        return arguments[0] / arguments[1]
    if tag == "square":
        return arguments[0] ** 2
    if tag == "power":
        return arguments[0] ** arguments[1]
    return {"log": sp.log, "exp": sp.exp, "sqrt": sp.sqrt,
            "sin": sp.sin, "cos": sp.cos, "abs": sp.Abs}[tag](arguments[0])


def expand_auxiliaries(tree, atoms):
    if tree[0] == "uni":
        if len(tree) != 2 or type(tree[1]) is not int or not 0 <= tree[1] < len(atoms):
            raise ValueError("invalid rewritten auxiliary reference")
        return atoms[tree[1]]
    if tree[0] in ("num", "var"):
        return tree
    return (tree[0], *(expand_auxiliaries(child, atoms) for child in tree[1:]))


def model_binding(record, expected_model):
    """Check exact source replacement rather than rerunning block discovery."""
    if record.get("original_model") != expected_model:
        raise ValueError("run model differs from pinned original model")
    if record.get("model_sha256") != model_digest(expected_model):
        raise ValueError("original model fingerprint mismatch")
    model = decode(expected_model)
    if record.get("status") == "source_model_mismatch":
        if (record.get("cuts") or record.get("detected_atoms") or record.get("nodes") != 0
                or any(record.get(key) is not None for key in
                       ("primal", "dual", "root_dual", "original_values"))):
            raise ValueError("refused source model unexpectedly reports solver evidence")
        return model, []
    nvars = len(model["var_lb"])
    atoms = []
    available = set()

    def collect(tree):
        available.add(tree)
        if tree[0] not in ("num", "var"):
            for child in tree[1:]:
                collect(child)

    for row in model["rows"]:
        if row["nl"] is not None:
            collect(tree_tuple(row["nl"]))
        for i, j, coefficient in row["quad"]:
            if coefficient:
                available.add(("times", ("var", i), ("var", j)))

    for i, atom in enumerate(record.get("detected_atoms", [])):
        tree = tree_tuple(atom["tree"])
        if atom.get("index") != i or tree not in available or tree in atoms:
            raise ValueError("auxiliary is not a unique indexed original source subtree")
        variables = sorted(source_variables(tree))
        if atom.get("variables") != variables or any(not 0 <= j < nvars for j in variables):
            raise ValueError("auxiliary source variable binding mismatch")
        atoms.append(tree)
    model["_admitted_atoms"] = {
        i for i, atom in enumerate(record.get("detected_atoms", [])) if atom.get("admitted") is True
    }

    if record["mode"] == "baseline":
        if atoms or record.get("cuts") or record.get("rewritten_rows") is not None:
            raise ValueError("baseline unexpectedly carries a reformulation or added cuts")
        return model, atoms
    rewritten = record.get("rewritten_rows")
    if not isinstance(rewritten, list) or len(rewritten) != len(model["rows"]):
        raise ValueError("missing original-to-reformulated row binding")
    for source, rewritten_tree in zip(model["rows"], rewritten):
        if source["nl"] is None:
            if rewritten_tree is not None:
                raise ValueError("rewriting introduced a nonlinear expression")
        elif expand_auxiliaries(tree_tuple(rewritten_tree), atoms) != tree_tuple(source["nl"]):
            raise ValueError("rewriting changed an original expression or its domain")
    seen_quadratic = set()
    for ri, qi, ai in record.get("quadratic_atoms", []):
        if any(type(index) is not int for index in (ri, qi, ai)):
            raise ValueError("noninteger quadratic binding index")
        if not (0 <= ri < len(model["rows"]) and 0 <= qi < len(model["rows"][ri]["quad"])
                and 0 <= ai < len(atoms)) or (ri, qi) in seen_quadratic:
            raise ValueError("invalid or duplicate quadratic binding")
        i, j, coefficient = model["rows"][ri]["quad"][qi]
        if not coefficient or atoms[ai] != ("times", ("var", i), ("var", j)):
            raise ValueError("quadratic auxiliary does not define its original product")
        seen_quadratic.add((ri, qi))
    if record["mode"] == "control" and record.get("cuts"):
        raise ValueError("reformulation control unexpectedly contains added cuts")
    return model, atoms


def expected_rows(model, variables):
    rows = []
    for row in model["rows"][1:]:
        if row["nl"] is not None or row["quad"]:
            continue
        linear = {int(i): coefficient for i, coefficient in row["lin"].items()}
        support = {i for i, coefficient in linear.items() if coefficient}
        if not 1 <= len(support) <= 2 or not support.issubset(variables):
            continue
        coefficients = [float(linear.get(i, 0)) for i in variables]
        if math.isfinite(row["ub"]):
            rows.append([coefficients, float(row["ub"])])
        if math.isfinite(row["lb"]):
            rows.append([[-coefficient for coefficient in coefficients], float(-row["lb"])])
    return rows


def check_cut(cut, model, atoms, replay_support):
    try:
        variables, ids = cut["variables"], cut["atoms"]
        if (not variables or any(type(i) is not int for i in variables + ids)
                or variables != sorted(set(variables)) or len(ids) != len(set(ids))
                or any(not 0 <= i < len(model["var_lb"]) for i in variables)
                or any(not 0 <= i < len(atoms) for i in ids)):
            return False, "invalid block variable or auxiliary indices"
        if any(not source_variables(atoms[i]).issubset(variables) for i in ids):
            return False, "block omits a source variable"
        if any(i not in model["_admitted_atoms"] for i in ids):
            return False, "cut uses an auxiliary that failed native/source semantic admission"
        if [tree_tuple(tree) for tree in cut["atom_trees"]] != [atoms[i] for i in ids]:
            return False, "cut atom source trees were changed"
        expected_columns = [f"v{i}" for i in variables] + [f"block_aux_{i}" for i in ids]
        if cut["column_names"] != expected_columns:
            return False, "cut columns do not match original variables and auxiliary definitions"
        box = [[model["var_lb"][i], model["var_ub"][i]] for i in variables]
        if cut["box"] != box or not all(math.isfinite(v) for pair in box for v in pair):
            return False, "cut uses a changed or nonfinite original box"
        rows = expected_rows(model, variables)
        if cut["rows"] != rows:
            return False, "cut uses changed or unjustified original affine rows"
        symbols = tuple(sp.Symbol(f"x{i}", real=True) for i in range(len(model["var_lb"])))
        block_symbols = tuple(symbols[i] for i in variables)
        features = block_symbols + tuple(source_expression(atoms[i], symbols) for i in ids)
        if cut["features"] != [str(feature) for feature in features]:
            return False, "cut features differ from the original source expressions"
        if cut["symbols"] != [str(symbol) for symbol in block_symbols]:
            return False, "cut symbolic coordinates were permuted or changed"
        coefficients = cut["coefficients"]
        if len(coefficients) != len(features) or not all(math.isfinite(c) for c in coefficients):
            return False, "invalid solver coefficient vector"
        witness = cut["certificate"]
        if witness.get("status") != "complete" or float(cut["rhs"]).hex() != witness.get("rhs"):
            return False, "exported row right-hand side does not match its certificate"
        if cut.get("local") is not False:
            return False, "unexpected local cut scope"
        actual = cut["actual_row"]
        if actual["local"] is not False or actual.get("fixed_substitutions"):
            return False, "actual row is local or trusts an unproved fixing"
        source_coefficients = {name: Fraction(float(coefficient))
                               for name, coefficient in zip(expected_columns, coefficients) if coefficient}
        mapping = actual["source_to_transformed"]
        if (len(mapping) != len(source_coefficients)
                or {entry["source"] for entry in mapping} != set(source_coefficients)
                or len({entry["transformed"] for entry in mapping}) != len(mapping)):
            return False, "actual row drops or aggregates original nonzero columns"
        actual_coefficients = {entry["transformed"]: source_coefficients[entry["source"]] for entry in mapping}
        if ({name: Fraction(float(value)) for name, value in actual["columns"].items()}
                != actual_coefficients):
            return False, "actual inserted float coefficients differ from the certified row"
        if (Fraction(float(actual["lhs"])) - Fraction(float(actual["constant"]))
                != Fraction(float(cut["rhs"]))):
            return False, "actual inserted float bound differs from the certified row"
        if (not math.isfinite(actual["scip_infinity"]) or actual["scip_infinity"] <= 0
                or actual["rhs"] < actual["scip_infinity"]):
            return False, "actual inserted row has an unexpected finite upper bound"
        if not replay_support(features, block_symbols, box, coefficients, rows, witness):
            return False, "support evidence did not replay against the original model"
        return True, "replayed original-model cut"
    except (KeyError, TypeError, ValueError, IndexError, AttributeError, OverflowError):
        return False, "malformed or unsupported cut binding"


def check_run(record, expected_model, replay_support):
    started = time.perf_counter()
    try:
        model, atoms = model_binding(record, expected_model)
        checks = [check_cut(cut, model, atoms, replay_support) for cut in record.get("cuts", [])]
        failures = [{"cut": i, "reason": reason} for i, (passed, reason) in enumerate(checks) if not passed]
        return {"run_id": record.get("run_id"), "model_bound": True,
                "source_model_refused": record.get("status") == "source_model_mismatch",
                "cuts": len(checks), "replayed_cuts": sum(passed for passed, _ in checks),
                "passed": not failures, "failures": failures,
                "replay_seconds": time.perf_counter() - started}
    except (KeyError, TypeError, ValueError, IndexError, AttributeError, OverflowError) as error:
        return {"run_id": record.get("run_id"), "model_bound": False,
                "cuts": len(record.get("cuts", [])), "replayed_cuts": 0,
                "passed": False, "failures": [{"reason": str(error)}],
                "replay_seconds": time.perf_counter() - started}


def tamper_checks(record, expected_model, replay_support):
    """Apply distinct realistic source, row, and coefficient corruptions."""
    mutations = {}
    cut = record["cuts"][0]
    mutations["coefficient"] = lambda data: data["cuts"][0]["coefficients"].__setitem__(
        0, math.nextafter(float(cut["coefficients"][0]), math.inf))
    mutations["rhs"] = lambda data: data["cuts"][0].__setitem__(
        "rhs", math.nextafter(float(cut["rhs"]), math.inf))
    mutations["box"] = lambda data: data["cuts"][0]["box"][0].__setitem__(
        0, math.nextafter(float(cut["box"][0][0]), math.inf))
    mutations["column"] = lambda data: data["cuts"][0]["column_names"].__setitem__(0, "unrelated_variable")
    mutations["feature"] = lambda data: data["cuts"][0]["features"].__setitem__(0, "__import__('os')")
    mutations["domain_row"] = lambda data: data["cuts"][0]["rows"].append(
        [[0.0] * len(cut["variables"]), -1.0])
    mutations["local_scope"] = lambda data: data["cuts"][0].__setitem__("local", True)
    mutations["atom_tree"] = lambda data: data["cuts"][0]["atom_trees"].__setitem__(0, ["num", 17.0])
    mutations["model_hash"] = lambda data: data.__setitem__("model_sha256", "0" * 64)
    first_actual_column = next(iter(cut["actual_row"]["columns"]))
    mutations["actual_coefficient"] = lambda data: data["cuts"][0]["actual_row"]["columns"].__setitem__(
        first_actual_column, math.nextafter(cut["actual_row"]["columns"][first_actual_column], math.inf))
    mutations["actual_bound"] = lambda data: data["cuts"][0]["actual_row"].__setitem__(
        "lhs", math.nextafter(cut["actual_row"]["lhs"], math.inf))
    mutations["actual_mapping"] = lambda data: data["cuts"][0]["actual_row"]["source_to_transformed"][0].__setitem__(
        "source", "unrelated_source")
    checks = {}
    for name, mutate in mutations.items():
        data = copy.deepcopy(record)
        mutate(data)
        checks[name] = not check_run(data, expected_model, replay_support)["passed"]
    return checks


def load_expected_model(case, snapshot):
    if "model" in case:
        return case["model"]
    path = snapshot / "original-osil" / (case["name"] + ".osil")
    if hashlib.sha256(path.read_bytes()).hexdigest() != case["source_sha256"]:
        raise ValueError("pinned original OSiL file is missing or has changed")
    sys.path.insert(0, str(snapshot / "code/univariate_envelopes"))
    from uenv.osil import read_osil
    return encode(asdict(read_osil(str(path))))


def replay_campaign(campaign):
    started = time.perf_counter()
    snapshot = campaign / "snapshot"
    manifest = json.loads((campaign / "source-manifest.json").read_text())
    mismatches = []
    for relative, expected_hash in manifest.items():
        path = snapshot / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
            mismatches.append(relative)
    if mismatches:
        raise ValueError("frozen source hash mismatch: " + ", ".join(mismatches))
    sys.path.insert(0, str(snapshot / TOPIC_NAME))
    from solver.certified import replay_support
    checker_path = Path(sys.modules[replay_support.__module__].__file__).resolve()
    if not checker_path.is_relative_to(snapshot.resolve()):
        raise ValueError("checker was already imported outside the verified frozen snapshot")
    expected_models, results, omitted, control_checks = {}, [], [], None
    records = [json.loads(line) for line in (campaign / "records.jsonl").read_text().splitlines() if line]
    for record in records:
        if "original_model" not in record:
            omitted.append({"run_id": record.get("run_id"), "status": record.get("status"),
                            "cuts": len(record["cuts"]) if "cuts" in record else None,
                            "reason": "worker did not save an original-model result"})
            continue
        name = record["name"]
        if name not in expected_models:
            case_path = campaign / "cases" / (name + ".json")
            pinned_case_path = snapshot / "frozen-cases" / (name + ".json")
            if (not pinned_case_path.is_file()
                    or str(pinned_case_path.relative_to(snapshot)) not in manifest
                    or case_path.read_bytes() != pinned_case_path.read_bytes()):
                raise ValueError("original case descriptor differs from the frozen input: " + name)
            case = json.loads(pinned_case_path.read_text())
            expected_models[name] = load_expected_model(case, snapshot)
        expected = expected_models[name]
        path = campaign / "runs" / (record["run_id"] + ".json")
        if not path.exists() or json.loads(path.read_text()) != record:
            result = {"run_id": record["run_id"], "passed": False, "model_bound": False,
                      "cuts": len(record.get("cuts", [])), "replayed_cuts": 0,
                      "failures": [{"reason": "raw run file differs from saved record stream"}]}
        else:
            result = check_run(record, expected, replay_support)
        results.append(result)
        if result["passed"] and record.get("cuts") and control_checks is None:
            control_checks = tamper_checks(record, expected, replay_support)
    return {
        "schema": "convexification-original-model-replay-v1",
        "campaign": str(campaign.resolve()), "checker": str(checker_path),
        "replay_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_files_verified": len(manifest), "records": len(records),
        "bound_runs": sum(result["model_bound"] for result in results),
        "cuts": sum(result["cuts"] for result in results) + sum(item["cuts"] or 0 for item in omitted),
        "replayed_cuts": sum(result["replayed_cuts"] for result in results),
        "missing_cut_logs": sum(item["cuts"] is None for item in omitted),
        "passed": all(result["passed"] for result in results)
                  and not any(item["cuts"] for item in omitted)
                  and (control_checks is None or all(control_checks.values())),
        "tamper_rejections": control_checks, "omitted_runs": omitted, "runs": results,
        "replay_seconds": time.perf_counter() - started,
        "scope": "Original-model binding and support certificates for recorded added rows only; missing worker logs have unknown cut counts and numerical SCIP bounds are not certified.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("campaign", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = replay_campaign(args.campaign)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({key: result[key] for key in
                      ("passed", "records", "bound_runs", "cuts", "replayed_cuts", "replay_seconds")}))
    raise SystemExit(0 if result["passed"] else 1)
