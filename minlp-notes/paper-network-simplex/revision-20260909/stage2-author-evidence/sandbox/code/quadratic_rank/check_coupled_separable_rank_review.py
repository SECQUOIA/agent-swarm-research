"""Exact independent checks for coupled separable curvature-rank bounds.

Checks a shared rational basis, gap domination, and joint error bands.
The scalar integration/compiler and abstract packing proofs are not simulated.
"""

from fractions import Fraction as Q
import random
import sympy as sp


x = sp.Symbol('x')
rng = random.Random(2026090523)


def rational(value):
    value = sp.Rational(value)
    return Q(int(value.p), int(value.q))


def evaluate(poly, point):
    return rational(poly.eval(sp.Rational(point.numerator, point.denominator)))


def gap(poly, left, right, weight):
    return ((1 - weight) * evaluate(poly, left) + weight * evaluate(poly, right)
            - evaluate(poly, (1 - weight) * left + weight * right))


def spanner(polynomials):
    nodes = len(polynomials[0])
    matrix = sp.Matrix([[p.nth(k) for p in row for k in range(2, 5)]
                        for row in polynomials])
    columns = list(matrix.rref()[1])
    reduced = matrix[:, columns]
    selected = list(reduced.T.rref()[1])
    exchanges = 0
    while True:
        coefficients = reduced * reduced[selected, :].inv()
        offending = next(((j, s) for j in range(coefficients.rows)
                          for s in range(coefficients.cols)
                          if abs(coefficients[j, s]) > 2), None)
        if offending is None:
            break
        j, s = offending
        previous = abs(reduced[selected, :].det())
        selected[s] = j
        assert abs(reduced[selected, :].det()) > 2 * previous
        exchanges += 1
    assert matrix == coefficients * matrix[selected, :]
    psi = [sp.Poly(sum(polynomials[j][i].as_expr() for j in selected), x)
           for i in range(nodes)]
    return psi, coefficients, exchanges


def precision(error):
    bits = 0
    while Q(1, 2**bits) > error:
        bits += 1
    return bits


def down(value, bits):
    scale = 2**bits
    return Q((value.numerator * scale) // value.denominator, scale)


def narrow_intervals(psi, tolerance):
    intervals = []
    for i, poly in enumerate(psi):
        curvature = sum(k * (k - 1) * abs(rational(poly.nth(k)))
                        for k in range(2, 5))
        left = Q(i + 1, 2 * (len(psi) + 1))
        width = min(Q(1, 8), tolerance / (1 + curvature))
        assert curvature * width**2 / 8 <= Q(13, 16) * tolerance
        intervals.append((left, left + width))
    return intervals


basis_checks = domination_checks = box_checks = facet_checks = exchanges = 0
negative_coefficients = 0
for trial in range(12):
    nodes, latent, outputs = 2 + trial % 3, 2 + trial % 2, 5
    hidden = [[sp.Poly((x - sp.Rational(s + 1, latent + 2))**4
                      + (i + s + 1) * (x - sp.Rational(i + 1, nodes + 2))**2, x)
               for i in range(nodes)] for s in range(latent)]
    weights = [[int(j == s) if j < latent else rng.randrange(1, 9)
                for s in range(latent)] for j in range(outputs)]
    original = [[sp.Poly(sum(weights[j][s] * hidden[s][i].as_expr()
                            for s in range(latent))
                         + rng.randrange(-8, 3) * x + rng.randrange(-3, 3), x)
                 for i in range(nodes)] for j in range(outputs)]
    normalized = [[sp.Poly((j + 1) * p.as_expr(), x) for p in row]
                  for j, row in enumerate(original)]
    psi, coefficients, changes = spanner(normalized)
    basis_checks += 1
    exchanges += changes
    negative_coefficients += sum(int(bool(c < 0)) for c in coefficients)
    for i in range(nodes):
        for weight in (Q(1, 4), Q(1, 2), Q(3, 4)):
            control = gap(psi[i], Q(0), Q(1), weight)
            for row in normalized:
                assert 0 <= gap(row[i], Q(0), Q(1), weight) <= 2 * control
                domination_checks += 1
    intervals = narrow_intervals(psi, Q(1, 2 * nodes))
    bits = precision(Q(1, 8 * nodes))
    for sample in range(5):
        theta = [Q((i + sample) % 5, 4) for i in range(nodes)]
        for row in normalized:
            true = rounded = Q(0)
            for p, (a, b), t in zip(row, intervals, theta):
                true += evaluate(p, (1 - t) * a + t * b)
                rounded += (1 - t) * down(evaluate(p, a), bits) + t * down(evaluate(p, b), bits)
            residual = rounded - true
            assert residual - Q(13, 16) <= 0 <= residual + Q(1, 8)
            assert max(abs(residual - Q(13, 16)), abs(residual + Q(1, 8))) <= Q(15, 16)
            box_checks += 1

    A = [[1] * outputs] + [[rng.randrange(5) for _ in range(outputs)] for _ in range(2)]
    b = [Q(1), Q(2), Q(3)]
    facets = [[sp.Poly(sum(sp.Rational(A[k][j], b[k]) * original[j][i].as_expr()
                           for j in range(outputs)), x) for i in range(nodes)]
              for k in range(len(A))]
    psi, coefficients, changes = spanner(facets)
    basis_checks += 1
    exchanges += changes
    negative_coefficients += sum(int(bool(c < 0)) for c in coefficients)
    intervals = narrow_intervals(psi, Q(1, 4 * nodes))
    row_sum = max(sum(row) / bound for row, bound in zip(A, b))
    bits = precision(min(Q(1), 1 / (16 * nodes * row_sum)))
    for sample in range(5):
        theta = [Q((i + sample) % 5, 4) for i in range(nodes)]
        residuals = []
        for row in original:
            true = rounded = Q(0)
            for p, (a, c), t in zip(row, intervals, theta):
                true += evaluate(p, (1 - t) * a + t * c)
                rounded += (1 - t) * down(evaluate(p, a), bits) + t * down(evaluate(p, c), bits)
            residuals.append(rounded - true)
        assert all(sum(weight * abs(v) for weight, v in zip(row, residuals)) / bound <= Q(15, 32)
                   for row, bound in zip(A, b))
        for j in range(outputs):
            radius = min(bound / (2 * row[j]) for row, bound in zip(A, b) if row[j])
            for sign in (-1, 1):
                error = residuals[:]
                error[j] += sign * radius
                assert all(sum(weight * abs(v) for weight, v in zip(row, error)) / bound <= Q(31, 32)
                           for row, bound in zip(A, b))
                facet_checks += 1

assert 5832 * 15 < 2**17 and 5832 * 27 < 2**18
print(f"PASS: {basis_checks} shared bases ({exchanges} determinant exchanges, "
      f"{negative_coefficients} negative representation entries); {domination_checks} "
      f"gap dominations; {box_checks} box bands; {facet_checks} coupled-body errors")
