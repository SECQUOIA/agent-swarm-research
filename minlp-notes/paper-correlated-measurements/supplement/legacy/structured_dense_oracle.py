"""Structured evaluation of the existing Liu selection relaxation.

This is an isolated comparison prototype, not a new relaxation. Its tridiagonal
solve is ordinary latent-precision algebra. Floating-point values and gradients
are not certified tangents. Run with BLAS/OpenMP threads set to one.
"""

from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
import math
import os
from pathlib import Path
import platform
from statistics import median
from time import perf_counter

import numpy as np
import scipy
from scipy.linalg import eigvalsh_tridiagonal, solveh_banded

from noisy_markov_design import DenseLiuOracle, NoisyDesign, generic_design, logdet


class StructuredLiuOracle:
    """Same objective and gradient as DenseLiuOracle, without dense n-by-n data.

    ``a`` optionally fixes the same covariance split as a comparator. Otherwise
    a selected tridiagonal eigenvalue computes the default split numerically.
    The class checks the numerical split condition, not an exact certificate.
    """

    def __init__(self, design: NoisyDesign, split_fraction: float = 0.5,
                 *, a: float | None = None):
        if not math.isfinite(split_fraction) or not 0 < split_fraction < 1:
            raise ValueError("split_fraction must lie strictly between zero and one")
        self.design = design
        n, rho, s, r = (design.n, design.rho, design.latent_variance,
                        design.nugget_variance)
        self.diagonal_variance = s + r if s == 0 or rho == 0 or n == 1 else None
        if self.diagonal_variance is not None:
            self.minimum_covariance_eigenvalue = self.diagonal_variance
            self.precision_scale = None
            self.precision_diagonal = None
            self.precision_offdiagonal = None
            self.precision_F = None
        else:
            # M = s*(1-rho^2)*Q avoids division by a small latent variance.
            self.precision_scale = s * (1 - rho * rho)
            diagonal = np.full(n, 1 + rho * rho)
            diagonal[0] = diagonal[-1] = 1
            offdiagonal = np.full(n - 1, -rho)
            largest = float(eigvalsh_tridiagonal(
                diagonal, offdiagonal, select="i", select_range=(n-1, n-1),
                check_finite=False)[0])
            self.minimum_covariance_eigenvalue = r + self.precision_scale / largest
            self.precision_diagonal = diagonal
            self.precision_offdiagonal = offdiagonal
            rhs = diagonal[:, None] * design.F
            rhs[:-1] += offdiagonal[:, None] * design.F[1:]
            rhs[1:] += offdiagonal[:, None] * design.F[:-1]
            self.precision_F = rhs
        self.a = (split_fraction * self.minimum_covariance_eigenvalue
                  if a is None else float(a))
        if (not math.isfinite(self.a)
                or not 0 < self.a < self.minimum_covariance_eigenvalue):
            raise ValueError("Require a finite split 0 < a < lambda_min(R)")

    def value_gradient(self, z: np.ndarray) -> tuple[float, np.ndarray]:
        z = np.asarray(z, dtype=float)
        if (z.shape != (self.design.n,) or not np.isfinite(z).all()
                or np.any(z < 0) or np.any(z > 1)):
            raise ValueError("z must be a finite n-vector in [0,1]")
        if not np.any(z):
            # Avoid solving M U=M F at the boundary where V=F exactly.
            V = self.design.F
            weighted_V = np.zeros_like(V)
        elif self.diagonal_variance is not None:
            denominator = self.a * (1-z) + self.diagonal_variance * z
            V = (self.a / denominator)[:, None] * self.design.F
            weighted_V = (z / denominator)[:, None] * self.design.F
        else:
            # t_i = a*w_i is evaluated as a positive sum to avoid cancellation.
            t = self.a * (1-z) + self.design.nugget_variance * z
            band = np.zeros((2, self.design.n))
            band[0] = self.precision_diagonal + self.precision_scale * (z / t)
            band[1, :-1] = self.precision_offdiagonal
            U = solveh_banded(band, self.precision_F, lower=True,
                             overwrite_ab=True, check_finite=False)
            V = (self.a / t)[:, None] * U
            weighted_V = (z / t)[:, None] * U
        J = self.design.prior + self.design.F.T @ weighted_V
        J = (J + J.T) / 2
        gradient = np.einsum("ij,ji->i", V, np.linalg.solve(J, V.T)) / self.a
        value = logdet(J)
        if not math.isfinite(value) or not np.isfinite(gradient).all():
            raise FloatingPointError("Oracle result is outside finite floating-point range")
        return value, gradient


def validate() -> dict:
    """Dense equality, objective interpretation, derivatives, and exact algebra."""
    rng = np.random.default_rng(2901)
    evaluations = binary_checks = derivative_checks = 0
    max_value_error = max_gradient_error = max_derivative_error = 0.0
    max_split_error = 0.0
    for n in (1, 2, 9):
        for rho in (-0.85, 0.0, 0.65):
            for s in (0.0, 1.0):
                for r in (0.05, 2.0):
                    design = NoisyDesign(rng.normal(size=(n, 3)), rho, s, r,
                                         0.1*np.eye(3), n//2)
                    for fraction in (0.5, 0.99):
                        dense = DenseLiuOracle(design, fraction)
                        structured = StructuredLiuOracle(design, fraction, a=dense.a)
                        automatic = StructuredLiuOracle(design, fraction)
                        max_split_error = max(max_split_error, abs(dense.a-automatic.a))
                        binary = (rng.random(n) < 0.5).astype(float)
                        points = [np.zeros(n), np.ones(n), binary,
                                  rng.uniform(0.1, 0.9, size=n)]
                        for z in points:
                            value, gradient = structured.value_gradient(z)
                            reference, reference_gradient = dense.value_gradient(z)
                            ve = abs(value-reference)
                            ge = float(np.max(abs(gradient-reference_gradient)))
                            max_value_error, max_gradient_error = (
                                max(max_value_error, ve), max(max_gradient_error, ge))
                            assert np.isclose(value, reference, atol=2e-11, rtol=2e-11)
                            assert np.allclose(gradient, reference_gradient,
                                               atol=2e-10, rtol=2e-10)
                            evaluations += 1
                            if np.all((z == 0) | (z == 1)):
                                selected = tuple(np.flatnonzero(z).tolist())
                                assert np.isclose(value, design.true_objective(selected),
                                                  atol=2e-11, rtol=2e-11)
                                binary_checks += 1
                        z = points[-1]
                        direction = rng.normal(size=n)
                        direction /= np.linalg.norm(direction)
                        epsilon = 1e-6
                        fd = (structured.value_gradient(z+epsilon*direction)[0]
                              - structured.value_gradient(z-epsilon*direction)[0])/(2*epsilon)
                        predicted = float(structured.value_gradient(z)[1] @ direction)
                        error = abs(fd-predicted)/max(1.0, abs(predicted))
                        max_derivative_error = max(max_derivative_error, error)
                        assert error < 2e-7
                        derivative_checks += 1

    # Additional conditioning probes and a nearly absent latent component.
    for rho, s, r in ((0.999, 1., .01), (-.999, 1., .01), (.8, 1e-12, 1.)):
        design = replace(generic_design(n=12, p=3, k=4), rho=rho,
                         latent_variance=s, nugget_variance=r)
        dense = DenseLiuOracle(design, .99)
        structured = StructuredLiuOracle(design, .99, a=dense.a)
        z = rng.uniform(size=design.n)
        value, gradient = structured.value_gradient(z)
        reference, reference_gradient = dense.value_gradient(z)
        assert np.isclose(value, reference, atol=2e-8, rtol=2e-8)
        assert np.allclose(gradient, reference_gradient, atol=2e-8, rtol=2e-8)
        evaluations += 1

    import sympy as sp
    rho, s, r, a = sp.Rational(1, 2), sp.Integer(2), sp.Rational(1, 3), sp.Rational(1, 10)
    F = sp.Matrix([[1, 2], [-1, 0], [2, 1]])
    K = sp.Matrix(3, 3, lambda i, j: s*rho**abs(i-j))
    R, Q = K+r*sp.eye(3), K.inv()
    z = sp.Matrix([0, sp.Rational(1, 3), 1])
    D = sp.diag(*(zi/a for zi in z))
    W = sp.eye(3)+(r-a)*D
    direct = (sp.eye(3)+(R-a*sp.eye(3))*D).inv()*F
    U = (Q+D*W.inv()).inv()*Q*F
    assert W.inv()*U == direct
    information = sp.eye(2)+F.T*D*direct
    exact_gradient = [(direct[i, :]*information.inv()*direct[i, :].T)[0]/a
                      for i in range(3)]
    assert all(value > 0 for value in exact_gradient)
    rejected = 0
    valid = StructuredLiuOracle(generic_design(n=3, p=2, k=1))
    for zbad in ([0., 0.], [0., -1e-9, 0.], [0., 1+1e-9, 0.], [0., np.nan, 0.]):
        try:
            valid.value_gradient(zbad)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("Malformed z was accepted")
    return {"dense_equality_evaluations": evaluations,
            "binary_objective_checks": binary_checks,
            "directional_derivative_checks": derivative_checks,
            "maximum_value_absolute_error": max_value_error,
            "maximum_gradient_absolute_error": max_gradient_error,
            "maximum_derivative_scaled_error": max_derivative_error,
            "maximum_automatic_split_absolute_error": max_split_error,
            "exact_rational_identity": "passed",
            "exact_rational_gradient": [str(value) for value in exact_gradient],
            "malformed_input_rejections": rejected}


def _median_evaluation(oracle, points, repetitions):
    for z in points:
        oracle.value_gradient(z)
    elapsed = []
    for repetition in range(repetitions):
        z = points[repetition % len(points)]
        start = perf_counter()
        oracle.value_gradient(z)
        elapsed.append(perf_counter()-start)
    return median(elapsed)


def benchmark() -> list[dict]:
    rows = []
    rng = np.random.default_rng(731)
    for n in (48, 96, 512, 2048):
        design = generic_design(n=n, p=3, k=n//4, rho=.6, seed=41,
                                nugget_variance=1.)
        start = perf_counter()
        dense = DenseLiuOracle(design, .99)
        dense_setup = perf_counter()-start
        start = perf_counter()
        structured = StructuredLiuOracle(design, .99)
        structured_setup = perf_counter()-start
        split_error = abs(dense.a-structured.a)
        # Compare evaluations with exactly the same stored floating-point split.
        structured_same = StructuredLiuOracle(design, .99, a=dense.a)
        points = [rng.uniform(size=n) for _ in range(4)]
        max_value_error = max_gradient_error = 0.0
        for z in points:
            value, gradient = structured_same.value_gradient(z)
            reference, reference_gradient = dense.value_gradient(z)
            max_value_error = max(max_value_error, abs(value-reference))
            max_gradient_error = max(max_gradient_error,
                                     float(np.max(abs(gradient-reference_gradient))))
            assert np.isclose(value, reference, atol=2e-10, rtol=2e-10)
            assert np.allclose(gradient, reference_gradient, atol=2e-10, rtol=2e-10)
        dense_time = _median_evaluation(dense, points, 9)
        structured_time = _median_evaluation(structured_same, points, 101)
        rows.append({"n": n, "p": design.p, "rho": design.rho,
                     "latent_variance": design.latent_variance,
                     "nugget_variance": design.nugget_variance,
                     "split_fraction": .99, "a": dense.a,
                     "automatic_split_absolute_error": split_error,
                     "dense_setup_seconds": dense_setup,
                     "structured_setup_seconds": structured_setup,
                     "dense_median_evaluation_seconds": dense_time,
                     "structured_median_evaluation_seconds": structured_time,
                     "evaluation_speedup": dense_time/structured_time,
                     "dense_repetitions": 9, "structured_repetitions": 101,
                     "point_type": "four deterministic interior random points",
                     "maximum_value_absolute_error": max_value_error,
                     "maximum_gradient_absolute_error": max_gradient_error})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_suffix(".json"))
    args = parser.parse_args()
    threads = {key: os.environ.get(key) for key in
               ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")}
    if any(value != "1" for value in threads.values()):
        raise RuntimeError("Set OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1")
    report = {"status": "passed", "thread_environment": threads,
              "python": platform.python_version(), "numpy": np.__version__,
              "scipy": scipy.__version__, "platform": platform.platform(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "dense_source_sha256": hashlib.sha256(
                  Path(__file__).with_name("noisy_markov_design.py").read_bytes()).hexdigest(),
              "validation": validate(),
              "benchmark": [] if args.validate_only else benchmark(),
              "limitations": "Floating-point oracle comparison only; no MIP or exact tangent certificate."}
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
