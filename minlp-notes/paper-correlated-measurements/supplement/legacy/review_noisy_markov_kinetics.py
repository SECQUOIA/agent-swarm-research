"""Independent, scoped review of the four saved smooth kinetics probes.

The mean and log-parameter sensitivities are derived from the augmented mass
balances, without importing the producer or its closed-form mean. This review
also reconstructs saved information matrices and replays the already reviewed
exact certificate library. It does not repeat the library's general tests.
"""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
from time import perf_counter

import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import solve_ivp

from certify_noisy_markov import certify


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"


def augmented_generator(A0, k1, k2, *, high_precision=False):
    """State order: x, dx/dlog(A0), dx/dlog(k1), dx/dlog(k2)."""
    zero = mp.mpf(0) if high_precision else 0.0
    M = [[zero for _ in range(12)] for _ in range(12)]
    J = [[-k1, zero, zero], [k1, -k2, zero], [zero, k2, zero]]
    Q1 = [[-k1, zero, zero], [k1, zero, zero], [zero, zero, zero]]
    Q2 = [[zero, zero, zero], [zero, -k2, zero], [zero, k2, zero]]
    for block in range(4):
        for i in range(3):
            for j in range(3):
                M[3*block+i][3*block+j] = J[i][j]
    for block, Q in ((2, Q1), (3, Q2)):
        for i in range(3):
            for j in range(3):
                M[3*block+i][j] = Q[i][j]
    initial = [zero for _ in range(12)]
    initial[0] = initial[3] = A0
    if high_precision:
        return mp.matrix(M), mp.matrix(initial)
    return np.array(M), np.array(initial)


def augmented_trajectory(times, A0, k1, k2):
    M, initial = augmented_generator(A0, k1, k2)
    solution = solve_ivp(lambda t, y: M @ y, (0, float(max(times))), initial,
                         method="DOP853", t_eval=times, rtol=2e-13, atol=2e-14)
    assert solution.success
    return solution.y.T


def covariance(record):
    indices = np.arange(record["n"])
    return (record["latent_variance"] * record["rho"] ** abs(indices[:, None]-indices)
            + record["nugget_variance"] * np.eye(record["n"]))


def dense_information(F, prior, R, selected):
    selected = np.asarray(selected, dtype=int)
    return prior + F[selected].T @ np.linalg.solve(R[np.ix_(selected, selected)], F[selected])


def local_information(F, prior, R, selected, L):
    """Rebuild local regressions directly from covariance principal blocks."""
    J = prior.copy()
    for t in sorted(selected):
        history = [j for j in selected if t-L <= j < t]
        if history:
            b = np.linalg.solve(R[np.ix_(history, history)], R[history, t])
            variance = R[t, t] - R[t, history] @ b
            sensitivity = F[t] - b @ F[history]
        else:
            variance = R[t, t]
            sensitivity = F[t]
        assert variance > 0
        J += np.outer(sensitivity, sensitivity)/variance
    return J


def exact_number(value):
    q = Fraction(str(value))
    return mp.mpf(q.numerator)/q.denominator


def high_precision_objective(record, selected):
    F = mp.matrix([[exact_number(x) for x in record["F"][t]] for t in selected])
    prior = mp.matrix([[exact_number(x) for x in row] for row in record["prior"]])
    P, r, rho = [exact_number(record[key]) for key in
                 ("latent_variance", "nugget_variance", "rho")]
    R = mp.matrix([[P*rho**abs(i-j)+(r if i == j else 0) for j in selected]
                   for i in selected])
    J = prior + F.T * (R**-1) * F
    return mp.log(mp.det(J))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_case(path, payload, case_index):
    case = payload["results"][case_index]
    exact_payload = json.loads(path.read_text(), parse_float=str)
    exact_case = exact_payload["results"][case_index]
    kinetics = case["kinetics"]
    n, p, k = case["n"], case["p"], case["k"]
    assert n in (48, 96) and p == 3 and k == n//3
    assert case["rho"] == 0.4
    assert case["latent_variance"] == case["nugget_variance"] == 0.00125
    F, prior = np.asarray(case["F"]), np.asarray(case["prior"])
    assert F.shape == (n, 3) and prior.shape == (3, 3)
    np.testing.assert_array_equal(prior, 0.01*np.eye(3))
    assert kinetics["parameter_names"] == ["log(A0)", "log(k1)", "log(k2)"]
    times = np.asarray(kinetics["candidate_times"])
    np.testing.assert_array_equal(times, 12*np.arange(1, n+1)/n)
    A0, k1, k2 = (kinetics[key] for key in ("A0", "k1", "k2"))
    assert A0 == 1 and k1 > k2 > 0

    trajectory = augmented_trajectory(times, A0, k1, k2)
    independent_F = trajectory[:, [4, 7, 10]]
    mean_error = float(np.max(abs(trajectory[:, 1]-kinetics["mean_B"])))
    sensitivity_error = float(np.max(abs(independent_F-F)))
    assert mean_error < 2e-11 and sensitivity_error < 2e-11
    mass_error = float(np.max(abs(trajectory[:, :3].sum(axis=1)-A0)))
    derivative_mass_error = float(np.max(abs(
        trajectory[:, 3:].reshape(n, 3, 3).sum(axis=2)-[A0, 0, 0])))
    assert mass_error < 1e-12 and derivative_mass_error < 1e-12
    assert np.min(trajectory[:, :3]) > -1e-12

    swapped = augmented_trajectory(times, A0*k1/k2, k2, k1)
    swap_error = float(np.max(abs(swapped[:, 1]-trajectory[:, 1])))
    assert swap_error < 2e-11
    expected_peak = np.log(k1/k2)/(k1-k2)
    assert abs(kinetics["nominal_peak_time"]-expected_peak) < 1e-13
    assert 0 < expected_peak < 12

    # A second precision scale and a matrix exponential, still assembled from
    # the balances rather than the producer's exponential difference formula.
    high_precision_rows = sorted(set((0, int(np.argmin(abs(times-expected_peak))), n//2-1, n-1)))
    hp_error = mp.mpf(0)
    with mp.workdps(70):
        M, initial = augmented_generator(*map(exact_number, (A0, k1, k2)), high_precision=True)
        for row in high_precision_rows:
            y = mp.expm(M*exact_number(times[row]))*initial
            for j, index in enumerate((4, 7, 10)):
                hp_error = max(hp_error, abs(y[index]-exact_number(exact_case["F"][row][j])))
            hp_error = max(hp_error, abs(y[1]-exact_number(exact_case["kinetics"]["mean_B"][row])))
        assert hp_error < mp.mpf("2e-14")
        hp_error_string = mp.nstr(hp_error, 18)

    R = covariance(case)
    assert np.linalg.eigvalsh(R).min() >= case["nugget_variance"]-1e-14
    assert abs(np.sqrt(R[0, 0])-0.05) < 1e-14
    assert abs(R[0, 1]/R[0, 0]-0.2) < 1e-14
    hull = case["hulls"][0]
    dense = case["dense_oa_strengthened"]
    selected_objectives = {}
    for name, solver, lb_key in (("memory", hull, "true_lower_bound"),
                                 ("dense", dense, "lower_bound")):
        selected = solver["selected"]
        assert len(selected) == len(set(selected)) == k
        assert all(isinstance(t, int) and 0 <= t < n for t in selected)
        np.testing.assert_array_equal(solver["selected_times"], times[selected])
        J = dense_information(F, prior, R, selected)
        sign, value = np.linalg.slogdet(J)
        assert sign == 1 and abs(value-solver[lb_key]) < 1e-9
        selected_objectives[name] = float(value)
    assert dense["initial_selected"] == hull["selected"]
    assert dense["selected"] == dense["initial_selected"]
    assert abs(dense["initial_lower_bound"]-hull["true_lower_bound"]) < 1e-12
    assert dense["status"] == "time_limit"
    assert dense["split_fraction"] == 0.99 and dense["root_oa_rounds"] == 200
    assert dense["root_status"] == "iteration_limit"
    assert dense["oa_rounds"] == 1
    assert 9.9 <= dense["wall_seconds"] <= 10.2
    assert hull["status"] == "hull_optimal_tolerance"
    assert 0 < hull["wall_seconds"] < 10 and hull["surrogate_hull_gap"] < 1e-6
    assert abs(hull["true_upper_bound"]-hull["true_lower_bound"]-hull["true_gap"]) < 1e-12
    assert abs(dense["upper_bound"]-dense["lower_bound"]-dense["absolute_gap"]) < 1e-12

    weights = np.asarray([point["weight"] for point in hull["hull_support"]])
    assert np.min(weights) >= 0 and abs(weights.sum()-1) < 1e-12
    reconstructed = np.zeros((3, 3))
    support_error = 0.0
    for point in hull["hull_support"]:
        selected = point["selected"]
        assert len(selected) == len(set(selected)) == k
        J = local_information(F, prior, R, selected, hull["L"])
        support_error = max(support_error, float(np.max(abs(J-np.asarray(point["information"])))))
        reconstructed += point["weight"]*J
    assert support_error < 2e-9
    np.testing.assert_allclose(reconstructed, hull["hull_information"], rtol=1e-12, atol=2e-9)
    assert abs(np.linalg.slogdet(reconstructed)[1]-hull["surrogate_hull_value"]) < 1e-9

    cert_path = RESULTS / f"noisy-markov-kinetics-certificate-n{n}-{kinetics['regime']}.json"
    certificate = json.loads(cert_path.read_text())
    assert certificate["input_sha256"] == sha256(path)
    assert certificate["source_sha256"] == sha256(HERE/"certify_noisy_markov.py")
    assert certificate["input_case_index"] == case_index
    assert certificate["input_hull_index"] == -1
    assert Path(certificate["input_file"]).name == path.name
    assert certificate["selected"] == hull["selected"]
    for key in ("n", "p", "k"):
        assert certificate[key] == case[key]
    assert certificate["L"] == hull["L"] == 8
    assert certificate["input_interpretation"] == "JSON decimal numbers are exact rational data"
    replay = certify(exact_case, exact_case["hulls"][0])
    replay = json.loads(json.dumps(replay, default=str))
    for key, value in replay.items():
        if key != "wall_seconds":
            assert value == certificate[key], key
    with mp.workdps(70):
        objective = high_precision_objective(exact_case, hull["selected"])
        lower, upper, gap = (exact_number(certificate[key]) for key in ("lower_bound", "upper_bound", "gap"))
        assert 0 <= objective-lower < mp.mpf("2e-13")
        assert objective <= upper and gap > 0
        assert abs(upper-lower-gap) < mp.mpf("1e-60")
        objective_string = mp.nstr(objective, 55)
        certificate_lb_slack = mp.nstr(objective-lower, 18)

    return {
        "n": n, "regime": kinetics["regime"], "input_sha256": sha256(path),
        "augmented_ode_rows": n, "augmented_ode_sensitivity_entries": 3*n,
        "max_mean_error": mean_error, "max_sensitivity_error": sensitivity_error,
        "mass_balance_error": mass_error, "sensitivity_mass_balance_error": derivative_mass_error,
        "rate_swap_mean_error": swap_error,
        "high_precision_augmented_expm_rows": len(high_precision_rows),
        "max_high_precision_saved_mean_sensitivity_error": hp_error_string,
        "full_sensitivity_singular_values": np.linalg.svd(F, compute_uv=False).tolist(),
        "selected_information_condition_number": float(np.linalg.cond(dense_information(F, prior, R, hull["selected"]))),
        "selected_objectives": selected_objectives,
        "support_path_count": len(weights), "support_count_weight_above_1e_8": int(np.count_nonzero(weights > 1e-8)),
        "max_support_information_entry_error": support_error,
        "certificate_file": cert_path.name, "certificate_sha256": sha256(cert_path),
        "certificate_replayed": True, "independent_high_precision_true_logdet": objective_string,
        "certificate_lower_slack": certificate_lb_slack,
        "certified_gap": certificate["display_gap"],
        "memory_seconds": hull["wall_seconds"], "dense_seconds": dense["wall_seconds"],
        "dense_gap": dense["absolute_gap"],
    }


def main():
    started = perf_counter()
    reports = []
    for filename in ("noisy-markov-kinetics-probe.json", "noisy-markov-kinetics-n96-probe.json"):
        path = RESULTS/filename
        payload = json.loads(path.read_text())
        metadata = payload["metadata"]
        assert metadata["sweep_complete"]
        assert metadata["solver_script_sha256"] == sha256(HERE/"noisy_markov_design.py")
        assert metadata["driver_sha256"] == sha256(HERE/"noisy_markov_kinetics_probe.py")
        assert metadata["per_invocation_time_limit"] == 10 and metadata["gurobi_threads"] == 1
        assert all(value == "1" for value in metadata["blas_environment"].values())
        assert "STYLIZED" in metadata["covariance_model"]
        assert len(payload["results"]) == 2
        for index in range(2):
            reports.append(audit_case(path, payload, index))
            print(json.dumps({key: reports[-1][key] for key in
                             ("n", "regime", "max_sensitivity_error", "certified_gap")}), flush=True)
    report = {
        "status": "passed", "review_script_sha256": sha256(Path(__file__)),
        "numpy_version": np.__version__, "scipy_version": scipy.__version__, "mpmath_version": mp.__version__,
        "scope": "Independent augmented mass balances, saved data and objectives, local information mixtures, exact certificate replay and dense high-precision incumbent check. No solver reruns or general certificate library retest.",
        "wall_seconds": perf_counter()-started, "cases": reports,
        "counts": {"cases": len(reports), "augmented_ode_sensitivity_entries": sum(r["augmented_ode_sensitivity_entries"] for r in reports),
                   "high_precision_augmented_expm_rows": sum(r["high_precision_augmented_expm_rows"] for r in reports),
                   "saved_support_paths": sum(r["support_path_count"] for r in reports), "exact_certificate_replays": len(reports)},
    }
    output = RESULTS/"noisy-markov-kinetics-independent-review.json"
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "counts": report["counts"], "wall_seconds": report["wall_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
