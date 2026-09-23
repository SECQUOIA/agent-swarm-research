"""Exact recursion checks, conditioning regressions, and one-thread timings."""

import argparse
import hashlib
from itertools import combinations
import json
import os
from pathlib import Path
import platform
from time import perf_counter

import numpy as np
import scipy
import sympy as sp

from covariance_dense_oracle import CovarianceLiuOracle
from noisy_markov_design import DenseLiuOracle, NoisyDesign, generic_design
from review_structured_dense_oracle import covariance_reference, high_precision_reference
from structured_dense_oracle import _median_evaluation


def ordinary_checks():
    rng = np.random.default_rng(8142)
    counts = {"dense_equalities": 0, "virtual_covariance_equalities": 0,
              "binary_objectives": 0, "directional_derivatives": 0,
              "concavity_tangents": 0, "automatic_splits": 0}
    errors = {"value_absolute": 0., "gradient_scaled": 0.,
              "directional_derivative_scaled": 0., "split_relative": 0.,
              "maximum_tangent_violation": 0.}
    for n in (1, 2, 7, 15):
        for rho in (-.99, -.6, 0., .7, .99):
            for s, r in ((0., .3), (1e-20, 1.), (1., .01), (1., 1.), (100., .2)):
                F = rng.normal(size=(n, 3))
                A = rng.normal(size=(3, 3))
                design = NoisyDesign(F, rho, s, r, A.T@A+.2*np.eye(3), n//2)
                for fraction in (.25, .99):
                    dense = DenseLiuOracle(design, fraction)
                    oracle = CovarianceLiuOracle(design, fraction, a=dense.a)
                    automatic = CovarianceLiuOracle(design, fraction)
                    error = abs(automatic.a-dense.a)/dense.a
                    errors["split_relative"] = max(errors["split_relative"], error)
                    assert error < 1e-10
                    counts["automatic_splits"] += 1
                    interior = rng.uniform(.1, .9, n)
                    mixed = interior.copy()
                    mixed[::3] = 0
                    tiny = interior.copy()
                    tiny[::2] = 1e-20
                    binary = rng.integers(0, 2, n).astype(float)
                    for z in (np.zeros(n), np.ones(n), binary, interior, mixed, tiny):
                        value, gradient = oracle.value_gradient(z)
                        for method in (dense.value_gradient,
                                       lambda z: covariance_reference(design, oracle.a, z)):
                            target, target_gradient = method(z)
                            ve = abs(value-target)
                            ge = float(np.max(abs(gradient-target_gradient)/np.maximum(1., abs(target_gradient))))
                            errors["value_absolute"] = max(errors["value_absolute"], ve)
                            errors["gradient_scaled"] = max(errors["gradient_scaled"], ge)
                            assert ve < 1e-9 and ge < 1e-9, (n, rho, s, r, ve, ge)
                        counts["dense_equalities"] += 1
                        counts["virtual_covariance_equalities"] += 1
                        if np.all((z == 0) | (z == 1)):
                            assert abs(value-design.true_objective(tuple(np.flatnonzero(z)))) < 1e-9
                            counts["binary_objectives"] += 1
                    value, gradient = oracle.value_gradient(interior)
                    direction = rng.normal(size=n)
                    direction /= np.linalg.norm(direction)
                    h = 1e-4
                    values = [oracle.value_gradient(interior+j*h*direction)[0] for j in (-2, -1, 1, 2)]
                    derivative = (values[0]-8*values[1]+8*values[2]-values[3])/(12*h)
                    expected = gradient@direction
                    error = abs(derivative-expected)/max(1., abs(expected))
                    assert error < 2e-7
                    errors["directional_derivative_scaled"] = max(errors["directional_derivative_scaled"], error)
                    counts["directional_derivatives"] += 1
                    for target_z in (binary, np.zeros(n), np.ones(n)):
                        target = covariance_reference(design, oracle.a, target_z)[0]
                        violation = target-value-gradient@(target_z-interior)
                        assert violation < 1e-8
                        errors["maximum_tangent_violation"] = max(errors["maximum_tangent_violation"], float(violation))
                        counts["concavity_tangents"] += 1
    return {"counts": counts, "maximum_errors": errors}


def exact_recursion(F, prior, rho, s, r, a, z):
    n, p = F.shape
    innovations, weights, predictions, betas, denominators = [], [], [], [], []
    J, P, mean = prior.copy(), s, sp.zeros(1, p)
    for i in range(n):
        predictions.append(P)
        beta = a*(1-z[i])+r*z[i]
        betas.append(beta)
        denominator = P*z[i]+beta
        residual = F[i, :]-mean
        innovations.append(residual)
        weights.append(z[i]/denominator)
        denominators.append(denominator)
        J += z[i]/denominator*residual.T*residual
        mean = mean + P*z[i]/denominator*residual
        P = P*beta/denominator
        P = rho*rho*P+s*(1-rho*rho)
        mean = rho*mean
    rows, adjoint = [None]*n, sp.zeros(1, p)
    for i in range(n-1, -1, -1):
        rows[i] = a/denominators[i]*(innovations[i]-rho*predictions[i]*adjoint)
        adjoint = weights[i]*innovations[i]+rho*betas[i]/denominators[i]*adjoint
    V = sp.Matrix.vstack(*rows)
    return J, V


def exact_checks():
    count = 0
    maximum_value_error = maximum_gradient_error = 0.
    for n in (1, 2, 4):
        F = sp.Matrix(n, 2, lambda i, j: sp.Rational((i+1)*(j+2)-3, i+j+2))
        prior = sp.Matrix([[2, sp.Rational(1, 3)], [sp.Rational(1, 3), 1]])
        for rho in (sp.Rational(-4, 5), sp.Integer(0), sp.Rational(3, 5)):
            for s in (sp.Integer(0), sp.Integer(2)):
                r = sp.Rational(1, 3)
                R = sp.Matrix(n, n, lambda i, j: s*rho**abs(i-j)+(r if i == j else 0))
                for a in ((sp.Rational(1, 10),) if s == 0 else (sp.Rational(1, 10), sp.Rational(2, 5))):
                    assert all((R-a*sp.eye(n))[:i, :i].det() > 0 for i in range(1, n+1))
                    for z in ([sp.Integer(0)]*n, [sp.Integer(1)]*n,
                              [sp.Rational(i % 3, 2) for i in range(n)]):
                        D = sp.diag(*(x/a for x in z))
                        V = (sp.eye(n)+(R-a*sp.eye(n))*D).inv()*F
                        J = prior+F.T*D*V
                        actual_J, actual_V = exact_recursion(F, prior, rho, s, r, a, z)
                        assert actual_J == J and actual_V == V
                        exact_gradient = np.array([(V[i, :]*J.inv()*V[i, :].T)[0]/a
                                                   for i in range(n)], dtype=float)
                        design = NoisyDesign(np.array(F, dtype=float), float(rho), float(s),
                                             float(r), np.array(prior, dtype=float), n//2)
                        value, gradient = CovarianceLiuOracle(design, a=float(a)).value_gradient(np.array(z, dtype=float))
                        ve = abs(value-float(sp.log(J.det()).evalf(50)))
                        ge = float(np.max(abs(gradient-exact_gradient)))
                        maximum_value_error = max(maximum_value_error, ve)
                        maximum_gradient_error = max(maximum_gradient_error, ge)
                        assert ve < 5e-12 and ge < 5e-12
                        count += 1
    return {"exact_information_and_residual_equalities": count,
            "matching_numerical_gradient_checks": count,
            "maximum_value_error": maximum_value_error,
            "maximum_gradient_error": maximum_gradient_error}


def conditioning_checks(path):
    saved = json.loads(path.read_text())["conditioning_limits"]
    F, prior, z = np.array(saved["F"]), np.array(saved["prior"]), np.array(saved["z"])
    rows, worst_violation = [], -float("inf")
    for previous in saved["rows"]:
        for sign in (1, -1):
            design = NoisyDesign(F, sign*previous["rho"], previous["latent_variance"],
                                 previous["nugget_variance"], prior, 4)
            oracle = CovarianceLiuOracle(design, a=previous["a"])
            value, gradient = oracle.value_gradient(z)
            target, target_gradient = covariance_reference(design, oracle.a, z)
            ve, ge = abs(value-target), float(np.max(abs(gradient-target_gradient)))
            assert ve < 5e-12 and ge < 5e-12
            row = {"rho": design.rho, "latent_variance": design.latent_variance,
                   "nugget_variance": design.nugget_variance, "a": oracle.a,
                   "value": value, "value_absolute_error": ve,
                   "gradient_absolute_error": ge}
            if sign == 1:
                row["previous_value_error"] = previous.get("value_error")
                row["previous_exception"] = previous.get("structured_exception")
                if "high_precision_value" in previous:
                    row["value_error_against_saved_high_precision"] = abs(value-float(previous["high_precision_value"]))
                    row["gradient_error_against_saved_high_precision"] = float(np.max(abs(gradient-np.array(previous["high_precision_gradient"], dtype=float))))
                    assert row["value_error_against_saved_high_precision"] < 5e-12
                    assert row["gradient_error_against_saved_high_precision"] < 5e-12
                if "binary_cut_check" in previous:
                    violations = []
                    for selected in combinations(range(design.n), design.k):
                        candidate = np.zeros(design.n)
                        candidate[list(selected)] = 1
                        objective = covariance_reference(design, oracle.a, candidate)[0]
                        violations.append(float(objective-value-gradient@(candidate-z)))
                    worst_violation = max(violations)
                    assert worst_violation < 1e-10
                    row["binary_cut_check"] = {"examined_subsets": len(violations),
                                               "violating_subsets_over_1e_10": sum(x > 1e-10 for x in violations),
                                               "maximum_underestimation": worst_violation}
            rows.append(row)
    return {"input_file": str(path), "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "saved_witnesses_replayed": len(saved["rows"]), "including_negative_rho_cases": len(rows),
            "rows": rows}


def invalid_checks():
    design = NoisyDesign(np.ones((3, 2)), .5, 1., 1., np.eye(2), 1)
    oracle = CovarianceLiuOracle(design)
    calls = [lambda z=z: oracle.value_gradient(z) for z in
             ([0, 0], [0, 0, 0, 0], [0, -.1, 0], [0, 1.1, 0],
              [0, float("nan"), 0], [0, float("inf"), 0], [[0, 0, 0]])]
    calls += [lambda f=f: CovarianceLiuOracle(design, f) for f in
              (0, 1, -.1, 1.1, float("nan"), float("inf"))]
    calls += [lambda a=a: CovarianceLiuOracle(design, a=a) for a in
              (0, -1, oracle.minimum_covariance_eigenvalue, 100, float("nan"), float("inf"))]
    for call in calls:
        try:
            call()
        except ValueError:
            pass
        else:
            raise AssertionError("Malformed input was accepted")
    return {"rejected_inputs": len(calls)}


def scale_regressions():
    """Reviewer counterexample and its negative-correlation/range variants."""
    rows = []
    for latent in (1e8, 1e12, 1e20, 1e30):
        for rho in (-.5, .5):
            design = NoisyDesign(np.array([[1.], [2.], [-1.]]), rho, latent, 1.,
                                 np.array([[1/latent]]), 3)
            oracle = CovarianceLiuOracle(design, .5)
            z = np.ones(3)
            value, gradient = oracle.value_gradient(z)
            target, target_gradient = high_precision_reference(design, oracle.a, z)
            ve = abs(value-float(target))
            ge = float(np.max(abs(gradient-np.array(target_gradient, dtype=float))))
            assert ve < 5e-12 and ge < 5e-12
            rows.append({"latent_variance": latent, "nugget_variance": 1., "rho": rho,
                         "a": oracle.a, "value": value, "gradient": gradient.tolist(),
                         "high_precision_value": target, "high_precision_gradient": target_gradient,
                         "value_absolute_error": ve, "gradient_absolute_error": ge})
    for rho in (-.9, .9):
        design = NoisyDesign(np.array([[1.], [2.]]), rho, 1e308, 1., np.array([[.1]]), 1)
        oracle = CovarianceLiuOracle(design, .5)
        z = np.array([.5, .5])
        value, gradient = oracle.value_gradient(z)
        target, target_gradient = high_precision_reference(design, oracle.a, z)
        target_gradient = np.array(target_gradient, dtype=float)
        assert abs(value-float(target)) < 5e-12
        relative = float(np.max(abs(gradient-target_gradient)/abs(target_gradient)))
        assert relative < 5e-12
        rows.append({"latent_variance": 1e308, "nugget_variance": 1., "rho": rho,
                     "process_variance": oracle.process_variance,
                     "gradient_relative_error": relative, "value_absolute_error": abs(value-float(target))})
    return {"high_precision_cases": len(rows), "rows": rows}


def benchmark():
    rows, rng = [], np.random.default_rng(731)
    for n in (48, 96, 512, 2048):
        design = generic_design(n=n, p=3, k=n//4, rho=.6, seed=41, nugget_variance=1.)
        start = perf_counter()
        dense = DenseLiuOracle(design, .99)
        dense_setup = perf_counter()-start
        start = perf_counter()
        oracle = CovarianceLiuOracle(design, .99, a=dense.a)
        covariance_setup = perf_counter()-start
        points = [rng.uniform(size=n) for _ in range(4)]
        ve = ge = 0.
        for z in points:
            value, gradient = oracle.value_gradient(z)
            target, target_gradient = dense.value_gradient(z)
            ve = max(ve, abs(value-target))
            ge = max(ge, float(np.max(abs(gradient-target_gradient))))
            assert ve < 5e-10 and ge < 5e-10
        dense_time = _median_evaluation(dense, points, 9)
        covariance_time = _median_evaluation(oracle, points, 31)
        row = {"n": n, "p": design.p, "rho": design.rho,
               "latent_variance": design.latent_variance, "nugget_variance": design.nugget_variance,
               "a": oracle.a, "split_fraction": .99,
               "dense_setup_seconds": dense_setup, "covariance_setup_seconds": covariance_setup,
               "dense_median_evaluation_seconds": dense_time,
               "covariance_median_evaluation_seconds": covariance_time,
               "dense_over_covariance_evaluation_ratio": dense_time/covariance_time,
               "dense_repetitions": 9, "covariance_repetitions": 31,
               "maximum_value_error": ve, "maximum_gradient_error": ge}
        rows.append(row)
        print(json.dumps({"stage": "benchmark", **row}), flush=True)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("results")/"covariance-dense-oracle-validation.json")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    threads = {key: os.environ.get(key) for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")}
    if any(value != "1" for value in threads.values()):
        raise RuntimeError("Set OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1")
    root = Path(__file__).parent
    result = {"status": "passed", "python": platform.python_version(), "numpy": np.__version__,
              "scipy": scipy.__version__, "sympy": sp.__version__, "thread_environment": threads,
              "source_hashes": {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in
                                ("covariance_dense_oracle.py", "verify_covariance_dense_oracle.py",
                                 "structured_dense_oracle.py", "noisy_markov_design.py", "review_structured_dense_oracle.py")},
              "ordinary_checks": ordinary_checks(), "exact_checks": exact_checks(),
              "conditioning_checks": conditioning_checks(root/"results"/"structured-dense-oracle-independent-review.json"),
              "invalid_checks": invalid_checks(), "scale_regressions": scale_regressions(),
              "benchmark": [] if args.validate_only else benchmark(),
              "limitations": "Numerical agreement in the tested domain; no exact floating-point tangents or full MIP timings."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "ordinary_checks": result["ordinary_checks"],
                      "exact_checks": result["exact_checks"], "invalid_checks": result["invalid_checks"]}, indent=2))


if __name__ == "__main__":
    main()
