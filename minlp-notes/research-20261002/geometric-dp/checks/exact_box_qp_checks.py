#!/usr/bin/env python3
"""Targeted exact-arithmetic checks for ../exact-box-qp.md.

Small face enumeration exercises the rational-height lemma, including cases
without uniqueness or growth. These finite checks are not its proof or a
benchmark of the geometric-grid algorithm. Python 3.10+, standard library only.
"""

from dataclasses import dataclass, replace
from fractions import Fraction as Q
from itertools import product
from math import lcm
from random import Random
import json


def require(condition, message):
    if not condition:
        raise AssertionError(message)


@dataclass(frozen=True)
class Case:
    name: str
    matrix: tuple
    linear: tuple
    offset: Q
    bounds: tuple
    expected_value: Q | None = None
    expected_point: tuple | None = None
    singular_faces: bool = False
    multiple_optima: bool = False
    integer: tuple = ()  # Indices of integer coordinates, with normalized bounds.

    @property
    def n(self):
        return len(self.bounds)

    def value(self, point):
        return self.offset + sum(a*x for a, x in zip(self.linear, point)) + sum(
            self.matrix[i][j]*point[i]*point[j]
            for i in range(self.n) for j in range(self.n)
        )

    def feasible(self, point):
        return (all(lo <= x <= hi for x, (lo, hi) in zip(point, self.bounds))
                and all(point[i].denominator == 1 for i in self.integer))


def solve_and_det(matrix, rhs):
    """Exact pivoted elimination; singular systems are deliberately skipped."""
    n = len(rhs)
    rows = [[Q(x) for x in row] + [Q(b)] for row, b in zip(matrix, rhs)]
    determinant = Q(1)
    for column in range(n):
        pivot = next((i for i in range(column, n) if rows[i][column]), None)
        if pivot is None:
            return None, Q(0)
        if pivot != column:
            rows[pivot], rows[column] = rows[column], rows[pivot]
            determinant = -determinant
        scale = rows[column][column]
        determinant *= scale
        rows[column] = [x/scale for x in rows[column]]
        for i in range(n):
            if i != column:
                scale = rows[i][column]
                rows[i] = [x-scale*y for x, y in zip(rows[i], rows[column])]
    return tuple(row[-1] for row in rows), determinant


def determinant(matrix):
    return solve_and_det(matrix, [Q(0)]*len(matrix))[1]


def height_bounds(case):
    data = [x for row in case.matrix for x in row]
    data += list(case.linear) + [case.offset]
    data += [x for bounds in case.bounds for x in bounds]
    denominator = lcm(*(x.denominator for x in data))
    integer_matrix = tuple(tuple(int(denominator*x) for x in row) for row in case.matrix)
    integer_linear = tuple(int(denominator*x) for x in case.linear)
    require(all((denominator*x).denominator == 1 for x in data), "common input denominator")
    coefficient = max(1, *(abs(x) for row in integer_matrix for x in row))
    delta = (2*case.n*coefficient)**case.n
    coordinate = denominator*delta
    value = denominator*coordinate**2
    return denominator, integer_matrix, integer_linear, delta, coordinate, value


def enumerate_candidates(case, counts):
    """Enumerate small integer slices and continuous face-stationary points.

    States -1/0/+1 mean lower bound/free/upper bound. A free solution must
    be strictly inside its face, avoiding duplicate descriptions at bounds.
    The minimum-face lemma ensures a global optimizer is in this finite set,
    even when singular stationary faces contain whole sets of optimizers.
    """
    candidates = []
    singular = 0
    continuous = tuple(i for i in range(case.n) if i not in case.integer)
    integer_domains = [range(int(case.bounds[i][0]), int(case.bounds[i][1])+1) for i in case.integer]
    for assignment in product(*integer_domains):
        if case.integer:
            counts["integer_slices_enumerated"] += 1
        for states in product((-1, 0, 1), repeat=len(continuous)):
            counts["faces_enumerated"] += 1
            free = tuple(i for i, state in zip(continuous, states) if state == 0)
            active = tuple(i for i in range(case.n) if i not in free)
            point = [None]*case.n
            for i, value in zip(case.integer, assignment):
                point[i] = Q(value)
            for i, state in zip(continuous, states):
                if state:
                    point[i] = case.bounds[i][state == 1]
            matrix = [[2*case.matrix[i][j] for j in free] for i in free]
            rhs = [-case.linear[i] - 2*sum(case.matrix[i][j]*point[j] for j in active)
                   for i in free]
            solution, _ = solve_and_det(matrix, rhs)
            if solution is None:
                singular += 1
                counts["singular_faces_skipped"] += 1
                continue
            if any(not case.bounds[i][0] < x < case.bounds[i][1] for i, x in zip(free, solution)):
                continue
            for i, x in zip(free, solution):
                point[i] = x
            point = tuple(point)
            require(case.feasible(point), case.name + ": candidate feasibility")
            require(all(2*sum(case.matrix[i][j]*point[j] for j in range(case.n))
                        + case.linear[i] == 0 for i in free), case.name + ": stationarity")
            candidates.append((case.value(point), point, free))
    require(candidates, case.name + ": corners supply candidates")
    require(len({point for _, point, _ in candidates}) == len(candidates),
            case.name + ": distinct minimal-face descriptions")
    if case.singular_faces:
        require(singular > 0, case.name + ": exercises singular faces")
    counts["stationary_candidates_including_corners"] += len(candidates)
    return candidates


def convergents(value):
    numerator, denominator = value.numerator, value.denominator
    p0, p1, q0, q1 = 0, 1, 1, 0
    while denominator:
        quotient = numerator // denominator
        p0, p1 = p1, quotient*p1+p0
        q0, q1 = q1, quotient*q1+q0
        yield Q(p1, q1)
        numerator, denominator = denominator, numerator-quotient*denominator


def reconstruct_interval(lower, upper, bound):
    require(bound >= 1 and lower <= upper, "rational reconstruction inputs")
    require(upper-lower < Q(1, bound**2), "strict rational separation")
    candidates = {x for x in convergents((lower+upper)/2)
                  if x.denominator <= bound and lower <= x <= upper}
    require(len(candidates) <= 1, "bounded-denominator uniqueness")
    return next(iter(candidates), None)


def accept_candidate(case, candidate, optimum):
    return candidate is not None and case.feasible(candidate) and case.value(candidate) == optimum


def check_candidate_height(case, candidate, free, bounds, counts):
    D, H, h, delta, R, V = bounds
    active = tuple(i for i in range(case.n) if i not in free)
    require(all(i in active and candidate[i].denominator == 1 for i in case.integer),
            case.name + ": integer coordinates are fixed in the continuous slice")
    matrix = [[2*H[i][j] for j in free] for i in free]
    det = determinant(matrix)
    require(det.denominator == 1 and det != 0, case.name + ": nonzero integral determinant")
    require(abs(det) <= delta, case.name + ": determinant bound")
    scaled_active = {j: D*candidate[j] for j in active}
    require(all(t.denominator == 1 for t in scaled_active.values()),
            case.name + ": active and integer coordinates clear with D")
    rhs = [-D*h[i] - 2*sum(H[i][j]*scaled_active[j] for j in active) for i in free]
    require(all(sum(matrix[row][column]*D*candidate[j]
                    for column, j in enumerate(free)) == rhs[row]
                for row in range(len(free))), case.name + ": cleared stationary system")
    q = D*abs(int(det))
    common = lcm(*(x.denominator for x in candidate))
    value = case.value(candidate)
    require(q % common == 0 and common <= R, case.name + ": common coordinate denominator")
    require((D*q*q) % value.denominator == 0 and value.denominator <= V,
            case.name + ": objective denominator")
    counts["candidate_height_checks"] += 1


def check_case(case, index, counts):
    require(all(lo < hi for lo, hi in case.bounds), case.name + ": nonfixed rational bounds")
    require(all(x.denominator == 1 for i in case.integer for x in case.bounds[i]),
            case.name + ": normalized integer endpoints")
    require(all(case.matrix[i][j] == case.matrix[j][i]
                for i in range(case.n) for j in range(case.n)), case.name + ": symmetric matrix")
    bounds = height_bounds(case)
    D, H, h, delta, R, V = bounds
    candidates = enumerate_candidates(case, counts)
    optimum = min(value for value, _, _ in candidates)
    minimizers = [item for item in candidates if item[0] == optimum]
    _, point, free = min(minimizers, key=lambda item: (len(item[2]), item[1]))
    if case.expected_value is not None:
        require(optimum == case.expected_value, case.name + ": analytic optimum value")
    if case.expected_point is not None:
        require(len(minimizers) == 1 and point == case.expected_point,
                case.name + ": analytic unique optimizer")
    if case.multiple_optima:
        require(len(minimizers) > 1, case.name + ": distinct exact optimal witnesses")

    for _, candidate, candidate_free in candidates:
        check_candidate_height(case, candidate, candidate_free, bounds, counts)

    # Sylvester's criterion on the selected nonsingular optimal face.
    for size in range(1, len(free)+1):
        minor = [[2*H[i][j] for j in free[:size]] for i in free[:size]]
        require(determinant(minor) > 0, case.name + ": positive definite optimal free Hessian")
        counts["positive_principal_minors_checked"] += 1

    width = Q(1, 4*V*V)
    proportion = (Q(0), Q(1, 7), Q(1, 2), Q(6, 7), Q(1))[index % 5]
    lower, upper = optimum-proportion*width, optimum+(1-proportion)*width
    require(reconstruct_interval(lower, upper, V) == optimum, case.name + ": value reconstruction")
    counts["value_reconstructions"] += 1

    rho = Q(1, 4*R*R)
    nearby = tuple(x if i in case.integer else min(hi, max(lo, x+(-1 if i % 2 else 1)*rho/(2*case.n)))
                   for i, (x, (lo, hi)) in enumerate(zip(point, case.bounds)))
    require(case.feasible(nearby) and sum((x-y)**2 for x, y in zip(point, nearby)) < rho*rho,
            case.name + ": close feasible reconstruction center")
    reconstructed = tuple(reconstruct_interval(y-rho, y+rho, R) for y in nearby)
    require(reconstructed == point and accept_candidate(case, reconstructed, optimum),
            case.name + ": exact optimizer reconstruction and acceptance")
    counts["coordinate_reconstructions"] += case.n

    wrong = next((candidate for value, candidate, _ in candidates if value > optimum), None)
    if wrong is not None:
        reconstructed_wrong = tuple(reconstruct_interval(x-rho, x+rho, R) for x in wrong)
        require(reconstructed_wrong == wrong and case.feasible(reconstructed_wrong),
                case.name + ": feasible wrong reconstruction")
        require(not accept_candidate(case, reconstructed_wrong, optimum),
                case.name + ": exact objective rejects wrong candidate")
        counts["wrong_candidate_rejections"] += 1

    return {"name": case.name, "dimension": case.n, "integer_coordinates": list(case.integer),
            "optimum": str(optimum),
            "selected_optimizer": [str(x) for x in point],
            "optimal_witnesses": len(minimizers), "selected_free_coordinates": len(free),
            "D": str(D), "Delta": str(delta), "R": str(R), "V": str(V),
            "maximum_height_bound_bits": max(R.bit_length(), V.bit_length())}


def shifted_case(name, matrix, center, bounds, offset=Q(0), **kwargs):
    n = len(center)
    linear = tuple(-2*sum(matrix[i][j]*center[j] for j in range(n)) for i in range(n))
    constant = offset + sum(matrix[i][j]*center[i]*center[j] for i in range(n) for j in range(n))
    return Case(name, matrix, linear, constant, bounds, **kwargs)


def fixtures():
    zero2 = ((Q(0), Q(0)), (Q(0), Q(0)))
    zero3 = tuple((Q(0),)*3 for _ in range(3))
    unit = (Q(0), Q(1))
    triangle = Case(
        "indefinite_triangle", ((Q(1), Q(1, 6), Q(1, 8)),
                                (Q(1, 6), Q(1), Q(1, 8)),
                                (Q(1, 8), Q(1, 8), Q(-1, 2))),
        (Q(-4, 5), Q(-41, 45), Q(49, 60)), Q(71, 225), (unit,)*3,
        expected_value=Q(0), expected_point=(Q(1, 3), Q(2, 5), Q(0)))
    return [
        shifted_case("coupled_rational_interior", ((Q(1), Q(1, 6)), (Q(1, 6), Q(1))),
                     (Q(1, 3), Q(2, 5)), ((Q(-2, 7), Q(5, 4)), (Q(-1, 3), Q(8, 9))),
                     Q(-7, 11), expected_value=Q(-7, 11), expected_point=(Q(1, 3), Q(2, 5))),
        Case("affine_rational_boundary", zero2, (Q(2, 3), Q(-5, 7)), Q(1, 11),
             ((Q(-2, 5), Q(7, 6)), (Q(1, 8), Q(11, 9))),
             expected_point=(Q(-2, 5), Q(11, 9)), singular_faces=True),
        Case("concave_tied_endpoints", ((Q(-1),),), (Q(0),), Q(0), ((Q(-2, 3), Q(2, 3)),),
             expected_value=Q(-4, 9), multiple_optima=True),
        Case("rank_one_optimal_segment", ((Q(1), Q(1)), (Q(1), Q(1))),
             (Q(-2, 3), Q(-2, 3)), Q(1, 9), (unit,)*2,
             expected_value=Q(0), singular_faces=True, multiple_optima=True),
        Case("constant_objective", zero3, (Q(0),)*3, Q(-5, 7),
             ((Q(-1, 3), Q(4, 5)), (Q(1, 7), Q(8, 9)), (Q(-2, 5), Q(3, 4))),
             expected_value=Q(-5, 7), singular_faces=True, multiple_optima=True),
        shifted_case("two_flat_directions", ((Q(1), Q(0), Q(0)), (Q(0),)*3, (Q(0),)*3),
                     (Q(2, 5), Q(0), Q(0)),
                     (unit, (Q(-2, 3), Q(4, 5)), (Q(1, 7), Q(8, 9))), Q(-2, 7),
                     expected_value=Q(-2, 7), singular_faces=True, multiple_optima=True),
        Case("bilinear_rational_boundary", ((Q(0), Q(1, 2)), (Q(1, 2), Q(0))),
             (Q(0), Q(0)), Q(0), ((Q(-2, 3), Q(5, 4)), (Q(-3, 5), Q(7, 8))),
             expected_value=Q(-3, 4), expected_point=(Q(5, 4), Q(-3, 5)), singular_faces=True),
        Case("stationary_boundary", ((Q(1),),), (Q(0),), Q(0), ((Q(0), Q(2, 3)),),
             expected_value=Q(0), expected_point=(Q(0),)),
        triangle,
    ]


def random_cases(seed=20261002, dimensions=range(1, 5), per_dimension=40):
    rng = Random(seed)
    for n in dimensions:
        for index in range(per_dimension):
            matrix = [[Q(0)]*n for _ in range(n)]
            for i in range(n):
                for j in range(i, n):
                    matrix[i][j] = matrix[j][i] = Q(rng.randint(-3, 3), rng.randint(1, 5))
            bounds = []
            for _ in range(n):
                lower = Q(rng.randint(-5, 0), rng.randint(1, 5))
                bounds.append((lower, lower+Q(rng.randint(1, 6), rng.randint(1, 5))))
            yield Case(f"seeded_{n}d_{index:02d}", tuple(map(tuple, matrix)),
                       tuple(Q(rng.randint(-4, 4), rng.randint(1, 5)) for _ in range(n)),
                       Q(rng.randint(-5, 5), rng.randint(1, 7)), tuple(bounds))


def mixed_fixtures(triangle):
    unit = (Q(0), Q(1))
    return [
        replace(triangle, name="mixed_triangle_binary_z", integer=(2,)),
        shifted_case("mixed_rank_one_tied_integer_slices",
                     ((Q(1), Q(1), Q(0)), (Q(1), Q(1), Q(0)), (Q(0), Q(0), Q(1))),
                     (Q(1, 3), Q(0), Q(1, 2)), (unit,)*3,
                     expected_value=Q(1, 4), singular_faces=True, multiple_optima=True, integer=(2,)),
        shifted_case("mixed_flat_integer_direction", ((Q(1), Q(0)), (Q(0), Q(0))),
                     (Q(1, 3), Q(0)), (unit, (Q(-1), Q(1))),
                     expected_value=Q(0), multiple_optima=True, integer=(1,)),
        Case("mixed_interior_integer_coupling", ((Q(1), Q(-1, 3)), (Q(-1, 3), Q(16, 63))),
             (Q(-4, 5), Q(-32, 105)), Q(128, 175), ((Q(-2, 3), Q(5, 3)), (Q(-1), Q(3))),
             expected_value=Q(0), expected_point=(Q(16, 15), Q(2)), integer=(1,)),
        shifted_case("pure_integer_tied_assignments", ((Q(1), Q(0)), (Q(0), Q(1))),
                     (Q(1, 2), Q(1, 3)), ((Q(-1), Q(2)), (Q(-1), Q(1))),
                     expected_value=Q(13, 36), multiple_optima=True, integer=(0, 1)),
    ]


def random_mixed_cases():
    for index, case in enumerate(random_cases(seed=20261003, dimensions=(2, 3, 4), per_dimension=8)):
        integer = (case.n-2, case.n-1) if case.n > 2 and index % 2 else (case.n-1,)
        bounds = tuple((Q(i % 2-1), Q(i % 2+1)) if i in integer else bound
                       for i, bound in enumerate(case.bounds))
        yield replace(case, name="mixed_"+case.name, bounds=bounds, integer=integer)


def check_long_integer_domain(counts):
    """Check one analytic optimizer without enumerating the huge integer domain."""
    point = (Q(2, 5), Q(10**60+3))
    case = shifted_case("long_integer_interval_analytic_optimum",
                        ((Q(1), Q(0)), (Q(0), Q(1))), point,
                        ((Q(-1, 3), Q(7, 5)), (Q(-10**80), Q(10**80+7))), integer=(1,))
    # The construction is exactly (x-2/5)^2+(z-(10^60+3))^2.
    require(case.feasible(point) and case.value(point) == 0, "long integer domain: analytic optimizer")
    bounds = height_bounds(case)
    check_candidate_height(case, point, (0,), bounds, counts)
    D, _, _, delta, R, V = bounds
    rho = Q(1, 4*R*R)
    reconstructed = tuple(reconstruct_interval(x-rho, x+rho, R) for x in point)
    require(reconstructed == point and accept_candidate(case, reconstructed, Q(0)),
            "long integer domain: exact reconstruction and integrality")
    require(reconstruct_interval(Q(-1, 8*V*V), Q(1, 8*V*V), V) == 0,
            "long integer domain: value reconstruction")
    counts["coordinate_reconstructions"] += 2
    counts["value_reconstructions"] += 1
    counts["analytic_optima_without_domain_enumeration"] += 1
    return {"name": case.name, "integer_domain_cardinality": str(2*10**80+8),
            "integer_values_enumerated": 0, "optimizer": [str(x) for x in point],
            "D": str(D), "Delta": str(delta), "R": str(R), "V": str(V),
            "maximum_height_bound_bits": max(R.bit_length(), V.bit_length())}


def check_integrality_rejection(case, counts):
    # This point is within every interval and has the exact optimum value, so
    # only the prescribed integrality requirement rejects it.
    nonintegral = (Q(1, 3), Q(1, 2))
    require(all(lo <= x <= hi for x, (lo, hi) in zip(nonintegral, case.bounds))
            and case.value(nonintegral) == 0, "integrality fixture: interval-feasible exact-value point")
    *_, R, _ = height_bounds(case)
    rho = Q(1, 4*R*R)
    candidate = tuple(reconstruct_interval(x-rho, x+rho, R) for x in nonintegral)
    require(candidate == nonintegral and not accept_candidate(case, candidate, Q(0)),
            "integrality fixture: exact objective alone is insufficient")
    counts["nonintegral_exact_value_rejections"] += 1


def check_triangle(case, counts):
    """Compare coefficients of an exact global nonnegative decomposition.

    F-17(u^2+v^2)/24-z^2/4 = (u+v)^2/6+(u+z)^2/8
                             +(v+z)^2/8+z(1-z).
    Every right-hand term is nonnegative on the box, proving g=1/4.
    """
    matrix = [[Q(0)]*3 for _ in range(3)]
    linear = [Q(0)]*3
    offset = Q(0)
    squares = [
        (Q(17, 24), (1, 0, 0), Q(-1, 3)),
        (Q(17, 24), (0, 1, 0), Q(-2, 5)),
        (Q(1, 4), (0, 0, 1), Q(0)),
        (Q(1, 6), (1, 1, 0), Q(-11, 15)),
        (Q(1, 8), (1, 0, 1), Q(-1, 3)),
        (Q(1, 8), (0, 1, 1), Q(-2, 5)),
    ]
    for weight, coefficients, constant in squares:
        offset += weight*constant**2
        for i in range(3):
            linear[i] += 2*weight*constant*coefficients[i]
            for j in range(3):
                matrix[i][j] += weight*coefficients[i]*coefficients[j]
    linear[2] += 1
    matrix[2][2] -= 1
    require(tuple(map(tuple, matrix)) == case.matrix and tuple(linear) == case.linear
            and offset == case.offset, "triangle: exact polynomial identity")
    require(Q(17, 24) >= Q(1, 4) and case.value(case.expected_point) == 0,
            "triangle: certified unique minimizer and growth")
    require(max(2*case.matrix[i][i] for i in range(3)) == 2 and case.matrix[2][2] < 0,
            "triangle: L=2 and negative curvature")
    for point in product((Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)), repeat=3):
        u, v, z = point[0]-Q(1, 3), point[1]-Q(2, 5), point[2]
        require(case.value(point) >= Q(17, 24)*(u*u+v*v)+z*z/4,
                "triangle: exact rational growth probes")
        counts["triangle_growth_probes"] += 1

    # Individually bounded coordinate denominators need not have a bounded lcm.
    *_, R, _ = height_bounds(case)
    arbitrary = (Q(1, R), Q(1, R-1), Q(0))
    require(max(x.denominator for x in arbitrary) <= R
            and lcm(*(x.denominator for x in arbitrary)) > R,
            "triangle: arbitrary reconstructed common denominator exceeds R")
    rho = Q(1, 4*R*R)
    reconstructed = tuple(reconstruct_interval(x-rho, x+rho, R) for x in arbitrary)
    require(reconstructed == arbitrary and case.feasible(reconstructed)
            and not accept_candidate(case, reconstructed, Q(0)),
            "triangle: exact equality rejects arbitrary reconstructed coordinates")
    counts["wrong_candidate_rejections"] += 1
    return {"optimizer": ["1/3", "2/5", "0"], "optimum": "0", "g": "1/4", "L": "2",
            "kappa": "8", "polynomial_identity_checked": True,
            "arbitrary_common_denominator_exceeds_R": True}


def main():
    counts = dict.fromkeys(("faces_enumerated", "singular_faces_skipped",
                           "stationary_candidates_including_corners", "candidate_height_checks",
                           "positive_principal_minors_checked", "value_reconstructions",
                           "coordinate_reconstructions", "wrong_candidate_rejections",
                           "triangle_growth_probes", "integer_slices_enumerated",
                           "analytic_optima_without_domain_enumeration",
                           "nonintegral_exact_value_rejections"), 0)
    continuous_named = fixtures()
    mixed_named = mixed_fixtures(continuous_named[-1])
    named = continuous_named + mixed_named
    cases = named + list(random_cases()) + list(random_mixed_cases())
    reports = [check_case(case, index, counts) for index, case in enumerate(cases)]
    triangle = check_triangle(continuous_named[-1], counts)
    check_integrality_rejection(mixed_named[2], counts)
    long_integer = check_long_integer_domain(counts)
    # Small integration boundary cases; broad signed CF sweeps are separate work.
    require(reconstruct_interval(Q(49, 100), Q(51, 100), 1) is None,
            "empty bounded-denominator interval")
    require(reconstruct_interval(Q(-2), Q(-2), 1) == -2,
            "negative singleton interval")
    require(counts["singular_faces_skipped"] > 0 and counts["wrong_candidate_rejections"] > 0,
            "required regression cases executed")
    print(json.dumps({
        "command": "python3 research-20261002/geometric-dp/checks/exact_box_qp_checks.py",
        "arithmetic": "fractions.Fraction; no floating-point arithmetic",
        "scope": "Finite height/reconstruction checks; not a proof or a full DP benchmark.",
        "continuous_seed": 20261002, "mixed_seed": 20261003,
        "named_cases": len(named), "seeded_cases": len(cases)-len(named),
        "enumerated_cases": len(cases), "total_cases_including_analytic": len(cases)+1,
        "cases_with_integer_coordinates": sum(bool(case.integer) for case in cases)+1,
        "pure_integer_cases": sum(len(case.integer) == case.n for case in cases), "counts": counts,
        "maximum_height_bound_bits": max(report["maximum_height_bound_bits"] for report in reports),
        "triangle": triangle, "long_integer_domain": long_integer,
        "named_case_results": reports[:len(named)], "passed": True,
    }, indent=2))


if __name__ == "__main__":
    main()
