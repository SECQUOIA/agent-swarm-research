"""Fresh exact dense-covariance review of certify_dense_design.py.

Reference calculations use selected covariance matrices and SymPy DomainMatrix
solves. They do not use the target's tridiagonal algebra, true-information
recursion, gradient routine, split test, or logarithm enclosure.
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

import certify_dense_design as target


HERE = Path(__file__).resolve().parent


def sm(rows):
    return sp.Matrix([[sp.Rational(x) for x in row] for row in rows])


def fq(x):
    return Q(int(x.p), int(x.q))


def covariance(problem):
    return sp.Matrix(problem.n, problem.n, lambda i, j:
                     sp.Rational(problem.latent)*sp.Rational(problem.rho)**abs(i-j)
                     +(sp.Rational(problem.nugget) if i == j else 0))


def dense_solve(A, B):
    numerator, denominator = DomainMatrix.from_Matrix(A).solve_den(
        DomainMatrix.from_Matrix(B))
    return (numerator/denominator).to_Matrix()


def direct(problem, z, a):
    """Use effective observation noise a(1/z-1) on positive coordinates."""
    R, F, prior = covariance(problem), sm(problem.F), sm(problem.prior)
    active = [i for i, value in enumerate(z) if value > 0]
    if active:
        B = R.extract(active, active)+sp.diag(*(
            sp.Rational(a)*(1/sp.Rational(z[i])-1) for i in active))
        X = dense_solve(B, F.extract(active, range(problem.p)))
        J = prior+F.extract(active, range(problem.p)).T*X
        V = F-(R-sp.Rational(a)*sp.eye(problem.n))[:, active]*X
    else:
        J, V = prior, F
    H = J.inv(method="DM")
    gradient = tuple(fq((V[i, :]*H*V[i, :].T)[0]/sp.Rational(a))
                     for i in range(problem.n))
    return R, J, gradient


def integer_information(problem, selected):
    F, J = sm(problem.F), sm(problem.prior)
    if selected:
        Fs = F.extract(selected, range(problem.p))
        J += Fs.T*dense_solve(covariance(problem).extract(selected, selected), Fs)
    return J


def independent_log(value):
    """A separate rational enclosure, using 160-bit dyadic rounding and 80 terms."""
    value = Q(value)
    if value <= 0:
        raise ValueError("Positive logarithm argument required")
    power = value.numerator.bit_length()-value.denominator.bit_length()
    unit = Q(2)**power
    while value < unit:
        power -= 1
        unit /= 2
    while value >= 2*unit:
        power += 1
        unit *= 2
    y = value/unit
    grid = 1 << 160
    scaled = y*grid
    low = Q(scaled.numerator//scaled.denominator, grid)
    high = low if low == y else low+Q(1, grid)

    def bounds(v):
        t = (v-1)/(v+1)
        partial = Q(0)
        term = t
        for i in range(80):
            partial += 2*term/(2*i+1)
            term *= t*t
        return partial, partial+2*term/(161*(1-t*t))

    lo, hi = bounds(low)[0], bounds(high)[1]
    a, b = bounds(Q(2))
    return ((lo+power*a, hi+power*b) if power >= 0
            else (lo+power*b, hi+power*a))


def assert_saved_log(lo, hi, determinant):
    reference = independent_log(determinant)
    assert Q(lo) <= reference[0] <= reference[1] <= Q(hi)


def random_record(rng, n, p, rho, latent):
    T = sp.Matrix(p, p, lambda i, j: rng.randrange(-3, 4))
    prior = T.T*T+sp.eye(p)/7
    return {"F": [[str(Q(rng.randrange(-9, 10), 5)) for _ in range(p)]
                  for _ in range(n)],
            "prior": [[str(prior[i, j]) for j in range(p)] for i in range(p)],
            "rho": str(rho), "latent_variance": str(latent),
            "nugget_variance": str(Q(rng.randrange(1, 8), 4)), "k": n//2}


def tiny_checks():
    rng = random.Random(923145)
    counts = {key: 0 for key in ("exact_oracles", "direct_split_tests",
              "binary_information", "binary_tangent_bounds", "fractional_tangent_bounds",
              "log_intervals", "feasible_rounding", "rejections")}
    problem = None
    for n in (1, 2, 3, 5):
        for rho in (Q(-999999999999, 10**12), Q(-2, 3), Q(0), Q(3, 5),
                    Q(999999999999, 10**12)):
            for latent in (Q(0), Q(3, 2)):
                p = 1 if n == 1 else 2
                record = random_record(rng, n, p, rho, latent)
                problem = target.Problem.read(record)
                # This conservative rational choice does not use numerical eigenvalues.
                a = Q(19, 20)*(problem.nugget+latent*(1-abs(rho))/(1+abs(rho)))
                R = covariance(problem)
                for proposed in (a, problem.latent+problem.nugget,
                                 problem.latent+problem.nugget+Q(1, 10)):
                    S = R-sp.Rational(proposed)*sp.eye(n)
                    reference = all(S[:i, :i].det() > 0 for i in range(1, n+1))
                    try:
                        target.verify_split(problem, proposed)
                        actual = True
                    except ValueError:
                        actual = False
                    assert actual == reference
                    counts["direct_split_tests"] += 1
                points = [(Q(0),)*n, (Q(1),)*n,
                          tuple(Q(rng.randrange(5), 4) for _ in range(n))]
                for point in points:
                    _, J, gradient = direct(problem, point, a)
                    actual = target.exact_oracle(problem, point, a)
                    assert sm(actual[0]) == J and actual[1] == gradient
                    assert actual[2] == fq(J.det())
                    counts["exact_oracles"] += 1
                z = target.round_feasible(tuple(str(Q(rng.randrange(-4, 15), 10))
                                                for _ in range(n)), problem.k, 100)
                assert sum(z) == problem.k and all(0 <= q <= 1 for q in z)
                counts["feasible_rounding"] += 1
                selections = list(combinations(range(n), problem.k))
                cert = target.certify(problem, z, a,
                                      {selected: ["fresh review"] for selected in selections})
                assert_saved_log(cert["tangent_logdet_lower"], cert["tangent_logdet_upper"],
                                 cert["information_determinant"])
                assert_saved_log(cert["incumbent_lower_bound"], cert["incumbent_upper_bound"],
                                 cert["incumbent_determinant"])
                counts["log_intervals"] += 2
                determinants = []
                for selected in selections:
                    J = integer_information(problem, selected)
                    binary = tuple(Q(i in selected) for i in range(n))
                    assert sm(target.exact_oracle(problem, binary, a)[0]) == J
                    counts["binary_information"] += 1
                    determinant = fq(J.det())
                    determinants.append(determinant)
                    # Check a known rigorous interval, not float(log(det)).
                    assert cert["upper_bound"] >= independent_log(determinant)[1]
                    counts["binary_tangent_bounds"] += 1
                assert cert["incumbent_determinant"] == max(determinants)
                testpoint = tuple(Q(problem.k, n) for _ in range(n))
                _, J, _ = direct(problem, testpoint, a)
                assert cert["upper_bound"] >= independent_log(fq(J.det()))[1]
                counts["fractional_tangent_bounds"] += 1
                # Off-cardinality tangents remain upper bounds but cannot certify a
                # feasible continuous lower bound.
                wrong = (Q(0),)*n if problem.k else (Q(1),)*n
                off = target.certify(problem, wrong, a,
                                     {selections[0]: ["fresh review"]})
                assert off["continuous_lower_bound"] is None
                assert off["upper_bound"] >= independent_log(max(determinants))[1]
    base = random_record(rng, 3, 2, Q(2, 5), Q(1))
    malformed = []
    for key, values in {
        "F": [[], [["1"]], [["1", "2"], ["3"]], [[True, "1"]], [[0.2, 1]]],
        "prior": [[], [["0", "0"], ["0", "1"]],
                  [["1", "2"], ["2", "1"]], [["1", "1"], ["0", "1"]]],
        "rho": ["1", "-1", "2", True, 0.2, "nan"],
        "latent_variance": ["-1", True],
        "nugget_variance": ["0", "-1", True],
        "k": [-1, 4, True, "1", 1.0],
    }.items():
        for value in values:
            malformed.append(lambda key=key, value=value:
                             target.Problem.read(dict(base, **{key: value})))
    problem = target.Problem.read(base)
    a = Q(1, 2)
    for point in ((Q(0),), (Q(-1), Q(1), Q(1)), (Q(2), Q(0), Q(0)),
                  (0.2, 0, 1), (True, 0, 1)):
        malformed.append(lambda point=point: target.certify(
            problem, point, a, {(0,): ["bad point"]}))
    for selected in ((0, 0), (-1,), (3,), (True,), (0.0,), ()):
        malformed.append(lambda selected=selected: target.certify(
            problem, (Q(1), Q(0), Q(0)), a, {selected: ["bad subset"]}))
    for action in malformed:
        try:
            action()
        except (ValueError, TypeError, ZeroDivisionError):
            counts["rejections"] += 1
        else:
            raise AssertionError("Malformed input was accepted")
    return counts


def symbolic_derivative_checks():
    problem = target.Problem.read({"F": [[1, -2], [3, 1]],
        "prior": [[2, 1], [1, 3]], "rho": "2/5", "latent_variance": "2",
        "nugget_variance": "1", "k": 1})
    a = Q(1)
    x, y = sp.symbols("x y")
    D = sp.diag(x, y)
    F, R = sm(problem.F), covariance(problem)
    J = sm(problem.prior)+F.T*D*(sp.eye(2)+(R-sp.eye(2))*D).inv()*F
    determinant = sp.factor(J.det())
    derivatives = [sp.cancel(sp.diff(determinant, v)/determinant) for v in (x, y)]
    checked = 0
    for z in ((Q(0), Q(0)), (Q(1, 4), Q(3, 4)), (Q(1), Q(1))):
        expected = tuple(fq(d.subs({x: sp.Rational(z[0]), y: sp.Rational(z[1])}))
                         for d in derivatives)
        assert target.exact_oracle(problem, z, a)[1] == expected
        checked += 2
    return checked


def saved_checks():
    dense_path = HERE/"results/dense-design-exact-certificates.json"
    input_path = HERE/"results/noisy-markov-extended-benchmark.json"
    report = json.loads(dense_path.read_text())
    source = json.loads(input_path.read_text(), parse_float=str)
    digest = hashlib.sha256(input_path.read_bytes()).hexdigest()
    assert report["input_sha256"] == digest
    assert report["source_sha256"] == hashlib.sha256(Path(target.__file__).read_bytes()).hexdigest()
    records = []
    for cert in report["results"]:
        index = cert["case"]
        memory_path = HERE/f"results/noisy-markov-extended-certificate-{index}.json"
        memory = json.loads(memory_path.read_text())
        problem = target.Problem.read(cert["problem_data"])
        assert problem == target.Problem.read(source["results"][index])
        assert problem == target.Problem.read(memory["problem_data"])
        assert memory["input_sha256"] == digest and memory["input_case_index"] == index
        assert (cert["n"], cert["p"], cert["k"]) == (problem.n, problem.p, problem.k)
        z, a = tuple(map(Q, cert["tangent_z"])), Q(cert["a"])
        assert len(z) == problem.n and sum(z) == problem.k and all(0 <= q <= 1 for q in z)
        assert a > 0
        R, J, gradient = direct(problem, z, a)
        assert J == sm(cert["information"])
        assert gradient == tuple(map(Q, cert["gradient"]))
        assert fq(J.det()) == Q(cert["information_determinant"])
        assert all(q >= 0 for q in gradient)
        # Check the saved exact split pivots using an independent covariance
        # identity and explicit tridiagonal factor reconstruction.
        n, rho = problem.n, sp.Rational(problem.rho)
        M = sp.diag(1, *((1+rho*rho,)*(n-2)), 1)
        for i in range(n-1):
            M[i, i+1] = M[i+1, i] = -rho
        scale = sp.Rational(problem.latent)*(1-rho*rho)
        G = scale*sp.eye(n)+(sp.Rational(problem.nugget)-sp.Rational(a))*M
        assert (R-sp.Rational(a)*sp.eye(n))*M == G
        # M is SPD by strict row diagonal dominance for |rho|<1.
        assert all(M[i, i] > sum(abs(M[i, j]) for j in range(n) if j != i)
                   for i in range(n))
        pivots = list(map(sp.Rational, cert["split_ldl_pivots"]))
        assert len(pivots) == n and all(value > 0 for value in pivots)
        L = sp.eye(n)
        for i in range(1, n):
            L[i, i-1] = G[i, i-1]/pivots[i-1]
        assert L*sp.diag(*pivots)*L.T == G
        priced = tuple(cert["priced_selection"])
        assert len(priced) == problem.k and len(set(priced)) == problem.k
        price = sum(sorted(gradient, reverse=True)[:problem.k], Q(0))
        assert sum(gradient[i] for i in priced) == price
        gap = price-sum(g*q for g, q in zip(gradient, z))
        assert gap == Q(cert["tangent_gap"]) and gap >= 0
        assert_saved_log(cert["tangent_logdet_lower"], cert["tangent_logdet_upper"], fq(J.det()))
        assert Q(cert["continuous_lower_bound"]) == Q(cert["tangent_logdet_lower"])
        assert Q(cert["upper_bound"]) == Q(cert["tangent_logdet_upper"])+gap
        selected = cert["incumbent_selection"]
        assert len(selected) == problem.k and len(set(selected)) == problem.k
        assert all(type(i) is int and 0 <= i < n for i in selected)
        incumbent = fq(integer_information(problem, selected).det())
        assert incumbent == Q(cert["incumbent_determinant"])
        assert_saved_log(cert["incumbent_lower_bound"], cert["incumbent_upper_bound"], incumbent)
        difference = Q(cert["continuous_lower_bound"])-Q(memory["upper_bound"])
        assert difference > 0
        records.append({"case": index, "n": n, "seed": cert["seed"],
                        "direct_dense_information_and_gradient": "exactly equal",
                        "exact_dense_lower_minus_memory_upper": str(difference),
                        "display_dense_lower_minus_memory_upper": float(difference),
                        "display_dense_continuous_gap": float(Q(cert["upper_bound"])
                                                               -Q(cert["continuous_lower_bound"])),
                        "memory_certificate_sha256": hashlib.sha256(memory_path.read_bytes()).hexdigest()})
    return {"records": records, "input_sha256": digest,
            "dense_certificate_sha256": hashlib.sha256(dense_path.read_bytes()).hexdigest()}


def main():
    sys.set_int_max_str_digits(0)
    started = perf_counter()
    report = {"status": "passed", "reviewer": "fresh dense_exact_review subagent",
              "small_exact_checks": tiny_checks(), "saved_certificates": saved_checks(),
              "symbolic_logdet_derivative_checks": symbolic_derivative_checks(),
              "source_sha256": hashlib.sha256(Path(target.__file__).read_bytes()).hexdigest(),
              "reviewer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "wall_seconds": perf_counter()-started}
    output = HERE/"results/dense-certificate-independent-review.json"
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "counts": report["small_exact_checks"],
                      "saved_certificates": len(report["saved_certificates"]["records"]),
                      "wall_seconds": report["wall_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
