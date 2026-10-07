"""Exhaustively recheck public kinetics inputs under two information formulas.

No author optimization code or stored pickle results are executed. This compares
our optima on the archived statistical inputs, not independently regenerated
kinetic sensitivities or the authors' saved selections. All objectives include
the source's 1e-4 diagonal regularization. Runtime needs NumPy only.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path
from time import perf_counter

import numpy as np


SOURCE_COMMIT = "430090e610446aab88328ce495ffb15b684c56c4"
SOURCE_URL = (
    "https://raw.githubusercontent.com/dowlinglab/measurement-opt/"
    + SOURCE_COMMIT + "/kinetics_source_data/Q_drop0.csv"
)
SOURCE_SHA256 = "54506ecb5606ea8900a99cb8490508bdd4b9a364aba4f26efe2676f9a7f6f3ca"
DEFAULT_DATA = Path(__file__).with_name("data") / "kinetics_Q_drop0.csv"
SPECIES = ("A", "B", "C")
TIMES = tuple(7.5 * (i + 1) for i in range(8))
BUDGETS = tuple(range(1000, 5001, 400))
REGULARIZATION = 1e-4 * np.eye(4)
CRITERIA = ("trace_information", "logdet_information", "trace_inverse_information")
DIRECTIONS = (1, 1, -1)
TIE_TOLERANCE = 1e-9


@dataclass(frozen=True)
class Schedule:
    static_mask: int
    manual: tuple[tuple[int, int], ...]  # (time index, species index)

    @property
    def static(self) -> tuple[int, ...]:
        return tuple(s for s in range(3) if self.static_mask & (1 << s))

    @property
    def cost(self) -> int:
        return (2000 * len(self.static) + 200 * len({s for _, s in self.manual})
                + 400 * len(self.manual))

    @property
    def time_patterns(self) -> tuple[int, ...]:
        masks = [self.static_mask] * 8
        for t, s in self.manual:
            masks[t] |= 1 << (s + 3)
        return tuple(masks)

    def describe(self) -> dict:
        return {
            "scm_species": [SPECIES[s] for s in self.static],
            "dcm_installed_species": sorted({SPECIES[s] for _, s in self.manual}),
            "manual_samples": [{"species": SPECIES[s], "time_minutes": TIMES[t]}
                               for t, s in self.manual],
            "cost": self.cost,
            "scalar_observation_count": 8 * len(self.static) + len(self.manual),
            "time_pattern_masks": self.time_patterns,
        }


def covariance() -> np.ndarray:
    B = np.array([[1, 0.1, 0.1], [0.1, 4, 0.5], [0.1, 0.5, 8]])
    return np.kron(np.array([[1, 0.5], [0.5, 1]]), B)


def load_sensitivities(path: Path) -> np.ndarray:
    """Validate immutable input bytes and return time-by-channel-by-parameter F."""
    if not path.is_file():
        raise FileNotFoundError(
            "Prepare the pinned input with data/prepare_input.py, or pass --data. "
            "See data/README.md for the source and preparation command."
        )
    if hashlib.sha256(path.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError("sensitivity file does not match the audited source hash")
    with path.open(newline="") as stream:
        rows = list(csv.reader(stream))
    if rows[0] != ["Unnamed: 0", "A1", "A2", "E1", "E2"]:
        raise ValueError("unexpected sensitivity CSV header")
    Q = np.array([[float(x) for x in row[1:]] for row in rows[1:]])
    if Q.shape != (24, 4) or not np.all(np.isfinite(Q)):
        raise ValueError("expected 24 finite sensitivity rows and four parameters")
    species_time = Q.reshape(3, 8, 4)
    by_time = species_time.transpose(1, 0, 2)
    return np.concatenate([by_time, by_time], axis=1)


def schedules() -> tuple[Schedule, ...]:
    """Enumerate every source-feasible schedule before applying its budget."""
    choices = []
    for static_mask in range(8):
        available_species = tuple(s for s in range(3) if not static_mask & (1 << s))
        for q in range(5):
            for times in combinations(range(8), q):
                if any(b - a < 2 for a, b in zip(times[:-1], times[1:])):
                    continue
                for species in product(available_species, repeat=q):
                    if static_mask == 0 and q == 0:
                        continue  # Source requires at least one selection.
                    choices.append(Schedule(static_mask, tuple(zip(times, species))))
    return tuple(sorted(choices, key=lambda x: (x.cost, x.static_mask, x.manual)))


def valid_patterns() -> tuple[int, ...]:
    masks = []
    for static in range(8):
        masks.append(static)
        for s in range(3):
            if not static & (1 << s):
                masks.append(static | (1 << (s + 3)))
    return tuple(sorted(masks))


def pattern_information(F: np.ndarray) -> tuple[np.ndarray, tuple[int, ...]]:
    """Return [marginal/gated, time, pattern, parameter, parameter] matrices."""
    R = covariance()
    full_precision = np.linalg.solve(R, np.eye(6))
    masks = valid_patterns()
    information = np.zeros((2, 8, len(masks), 4, 4))
    for j, mask in enumerate(masks):
        selected = [s for s in range(6) if mask & (1 << s)]
        if not selected:
            continue
        Rsub = R[np.ix_(selected, selected)]
        Ksub = full_precision[np.ix_(selected, selected)]
        for t in range(8):
            sens = F[t, selected]
            information[0, t, j] = sens.T @ np.linalg.solve(Rsub, sens)
            information[1, t, j] = sens.T @ Ksub @ sens
    information = (information + information.swapaxes(-1, -2)) / 2
    return information, masks


def evaluate_matrices(matrices: np.ndarray) -> np.ndarray:
    """Three native criteria; only trace of inverse information is minimized."""
    chol = np.linalg.cholesky(matrices)
    trace = np.trace(matrices, axis1=-2, axis2=-1)
    logdet = 2 * np.log(np.diagonal(chol, axis1=-2, axis2=-1)).sum(axis=-1)
    inverses = np.linalg.solve(matrices, np.broadcast_to(np.eye(4), matrices.shape))
    trace_inverse = np.trace(inverses, axis1=-2, axis2=-1)
    return np.stack((trace, logdet, trace_inverse), axis=-1)


def validate_enumeration(all_schedules: tuple[Schedule, ...]) -> dict:
    expected_with_empty = sum(math.comb(3, s) * sum(
        math.comb(9 - q, q) * (3 - s)**q for q in range(5)) for s in range(4))
    assert expected_with_empty == 2348
    assert len(all_schedules) == expected_with_empty - 1
    assert len(set(all_schedules)) == len(all_schedules)
    # Independently enumerate four states per time: none, or one species.
    # This tests the global timing restriction and the count without reusing
    # the combinations-with-no-adjacency generator.
    independent = set()
    for state in product(range(-1, 3), repeat=8):
        if any(state[t] >= 0 and state[t + 1] >= 0 for t in range(7)):
            continue
        manual = tuple((t, s) for t, s in enumerate(state) if s >= 0)
        used = {s for _, s in manual}
        for static_mask in range(8):
            if any(static_mask & (1 << s) for s in used):
                continue
            if not static_mask and not manual:
                continue
            independent.add(Schedule(static_mask, manual))
    assert independent == set(all_schedules)
    return {"enumeration_with_empty": expected_with_empty,
            "nonempty_schedules": len(all_schedules),
            "independent_state_enumeration_matches": True,
            "maximum_manual_sample_count": max(len(s.manual) for s in all_schedules)}


def validate_information(F: np.ndarray, all_schedules: tuple[Schedule, ...],
                         matrices: np.ndarray) -> dict:
    """Compare all pattern sums with independent full 48-candidate calculations."""
    full_covariance = np.kron(np.eye(8), covariance())
    full_precision = np.linalg.solve(full_covariance, np.eye(48))
    full_F = F.reshape(48, 4)
    max_relative_error = 0.0
    max_criterion_error = np.zeros(3)
    max_relative_criterion_error = np.zeros(3)
    min_relative_inflation_eigenvalue = 0.0
    for i, schedule in enumerate(all_schedules):
        selected = [6*t + channel for t, mask in enumerate(schedule.time_patterns)
                    for channel in range(6) if mask & (1 << channel)]
        sens = full_F[selected]
        Rsub = full_covariance[np.ix_(selected, selected)]
        Ksub = full_precision[np.ix_(selected, selected)]
        refs = np.array([REGULARIZATION + sens.T @ np.linalg.solve(Rsub, sens),
                         REGULARIZATION + sens.T @ Ksub @ sens])
        refs = (refs + refs.swapaxes(-1, -2)) / 2
        for model in range(2):
            error = np.linalg.norm(refs[model] - matrices[model, i]) / max(
                1, np.linalg.norm(refs[model]))
            max_relative_error = max(max_relative_error, float(error))
        reference_criteria = evaluate_matrices(refs)
        discrepancies = np.abs(reference_criteria - evaluate_matrices(matrices[:, i]))
        criterion_difference = np.max(discrepancies, axis=0)
        max_criterion_error = np.maximum(max_criterion_error, criterion_difference)
        relative_discrepancies = np.max(discrepancies / np.maximum(1, np.abs(reference_criteria)), axis=0)
        max_relative_criterion_error = np.maximum(max_relative_criterion_error, relative_discrepancies)
        inflation = matrices[1, i] - matrices[0, i]
        eigenvalue = np.linalg.eigvalsh(inflation)[0] / max(1, np.linalg.norm(inflation))
        min_relative_inflation_eigenvalue = min(min_relative_inflation_eigenvalue,
                                               float(eigenvalue))
    assert max_relative_error < 1e-12, max_relative_error
    assert max_relative_criterion_error.max() < 1e-9, max_relative_criterion_error
    assert min_relative_inflation_eigenvalue > -1e-12, min_relative_inflation_eigenvalue
    return {"full_covariance_dimension": 48,
            "all_schedules_checked_under_both_formulas": len(all_schedules),
            "max_relative_information_error": max_relative_error,
            "max_absolute_criterion_error": dict(zip(CRITERIA, max_criterion_error.tolist())),
            "max_relative_criterion_error": dict(zip(CRITERIA, max_relative_criterion_error.tolist())),
            "min_relative_gating_inflation_eigenvalue": min_relative_inflation_eigenvalue}


def selected_record(index: int, all_schedules: tuple[Schedule, ...],
                    criteria: np.ndarray) -> dict:
    marginal = criteria[0, index]
    gated = criteria[1, index]
    logdet_difference = float(gated[1] - marginal[1])
    return {
        "schedule": all_schedules[index].describe(),
        "marginal_criteria": dict(zip(CRITERIA, marginal.tolist())),
        "gated_criteria": dict(zip(CRITERIA, gated.tolist())),
        "information_inflation": {
            "trace_ratio_gated_over_marginal": float(gated[0] / marginal[0]),
            "logdet_gated_minus_marginal": logdet_difference,
            "determinant_ratio_gated_over_marginal": math.exp(logdet_difference),
            "d_information_ratio_gated_over_marginal": math.exp(logdet_difference / 4),
            "inverse_trace_ratio_marginal_over_gated": float(marginal[2] / gated[2]),
        },
    }


def compare_budget(budget: int, all_schedules: tuple[Schedule, ...],
                   criteria: np.ndarray) -> dict:
    feasible = np.array([i for i, s in enumerate(all_schedules) if s.cost <= budget])
    if not len(feasible):
        raise ValueError("budget permits no nonempty schedule")
    output = {"budget": budget, "feasible_schedules": len(feasible), "criteria": {}}
    for c, name in enumerate(CRITERIA):
        direction = DIRECTIONS[c]
        marginal_utility = direction * criteria[0, feasible, c]
        gated_utility = direction * criteria[1, feasible, c]
        best_true = float(marginal_utility.max())
        best_gated = float(gated_utility.max())
        true_tolerance = TIE_TOLERANCE * max(1, abs(best_true))
        gated_tolerance = TIE_TOLERANCE * max(1, abs(best_gated))
        marginal_ties = feasible[best_true - marginal_utility <= true_tolerance]
        gated_ties = feasible[best_gated - gated_utility <= gated_tolerance]
        # Schedules are sorted by cost and then fixed integer/tuple keys.
        # This gives a deterministic representative within the stated tolerance.
        marginal_index, gated_index = int(marginal_ties[0]), int(gated_ties[0])
        marginal_scores_at_gate_ties = criteria[0, gated_ties, c]
        gate_tie_true_utility = direction * marginal_scores_at_gate_ties
        representative_true = float(criteria[0, gated_index, c])
        regret = max(0, best_true - direction * representative_true)
        record = {
            "direction": "maximize" if direction == 1 else "minimize",
            "marginal_optimum": direction * best_true,
            "gated_optimum": direction * best_gated,
            "marginal_optimal_selection": selected_record(marginal_index, all_schedules, criteria),
            "gated_optimal_selection": selected_record(gated_index, all_schedules, criteria),
            "representative_selections_differ": marginal_index != gated_index,
            "gated_selection_true_criterion": representative_true,
            "true_criterion_regret": regret,
            "marginal_numerical_optimal_count": len(marginal_ties),
            "gated_numerical_optimal_count": len(gated_ties),
            "marginal_tie_absolute_tolerance": true_tolerance,
            "gated_tie_absolute_tolerance": gated_tolerance,
            "gated_ties_true_criterion_best": direction * float(gate_tie_true_utility.max()),
            "gated_ties_true_criterion_worst": direction * float(gate_tie_true_utility.min()),
            "gated_ties_true_regret_best": max(0, best_true - float(gate_tie_true_utility.max())),
            "gated_ties_true_regret_worst": max(0, best_true - float(gate_tie_true_utility.min())),
            "gated_tie_schedules": [all_schedules[int(i)].describe() for i in gated_ties],
        }
        if c == 1:
            record["gated_selection_d_efficiency"] = math.exp(-regret / 4)
            record["gated_selection_determinant_efficiency"] = math.exp(-regret)
        else:
            native_optimum = direction * best_true
            record["relative_true_criterion_regret"] = regret / abs(native_optimum)
        output["criteria"][name] = record
    return output


def run_recheck(data_path: Path = DEFAULT_DATA) -> dict:
    started = perf_counter()
    F = load_sensitivities(data_path)
    all_schedules = schedules()
    enumeration_seconds = perf_counter() - started
    score_started = perf_counter()
    patterns, masks = pattern_information(F)
    mask_index = {mask: i for i, mask in enumerate(masks)}
    matrices = np.array([
        [REGULARIZATION + patterns[model, np.arange(8),
                          [mask_index[m] for m in schedule.time_patterns]].sum(axis=0)
         for schedule in all_schedules] for model in range(2)
    ])
    criteria = evaluate_matrices(matrices)
    results = [compare_budget(budget, all_schedules, criteria) for budget in BUDGETS]
    scoring_seconds = perf_counter() - score_started
    validation_started = perf_counter()
    checks = validate_enumeration(all_schedules)
    checks.update(validate_information(F, all_schedules, matrices))
    validation_seconds = perf_counter() - validation_started
    return {
        "metadata": {
            "source_commit": SOURCE_COMMIT, "sensitivity_url": SOURCE_URL,
            "sensitivity_sha256": SOURCE_SHA256,
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "numpy_version": np.__version__, "parameter_names": ["A1", "A2", "E1", "E2"],
            "channel_order": ["SCM-A", "SCM-B", "SCM-C", "DCM-A", "DCM-B", "DCM-C"],
            "time_minutes": TIMES, "same_time_covariance": covariance().tolist(),
            "times_independent": True, "diagonal_regularization": 1e-4,
            "scm_install_cost": 2000, "dcm_install_cost": 200, "dcm_sample_cost": 400,
            "dcm_global_minimum_interval_minutes": 10,
            "same_species_modalities_mutually_exclusive": True,
            "per_species_manual_cap": 10, "total_manual_cap": 10,
            "nonempty_selection_required": True,
            "same_time_pattern_count": len(masks),
            "numerical_tie_rule": "within 1e-9 * max(1, abs(best native objective))",
            "tie_representative": "minimum cost, then static bitmask, then manual tuple",
            "search": "exhaustive enumeration of every feasible nonempty schedule before budget filtering",
            "numerics": "floating-point objective comparisons; no exact-arithmetic or interval certificate",
            "source_trace_objective": "maximize trace information, called A-optimality in the source",
            "conventional_a_objective": "minimize trace inverse information; additional independent comparison",
            "selection_provenance": "our independently computed optima on archived Q_drop0.csv inputs; no author result files deserialized",
            "physical_provenance_limit": "archived sensitivities used verbatim; generator experiment and scaling not independently established",
        },
        "validation": checks,
        "timing_seconds": {"input_and_enumeration": enumeration_seconds,
                           "pattern_scoring_and_all_budget_comparisons": scoring_seconds,
                           "independent_validation": validation_seconds,
                           "total": perf_counter() - started},
        "results": results,
    }


def write_summary(result: dict, path: Path) -> None:
    rows = []
    for budget in result["results"]:
        for criterion, comparison in budget["criteria"].items():
            rows.append({
                "budget": budget["budget"], "criterion": criterion,
                "feasible_schedules": budget["feasible_schedules"],
                "marginal_optimum": comparison["marginal_optimum"],
                "gated_optimum": comparison["gated_optimum"],
                "gated_selection_true_criterion": comparison["gated_selection_true_criterion"],
                "true_criterion_regret": comparison["true_criterion_regret"],
                "best_true_regret_among_gated_ties": comparison["gated_ties_true_regret_best"],
                "worst_true_regret_among_gated_ties": comparison["gated_ties_true_regret_worst"],
                "selections_differ": comparison["representative_selections_differ"],
                "marginal_numerical_optimal_count": comparison["marginal_numerical_optimal_count"],
                "gated_numerical_optimal_count": comparison["gated_numerical_optimal_count"],
                "marginal_selection": json.dumps(comparison["marginal_optimal_selection"]["schedule"], sort_keys=True),
                "gated_selection": json.dumps(comparison["gated_optimal_selection"]["schedule"], sort_keys=True),
            })
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()
    result = run_recheck(args.data)
    serialized = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(serialized)
    else:
        print(serialized, end="")
    if args.summary:
        write_summary(result, args.summary)


if __name__ == "__main__":
    main()
