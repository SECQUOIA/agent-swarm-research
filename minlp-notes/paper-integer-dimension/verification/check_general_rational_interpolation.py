#!/usr/bin/env python3
"""Exact checks of signed rational endpoint interpolation, including zero bits.

These finite cases exercise the general denominator gadget beyond its positive
Stieltjes special case. They supplement the proof and do not certify it.
"""
from fractions import Fraction as Q


def value(coefficients, x):
    return sum((c * x**k for k, c in enumerate(coefficients)), Q(0))


def product(a, b):
    c = [Q(0)] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            c[i+j] += u*v
    return c


denominator = [Q(5, 16), Q(-1), Q(1)]  # (x-1/2)^2 + 1/16
q_min = Q(1, 16)
examples = [
    ([Q(0), Q(1), Q(-1)], denominator),
    (product([Q(0), Q(-3), Q(12), Q(-8)], denominator), denominator),
    ([Q(-2)], [Q(3)]),
]
cases = 0
outside = 0
for numerator, den in examples:
    degree = max(len(numerator), len(den)) - 1
    bound = q_min if den == denominator else Q(3)
    for depth in range(5):
        h = Q(1, 2**depth)
        for index in range(2**depth):
            bits = [(index >> (depth-j)) & 1 for j in range(1, depth+1)]
            prefix = sum((Q(bit, 2**j) for j, bit in enumerate(bits, 1)), Q(0))
            assert prefix == index*h
            for weight in [Q(0), Q(1, 7), Q(1, 2), Q(6, 7), Q(1)]:
                contributions = []
                for offset, theta in [(0, 1-weight), (1, weight)]:
                    t = prefix + offset*h
                    qt = value(den, t)
                    assert qt >= bound > 0
                    variables = [t**k * theta/qt for k in range(degree+1)]
                    assert all(0 <= v <= 1/bound for v in variables)
                    assert sum(c*variables[k] for k, c in enumerate(den)) == theta
                    for k in range(1, degree+1):
                        previous = variables[k-1]
                        products = [bit*previous for bit in bits]
                        for bit, z in zip(bits, products):
                            assert 0 <= z <= bit/bound
                            assert z <= previous and z >= previous-(1-bit)/bound
                        recurrence = sum((Q(1, 2**j)*z for j, z in enumerate(products, 1)), Q(0))
                        recurrence += offset*h*previous
                        assert recurrence == variables[k]
                    contribution = sum(c*variables[k] for k, c in enumerate(numerator))
                    assert contribution == theta*value(numerator, t)/qt
                    contributions.append(contribution)
                interpolant = sum(contributions)
                exact = (1-weight)*value(numerator, prefix)/value(den, prefix)
                exact += weight*value(numerator, prefix+h)/value(den, prefix+h)
                assert interpolant == exact
                outside += int(not 0 <= interpolant <= 1)
                cases += 1

assert cases == 465
assert outside > 0  # The general gadget must retain any original input bounds.
print(f"PASS: {cases} exact signed rational interpolation cases; {outside} values require input clipping.")
