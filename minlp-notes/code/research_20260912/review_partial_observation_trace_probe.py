"""Independent bounded audit of the partial-observation weighted-trace probe."""

from hashlib import sha256
from itertools import combinations
import json
import math
from pathlib import Path
import platform
from time import perf_counter
from unittest.mock import patch

import numpy as np
import scipy
from scipy.linalg import expm, expm_frechet

import partial_observation_trace_probe as target
import noisy_markov_design
from review_noisy_markov_solver import Reference as GeneralReference


HERE = Path(__file__).resolve().parent
OUTPUT = HERE/"results/partial-observation-trace-independent-review.json"


def close(x, y, label, atol=2e-8):
    if not np.allclose(x, y, atol=atol, rtol=2e-10):
        raise AssertionError((label, x, y))


class Reference(GeneralReference):
    def __init__(self, design, L):
        self.d, self.L, self.cache = design, min(L, design.n-1), {}
        A, H = np.diag([.4, .2]), np.array([[.6, .8]])
        Q = design.variance*(np.eye(2)-A@A.T)
        self.R = design.variance*np.eye(design.n)
        # Independent latent-innovation loading construction, then projection.
        for u in range(design.n):
            G = np.zeros((design.n, 2))
            state = np.eye(2)
            for t in range(u, design.n):
                G[t] = H@state
                state = A@state
            covariance = design.variance*np.eye(2) if u == 0 else Q
            self.R += G@covariance@G.T

    def trace(self, selected, W):
        selected = tuple(sorted(selected))
        F = self.d.F[list(selected)]
        J = self.d.prior+F.T@np.linalg.solve(self.R[np.ix_(selected, selected)], F)
        return float(np.trace(W@J))

    def liu(self, z, a, W):
        diagonal = z/a
        S = self.R-a*np.eye(self.d.n)
        V = np.linalg.solve(np.eye(self.d.n)+S*diagonal, self.d.F)
        J = self.d.prior+self.d.F.T@(diagonal[:, None]*V)
        return float(np.trace(W@J)), np.einsum("ij,jk,ik->i", V, W, V)/a


def delta(n, L):
    if L >= n-1:
        return 0.
    gamma = .4
    # Independently sum the finite near-pair majorants, with a geometric far tail.
    near = sum(sum(gamma**(h+2*d) for d in range(L+1-h, L+1)) for h in range(1, L+1))
    return 2*(gamma**(L+1)/(1-gamma)+near)


def audit_dp(design, W, L, result, ref):
    if result["true_lower_bound"] is None:
        assert result["status"] in ("memory_limit", "time_limit")
        assert result["surrogate_optimum"] is None
        return
    selected = tuple(result["selected"])
    assert len(selected) == design.k and len(set(selected)) == len(selected)
    close(result["true_lower_bound"], ref.trace(selected, W), "true DP incumbent")
    full = ref.trace(tuple(range(design.n)), W)
    upper = full
    if result["surrogate_optimum"] is not None:
        price, _ = ref.price(W)
        prior_trace = float(np.trace(W@design.prior))
        close(result["surrogate_optimum"], prior_trace+price, "independent tuple-DP price")
        surrogate_selected = tuple(result["surrogate_selected"])
        true, surrogate, _ = ref.information(surrogate_selected)
        close(result["selected_surrogate_information_matrix"], surrogate, "saved surrogate matrix")
        close(result["selected_true_information_matrix"], ref.information(selected)[0], "saved true matrix")
        close(np.trace(W@surrogate), prior_trace+price, "surrogate schedule recovery")
        close(result["surrogate_selected_true_information"], np.trace(W@true), "surrogate schedule true value")
        close(sum(result["selected_arc_trace"]), price, "saved arc trace sum")
        dd = delta(design.n, L)
        close(result["delta"], dd, "partial-observation delta")
        if dd < 1:
            transferred = prior_trace+price/(1-dd)
            close(result["transferred_true_upper_bound"], transferred, "partial-observation transfer")
            upper = min(upper, transferred)
        else:
            assert result["transferred_true_upper_bound"] is None
        assert result["pricing_calls_completed"] == 1
    else:
        assert result["pricing_calls_completed"] == 0
    close(result["true_upper_bound"], upper, "reported true DP upper")


def audit_dense(design, W, result, ref):
    close(result["true_lower_bound"], ref.trace(tuple(result["selected"]), W), "dense true incumbent")
    assert 0 < result["split_a"] < np.linalg.eigvalsh(ref.R)[0]
    upper = ref.trace(tuple(range(design.n)), W)
    witness = result["upper_witness"]
    if witness is not None:
        z = np.array(witness["z"])
        value, gradient = ref.liu(z, result["split_a"], W)
        close(value, witness["value"], "trace tangent value")
        close(gradient, witness["gradient"], "trace tangent gradient")
        price = sum(sorted(gradient, reverse=True)[:design.k])
        close(price, witness["linear_price"], "top-k tangent price")
        upper = min(upper, value-gradient@z+price)
    close(result["true_upper_bound"], upper, "reconstructed dense upper")
    if result["continuous_z"] is not None:
        z = np.array(result["continuous_z"])
        close(z.sum(), design.k, "fractional exact count", atol=1e-8)
        assert np.min(z) >= 0 and np.max(z) <= 1
        value = ref.liu(z, result["split_a"], W)[0]
        close(value, result["continuous_value"], "fractional trace value")
        close(upper-value, result["continuous_tangent_gap"], "fractional tangent gap")
        close(result["rounded_true_information"], ref.trace(tuple(result["rounded_selected"]), W), "rounded true trace")


def main():
    started = perf_counter()
    names = ("partial_observation_trace_probe.py", "noisy_markov_design.py",
             "noisy_markov_kinetics_probe.py", "review_noisy_markov_solver.py", Path(__file__).name)
    source = {name: (HERE/name).read_bytes() for name in names}
    rng = np.random.default_rng(827409)
    counts = {k: 0 for k in ("covariance_checks", "local_matrices", "spectral_checks", "dp_enumerations",
                             "dp_solves", "liu_binary_identities", "liu_derivative_directions",
                             "liu_tangent_checks", "liu_solves", "saved_dp_records", "saved_dense_records",
                             "greedy_candidate_evaluations", "exchange_neighbors", "kinetic_derivatives",
                             "invalid_inputs")}
    worst = {"covariance": 0., "local_information": 0., "liu_scaled_derivative": 0., "kinetic_derivative": 0.}
    for n, k in ((1, 0), (1, 1), (6, 0), (6, 1), (6, 3), (6, 6)):
        F = rng.normal(size=(n, 3))
        prior = np.diag([0., .02, .03])
        d = target.TwoModeDesign(F, prior, k)
        vector = np.array([1., 2., -1.])
        for W in (np.eye(3), np.outer(vector, vector), np.zeros((3, 3))):
            subsets = list(combinations(range(n), k))
            for L in sorted(set((0, min(2, n-1), n-1))):
                ref, oracle = Reference(d, L), target.CalendarOracle(d, L, max_paths=1)
                error = float(np.max(abs(ref.R-d.covariance())))
                worst["covariance"] = max(worst["covariance"], error)
                close(ref.R, d.covariance(), "projected latent covariance")
                counts["covariance_checks"] += 1
                scores, true_scores = [], []
                for s in subsets:
                    true, surrogate, C = ref.information(s)
                    close(d.true_information(s), true, "true matrix")
                    close(oracle.information(s), surrogate, "local matrix")
                    worst["local_information"] = max(worst["local_information"], float(np.max(abs(oracle.information(s)-surrogate))))
                    if L >= n-1:
                        close(surrogate, true, "full history")
                    if s:
                        assert max(abs(np.linalg.eigvalsh(C)-1)) <= delta(n, L)+1e-9
                        counts["spectral_checks"] += 1
                    scores.append(float(np.trace(W@surrogate)))
                    true_scores.append(float(np.trace(W@true)))
                    counts["local_matrices"] += 1
                price, _ = oracle.price(W)
                close(price+np.trace(W@prior), max(scores), "enumerated weighted trace price")
                counts["dp_enumerations"] += 1
                with patch.object(noisy_markov_design, "spectral_delta", side_effect=AssertionError("wrong scalar theorem")):
                    solved = target.solve_trace_dp(d, W, L, time_limit=2)
                audit_dp(d, W, L, solved, ref)
                assert solved["true_lower_bound"] <= max(true_scores)+1e-7 <= solved["true_upper_bound"]+2e-7
                counts["dp_solves"] += 1
            dense, ref = target.TraceLiuOracle(d, W), Reference(d, 0)
            for s in subsets:
                z = np.zeros(n)
                z[list(s)] = 1
                value, gradient = dense.value_gradient(z)
                expected, expected_gradient = ref.liu(z, dense.a, W)
                close(value, ref.trace(s, W), "weighted Liu binary identity")
                close((value, *gradient), (expected, *expected_gradient), "independent weighted Liu boundary")
                counts["liu_binary_identities"] += 1
            z = rng.uniform(.2, .8, n)
            value, gradient = dense.value_gradient(z)
            direction = rng.normal(size=n)
            direction /= np.linalg.norm(direction)
            h = 2e-5
            f = [dense.value_gradient(z+j*h*direction)[0] for j in (-2, -1, 1, 2)]
            finite = (f[0]-8*f[1]+8*f[2]-f[3])/(12*h)
            predicted = gradient@direction
            error = abs(finite-predicted)/max(1., abs(predicted))
            assert error < 2e-8
            worst["liu_scaled_derivative"] = max(worst["liu_scaled_derivative"], error)
            counts["liu_derivative_directions"] += 1
            for s in subsets:
                endpoint = np.zeros(n)
                endpoint[list(s)] = 1
                assert ref.trace(s, W) <= value+gradient@(endpoint-z)+1e-7
                counts["liu_tangent_checks"] += 1
            dense_result = target.solve_trace_relaxation(d, W, time_limit=2)
            audit_dense(d, W, dense_result, ref)
            assert dense_result["true_upper_bound"] >= max(ref.trace(s, W) for s in subsets)-1e-7
            counts["liu_solves"] += 1
    retained = []
    d = target.TwoModeDesign(np.ones((7, 1)), np.zeros((1, 1)), 3)
    for L in (0, 1):
        result = target.solve_trace_dp(d, np.ones((1, 1)), L)
        audit_dp(d, np.ones((1, 1)), L, result, Reference(d, L))
        assert result["selected"] != result["surrogate_selected"]
        assert result["true_lower_bound"] > result["surrogate_selected_true_information"]
        retained.append({"L": L, "selected": result["selected"], "surrogate_selected": result["surrogate_selected"],
                         "true_lower_bound": result["true_lower_bound"], "surrogate_selected_true_information": result["surrogate_selected_true_information"]})
    path = HERE/"results/partial-observation-trace-probe.json"
    saved = json.loads(path.read_text())
    assert saved["complete"]
    meta = saved["metadata"]
    assert meta["source_sha256"] == sha256(source[names[0]]).hexdigest()
    assert meta["calendar_source_sha256"] == sha256(source["noisy_markov_design.py"]).hexdigest()
    assert meta["kinetics_source_sha256"] == sha256(source["noisy_markov_kinetics_probe.py"]).hexdigest()
    assert all(x == "1" for x in meta["blas_environment"].values())
    saved_rows = []
    for row in saved["results"]:
        d = target.TwoModeDesign(np.array(row["F"]), np.array(row["prior"]), row["k"], row["variance"])
        W, true_ref = np.array(row["W"]), Reference(d, 0)
        assert row["p"] == 3 and d.k == d.n//3
        for dp in row["dp"]:
            audit_dp(d, W, dp["L"], dp, Reference(d, dp["L"]))
            close(dp["selected_times"], np.array(row["kinetics"]["candidate_times"])[list(dp["selected"])], "selected physical times")
            counts["saved_dp_records"] += 1
        dense_result = row["liu_continuous"]
        audit_dense(d, W, dense_result, true_ref)
        counts["saved_dense_records"] += 1
        candidates = row["dp"]+[row["greedy_exchange"]]
        supplied = max(candidates, key=lambda x: x["true_lower_bound"])["selected"]
        assert tuple(supplied) == tuple(dense_result["disclosed_initial_selected"])
        close(dense_result["true_lower_bound"], true_ref.trace(tuple(supplied), W), "shared dense incumbent")
        assert dense_result["rounded_true_information"] < dense_result["true_lower_bound"]
        greedy = row["greedy_exchange"]
        selected = tuple(greedy["selected"])
        score = true_ref.trace(selected, W)
        close(score, greedy["true_lower_bound"], "saved exchange incumbent")
        current = ()
        for _ in range(d.k):
            options = []
            for t in range(d.n):
                if t not in current:
                    proposed = tuple(sorted((*current, t)))
                    options.append((true_ref.trace(proposed, W), proposed))
                    counts["greedy_candidate_evaluations"] += 1
            current = max(options, key=lambda pair: pair[0])[1]
        assert current == tuple(greedy["greedy_selected"])
        close(true_ref.trace(current, W), greedy["greedy_information"], "independent greedy construction")
        for removed in selected:
            for added in range(d.n):
                if added not in selected:
                    neighbor = tuple(sorted((set(selected)-{removed}) | {added}))
                    assert true_ref.trace(neighbor, W) <= score+1e-8
                    counts["exchange_neighbors"] += 1
        kinetic = row["kinetics"]
        k1, k2, A0 = kinetic["k1"], kinetic["k2"], kinetic["A0"]
        G = np.array([[-k1, 0., 0.], [k1, -k2, 0.], [0., k2, 0.]])
        Es = [np.array([[-k1, 0., 0.], [k1, 0., 0.], [0., 0., 0.]]),
              np.array([[0., 0., 0.], [0., -k2, 0.], [0., k2, 0.]])]
        times = 12*np.arange(1, d.n+1)/d.n
        close(times, kinetic["candidate_times"], "fixed time grid")
        expected_F = []
        for t in times:
            B = A0*expm(t*G)[1, 0]
            expected_F.append([B]+[A0*expm_frechet(t*G, t*E, compute_expm=False)[1, 0] for E in Es])
            counts["kinetic_derivatives"] += 3
        error = float(np.max(abs(np.array(expected_F)-d.F)))
        assert error < 2e-12
        worst["kinetic_derivative"] = max(worst["kinetic_derivative"], error)
        close(np.array(expected_F)[:, 0], kinetic["mean_B"], "nominal concentration")
        best_dp = min(row["dp"], key=lambda x: x["true_upper_bound"])
        assert best_dp["true_upper_bound"] < dense_result["true_upper_bound"]
        assert all(x["wall_seconds"] > dense_result["wall_seconds"] for x in row["dp"])
        saved_rows.append({"n": d.n, "regime": row["regime"], "dp_lower": best_dp["true_lower_bound"],
                           "dp_upper": best_dp["true_upper_bound"], "greedy_lower": score,
                           "improvement_over_greedy": best_dp["true_lower_bound"]/score-1,
                           "loss_against_DP_schedule": 1-score/best_dp["true_lower_bound"],
                           "dense_upper": dense_result["true_upper_bound"],
                           "dense_lower_inherited": True, "dense_status": dense_result["status"]})
    validation_path = HERE/"results/partial-observation-trace-validation.json"
    old = json.loads(validation_path.read_text())
    assert old["metadata"]["source_sha256"] == sha256(source[names[0]]).hexdigest()
    F = np.random.default_rng(82739).integers(-10, 11, size=(10, 3))/10
    d, W = target.TwoModeDesign(F, .01*np.eye(3), 3), np.eye(3)
    for row in old["rows"]:
        ref = Reference(d, row["L"])
        audit_dp(d, W, row["L"], row["result"], ref)
        optimum = max(ref.trace(s, W) for s in combinations(range(10), 3))
        close(row["true_enumerated_optimum"], optimum, "saved true optimum")
        assert row["result"]["true_lower_bound"] <= optimum+1e-7 <= row["result"]["true_upper_bound"]+2e-7
    audit_dense(d, W, old["liu_continuous"], Reference(d, 0))
    cap_checks = []
    with patch.object(target.TwoModeDesign, "true_information", side_effect=AssertionError("objective evaluated before guard")):
        refused = target.solve_trace_dp(d, W, 6, max_memory_mb=1e-9)
        assert refused["status"] == "memory_limit" and refused["true_lower_bound"] is None
        expired = target.solve_trace_dp(d, W, 6, time_limit=1e-12)
        assert expired["status"] == "time_limit" and expired["true_lower_bound"] is None
    cap_checks += ["memory preflight before objectives", "initial deadline before objectives"]
    with patch.object(target.CalendarOracle, "price", side_effect=target.TimeBudgetExceeded("injected deadline")):
        interrupted = target.solve_trace_dp(d, W, 2)
        audit_dp(d, W, 2, interrupted, Reference(d, 2))
        assert interrupted["status"] == "time_limit" and interrupted["transferred_true_upper_bound"] is None
    cap_checks.append("incomplete price cannot create transferred upper bound")
    interrupted = target.solve_trace_relaxation(d, W, time_limit=1e-12)
    audit_dense(d, W, interrupted, Reference(d, 0))
    assert interrupted["status"] == "time_limit" and interrupted["upper_witness"] is None
    cap_checks.append("dense deadline retains true baseline bounds")
    invalid = [lambda: target.solve_trace_dp(d, -np.eye(3), 2),
               lambda: target.TwoModeDesign(F, -np.eye(3), 3),
               lambda: target.TwoModeDesign(F, np.eye(3), True),
               lambda: d.true_information((0, 0)), lambda: d.true_information((-1,)),
               lambda: d.true_information((.5,)), lambda: d.true_information((True,)),
               lambda: target.TraceLiuOracle(d, W).value_gradient([0]*9),
               lambda: target.TraceLiuOracle(d, W).value_gradient(np.full(10, np.nan)),
               lambda: target.TraceLiuOracle(d, W, split_fraction=1)]
    for call in invalid:
        try:
            call()
        except ValueError:
            counts["invalid_inputs"] += 1
        else:
            raise AssertionError("invalid input accepted")
    assert all((HERE/name).read_bytes() == data for name, data in source.items())
    report = {"status": "passed", "source_hashes": {name: sha256(data).hexdigest() for name, data in source.items()},
              "artifact_hashes": {path.name: sha256(path.read_bytes()).hexdigest(), validation_path.name: sha256(validation_path.read_bytes()).hexdigest()},
              "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
              "counts": counts, "maximum_errors": worst, "retained_better_seed_cases": retained,
              "saved_case_audits": saved_rows, "cap_checks": cap_checks, "wall_seconds": perf_counter()-started,
              "scope": "Original accepted partial-observation delta only; normalized refinement not used.",
              "limitations": ["Floating-point tests and bounds, not exact certification.",
                              "Shared discrete-incumbent generation is excluded from dense comparator time.",
                              "Application true optima are not exhaustively enumerated here."]}
    temp = OUTPUT.with_suffix(".json.tmp")
    temp.write_text(json.dumps(report, indent=2)+"\n")
    temp.replace(OUTPUT)
    print(json.dumps({key: report[key] for key in ("status", "counts", "maximum_errors", "saved_case_audits", "wall_seconds")}, indent=2))


if __name__ == "__main__":
    main()
