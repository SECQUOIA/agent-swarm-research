"""Fresh review of the all-scalar-splits lower certificates.

Uses dense exact covariance systems, exact principal minors, and the independent
logarithm enclosure from the preceding fresh dense-certificate review.
"""

from fractions import Fraction as Q
from itertools import combinations
import hashlib
import json
from pathlib import Path
import random
import sys
from time import perf_counter

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import certify_all_splits as target
from certify_dense_design import Problem
from review_dense_certificate_independent import (
    covariance, dense_solve, fq, independent_log, random_record, sm,
)


HERE = Path(__file__).resolve().parent


def point_information(problem, z, split):
    active = [i for i, value in enumerate(z) if value]
    J = sm(problem.prior)
    if active:
        R = covariance(problem).extract(active, active)
        B = R+sp.diag(*(sp.Rational(split)*(1-sp.Rational(z[i]))/sp.Rational(z[i])
                        for i in active))
        F = sm(problem.F).extract(active, range(problem.p))
        J += F.T*dense_solve(B, F)
    return J


def psd_by_all_principal_minors(matrix):
    return all(matrix.extract(indices, indices).det() >= 0
               for k in range(1, matrix.rows+1)
               for indices in combinations(range(matrix.rows), k))


def validate_witness(matrix, witness):
    """Verify the saved witness by exact leading determinants, not elimination."""
    failed = witness["failed_index"]
    prefix = tuple(map(Q, witness["positive_prefix_pivots"]))
    pivot = Q(witness["nonpositive_pivot"])
    assert type(failed) is int and 0 <= failed < matrix.rows
    assert len(prefix) == failed and all(q > 0 for q in prefix) and pivot <= 0
    preceding = sp.Integer(1)
    for i, expected in enumerate(prefix+(pivot,)):
        determinant = matrix[:i+1, :i+1].det(method="domain-ge")
        assert fq(determinant/preceding) == expected
        preceding = determinant


def small_checks():
    rng = random.Random(921633)
    counts = {key: 0 for key in ("dense_point_values", "matrix_monotonicity",
              "spectral_classifications", "exact_lower_bounds", "failed_pivot_witnesses",
              "malformed_rejections")}
    for n in (1, 2, 4, 6):
        for rho in (Q(-999999999999, 10**12), Q(-1, 3), Q(0), Q(4, 5),
                    Q(999999999999, 10**12)):
            for latent in (Q(0), Q(3, 2)):
                problem = Problem.read(random_record(rng, n, 3, rho, latent))
                low = Q(1, 3)*(problem.nugget+latent*(1-abs(rho))/(1+abs(rho)))
                upper = problem.nugget+latent
                for proposed in (low, upper, upper+1):
                    S = covariance(problem)-sp.Rational(proposed)*sp.eye(n)
                    not_spd = any(S[:i, :i].det() <= 0 for i in range(1, n+1))
                    try:
                        target.spectral_upper_witness(problem, proposed)
                        accepted = True
                    except ValueError:
                        accepted = False
                    assert accepted == not_spd
                    counts["spectral_classifications"] += 1
                points = [(Q(0),)*n, (Q(1),)*n,
                          tuple(Q(0) if i % 3 == 0 else
                                (Q(1, 10**20) if i % 3 == 1 else Q(3, 4))
                                for i in range(n))]
                for z in points:
                    previous = None
                    for a in (low, upper, 2*upper+1):
                        reference = point_information(problem, z, a)
                        actual = sm(target.virtual_information(problem, z, a))
                        assert actual == reference
                        counts["dense_point_values"] += 1
                        if previous is not None:
                            assert psd_by_all_principal_minors(previous-reference)
                            counts["matrix_monotonicity"] += 1
                        previous = reference
                z = (Q(problem.k, n),)*n
                cert = target.certify(problem, z, upper)
                reference = point_information(problem, z, upper)
                assert reference == sm(cert["information_at_upper_split"])
                assert fq(reference.det()) == cert["information_determinant"]
                log = independent_log(fq(reference.det()))
                assert cert["all_splits_lower_bound"] <= log[0] <= log[1] <= cert["point_value_upper_bound"]
                for a in (low, low*2):
                    assert cert["all_splits_lower_bound"] <= independent_log(
                        fq(point_information(problem, z, a).det()))[0]
                    counts["exact_lower_bounds"] += 1

    for n in range(1, 7):
        for _ in range(10):
            diagonal = tuple(Q(rng.randrange(-3, 5), 2) for _ in range(n))
            off = tuple(Q(rng.randrange(-3, 4), 3) for _ in range(n-1))
            M = sp.diag(*map(sp.Rational, diagonal))
            for i, q in enumerate(off):
                M[i, i+1] = M[i+1, i] = sp.Rational(q)
            witness = target.nonpositive_pivot(diagonal, off)
            not_spd = any(M[:i, :i].det() <= 0 for i in range(1, n+1))
            assert (witness is not None) == not_spd
            if witness is not None:
                validate_witness(M, witness)
                counts["failed_pivot_witnesses"] += 1

    problem = Problem.read({"F": [[1], [-1]], "prior": [[1]], "rho": "2/3",
                            "latent_variance": "3/2", "nugget_variance": "1/2", "k": 1})
    cert = target.certify(problem, (Q(1, 2), Q(1, 2)), Q(1))
    assert cert["information_determinant"] == 2
    assert cert["spectral_upper_witness"]["nonpositive_pivot"] == 0
    assert cert["all_splits_lower_bound"] > independent_log(Q(3, 2))[1]
    bad_calls = []
    for z in ((), (Q(0), Q(0)), (Q(1), Q(1)), (Q(-1), Q(2)),
              (0.5, 0.5), (True, 0)):
        bad_calls.append(lambda z=z: target.certify(problem, z, Q(1)))
    for upper in (Q(-1), Q(0), Q(1, 4), True, 1.0):
        bad_calls.append(lambda upper=upper: target.certify(problem, (Q(1, 2), Q(1, 2)), upper))
    for grid in (0, -1, True, 1.0):
        bad_calls.append(lambda grid=grid: target.choose_upper_split(problem, Q(1), grid))
    bad_calls += [lambda: target.nonpositive_pivot((), ()),
                  lambda: target.nonpositive_pivot((1, 2), ()),
                  lambda: target.virtual_information(problem, (Q(1),), Q(1)),
                  lambda: target.virtual_information(problem, (Q(1), Q(0)), Q(0)),
                  lambda: target.choose_upper_split(problem, Q(1, 4))]
    for call in bad_calls:
        try:
            call()
        except (ValueError, TypeError):
            counts["malformed_rejections"] += 1
        else:
            raise AssertionError("Malformed input or impossible proposal accepted")
    counts["exact_two_candidate_uniform_separation"] = {"all_splits_information_lower": "2",
                                                       "integer_information": "3/2"}
    return counts


def saved_checks():
    path = HERE/"results/dense-all-splits-certificates.json"
    dense_path = HERE/"results/dense-design-exact-certificates.json"
    report = json.loads(path.read_text())
    dense = json.loads(dense_path.read_text())
    assert report["source_sha256"] == hashlib.sha256(Path(target.__file__).read_bytes()).hexdigest()
    assert report["dense_certificate_sha256"] == hashlib.sha256(dense_path.read_bytes()).hexdigest()
    # Exact dense determinants are computed once per distinct covariance/split.
    spectral_cache = {}
    records = []
    for cert in report["results"]:
        problem = Problem.read(cert["problem_data"])
        index = cert["case"]
        original = next(x for x in dense["results"] if x["case"] == index)
        assert problem == Problem.read(original["problem_data"])
        assert tuple(map(Q, cert["feasible_point"])) == tuple(map(Q, original["tangent_z"]))
        z, upper = tuple(map(Q, cert["feasible_point"])), Q(cert["upper_split"])
        assert upper > 0 and len(z) == problem.n
        assert sum(z) == problem.k and all(0 <= q <= 1 for q in z)
        J = point_information(problem, z, upper)
        assert J == sm(cert["information_at_upper_split"])
        determinant = fq(J.det())
        assert determinant == Q(cert["information_determinant"])
        lower, high = independent_log(determinant)
        assert Q(cert["all_splits_lower_bound"]) <= lower <= high <= Q(cert["point_value_upper_bound"])
        key = (problem.n, problem.rho, problem.latent, problem.nugget, upper)
        if key not in spectral_cache:
            R = covariance(problem)
            # A negative determinant directly certifies R-upper*I is not SPD.
            # This independently bypasses all precision and LDL code paths.
            det_split = DomainMatrix.from_Matrix(R-sp.Rational(upper)*sp.eye(problem.n)).det()
            assert det_split < 0
            rho = sp.Rational(problem.rho)
            M = sp.diag(1, *((1+rho*rho,)*(problem.n-2)), 1)
            for i in range(problem.n-1):
                M[i, i+1] = M[i+1, i] = -rho
            G = (R-sp.Rational(upper)*sp.eye(problem.n))*M
            w = cert["spectral_upper_witness"]
            prefix = tuple(map(sp.Rational, w["positive_prefix_pivots"]))
            pivots = prefix+(sp.Rational(w["nonpositive_pivot"]),)
            assert w["failed_index"] == len(prefix) == problem.n-1
            assert all(p > 0 for p in prefix) and pivots[-1] < 0
            L = sp.eye(problem.n)
            for i in range(1, problem.n):
                L[i, i-1] = G[i, i-1]/pivots[i-1]
            assert L*sp.diag(*pivots)*L.T == G
            spectral_cache[key] = {"dense_shifted_covariance_determinant_sign": "negative",
                                   "witness": w}
        assert spectral_cache[key]["witness"] == cert["spectral_upper_witness"]
        memory_path = HERE/"results"/cert["memory_certificate"]
        memory = json.loads(memory_path.read_text())
        assert hashlib.sha256(memory_path.read_bytes()).hexdigest() == cert["memory_certificate_sha256"]
        assert problem == Problem.read(memory["problem_data"])
        assert memory["input_case_index"] == index
        assert Q(cert["memory_upper_bound"]) == Q(memory["upper_bound"])
        difference = Q(cert["all_splits_lower_bound"])-Q(memory["upper_bound"])
        assert difference == Q(cert["all_splits_separation"]) and difference > 0
        records.append({"case": index, "n": problem.n, "seed": cert["seed"],
                        "direct_dense_point_information": "exactly equal",
                        "exact_all_splits_lower_minus_memory_upper": str(difference),
                        "display_all_splits_lower_minus_memory_upper": float(difference)})
    return {"records": records, "distinct_exact_dense_spectral_determinants": len(spectral_cache),
            "all_splits_certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    sys.set_int_max_str_digits(0)
    started = perf_counter()
    result = {"status": "passed", "reviewer": "fresh dense_exact_review subagent",
              "small_checks": small_checks(), "saved_certificates": saved_checks(),
              "source_sha256": hashlib.sha256(Path(target.__file__).read_bytes()).hexdigest(),
              "reviewer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "wall_seconds": perf_counter()-started}
    (HERE/"results/all-splits-independent-review.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "small_checks": result["small_checks"],
                      "saved_certificates": len(result["saved_certificates"]["records"]),
                      "wall_seconds": result["wall_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
