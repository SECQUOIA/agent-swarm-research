#!/usr/bin/env python3
"""Exact finite diagnostics for Section 10's rational interpolation lemma.

This checks supplied algebraic fixtures, not general quantifier elimination
or the full network optimizer. All numerical inequalities use Fraction.
SymPy is used only for exact annihilator and resultant identities.
"""

from fractions import Fraction as F
import json

import sympy as sp


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rational(value):
    value = sp.Rational(value)
    return F(int(value.p), int(value.q))


def enclose_root(function, target, width, lower=F(0), upper=F(1)):
    require(function(lower) <= target <= function(upper), "invalid root bracket")
    while upper - lower > width:
        middle = (lower + upper) / 2
        if function(middle) < target:
            lower = middle
        else:
            upper = middle
    require(function(lower) <= target <= function(upper), "lost root enclosure")
    return lower, upper


def dyadic_below(bound):
    result = F(1)
    while result > bound:
        result /= 2
    return result


def merged_bands(critical_intervals, rho):
    padded = [(lo - rho, hi + rho) for lo, hi in critical_intervals]
    padded.extend([(-rho, rho), (1 - rho, 1 + rho)])
    intervals = sorted((max(F(0), lo), min(F(1), hi))
                       for lo, hi in padded if hi >= 0 and lo <= 1)
    result = []
    for lo, hi in intervals:
        if result and lo <= result[-1][1]:
            result[-1] = (result[-1][0], max(hi, result[-1][1]))
        else:
            result.append((lo, hi))
    return result


def gap_panels(left, right, rho):
    middle = (left + right) / 2
    result = []
    point = left
    while point < middle:
        following = min(middle, point + (point - left + rho) / 32)
        result.append((point, following))
        point = following
    point = right
    while point > middle:
        following = max(middle, point - (right - point + rho) / 32)
        result.append((following, point))
        point = following
    return sorted(result)


def interpolate(nodes, values):
    """Return dense rational coefficients via Newton divided differences."""
    differences = list(values)
    newton = [differences[0]]
    for order in range(1, len(nodes)):
        differences = [(differences[i + 1] - differences[i]) /
                       (nodes[i + order] - nodes[i])
                       for i in range(len(differences) - 1)]
        newton.append(differences[0])
    polynomial = [newton[-1]]
    for i in range(len(newton) - 2, -1, -1):
        product = [F(0)] * (len(polynomial) + 1)
        for j, coefficient in enumerate(polynomial):
            product[j] -= nodes[i] * coefficient
            product[j + 1] += coefficient
        product[0] += newton[i]
        polynomial = product
    return polynomial


def evaluate(coefficients, point):
    result = F(0)
    for coefficient in reversed(coefficients):
        result = result * point + coefficient
    return result


def run():
    t, y = sp.symbols("t y")
    small = F(1, 256)
    pole = F(1, 64)
    eta = F(1, 16)
    fifth = y**5 + y - t
    require(sp.resultant(fifth, sp.diff(fifth, y), y) == 3125*t**4 + 256,
            "quintic discriminant identity")
    repeated = (t - sp.Rational(1, 3)) * fifth**2 * (y + 7)
    primitive = sp.Poly(repeated, y).primitive()[1]
    squarefree = primitive.sqf_part().as_expr()
    require(sp.expand(sp.Poly(squarefree, y).monic().as_expr() - fifth*(y+7)) == 0,
            "content and squarefree product identity")

    def fifth_critical(width):
        lo, hi = enclose_root(lambda x: x**4, F(64, 3125), width)
        return [(lo, hi), (-hi, -lo)]

    fixtures = [
        ("implicit_quintic", fifth, F(1), fifth_critical,
         lambda x, width: enclose_root(lambda z: z**5 + z, x, width)),
        ("real_branch_switch", y**2 - (t-sp.Rational(1, 3))**2, F(1),
         lambda width: [(F(1, 3), F(1, 3))],
         lambda x, width: (abs(x-F(1, 3)), abs(x-F(1, 3)))),
        ("near_nonreal_branch_points", y**2 - (t-sp.Rational(1, 2))**2
         - sp.Rational(small.numerator, small.denominator)**2, F(1),
         lambda width: [(F(1, 2), F(1, 2))],
         lambda x, width: enclose_root(lambda z: z*z,
                                      (x-F(1, 2))**2 + small**2, width)),
        ("near_external_pole", (t+sp.Rational(1, 64))*y-1, pole**-2,
         lambda width: [(-pole, -pole)],
         lambda x, width: (1/(x+pole), 1/(x+pole))),
    ]
    rows = []
    for name, polynomial, lipschitz, critical, oracle in fixtures:
        coefficients = sp.Poly(polynomial, y).all_coeffs()
        leading = sp.Poly(coefficients[0], t)
        leading_degree = leading.degree()
        leading_scalar = rational(leading.LC())
        exceptional = sp.expand(coefficients[0] *
                                sp.resultant(polynomial, sp.diff(polynomial, y), y))
        exceptional_degree = sp.degree(exceptional, t)
        rho = dyadic_below(min(F(1, 16), eta/(64*lipschitz*(exceptional_degree+1))))
        real_parts = critical(rho)
        bands = merged_bands(real_parts, rho)
        require(sum(hi-lo for lo, hi in bands) <= 4*(exceptional_degree+1)*rho,
                name + ": merged-band length")
        band_checks = 0
        for lo, hi in bands:
            center = (lo+hi)/2
            bracket = oracle(center, eta/8)
            value = sum(bracket)/2
            for point in (lo, center, hi):
                lower, upper = oracle(point, eta/64)
                require(max(abs(value-lower), abs(value-upper)) <= eta/4,
                        name + ": bad-band constant error")
                band_checks += 1

        coefficient_bound = max(F(1), max(
            sum(abs(rational(coefficient))*2**power[0]
                for power, coefficient in sp.Poly(a, t).terms())
            for a in coefficients))
        complex_bound = 1 + coefficient_bound / (
            abs(leading_scalar)*(3*rho/4)**leading_degree)
        order = 1
        while complex_bound/F(2)**order > eta/8:
            order += 1
        node_tolerance = eta/(8*(2*order)**order)
        selected = []
        all_count = 0
        geometry_checks = 0
        for first, second in zip(bands, bands[1:]):
            a, b = first[1], second[0]
            panels = gap_panels(a, b, rho)
            all_count += len(panels)
            for left, right in panels:
                center, half = (left+right)/2, (right-left)/2
                distance = min(center-a+rho, b-center+rho)
                radius = distance/4
                require(half <= radius/16, name + ": analytic panel radius")
                for lo, hi in real_parts:
                    real_distance = min(abs(center-lo), abs(center-hi))
                    require(not lo <= center <= hi and real_distance >= distance,
                            name + ": distance from exceptional real part")
                require(radius > 0 and center+radius < 2,
                        name + ": root-bound disk range")
                geometry_checks += 1
            indices = {0, len(panels)//4, len(panels)//2, 3*len(panels)//4, len(panels)-1}
            selected.extend((a, b, panels[i]) for i in sorted(indices))

        interpolation_checks = 0
        encoding_bits = 0
        for a, b, (left, right) in selected:
            center, half = (left+right)/2, (right-left)/2
            radius = min(center-a+rho, b-center+rho)/4
            remainder = complex_bound*radius/(radius-half) * (
                2*half/(radius-half))**(order+1)
            require(remainder <= complex_bound/F(2)**order <= eta/8,
                    name + ": exact contour-remainder bound")
            nodes = [left+(right-left)*i/order for i in range(order+1)]
            brackets = [oracle(node, node_tolerance) for node in nodes]
            values = [sum(pair)/2 for pair in brackets]
            interpolant = interpolate(nodes, values)
            for node, value in zip(nodes, values):
                require(evaluate(interpolant, node) == value,
                        name + ": exact interpolation identity")
            for i in range(17):
                point = left+(right-left)*i/16
                estimate = evaluate(interpolant, point)
                lower, upper = oracle(point, eta/128)
                require(max(abs(estimate-lower), abs(estimate-upper)) <= eta/4,
                        name + ": certified sampled approximation error")
                interpolation_checks += 1
            encoding_bits = max(encoding_bits, max(
                coefficient.numerator.bit_length()+coefficient.denominator.bit_length()
                for coefficient in interpolant))
        rows.append({"fixture": name, "degree": sp.degree(polynomial, y),
                     "exceptional_degree": int(exceptional_degree), "order": order,
                     "panels_constructed": all_count, "geometry_checks": geometry_checks,
                     "panels_interpolated": len(selected), "band_checks": band_checks,
                     "certified_sample_checks": interpolation_checks,
                     "largest_coefficient_encoding_bits": encoding_bits})
    print(json.dumps({"passed": True, "arithmetic": "exact rational",
                      "fixtures": rows, "scope": "finite examples; no general QE implementation"},
                     indent=2, default=int))


if __name__ == "__main__":
    run()
