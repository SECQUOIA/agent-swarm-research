"""Exact lower bounds for every diagonal-split continuous relaxation.

A numerical tangent reference and SDP-dual matrix only propose witnesses.
All point/gradient arithmetic, PSD factor construction, diagonal domination,
and bound comparisons below are rational. No SDP solver status is trusted.
"""

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
from time import perf_counter

import numpy as np

from certify_dense_design import Problem, scaled_precision, tridiagonal_ldl, tridiagonal_solve
from certify_noisy_markov import fraction, log_enclosure, rational, require_spd


def exact_diagonal_point(problem, z, a):
    z, a = tuple(map(rational, z)), tuple(map(rational, a))
    n, p = problem.n, problem.p
    if (len(z) != n or len(a) != n or any(x < 0 or x > 1 for x in z)
            or any(x <= 0 for x in a)):
        raise ValueError("Require a point in [0,1]^n and a positive diagonal reference")
    denominators = tuple(ai*(1-zi)+problem.nugget*zi for ai, zi in zip(a, z))
    if problem.latent == 0 or problem.rho == 0 or n == 1:
        denominators = tuple(ai*(1-zi)+(problem.latent+problem.nugget)*zi
                             for ai, zi in zip(a, z))
        U = problem.F
    else:
        diagonal, offdiagonal, scale = scaled_precision(problem)
        hdiag = tuple(q+scale*zi/ti for q, zi, ti in zip(diagonal, z, denominators))
        rhs = tuple(tuple(diagonal[i]*problem.F[i][j]
                          +(offdiagonal[i-1]*problem.F[i-1][j] if i else 0)
                          +(offdiagonal[i]*problem.F[i+1][j] if i+1 < n else 0)
                          for j in range(p)) for i in range(n))
        U = tridiagonal_solve(tridiagonal_ldl(hdiag, offdiagonal), rhs)
    information = tuple(tuple(problem.prior[i][j]
                              +sum((problem.F[t][i]*z[t]*U[t][j]/denominators[t]
                                    for t in range(n)), Q(0))
                              for j in range(p)) for i in range(p))
    exact_J = require_spd(information)
    inverse = exact_J.inv()
    gradient = tuple(-zi*(1-zi)/ti**2
                     *sum((row[i]*fraction(inverse[i, j])*row[j]
                           for i in range(p) for j in range(p)), Q(0))
                     for zi, ti, row in zip(z, denominators, U))
    if any(x > 0 for x in gradient):
        raise ArithmeticError("A diagonal-noise gradient cannot be positive")
    return information, gradient, fraction(exact_J.det())


def psd_dual_certificate(problem, gradient, approximate_Y, grid=10**8):
    if isinstance(grid, bool) or not isinstance(grid, int) or grid < 1:
        raise ValueError("A positive integer factor grid is required")
    n = problem.n
    Y = np.asarray(approximate_Y, dtype=float)
    if Y.shape != (n, n) or not np.isfinite(Y).all():
        raise ValueError("A finite square numerical dual proposal is required")
    values, vectors = np.linalg.eigh((Y+Y.T)/2)
    approximate_B = vectors*np.sqrt(np.maximum(values, 0))
    # Every returned rational B defines BB^T PSD, irrespective of eigensolver error.
    B = tuple(tuple(Q(round(float(x)*grid), grid) for x in row) for row in approximate_B)
    w = tuple(-rational(x) for x in gradient)
    if len(w) != n or any(x < 0 for x in w):
        raise ValueError("Nonnegative diagonal requirements are needed")
    correction = tuple(max(Q(0), wi-sum((x*x for x in row), Q(0))) for wi, row in zip(w, B))
    covariance = tuple(tuple(problem.latent*problem.rho**abs(i-j)
                             +(problem.nugget if i == j else 0)
                             for j in range(n)) for i in range(n))
    trace = sum((covariance[i][j]*sum((B[i][k]*B[j][k] for k in range(n)), Q(0))
                 for i in range(n) for j in range(n)), Q(0))
    trace += sum((covariance[i][i]*correction[i] for i in range(n)), Q(0))
    return {"factor": B, "diagonal_correction": correction, "trace_RY": trace,
            "factor_grid": grid,
            "construction": "Y=BB^T+diag(c), c_i=max(0,-g_i-sum_j B_ij^2)"}


def certify(problem, z, a, Y, factor_grid=10**8):
    started = perf_counter()
    z, a = tuple(map(rational, z)), tuple(map(rational, a))
    if sum(z, Q(0)) != problem.k:
        raise ValueError("The fixed selection point must be exactly cardinality feasible")
    information, gradient, determinant = exact_diagonal_point(problem, z, a)
    lower_log, upper_log = log_enclosure(determinant)
    dual = psd_dual_certificate(problem, gradient, Y, factor_grid)
    constant = -sum((gi*ai for gi, ai in zip(gradient, a)), Q(0))-dual["trace_RY"]
    lower = lower_log+constant
    return {"status": "certified lower bound for every positive diagonal split with R-diag(a) PSD",
            "selection_point": z, "reference_diagonal": a,
            "reference_information": information, "reference_determinant": determinant,
            "gradient": gradient, "dual_certificate": dual,
            "reference_logdet_lower": lower_log, "reference_logdet_upper": upper_log,
            "all_diagonal_lower_bound": lower, "display_all_diagonal_lower_bound": float(lower),
            "seconds": perf_counter()-started}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("probe", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--reference-grid", type=int, default=10**8)
    parser.add_argument("--factor-grid", type=int, default=10**8)
    args = parser.parse_args()
    if args.reference_grid < 1:
        raise ValueError("A positive reference grid is required")
    sys.set_int_max_str_digits(0)
    source = json.loads(args.probe.read_text())
    problem = Problem.read(source["problem_data"])
    numerical = source["benchmark"]
    a = tuple(Q(max(1, round(float(x)*args.reference_grid)), args.reference_grid)
              for x in numerical["a"])
    result = certify(problem, source["z"], a, numerical["Y"], args.factor_grid)
    memory_path = Path(source["memory_source"])
    memory = json.loads(memory_path.read_text())
    if memory["status"] != "certified" or Problem.read(memory["problem_data"]) != problem:
        raise ValueError("Exact memory certificate problem or status mismatch")
    difference = result["all_diagonal_lower_bound"]-rational(memory["upper_bound"])
    result.update({"problem_data": source["problem_data"],
                   "memory_upper_bound": rational(memory["upper_bound"]),
                   "separation": difference, "display_separation": float(difference),
                   "memory_source": str(memory_path),
                   "memory_sha256": hashlib.sha256(memory_path.read_bytes()).hexdigest(),
                   "probe_source": str(args.probe),
                   "probe_sha256": hashlib.sha256(args.probe.read_bytes()).hexdigest(),
                   "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    args.output.write_text(json.dumps(result, default=str, indent=2)+"\n")
    print(json.dumps({key: result[key] for key in
                      ("status", "display_all_diagonal_lower_bound", "display_separation", "seconds")}))


if __name__ == "__main__":
    main()
