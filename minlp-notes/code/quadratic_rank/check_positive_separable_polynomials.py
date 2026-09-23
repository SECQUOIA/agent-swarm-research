"""Exact checks for power-coordinate lower bounds and shared Taylor bands."""

import random

import sympy as sp

rng = random.Random(2026090554)
jensen_cases = band_cases = covariance_cases = 0
for degree in range(2, 13):
    for power in range(2, degree + 1):
        for trial in range(12):
            first = sp.Rational(rng.randint(0, 16), 16)
            second = sp.Rational(rng.randint(0, 16), 16)
            if trial == 0:
                first, second = sp.Integer(0), sp.Integer(1)
            a, b = first ** 2, second ** 2
            gap = (a ** power + b ** power) / 2 - ((a + b) / 2) ** power
            transformed_square = (first ** degree - second ** degree) ** 2
            assert gap >= transformed_square / degree ** 2
            jensen_cases += 1

for rank in range(1, 5):
    degrees = [rng.randint(2, 9) for _ in range(rank)]
    coefficients = [[[sp.Integer(rng.randint(0, 4)) for _ in range(degree - 1)]
                     for degree in degrees] for _ in range(3)]
    for output in range(3):
        for i in range(rank):
            coefficients[output][i][0] += 1
    sums = [[sum(coefficients[j][i]) for i in range(rank)] for j in range(3)]
    allocation = [sp.Rational(1, rng.randint(1, 8)) for _ in range(rank)]
    tolerance = [sum(sums[j][i] * allocation[i] for i in range(rank)) for j in range(3)]
    for _ in range(16):
        points = []
        values = []
        mixed = []
        for degree, allocated in zip(degrees, allocation):
            depth = 0
            while sp.Integer(2) ** (2 * depth) * allocated < degree ** 2:
                depth += 1
            width = sp.Rational(1, 2 ** depth)
            bits = [rng.randint(0, 1) for _ in range(depth)]
            weights = [sp.Rational(1, 2 ** (l + 1)) for l in range(depth)]
            base = sum(bit * weight for bit, weight in zip(bits, weights))
            residual = width * sp.Rational(rng.randint(0, 8), 8)
            points.append(base + residual)
            powers = [sp.Integer(1)]
            products = [residual]
            for power in range(1, degree + 1):
                next_value = sum(weight * bit * powers[-1] for bit, weight in zip(bits, weights))
                next_product = sum(weight * bit * products[-1] for bit, weight in zip(bits, weights))
                assert next_value == base ** power
                assert next_product == base ** power * residual
                assert 0 <= next_value <= 1
                assert 0 <= next_product <= width
                powers.append(next_value)
                products.append(next_product)
            values.append(powers)
            mixed.append(products)
        for j in range(3):
            exact = sum(coefficients[j][i][k - 2] * points[i] ** k
                        for i in range(rank) for k in range(2, degrees[i] + 1))
            tangent = sum(coefficients[j][i][k - 2] * (values[i][k] + k * mixed[i][k - 1])
                          for i in range(rank) for k in range(2, degrees[i] + 1))
            assert 0 <= exact - tangent <= tolerance[j] / 2
            assert abs(tangent - exact) <= tolerance[j] / 2
            assert abs(tangent + tolerance[j] / 2 - exact) <= tolerance[j] / 2
            band_cases += 1

    original_points = [[sp.Rational(rng.randint(0, 8), 8) ** 2 for _ in range(rank)] for _ in range(5)]
    transformed = [sp.Matrix([sp.sqrt(point[i]) ** degrees[i] for i in range(rank)]) for point in original_points]
    mean = sum(transformed, sp.zeros(rank, 1)) / len(transformed)
    covariance = sum(((point - mean) * (point - mean).T for point in transformed), sp.zeros(rank)) / len(transformed)
    lower_allocation = [2 * covariance[i, i] / degrees[i] ** 2 for i in range(rank)]
    assert all(0 <= value <= 1 for value in lower_allocation)
    for j in range(3):
        def polynomial(point):
            return sum(coefficients[j][i][k - 2] * point[i] ** k
                       for i in range(rank) for k in range(2, degrees[i] + 1))
        maximum_gap = max((polynomial(x) + polynomial(y)) / 2 - polynomial([(a + b) / 2 for a, b in zip(x, y)])
                          for x in original_points for y in original_points)
        assert sum(sums[j][i] * lower_allocation[i] for i in range(rank)) <= maximum_gap
        covariance_cases += 1

print(f'PASS: {jensen_cases} exact power Jensen bounds, {band_cases} recursive-prefix Taylor bands, '
      f'and {covariance_cases} transformed-covariance allocations')
