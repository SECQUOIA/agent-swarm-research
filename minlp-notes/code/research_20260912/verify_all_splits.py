"""Independent exact dense-matrix checks of all-splits lower certificates."""

from dataclasses import replace
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import random
import sys

import sympy as sp

import certify_all_splits as target
from certify_dense_design import Problem
from certify_noisy_markov import fraction, log_enclosure, sympy_matrix


def dense_value(problem, z, split):
    selected = tuple(i for i, weight in enumerate(z) if weight > 0)
    if not selected:
        return sympy_matrix(problem.prior)
    covariance = sp.Matrix(len(selected), len(selected), lambda i, j:
                           sp.Rational(problem.latent)*sp.Rational(problem.rho)**abs(selected[i]-selected[j])
                           +(sp.Rational(problem.nugget+split*(1-z[selected[i]])/z[selected[i]])
                             if i == j else 0))
    F = sympy_matrix(problem.F).extract(selected, range(problem.p))
    return sympy_matrix(problem.prior)+F.T*covariance.inv()*F


def validate():
    rng = random.Random(917)
    value_checks = monotonicity_checks = spectral_checks = lower_checks = 0
    for n in (1, 2, 5):
        for rho in (Q(-3, 4), Q(0), Q(3, 4)):
            for latent in (Q(0), Q(1)):
                F = tuple(tuple(Q(rng.randrange(-5, 6), 3) for _ in range(2)) for _ in range(n))
                problem = Problem(F, ((Q(1), Q(0)), (Q(0), Q(1))), rho, latent, Q(1, 2), n//2)
                upper = latent+problem.nugget
                witness = target.spectral_upper_witness(problem, upper)
                assert witness["nonpositive_pivot"] <= 0
                assert all(x > 0 for x in witness["positive_prefix_pivots"])
                try:
                    target.spectral_upper_witness(problem, Q(1, 4))
                except ValueError:
                    spectral_checks += 1
                else:
                    raise AssertionError("A split below every covariance eigenvalue was accepted")
                spectral_checks += 1
                points = [(Q(0),)*n, (Q(1),)*n,
                          tuple(Q(0) if i % 2 == 0 else Q(1, 2) for i in range(n)),
                          tuple(Q(i+1, n+1) for i in range(n))]
                for z in points:
                    previous = None
                    for split in (Q(1, 8), Q(1, 4), upper):
                        observed = sympy_matrix(target.virtual_information(problem, z, split))
                        expected = dense_value(problem, z, split)
                        assert observed == expected
                        value_checks += 1
                        if previous is not None:
                            difference = previous-observed
                            assert all(difference[i, i] >= 0 for i in range(problem.p))
                            assert difference.det() >= 0
                            monotonicity_checks += 1
                        previous = observed
                z = (Q(problem.k, n),)*n
                certificate = target.certify(problem, z, upper)
                for split in (Q(1, 8), Q(1, 4)):
                    detJ = fraction(dense_value(problem, z, split).det())
                    assert log_enclosure(detJ)[1] >= certificate["all_splits_lower_bound"]
                    lower_checks += 1
                assert certificate["all_splits_lower_bound"] <= log_enclosure(
                    fraction(dense_value(problem, z, upper).det()))[0]

    separation = Problem(((Q(1),), (Q(-1),)), ((Q(1),),),
                         Q(2, 3), Q(3, 2), Q(1, 2), 1)
    certificate = target.certify(separation, (Q(1, 2), Q(1, 2)), Q(1))
    assert certificate["information_determinant"] == 2
    assert certificate["spectral_upper_witness"]["nonpositive_pivot"] == 0
    assert certificate["all_splits_lower_bound"] > log_enclosure(Q(3, 2))[1]
    chosen, witness, _ = target.choose_upper_split(separation, Q(999999999999, 10**12))
    assert chosen == 1 and witness["nonpositive_pivot"] == 0

    rejected = 0
    failures = [lambda: target.certify(separation, (Q(0), Q(0)), 1),
                lambda: target.certify(separation, (Q(-1), Q(2)), 1),
                lambda: target.certify(separation, (Q(1, 2), Q(1, 2)), Q(1, 2)),
                lambda: target.virtual_information(separation, (Q(1),), 1),
                lambda: target.virtual_information(separation, (Q(0), Q(1)), 0),
                lambda: target.nonpositive_pivot([1, 1], [])]
    for call in failures:
        try:
            call()
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("Malformed all-splits certificate input accepted")
    return {"status": "passed", "exact_dense_value_checks": value_checks,
            "exact_matrix_monotonicity_checks": monotonicity_checks,
            "exact_spectral_witness_checks": spectral_checks,
            "valid_split_lower_bound_checks": lower_checks,
            "two_candidate_uniform_information_lower_bound": "2",
            "two_candidate_integer_information": "3/2",
            "malformed_input_rejections": rejected,
            "source_sha256": hashlib.sha256(Path(target.__file__).read_bytes()).hexdigest(),
            "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == "__main__":
    sys.set_int_max_str_digits(0)
    result = validate()
    Path(__file__).with_name("all-splits-validation.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
