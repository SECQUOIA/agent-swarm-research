#!/usr/bin/env python3
"""Exact diagnostics for convex-cubic optimizer-set distance bounds.

Optimizer sets are explicit fixture data. No generic convex optimizer,
convexity recognizer, or canonical/minimum-norm selection is implemented.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, prod


def poly_add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for powers, coefficient in polynomial.items():
            answer[powers] = answer.get(powers, F(0)) + coefficient
    return {powers: coefficient for powers, coefficient in answer.items() if coefficient}


def poly_scale(polynomial, scale):
    return {powers: coefficient * scale for powers, coefficient in polynomial.items() if coefficient * scale}


def poly_mul(left, right):
    answer = {}
    for powers, coefficient in left.items():
        for other, value in right.items():
            key = tuple(a + b for a, b in zip(powers, other))
            answer[key] = answer.get(key, F(0)) + coefficient * value
    return {powers: coefficient for powers, coefficient in answer.items() if coefficient}


def poly_power(polynomial, exponent):
    n = len(next(iter(polynomial)))
    result = {(0,) * n: F(1)}
    for _ in range(exponent):
        result = poly_mul(result, polynomial)
    return result


def variable(n, index):
    return {tuple(int(i == index) for i in range(n)): F(1)}


def constant(n, value):
    return {(0,) * n: F(value)}


def derivative(polynomial, index):
    answer = {}
    for powers, coefficient in polynomial.items():
        if powers[index]:
            reduced = list(powers)
            reduced[index] -= 1
            answer[tuple(reduced)] = coefficient * powers[index]
    return answer


def evaluate(polynomial, point):
    return sum(coefficient * prod(x**power for x, power in zip(point, powers))
               for powers, coefficient in polynomial.items())


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def matvec(matrix, point):
    return tuple(dot(row, point) for row in matrix)


def quadratic(matrix, point):
    return dot(point, matvec(matrix, point))


def determinant(matrix):
    n = len(matrix)
    if not n:
        return F(1)
    work = [[F(x) for x in row] for row in matrix]
    result = F(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if work[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            work[pivot], work[j] = work[j], work[pivot]
            result = -result
        scale = work[j][j]
        result *= scale
        for i in range(j + 1, n):
            ratio = work[i][j] / scale
            for k in range(j + 1, n):
                work[i][k] -= ratio * work[j][k]
    return result


def inverse(matrix):
    n = len(matrix)
    work = [[F(x) for x in row] + [F(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if work[i][j])
        work[pivot], work[j] = work[j], work[pivot]
        scale = work[j][j]
        work[j] = [x / scale for x in work[j]]
        for i in range(n):
            if i != j:
                scale = work[i][j]
                work[i] = [a - scale * b for a, b in zip(work[i], work[j])]
    return tuple(tuple(row[n:]) for row in work)


def psd(matrix):
    n = len(matrix)
    return all(determinant([[matrix[i][j] for j in indices] for i in indices]) >= 0
               for size in range(1, n + 1) for indices in combinations(range(n), size))


def rowspace_projection(matrix):
    basis = []
    for row in matrix:
        candidate = basis + [row]
        gram = [[dot(a, b) for b in candidate] for a in candidate]
        if determinant(gram):
            basis.append(row)
    if not basis:
        return tuple(tuple(F(0) for _ in matrix) for _ in matrix), 0
    gram_inverse = inverse([[dot(a, b) for b in basis] for a in basis])
    projection = tuple(tuple(sum(basis[a][i] * gram_inverse[a][b] * basis[b][j]
                                for a in range(len(basis)) for b in range(len(basis)))
                            for j in range(len(matrix))) for i in range(len(matrix)))
    return projection, len(basis)


def normalized_polynomial(polynomial, bounds):
    if any(lo > hi for lo, hi in bounds):
        raise ValueError("empty box")
    free = [i for i, (lo, hi) in enumerate(bounds) if lo < hi]
    dimension = len(free)
    positions = {original: i for i, original in enumerate(free)}
    result = {}
    for powers, coefficient in polynomial.items():
        term = {(0,) * dimension: coefficient}
        for i, power in enumerate(powers):
            lo, hi = bounds[i]
            if i not in positions:
                term = poly_scale(term, lo**power)
                continue
            expansion = {}
            for exponent in range(power + 1):
                key = [0] * dimension
                key[positions[i]] = exponent
                expansion[tuple(key)] = F(comb(power, exponent)) * lo**(power - exponent) * (hi - lo)**exponent
            term = poly_mul(term, expansion)
        result = poly_add(result, term)
    return result, free


EPSILON = F(1, 2**100)
GRID = (F(0), F(1, 4), F(1, 3), F(1, 2), F(3, 4), F(1))


def fixtures():
    x = variable(1, 0)
    yield "endpoint cubic", poly_power(x, 3), [(F(0),)], lambda p: p[0] ** 2
    x, y = variable(2, 0), variable(2, 1)
    yield "rank-deficient sum cubic", poly_power(poly_add(x, y), 3), [(F(0), F(0))], lambda p: dot(p, p)
    difference = poly_add(x, poly_scale(y, -1))
    diagonal = poly_add(poly_power(difference, 2), poly_scale(poly_power(difference, 3), F(1, 6)))
    diagonal_optima = [(t, t) for t in (F(0), F(1, 2), F(1))]
    yield "diagonal optimal segment", diagonal, diagonal_optima, lambda p: (p[0] - p[1]) ** 2 / 2
    thin = poly_add(diagonal, poly_scale(poly_add(x, y), EPSILON))
    yield "tiny affine-kernel slope", thin, [(F(0), F(0))], lambda p: dot(p, p)
    x, y, z = (variable(3, i) for i in range(3))
    mixed = poly_add(poly_power(x, 3), poly_power(poly_add(y, constant(3, F(-1, 3))), 2))
    yield "mixed flat kernel", mixed, [(F(0), F(1, 3), t) for t in (F(0), F(1, 2), F(1))], lambda p: p[0] ** 2 + (p[1] - F(1, 3)) ** 2
    yield "mixed affine kernel", poly_add(mixed, poly_scale(z, EPSILON)), [(F(0), F(1, 3), F(0))], lambda p: p[0] ** 2 + (p[1] - F(1, 3)) ** 2 + p[2] ** 2
    affine = poly_add(poly_scale(x, EPSILON), poly_scale(y, -2), constant(3, F(1, 7)))
    yield "affine endpoint branch", affine, [(F(0), F(1), F(0))], lambda p: p[0] ** 2 + (p[1] - 1) ** 2
    yield "constant branch", constant(2, F(5, 11)), [(F(0), F(0))], lambda p: F(0)


def check_fixture(name, polynomial, optimizers, distance_squared, counts, heights):
    n = len(optimizers[0])
    center = (F(1, 2),) * n
    gradient_polynomials = [derivative(polynomial, i) for i in range(n)]
    hessian_polynomials = [[derivative(gradient_polynomials[i], j) for j in range(n)] for i in range(n)]
    gradient = lambda x: tuple(evaluate(p, x) for p in gradient_polynomials)
    hessian = lambda x: tuple(tuple(evaluate(p, x) for p in row) for row in hessian_polynomials)
    hc, gc = hessian(center), gradient(center)
    projection, positive_rank = rowspace_projection(hc)
    assert psd(hc)
    optimum = evaluate(polynomial, optimizers[0])
    assert all(evaluate(polynomial, y) == optimum for y in optimizers)
    if not positive_rank:
        chosen = tuple(F(0) if coefficient >= 0 else F(1) for coefficient in gc)
        assert evaluate(polynomial, chosen) == optimum
        assert distance_squared(chosen) == 0
        for point in product(GRID, repeat=n):
            assert hessian(point) == hc
            assert evaluate(polynomial, point) - evaluate(polynomial, center) == dot(gc, tuple(a - b for a, b in zip(point, center)))
            counts["affine/constant branch evaluations"] += 1
        counts["affine/constant fixtures"] += 1
        return

    M = max(F(1), *(sum(abs(a) for a in row) for row in hc))
    entries = [x for row in hc for x in row] + list(gc)
    D = prod(x.denominator for x in entries)
    integer_rows = tuple(tuple(D * a for a in row) for row in hc) + (tuple(D * a for a in gc),)
    assert all(a.denominator == 1 for row in integer_rows for a in row)
    C = max(F(1), *(abs(a) for row in integer_rows for a in row))
    lambda0 = F(1, D**n) * M ** (-(n - 1))
    assert psd(tuple(tuple(hc[i][j] - lambda0 * projection[i][j] for j in range(n)) for i in range(n)))
    R0 = 96 * M * n / lambda0**2
    gamma = (n * C) ** (n - 1) * D * (1 + M * (1 + 2 * n) * R0)
    assert gamma >= 1 and D.bit_length() <= 1 + sum(a.denominator.bit_length() for a in entries)
    input_height = max(max(abs(a.numerator).bit_length(), a.denominator.bit_length()) for a in polynomial.values())
    gamma_height = max(gamma.numerator.bit_length(), gamma.denominator.bit_length())
    heights.append((name, input_height, gamma_height))
    eta0 = F(1) / gamma**4
    for q in (0, 8, 32, 100):
        eta = (F(1, 2**q) / gamma) ** 4
        assert eta == eta0 / 2**(4 * q)
        if gamma.denominator == 1:
            assert eta.denominator.bit_length() == eta0.denominator.bit_length() + 4 * q
        counts["exact precision-scale checks"] += 1

    for point in product(GRID, repeat=n):
        hp = hessian(point)
        reflected = hessian(tuple(1 - t for t in point))
        assert psd(hp)
        assert tuple(tuple(hp[i][j] + reflected[i][j] for j in range(n)) for i in range(n)) == tuple(tuple(2 * a for a in row) for row in hc)
        assert psd(tuple(tuple(2 * hc[i][j] - hp[i][j] for j in range(n)) for i in range(n)))
        gap = evaluate(polynomial, point) - optimum
        assert gap >= 0
        if gap <= 1:
            assert distance_squared(point) ** 2 <= gamma**4 * gap
            counts["actual fourth-root distance bounds"] += 1
        y = optimizers[0]
        displacement = tuple(a - b for a, b in zip(point, y))
        in_slice = all(a == 0 for a in matvec(hc, displacement)) and dot(gc, displacement) == 0
        assert in_slice == (gap == 0)
        counts["optimizer-slice equivalences"] += 1
        for optimizer in optimizers:
            d = tuple(a - b for a, b in zip(point, optimizer))
            hy = hessian(optimizer)
            a, b = quadratic(hy, d), quadratic(hp, d)
            assert a >= 0 and b >= 0
            slope = dot(gradient(optimizer), d)
            assert slope >= 0
            assert gap == slope + (2 * a + b) / 6
            assert gap >= (a + b) / 6
            delta_h_d = tuple(x - y for x, y in zip(matvec(hp, d), matvec(hy, d)))
            assert quadratic(hc, d) == a + dot(tuple(c - y for c, y in zip(center, optimizer)), delta_h_d)
            assert gap >= quadratic(hc, d) ** 2 / (96 * M * n)
            assert gap >= lambda0**2 * dot(matvec(projection, d), matvec(projection, d)) ** 2 / (96 * M * n)
            counts["cubic identity and endpoint-gap checks"] += 1
    if name == "endpoint cubic":
        assert hessian((F(0),)) == ((F(0),),) and positive_rank == 1
        counts["enlarged endpoint-kernel guards"] += 1
    if name == "rank-deficient sum cubic":
        assert positive_rank == 1 and all(a == 0 for row in hessian((F(0), F(0))) for a in row)
        counts["enlarged endpoint-kernel guards"] += 1
    if name == "tiny affine-kernel slope":
        witness = (F(1, 2), F(1, 2))
        assert matvec(hc, witness) == (0, 0)
        assert dot(gc, witness) == EPSILON
        assert evaluate(polynomial, witness) - optimum == EPSILON
        assert distance_squared(witness) == F(1, 2)
        assert distance_squared(witness) ** 2 > evaluate(polynomial, witness) - optimum
        counts["omitted affine-kernel equality counterchecks"] += 1
    counts["positive-rank cubic fixtures"] += 1


# Exact arithmetic in Q(sqrt(2)) for the irrational-right-hand-side slice.
def radical_add(x, y):
    return x[0] + y[0], x[1] + y[1]


def radical_scale(x, scale):
    return x[0] * scale, x[1] * scale


def radical_square(x):
    a, b = x
    return a * a + 2 * b * b, 2 * a * b


def radical_sign(x):
    a, b = x
    if not b:
        return (a > 0) - (a < 0)
    if not a:
        return (b > 0) - (b < 0)
    if a > 0 and b > 0:
        return 1
    if a < 0 and b < 0:
        return -1
    comparison = a * a - 2 * b * b
    assert comparison
    return ((comparison > 0) - (comparison < 0)) * (1 if a > 0 else -1)


def check_irrational_hoffman(counts):
    zero, one = (F(0), F(0)), (F(1), F(0))
    lower = (F(-1), F(1))
    for x, y in product((F(i, 8) for i in range(9)), repeat=2):
        projected_first = (F(x - y, 2), F(1, 2))
        if radical_sign(radical_add(projected_first, radical_scale(lower, -1))) < 0:
            projection = (lower, one)
            counts["Hoffman projections on box boundaries"] += 1
        elif radical_sign(radical_add(projected_first, radical_scale(one, -1))) > 0:
            projection = (one, lower)
            counts["Hoffman projections on box boundaries"] += 1
        else:
            projection = (projected_first, (F(y - x, 2), F(1, 2)))
        distance = zero
        for coordinate, projected in zip((x, y), projection):
            distance = radical_add(distance, radical_square(radical_add((coordinate, F(0)), radical_scale(projected, -1))))
        residual = radical_square((x + y, F(-1)))
        # A=[1,1], n=2, C=1: Hoffman constant 2; square both sides.
        assert radical_sign(radical_add(radical_scale(residual, 4), radical_scale(distance, -1))) >= 0
        # Add redundant row [2,2] and RHS 2sqrt(2): C=2, constant4,
        # and squared residual norm is five times that of the first row.
        assert radical_sign(radical_add(radical_scale(residual, 80), radical_scale(distance, -1))) >= 0
        counts["irrational-RHS Hoffman bounds"] += 2


def check_normalization(counts):
    x, y, fixed, z = (variable(4, i) for i in range(4))
    ux = poly_scale(poly_add(x, constant(4, 2)), F(1, 5))
    uy = poly_scale(poly_add(y, constant(4, -2)), F(1, 3))
    uz = poly_scale(poly_add(z, constant(4, 1)), F(1, 2))
    original = poly_add(poly_power(ux, 3), poly_power(poly_add(uy, constant(4, F(-1, 3))), 2),
                        poly_scale(uz, EPSILON), poly_power(poly_add(fixed, constant(4, F(-7, 3))), 2))
    bounds = ((F(-2), F(3)), (F(2), F(5)), (F(7, 3), F(7, 3)), (F(-1), F(1)))
    normalized, free = normalized_polynomial(original, bounds)
    assert free == [0, 1, 3]
    unit_fixture = next(item for item in fixtures() if item[0] == "mixed affine kernel")[1]
    assert normalized == unit_fixture
    for point in product(GRID, repeat=3):
        lifted = (5 * point[0] - 2, 3 * point[1] + 2, F(7, 3), 2 * point[2] - 1)
        assert evaluate(original, lifted) == evaluate(normalized, point)
        original_distance = (lifted[0] + 2) ** 2 + (lifted[1] - 3) ** 2 + (lifted[3] + 1) ** 2
        unit_distance = point[0] ** 2 + (point[1] - F(1, 3)) ** 2 + point[2] ** 2
        assert original_distance <= 25 * unit_distance
        counts["nonunit/fixed-coordinate normalization checks"] += 1
    fixed_box = tuple((lo, lo) for lo, hi in bounds)
    fixed_poly, free = normalized_polynomial(original, fixed_box)
    assert not free and evaluate(fixed_poly, ()) == evaluate(original, tuple(lo for lo, _ in bounds))
    counts["all-fixed branches"] += 1
    try:
        normalized_polynomial(original, ((F(1), F(0)),) + bounds[1:])
    except ValueError:
        counts["empty-box guards"] += 1
    else:
        raise AssertionError("empty box accepted")


def main():
    counts, heights = Counter(), []
    for arguments in fixtures():
        check_fixture(*arguments, counts, heights)
    check_irrational_hoffman(counts)
    check_normalization(counts)
    # H(x,y)=diag(1+y,1) is affine PSD but is not a Hessian field.
    field = lambda point: ((1 + point[1], F(0)), (F(0), F(1)))
    point, origin, center = (F(1), F(0)), (F(0), F(0)), (F(1, 2), F(1, 2))
    assert all(psd(field(p)) for p in product((F(0), F(1)), repeat=2))
    change = tuple(a - b for a, b in zip(matvec(field(point), point), matvec(field(origin), point)))
    assert quadratic(field(center), point) != quadratic(field(origin), point) + dot(center, change)
    counts["non-Hessian affine-field counterchecks"] += 1
    # Only this normalization trap concerns the separately reviewed canonical
    # corollary; it does not implement a regularized or minimum-norm solver.
    x, y = variable(2, 0), variable(2, 1)
    difference = poly_add(x, poly_scale(y, -1))
    original = poly_add(poly_power(difference, 2), poly_scale(poly_power(difference, 3), F(1, 12)))
    normalized, free = normalized_polynomial(original, ((F(-1), F(1)),) * 2)
    assert free == [0, 1]
    assert normalized == poly_add(poly_scale(poly_power(difference, 2), 4),
                                  poly_scale(poly_power(difference, 3), F(2, 3)))
    for t in (F(-1), F(-1, 2), F(0), F(1, 2), F(1)):
        assert evaluate(original, (t, t)) == 0
        assert dot((t, t), (t, t)) == 2 * t * t
        assert dot(((t + 1) / 2,) * 2, ((t + 1) / 2,) * 2) == (t + 1) ** 2 / 2
    original_minimum_norm_point = (F(0), F(0))
    normalized_norm_choice_in_original_coordinates = (F(-1), F(-1))
    assert evaluate(original, original_minimum_norm_point) == evaluate(original, normalized_norm_choice_in_original_coordinates) == 0
    assert dot(original_minimum_norm_point, original_minimum_norm_point) == 0
    assert dot(normalized_norm_choice_in_original_coordinates, normalized_norm_choice_in_original_coordinates) == 2
    counts["original-versus-normalized norm traps"] += 1
    print("PASS: " + "; ".join(f"{value} {name}" for name, value in counts.items()))
    print("Coefficient/Gamma bit heights: " + "; ".join(f"{name}: {a}/{b}" for name, a, b in heights))
    print("Scope: explicit optimizer sets, exact fractions/radicals, fixture-specific convexity and normalization; no generic optimizer, canonical selection, or general convexity test.")


if __name__ == "__main__":
    main()
