"""Exact fixed-schedule comparisons using saved robust reference certificates.

The input certificate must separately pass its independent verifier. This
comparison recomputes the nominal schedule's information from exact model data.
"""

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

from certify_noisy_markov import fraction, log_enclosure, require_spd, true_information
from certify_robust_design import outward, scenario_data


def compare(record, certificate):
    n, p, k = certificate["n"], certificate["p"], certificate["k"]
    data = [scenario_data(s, n, p, k) for s in record["scenarios"]]
    saved = [scenario_data(s, n, p, k) for s in certificate["problem_data"]]
    if data != saved or record["k"] != k:
        raise ValueError("numerical record and certificate specify different models")
    nominal = tuple(record["evaluations"]["nominal_central"]["selected"])
    if (len(nominal) != k or len(set(nominal)) != k
            or any(isinstance(t, bool) or not isinstance(t, int) or not 0 <= t < n for t in nominal)):
        raise ValueError("nominal schedule is not feasible")
    nominal = tuple(sorted(nominal))
    grid = certificate["log_grid"]
    intervals = []
    for F, prior, rho, latent, nugget in data:
        J = true_information(F, prior, nominal, rho, latent, nugget)
        low, high = log_enclosure(fraction(require_spd(J).det()))
        intervals.append((outward(low, grid), outward(high, grid, True)))
    ell = tuple(map(Q, certificate["individual_optimum_lower_bounds"]))
    upper_individual = tuple(map(Q, certificate["individual_optimum_upper_bounds"]))
    if len(ell) != len(data) or len(upper_individual) != len(data):
        raise ValueError("reference bound dimensions differ")
    nominal_lower = min(x[0]-u for x, u in zip(intervals, upper_individual))
    nominal_upper = min(x[1]-l for x, l in zip(intervals, ell))
    selected_lower = Q(certificate["standardized"]["lower_bound"])
    selected_intervals = certificate["selected_logdet_intervals"]
    selected_upper = min(Q(x[1])-l for x, l in zip(selected_intervals, ell))
    margin = selected_lower-nominal_upper
    return {"n": n, "p": p, "k": k, "nominal_selected": nominal,
            "certified_selected": certificate["selected"],
            "nominal_logdet_intervals": intervals,
            "nominal_standardized_interval": (nominal_lower, nominal_upper),
            "selected_standardized_interval": (selected_lower, selected_upper),
            "strict_improvement_proved": margin > 0,
            "log_efficiency_ratio_lower_bound": margin/p,
            "ratio_interpretation": "selected efficiency / nominal efficiency >= exp(log_efficiency_ratio_lower_bound)",
            "display_nominal_interval": [float(nominal_lower), float(nominal_upper)],
            "display_selected_interval": [float(selected_lower), float(selected_upper)],
            "display_log_efficiency_ratio_lower_bound": float(margin/p),
            "scope": "conditional on the separately verified input certificate; exact rational decimal model"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    record = json.loads(args.input.read_text(), parse_float=str)
    certificate = json.loads(args.certificate.read_text(), parse_float=str)
    result = compare(record, certificate)
    result["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["input_sha256"] = hashlib.sha256(args.input.read_bytes()).hexdigest()
    result["certificate_sha256"] = hashlib.sha256(args.certificate.read_bytes()).hexdigest()
    args.output.write_text(json.dumps(result, default=str, indent=2)+"\n")
    print(json.dumps({k: result[k] for k in (
        "n", "strict_improvement_proved", "display_nominal_interval",
        "display_selected_interval", "display_log_efficiency_ratio_lower_bound")}))


if __name__ == "__main__":
    main()
