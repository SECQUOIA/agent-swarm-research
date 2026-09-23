"""Exact rational trace comparison for the archived kinetics decimal inputs.

Decimal strings in Q_drop0.csv are interpreted as exact rational numbers. This
certifies the finite supplied-data trace problem, not exact physical sensitivities.
The exhaustive schedule set is independently checked by a second enumeration.
Trace arithmetic and ranking decisions are exact; decimal display values and
runtime fields use floating point.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
from time import perf_counter

from kinetics_selection_recheck import (
    BUDGETS, DEFAULT_DATA, SOURCE_COMMIT, SOURCE_SHA256, SOURCE_URL,
    Schedule, schedules, valid_patterns, validate_enumeration,
)


def inverse(matrix: list[list[Q]]) -> list[list[Q]]:
    """Gauss-Jordan elimination over rational numbers, with exact pivot tests."""
    n = len(matrix)
    work = [row[:] + [Q(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if work[i][col] != 0), None)
        if pivot is None:
            raise ValueError("singular rational matrix")
        work[col], work[pivot] = work[pivot], work[col]
        divisor = work[col][col]
        work[col] = [value / divisor for value in work[col]]
        for i in range(n):
            if i == col:
                continue
            multiplier = work[i][col]
            work[i] = [a - multiplier*b for a, b in zip(work[i], work[col])]
    assert all(work[i][j] == int(i == j) for i in range(n) for j in range(n))
    return [row[n:] for row in work]


def exact_pattern_traces(data_path: Path) -> tuple[dict[int, list[Q]], dict[int, list[Q]]]:
    if hashlib.sha256(data_path.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError("sensitivity file does not match the audited source hash")
    with data_path.open(newline="") as stream:
        rows = list(csv.reader(stream))
    assert rows[0] == ["Unnamed: 0", "A1", "A2", "E1", "E2"]
    F = [[Q(value) for value in row[1:]] for row in rows[1:]]
    assert len(F) == 24 and all(len(row) == 4 for row in F)
    B = [[Q(1), Q(1, 10), Q(1, 10)],
         [Q(1, 10), Q(4), Q(1, 2)],
         [Q(1, 10), Q(1, 2), Q(8)]]
    R = [[B[i % 3][j % 3] * (1 if i // 3 == j // 3 else Q(1, 2))
          for j in range(6)] for i in range(6)]
    K = inverse(R)
    marginal, gated = {}, {}
    for mask in valid_patterns():
        selected = [i for i in range(6) if mask & (1 << i)]
        Rsub = [[R[i][j] for j in selected] for i in selected]
        Ksub = [[K[i][j] for j in selected] for i in selected]
        selected_precision = inverse(Rsub) if selected else []
        marginal[mask], gated[mask] = [], []
        for t in range(8):
            rows_at_time = [F[(i % 3)*8 + t] for i in selected]
            for output, precision in ((marginal, selected_precision), (gated, Ksub)):
                trace = sum((precision[i][j] * sum((a*b for a, b in zip(fi, fj)), Q(0))
                             for i, fi in enumerate(rows_at_time)
                             for j, fj in enumerate(rows_at_time)), Q(0))
                output[mask].append(trace)
    return marginal, gated


def rational_record(value: Q) -> dict:
    return {"numerator": str(value.numerator), "denominator": str(value.denominator),
            "fraction": str(value), "decimal_approximation": float(value)}


def ranking_record(indices: list[int], traces: list[Q],
                   all_schedules: tuple[Schedule, ...]) -> tuple[dict, int]:
    ranked = sorted(indices, key=lambda i: (-traces[i], i))
    best, second = ranked[0], ranked[1]
    ties = [i for i in ranked if traces[i] == traces[best]]
    return {
        "winning_selection": all_schedules[best].describe(),
        "winning_trace": rational_record(traces[best]),
        "exact_optimal_count": len(ties),
        "exact_optimal_selections": [all_schedules[i].describe() for i in ties],
        "runner_up_selection": all_schedules[second].describe(),
        "runner_up_trace": rational_record(traces[second]),
        "winning_margin_to_runner_up": rational_record(traces[best] - traces[second]),
    }, best


def certify(data_path: Path = DEFAULT_DATA) -> dict:
    started = perf_counter()
    all_schedules = schedules()
    enumeration_check = validate_enumeration(all_schedules)
    pattern_traces = exact_pattern_traces(data_path)
    # Four diagonal regularization entries, each exactly 1/10000.
    traces = [[Q(4, 10000) + sum((patterns[mask][t]
                               for t, mask in enumerate(schedule.time_patterns)), Q(0))
               for schedule in all_schedules] for patterns in pattern_traces]
    assert all(gated >= marginal for marginal, gated in zip(*traces))
    results = []
    for budget in BUDGETS:
        feasible = [i for i, schedule in enumerate(all_schedules) if schedule.cost <= budget]
        marginal, marginal_best = ranking_record(feasible, traces[0], all_schedules)
        gated, gated_best = ranking_record(feasible, traces[1], all_schedules)
        true_at_gated = traces[0][gated_best]
        regret = traces[0][marginal_best] - true_at_gated
        results.append({
            "budget": budget, "feasible_schedules": len(feasible),
            "marginal": marginal, "gated": gated,
            "selections_differ": marginal_best != gated_best,
            "gated_selection_true_trace": rational_record(true_at_gated),
            "exact_true_regret": rational_record(regret),
            "exact_relative_true_regret": rational_record(regret / traces[0][marginal_best]),
            "gating_inflation_at_marginal_selection": rational_record(
                traces[1][marginal_best] / traces[0][marginal_best]),
            "gating_inflation_at_gated_selection": rational_record(
                traces[1][gated_best] / true_at_gated),
        })
    return {
        "metadata": {
            "source_commit": SOURCE_COMMIT, "sensitivity_url": SOURCE_URL,
            "sensitivity_sha256": SOURCE_SHA256,
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "arithmetic": "Python Fraction for every information coefficient, objective, ordering, equality test, regret, and inflation ratio",
            "input_interpretation": "exact rational interpretation of the archived CSV decimal strings and rational code covariance; no claim of exact physical sensitivities",
            "regularization": "1/10000 on each of four information diagonal entries",
            "criterion": "maximize trace information, called A-optimality in the source",
            "numerical_approximations": "decimal_approximation fields are displays only and never determine rankings",
            "selection_provenance": "our exhaustive exact rankings, not deserialized author selections",
        },
        "enumeration_validation": enumeration_check,
        "exact_gating_trace_at_least_marginal_for_every_schedule": True,
        "results": results,
        "wall_seconds": perf_counter() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(certify(args.data), indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(result)
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
