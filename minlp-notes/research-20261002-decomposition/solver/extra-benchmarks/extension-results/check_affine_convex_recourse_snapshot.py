#!/usr/bin/env python3
"""Exact diagnostics for the affine convex-recourse certificate.

This is a small certificate checker and regression harness, not the global
optimization algorithm. All matrix and polynomial checks use Fraction.
"""

from fractions import Fraction as Q
from itertools import product
import json
import random


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def mv(a, x):
    return [dot(row, x) for row in a]


def transpose(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    return [[dot(row, col) for col in transpose(b)] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def psd(a):
    """Exact symmetric Schur test, allowing singular matrices."""
    a = [[Q(x) for x in row] for row in a]
    if a != transpose(a):
        return False
    while a:
        if any(a[i][i] < 0 for i in range(len(a))):
            return False
        pivot = next((i for i in range(len(a)) if a[i][i] > 0), None)
        if pivot is None:
            return all(x == 0 for row in a for x in row)
        others = [i for i in range(len(a)) if i != pivot]
        a = [[a[i][j] - a[i][pivot] * a[pivot][j] / a[pivot][pivot]
              for j in others] for i in others]
    return True


def affine(a, b, z):
    return [x + v for x, v in zip(a, mv(b, z))]


def affine_range(a, b, box):
    lower, upper = a, a
    for coefficient, (left, right) in zip(b, box):
        lower += coefficient * (left if coefficient >= 0 else right)
        upper += coefficient * (right if coefficient >= 0 else left)
    return lower, upper


def product_zero(a, b, c, d):
    """Whether (a+b'z)(c+d'z) is the zero polynomial."""
    if a * c != 0:
        return False
    n = len(b)
    if any(a * d[i] + c * b[i] != 0 for i in range(n)):
        return False
    for i in range(n):
        for j in range(i, n):
            coefficient = b[i] * d[j]
            if i != j:
                coefficient += b[j] * d[i]
            if coefficient != 0:
                return False
    return True


def validate(case):
    cmat, coupling, linear = case["C"], case["D"], case["c"]
    a, b = case["a"], case["B"]
    lower_a, lower_b = case["ell_a"], case["ell_B"]
    upper_a, upper_b = case["upper_a"], case["upper_B"]
    zbox, ybox = case["zbox"], case["ybox"]
    assert all(left < right for left, right in zbox), "fixed z must be substituted"
    assert psd(cmat), "private Hessian is not PSD"
    constant_gradient = [x + y for x, y in zip(mv(cmat, a), linear)]
    linear_gradient = add(mm(cmat, b), coupling)
    for i, (left, right) in enumerate(ybox):
        low, high = affine_range(a[i], b[i], zbox)
        assert left <= low <= high <= right, "response leaves private box"
        assert affine_range(lower_a[i], lower_b[i], zbox)[0] >= 0, "negative lower multiplier"
        assert affine_range(upper_a[i], upper_b[i], zbox)[0] >= 0, "negative upper multiplier"
        assert constant_gradient[i] == lower_a[i] - upper_a[i], "constant stationarity"
        assert linear_gradient[i] == [x - y for x, y in zip(lower_b[i], upper_b[i])], "linear stationarity"
        assert product_zero(lower_a[i], lower_b[i], a[i] - left, b[i]), "lower complementarity"
        assert product_zero(upper_a[i], upper_b[i], right - a[i], [-v for v in b[i]]), "upper complementarity"


def value(case, y, z):
    return (dot(y, mv(case["C"], y)) / 2
            + dot(y, mv(case["D"], z)) + dot(case["c"], y)
            + dot(z, mv(case["A"], z)) / 2 + dot(case["d"], z)
            + case["e"])


def reduced_coefficients(case):
    a, b = case["a"], case["B"]
    bt = transpose(b)
    hessian = add(case["A"], mm(mm(bt, case["C"]), b))
    hessian = add(hessian, mm(bt, case["D"]))
    hessian = add(hessian, mm(transpose(case["D"]), b))
    linear = [x + y + z + w for x, y, z, w in zip(
        case["d"], mv(bt, mv(case["C"], a)),
        mv(transpose(case["D"]), a), mv(bt, case["c"]))]
    constant = dot(a, mv(case["C"], a)) / 2 + dot(case["c"], a) + case["e"]
    return hessian, linear, constant


def case(name, cmat, coupling, linear, a, b, *, lower=None, upper=None):
    r, k = len(a), len(b[0])
    zeros_a = [Q(0)] * r
    zeros_b = [[Q(0)] * k for _ in range(r)]
    result = {
        "name": name, "C": cmat, "D": coupling, "c": linear,
        "A": [[Q(2 if i == j else 0) for j in range(k)] for i in range(k)],
        "d": [Q(-1, 3)] * k, "e": Q(2, 7), "a": a, "B": b,
        "ell_a": lower[0] if lower else zeros_a,
        "ell_B": lower[1] if lower else zeros_b,
        "upper_a": upper[0] if upper else zeros_a,
        "upper_B": upper[1] if upper else zeros_b,
        "zbox": [(Q(0), Q(1))] * k, "ybox": [(Q(0), Q(1))] * r,
    }
    return result


def test_certificates():
    cases = []
    for stiffness in [Q(1), Q(19), Q(10**20)]:
        item = case(f"stiff_{stiffness}", [[2 * stiffness]], [[-2 * stiffness]], [Q(0)],
                    [Q(0)], [[Q(1)]])
        item["A"] = [[2 * stiffness]]
        cases.append(item)
    cases.append(case("lower_active", [[Q(2)]], [[Q(1)]], [Q(1)], [Q(0)], [[Q(0)]],
                      lower=([Q(1)], [[Q(1)]])))
    cases.append(case("upper_active", [[Q(2)]], [[Q(-1)]], [Q(-3)], [Q(1)], [[Q(0)]],
                      upper=([Q(1)], [[Q(1)]])))
    cases.append(case("mixed_face", [[Q(4), Q(1)], [Q(1), Q(2)]],
                      [[Q(-1)], [Q(0)]], [Q(-1), Q(2)], [Q(1, 4), Q(0)],
                      [[Q(1, 4)], [Q(0)]],
                      lower=([Q(0), Q(9, 4)], [[Q(0)], [Q(1, 4)]])))
    cases.append(case("singular_tied_response", [[Q(2), Q(-2)], [Q(-2), Q(2)]],
                      [[Q(0)], [Q(0)]], [Q(0), Q(0)], [Q(0), Q(0)],
                      [[Q(1)], [Q(1)]]))
    cases.append(case("two_parameter_free", [[Q(2)]], [[Q(-1, 2), Q(-1, 2)]],
                      [Q(-1, 2)], [Q(1, 4)], [[Q(1, 4), Q(1, 4)]]))
    randomizer = random.Random(1701)
    identities = 0
    for item in cases:
        validate(item)
        hessian, linear, constant = reduced_coefficients(item)
        zs = list(product([Q(0), Q(1)], repeat=len(item["zbox"])))
        zs += [tuple(Q(randomizer.randrange(18), 17) for _ in item["zbox"]) for _ in range(40)]
        for z in zs:
            response = affine(item["a"], item["B"], z)
            lower = affine(item["ell_a"], item["ell_B"], z)
            upper = affine(item["upper_a"], item["upper_B"], z)
            reduced = dot(z, mv(hessian, z)) / 2 + dot(linear, z) + constant
            assert value(item, response, z) == reduced
            for y in product([Q(0), Q(2, 5), Q(1)], repeat=len(item["ybox"])):
                delta = [left - right for left, right in zip(y, response)]
                rhs = dot(delta, mv(item["C"], delta)) / 2
                rhs += dot(lower, [v - bounds[0] for v, bounds in zip(y, item["ybox"])])
                rhs += dot(upper, [bounds[1] - v for v, bounds in zip(y, item["ybox"])])
                assert value(item, y, z) - reduced == rhs >= 0
                identities += 1
        # The growth metric is positive definite even with singular private C.
        metric = add([[Q(i == j) for j in range(len(item["zbox"]))]
                      for i in range(len(item["zbox"]))], mm(transpose(item["B"]), item["B"]))
        assert psd(metric)
    bad_cases = [
        case("center_only_primal", [[Q(2)]], [[Q(-4)]], [Q(1)], [Q(-1, 2)], [[Q(2)]]),
        case("center_only_multiplier", [[Q(2)]], [[Q(1)]], [Q(-1, 2)], [Q(0)], [[Q(0)]],
             lower=([Q(-1, 2)], [[Q(1)]])),
        case("false_complementarity", [[Q(0)]], [[Q(0)]], [Q(1)], [Q(1, 2)], [[Q(0)]],
             lower=([Q(1)], [[Q(0)]])),
        case("stationary_concave", [[Q(-2)]], [[Q(2)]], [Q(0)], [Q(0)], [[Q(1)]]),
        case("false_stationarity", [[Q(2)]], [[Q(-1)]], [Q(0)], [Q(0)], [[Q(1)]]),
    ]
    rejected = 0
    for item in bad_cases:
        try:
            validate(item)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError(f"accepted invalid certificate {item['name']}")
    return len(cases), identities, rejected


def family_value(u, v, y, stiffness):
    a, eta = Q(1, 3), Q(1, 16)
    total = sum(((ui - a)**2 - (ui - a) * vi - vi**2 + 3 * vi
                 for ui, vi in zip(u, v)), Q(0))
    total += eta * sum(((u[i + 1] - u[i])**2 + (v[i + 1] - v[i])**2
                       for i in range(len(u) - 1)), Q(0))
    return total + stiffness * sum(((yi - ui)**2 for yi, ui in zip(y, u)), Q(0))


def family_hessian(m, stiffness):
    hessian = [[Q(0)] * (3 * m) for _ in range(3 * m)]
    for i in range(m):
        hessian[i][i] += 2
        hessian[m + i][m + i] -= 2
        hessian[i][m + i] = hessian[m + i][i] = Q(-1)
        hessian[i][i] += 2 * stiffness
        hessian[2 * m + i][2 * m + i] += 2 * stiffness
        hessian[i][2 * m + i] = hessian[2 * m + i][i] = -2 * stiffness
    for offset in [0, m]:
        for i in range(m - 1):
            left, right = offset + i, offset + i + 1
            hessian[left][left] += Q(1, 8)
            hessian[right][right] += Q(1, 8)
            hessian[left][right] -= Q(1, 8)
            hessian[right][left] -= Q(1, 8)
    return hessian


def test_family():
    randomizer = random.Random(20261002)
    growth_checks, matrix_checks = 0, 0
    for m in range(1, 7):
        for stiffness in [Q(1), Q(17), Q(10**12)]:
            hessian = family_hessian(m, stiffness)
            # nu <= sqrt(5) < 9/4, checked with a rational larger shift.
            shifted = add(hessian, [[Q(9, 4) if i == j else Q(0) for j in range(3 * m)]
                                   for i in range(3 * m)])
            assert psd(shifted)
            # Restrict to y=u: exact Schur cancellation removes stiffness.
            lift = [[Q(i == j) for j in range(2 * m)] for i in range(2 * m)]
            lift += [[Q(i == j) for j in range(2 * m)] for i in range(m)]
            reduced = mm(mm(transpose(lift), hessian), lift)
            expected = [row[:2 * m] for row in family_hessian(m, Q(0))[:2 * m]]
            assert reduced == expected
            assert max(reduced[i][i] for i in range(2 * m)) <= Q(9, 4)
            # v-only directions already span an m-dimensional negative subspace.
            negative_v = [[-reduced[m + i][m + j] for j in range(m)] for i in range(m)]
            assert psd(negative_v)
            assert all(negative_v[i][i] > sum(abs(negative_v[i][j]) for j in range(m) if j != i)
                       for i in range(m))
            assert family_value([Q(1, 3)] * m, [Q(0)] * m, [Q(1, 3)] * m, stiffness) == 0
            matrix_checks += 1
            for _ in range(80):
                u = [Q(randomizer.randrange(24), 23) for _ in range(m)]
                v = [Q(randomizer.randrange(24), 23) for _ in range(m)]
                y = [Q(randomizer.randrange(24), 23) for _ in range(m)]
                distance = sum(((ui - Q(1, 3))**2 + vi**2 + (yi - Q(1, 3))**2
                                for ui, vi, yi in zip(u, v, y)), Q(0))
                assert 3 * family_value(u, v, y, stiffness) >= distance
                assert family_value(u, v, y, stiffness) >= family_value(u, v, u, stiffness)
                growth_checks += 1
    return growth_checks, matrix_checks


def test_changing_active_recourse():
    """The extra contract for sparse convex-QP value factors.

    A pair attachment has y in [0,1] and cost
    M[y^2 + (1-2(z_left+z_right))y]. Its optimal response is clipped,
    with three active regimes. The retained q0 has diagonal at most 9/4.
    """
    randomizer = random.Random(61002)
    regimes = set()
    oracle_checks = 0

    def residual_value(z, stiffness):
        nonlocal oracle_checks
        total = sum(((zi - Q(1, 3))**2 for zi in z), Q(0))
        for left, right in zip(z, z[1:]):
            total += Q(1, 16) * (right - left)**2
            response = max(Q(0), min(Q(1), left + right - Q(1, 2)))
            gradient = stiffness * (2 * response + 1 - 2 * (left + right))
            lower = gradient if response == 0 else Q(0)
            upper = -gradient if response == 1 else Q(0)
            assert lower >= 0 and upper >= 0 and gradient == lower - upper
            assert lower * response == 0 and upper * (1 - response) == 0
            regimes.add("lower" if response == 0 else "upper" if response == 1 else "free")
            candidate = stiffness * (response**2 + (1 - 2 * (left + right)) * response)
            # Compare against every bound and the unconstrained critical point
            # when feasible, independently of the clipping expression.
            candidates = [Q(0), stiffness * (2 - 2 * (left + right))]
            critical = left + right - Q(1, 2)
            if 0 <= critical <= 1:
                candidates.append(stiffness * (critical**2 + (1 - 2 * (left + right)) * critical))
            assert candidate == min(candidates)
            total += candidate
            oracle_checks += 1
        return total

    interpolation_checks = 0
    for n in range(2, 5):
        for stiffness in [Q(1), Q(23), Q(10**8)]:
            for _ in range(60):
                box = []
                probabilities = []
                point = []
                for _ in range(n):
                    left = Q(randomizer.randrange(7), 8)
                    right = left + Q(randomizer.randrange(1, int(8 * (1 - left)) + 1), 8)
                    probability = Q(randomizer.randrange(12), 11)
                    box.append((left, right))
                    probabilities.append(probability)
                    point.append(left + probability * (right - left))
                average = Q(0)
                for bits in product([0, 1], repeat=n):
                    weight = Q(1)
                    corner = []
                    for bit, probability, (left, right) in zip(bits, probabilities, box):
                        weight *= probability if bit else 1 - probability
                        corner.append(right if bit else left)
                    average += weight * residual_value(corner, stiffness)
                at_point = residual_value(point, stiffness)
                exact_direct_error = Q(0)
                for i, (probability, (left, right)) in enumerate(zip(probabilities, box)):
                    degree = int(i > 0) + int(i < n - 1)
                    diagonal = 2 + Q(degree, 8)
                    exact_direct_error += diagonal * probability * (1 - probability) * (right - left)**2 / 2
                uniform_error = Q(9, 32) * sum(((right - left)**2 for left, right in box), Q(0))
                assert average - at_point <= exact_direct_error <= uniform_error
                interpolation_checks += 1
    assert regimes == {"lower", "free", "upper"}
    return oracle_checks, interpolation_checks


if __name__ == "__main__":
    certificates, identities, invalid_rejected = test_certificates()
    growth, matrices = test_family()
    oracle_values, interpolation = test_changing_active_recourse()
    print(json.dumps({
        "arithmetic": "exact fractions", "valid_certificates": certificates,
        "elimination_identity_checks": identities, "invalid_certificates_rejected": invalid_rejected,
        "family_growth_checks": growth, "family_matrix_checks": matrices,
        "changing_active_oracle_checks": oracle_values,
        "value_factor_interpolation_checks": interpolation,
        "scope": "targeted algebraic diagnostics; no global solver benchmark",
    }, indent=2))
