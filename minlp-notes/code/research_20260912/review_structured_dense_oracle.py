"""Independent checks for the structured Liu oracle.

The numerical reference uses the covariance of active, heteroscedastic virtual
observations, rather than the latent precision or author's nonsymmetric solve.
Extreme correlation probes are recorded as limitations, not silently excluded.
"""

from __future__ import annotations

import hashlib
from itertools import combinations
import json
import math
import os
from pathlib import Path
import platform

import mpmath as mp
import numpy as np
import scipy
from scipy.linalg import cho_factor, cho_solve
import sympy as sp

from noisy_markov_design import DenseLiuOracle, NoisyDesign
from structured_dense_oracle import StructuredLiuOracle


def covariance_reference(design, a, z):
    """Direct virtual-observation covariance, including zero-weight derivatives."""
    n = design.n
    R = np.array([[design.latent_variance * design.rho ** abs(i-j)
                   + (design.nugget_variance if i == j else 0)
                   for j in range(n)] for i in range(n)])
    chosen = np.flatnonzero(z > 0)
    residual = design.F.copy()
    information = design.prior.copy()
    if len(chosen):
        covariance = R[np.ix_(chosen, chosen)].copy()
        covariance.flat[::len(chosen)+1] += a*(1/z[chosen]-1)
        precision_F = cho_solve(cho_factor(covariance, lower=True), design.F[chosen])
        information += design.F[chosen].T @ precision_F
        residual -= R[:, chosen] @ precision_F
        residual[chosen] = (a/z[chosen])[:, None] * precision_F
    L = np.linalg.cholesky(information)
    value = 2*sum(np.log(np.diag(L)))
    gradient = np.sum(np.linalg.solve(L, residual.T)**2, axis=0)/a
    return float(value), gradient


def ordinary_checks():
    rng = np.random.default_rng(61237)
    counts = {"covariance_reference_evaluations": 0, "binary_objectives": 0,
              "central_derivatives": 0, "concavity_tangents": 0,
              "automatic_splits": 0, "dense_equalities": 0}
    errors = {"value_absolute": 0., "gradient_scaled": 0.,
              "derivative_scaled": 0., "automatic_split_relative": 0.,
              "tangent_upper_violation": 0.}
    for n in (1, 2, 5, 11):
        for rho in (-.98, -.6, 0., .7, .98):
            for latent, nugget in ((0., .3), (.001, 2.), (1., .01), (1., 1.), (100., .2)):
                F = rng.normal(size=(n, 3))
                P = rng.normal(size=(3, 3))
                design = NoisyDesign(F, rho, latent, nugget, P.T@P+.2*np.eye(3), n//2)
                for fraction in (.25, .99):
                    oracle = StructuredLiuOracle(design, fraction)
                    smallest = np.linalg.eigvalsh(design.covariance())[0]
                    split_error = abs(oracle.a-fraction*smallest)/smallest
                    errors["automatic_split_relative"] = max(errors["automatic_split_relative"], split_error)
                    assert split_error < 2e-11
                    counts["automatic_splits"] += 1
                    dense = DenseLiuOracle(design, fraction)
                    # Force both implementations to share the exact floating split.
                    dense.a = oracle.a
                    dense.S = design.covariance()-oracle.a*np.eye(n)
                    interior = rng.uniform(.15, .85, n)
                    binary = rng.integers(0, 2, n).astype(float)
                    mixed = rng.uniform(.05, .95, n)
                    mixed[::3] = 0
                    for z in (np.zeros(n), np.ones(n), binary, interior, mixed):
                        value, gradient = oracle.value_gradient(z)
                        target, target_gradient = covariance_reference(design, oracle.a, z)
                        ve = abs(value-target)
                        ge = float(np.max(abs(gradient-target_gradient)/np.maximum(1., abs(target_gradient))))
                        errors["value_absolute"] = max(errors["value_absolute"], ve)
                        errors["gradient_scaled"] = max(errors["gradient_scaled"], ge)
                        assert ve < 5e-9 and ge < 5e-9, (n, rho, latent, nugget, ve, ge)
                        counts["covariance_reference_evaluations"] += 1
                        dv, dg = dense.value_gradient(z)
                        assert abs(dv-value) < 5e-9
                        assert np.max(abs(dg-gradient)/np.maximum(1., abs(gradient))) < 5e-9
                        counts["dense_equalities"] += 1
                        if np.all((z == 0) | (z == 1)):
                            assert abs(value-design.true_objective(tuple(np.flatnonzero(z)))) < 5e-9
                            counts["binary_objectives"] += 1
                    value, gradient = oracle.value_gradient(interior)
                    direction = rng.normal(size=n)
                    direction /= np.linalg.norm(direction)
                    h = 1e-4
                    values = [covariance_reference(design, oracle.a, interior+j*h*direction)[0]
                              for j in (-2, -1, 1, 2)]
                    derivative = (values[0]-8*values[1]+8*values[2]-values[3])/(12*h)
                    expected = gradient@direction
                    de = abs(derivative-expected)/max(1., abs(expected))
                    assert de < 2e-7
                    errors["derivative_scaled"] = max(errors["derivative_scaled"], de)
                    counts["central_derivatives"] += 1
                    for target in (binary, np.zeros(n), np.ones(n), rng.uniform(size=n)):
                        target_value = covariance_reference(design, oracle.a, target)[0]
                        violation = target_value-value-gradient@(target-interior)
                        errors["tangent_upper_violation"] = max(errors["tangent_upper_violation"], float(violation))
                        assert violation < 2e-8
                        counts["concavity_tangents"] += 1
    return {"counts": counts, "maximum_errors": errors}


def exact_checks():
    """Symbolic virtual covariance derivatives; exact split equivalence."""
    derivatives = boundary_checks = split_checks = exact_values = 0
    x, y = sp.symbols("x y", positive=True)
    F = sp.Matrix([[1, 2], [-1, 3]])
    prior = sp.Matrix([[2, sp.Rational(1, 3)], [sp.Rational(1, 3), 1]])
    for rho in (sp.Rational(-3, 4), 0, sp.Rational(2, 3)):
        for latent in (0, sp.Rational(3, 2)):
            nugget, a = sp.Rational(2, 5), sp.Rational(1, 10)
            R = sp.Matrix(2, 2, lambda i, j: latent*rho**abs(i-j)+(nugget if i == j else 0))
            virtual = R+sp.diag(a*(1/x-1), a*(1/y-1))
            determinant = sp.factor((prior+F.T*virtual.inv()*F).det())
            point = {x: sp.Rational(2, 5), y: sp.Rational(4, 5)}
            exact_gradient = [sp.cancel(sp.diff(determinant, var)/determinant).subs(point)
                              for var in (x, y)]
            design = NoisyDesign(np.array(F).astype(float), float(rho), float(latent),
                                 float(nugget), np.array(prior).astype(float), 1)
            oracle = StructuredLiuOracle(design, a=float(a))
            value, gradient = oracle.value_gradient(np.array([.4, .8]))
            assert abs(value-float(sp.log(determinant.subs(point)).evalf(50))) < 2e-12
            assert np.max(abs(gradient-np.array(exact_gradient, dtype=float))) < 2e-12
            derivatives += 2
            exact_values += 1
            # Taking the symbolic derivative limit verifies one-sided boundary
            # derivatives independently of the author's V-row expression.
            for xb, yb in ((0, 0), (0, 1), (1, 0), (1, 1)):
                gv = [sp.limit(sp.limit(sp.cancel(sp.diff(determinant, var)/determinant),
                                       x, xb), y, yb) for var in (x, y)]
                _, numerical = oracle.value_gradient(np.array([xb, yb], dtype=float))
                assert np.max(abs(numerical-np.array(gv, dtype=float))) < 2e-11
                boundary_checks += 2
    for n in range(2, 7):
        for rho in (sp.Rational(-4, 5), sp.Rational(1, 3), sp.Rational(9, 10)):
            s, r = sp.Rational(7, 4), sp.Rational(1, 5)
            R = sp.Matrix(n, n, lambda i, j: s*rho**abs(i-j)+(r if i == j else 0))
            M = sp.zeros(n)
            for i in range(n):
                M[i, i] = 1 if i in (0, n-1) else 1+rho*rho
                if i+1 < n:
                    M[i, i+1] = M[i+1, i] = -rho
            c = s*(1-rho*rho)
            assert (R-r*sp.eye(n))*M == c*sp.eye(n)
            for a in (sp.Rational(1, 20), r, sp.Rational(1, 3), sp.Rational(1, 2), sp.Integer(2)):
                G = c*sp.eye(n)+(r-a)*M
                covariance_spd = all((R-a*sp.eye(n))[:k, :k].det() > 0 for k in range(1, n+1))
                precision_spd = all(G[:k, :k].det() > 0 for k in range(1, n+1))
                assert covariance_spd == precision_spd
                split_checks += 1
    return {"symbolic_interior_gradient_entries": derivatives,
            "symbolic_boundary_gradient_entries": boundary_checks,
            "exact_virtual_covariance_objectives": exact_values,
            "exact_split_equivalence_checks": split_checks}


def invalid_inputs():
    design = NoisyDesign(np.ones((3, 2)), .5, 1., 1., np.eye(2), 1)
    oracle = StructuredLiuOracle(design)
    calls = [lambda z=z: oracle.value_gradient(z) for z in
             ([0, 0], [0, 0, 0, 0], [0, -.1, 0], [0, 1.1, 0],
              [0, float("nan"), 0], [0, float("inf"), 0], [[0, 0, 0]])]
    calls += [lambda f=f: StructuredLiuOracle(design, f) for f in
              (0, 1, -.1, 1.1, float("nan"), float("inf"))]
    calls += [lambda a=a: StructuredLiuOracle(design, a=a) for a in
              (0, -1, oracle.minimum_covariance_eigenvalue, 100,
               float("nan"), float("inf"))]
    for call in calls:
        try:
            call()
        except ValueError:
            pass
        else:
            raise AssertionError("An invalid input was accepted")
    return {"rejected_inputs": len(calls)}


def high_precision_reference(design, a, z):
    with mp.workdps(90):
        R = mp.matrix([[mp.mpf(design.latent_variance)*mp.mpf(design.rho)**abs(i-j)
                        + (mp.mpf(design.nugget_variance)+mp.mpf(a)*(1/mp.mpf(z[i])-1)
                           if i == j else 0)
                        for j in range(design.n)] for i in range(design.n)])
        F = mp.matrix(design.F.tolist())
        precision_F = R**-1*F
        information = mp.matrix(design.prior.tolist())+F.T*precision_F
        value = mp.log(mp.det(information))
        gradient = [mp.mpf(a)/mp.mpf(z[i])**2
                    * (precision_F[i, :]*information**-1*precision_F[i, :].T)[0]
                    for i in range(design.n)]
        return mp.nstr(value, 60), [mp.nstr(v, 60) for v in gradient]


def conditioning_limits():
    rng = np.random.default_rng(492)
    F = rng.normal(size=(12, 3))
    prior, z = .1*np.eye(3), np.linspace(.2, .8, 12)
    rows = []
    for latent in (1., 1e-8, 1e-20):
        for rho in (.999, .99999999, .999999999999, np.nextafter(1., 0.)):
            design = NoisyDesign(F, float(rho), latent, 1., prior, 4)
            oracle = StructuredLiuOracle(design, .99)
            value, gradient = covariance_reference(design, oracle.a, z)
            row = {"rho": float(rho), "latent_variance": latent,
                   "nugget_variance": 1., "a": oracle.a,
                   "covariance_condition_number": float(np.linalg.cond(design.covariance())),
                   "reference_value": value}
            try:
                actual, actual_gradient = oracle.value_gradient(z)
                row.update(structured_value=actual, value_error=actual-value,
                           maximum_gradient_absolute_error=float(np.max(abs(actual_gradient-gradient))))
            except (np.linalg.LinAlgError, FloatingPointError) as exc:
                row["structured_exception"] = f"{type(exc).__name__}: {exc}"
            if rho == np.nextafter(1., 0.):
                hv, hg = high_precision_reference(design, oracle.a, z)
                row["high_precision_value"] = hv
                row["high_precision_gradient"] = hg
                assert abs(float(hv)-value) < 5e-13
                assert np.max(abs(np.array(hg, dtype=float)-gradient)) < 5e-13
                if latent == 1. and "structured_exception" not in row:
                    violations = []
                    for chosen in combinations(range(design.n), design.k):
                        target = np.zeros(design.n)
                        target[list(chosen)] = 1
                        true_value = covariance_reference(design, oracle.a, target)[0]
                        cut = actual+actual_gradient@(target-z)
                        violations.append((true_value-cut, chosen, true_value, cut))
                    worst = max(violations)
                    row["binary_cut_check"] = {
                        "k": design.k, "examined_subsets": len(violations),
                        "violating_subsets_over_1e_10": sum(int(v[0] > 1e-10) for v in violations),
                        "maximum_underestimation": float(worst[0]),
                        "selected": worst[1], "true_objective": float(worst[2]),
                        "computed_tangent": float(worst[3])}
            rows.append(row)
    return {"F": F.tolist(), "prior": prior.tolist(), "z": z.tolist(),
            "rows": rows,
            "interpretation": "Near-unit latent correlation can make precision coordinates unreliable even when R is well conditioned. These are documented limitations, not ordinary-domain test failures."}


def main():
    threads = {name: os.environ.get(name) for name in
               ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")}
    if any(v != "1" for v in threads.values()):
        raise RuntimeError("Set all three BLAS/OpenMP thread variables to 1")
    here = Path(__file__).resolve().parent
    report = {"status": "ordinary_domain_passed_with_documented_conditioning_limit",
              "python": platform.python_version(), "numpy": np.__version__,
              "scipy": scipy.__version__, "sympy": sp.__version__,
              "mpmath": mp.__version__, "thread_environment": threads,
              "source_hashes": {name: hashlib.sha256((here/name).read_bytes()).hexdigest()
                                for name in ("structured_dense_oracle.py", "noisy_markov_design.py",
                                             "review_structured_dense_oracle.py")},
              "ordinary_checks": ordinary_checks(), "exact_checks": exact_checks(),
              "invalid_inputs": invalid_inputs(), "conditioning_limits": conditioning_limits()}
    target = here/"results"/"structured-dense-oracle-independent-review.json"
    target.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({key: value for key, value in report.items() if key != "conditioning_limits"}, indent=2))
    print(f"Conditioning witnesses: {target}")


if __name__ == "__main__":
    main()
