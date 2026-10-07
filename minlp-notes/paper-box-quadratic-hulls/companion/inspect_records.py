#!/usr/bin/env python3
"""Inspect archived records without importing or running optimization code.

The standard-library-only default verifies copied source hashes, reconstructs
reported tables, and checks the archived rounded tables. --write also exports
the reconstructed tables as CSV. It never solves a model or generates an instance.
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import statistics


BASE = Path(__file__).resolve().parent


def json_lines(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def check_hashes():
    records = json.loads((BASE / "source-manifest.json").read_text())["files"]
    for record in records:
        path = BASE / record["copy"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != record["sha256"]:
            raise ValueError("Checksum differs: " + record["copy"])
    return len(records)


def methods(path):
    grouped = {}
    for record in json_lines(path):
        grouped.setdefault(record["method"], []).append(record)
    return grouped


def reference(tag):
    candidates = []
    gurobi = []
    for directory in ("ub", "ub2"):
        path = BASE / "logs" / directory / (tag + ".json")
        if path.exists():
            candidates.append(json_lines(path)[-1]["ub"])
    for directory in ("gurobi", "gurobi2"):
        path = BASE / "logs" / directory / (tag + ".log")
        if path.exists():
            text = path.read_text()
            matches = re.findall(
                r"Best objective ([-+0-9.e]+), best bound ([-+0-9.e]+), gap ([-+0-9.e]+)%",
                text,
            )
            if matches:
                upper, lower, _ = map(float, matches[-1])
                candidates.append(upper)
                gurobi.append((upper, lower, "Optimal solution found" in text))
    if any(record[2] for record in gurobi):
        return min(record[0] for record in gurobi), "optimal within requested tolerance"
    if not candidates:
        raise ValueError("No reference value for " + tag)
    return min(candidates), "feasible value"


def stage(records, method):
    own = records if method == "B" else records[1:]
    return (
        sum(record["time_solve"] for record in own),
        sum(record["time_sep"] for record in records),
        len(records) - (0 if method == "B" else 1),
    )


def constructed_rows():
    rows = []
    for family in ("chain", "cactus", "ht"):
        for path in sorted((BASE / "logs" / family).glob("*.jsonl")):
            if path.name.startswith("xf_"):
                continue
            grouped = methods(path)
            xf = BASE / "logs" / "chain" / ("xf_" + path.name)
            if "XF" not in grouped and xf.exists():
                grouped["XF"] = methods(xf)["XF"]
            tag = path.stem
            upper, kind = reference(tag)
            baseline = grouped["B"][-1]["safe"]
            best = max(records[-1]["safe"] for records in grouped.values())
            for method, records in grouped.items():
                last = records[-1]
                solve, separation, rounds = stage(records, method)
                if method in ("KAF", "KAFc", "KAX"):
                    own_solve, _, own_rounds = stage(grouped["KA"], "KA")
                    solve += own_solve
                    rounds += own_rounds
                rows.append({
                    "instance": tag,
                    "family": family,
                    "reference": upper,
                    "reference_kind": kind,
                    "method": method,
                    "bound_estimate": last["safe"],
                    "baseline_bound_estimate": baseline,
                    "closure": (last["safe"] - baseline) / (upper - baseline),
                    "closure_to_best_reported_bound": (last["safe"] - baseline) / (best - baseline)
                    if best - baseline > 1e-9 * max(1, abs(best)) else None,
                    "rounds": rounds,
                    "solve_seconds": solve,
                    "separation_seconds": separation,
                    "variables": last["size"]["vars"],
                    "soc": last["size"]["soc"],
                    "psd_entries": last["size"]["psd_svec"],
                    "family_blocks": last["size"]["F"],
                    "lifted_triples": last["size"]["X"],
                    "status": last["status"],
                    "reported_primal_infeasibility": last["pinf"],
                    "primal_value": last["pobj"],
                    "xf_separate_run": method == "XF" and family == "chain",
                })
    return rows


def check_archived_tables(rows):
    lookup = {(row["instance"], row["method"]): row for row in rows}
    checked = 0
    for family in ("chain", "cactus", "ht"):
        current = None
        for line in (BASE / "logs" / ("table_" + family + ".md")).read_text().splitlines()[2:]:
            columns = [part.strip() for part in line.split("|")[1:-1]]
            if not columns:
                continue
            if columns[0]:
                current = columns[0]
            row = lookup[(current, columns[2])]
            comparisons = (
                ("bound_estimate", 3, 0.00000051),
                ("closure", 4, 0.000051),
                ("solve_seconds", 7, 0.0051),
                ("separation_seconds", 8, 0.0051),
                ("variables", 10, 0),
                ("soc", 11, 0),
                ("psd_entries", 12, 0),
            )
            for field, column, tolerance in comparisons:
                if abs(row[field] - float(columns[column])) > tolerance:
                    raise ValueError(f"Archived table differs: {current}, {row['method']}, {field}")
            checked += 1
    return checked


def hard_three_rows():
    records = json_lines(BASE / "data" / "pool_hard3.jsonl")
    if len(records) != 109:
        raise ValueError("Unexpected hard objective count")
    rows = []
    for method in ("K", "A", "KA", "F", "KAF"):
        values = [
            (record[method + "_safe"] - record["B_safe"])
            / (record["X_safe"] - record["B_safe"])
            for record in records
        ]
        rows.append({"method": method, "count": len(values),
                     "mean": statistics.mean(values),
                     "median": statistics.median(values), "minimum": min(values)})
    return rows


def strict_sensitivity_rows():
    record = json.loads((BASE / "logs" / "strict_r1" / "spar090-075-1.json").read_text())
    residual = record["max_triangle_violation"]
    depth = record["min_depth"]
    gap = record["opt"] - record["B_safe"]
    margin = record["B"] - record["B_safe"]
    choices = (
        ("computed depths (diagnostic)", max(0, -depth)),
        ("triangle residual (lower bound on gain expression)", 4 * residual),
        ("assume exact minimum depth >= -1e-7", 1e-7),
        ("assume each computed depth overestimates exact depth by <= 1e-7", max(0, -depth) + 1e-7),
    )
    rows = []
    for assumption, epsilon in choices:
        gain = epsilon * (record["f_uniform"] - record["B"]) / (1 + epsilon)
        rows.append({"assumption": assumption, "epsilon": epsilon,
                     "gain_expression": gain, "percent_of_recorded_gap": 100 * gain / gap,
                     "percent_with_primal_to_dual_margin": 100 * (gain + margin) / gap,
                     "certified": False})
    return rows


def write_csv(path, rows):
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="also export reconstructed CSV tables")
    arguments = parser.parse_args()
    hashes = check_hashes()
    constructed = constructed_rows()
    checked = check_archived_tables(constructed)
    hard = hard_three_rows()
    strict = strict_sensitivity_rows()
    if arguments.write:
        directory = BASE / "tables"
        directory.mkdir(exist_ok=True)
        for name, rows in (("constructed-results", constructed), ("hard-three-closures", hard),
                           ("strict-sensitivity", strict)):
            write_csv(directory / (name + ".csv"), rows)
    print(f"PASS: {hashes} copied-source SHA256 hashes verified")
    print(f"PASS: {checked} archived constructed-method table rows reconstructed")
    print("PASS: 109 hard-objective closures and strict gain sensitivities reconstructed")
    print("No optimization code imported; no instance generated; no model solved.")


if __name__ == "__main__":
    main()
