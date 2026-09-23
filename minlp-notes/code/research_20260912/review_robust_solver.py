"""Independent reconstruction of robust kinetic solver results and edge cases.

Run with one BLAS thread. Independent information uses Cholesky whitening;
local conditionals and scalar pricing are rebuilt here, without author pricing.
Only explicitly labeled behavioral checks call the implementation under review.
"""

import hashlib
import json
import math
from itertools import combinations
from pathlib import Path
from time import perf_counter
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
import scipy
from scipy.linalg import expm, expm_frechet, solve_triangular
import robust_kinetic_design as implementation


HERE = Path(__file__).resolve().parent
REPORT = {"source_sha256": hashlib.sha256((HERE / "robust_kinetic_design.py").read_bytes()).hexdigest(),
          "core_sha256": hashlib.sha256((HERE / "noisy_markov_design.py").read_bytes()).hexdigest(),
          "numpy": np.__version__, "scipy": scipy.__version__, "residuals": {}, "cases": []}


def close(name, actual, expected, tolerance=2e-8):
    residual = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
    REPORT["residuals"][name] = max(residual, REPORT["residuals"].get(name, 0.0))
    assert residual <= tolerance, (name, residual, actual, expected)


def ld(matrix):
    sign, value = np.linalg.slogdet(matrix)
    assert sign > 0
    return float(value)


class IndependentModel:
    def __init__(self, records, offsets, L):
        self.F = np.stack([record["F"] for record in records])
        self.prior = np.stack([record["prior"] for record in records])
        self.q, self.n, self.p = self.F.shape
        self.k = records[0]["k"]
        self.offsets = np.asarray(offsets)
        self.L = min(L, self.n - 1)
        record = records[0]
        self.rho, self.latent, self.nugget = [record[key] for key in ("rho", "latent_variance", "nugget_variance")]
        distance = abs(np.arange(self.n)[:, None] - np.arange(self.n))
        self.R = self.latent * self.rho ** distance + self.nugget * np.eye(self.n)
        self.cache = {}

    def true(self, path):
        path = tuple(path)
        if path not in self.cache:
            result = self.prior.copy()
            if path:
                C = np.linalg.cholesky(self.R[np.ix_(path, path)])
                for s in range(self.q):
                    whitened = solve_triangular(C, self.F[s, list(path)], lower=True)
                    result[s] += whitened.T @ whitened
            self.cache[path] = np.array([ld(matrix) for matrix in result])
        return self.cache[path]

    def score(self, path):
        return float(np.min(self.true(path) - self.offsets))

    def arc(self, t, history):
        adjusted = self.F[:, t].copy()
        variance = self.R[t, t]
        if history:
            C = np.linalg.cholesky(self.R[np.ix_(history, history)])
            cross = self.R[history, t]
            coeff = solve_triangular(C.T, solve_triangular(C, cross, lower=True), lower=False)
            variance -= cross @ coeff
            adjusted -= np.einsum("h,shp->sp", coeff, self.F[:, history])
        return np.einsum("si,sj->sij", adjusted, adjusted) / variance

    def local(self, path):
        result = self.prior.copy()
        for i, t in enumerate(path):
            result += self.arc(t, [j for j in path[:i] if t - j <= self.L])
        return result

    def all_arcs(self):
        if not hasattr(self, "arcs"):
            self.arcs = np.zeros((self.n, 1 << self.L, self.q, self.p, self.p))
            for t in range(self.n):
                for mask in range(1 << min(t, self.L)):
                    if mask.bit_count() < self.k:
                        history = [t - j - 1 for j in range(min(t, self.L)) if mask & (1 << j)]
                        self.arcs[t, mask] = self.arc(t, history)
        return self.arcs

    def price(self, gradients):
        scores = np.einsum("sij,tmsji->tm", gradients, self.all_arcs())
        states = {(0, 0): (0., ())}
        mask_limit = (1 << self.L) - 1
        for t in range(self.n):
            updated = {}
            for (count, history), (value, path) in states.items():
                shifted = (history << 1) & mask_limit
                if count + self.n - t - 1 >= self.k:
                    key = (count, shifted)
                    if key not in updated or value > updated[key][0]:
                        updated[key] = (value, path)
                if count < self.k:
                    key = (count + 1, shifted | int(self.L > 0))
                    candidate = value + scores[t, history]
                    if key not in updated or candidate > updated[key][0]:
                        updated[key] = (candidate, path + (t,))
            states = updated
        return max(states.values())

    def delta(self):
        r = abs(self.rho)
        if not r or not self.latent or self.L >= self.n - 1:
            return 0.
        gain = self.latent / (self.latent + self.nugget)
        return 2 * self.latent / self.nugget * r ** (self.L + 1) / (1 - r) * (1 + gain * sum(r ** j for j in range(1, self.L + 1)))


def reference_check(model, index, reference):
    result = reference["hull"]
    close("individual_selected_scores", model.true(result["selected"])[index], result["true_lower_bound"])
    matrices = np.stack([model.local(tuple(row["selected"]))[index] for row in result["hull_support"]])
    weights = np.array([row["weight"] for row in result["hull_support"]])
    close("individual_support", matrices, [row["information"] for row in result["hull_support"]])
    close("individual_simplex", weights.sum(), 1.)
    assert min(weights) >= 0
    close("individual_mixture", np.einsum("a,aij->ij", weights, matrices), result["hull_information"])
    uppers = [model.true(tuple(range(model.n)))[index]]
    for prior_aware, key in [(False, "upper_bound_witness"), (True, "prior_aware_witness")]:
        witness = result[key]
        N = np.array(witness["N" if prior_aware else "hull_information"])
        inverse = np.linalg.inv(N)
        scale = 1 / (1 - model.delta()) if prior_aware else 1.
        H = np.zeros_like(model.prior)
        H[index] = scale * inverse
        price, path = model.price(H)
        close("individual_witness_price", price, witness["linear_price_excluding_prior"])
        saved_path = tuple(witness["priced_selection"])
        close("individual_witness_path", price, np.einsum("sij,sji->", H, model.local(saved_path) - model.prior))
        upper = ld(N) - model.p + np.trace(inverse @ model.prior[index]) + price
        close("individual_witness_bound", upper, witness["true_upper_bound" if prior_aware else "surrogate_upper_bound"])
        uppers.append(upper if prior_aware else upper - model.p * math.log1p(-model.delta()))
    close("individual_true_upper", min(uppers), result["true_upper_bound"])


def independent_greedy(model):
    count = 1
    path = ()
    for _ in range(model.k):
        candidates = [tuple(sorted(path + (t,))) for t in range(model.n) if t not in path]
        count += len(candidates)
        path = max(candidates, key=model.score)
    greedy = path
    exchanges = 0
    while True:
        candidates = [tuple(sorted(set(path) - {dropped} | {added})) for dropped in path for added in range(model.n) if added not in path]
        count += len(candidates)
        neighbor = max(candidates, key=model.score) if candidates else path
        if model.score(neighbor) <= model.score(path) + 1e-11:
            return greedy, path, exchanges, count
        path = neighbor
        exchanges += 1


def neighbors(model, path):
    paths = [tuple(sorted(set(path) - {dropped} | {added})) for dropped in path for added in range(model.n) if added not in path]
    best = max(paths, key=model.score) if paths else path
    return {"neighbors": len(paths), "best_neighbor": best, "best_neighbor_score": model.score(best),
            "improvement": model.score(best) - model.score(path)}


def saved_case(n):
    started = perf_counter()
    data = json.loads((HERE / "results" / f"robust-kinetic-n{n}.json").read_text())
    assert data["metadata"]["reviewed_core_sha256"] == REPORT["core_sha256"]
    model = IndependentModel(data["scenarios"], data["offsets"], data["L"])
    sensitivity_error = 0.
    swap_error = 0.
    for scenario in data["scenarios"]:
        kinetics = scenario["kinetics"]
        a, b, c = [kinetics[name] for name in ["A0", "k1", "k2"]]
        K = np.array([[-b, 0.], [b, -c]])
        direction_b = np.array([[-b, 0.], [b, 0.]])
        direction_c = np.array([[0., 0.], [0., -c]])
        initial = np.array([a, 0.])
        rows = []
        for t in kinetics["times"]:
            mean = (expm(t * K) @ initial)[1]
            rows.append([mean, (expm_frechet(t * K, t * direction_b, compute_expm=False) @ initial)[1],
                         (expm_frechet(t * K, t * direction_c, compute_expm=False) @ initial)[1]])
            swapped = (a * b / c) * c / (b - c) * (np.exp(-c * t) - np.exp(-b * t))
            swap_error = max(swap_error, abs(mean - swapped))
        sensitivity_error = max(sensitivity_error, float(np.max(abs(np.asarray(rows) - scenario["F"]))))
    close("matrix_exponential_sensitivities", sensitivity_error, 0., 1e-12)
    close("rate_swap_ambiguity", swap_error, 0., 1e-12)
    for i, reference in enumerate(data["references"]):
        reference_check(model, i, reference)
    result = data["robust"]
    lower = np.array([row["hull"]["true_lower_bound"] for row in data["references"]])
    upper = np.array([row["hull"]["true_upper_bound"] for row in data["references"]])
    close("offsets", lower, data["offsets"])
    support = [tuple(row["selected"]) for row in result["hull_support"]]
    blocks = np.array([model.local(path) for path in support])
    weights = np.array([row["weight"] for row in result["hull_support"]])
    close("shared_support_blocks", blocks, [row["scenario_information"] for row in result["hull_support"]])
    close("shared_simplex", weights.sum(), 1.)
    assert min(weights) >= 0
    mixture = np.einsum("a,asij->sij", weights, blocks)
    close("shared_mixture", mixture, result["hull_information"])
    close("shared_mixture_value", min(ld(matrix) - offset for matrix, offset in zip(mixture, lower)), result["surrogate_hull_value"])
    bounds = [model.score(tuple(range(n)))]
    for name in ["upper_bound_witness", "prior_aware_witness"]:
        witness = result[name]
        dual = np.asarray(witness["dual_weights"])
        close("witness_simplex", dual.sum(), 1.)
        assert min(dual) >= 0
        scale = 1 / (1 - model.delta()) if witness["prior_aware"] else 1.
        matrices = np.asarray(witness["hull_information"])
        N = model.prior + scale * (matrices - model.prior)
        close("tangent_references", N, witness["tangent_reference_information"])
        H = dual[:, None, None] * scale * np.linalg.inv(N)
        close("tangent_gradients", H, witness["arc_gradient_blocks"])
        constants = np.array([ld(N[s]) - lower[s] - model.p + np.trace(np.linalg.solve(N[s], model.prior[s])) for s in range(model.q)])
        close("tangent_constants", constants, witness["scenario_constants"])
        price, path = model.price(H)
        close("shared_witness_price", price, witness["linear_price_excluding_prior"])
        close("shared_witness_path", price, np.einsum("sij,sji->", H, model.local(tuple(witness["priced_selection"])) - model.prior))
        value = dual @ constants + price
        close("shared_witness_upper", value, witness["upper_bound"])
        bounds.append(value if witness["prior_aware"] else value - model.p * math.log1p(-model.delta()))
    close("shared_true_upper", min(bounds), result["true_upper_bound"])
    candidates = support + [tuple(result[name]["priced_selection"]) for name in ["upper_bound_witness", "prior_aware_witness"]]
    close("selected_is_best_retained_path", max(model.score(path) for path in candidates), result["true_lower_bound"])
    for name in ["robust", "greedy_exchange"]:
        run = data[name]
        evaluation = data["evaluations"][name]
        path = tuple(run["selected"])
        assert len(path) == model.k and len(set(path)) == model.k
        values = model.true(path)
        close("selected_scenario_logdet", values, run["selected_scenario_logdet"])
        close("selected_lower_bound", model.score(path), run["true_lower_bound"])
        close("standardized_score_lower", min(values - upper), evaluation["standardized_score_lower"])
        close("standardized_score_upper", min(values - lower), evaluation["standardized_score_upper"])
        close("standardized_efficiency_lower", np.exp((values - upper) / model.p), evaluation["scenario_efficiency_lower"])
        close("standardized_efficiency_upper", np.exp((values - lower) / model.p), evaluation["scenario_efficiency_upper"])
        assert run["wall_seconds"] <= run["time_limit"]
    greedy_started = perf_counter()
    greedy, completed, exchanges, evaluations = independent_greedy(model)
    greedy_wall = perf_counter() - greedy_started
    stored = data["greedy_exchange"]
    assert greedy == tuple(stored["greedy_selected"])
    assert completed == tuple(stored["selected"])
    assert (exchanges, evaluations) == (stored["accepted_exchanges"], stored["objective_evaluations"])
    close("reference_timing_sum", sum(row["hull"]["wall_seconds"] for row in data["references"]), data["reference_wall_seconds"])
    close("robust_pipeline_timing_sum", data["reference_wall_seconds"] + result["wall_seconds"], data["robust_pipeline_seconds"])
    close("greedy_pipeline_timing_sum", data["reference_wall_seconds"] + stored["wall_seconds"], data["greedy_pipeline_seconds"])
    elapsed_components = data["reference_wall_seconds"] + result["wall_seconds"] + stored["wall_seconds"]
    assert data["pipeline_wall_seconds"] >= elapsed_components
    row = {"n": n, "k": model.k, "artifact_source_sha256": data["metadata"]["source_sha256"],
           "robust_status": result["status"], "greedy_status": stored["status"],
           "robust_fixed_offset_score": result["true_lower_bound"], "greedy_fixed_offset_score": stored["true_lower_bound"],
           "numerical_upper": result["true_upper_bound"], "robust_single_exchange": neighbors(model, tuple(result["selected"])),
           "greedy_single_exchange": neighbors(model, completed), "independent_greedy_seconds": greedy_wall,
           "greedy_exchanges": exchanges, "greedy_evaluations": evaluations,
           "recorded_seconds": {key: data[key] for key in ["reference_wall_seconds", "robust_pipeline_seconds", "greedy_pipeline_seconds", "pipeline_wall_seconds"]},
           "standardized_efficiency_lower": {name: min(data["evaluations"][name]["scenario_efficiency_lower"]) for name in ["robust", "greedy_exchange", "nominal_central"]},
           "standardized_optimality_ratio_lower": {name: math.exp((data["evaluations"][name]["standardized_score_lower"] - min(0., result["true_upper_bound"])) / model.p) for name in ["robust", "greedy_exchange"]},
           "all_checks_seconds": perf_counter() - started}
    REPORT["cases"].append(row)
    print(json.dumps(row), flush=True)


def tiny_checks():
    rng = np.random.default_rng(271828)
    tests = []
    for rho in [-.45, .4]:
        n, p, k, q = 8, 2, 3, 3
        scenarios = tuple(implementation.NoisyDesign(rng.normal(size=(n, p)), rho, .5, 1., np.diag([.2 + .1 * s, .4 + .2 * s]), k) for s in range(q))
        records = [{"F": s.F, "prior": s.prior, "rho": rho, "latent_variance": .5, "nugget_variance": 1., "k": k} for s in scenarios]
        paths = list(combinations(range(n), k))
        for L in [0, 2, 5, 7]:
            model = IndependentModel(records, np.zeros(q), L)
            true = np.array([model.true(path) for path in paths])
            offsets = true.max(axis=0)
            model.offsets = offsets
            design = implementation.RobustDesign(scenarios, offsets)
            oracle = implementation.CalendarOracle(design.pricing_container(), L)
            blocks = np.array([model.local(path) for path in paths])
            for path, block in zip(paths, blocks):
                actual = implementation.scenario_blocks(oracle.information(path), q, p)
                close("tiny_shared_blocks", actual, block)
            if L == 7:
                close("full_history_true_values", [[ld(matrix) for matrix in block] for block in blocks], true)
            chosen = rng.choice(len(paths), 5, replace=False)
            w = rng.uniform(size=5); w /= w.sum()
            mix = np.einsum("a,asij->sij", w, blocks[chosen])
            dual = rng.uniform(size=q); dual /= dual.sum()
            tangent, priced, witness = implementation.tangent_price(design, oracle, mix, dual)
            H = np.array(witness["arc_gradient_blocks"])
            direct = np.einsum("sij,asji->a", H, blocks - model.prior)
            close("tiny_exhaustive_price", max(direct), witness["linear_price_excluding_prior"])
            close("tiny_returned_path_price", direct[paths.index(priced)], max(direct))
            assert tangent >= max(min(ld(matrix) - offset for matrix, offset in zip(block, offsets)) for block in blocks) - 1e-8
            optimum = float(np.min(true - offsets, axis=1).max())
            if model.delta() < 1:
                prior_bound, _, _ = implementation.tangent_price(design, oracle, mix, dual, prior_aware=True)
                assert prior_bound >= optimum - 1e-8
                for path, block in zip(paths, blocks):
                    indices = list(path)
                    for s in range(q):
                        F = model.F[s, indices]
                        exact = model.prior[s] + F.T @ np.linalg.solve(model.R[np.ix_(indices, indices)], F)
                        majorant = model.prior[s] + (block[s] - model.prior[s]) / (1 - model.delta())
                        assert min(np.linalg.eigvalsh(majorant - exact)) >= -1e-8
            values, gradients = implementation.values_and_gradients(blocks[chosen], w, offsets)
            for j in range(5):
                h = np.zeros(5); h[j] = 1e-6
                plus = np.einsum("a,asij->sij", w + h, blocks[chosen])
                minus = np.einsum("a,asij->sij", w - h, blocks[chosen])
                finite = np.array([(ld(A) - ld(B)) / 2e-6 for A, B in zip(plus, minus)])
                close("tiny_mixture_gradient", finite, gradients[:, j], 2e-7)
            result = implementation.solve_robust_hull(design, L, time_limit=10)
            assert result["true_lower_bound"] <= optimum + 1e-8 <= result["true_upper_bound"] + 2e-8
            assert result["surrogate_hull_gap"] >= -1e-7
            tests.append({"rho": rho, "L": L, "schedules": len(paths), "optimum": optimum, "status": result["status"], "lower": result["true_lower_bound"], "upper": result["true_upper_bound"]})
    REPORT["tiny_exhaustive"] = tests
    analytic = np.array([[[[4.]], [[1.]]], [[[1.]], [[2.]]]])
    # 1 + 3w = 2 - w => w = 1/4. KKT scenario weights are 1/4, 3/4.
    weights, dual, status = implementation.correct_mixture(analytic, np.array([.9, .1]), np.zeros(2), perf_counter() + 5)
    close("asymmetric_analytic_mixture", weights, [.25, .75], 1e-6)
    close("asymmetric_analytic_dual_sign", dual, [.25, .75], 1e-6)
    behavior = []
    for multipliers in [[0., -2., 3.], [0., 0., 0.], [0., math.nan, 1.], [0., 1e308, 1e308]]:
        fake = SimpleNamespace(success=False, message="review_injected_failure", nit=1, multipliers=multipliers)
        with patch.object(implementation, "minimize", return_value=fake):
            try:
                w, dual, status = implementation.correct_mixture(analytic, np.array([.25, .75]), np.zeros(2), perf_counter() + 5)
                valid = np.isfinite(dual).all() and min(dual) >= 0 and abs(sum(dual) - 1.) < 1e-12
                behavior.append({"multipliers": [str(x) for x in multipliers], "simplex_valid": bool(valid), "dual": dual.tolist(), "status": status})
            except ValueError as error:
                behavior.append({"multipliers": [str(x) for x in multipliers], "rejected": str(error)})
    REPORT["unsuccessful_slsqp_dual_checks"] = behavior
    scalar = implementation.NoisyDesign(np.ones((2, 1)), 0., 0., 1., np.array([[2.]]), 1)
    scalar_design = implementation.RobustDesign((scalar, scalar), np.zeros(2))
    scalar_oracle = implementation.CalendarOracle(scalar_design.pricing_container(), 0)
    scalar_matrices = implementation.scenario_blocks(scalar_oracle.information((0,)), 2, 1)
    extreme_bound, _, extreme_witness = implementation.tangent_price(scalar_design, scalar_oracle, scalar_matrices, np.array([1e308, 1e308]))
    close("extreme_finite_dual_bound", extreme_bound, math.log(3.))
    REPORT["extreme_finite_dual_regression"] = {"bound": extreme_bound, "dual": extreme_witness["dual_weights"]}
    cap = implementation.solve_robust_hull(design, 7, time_limit=1e-12)
    refusal = implementation.solve_robust_hull(design, 7, max_memory_mb=1e-10)
    assert cap["status"] == "time_limit" and cap["true_lower_bound"] is None
    assert refusal["status"] == "memory_limit" and refusal["true_lower_bound"] is None
    partial = implementation.solve_robust_hull(design, 7, max_rounds=1)
    assert partial["status"] == "iteration_limit" and partial["true_lower_bound"] <= optimum + 1e-8 <= partial["true_upper_bound"] + 2e-8
    REPORT["limits"] = {"immediate_deadline": cap["status"], "memory_refusal": refusal["status"], "one_round": partial["status"],
                        "interpretation": "Cooperative elapsed-time checks and memory estimates; no process-level hard cap."}
    original_oracle = implementation.CalendarOracle
    calls = 0

    def capped_oracle(*args, **kwargs):
        oracle = original_oracle(*args, **kwargs)
        original_price = oracle.price

        def price(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls > 1:
                raise implementation.TimeBudgetExceeded("independent injected pricing deadline")
            return original_price(*args, **kwargs)

        oracle.price = price
        return oracle

    with patch.object(implementation, "CalendarOracle", capped_oracle):
        interrupted = implementation.solve_robust_hull(design, 7)
    assert interrupted["status"] == "time_limit"
    assert interrupted["upper_bound_witness"] is not None
    assert interrupted["true_lower_bound"] <= optimum + 1e-8 <= interrupted["true_upper_bound"] + 2e-8
    REPORT["limits"]["interrupted_after_completed_price"] = {key: interrupted[key] for key in ["status", "selected", "true_lower_bound", "true_upper_bound", "pricing_rounds"]}
    extremes = []
    for count in [0, 3]:
        scenario = implementation.NoisyDesign(np.array([[1.], [2.], [3.]]), .2, 1., 1., np.array([[.4]]), count)
        singleton = implementation.RobustDesign((scenario,), np.array([.2]))
        fixed_path = tuple(range(3)) if count else ()
        result = implementation.solve_robust_hull(singleton, 2)
        close("exact_count_boundaries", result["true_lower_bound"], singleton.true_score(fixed_path))
        close("exact_count_boundary_upper", result["true_upper_bound"], singleton.true_score(fixed_path))
        extremes.append({"k": count, "status": result["status"], "selected": result["selected"]})
    REPORT["single_scenario_count_boundaries"] = extremes


def incumbent_status_regression():
    arrays = .2 * np.array([[[-4, 0], [0, 2], [4, 3], [0, 0], [4, 1], [-3, 0], [0, 4]],
                            [[0, 0], [-2, 0], [-2, 2], [-3, -3], [-1, 2], [-1, 1], [1, 0]],
                            [[4, 0], [2, -1], [-3, 0], [0, 3], [0, 4], [-3, -3], [-1, -2]]])
    scenarios = tuple(implementation.NoisyDesign(F, .5, 1., 1., .1 * np.eye(2), 3) for F in arrays)
    offsets = np.max([[s.true_objective(path) for s in scenarios] for path in combinations(range(7), 3)], axis=0)
    design = implementation.RobustDesign(scenarios, offsets)
    result = implementation.greedy_exchange(design)
    path = tuple(result["selected"])
    candidates = [tuple(sorted(set(path) - {dropped} | {added})) for dropped in path for added in range(7) if added not in path]
    best = max(candidates, key=design.true_score)
    improvement = design.true_score(best) - result["true_lower_bound"]
    status_accurate = result["status"] != "single_exchange_local_optimum" or improvement <= 1e-10
    REPORT["retained_seed_status_regression"] = {"result": result, "best_neighbor": best,
                                                "neighbor_improvement": improvement, "status_accurate": status_accurate}
    assert status_accurate, REPORT["retained_seed_status_regression"]


def main():
    started = perf_counter()
    tiny_checks()
    incumbent_status_regression()
    for n in [48, 96]:
        saved_case(n)
    REPORT["status"] = "passed_except_reported_edge_cases" if any(not row.get("simplex_valid", True) for row in REPORT["unsuccessful_slsqp_dual_checks"]) else "passed"
    REPORT["wall_seconds"] = perf_counter() - started
    assert REPORT["source_sha256"] == hashlib.sha256((HERE / "robust_kinetic_design.py").read_bytes()).hexdigest()
    path = HERE / "results" / "robust-solver-independent-review.json"
    path.write_text(json.dumps(REPORT, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": REPORT["status"], "residuals": REPORT["residuals"], "wall_seconds": REPORT["wall_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
