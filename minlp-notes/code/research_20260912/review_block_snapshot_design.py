"""Independent bounded audit of full-vector snapshot design and saved probes."""

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

import block_snapshot_design as target


HERE = Path(__file__).resolve().parent
OUTPUT = HERE/"results/block-snapshot-independent-review.json"


def check_close(x, y, label, atol=2e-9):
    if not np.allclose(x, y, atol=atol, rtol=atol):
        raise AssertionError((label, x, y))


class Reference:
    def __init__(self, design, L):
        self.d = design
        self.L = min(L, design.n-1)
        n, dim = design.n, design.d
        # Build the latent process from independent innovation loadings.
        Q = np.eye(dim)-design.A @ design.A.T
        blocks = [np.eye(dim)]+[Q]*(n-1)
        self.R = np.eye(n*dim)
        for u in range(n):
            G = np.zeros((n*dim, dim))
            state = np.eye(dim)
            for t in range(u, n):
                G[t*dim:(t+1)*dim] = state
                state = design.A @ state
            self.R += G @ blocks[u] @ G.T
        self.regressions = {}

    def indices(self, selected):
        return np.array([i*self.d.d+j for i in selected for j in range(self.d.d)], dtype=int)

    def true(self, selected):
        ids = self.indices(selected)
        f = self.d.F.reshape(-1)[ids]
        return float(self.d.prior+f @ np.linalg.solve(self.R[np.ix_(ids, ids)], f))

    def local(self, time, history):
        # Canonical chronological ages, using a late anchor instead of the
        # implementation's nearest-first order and anchor at L.
        ages = tuple(time-j for j in history)
        if ages not in self.regressions:
            anchor = self.d.n-1
            hi, ti = self.indices([anchor-age for age in ages]), self.indices([anchor])
            beta = self.R[np.ix_(ti, hi)] @ np.linalg.inv(self.R[np.ix_(hi, hi)])
            D = self.R[np.ix_(ti, ti)]-beta @ self.R[np.ix_(hi, ti)]
            self.regressions[ages] = beta, D
        beta, D = self.regressions[ages]
        adjusted = self.d.F[time]-beta @ self.d.F[list(history)].reshape(-1)
        return float(adjusted @ np.linalg.solve(D, adjusted))

    def surrogate(self, selected):
        return self.d.prior+sum(self.local(t, tuple(s for s in selected if t-self.L <= s < t))
                                for t in selected)

    def residual_spectrum(self, selected):
        dim, ids = self.d.d, self.indices(selected)
        transform, D = np.eye(len(ids)), np.zeros((len(ids), len(ids)))
        for i, t in enumerate(selected):
            history_positions = [j for j, s in enumerate(selected[:i]) if s >= t-self.L]
            history = [selected[j] for j in history_positions]
            hi, ti = self.indices(history), self.indices([t])
            beta = self.R[np.ix_(ti, hi)] @ np.linalg.inv(self.R[np.ix_(hi, hi)])
            rows = slice(i*dim, (i+1)*dim)
            for h, j in enumerate(history_positions):
                transform[rows, j*dim:(j+1)*dim] = -beta[:, h*dim:(h+1)*dim]
            D[rows, rows] = self.R[np.ix_(ti, ti)]-beta @ self.R[np.ix_(hi, ti)]
        if not len(ids):
            return np.empty(0)
        root = np.linalg.cholesky(D)
        B = np.linalg.solve(root, transform)
        return np.linalg.eigvalsh(B @ self.R[np.ix_(ids, ids)] @ B.T)

    def maximize(self):
        # Independent tuple-history state representation; no bit masks.
        states = {(0, ()): (self.d.prior, ())}
        self.visited_states = 0
        for t in range(self.d.n):
            self.visited_states += len(states)
            following = {}
            for (count, history), (value, selected) in states.items():
                for take in (False, True):
                    q = count+take
                    if not q <= self.d.k <= q+self.d.n-t-1:
                        continue
                    short = tuple(s for s in history if s >= t+1-self.L)
                    candidate = value+(self.local(t, history) if take else 0)
                    if take and self.L:
                        short += (t,)
                    state = q, short
                    if state not in following or candidate > following[state][0]:
                        following[state] = candidate, selected+((t,) if take else ())
            states = following
        return max(states.values(), key=lambda x: x[0])

    def liu(self, z, a):
        diagonal = np.repeat(z/a, self.d.d)
        S = self.R-a*np.eye(len(self.R))
        f = self.d.F.reshape(-1)
        V = np.linalg.solve(np.eye(len(self.R))+S*diagonal, f)
        J = self.d.prior+f @ (diagonal*V)
        gradient = (V.reshape(self.d.n, self.d.d)**2).sum(axis=1)/(a*J)
        return math.log(J), gradient


def delta(design, L):
    if L >= design.n-1 or design.rho == 0:
        return 0.
    r = design.rho
    tail = 2*r**(L+1)/(1-r)
    full = 2*r**(L+1)*(1-r**(L+1))/(1-r)**2
    return tail+.5*(full-tail)


def audit_solution(design, L, result, ref):
    if result["true_lower_bound"] is None:
        assert result["status"] in ("time_limit", "memory_limit")
        return
    check_close(result["true_lower_bound"], ref.true(tuple(result["selected"])), "reported DP lower")
    if result["surrogate_optimum"] is not None:
        optimum, _ = ref.maximize()
        assert ref.visited_states == result["visited_states"]
        check_close(result["surrogate_optimum"], optimum, "independent DP optimum")
        check_close(ref.surrogate(tuple(result["selected"])), optimum, "DP selected score")
        check_close(sum(result["selected_arc_information"])+design.prior, optimum, "saved arc sum")
        expected_upper = ref.true(tuple(range(design.n)))
        dd = delta(design, L)
        check_close(result["delta"]["used"], dd, "uniform delta")
        if dd < 1:
            transferred = design.prior+(optimum-design.prior)/(1-dd)
            check_close(result["transferred_information_upper_bound"], transferred, "prior-aware transfer")
            expected_upper = min(expected_upper, transferred)
        check_close(result["true_upper_bound"], expected_upper, "reported DP upper")


def audit_liu(design, result, ref):
    lower = ref.true(tuple(result["selected"]))
    check_close(result["true_lower_bound"], lower, "Liu feasible lower")
    bound = math.log(ref.true(tuple(range(design.n))))
    w = result["upper_witness"]
    if w is not None:
        z = np.array(w["z"])
        value, gradient = ref.liu(z, result["split_a"])
        check_close(value, w["log_information"], "Liu witness value")
        check_close(gradient, w["gradient"], "Liu witness gradient")
        price = sum(sorted(gradient, reverse=True)[:design.k])
        check_close(price, w["linear_price"], "Liu top-k price")
        bound = min(bound, value+price-gradient@z)
    check_close(result["true_upper_bound"], math.exp(bound), "Liu reconstructed upper")
    if result["continuous_z"] is not None:
        z = np.array(result["continuous_z"])
        check_close(z.sum(), design.k, "continuous count", atol=1e-8)
        assert np.min(z) >= 0 and np.max(z) <= 1
        value = ref.liu(z, result["split_a"])[0]
        check_close(value, result["continuous_log_information"], "continuous objective")
        check_close(bound-value, result["continuous_tangent_gap"], "continuous tangent gap")


def main():
    started = perf_counter()
    source = Path(target.__file__).read_bytes()
    rng = np.random.default_rng(719206)
    counts = {k: 0 for k in ("covariance_constructions", "local_information", "residual_spectra",
                             "dp_comparisons", "snapshot_solves", "liu_binary", "liu_derivatives",
                             "liu_tangents", "liu_solves", "invalid_inputs", "saved_exchange_neighbors",
                             "independent_greedy_evaluations")}
    max_errors = {"covariance": 0., "local": 0., "liu_gradient": 0., "kinetic_derivative": 0.}
    for n, dim in ((1, 1), (2, 2), (5, 3), (7, 2)):
        M = rng.normal(size=(dim, dim))
        rho = .4 if n == 7 else .7
        A = rho*M/max(1, np.linalg.norm(M, 2))
        if n == 1:
            A[:] = 0
        for k in sorted(set((0, 1, n//2, n))):
            d = target.SnapshotDesign(rng.normal(size=(n, dim)), A, rho if n>1 else 0., .13, k)
            subsets = list(combinations(range(n), k))
            for L in sorted(set((0, min(2, n-1), n-1))):
                ref, oracle = Reference(d, L), target.BlockCalendarOracle(d, L)
                err = float(np.max(abs(ref.R-d.covariance())))
                max_errors["covariance"] = max(max_errors["covariance"], err)
                check_close(ref.R, d.covariance(), "innovation-loading covariance")
                counts["covariance_constructions"] += 1
                scores, true_scores = [], []
                for s in subsets:
                    score = ref.surrogate(s)
                    max_errors["local"] = max(max_errors["local"], abs(score-oracle.information(s)))
                    check_close(score, oracle.information(s), "local factorization")
                    true = ref.true(s)
                    check_close(true, d.true_information(s), "true information")
                    if L >= n-1:
                        check_close(score, true, "full-history equality")
                    eig = ref.residual_spectrum(s)
                    if len(eig):
                        assert max(abs(eig-1)) <= delta(d, L)+1e-9
                        counts["residual_spectra"] += 1
                    scores.append(score)
                    true_scores.append(true)
                    counts["local_information"] += 1
                answer = oracle.maximize()
                check_close(answer["surrogate_optimum"], max(scores), "enumerated DP optimum")
                check_close(answer["surrogate_optimum"], ref.maximize()[0], "tuple DP optimum")
                counts["dp_comparisons"] += 1
                solved = target.solve_snapshot(d, L, time_limit=2)
                audit_solution(d, L, solved, ref)
                assert solved["true_lower_bound"] <= max(true_scores)+1e-9 <= solved["true_upper_bound"]+2e-9
                counts["snapshot_solves"] += 1
            dense, ref = target.BlockLiuOracle(d), Reference(d, 0)
            for s in subsets:
                z = np.zeros(n)
                z[list(s)] = 1
                value, gradient = dense.value_gradient(z)
                direct, direct_gradient = ref.liu(z, dense.a)
                check_close(math.exp(value), ref.true(s), "block Liu binary identity")
                check_close((value, *gradient), (direct, *direct_gradient), "direct Liu boundary")
                counts["liu_binary"] += 1
            z = rng.uniform(.15, .85, size=n)
            value, gradient = dense.value_gradient(z)
            check_close((value, *gradient), (ref.liu(z, dense.a)[0], *ref.liu(z, dense.a)[1]), "direct Liu interior")
            for j in range(n):
                step = np.zeros(n)
                step[j] = 1e-6
                fd = (dense.value_gradient(z+step)[0]-dense.value_gradient(z-step)[0])/2e-6
                max_errors["liu_gradient"] = max(max_errors["liu_gradient"], abs(fd-gradient[j]))
                check_close(fd, gradient[j], "block gradient derivative", atol=2e-7)
                counts["liu_derivatives"] += 1
            for s in subsets:
                endpoint = np.zeros(n)
                endpoint[list(s)] = 1
                assert math.log(ref.true(s)) <= value+gradient@(endpoint-z)+1e-9
                counts["liu_tangents"] += 1
            continuous = target.solve_liu_relaxation(d, time_limit=2)
            audit_liu(d, continuous, ref)
            assert continuous["true_upper_bound"] >= max(ref.true(s) for s in subsets)-1e-9
            counts["liu_solves"] += 1
    independent_noise = target.SnapshotDesign(np.zeros((6, 2)), np.zeros((2, 2)), 0., .7, 2)
    ref = Reference(independent_noise, 3)
    answer = target.solve_snapshot(independent_noise, 3, time_limit=2)
    audit_solution(independent_noise, 3, answer, ref)
    assert answer["true_lower_bound"] == .7 and answer["true_upper_bound"] == .7
    counts["snapshot_solves"] += 1
    continuous = target.solve_liu_relaxation(independent_noise, time_limit=2)
    audit_liu(independent_noise, continuous, ref)
    check_close(continuous["true_upper_bound"], .7, "zero-information tie")
    counts["liu_solves"] += 1
    saved_rows, hashes = [], {}
    for dim in (4, 16):
        path = HERE/f"results/block-snapshot-d{dim}-probe.json"
        data = json.loads(path.read_text())
        hashes[path.name] = sha256(path.read_bytes()).hexdigest()
        assert data["metadata"]["driver_sha256"] == sha256(source).hexdigest()
        assert data["metadata"]["complete"]
        assert all(value == "1" for value in data["metadata"]["blas_environment"].values())
        d = target.SnapshotDesign(np.array(data["F"]), np.array(data["A"]), data["rho"], data["prior"], data["k"])
        ref = Reference(d, data["L"])
        prescribed_A = np.zeros_like(d.A)
        for j in range(dim):
            prescribed_A[(j+1)%dim, j] += .2
            prescribed_A[j, j] += .2*(-1 if j%2 else 1)
        check_close(prescribed_A, d.A, "prescribed nonnormal transition")
        check_close(np.eye(dim)-d.A@d.A.T, data["Q"], "saved innovation covariance")
        assert np.linalg.norm(d.A@d.A.T-d.A.T@d.A, 2) > .1
        audit_solution(d, data["L"], data["dp"], ref)
        audit_liu(d, data["liu_continuous"], ref)
        selected = tuple(data["greedy_exchange"]["selected"])
        score = ref.true(selected)
        check_close(score, data["greedy_exchange"]["true_lower_bound"], "saved greedy objective")
        greedy = ()
        for _ in range(d.k):
            options = []
            for added in range(d.n):
                if added not in greedy:
                    proposed = tuple(sorted((*greedy, added)))
                    options.append((ref.true(proposed), proposed))
                    counts["independent_greedy_evaluations"] += 1
            greedy = max(options, key=lambda pair: pair[0])[1]
        assert greedy == tuple(data["greedy_exchange"]["greedy_selected"])
        check_close(ref.true(greedy), data["greedy_exchange"]["greedy_information"], "saved greedy construction")
        assert selected == tuple(data["dp"]["selected"]) == tuple(data["liu_continuous"]["selected"])
        for dropped in selected:
            for added in range(d.n):
                if added in selected:
                    continue
                swapped = tuple(sorted((set(selected)-{dropped}) | {added}))
                assert ref.true(swapped) <= score+1e-10
                counts["saved_exchange_neighbors"] += 1
        kinetics = data["kinetics"]
        k1, k2, A0 = kinetics["k1"], kinetics["k2"], kinetics["A0"]
        G = np.array([[-k1, 0., 0.], [k1, -k2, 0.], [0., k2, 0.]])
        E = np.array([[-k1, 0., 0.], [k1, 0., 0.], [0., 0., 0.]])
        channels = np.array(kinetics["channel_coordinate"])
        check_close(kinetics["time_grid"], 12*np.arange(1, d.n+1)/d.n, "prescribed time grid")
        check_close(channels, np.linspace(0, 1, dim), "prescribed channel grid")
        centers, widths = np.array(kinetics["profile_centers"]), np.array(kinetics["profile_widths"])
        profiles = np.exp(-((channels[:, None]-centers)/widths)**2/2)
        check_close(profiles, kinetics["channel_profiles"], "channel profile provenance")
        concentrations, derivative = [], []
        for t in kinetics["time_grid"]:
            concentrations.append(A0*expm(t*G)[:, 0])
            derivative.append(A0*expm_frechet(t*G, t*E, compute_expm=False)[:, 0] @ profiles.T)
        check_close(concentrations, kinetics["species_concentrations"], "matrix exponential kinetics")
        check_close(np.array(concentrations)@profiles.T, kinetics["mean_spectra"], "mean spectrum provenance")
        error = float(np.max(abs(np.array(derivative)-d.F)))
        max_errors["kinetic_derivative"] = max(max_errors["kinetic_derivative"], error)
        check_close(derivative, d.F, "Frechet log-rate sensitivity", atol=1e-12)
        assert data["liu_continuous"]["true_upper_bound"] < data["dp"]["true_upper_bound"]
        saved_rows.append({"d": dim, "selected": selected, "true_information": score,
                           "dp_upper": data["dp"]["true_upper_bound"],
                           "liu_upper": data["liu_continuous"]["true_upper_bound"],
                           "kinetic_derivative_error": error, "independent_DP_visited_states": ref.visited_states})
    validation_path = HERE/"results/block-snapshot-validation.json"
    saved_validation = json.loads(validation_path.read_text())
    hashes[validation_path.name] = sha256(validation_path.read_bytes()).hexdigest()
    assert saved_validation["driver_sha256"] == sha256(source).hexdigest()
    rng_saved = np.random.default_rng(7183)
    F = rng_saved.integers(-10, 11, size=(10, 3))/10
    # Independently reconstruct the stated cyclic/sign transition.
    A = np.zeros((3, 3))
    for j in range(3):
        A[(j+1)%3, j] += .2
        A[j, j] += .2*(-1 if j%2 else 1)
    d = target.SnapshotDesign(F, A, .4, .01, 3)
    for row in saved_validation["rows"]:
        ref = Reference(d, row["L"])
        audit_solution(d, row["L"], row["result"], ref)
        optimum = max(ref.true(s) for s in combinations(range(d.n), d.k))
        check_close(optimum, row["true_optimum"], "saved validation true optimum")
        assert row["result"]["true_lower_bound"] <= optimum+1e-9 <= row["result"]["true_upper_bound"]+2e-9
    audit_liu(d, saved_validation["liu_continuous"], Reference(d, 0))
    limits = []
    with patch.object(target.SnapshotDesign, "covariance", side_effect=AssertionError("allocation before refusal")):
        refusal = target.solve_snapshot(d, 6, max_memory_mb=1e-9)
        assert refusal["status"] == "memory_limit" and refusal["true_lower_bound"] is None
        expired = target.solve_snapshot(d, 2, time_limit=1e-12)
        assert expired["status"] == "time_limit" and expired["true_lower_bound"] is None
    limits.extend(["memory refusal precedes covariance allocation", "initial deadline precedes covariance allocation"])
    with patch.object(target.BlockCalendarOracle, "maximize", side_effect=target.DeadlineExceeded("injected deadline")):
        expired = target.solve_snapshot(d, 2)
        assert expired["status"] == "time_limit" and expired["surrogate_optimum"] is None
        audit_solution(d, 2, expired, Reference(d, 2))
        assert "transferred_information_upper_bound" not in expired
    limits.append("interrupted DP retains only true baseline bounds")
    expired = target.solve_liu_relaxation(d, time_limit=1e-12)
    audit_liu(d, expired, Reference(d, 0))
    assert expired["status"] == "time_limit" and expired["upper_witness"] is None
    limits.append("interrupted Liu solve preserves true baseline bounds")
    for bad in ((0, 0), (-1,), (d.n,), (.5,), (True,)):
        try:
            d.true_information(bad)
        except ValueError:
            counts["invalid_inputs"] += 1
        else:
            raise AssertionError("invalid block subset accepted")
    oracle = target.BlockCalendarOracle(d, 2)
    for bad in (-1, 4, 2.5, True):
        try:
            oracle.conditional_map(bad)
        except ValueError:
            counts["invalid_inputs"] += 1
        else:
            raise AssertionError("invalid history mask accepted")
    assert Path(target.__file__).read_bytes() == source
    report = {"status": "passed", "source_sha256": sha256(source).hexdigest(),
              "reviewer_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "artifact_hashes": hashes, "python": platform.python_version(), "numpy": np.__version__,
              "scipy": scipy.__version__, "counts": counts, "maximum_errors": max_errors,
              "saved_probe_audit": saved_rows, "cap_checks": limits, "wall_seconds": perf_counter()-started,
              "limitations": ["Numerical checks, not interval or rational certificates.",
                              "The two stylized application schedules are not exhaustively proved optimal.",
                              "Time and memory controls are soft operation/array estimates, not process limits."]}
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(report, indent=2)+"\n")
    temporary.replace(OUTPUT)
    print(json.dumps({key: report[key] for key in ("status", "counts", "maximum_errors", "saved_probe_audit", "cap_checks", "wall_seconds")}, indent=2))


if __name__ == "__main__":
    main()
