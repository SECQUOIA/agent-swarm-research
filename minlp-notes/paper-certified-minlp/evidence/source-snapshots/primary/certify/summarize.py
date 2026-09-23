"""Summarize replay verdicts and exact comparisons with unverified references.

Recorded MINLPLib primal values and solver objectives are comparison data,
not independently checked feasible bounds. No comparison certifies optimality
or establishes a solver defect. Decimal reference strings are compared as
exact rationals representing those strings, with no binary-float conversion.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from fractions import Fraction
import json
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]


def rational(value):
    if value is None or value in ("", "NA"):
        return None
    try:
        return Fraction(str(value))
    except (ValueError, ZeroDivisionError):
        return None


def reference_comparison(bound, reference, sense):
    """A negative signed difference puts a reference beyond the bound."""
    bound, reference = rational(bound), rational(reference)
    if bound is None or reference is None or sense not in (1, -1):
        return None
    difference = sense * (reference - bound)
    relative = difference / max(Fraction(1), abs(reference))
    return {"bound": str(bound), "reference": str(reference),
            "signed_difference": str(difference), "normalized_difference": str(relative),
            "reference_beyond_bound": difference < 0,
            "near_reference_1e4": 0 <= relative <= Fraction(1, 10000),
            "near_reference_1e2": 0 <= relative <= Fraction(1, 100)}


def summarize(records, metadata, baselines, expected_records=None):
    statuses = Counter(record.get("status", "unknown") for record in records)
    # Historical OK flags are retained for audit, but cannot confer a new verdict.
    historical_accepted = [r for r in records
                           if r.get("historical_checker", r.get("checker")) == "OK"
                           and r.get("historical_viprchk", r.get("viprchk")) == "OK"]
    indices = [r.get("record_index") for r in records]
    complete = (expected_records is not None and len(indices) == expected_records
                and set(indices) == set(range(expected_records)))
    verified = [r for r in records if r.get("schema") == 1 and r.get("status") == "verified"
                and r.get("report", {}).get("ok") is True]
    rows, discrepancies = [], []
    for record in verified:
        name = record["instance"]
        bound, sense = record.get("certified_bound_original_sense"), record.get("sense")
        comparison = reference_comparison(bound, metadata.get(name, {}).get("primalbound"), sense)
        rows.append({"instance": name, "sense": sense, "bound": bound,
                     "recorded_primal_comparison": comparison,
                     "checker_seconds": record.get("checker_seconds"),
                     "artifact_bytes": record.get("artifact_bytes"),
                     "proof_bytes": record.get("artifacts", {}).get("proof", {}).get("bytes"),
                     "bound_comparison": record.get("bound_comparison")})
        for solver, baseline in baselines.get(name, {}).items():
            if baseline["model_status"] not in (1, 2, 8):
                continue
            result = reference_comparison(bound, baseline["objective"], sense)
            if result is None:
                continue
            # Preserve the historical tolerance, applied with exact arithmetic.
            excess = -Fraction(result["signed_difference"])
            tolerance = Fraction(1, 1000000) * max(Fraction(1), abs(Fraction(bound)))
            if excess > tolerance:
                discrepancies.append({"instance": name, "solver": solver,
                                      "model_status": baseline["model_status"], "comparison": result})
    comparisons = [row["recorded_primal_comparison"] for row in rows if row["recorded_primal_comparison"]]
    times = sorted(r["checker_seconds"] for r in verified if r.get("checker_seconds") is not None)
    return {
        "records": len(records), "expected_records": expected_records, "replay_complete": complete,
        "statuses": dict(statuses), "historical_accepted_total": len(historical_accepted),
        "historical_accepted_unrevalidated": sum(r not in verified for r in historical_accepted),
        "verified": len(verified), "verified_finite_bounds": sum(r["bound"] is not None for r in rows),
        "reference_comparisons": len(comparisons),
        "near_recorded_primal_1e4": sum(c["near_reference_1e4"] for c in comparisons),
        "near_recorded_primal_1e2": sum(c["near_reference_1e2"] for c in comparisons),
        "recorded_primals_beyond_bound": sum(c["reference_beyond_bound"] for c in comparisons),
        "checker_seconds_total": sum(times), "checker_seconds_max": max(times, default=None),
        "proof_bytes_total": sum(r["proof_bytes"] or 0 for r in rows),
        "rows": rows, "solver_discrepancies": discrepancies,
        "interpretation": "Reference primal values and solver objectives are unverified comparison data. "
                          "Near-reference bounds do not certify optimality. Discrepancies require model "
                          "equivalence and returned-solution checks before attributing solver errors.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", type=Path)
    parser.add_argument("--metadata", type=Path, default=LAB / "instances/instancedata.csv")
    parser.add_argument("--baseline", type=Path, default=LAB / "baseline/out")
    parser.add_argument("--out", type=Path, help="optional new JSON summary; existing files are refused")
    args = parser.parse_args()
    records = [json.loads(line) for line in args.records.read_text().splitlines() if line.strip()]
    with args.metadata.open() as stream:
        metadata = {row["name"]: row for row in csv.DictReader(stream, delimiter=";")}
    baselines = {}
    for path in sorted(args.baseline.glob("*.txt")):
        instance, solver = path.stem.rsplit(".", 1)
        fields = path.read_text().strip().split(",")
        try:
            baselines.setdefault(instance, {})[solver] = {"model_status": int(fields[0]), "objective": fields[2]}
        except (ValueError, IndexError):
            continue
    manifest_path = args.records.with_suffix(args.records.suffix + ".manifest.json")
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    summary = summarize(records, metadata, baselines, manifest.get("record_count"))
    if args.out:
        with args.out.open("x") as stream:
            json.dump(summary, stream, indent=2)
            stream.write("\n")
    for key, value in summary.items():
        if key not in ("rows", "solver_discrepancies"):
            print(f"{key}: {value}")
    print(f"solver_discrepancies_requiring_investigation: {len(summary['solver_discrepancies'])}")


if __name__ == "__main__":
    main()
