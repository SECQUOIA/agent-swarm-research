"""Replay original-row cuts against archived source models in a fresh process.

Saved feature strings and affine cut coefficients are never treated as model
definitions. This module independently reconstructs signed original row sides.
The support and affine-bound checkers share exact primitives with producers;
this is an implementation audit, not formal or complete solver verification.
"""
from __future__ import annotations

import argparse
import copy
from dataclasses import asdict
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import sympy as sp

TOPIC_NAME = "research-20261003-convexification"


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


def tree_expression(tree, symbols):
    """Exact interpretation of original binary64 leaves; no text evaluation."""
    if not isinstance(tree, (list, tuple)) or not tree:
        raise ValueError("malformed original source tree")
    tag = tree[0]
    if tag == "num":
        if len(tree) != 2 or not math.isfinite(tree[1]):
            raise ValueError("invalid original constant")
        return sp.Rational(float(tree[1]))
    if tag == "var":
        if len(tree) != 2 or type(tree[1]) is not int or not 0 <= tree[1] < len(symbols):
            raise ValueError("invalid original variable")
        return symbols[tree[1]]
    args = [tree_expression(t, symbols) for t in tree[1:]]
    if tag == "sum":
        return sp.Add(*args)
    if tag == "times":
        return sp.Mul(*args)
    if tag == "negate":
        return -args[0]
    if tag == "divide":
        return args[0] / args[1]
    if tag == "square":
        return args[0] ** 2
    if tag == "power":
        # The model admission separately proves a strictly positive base for
        # variable powers before applying this real identity.
        return sp.exp(args[1] * sp.log(args[0])) if args[1].free_symbols else args[0] ** args[1]
    return {"log": sp.log, "exp": sp.exp, "sqrt": sp.sqrt,
            "sin": sp.sin, "cos": sp.cos, "abs": sp.Abs}[tag](args[0])


def original_rows(model):
    symbols = tuple(sp.Symbol(f"x{i}", real=True) for i in range(len(model["var_lb"])))
    expressions = []
    for i, row in enumerate(model["rows"]):
        terms = [sp.Rational(float(c)) * symbols[int(j)] for j, c in row["lin"].items()]
        terms += [sp.Rational(float(c)) * symbols[j] * symbols[k] for j, k, c in row["quad"]]
        if row["nl"] is not None:
            terms.append(tree_expression(row["nl"], symbols))
        if i == 0:
            terms.append(sp.Rational(float(model["obj_const"])))
        expressions.append(sp.Add(*terms))
    return symbols, expressions


def split_affine(expression, symbols):
    """Independently implement the documented exact row partition."""
    expression = sp.expand(expression, mul=True, multinomial=False,
                           power_base=False, power_exp=False)
    constant, affine, nonlinear = sp.Rational(0), {}, []
    positions = {symbol: i for i, symbol in enumerate(symbols)}
    for term in sp.Add.make_args(expression):
        local_symbols = tuple(symbol for symbol in symbols if symbol in term.free_symbols)
        if not local_symbols:
            if term.is_Rational:
                constant += term
            else:
                nonlinear.append(term)
            continue
        try:
            # Absent global variables cannot change polynomial degree. Using
            # only present generators also avoids SymPy recursion on a sparse
            # row in an otherwise very large original model.
            polynomial = sp.Poly(term, *local_symbols)
        except (sp.PolynomialError, RecursionError):
            nonlinear.append(term)
            continue
        if polynomial.total_degree() > 1:
            nonlinear.append(term)
            continue
        for powers, coefficient in polynomial.terms():
            if not coefficient.is_Rational:
                # A nonrational constant cannot silently be rounded into a
                # rational cut-elimination coefficient.
                nonlinear.append(coefficient * sp.Mul(*(
                    symbol ** power for symbol, power in zip(local_symbols, powers))))
            elif sum(powers) == 0:
                constant += coefficient
            else:
                index = positions[local_symbols[powers.index(1)]]
                affine[index] = affine.get(index, sp.Rational(0)) + coefficient
    return sp.Add(*nonlinear), {i: c for i, c in affine.items() if c}, constant


def signed_original_side(model, symbols, expression, row_index, sign, objective):
    if type(row_index) is not int or not 0 <= row_index < len(model["rows"]):
        raise ValueError("invalid original row index")
    if sign not in (-1, 1) or type(sign) is not int or type(objective) is not bool:
        raise ValueError("invalid signed original side")
    if objective != (row_index == 0):
        raise ValueError("objective side bound to wrong original row")
    h, affine, constant = split_affine(expression, symbols)
    terms = {f"x{i}": Q(sign * coefficient) for i, coefficient in affine.items()}
    if objective:
        expected = 1 if model["obj_sense"] == "min" else -1
        if sign != expected:
            raise ValueError("objective sense changed")
        terms["objective_epigraph"] = Q(-sign)
        rhs = -sign * Q(constant)
        source_id = "row0:objective"
    else:
        side = model["rows"][row_index]["ub" if sign == 1 else "lb"]
        if not math.isfinite(side):
            raise ValueError("claimed original side is infinite")
        rhs = sign * (Q(float(side)) - Q(constant))
        source_id = f"row{row_index}:" + ("upper" if sign == 1 else "lower")
    return sign * h, terms, rhs, source_id


def original_instance(model):
    from types import SimpleNamespace
    model = copy.deepcopy(model)
    for row in model["rows"]:
        row["lin"] = {int(i): c for i, c in row["lin"].items()}
    return SimpleNamespace(**model)


def admitted_bounds(record, model):
    from solver.bounds import replay_bounds
    certificate = record["model_metadata"]["bound_certificate"]
    if not replay_bounds(original_instance(model), certificate):
        raise ValueError("affine bound proof failed against original model")
    if certificate["result"]["infeasible"]:
        raise ValueError("a solved model has contradictory affine bounds")
    result = certificate["result"]
    lower = [float.fromhex(x) for x in result["float_lower"]]
    upper = [float.fromhex(x) for x in result["float_upper"]]
    if not len(lower) == len(upper) == len(model["var_lb"]):
        raise ValueError("wrong proved bound dimension")
    return tuple(zip(lower, upper))


def sum_terms(terms):
    result = {}
    for name, value in terms:
        if not isinstance(name, str):
            raise ValueError("invalid source column")
        result[name] = result.get(name, Q(0)) + Q(value)
    return {name: value for name, value in result.items() if value}


def check_cut(cut, model, bounds, replay_support):
    from solver.row_certificate import AffineSide, replay_row_certificate
    try:
        symbols, expressions = original_rows(model)
        variables = cut["variables"]
        if (not variables or any(type(i) is not int for i in variables)
                or variables != sorted(set(variables))
                or any(not 0 <= i < len(symbols) for i in variables)):
            return False, "invalid block variable indices"
        block_symbols = tuple(symbols[i] for i in variables)
        if cut["symbols"] != [str(s) for s in block_symbols]:
            return False, "changed symbolic source coordinates"
        box = tuple(bounds[i] for i in variables)
        if not all(math.isfinite(v) for pair in box for v in pair):
            return False, "support domain lacks finite proved bounds"
        if cut["box"] != [[str(Q(v)) for v in pair] for pair in box]:
            return False, "support box differs from replayed affine implications"

        features, sides = list(block_symbols), []
        for side in cut["signed_sides"]:
            ri, sign = side["row_index"], side["sign"]
            h, terms, rhs, source_id = signed_original_side(
                model, symbols, expressions[ri], ri, sign, ri == 0)
            if h.free_symbols - set(block_symbols):
                return False, "support omits an original nonlinear variable"
            expected_side = "objective" if ri == 0 else "upper" if sign == 1 else "lower"
            if (side["source_id"] != source_id or side["side"] != expected_side
                    or side["nonlinear"] != str(h)
                    or sum_terms(side["affine_terms"]) != terms or Q(side["rhs"]) != rhs):
                return False, "signed side differs from original source row"
            features.append(h)
            # The ordering is irrelevant to the original equation, but is
            # retained for the lower-level certificate's exact JSON binding.
            sides.append(AffineSide(source_id, side["affine_terms"], rhs))
        if not sides or cut["features"] != [str(f) for f in features]:
            return False, "saved support features differ from source-derived features"

        domain = []
        for row in cut["domain_rows"]:
            ri, sign = row["row_index"], row["sign"]
            if ri == 0:
                return False, "objective incorrectly used as a domain constraint"
            h, terms, rhs, _ = signed_original_side(
                model, symbols, expressions[ri], ri, sign, False)
            if h != 0 or any(name not in {f"x{i}" for i in variables} for name in terms):
                return False, "domain row is not an original affine block restriction"
            coefficients = tuple(terms.get(f"x{i}", Q(0)) for i in variables)
            if row["coefficients"] != [str(c) for c in coefficients] or Q(row["rhs"]) != rhs:
                return False, "domain coefficients differ from the original row"
            domain.append((coefficients, rhs))

        coefficients = cut["coefficients"]
        if len(coefficients) != len(features) or not all(math.isfinite(v) for v in coefficients):
            return False, "invalid actual support normal"
        multipliers = coefficients[len(variables):]
        if any(v < 0 for v in multipliers):
            return False, "negative source-side multiplier"
        witness = cut["support_witness"]
        if witness.get("status") != "complete":
            return False, "no completed support certificate"
        beta = float.fromhex(witness["rhs"])
        if not math.isfinite(beta) or not replay_support(
                tuple(features), block_symbols, box, coefficients, domain, witness):
            return False, "support proof failed against original source features"
        support_id = hashlib.sha256(json.dumps(witness, sort_keys=True,
                                               separators=(",", ":"), allow_nan=False).encode()).hexdigest()
        certificate = cut["row_certificate"]
        names = certificate["binding"]["variables"]
        allowed_names = {f"x{i}": bounds[i] for i in range(len(symbols))}
        allowed_names["objective_epigraph"] = (-math.inf, math.inf)
        if len(names) != len(set(names)) or any(name not in allowed_names for name in names):
            return False, "unbound eliminated-row variable"
        linear = {f"x{i}": coefficient for i, coefficient in zip(variables, coefficients)
                  if coefficient}
        if not replay_row_certificate(
                certificate, variables=names, bounds={name: allowed_names[name] for name in names},
                linear_terms=linear, multipliers=multipliers, support_rhs=beta,
                sides=sides, support_id=support_id):
            return False, "original-row elimination or binary64 compensation failed"
        exported = certificate["exported"]
        if cut["rhs"] != exported["rhs"] or cut.get("local") is not False:
            return False, "actual requested bound or scope differs from row certificate"
        source_names = ["v" + name[1:] if name.startswith("x") else name for name in names]
        if cut["column_names"] != source_names:
            return False, "requested columns do not match original variables"
        nonzero = {name: Q(float(value)) for name, value in zip(source_names, exported["coefficients"]) if value}
        actual = cut["actual_row"]
        if actual["local"] is not False or actual.get("fixed_substitutions"):
            return False, "actual row assumes an unproved local restriction or fixing"
        mapping = actual["source_to_transformed"]
        if (len(mapping) != len(nonzero) or {entry["source"] for entry in mapping} != set(nonzero)
                or len({entry["transformed"] for entry in mapping}) != len(mapping)):
            return False, "actual row drops or aggregates a certified source column"
        actual_coefficients = {entry["transformed"]: nonzero[entry["source"]] for entry in mapping}
        if {name: Q(float(value)) for name, value in actual["columns"].items()} != actual_coefficients:
            return False, "actual inserted coefficients differ from the exported certificate"
        if Q(float(actual["lhs"])) - Q(float(actual["constant"])) != Q(float(exported["rhs"])):
            return False, "actual inserted lower bound differs from exported certificate"
        if (not math.isfinite(actual["scip_infinity"]) or actual["scip_infinity"] <= 0
                or not actual["rhs"] >= actual["scip_infinity"]):
            return False, "actual row has an unexpected finite upper bound"
        return True, "replayed original-side aggregation, support, and actual row"
    except (KeyError, TypeError, ValueError, IndexError, AttributeError, OverflowError, ZeroDivisionError):
        return False, "malformed or unsupported saved cut"


def check_run(record, expected_model, replay_support):
    started = time.perf_counter()
    try:
        if record.get("original_model") != expected_model or record.get("model_sha256") != model_digest(expected_model):
            raise ValueError("saved original model differs from the frozen input")
        model = decode(expected_model)
        cuts = record.get("cuts")
        if not isinstance(cuts, list):
            raise ValueError("missing complete added-cut list")
        metadata = record.get("model_metadata")
        if metadata is None:
            if cuts or any(record.get(key) is not None for key in
                           ("primal", "dual", "root_dual", "original_values")):
                raise ValueError("unadmitted model unexpectedly contains solver evidence")
            return {"run_id": record.get("run_id"), "model_bound": True, "model_admitted": False,
                    "cuts": 0, "replayed_cuts": 0, "passed": True, "failures": [],
                    "cut_log_complete": record.get("cut_log_complete") is True,
                    "replay_seconds": time.perf_counter() - started}
        from reviews.model_binding_audit import replay_model_metadata
        if not replay_model_metadata(original_instance(model), metadata):
            raise ValueError("source domains or native variable metadata did not replay")
        bounds = admitted_bounds(record, model)
        if record.get("mode") == "baseline" and cuts:
            raise ValueError("baseline unexpectedly contains experimental cuts")
        checks = [check_cut(cut, model, bounds, replay_support) for cut in cuts]
        failures = [{"cut": i, "reason": reason} for i, (passed, reason) in enumerate(checks) if not passed]
        return {"run_id": record.get("run_id"), "model_bound": True, "model_admitted": True,
                "cuts": len(cuts), "replayed_cuts": sum(passed for passed, _ in checks),
                "passed": not failures, "failures": failures,
                "cut_log_complete": record.get("cut_log_complete") is True,
                "replay_seconds": time.perf_counter() - started}
    except (KeyError, TypeError, ValueError, IndexError, AttributeError, OverflowError, ZeroDivisionError) as exc:
        return {"run_id": record.get("run_id"), "model_bound": False, "model_admitted": False,
                "cuts": len(record["cuts"]) if isinstance(record.get("cuts"), list) else None,
                "replayed_cuts": 0, "passed": False, "failures": [{"reason": str(exc)}],
                "cut_log_complete": record.get("cut_log_complete") is True,
                "replay_seconds": time.perf_counter() - started}


def tamper_checks(record, expected_model, replay_support):
    """Distinct model, row-premise, support, conversion and actual-row edits."""
    first = record["cuts"][0]
    mutations = {
        "original_model_digest": lambda r: r.__setitem__("model_sha256", "0"*64),
        "support_coefficient": lambda r: r["cuts"][0]["coefficients"].__setitem__(
            0, math.nextafter(first["coefficients"][0], math.inf)),
        "source_side_rhs": lambda r: r["cuts"][0]["signed_sides"][0].__setitem__(
            "rhs", str(Q(first["signed_sides"][0]["rhs"])+1)),
        "source_side_identity": lambda r: r["cuts"][0]["signed_sides"][0].__setitem__("source_id", "unrelated"),
        "support_feature": lambda r: r["cuts"][0]["features"].__setitem__(0, "__import__('os')"),
        "support_box": lambda r: r["cuts"][0]["box"][0].__setitem__(0, str(Q(first["box"][0][0])+1)),
        "row_rhs": lambda r: r["cuts"][0].__setitem__("rhs", math.nextafter(first["rhs"], math.inf)),
        "local_scope": lambda r: r["cuts"][0].__setitem__("local", True),
        "rounding_compensation": lambda r: r["cuts"][0]["row_certificate"]["exact"].__setitem__(
            "box_compensation", str(Q(first["row_certificate"]["exact"]["box_compensation"])+1)),
        "support_identity": lambda r: r["cuts"][0]["row_certificate"]["binding"]["support"].__setitem__(
            "support_id", "0"*64),
    }
    column = next(iter(first["actual_row"]["columns"]), None)
    mutations["actual_coefficient"] = lambda r: r["cuts"][0]["actual_row"]["columns"].__setitem__(
        "forged_column" if column is None else column,
        1.0 if column is None else math.nextafter(first["actual_row"]["columns"][column], math.inf))
    mutations["actual_bound"] = lambda r: r["cuts"][0]["actual_row"].__setitem__(
        "lhs", math.nextafter(first["actual_row"]["lhs"], math.inf))
    if first["actual_row"]["source_to_transformed"]:
        mutations["actual_mapping"] = lambda r: r["cuts"][0]["actual_row"]["source_to_transformed"][0].__setitem__(
            "source", "unrelated_source")
    else:
        mutations["actual_mapping"] = lambda r: r["cuts"][0]["actual_row"]["source_to_transformed"].append(
            {"source": "unrelated_source", "transformed": "forged_column"})
    mutations["bound_proof"] = lambda r: r["model_metadata"]["bound_certificate"]["result"]["float_lower"].__setitem__(
        0, math.nextafter(float.fromhex(r["model_metadata"]["bound_certificate"]["result"]["float_lower"][0]), math.inf).hex())
    results = {}
    for name, mutate in mutations.items():
        data = copy.deepcopy(record)
        mutate(data)
        results[name] = not check_run(data, expected_model, replay_support)["passed"]
    return results


def load_expected_model(case, snapshot):
    if "model" in case:
        return case["model"]
    path = snapshot / "original-osil" / (case["name"] + ".osil")
    if hashlib.sha256(path.read_bytes()).hexdigest() != case["source_sha256"]:
        raise ValueError("pinned original OSiL file has changed")
    sys.path.insert(0, str(snapshot / "code/univariate_envelopes"))
    from uenv.osil import read_osil
    return encode(asdict(read_osil(str(path))))


def replay_campaign(campaign):
    started = time.perf_counter()
    snapshot = campaign / "snapshot"
    manifest = json.loads((campaign / "source-manifest.json").read_text())
    mismatches = [relative for relative, expected in manifest.items()
                  if not (snapshot/relative).is_file()
                  or hashlib.sha256((snapshot/relative).read_bytes()).hexdigest() != expected]
    if mismatches:
        raise ValueError("frozen source hash mismatch: " + ", ".join(mismatches))
    sys.path.insert(0, str(snapshot/TOPIC_NAME))
    from solver.support import replay_support
    checker = Path(sys.modules[replay_support.__module__].__file__).resolve()
    if not checker.is_relative_to(snapshot.resolve()):
        raise ValueError("support checker imported from outside verified snapshot")
    records = [json.loads(line) for line in (campaign/"records.jsonl").read_text().splitlines() if line]
    results, omitted, expected_models, controls = [], [], {}, None
    for record in records:
        if "original_model" not in record:
            omitted.append({"run_id": record.get("run_id"), "status": record.get("status"),
                            "cuts": len(record["cuts"]) if isinstance(record.get("cuts"), list) else None,
                            "cut_log_complete": record.get("cut_log_complete") is True,
                            "reason": "worker did not save an original-model result"})
            continue
        name = record["name"]
        if name not in expected_models:
            descriptor = campaign/"cases"/(name+".json")
            pinned = snapshot/"frozen-cases"/(name+".json")
            if (not pinned.is_file() or str(pinned.relative_to(snapshot)) not in manifest
                    or descriptor.read_bytes() != pinned.read_bytes()):
                raise ValueError("case descriptor differs from frozen input: " + name)
            expected_models[name] = load_expected_model(json.loads(pinned.read_text()), snapshot)
        expected = expected_models[name]
        raw = campaign/"runs"/(record["run_id"]+".json")
        if not raw.exists() or json.loads(raw.read_text()) != record:
            result = {"run_id": record["run_id"], "passed": False, "model_bound": False,
                      "model_admitted": False, "cuts": len(record.get("cuts") or []), "replayed_cuts": 0,
                      "cut_log_complete": False, "failures": [{"reason": "raw run differs from ledger"}]}
        else:
            result = check_run(record, expected, replay_support)
        results.append(result)
        if result["passed"] and record.get("cuts") and controls is None:
            controls = tamper_checks(record, expected, replay_support)
    return {
        "schema": "original-row-aggregation-replay-v2", "campaign": str(campaign.resolve()),
        "checker": str(checker), "replay_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_files_verified": len(manifest), "records": len(records),
        "bound_runs": sum(r["model_bound"] for r in results),
        "admitted_runs": sum(r["model_admitted"] for r in results),
        "cuts": sum(r["cuts"] or 0 for r in results) + sum(r["cuts"] or 0 for r in omitted),
        "replayed_cuts": sum(r["replayed_cuts"] for r in results),
        "missing_cut_logs": sum(not r["cut_log_complete"] for r in results + omitted),
        "passed": all(r["passed"] for r in results) and not any(r["cuts"] for r in omitted)
                  and (controls is None or all(controls.values())),
        "tamper_rejections": controls, "omitted_runs": omitted, "runs": results,
        "replay_seconds": time.perf_counter()-started,
        "scope": "Original-model domain binding, support, source-side elimination, binary64 compensation, and actual recorded SCIP rows; numerical solver bounds and missing cut logs are not certified.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("campaign", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = replay_campaign(args.campaign)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(json.dumps({k: result[k] for k in
                      ("passed", "records", "bound_runs", "cuts", "replayed_cuts", "replay_seconds")}))
    raise SystemExit(0 if result["passed"] else 1)
