"""Lower-bound every admissible scalar-split Liu relaxation optimum.

This separate module evaluates a feasible point at a certified upper bound on
lambda_min(R). It uses virtual-noise monotonicity, NOT a tangent at that split.
No reviewed core is modified. Exact filtering handles heterogeneous virtual
noise and zero selection weights without a dense covariance inverse.
"""

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
from time import perf_counter

from certify_dense_design import Problem, scaled_precision
from certify_noisy_markov import fraction, log_enclosure, rational, require_spd


def nonpositive_pivot(diagonal, offdiagonal):
    """Return an exact leading-principal-minor witness that a matrix is not SPD."""
    diagonal, offdiagonal = tuple(map(rational, diagonal)), tuple(map(rational, offdiagonal))
    if not diagonal or len(offdiagonal) != len(diagonal)-1:
        raise ValueError("Invalid tridiagonal dimensions")
    prefix = []
    for i, entry in enumerate(diagonal):
        pivot = entry if i == 0 else entry-offdiagonal[i-1]**2/prefix[-1]
        if pivot <= 0:
            return {"failed_index": i, "positive_prefix_pivots": tuple(prefix),
                    "nonpositive_pivot": pivot}
        prefix.append(pivot)
    return None


def spectral_upper_witness(problem, upper_split):
    upper_split = rational(upper_split)
    if upper_split <= 0:
        raise ValueError("A positive upper split is required")
    if problem.latent == 0:
        diagonal = (problem.nugget-upper_split,)*problem.n
        offdiagonal = (Q(0),)*(problem.n-1)
    else:
        diagonal, offdiagonal, scale = scaled_precision(problem)
        shift = problem.nugget-upper_split
        diagonal = tuple(scale+shift*x for x in diagonal)
        offdiagonal = tuple(shift*x for x in offdiagonal)
    witness = nonpositive_pivot(diagonal, offdiagonal)
    if witness is None:
        raise ValueError("Proposed upper split is below lambda_min(R)")
    return witness


def choose_upper_split(problem, approximate, grid=10**12):
    if isinstance(grid, bool) or not isinstance(grid, int) or grid < 1:
        raise ValueError("Positive integer upper-split grid required")
    approximate = rational(approximate)
    if approximate <= 0:
        raise ValueError("A positive spectral proposal is required")
    scaled = approximate*grid
    candidate = Q(-((-scaled.numerator)//scaled.denominator), grid)
    for attempt in range(20):
        try:
            witness = spectral_upper_witness(problem, candidate)
            return candidate, witness, attempt
        except ValueError:
            candidate += Q(2**attempt, grid)
    raise ValueError("No spectral upper witness found near the proposal")


def virtual_information(problem, z, split):
    """Exact F^T(R+split*diag((1-z)/z))^-1 F on positive-weight rows.

    This value exists for every positive split. It is used only as a point
    value; a split above lambda_min(R) cannot justify Liu concave tangents.
    """
    z, split = tuple(map(rational, z)), rational(split)
    if split <= 0 or len(z) != problem.n or any(x < 0 or x > 1 for x in z):
        raise ValueError("Positive split and a point in [0,1]^n are required")
    information = [list(row) for row in problem.prior]
    posterior = problem.latent
    sensitivity = [Q(0)]*problem.p
    previous = None
    for t, weight in enumerate(z):
        if weight == 0:
            continue
        transition = Q(1) if previous is None else problem.rho**(t-previous)
        prediction = (problem.latent if previous is None else
                      transition**2*posterior+problem.latent*(1-transition**2))
        predicted = [transition*x for x in sensitivity]
        adjusted = [x-y for x, y in zip(problem.F[t], predicted)]
        noise = problem.nugget+split*(1-weight)/weight
        variance = prediction+noise
        for i in range(problem.p):
            for j in range(problem.p):
                information[i][j] += adjusted[i]*adjusted[j]/variance
        gain = prediction/variance
        sensitivity = [x+gain*y for x, y in zip(predicted, adjusted)]
        posterior = prediction*noise/variance
        previous = t
    result = tuple(tuple(row) for row in information)
    require_spd(result)
    return result


def certify(problem, z, upper_split):
    started = perf_counter()
    z, upper_split = tuple(map(rational, z)), rational(upper_split)
    if (len(z) != problem.n or any(x < 0 or x > 1 for x in z)
            or sum(z, Q(0)) != problem.k):
        raise ValueError("The all-splits point must be exactly cardinality feasible")
    witness = spectral_upper_witness(problem, upper_split)
    information = virtual_information(problem, z, upper_split)
    determinant = fraction(require_spd(information).det())
    bounds = log_enclosure(determinant)
    return {"status": "certified lower bound on every admissible split relaxation optimum",
            "upper_split": upper_split, "spectral_upper_witness": witness,
            "feasible_point": z, "information_at_upper_split": information,
            "information_determinant": determinant,
            "all_splits_lower_bound": bounds[0], "point_value_upper_bound": bounds[1],
            "display_all_splits_lower_bound": float(bounds[0]),
            "exact_certificate_seconds": perf_counter()-started,
            "scope": "All scalar splits 0<a<lambda_min(R); no upper tangent at upper_split"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dense_certificates", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--memory-dir", type=Path)
    args = parser.parse_args()
    sys.set_int_max_str_digits(0)
    source = json.loads(args.dense_certificates.read_text(), parse_float=str)
    results = []
    report = {"source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "dense_certificate_sha256": hashlib.sha256(args.dense_certificates.read_bytes()).hexdigest(),
              "results": results}
    for record in source["results"]:
        started = perf_counter()
        problem = Problem.read(record["problem_data"])
        # This is merely a nearby proposal, not a trusted eigenvalue assertion.
        upper_split, _, adjustments = choose_upper_split(problem, Q(record["a"])*Q(100, 99))
        certificate = certify(problem, record["tangent_z"], upper_split)
        certificate.update({"case": record["case"], "n": problem.n, "p": problem.p,
                            "k": problem.k, "seed": record.get("seed"),
                            "problem_data": record["problem_data"],
                            "spectral_proposal_adjustments": adjustments})
        if args.memory_dir is not None:
            path = args.memory_dir/f"noisy-markov-extended-certificate-{record['case']}.json"
            memory = json.loads(path.read_text(), parse_float=str)
            if memory.get("status") != "certified" or Problem.read(memory["problem_data"]) != problem:
                raise ValueError("Memory certificate status or exact problem data mismatch")
            memory_upper = rational(memory["upper_bound"])
            difference = certificate["all_splits_lower_bound"]-memory_upper
            certificate.update({"memory_certificate": path.name,
                                "memory_certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                "memory_L": memory["L"], "memory_upper_bound": memory_upper,
                                "all_splits_separation": difference,
                                "display_all_splits_separation": float(difference)})
        certificate["total_case_seconds"] = perf_counter()-started
        results.append(certificate)
        print(json.dumps({key: certificate[key] for key in
                          ("case", "n", "display_all_splits_lower_bound", "total_case_seconds")}
                         | {"display_all_splits_separation": certificate.get("display_all_splits_separation")}),
              flush=True)
    args.output.write_text(json.dumps(report, default=str, indent=2)+"\n")


if __name__ == "__main__":
    main()
