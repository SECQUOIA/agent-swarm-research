"""Independent dense-matrix checks of the rational structured certificate.

The reference path forms and inverts the exact covariance directly with SymPy.
It does not reuse the tridiagonal representation or its solve for expected data.
"""

from dataclasses import replace
from fractions import Fraction as Q
from itertools import combinations
import hashlib
import json
from pathlib import Path
import random
import sys

import sympy as sp

import certify_dense_design as target
from certify_noisy_markov import fraction, log_enclosure, sympy_matrix


def direct(problem, z, a):
    n = problem.n
    R = sp.Matrix(n, n, lambda i, j:
                  sp.Rational(problem.latent)*sp.Rational(problem.rho)**abs(i-j)
                  +(sp.Rational(problem.nugget) if i == j else 0))
    F = sympy_matrix(problem.F)
    D = sp.diag(*(sp.Rational(value/a) for value in z))
    V = (sp.eye(n)+(R-sp.Rational(a)*sp.eye(n))*D).inv()*F
    J = sympy_matrix(problem.prior)+F.T*D*V
    invJ = J.inv()
    gradient = tuple(fraction((V[i, :]*invJ*V[i, :].T)[0]/sp.Rational(a))
                     for i in range(n))
    return R, J, gradient


def validate():
    rng = random.Random(6109)
    solve_checks = oracle_checks = split_checks = tangent_checks = 0
    for n in (1, 2, 5, 12):
        for p in (1, 3):
            diagonal = [Q(rng.randrange(5, 10), 3) for _ in range(n)]
            offdiagonal = [Q(rng.randrange(-2, 3), 5) for _ in range(n-1)]
            rhs = [[Q(rng.randrange(-5, 6), 7) for _ in range(p)] for _ in range(n)]
            M = sp.diag(*(sp.Rational(value) for value in diagonal))
            for i, value in enumerate(offdiagonal):
                M[i, i+1] = M[i+1, i] = sp.Rational(value)
            actual = target.tridiagonal_solve(target.tridiagonal_ldl(diagonal, offdiagonal), rhs)
            assert sympy_matrix(actual) == M.inv()*sympy_matrix(rhs)
            solve_checks += 1
    saved_problem = None
    for n in (1, 2, 4):
        for rho in (Q(-2, 5), Q(0), Q(2, 5)):
            for latent in (Q(0), Q(2)):
                F = tuple(tuple(Q(rng.randrange(-5, 6), 3) for _ in range(2))
                          for _ in range(n))
                problem = target.Problem(F, ((Q(1), Q(0)), (Q(0), Q(1))),
                                         rho, latent, Q(3, 4), n//2)
                a = Q(9, 10)*(problem.nugget+latent*(1-abs(rho))/(1+abs(rho)))
                for z in ((Q(0),)*n, (Q(1),)*n,
                          tuple(Q(i+1, n+1) for i in range(n))):
                    J, gradient, detJ, _ = target.exact_oracle(problem, z, a)
                    R, reference, reference_gradient = direct(problem, z, a)
                    assert sympy_matrix(J) == reference
                    assert gradient == reference_gradient and detJ == fraction(reference.det())
                    oracle_checks += 1
                S = R-sp.Rational(a)*sp.eye(n)
                assert all(S[:i, :i].det() > 0 for i in range(1, n+1))
                target.verify_split(problem, a)
                split_checks += 1
                try:
                    target.verify_split(problem, problem.nugget+latent+1)
                except ValueError:
                    split_checks += 1
                else:
                    raise AssertionError("Invalid split accepted")
                if n == 4:
                    for k in (0, 1, 2, 4):
                        prob = replace(problem, k=k)
                        z = tuple(Q(i+1, n+1) for i in range(n))  # Usually off simplex.
                        candidates = {tuple(range(k)): ["independent test"]}
                        cert = target.certify(prob, z, a, candidates)
                        for selected in combinations(range(n), k):
                            if selected:
                                Fs = sympy_matrix(F).extract(selected, range(2))
                                exactJ = sympy_matrix(prob.prior)+Fs.T*R.extract(selected, selected).inv()*Fs
                            else:
                                exactJ = sympy_matrix(prob.prior)
                            assert cert["upper_bound"] >= log_enclosure(fraction(exactJ.det()))[1]
                            tangent_checks += 1
                    saved_problem, saved_a = problem, a

    # Symbolically differentiate a determinant, independently of the row formula.
    problem = replace(saved_problem, F=saved_problem.F[:2], k=1)
    a = saved_a
    x, y = sp.symbols("x y")
    R, _, _ = direct(problem, (Q(1, 3), Q(2, 3)), a)
    F = sympy_matrix(problem.F)
    D = sp.diag(x/sp.Rational(a), y/sp.Rational(a))
    symbolicJ = sympy_matrix(problem.prior)+F.T*D*(sp.eye(2)+(R-sp.Rational(a)*sp.eye(2))*D).inv()*F
    determinant = sp.factor(symbolicJ.det())
    point = {x: sp.Rational(1, 3), y: sp.Rational(2, 3)}
    expected = tuple(fraction(sp.cancel(sp.diff(determinant, variable)/determinant).subs(point))
                     for variable in (x, y))
    assert target.exact_oracle(problem, (Q(1, 3), Q(2, 3)), a)[1] == expected

    # Exact two-candidate separation suggested by root: R=[[2,1],[1,2]],
    # F=(1,-1), prior=1, k=1, and the admissible split a=99/100.
    separation = target.Problem(((Q(1),), (Q(-1),)), ((Q(1),),),
                                Q(2, 3), Q(3, 2), Q(1, 2), 1)
    half = (Q(1, 2), Q(1, 2))
    sepJ, sepgradient, _, _ = target.exact_oracle(separation, half, Q(99, 100))
    assert sepJ == ((Q(399, 199),),) and sepgradient[0] == sepgradient[1]
    certificate = target.certify(separation, half, Q(99, 100),
                                 {(0,): ["exact separation"], (1,): ["exact separation"]})
    assert certificate["incumbent_determinant"] == Q(3, 2)
    assert certificate["tangent_gap"] == 0

    rounding_checks = 0
    for n in (1, 3, 9):
        for k in range(n+1):
            for point in (tuple(Q(0) for _ in range(n)), tuple(Q(1) for _ in range(n)),
                          tuple(Q(rng.randrange(-3, 14), 10) for _ in range(n))):
                z = target.round_feasible(point, k, 100)
                assert len(z) == n and all(0 <= value <= 1 for value in z) and sum(z) == k
                rounding_checks += 1

    rejected = 0
    failures = [lambda: target.tridiagonal_ldl([0], []),
                lambda: target.tridiagonal_ldl([1, 1], [2]),
                lambda: target.tridiagonal_ldl([1, 1], []),
                lambda: target.exact_oracle(problem, [Q(-1), Q(1)], a),
                lambda: target.exact_oracle(problem, [Q(0)], a),
                lambda: target.verify_split(problem, Q(0)),
                lambda: target.certify(problem, [Q(0), Q(1)], a, {(0, 1): ["wrong k"]})]
    for call in failures:
        try:
            call()
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("Invalid certificate input accepted")
    return {"status": "passed", "independent_tridiagonal_solves": solve_checks,
            "exact_dense_oracle_checks": oracle_checks, "exact_split_checks": split_checks,
            "enumerated_tangent_comparisons": tangent_checks,
            "symbolic_logdet_derivatives": 2, "exact_feasible_rounding_checks": rounding_checks,
            "two_candidate_separation": {"continuous_information": "399/199",
                                         "integer_information": "3/2",
                                         "exact_tangent_gap": "0"},
            "malformed_input_rejections": rejected,
            "source_sha256": hashlib.sha256(Path(target.__file__).read_bytes()).hexdigest(),
            "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == "__main__":
    sys.set_int_max_str_digits(0)
    report = validate()
    output = Path(__file__).with_name("dense-certificate-validation.json")
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))
