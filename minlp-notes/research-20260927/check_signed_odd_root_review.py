"""Independent exact mixed-sign check of the odd-root circuit lift.

Uses a negative cube-root gate and a fifth-root gate depending with signed
coefficients on both retained powers. This tests the normalization and
coupled exposing construction, not the universal complexity proof.
"""

import sympy as s


def interval_power(box, exponent):
    values = [endpoint ** exponent for endpoint in box]
    return min(values), max(values)


def interval_affine(constant, terms):
    low = high = constant
    for coefficient, box in terms:
        values = [coefficient * endpoint for endpoint in box]
        low += min(values)
        high += max(values)
    return low, high


def local_exposing(alpha, variables, radicand):
    n = len(variables)
    degree = 2 * n - 1
    x = (s.Integer(1),) + tuple(variables)
    differences = s.Matrix([x[j + 1] - alpha * x[j] for j in range(n)])
    matrix = s.diag(*[alpha ** (degree - 1 - 2 * j) for j in range(n)])
    for j in range(n - 1):
        matrix[j, j + 1] = matrix[j + 1, j] = alpha ** (degree - 2 - 2 * j) / 2
    polynomial = s.expand((differences.T * matrix * differences)[0])

    def representative(weight):
        if weight == 0:
            return s.Integer(1)
        if weight <= n:
            return x[weight]
        return x[n] * x[weight - n]

    representation = x[n] ** 2 - radicand * x[1]
    representation -= alpha * (x[n - 1] * x[n] - radicand)
    for exponent, coefficient in s.Poly(polynomial, *variables).terms():
        monomial = s.prod(variable ** power for variable, power in zip(variables, exponent))
        weight = sum((j + 1) * power for j, power in enumerate(exponent))
        representation += coefficient * (monomial - representative(weight))
    direct = polynomial + (alpha - x[1]) * (radicand - alpha ** degree)
    assert s.expand(representation - direct) == 0
    return s.expand(representation)


def positive_definite(matrix):
    _, diagonal = matrix.LDLdecomposition(hermitian=False)
    assert all(diagonal[j, j] > 0 for j in range(matrix.rows))


degrees = (3, 5)
sizes = (2, 3)
roots = (s.Rational(-1, 2), s.Rational(3, 4))
boxes = ((s.Rational(-51, 100), s.Rational(-49, 100)),
         (s.Rational(7, 10), s.Rational(4, 5)))
constants = (s.Rational(-1, 8), s.Rational(2035, 1024))
coefficients = (s.Integer(2), s.Integer(-3))
first_radicand = (constants[0], constants[0])
second_radicand = interval_affine(constants[1], [
    (coefficients[e - 1], interval_power(boxes[0], e)) for e in (1, 2)
])
for box, degree, radicand in zip(boxes, degrees, (first_radicand, second_radicand)):
    lower, upper = interval_power(box, degree)
    assert lower <= radicand[0] <= radicand[1] <= upper
assert roots[0] ** 3 == constants[0]
assert roots[1] ** 5 == constants[1] + 2 * roots[0] - 3 * roots[0] ** 2

signs = (-1, 1)
kappa = max(s.Integer(1), *[1 / min(abs(t) for t in box) for box in boxes])
alpha = tuple(sign * kappa * root for sign, root in zip(signs, roots))
normalized_boxes = tuple(tuple(sorted(sign * kappa * t for t in box))
                         for sign, box in zip(signs, boxes))
normalized_constants = tuple(signs[i] * kappa ** degrees[i] * constants[i] for i in (0, 1))
normalized_coefficients = tuple(signs[1] * signs[0] ** e * kappa ** (degrees[1] - e)
                                * coefficients[e - 1] for e in (1, 2))
normalized_radicand = interval_affine(normalized_constants[1], [
    (normalized_coefficients[e - 1], interval_power(normalized_boxes[0], e)) for e in (1, 2)
])
assert normalized_radicand == tuple(kappa ** 5 * t for t in second_radicand)
assert all(1 <= box[0] <= value <= box[1] for box, value in zip(normalized_boxes, alpha))
assert alpha[0] ** 3 == normalized_constants[0]
assert alpha[1] ** 5 == normalized_constants[1] + sum(
    normalized_coefficients[e - 1] * alpha[0] ** e for e in (1, 2)
)
for i in (0, 1):
    for e in range(1, sizes[i] + 1):
        assert (s.Rational(signs[i], 1) / kappa) ** e * alpha[i] ** e == roots[i] ** e

N = sum(sizes)
A = 3 + sum(box[1] for box in normalized_boxes)
A += sum(abs(value) for value in normalized_constants + normalized_coefficients)
h0 = 1 / (N ** 2 * (N + 1) ** 2 * A ** (2 * N))
rho = (h0 / (2 * N * A)) ** 2
gamma = h0 * rho / 2
variables = s.symbols('x1 x2 y1 y2 y3')
blocks = (variables[:2], variables[2:])
radicands = (normalized_constants[0], normalized_constants[1] + sum(
    normalized_coefficients[e - 1] * blocks[0][e - 1] for e in (1, 2)
))
point = tuple(alpha[i] ** e for i in (0, 1) for e in range(1, sizes[i] + 1))
substitution = dict(zip(variables, point))
exposing = [local_exposing(alpha[i], blocks[i], radicands[i]) for i in (0, 1)]
for polynomial in exposing:
    assert polynomial.subs(substitution) == 0
    assert all(s.diff(polynomial, variable).subs(substitution) == 0 for variable in variables)
weighted = exposing[0] + rho * exposing[1]
H = s.hessian(weighted, variables) / 2
positive_definite(H - gamma * s.eye(N))

residuals = []
for block, radicand in zip(blocks, radicands):
    residuals += [block[0] * block[j] - block[j + 1] for j in range(len(block) - 1)]
    residuals += [block[-2] * block[-1] - radicand]
J = s.Matrix(residuals).jacobian(variables).subs(substitution)
assert J.det() == s.prod(degrees[i] * alpha[i] ** (degrees[i] - 1) for i in (0, 1))
V = 4 * N * A ** N
assert sum(entry ** 2 for entry in J) <= V ** 2

# Evaluate the zero-preserving representation at perturbed rational roots.
B0 = A + 1 + 32 * N ** 2 * (A + 1) ** (2 * N)
theta = gamma / (16 * B0 * A ** N)
approximations = (alpha[0] + theta, alpha[1] - theta)
symbol = s.Symbol('alpha')
approximated = [local_exposing(symbol, blocks[i], radicands[i]).subs(symbol, approximations[i])
                for i in (0, 1)]
G = s.expand(approximated[0] + rho * approximated[1])
assert G.subs(substitution) == 0
coefficient_error = sum(abs(value) for value in s.Poly(G - weighted, *variables).coeffs())
assert coefficient_error <= 2 * B0 * theta
gradient_error = s.Matrix([s.diff(G, variable).subs(substitution) for variable in variables])
assert gradient_error.dot(gradient_error) <= (4 * A ** N * B0 * theta) ** 2
positive_definite(s.hessian(G, variables) / 2 - gamma * s.eye(N) / 2)

print('PASS: mixed-sign interval normalization and recovery; signed predecessor powers.')
print('PASS: full-gradient cancellation; exact global exposing margin and Jacobian bound.')
print('PASS: coefficient approximation preserves exact zero, stated errors, and positive curvature.')
