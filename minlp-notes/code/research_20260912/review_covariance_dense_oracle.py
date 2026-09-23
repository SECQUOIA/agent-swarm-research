"""Independent covariance-space Liu oracle review, including repaired witnesses.

References use direct covariance algebra and 100--400 digit arithmetic; the
exact recurrence comparison uses rational resolvents. No MIP is run and no
floating-point tangent is declared an exact certificate.
"""

from dataclasses import replace
from hashlib import sha256
from importlib.machinery import SourceFileLoader
from itertools import combinations, product
import json
import math
from pathlib import Path
import platform
from time import perf_counter

import mpmath as mp
import numpy as np
import sympy as sp

from covariance_dense_oracle import CovarianceLiuOracle
from noisy_markov_design import NoisyDesign
from structured_dense_oracle import StructuredLiuOracle


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "results/covariance-dense-oracle-independent-review.json"


def reference(design, a, z, *, digits=100):
    """Independent active-subset virtual covariance solve, including zero weights."""
    with mp.workdps(digits):
        n, p = design.F.shape
        F = mp.matrix(design.F.tolist())
        prior = mp.matrix(design.prior.tolist())
        latent, rho, noise, split = map(mp.mpf, (float(design.latent_variance),
                                               float(design.rho), float(design.nugget_variance), float(a)))
        zz = [mp.mpf(float(x)) for x in z]
        active = [i for i in range(n) if zz[i] > 0]
        J, V = prior.copy(), F.copy()
        if active:
            K = mp.matrix([[latent*rho**abs(i-j) for j in active] for i in range(n)])
            B = mp.matrix([[K[i, j] for j in range(len(active))] for i in active])
            FA = mp.matrix([[F[i, j] for j in range(p)] for i in active])
            for j, i in enumerate(active):
                B[j, j] += noise+split*(1-zz[i])/zz[i]
            QF = B**-1 * FA
            J += FA.T * QF
            # On positive weights use V_i=(a/z_i)(B^-1 F)_i directly.
            # Only zero-weight rows need a posterior residual subtraction.
            for j, i in enumerate(active):
                for col in range(p):
                    V[i, col] = split/zz[i]*QF[j, col]
            for i in set(range(n))-set(active):
                for col in range(p):
                    V[i, col] -= sum(K[i, j]*QF[j, col] for j in range(len(active)))
        inverse = J**-1
        gradient = [sum(V[i, j]*inverse[j, k]*V[i, k]
                        for j in range(p) for k in range(p))/split for i in range(n)]
        return float(mp.log(mp.det(J))), np.array([float(x) for x in gradient])


def scaled_error(actual, expected):
    return float(np.max(abs(actual-expected)/np.maximum(1., abs(expected))))


def exact_adjoint_checks():
    """An exact identity test, independent of floating-point implementation."""
    count = 0
    for n in (1, 3, 4):
        for rho in (sp.Rational(-3, 5), sp.Rational(2, 3)):
            latent, noise, a = sp.Integer(2), sp.Rational(1, 3), sp.Rational(1, 10)
            F = sp.Matrix(n, 2, lambda i, j: sp.Rational((i+1)*(j+1)-2, i+j+1))
            R = sp.Matrix(n, n, lambda i, j: latent*rho**abs(i-j)+(noise if i == j else 0))
            for z in product((sp.Integer(0), sp.Rational(1, 2), sp.Integer(1)), repeat=n):
                e, pred, den, beta, weight = [], [], [], [], []
                mean, P, info = sp.zeros(1, 2), latent, sp.zeros(2)
                for i in range(n):
                    pred.append(P)
                    e.append(F[i, :]-mean)
                    beta.append(a*(1-z[i])+noise*z[i])
                    den.append(P*z[i]+beta[-1])
                    weight.append(z[i]/den[-1])
                    info += weight[-1]*e[-1].T*e[-1]
                    mean = rho*(mean+P*weight[-1]*e[-1])
                    P = rho*rho*P*beta[-1]/den[-1]+latent*(1-rho*rho)
                adjoint, rows = sp.zeros(1, 2), []
                for i in range(n-1, -1, -1):
                    rows.append(a/den[i]*(e[i]-rho*pred[i]*adjoint))
                    adjoint = weight[i]*e[i]+rho*beta[i]/den[i]*adjoint
                V = sp.Matrix.vstack(*reversed(rows))
                D = sp.diag(*(zi/a for zi in z))
                direct = (sp.eye(n)+(R-a*sp.eye(n))*D).inv()*F
                assert V == direct and info == F.T*D*direct
                count += 1
    return count


def main():
    started = perf_counter()
    source_names = ("covariance_dense_oracle.py", "structured_dense_oracle.py",
                    "noisy_markov_design.py", Path(__file__).name)
    sources = {name: (HERE/name).read_bytes() for name in source_names}
    rng = np.random.default_rng(192602)
    counts = {k: 0 for k in ("high_precision_comparisons", "binary_objectives",
                             "derivative_directions", "tangent_checks", "boundary_gradients",
                             "invalid_inputs", "saved_witness_replays")}
    errors = {"value_absolute": 0., "gradient_scaled": 0., "derivative_scaled": 0.}
    for n in (1, 2, 5, 9):
        for rho, latent, noise in ((0., 1., .3), (-.8, 2., .4), (.6, 0., 2.),
                                   (.9, 1e-12, 1.), (-.95, 100., .01)):
            F = rng.normal(size=(n, 2))
            B = rng.normal(size=(2, 2))
            design = NoisyDesign(F, rho, latent, noise, B.T@B+.4*np.eye(2), n//2)
            for fraction in (.2, .99):
                oracle = CovarianceLiuOracle(design, fraction)
                expected_minimum = np.linalg.eigvalsh(design.covariance())[0]
                assert abs(oracle.minimum_covariance_eigenvalue-expected_minimum) <= 1e-10*max(1, expected_minimum)
                interior = rng.uniform(.15, .85, n)
                mixed = interior.copy()
                mixed[::2] = 0
                tiny = interior.copy()
                tiny[::2] = 1e-30
                binary = rng.integers(0, 2, size=n).astype(float)
                for z in (np.zeros(n), np.ones(n), mixed, tiny, binary, interior):
                    value, gradient = oracle.value_gradient(z)
                    other, other_gradient = reference(design, oracle.a, z)
                    ve, ge = abs(value-other), scaled_error(gradient, other_gradient)
                    assert ve < 2e-10 and ge < 2e-9, (n, rho, latent, noise, z, ve, ge)
                    errors["value_absolute"] = max(errors["value_absolute"], ve)
                    errors["gradient_scaled"] = max(errors["gradient_scaled"], ge)
                    counts["high_precision_comparisons"] += 1
                    if np.all((z == 0) | (z == 1)):
                        selected = tuple(np.flatnonzero(z))
                        assert abs(value-design.true_objective(selected)) < 2e-9
                        counts["binary_objectives"] += 1
                    counts["boundary_gradients"] += int(np.any((z == 0) | (z == 1)))
                value, gradient = oracle.value_gradient(interior)
                direction = rng.normal(size=n)
                direction /= np.linalg.norm(direction)
                h = 2e-5
                f = [oracle.value_gradient(interior+j*h*direction)[0] for j in (-2, -1, 1, 2)]
                actual = (f[0]-8*f[1]+8*f[2]-f[3])/(12*h)
                expected = gradient@direction
                error = abs(actual-expected)/max(1., abs(expected))
                assert error < 1e-7
                errors["derivative_scaled"] = max(errors["derivative_scaled"], error)
                counts["derivative_directions"] += 1
                for endpoint in (binary, mixed, np.zeros(n), np.ones(n)):
                    objective = reference(design, oracle.a, endpoint)[0]
                    assert objective <= value+gradient@(endpoint-interior)+2e-9
                    counts["tangent_checks"] += 1
    exact_count = exact_adjoint_checks()
    extreme_rows = []
    for latent in (1e8, 1e12, 1e16, 1e20, 1e30, 1e100):
        for rho in (.5, -.5):
            design = NoisyDesign(np.array([[1.], [2.], [-1.]]), rho, latent, 1.,
                                 np.array([[1/latent]]), 2)
            oracle = CovarianceLiuOracle(design)
            for z in (np.ones(3), np.array([0., .7, 1.]), np.array([.3, 1., 0.])):
                value, gradient = oracle.value_gradient(z)
                other, other_gradient = reference(design, oracle.a, z, digits=180)
                ve, ge = abs(value-other), scaled_error(gradient, other_gradient)
                assert ve < 2e-10 and ge < 2e-10
                extreme_rows.append({"rho": rho, "P": latent, "r": 1., "prior": 1/latent,
                                     "z": z.tolist(), "value_absolute_error": ve, "gradient_scaled_error": ge})
    for rho in (np.nextafter(1., 0.), -np.nextafter(1., 0.)):
        design = NoisyDesign(np.array([[1.], [2.], [-1.]]), rho, 1e30, 1., np.array([[1e-30]]), 2)
        oracle = CovarianceLiuOracle(design)
        for z in (np.ones(3), np.array([0., .7, 1.]), np.array([.3, 1., 0.])):
            value, gradient = oracle.value_gradient(z)
            other, other_gradient = reference(design, oracle.a, z, digits=180)
            ve, ge = abs(value-other), scaled_error(gradient, other_gradient)
            assert ve < 2e-10 and ge < 2e-10
            extreme_rows.append({"rho": rho, "P": 1e30, "r": 1., "prior": 1e-30,
                                 "z": z.tolist(), "value_absolute_error": ve, "gradient_scaled_error": ge})
    scale_rows = []
    base = NoisyDesign(np.array([[1.], [2.], [-1.]]), -.7, 2., 3., np.array([[.3]]), 2)
    base_oracle, point = CovarianceLiuOracle(base), np.array([0., .7, 1.])
    base_value, base_gradient = base_oracle.value_gradient(point)
    for scale in (1e-200, 1e200):
        design = replace(base, latent_variance=base.latent_variance*scale,
                         nugget_variance=base.nugget_variance*scale, prior=base.prior/scale)
        oracle = CovarianceLiuOracle(design, a=base_oracle.a*scale)
        value, gradient = oracle.value_gradient(point)
        ve, ge = abs(value-(base_value-math.log(scale))), scaled_error(gradient, base_gradient)
        assert ve < 2e-10 and ge < 2e-10
        scale_rows.append({"scale": scale, "value_absolute_error": ve, "gradient_scaled_error": ge})
    finite_range_rows = []
    for rho in (-.9, .9):
        design = NoisyDesign(np.ones((2, 1)), rho, 1e308, 1., np.eye(1), 1)
        oracle = CovarianceLiuOracle(design)
        value, gradient = oracle.value_gradient(np.array([.5, .5]))
        other, other_gradient = reference(design, oracle.a, [.5, .5], digits=400)
        assert abs(value-other) < 1e-12
        np.testing.assert_allclose(gradient, other_gradient, atol=1e-320, rtol=1e-10)
        finite_range_rows.append({"rho": rho, "P": 1e308, "process_variance": oracle.process_variance,
                                  "value": value, "gradient": gradient.tolist(), "reference_gradient": other_gradient.tolist()})
    saved_path = HERE/"results/structured-dense-oracle-independent-review.json"
    saved = json.loads(saved_path.read_text())["conditioning_limits"]
    F, prior, z = np.array(saved["F"]), np.array(saved["prior"]), np.array(saved["z"])
    witness_rows, cut_rows = [], []
    for old in saved["rows"]:
        for sign in (1, -1):
            design = NoisyDesign(F, sign*old["rho"], old["latent_variance"], old["nugget_variance"], prior, 4)
            oracle = CovarianceLiuOracle(design, a=old["a"])
            value, gradient = oracle.value_gradient(z)
            other, other_gradient = reference(design, oracle.a, z)
            ve, ge = abs(value-other), scaled_error(gradient, other_gradient)
            assert ve < 2e-11 and ge < 2e-11
            witness_rows.append({"rho": design.rho, "P": design.latent_variance,
                                 "value_absolute_error": ve, "gradient_scaled_error": ge})
            counts["saved_witness_replays"] += 1
            if "binary_cut_check" in old:
                maximum, violations = -math.inf, 0
                old_value, old_gradient = StructuredLiuOracle(design, a=oracle.a).value_gradient(z)
                old_maximum, old_violations = -math.inf, 0
                for subset in combinations(range(design.n), design.k):
                    candidate = np.zeros(design.n)
                    candidate[list(subset)] = 1
                    objective = reference(design, oracle.a, candidate)[0]
                    violation = objective-value-gradient@(candidate-z)
                    maximum, violations = max(maximum, violation), violations+int(violation>1e-10)
                    old_violation = objective-old_value-old_gradient@(candidate-z)
                    old_maximum = max(old_maximum, old_violation)
                    old_violations += int(old_violation>1e-10)
                assert violations == 0
                cut_rows.append({"rho": design.rho, "subsets": math.comb(design.n, design.k),
                                 "violations_over_1e_10": violations, "maximum_violation": maximum,
                                 "old_precision_violations_over_1e_10": old_violations,
                                 "old_precision_maximum_violation": old_maximum})
    # Reconstruct the new review's failure from the author's archived RTS source.
    archive = HERE/"results/covariance-dense-oracle-rts-initial-source.txt"
    legacy = SourceFileLoader("covariance_rts_archived_review", str(archive)).load_module()
    failure_rows = []
    for latent in (1e12, 1e16, 1e20, 1e30):
        design = NoisyDesign(np.array([[1.], [2.], [-1.]]), .5, latent, 1., np.array([[1/latent]]), 2)
        old_oracle, oracle = legacy.CovarianceLiuOracle(design), CovarianceLiuOracle(design)
        point, candidate = np.ones(3), np.array([0., 1., 1.])
        old_value, old_gradient = old_oracle.value_gradient(point)
        value, gradient = oracle.value_gradient(point)
        other, other_gradient = reference(design, oracle.a, point, digits=150)
        candidate_value = reference(design, oracle.a, candidate, digits=150)[0]
        failure_rows.append({"P": latent, "r": 1., "prior": 1/latent, "rho": .5,
                             "F": design.F.tolist(), "a": oracle.a, "z": point.tolist(),
                             "old_gradient": old_gradient.tolist(), "reference_gradient": other_gradient.tolist(),
                             "new_gradient": gradient.tolist(), "old_value_error": old_value-other,
                             "new_value_error": value-other, "candidate": candidate.tolist(),
                             "old_binary_cut_violation": candidate_value-old_value-old_gradient@(candidate-point),
                             "new_binary_cut_violation": candidate_value-value-gradient@(candidate-point)})
    assert failure_rows[-1]["old_binary_cut_violation"] > 1e20
    valid = CovarianceLiuOracle(NoisyDesign(np.ones((3, 2)), .5, 1., 1., np.eye(2), 1))
    for bad in ([0, 0], [0, 0, 0, 0], [0, -.1, 1], [0, 1.1, 1], [0, np.nan, 1], [0, np.inf, 1], [[0, 0, 1]]):
        try:
            valid.value_gradient(bad)
        except ValueError:
            counts["invalid_inputs"] += 1
        else:
            raise AssertionError("malformed selection accepted")
    for bad in (0, 1, -1, np.nan, np.inf):
        try:
            CovarianceLiuOracle(valid.design, bad)
        except ValueError:
            counts["invalid_inputs"] += 1
        else:
            raise AssertionError("malformed split fraction accepted")
    for bad in (0, -1, valid.minimum_covariance_eigenvalue, np.nan, np.inf):
        try:
            CovarianceLiuOracle(valid.design, a=bad)
        except ValueError:
            counts["invalid_inputs"] += 1
        else:
            raise AssertionError("malformed explicit split accepted")
    assert all((HERE/name).read_bytes() == data for name, data in sources.items())
    report = {"status": "passed_after_adjoint_and_process_variance_repairs", "python": platform.python_version(),
              "numpy": np.__version__, "sympy": sp.__version__, "mpmath": mp.__version__,
              "source_hashes": {name: sha256(data).hexdigest() for name, data in sources.items()},
              "saved_witness_sha256": sha256(saved_path.read_bytes()).hexdigest(),
              "archived_rts_source_sha256": sha256(archive.read_bytes()).hexdigest(),
              "counts": counts, "maximum_ordinary_errors": errors, "exact_adjoint_matrix_identities": exact_count,
              "extreme_ratio_cases": extreme_rows, "scale_invariance_cases": scale_rows,
              "finite_range_cases": finite_range_rows,
              "near_unit_witnesses": witness_rows, "near_unit_binary_cut_checks": cut_rows,
              "repaired_large_signal_witnesses": failure_rows, "wall_seconds": perf_counter()-started,
              "limitations": ["High precision is numerical evidence, not interval certification.",
                              "Extreme finite arithmetic can still fail or lose accuracy outside tested cases.",
                              "No MIP or runtime superiority experiment is included."]}
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(report, indent=2)+"\n")
    temporary.replace(OUTPUT)
    print(json.dumps({k: report[k] for k in ("status", "counts", "maximum_ordinary_errors", "exact_adjoint_matrix_identities", "near_unit_binary_cut_checks", "wall_seconds")}, indent=2))


if __name__ == "__main__":
    main()
