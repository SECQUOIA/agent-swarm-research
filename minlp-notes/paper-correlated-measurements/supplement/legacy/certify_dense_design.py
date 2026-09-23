"""Exact tangent upper bounds for the Liu continuous selection relaxation.

JSON decimal input defines rational model data. Numerical optimization proposes
a tangent point; rational arithmetic verifies the split and recomputes the
information, gradient, cardinality price, and logarithm bounds independently.
This isolated comparator does not modify the reviewed floating-point core.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import sys
from time import perf_counter

import numpy as np
from scipy.optimize import minimize

from certify_noisy_markov import (
    fraction, log_enclosure, matrix, rational, require_spd, sympy_matrix,
    true_information,
)
from noisy_markov_design import NoisyDesign
from structured_dense_oracle import StructuredLiuOracle


@dataclass(frozen=True)
class Problem:
    F: tuple
    prior: tuple
    rho: Q
    latent: Q
    nugget: Q
    k: int

    @property
    def n(self):
        return len(self.F)

    @property
    def p(self):
        return len(self.prior)

    @classmethod
    def read(cls, record):
        F, prior = matrix(record["F"]), matrix(record["prior"])
        require_spd(prior)
        rho, latent, nugget = map(rational, (
            record["rho"], record["latent_variance"], record["nugget_variance"]))
        k = record["k"]
        if (any(len(row) != len(prior) for row in F)
                or abs(rho) >= 1 or latent < 0 or nugget <= 0
                or isinstance(k, bool) or not isinstance(k, int) or not 0 <= k <= len(F)):
            raise ValueError("Invalid dimensions, covariance, or cardinality")
        return cls(F, prior, rho, latent, nugget, k)

    def numerical(self):
        return NoisyDesign(np.array(self.F, dtype=float), float(self.rho),
                           float(self.latent), float(self.nugget),
                           np.array(self.prior, dtype=float), self.k)


def tridiagonal_ldl(diagonal, offdiagonal):
    """Exact SPD test and LDL factor; raises at the first nonpositive pivot."""
    diagonal, offdiagonal = tuple(map(rational, diagonal)), tuple(map(rational, offdiagonal))
    if not diagonal or len(offdiagonal) != len(diagonal)-1:
        raise ValueError("Invalid tridiagonal dimensions")
    pivots, multipliers = [], []
    for i, value in enumerate(diagonal):
        if i:
            multiplier = offdiagonal[i-1]/pivots[-1]
            multipliers.append(multiplier)
            value -= multiplier*offdiagonal[i-1]
        if value <= 0:
            raise ValueError(f"Tridiagonal matrix is not SPD: pivot {i}")
        pivots.append(value)
    return tuple(pivots), tuple(multipliers)


def tridiagonal_solve(factor, rhs):
    pivots, multipliers = factor
    rhs = matrix(rhs)
    if len(rhs) != len(pivots):
        raise ValueError("Tridiagonal RHS dimension mismatch")
    forward = [list(row) for row in rhs]
    for i in range(1, len(pivots)):
        forward[i] = [x-multipliers[i-1]*y for x, y in zip(forward[i], forward[i-1])]
    solution = [None]*len(pivots)
    for i in range(len(pivots)-1, -1, -1):
        row = [value/pivots[i] for value in forward[i]]
        if i+1 < len(pivots):
            row = [x-multipliers[i]*y for x, y in zip(row, solution[i+1])]
        solution[i] = tuple(row)
    return tuple(solution)


def scaled_precision(problem):
    if problem.latent <= 0:
        raise ValueError("Positive latent variance required for its precision")
    if problem.n == 1:
        return (Q(1),), (), problem.latent
    rho = problem.rho
    diagonal = (Q(1),)+(1+rho*rho,)*(problem.n-2)+(Q(1),)
    return diagonal, (-rho,)*(problem.n-1), problem.latent*(1-rho*rho)


def verify_split(problem, a):
    a = rational(a)
    if a <= 0:
        raise ValueError("The covariance split must be positive")
    if problem.latent == 0:
        return tridiagonal_ldl((problem.nugget-a,)*problem.n, (Q(0),)*(problem.n-1))
    diagonal, offdiagonal, scale = scaled_precision(problem)
    shift = problem.nugget-a
    return tridiagonal_ldl(tuple(scale+shift*x for x in diagonal),
                           tuple(shift*x for x in offdiagonal))


def choose_split(problem, grid=10**12):
    if isinstance(grid, bool) or not isinstance(grid, int) or grid < 1:
        raise ValueError("Positive integer split grid required")
    proposal = StructuredLiuOracle(problem.numerical(), .99).a
    scaled = Q(str(proposal))*grid
    a = Q(scaled.numerator//scaled.denominator, grid)
    verify_split(problem, a)
    return a


def exact_oracle(problem, z, a):
    z, a = tuple(map(rational, z)), rational(a)
    if len(z) != problem.n or any(value < 0 or value > 1 for value in z):
        raise ValueError("Tangent coordinates must be in [0,1]")
    split_factor = verify_split(problem, a)
    F, n, p = problem.F, problem.n, problem.p
    if problem.latent == 0 or problem.rho == 0 or n == 1:
        variance = problem.latent+problem.nugget
        denominators = tuple(a*(1-value)+variance*value for value in z)
        V = tuple(tuple(a*x/t for x in row) for row, t in zip(F, denominators))
        weighted = tuple(tuple(value*x/t for x in row)
                         for row, value, t in zip(F, z, denominators))
    else:
        diagonal, offdiagonal, scale = scaled_precision(problem)
        denominators = tuple(a*(1-value)+problem.nugget*value for value in z)
        hdiag = tuple(q+scale*value/t for q, value, t in zip(diagonal, z, denominators))
        rhs = []
        for i in range(n):
            rhs.append(tuple(diagonal[i]*F[i][j]
                             +(offdiagonal[i-1]*F[i-1][j] if i else 0)
                             +(offdiagonal[i]*F[i+1][j] if i+1 < n else 0)
                             for j in range(p)))
        U = tridiagonal_solve(tridiagonal_ldl(hdiag, offdiagonal), rhs)
        V = tuple(tuple(a*x/t for x in row) for row, t in zip(U, denominators))
        weighted = tuple(tuple(value*x/t for x in row)
                         for row, value, t in zip(U, z, denominators))
    information = tuple(tuple(problem.prior[i][j]
                              +sum((F[t][i]*weighted[t][j] for t in range(n)), Q(0))
                              for j in range(p)) for i in range(p))
    exact_J = require_spd(information)
    inverse = exact_J.inv()
    inverse = tuple(tuple(fraction(inverse[i, j]) for j in range(p)) for i in range(p))
    gradient = tuple(sum((row[i]*inverse[i][j]*row[j]
                         for i in range(p) for j in range(p)), Q(0))/a for row in V)
    if any(value < 0 for value in gradient):
        raise ArithmeticError("A Liu selection gradient cannot be negative")
    return information, gradient, fraction(exact_J.det()), split_factor[0]


def round_feasible(point, k, grid=10**8):
    """Round an approximate capped-simplex point to an exact cardinality point."""
    if isinstance(grid, bool) or not isinstance(grid, int) or grid < 1:
        raise ValueError("Positive integer point grid required")
    values = [min(Q(1), max(Q(0), rational(value))) for value in point]
    if isinstance(k, bool) or not isinstance(k, int) or not 0 <= k <= len(values):
        raise ValueError("Invalid point cardinality")
    scaled = [value*grid for value in values]
    counts = [value.numerator//value.denominator for value in scaled]
    deficit = k*grid-sum(counts)
    if deficit > 0:
        order = sorted(range(len(values)), key=lambda i: scaled[i]-counts[i], reverse=True)
        # First preserve the usual largest-remainder rounding near a feasible input.
        for i in order:
            if deficit and counts[i] < grid:
                counts[i] += 1
                deficit -= 1
        for i in order:
            added = min(deficit, grid-counts[i])
            counts[i] += added
            deficit -= added
    elif deficit < 0:
        for i in sorted(range(len(values)), key=lambda i: scaled[i]-counts[i]):
            removed = min(-deficit, counts[i])
            counts[i] -= removed
            deficit += removed
    assert deficit == 0 and sum(counts) == k*grid
    return tuple(Q(value, grid) for value in counts)


def numerical_tangent(problem, a, point_grid=10**8):
    if problem.k in (0, problem.n):
        z = (Q(problem.k//problem.n),)*problem.n
        return z, {"method": "trivial cardinality endpoint", "success": True, "iterations": 0}
    oracle = StructuredLiuOracle(problem.numerical(), .99, a=float(a))
    def objective(z):
        value, gradient = oracle.value_gradient(z)
        return -value, -gradient
    result = minimize(objective, np.full(problem.n, problem.k/problem.n), jac=True,
                      method="SLSQP", bounds=[(0., 1.)]*problem.n,
                      constraints={"type": "eq", "fun": lambda z: z.sum()-problem.k,
                                   "jac": lambda z: np.ones(problem.n)},
                      options={"maxiter": 1000, "ftol": 1e-13})
    if not np.isfinite(result.x).all():
        raise ArithmeticError("Numerical tangent proposal is nonfinite")
    z = round_feasible(tuple(str(value) for value in result.x), problem.k, point_grid)
    value, gradient = oracle.value_gradient(np.array(z, dtype=float))
    return z, {"method": "SLSQP on capped simplex; exact feasibility after rounding",
               "success": bool(result.success), "message": str(result.message),
               "iterations": int(result.nit), "evaluations": int(result.nfev),
               "numerical_value": value,
               "numerical_tangent_gap": float(np.sort(gradient)[-problem.k:].sum()
                                               -gradient@np.array(z, dtype=float)),
               "point_grid": point_grid}


def incumbent_candidates(record, problem):
    candidates = {}
    sources = [(key, value) for key, value in record.items()
               if key.startswith("dense") and isinstance(value, dict)]
    sources += [(f"hull_L{hull['L']}", hull) for hull in record.get("hulls", [])]
    for source, value in sources:
        selected = tuple(value.get("selected", ()))
        if (len(selected) != problem.k or len(set(selected)) != len(selected)
                or any(isinstance(i, bool) or not isinstance(i, int)
                       or not 0 <= i < problem.n for i in selected)):
            raise ValueError(f"Invalid saved incumbent in {source}")
        candidates.setdefault(tuple(sorted(selected)), []).append(source)
    if not candidates:
        raise ValueError("No saved feasible incumbent found")
    return candidates


def certify(problem, z, a, candidates):
    started = perf_counter()
    z, a = tuple(map(rational, z)), rational(a)
    information, gradient, determinant, split_pivots = exact_oracle(problem, z, a)
    priced = tuple(sorted(sorted(range(problem.n), key=lambda i: gradient[i],
                                reverse=True)[:problem.k]))
    tangent_gap = sum((gradient[i] for i in priced), Q(0)) -sum(
        (g*value for g, value in zip(gradient, z)), Q(0))
    logdet = log_enclosure(determinant)
    upper = logdet[1]+tangent_gap
    continuous_lower = logdet[0] if sum(z, Q(0)) == problem.k else None
    if continuous_lower is not None and tangent_gap < 0:
        raise ArithmeticError("Negative exact tangent gap at a feasible point")
    tangent_seconds = perf_counter()-started
    incumbent_start = perf_counter()
    best = None
    for selected, sources in candidates.items():
        if (len(selected) != problem.k or len(set(selected)) != len(selected)
                or any(isinstance(i, bool) or not isinstance(i, int)
                       or not 0 <= i < problem.n for i in selected)):
            raise ValueError("Incumbent must be a cardinality-k subset")
        selected = tuple(sorted(selected))
        J = true_information(problem.F, problem.prior, selected, problem.rho,
                             problem.latent, problem.nugget)
        detJ = fraction(require_spd(J).det())
        if best is None or detJ > best[0]:
            best = detJ, selected, sources
    if best is None:
        raise ValueError("At least one feasible incumbent is required")
    incumbent_log = log_enclosure(best[0])
    lower = incumbent_log[0]
    if upper < lower:
        raise ArithmeticError("Certified upper bound is below incumbent lower bound")
    return {"status": "certified", "a": a, "tangent_z": z,
            "split_ldl_pivots": split_pivots, "information": information,
            "information_determinant": determinant, "gradient": gradient,
            "priced_selection": priced, "tangent_gap": tangent_gap,
            "tangent_logdet_lower": logdet[0], "tangent_logdet_upper": logdet[1],
            "upper_bound": upper, "continuous_lower_bound": continuous_lower,
            "continuous_certificate_gap": (None if continuous_lower is None
                                           else upper-continuous_lower),
            "incumbent_selection": best[1], "incumbent_sources": best[2],
            "incumbent_determinant": best[0], "incumbent_lower_bound": lower,
            "incumbent_upper_bound": incumbent_log[1], "gap_to_incumbent": upper-lower,
            "display_upper_bound": float(upper),
            "display_continuous_lower_bound": (None if continuous_lower is None
                                               else float(continuous_lower)),
            "display_continuous_certificate_gap": (None if continuous_lower is None
                                                   else float(upper-continuous_lower)),
            "display_incumbent_lower_bound": float(lower),
            "display_gap_to_incumbent": float(upper-lower),
            "exact_tangent_seconds": tangent_seconds,
            "exact_incumbent_seconds": perf_counter()-incumbent_start}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--case", type=int, action="append")
    parser.add_argument("--point-grid", type=int, default=10**8)
    args = parser.parse_args()
    sys.set_int_max_str_digits(0)  # Exact certificate fractions can exceed 4300 digits.
    threads = {key: os.environ.get(key) for key in
               ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")}
    if any(value != "1" for value in threads.values()):
        raise RuntimeError("Set OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1")
    source = json.loads(args.input.read_text(), parse_float=str)
    chosen = list(range(len(source["results"]))) if args.case is None else args.case
    results = []
    report = {"input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "thread_environment": threads,
              "input_interpretation": "JSON decimal input is exact rational model data",
              "results": results}
    for index in chosen:
        started = perf_counter()
        record = source["results"][index]
        problem = Problem.read(record)
        split_start = perf_counter()
        a = choose_split(problem)
        split_seconds = perf_counter()-split_start
        numerical_start = perf_counter()
        z, optimization = numerical_tangent(problem, a, args.point_grid)
        numerical_seconds = perf_counter()-numerical_start
        certificate = certify(problem, z, a, incumbent_candidates(record, problem))
        certificate.update({"case": index, "n": problem.n, "p": problem.p, "k": problem.k,
                            "seed": record.get("seed"), "rho": problem.rho,
                            "problem_data": {"F": problem.F, "prior": problem.prior,
                                             "rho": problem.rho, "latent_variance": problem.latent,
                                             "nugget_variance": problem.nugget, "k": problem.k},
                            "numerical_optimization": optimization,
                            "split_seconds": split_seconds,
                            "numerical_tangent_seconds": numerical_seconds,
                            "total_case_seconds": perf_counter()-started})
        results.append(certificate)
        args.output.write_text(json.dumps(report, default=str, indent=2)+"\n")
        print(json.dumps({key: certificate[key] for key in
                          ("case", "n", "display_upper_bound", "display_continuous_certificate_gap",
                           "display_gap_to_incumbent", "split_seconds", "numerical_tangent_seconds",
                           "exact_tangent_seconds", "exact_incumbent_seconds", "total_case_seconds")} ),
              flush=True)


if __name__ == "__main__":
    main()
