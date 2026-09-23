"""Fresh dense rational review of diagonal-split lower certificates.

The reference calculations do not use the author's tridiagonal solver,
information or gradient functions, logarithm enclosure, or memory pricing DP.
The production entry points are called only as the objects under test.
"""

from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import random
import sys
from time import perf_counter

import numpy as np
import sympy as sp

from certify_dense_design import Problem
import certify_diagonal_split as target


HERE = Path(__file__).resolve().parent
BASE = HERE / "results"


def fq(x):
    return Q(int(x.p), int(x.q))


def sm(rows):
    return sp.Matrix([[Q(x) for x in row] for row in rows])


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def covariance(problem):
    return sp.Matrix([[problem.latent * problem.rho ** abs(i-j)
                       + (problem.nugget if i == j else 0)
                       for j in range(problem.n)] for i in range(problem.n)])


def dense_point(problem, z, diagonal):
    active = [i for i in range(problem.n) if z[i] > 0]
    J = sm(problem.prior)
    gradient = [Q(0)] * problem.n
    if not active:
        return J, tuple(gradient)
    R = covariance(problem).extract(active, active)
    S = R + sp.diag(*[diagonal[i]*(1-z[i])/z[i] for i in active])
    F = sm(problem.F).extract(active, range(problem.p))
    numerator, denominator = S.to_DM().solve_den(F.to_DM())
    V = numerator.to_Matrix() / sp.Rational(denominator.numerator, denominator.denominator)
    J += F.T * V
    Ji = J.inv()
    for row, i in enumerate(active):
        gradient[i] = fq(-(1-z[i])/z[i] * (V[row, :] * Ji * V[row, :].T)[0])
    return J, tuple(gradient)


def independent_log_bounds(x):
    """Rational enclosure using 80 terms and a finer, independently chosen grid."""
    x, exponent = Q(x), 0
    assert x > 0
    while x < 1:
        x *= 2
        exponent -= 1
    while x >= 2:
        x /= 2
        exponent += 1

    def series(y):
        q = (y-1)/(y+1)
        value, power = Q(0), q
        for j in range(80):
            value += 2*power/(2*j+1)
            power *= q*q
        remainder = 2*power/(161*(1-q*q))
        return value, value+remainder

    grid = 10**24
    count = (x*grid).numerator // (x*grid).denominator
    lo = series(Q(count, grid))[0]
    hi = series(Q(count+1, grid))[1]
    log2lo, log2hi = series(Q(2))
    if exponent >= 0:
        return lo+exponent*log2lo, hi+exponent*log2hi
    return lo+exponent*log2hi, hi+exponent*log2lo


def verify_saved_log(lower, upper, determinant):
    low, high = independent_log_bounds(determinant)
    assert Q(lower) <= low <= high <= Q(upper)


def check_dual(problem, gradient, dual):
    B = sm(dual["factor"])
    correction = tuple(map(Q, dual["diagonal_correction"]))
    assert B.shape == (problem.n, problem.n) and len(correction) == problem.n
    assert all(c >= 0 for c in correction)
    Y = B*B.T + sp.diag(*correction)
    assert all(Y[i, i] >= -gradient[i] for i in range(problem.n))
    assert fq((covariance(problem)*Y).trace()) == Q(dual["trace_RY"])
    return Y


def replay_memory(record):
    """Recompute the saved memory upper bound with dense conditionals and recursion."""
    problem = Problem.read(record["problem_data"])
    n, p, k, window = problem.n, problem.p, problem.k, record["L"]
    R = covariance(problem)
    _, D = R.LDLdecomposition(hermitian=False)
    floor = fq(min(D.diagonal()))
    assert floor == Q(record["full_grid_innovation_variance_floor"])
    rho = abs(problem.rho)
    if window >= n-1 or rho == 0 or problem.latent == 0:
        delta = Q(0)
    else:
        gain = problem.latent/(problem.latent+problem.nugget)
        delta = (2*problem.latent/floor*rho**(window+1)/(1-rho)
                 * (1+gain*rho*(1-rho**window)/(1-rho)))
    assert delta == Q(record["delta"]) and delta < 1
    N = sm(record["tangent_reference"])
    assert N == N.T and all(N[:i, :i].det() > 0 for i in range(1, p+1))
    Ni = N.inv()
    H = tuple(tuple(fq(Ni[i, j])/(1-delta) for j in range(p)) for i in range(p))
    F = tuple(tuple(Q(x) for x in row) for row in problem.F)
    grid = record["score_grid"]

    @lru_cache(None)
    def conditional(ages):
        if not ages:
            return (), problem.latent+problem.nugget
        C = sp.Matrix([[problem.latent*problem.rho**abs(i-j)
                        +(problem.nugget if i == j else 0) for j in ages] for i in ages])
        cross = sp.Matrix([[problem.latent*problem.rho**age for age in ages]])
        b = cross*C.inv()
        return tuple(fq(x) for x in b), fq(problem.latent+problem.nugget-(b*cross.T)[0])

    @lru_cache(None)
    def arc(t, history):
        ages = tuple(t-i for i in history)
        b, d = conditional(ages)
        f = tuple(F[t][j]-sum((bi*F[i][j] for bi, i in zip(b, history)), Q(0)) for j in range(p))
        score = sum((H[i][j]*f[i]*f[j] for i in range(p) for j in range(p)), Q(0))/d
        scaled = score*grid
        return -((-scaled.numerator)//scaled.denominator)

    @lru_cache(None)
    def price(t, needed, history):
        if needed == 0:
            return 0
        if n-t < needed:
            return None
        if t == n:
            return None
        skipped_history = tuple(i for i in history if t+1-i <= window)
        options = []
        skipped = price(t+1, needed, skipped_history)
        if skipped is not None:
            options.append(skipped)
        following = tuple(i for i in history+(t,) if t+1-i <= window)
        chosen = price(t+1, needed-1, following)
        if chosen is not None:
            options.append(arc(t, history)+chosen)
        return max(options) if options else None

    maximum = price(0, k, ())
    assert maximum == record["integer_price"]
    saved_path = tuple(record["priced_selection"])
    assert len(saved_path) == len(set(saved_path)) == k
    assert all(0 <= i < n for i in saved_path) and saved_path == tuple(sorted(saved_path))
    assert sum(arc(t, tuple(j for j in saved_path if t-window <= j < t))
               for t in saved_path) == maximum
    constant = -p+fq((Ni*sm(problem.prior)).trace())+Q(maximum, grid)
    upper_log = Q(record["upper_bound"])-constant
    assert upper_log >= independent_log_bounds(fq(N.det()))[1]
    selected = tuple(record["selected"])
    assert len(selected) == len(set(selected)) == k and all(0 <= i < n for i in selected)
    selected_F = sm(problem.F).extract(selected, range(p))
    J = sm(problem.prior)+selected_F.T*R.extract(selected, selected).inv()*selected_F
    assert Q(record["lower_bound"]) <= independent_log_bounds(fq(J.det()))[0]
    assert Q(record["gap"]) == Q(record["upper_bound"])-Q(record["lower_bound"])
    return {"conditional_patterns": conditional.cache_info().currsize,
            "priced_arcs": arc.cache_info().currsize, "recursive_states": price.cache_info().currsize}


def main():
    sys.set_int_max_str_digits(0)
    started = perf_counter()
    rng = random.Random(719025)
    counts = {"dense_point_and_gradient": 0, "dual_factor": 0,
              "universal_lower_samples": 0, "convexity_segments": 0,
              "invalid_inputs": 0, "saved_certificates": 0}
    prior = ((Q(2), Q(-1, 3)), (Q(-1, 3), Q(1)))
    for n in (1, 2, 3, 5):
        for rho in (Q(-4, 5), Q(0), Q(1, 2)):
            for latent in (Q(0), Q(5, 4)):
                problem = Problem(tuple(tuple(Q(rng.randrange(-8, 9), 4) for _ in range(2))
                                        for _ in range(n)), prior, rho, latent, Q(3, 5), n//2)
                points = [tuple(Q(0) for _ in range(n)), tuple(Q(1) for _ in range(n)),
                          tuple(Q(rng.randrange(5), 4) for _ in range(n))]
                feasible = [Q(1) if i < problem.k else Q(0) for i in range(n)]
                if 0 < problem.k < n:
                    feasible[0] = feasible[-1] = Q(1, 2)
                points.append(tuple(feasible))
                for z in points:
                    a = tuple(Q(rng.randrange(1, 40), 7) for _ in range(n))
                    expected_J, expected_g = dense_point(problem, z, a)
                    J, g, determinant = target.exact_diagonal_point(problem, z, a)
                    assert sm(J) == expected_J and tuple(g) == expected_g
                    assert determinant == fq(expected_J.det())
                    counts["dense_point_and_gradient"] += 1
                    proposal = np.array([[rng.randrange(-5, 6) for _ in range(n)] for _ in range(n)])
                    dual = target.psd_dual_certificate(problem, g, proposal, grid=57)
                    check_dual(problem, g, dual)
                    counts["dual_factor"] += 1
                    b = tuple(Q(rng.randrange(1, 40), 7) for _ in range(n))
                    Jb, _ = dense_point(problem, z, b)
                    mid = tuple((ai+bi)/2 for ai, bi in zip(a, b))
                    Jm, _ = dense_point(problem, z, mid)
                    # Convexity at the midpoint has an entirely rational determinant test.
                    assert Jm.det()**2 <= expected_J.det()*Jb.det()
                    counts["convexity_segments"] += 1
                    if sum(z) == problem.k:
                        certificate = target.certify(problem, z, a, proposal, factor_grid=57)
                        verify_saved_log(certificate["reference_logdet_lower"],
                                         certificate["reference_logdet_upper"], determinant)
                        for _ in range(3):
                            # Each coordinate below r gives R-diag(b) PSD, including singular K.
                            admissible = tuple(problem.nugget*Q(rng.randrange(1, 10), 10)
                                               for _ in range(n))
                            actual_J, _ = dense_point(problem, z, admissible)
                            actual_lower = independent_log_bounds(fq(actual_J.det()))[0]
                            assert certificate["all_diagonal_lower_bound"] <= actual_lower
                            counts["universal_lower_samples"] += 1

    problem = Problem(((Q(1),), (Q(-1),)), ((Q(1),),), Q(2, 3), Q(3, 2), Q(1, 2), 1)
    valid_z, valid_a, Y = (Q(1, 2),)*2, (Q(1),)*2, np.eye(2)
    invalid_calls = [
        lambda: target.certify(problem, (Q(0), Q(0)), valid_a, Y),
        lambda: target.certify(problem, (Q(-1), Q(2)), valid_a, Y),
        lambda: target.certify(problem, (Q(1),), valid_a, Y),
        lambda: target.certify(problem, valid_z, (Q(0), Q(1)), Y),
        lambda: target.certify(problem, valid_z, (Q(-1), Q(1)), Y),
        lambda: target.certify(problem, valid_z, (Q(1),), Y),
        lambda: target.certify(problem, (0.5, 0.5), valid_a, Y),
        lambda: target.certify(problem, (True, Q(0)), valid_a, Y),
        lambda: target.certify(problem, valid_z, valid_a, np.ones((1, 2))),
        lambda: target.certify(problem, valid_z, valid_a, np.full((2, 2), np.nan)),
        lambda: target.certify(problem, valid_z, valid_a, np.full((2, 2), np.inf)),
        lambda: target.certify(problem, valid_z, valid_a, Y, factor_grid=0),
        lambda: target.certify(problem, valid_z, valid_a, Y, factor_grid=True),
        lambda: target.certify(problem, valid_z, valid_a, Y, factor_grid=1.5),
        lambda: target.psd_dual_certificate(problem, (Q(1), Q(0)), Y),
        lambda: target.psd_dual_certificate(problem, (Q(-1),), Y),
    ]
    for call in invalid_calls:
        try:
            call()
        except (TypeError, ValueError):
            counts["invalid_inputs"] += 1
        else:
            raise AssertionError("Malformed certificate input was accepted")

    path = BASE / "diagonal-split-kinetics-certificate.json"
    saved = json.loads(path.read_text())
    problem = Problem.read(saved["problem_data"])
    z, a = tuple(map(Q, saved["selection_point"])), tuple(map(Q, saved["reference_diagonal"]))
    assert len(z) == len(a) == problem.n and sum(z) == problem.k
    assert all(0 <= x <= 1 for x in z) and all(x > 0 for x in a)
    J, gradient = dense_point(problem, z, a)
    assert J == sm(saved["reference_information"])
    assert gradient == tuple(map(Q, saved["gradient"]))
    determinant = fq(J.det())
    assert determinant == Q(saved["reference_determinant"])
    verify_saved_log(saved["reference_logdet_lower"], saved["reference_logdet_upper"], determinant)
    check_dual(problem, gradient, saved["dual_certificate"])
    constant = -sum((gi*ai for gi, ai in zip(gradient, a)), Q(0))
    constant -= Q(saved["dual_certificate"]["trace_RY"])
    lower = Q(saved["reference_logdet_lower"])+constant
    assert lower == Q(saved["all_diagonal_lower_bound"])
    assert saved["source_sha256"] == sha(target.__file__)
    assert saved["probe_sha256"] == sha(saved["probe_source"])
    assert saved["memory_sha256"] == sha(saved["memory_source"])
    probe = json.loads(Path(saved["probe_source"]).read_text())
    memory = json.loads(Path(saved["memory_source"]).read_text())
    assert Problem.read(probe["problem_data"]) == Problem.read(memory["problem_data"]) == problem
    assert tuple(map(Q, probe["z"])) == z
    assert memory["status"] == "certified"
    memory_counts = replay_memory(memory)
    assert Q(saved["memory_upper_bound"]) == Q(memory["upper_bound"])
    separation = lower-Q(memory["upper_bound"])
    assert separation == Q(saved["separation"]) > 0
    counts["saved_certificates"] += 1
    report = {"status": "passed", "scope": "Fresh dense rational and PSD-dual review; saved memory price independently replayed",
              "counts": counts, "memory_replay_counts": memory_counts,
              "display_all_diagonal_lower_bound": float(lower),
              "display_memory_upper_bound": float(Q(memory["upper_bound"])),
              "display_separation": float(separation), "exact_separation": str(separation),
              "source_sha256": sha(target.__file__), "certificate_sha256": sha(path),
              "reviewer_sha256": sha(__file__), "seconds": perf_counter()-started}
    (BASE / "diagonal-split-independent-review.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: v for k, v in report.items() if k != "exact_separation"}), flush=True)


if __name__ == "__main__":
    main()
