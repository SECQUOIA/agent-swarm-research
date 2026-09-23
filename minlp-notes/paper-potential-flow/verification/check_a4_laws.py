#!/usr/bin/env python3
"""Focused S2 regressions; not a certified global optimizer or proof.

Exact symbolic checks cover denominator clearing, the odd-power extension,
flat-piece coefficient tests, and even-denominator SRS data. Floating-point
quadrature and physical-state comparisons supplement the analytic proofs.
Requires numpy, scipy and sympy in the project's research environment.
"""
from fractions import Fraction
from math import ceil
import random

import numpy as np
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss
import sympy as sp

COUNTS = {}


def check(ok, kind):
    if not ok:
        raise AssertionError(kind)
    COUNTS[kind] = COUNTS.get(kind, 0) + 1


def exact_encoding_checks():
    x, c, z, w, v = sp.symbols('x c z w v')
    # The new q>3 range relies on this derivative for arbitrary fixed j.
    for j in range(6):
        term = x**(2*j+3)/(x*x+c)
        asserted = x**(2*j+2)*((2*j+1)*x*x+(2*j+3)*c)/(x*x+c)**2
        check(sp.cancel(sp.diff(term, x)-asserted) == 0, 'odd_power_derivative')
    # Three edges with independent resistance coefficients and two core
    # variables. Compare a cleared cycle/path equation with direct evaluation.
    flows = [z, w-z, 1-w]
    beta = sp.symbols('b0:3')
    nums = [f**(2*j+3)*(f*f+2)+sp.Rational(j+1, 3)*f**(2*j+3)
            for j, f in enumerate(flows)]
    dens = [(f*f+1)*(f*f+2) for f in flows]
    common = sp.prod(dens)
    cleared = sp.expand(sum(beta[i]*nums[i]*sp.prod(dens[k] for k in range(3) if k != i)
                            for i in range(3))-v*common)
    poly = sp.Poly(cleared, z, w, v, *beta)
    check(poly.degree(v) == 1 and all(poly.degree(b) == 1 for b in beta),
          'clearing_preserves_leaf_linearity')
    rng = random.Random(4004)
    for _ in range(20):
        vals = {z: sp.Rational(rng.randint(-8, 8), 3),
                w: sp.Rational(rng.randint(-8, 8), 5), v: sp.Rational(2, 7)}
        vals.update({b: sp.Rational(rng.randint(1, 9), 4) for b in beta})
        direct = sum(beta[i]*nums[i]/dens[i] for i in range(3))-v
        check(common.subs(vals) > 0 and
              cleared.subs(vals) == (common*direct).subs(vals),
              'exact_cleared_equation')
    # A polynomial derivative can vanish at a point without a flat piece.
    theta = sp.symbols('theta')
    for deriv, expected in [(1-theta, {1}), (1+theta, {-1}),
                            (3*(1-theta)*x*x+theta, set())]:
        sol = sp.solve(sp.Poly(deriv, x).all_coeffs(), [theta], dict=True)
        got = {s[theta] for s in sol}
        check(got == expected, 'flat_piece_coefficient_matching')
    # Exact even-denominator threshold contributions, including q>3.
    for exponent in [Fraction(3, 2), Fraction(5, 4), Fraction(7, 2), Fraction(13, 4)]:
        p, q = exponent.numerator, exponent.denominator
        for a in [2, 3, 7, 16, 23]:
            flow = sp.Integer(a)**(q//2)
            resistance = sp.Integer(a)**(-(p-1)//2)
            check(sp.simplify(resistance*flow**sp.Rational(p, q)-sp.sqrt(a)) == 0,
                  'even_denominator_radical_identity')


def rational_rounding_checks():
    # Exact regression for upward rounding, including a weight far below
    # machine precision. The test does not pretend to enclose Gauss roots.
    h = Fraction(1, 2**40)
    pairs = [(Fraction(1, 2**1000), Fraction(1, 256)),
             (Fraction(19, 7), Fraction(2, 97)),
             (Fraction(2, 3), Fraction(173, 5))]
    def upward(number):
        ratio = number/h
        return ((ratio.numerator+ratio.denominator-1)//ratio.denominator)*h
    rounded = [(upward(a), upward(s)) for a, s in pairs]
    for (a, s), (ar, sr) in zip(pairs, rounded):
        check(0 < ar and 0 < sr and 0 <= ar-a <= h and 0 <= sr-s <= h,
              'positive_rational_upward_rounding')
    def evaluate(data, t):
        return sum((a*t/(t+s) for a, s in data), Fraction(0))
    bound = len(pairs)*h*(1+2**17)
    for t in [Fraction(0), Fraction(1, 10**15), Fraction(1, 3), Fraction(1)]:
        check(abs(evaluate(pairs, t)-evaluate(rounded, t)) <= bound,
              'exact_rational_rounding_bound')
    norm = evaluate(rounded, Fraction(1))
    normalized = [(a/norm, s) for a, s in rounded]
    check(evaluate(normalized, Fraction(1)) == 1, 'exact_rational_normalization')


def scalar_approximant(alpha, precision=16):
    # Conservative analytical budget as in Lemma 4.8. This uses floating
    # Gauss data; it checks formulas, not the rational enclosure algorithm.
    zeta = 2.0**(-precision)/24
    length = max(1, ceil(np.log2(4/(alpha*zeta))/alpha),
                 ceil(np.log2(4/((1-alpha)*zeta))/(1-alpha)))
    order = max(1, ceil((length+np.log2(32*length/zeta))/2))
    nodes, weights = leggauss(order)
    nodes = (nodes+3)/2
    weights = weights/2
    scales = np.exp2(np.arange(-length, length, dtype=float))
    s = (scales[:, None]*nodes).ravel()
    a = (scales[:, None]**alpha*nodes[None, :]**(alpha-1)*weights).ravel()
    normalizer = np.sum(a/(1+s))
    bound = (2**(-alpha*length)/alpha
             +2**(-(1-alpha)*length)/(1-alpha)+16*length*2.0**(length-2*order))
    def evaluate(t):
        return np.sum(a*t/(t+s))/normalizer
    check(np.all(a > 0) and np.all(s > 0), 'positive_quadrature_data')
    for t in np.r_[0, np.geomspace(1e-25, 1, 80)]:
        check(abs(evaluate(t)-t**alpha) <= 24*bound+1e-13,
              'scalar_uniform_sample')
    return evaluate, 24*bound


def phi(x, q):
    return np.sign(x)*abs(x)**q


def extended_fractional_checks():
    family = [Fraction(3, 2), Fraction(7, 2), Fraction(13, 4), Fraction(9, 2), Fraction(5)]
    surrogates = []
    errors = []
    flow_bound = 4.0
    for exponent in family:
        q = float(exponent)
        if exponent.denominator == 1 and exponent.numerator % 2 == 1:
            surrogates.append(lambda x, q=q: x**int(q))
            errors.append(0.0)
            continue
        j = (exponent.numerator-exponent.denominator)//(2*exponent.denominator)
        alpha = (q-2*j-1)/2
        scalar, error = scalar_approximant(alpha)
        def law(x, j=j, alpha=alpha, scalar=scalar):
            return flow_bound**(2*alpha)*x**(2*j+1)*scalar(x*x/flow_bound**2)
        surrogates.append(law)
        errors.append(flow_bound**q*error)
        points = np.linspace(-flow_bound, flow_bound, 121)
        evaluated = [law(x) for x in points]
        check(np.all(np.diff(evaluated) > 0), 'extended_law_strict_sample')
        check(max(abs(y-phi(x, q)) for x, y in zip(points, evaluated)) <= errors[-1]+1e-10,
              'extended_law_error_sample')
    # Heterogeneous cycle at the same nominations/resistances. Subtracting
    # its two roots tests the circulation identity and physical error bound.
    base = np.array([1.0, -0.7, 0.2, -1.4, 0.8])
    beta = np.array([0.7, 1.3, 0.8, 1.1, 1.8])
    def equation(z, surrogate):
        return sum(beta[i]*(surrogates[i](base[i]+z) if surrogate
                           else phi(base[i]+z, float(family[i]))) for i in range(5))
    original_root = brentq(lambda z: equation(z, False), -1.5, 1.5, xtol=1e-14)
    surrogate_root = brentq(lambda z: equation(z, True), -1.5, 1.5, xtol=1e-14)
    x, y = base+original_root, base+surrogate_root
    dx = x-y
    lhs = sum(beta[i]*(phi(x[i], float(family[i]))-phi(y[i], float(family[i])))*dx[i]
              for i in range(5))
    rhs = sum(beta[i]*(surrogates[i](y[i])-phi(y[i], float(family[i])))*dx[i]
              for i in range(5))
    check(abs(lhs-rhs) <= 1e-11, 'heterogeneous_circulation_identity')
    h = ceil(max(float(q) for q in family))
    cstar = 2.0**(1-h)
    d = max(abs(dx))
    delta = max(errors)
    for q in family:
        check(d**float(q) <= len(base)*max(beta)*delta/(cstar*min(beta))+1e-10,
              'heterogeneous_physical_bound')
    rng = random.Random(441)
    for q in family:
        for _ in range(100):
            a, b = rng.uniform(-4, 4), rng.uniform(-4, 4)
            left = (phi(a, float(q))-phi(b, float(q)))*(a-b)
            check(left+1e-12 >= cstar*abs(a-b)**(float(q)+1), 'extended_strong_monotonicity')
    print(f'Numerical heterogeneous cycle root difference: {d:.3g}; law bound: {delta:.3g}')


if __name__ == '__main__':
    exact_encoding_checks()
    rational_rounding_checks()
    extended_fractional_checks()
    for name, count in sorted(COUNTS.items()):
        print(f'PASS: {name}: {count}')
    print(f'Total: {sum(COUNTS.values())} checks; numerical checks are regression evidence only.')
