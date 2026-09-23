"""Mechanism checks for the affine-load weighted cactus approximation theorem.

Exact fractions certify sampled sqrt approximation errors by squaring rational
interval endpoints. Random cycle tests independently compare the selected local
quadratic/rational formula with monotone scalar root finding. These checks do
not implement the fixed-dimensional semialgebraic global optimizer.
"""
from fractions import Fraction as F
import json
import random
import numpy as np
from scipy.optimize import brentq


def sqrt_panel_parameters(bits):
    eta = F(1, 2**bits)
    degree = 0
    while F(9, 2) * F(7, 9) ** (degree + 1) > eta:
        degree += 1
    return bits, degree


def sqrt_surrogate(x, bits):
    """Evaluate a panel polynomial using only exact rational arithmetic."""
    assert 0 <= x <= 1
    panels, degree = sqrt_panel_parameters(bits)
    if x <= F(1, 4**panels):
        return F(0)
    for j in range(panels):
        if F(1, 4**(j + 1)) <= x <= F(1, 4**j):
            center = F(9, 16 * 4**j)
            v = x / center - 1
            coefficient = F(1)
            value = coefficient
            power = F(1)
            for k in range(1, degree + 1):
                coefficient *= (F(1, 2) - (k - 1)) / k
                power *= v
                value += coefficient * power
            return F(3, 4 * 2**j) * value
    raise AssertionError('Uncovered input')


def exact_error_check(value, x, eta):
    """Certify |value-sqrt(x)|<=eta without computing any square root."""
    lower, upper = value - eta, value + eta
    assert upper >= 0 and upper * upper >= x
    assert lower <= 0 or lower * lower <= x


def run():
    panel_checks = 0
    panel_summary = []
    for bits in (4, 8, 12, 20):
        panels, degree = sqrt_panel_parameters(bits)
        samples = {F(0), F(1), F(1, 4**panels)}
        for j in range(panels):
            lo, hi = F(1, 4**(j+1)), F(1, 4**j)
            samples.update(lo + (hi-lo)*F(k, 8) for k in range(9))
        for x in sorted(samples):
            exact_error_check(sqrt_surrogate(x, bits), x, F(1, 2**bits))
            panel_checks += 1
        panel_summary.append({'bits': bits, 'nonzero_panels': panels,
                              'degree': degree, 'exact_samples': len(samples)})

    rng = random.Random(690606)
    counts = {'negative_A': 0, 'positive_A': 0, 'rational_A_zero': 0}
    worst_flow_error = 0.0
    worst_drop_error = 0.0
    # Each cycle receives an affine function of the same two parameters.
    for _ in range(1200):
        n = rng.randrange(3, 12)
        z = np.array([rng.uniform(-2, 2), rng.uniform(-2, 2)])
        offsets = np.array([rng.randrange(-5, 6) +
                            np.dot([rng.randrange(-3, 4), rng.randrange(-3, 4)], z)
                            for _ in range(n)])
        positive = np.array([rng.randrange(1, 8) for _ in range(n)])
        negative = np.array([rng.randrange(1, 8) for _ in range(n)])
        def law(x):
            return np.where(x >= 0, positive * x*x, -negative * x*x)
        q = brentq(lambda s: float(sum(law(s + offsets))),
                   -max(offsets)-1, -min(offsets)+1, xtol=1e-13)
        x = q + offsets
        coefficients = np.where(x >= 0, positive, -negative)
        A = int(sum(coefficients))
        B = float(2 * np.dot(coefficients, offsets))
        C = float(np.dot(coefficients, offsets * offsets))
        if A:
            discriminant = B*B - 4*A*C
            assert discriminant >= -1e-8
            q_formula = (-B + np.sqrt(max(0., discriminant))) / (2*A)
            counts['positive_A' if A > 0 else 'negative_A'] += 1
        else:
            assert B > 0
            q_formula = -C/B
            counts['rational_A_zero'] += 1
        worst_flow_error = max(worst_flow_error, abs(q-q_formula))
        weights = np.array([rng.randrange(-5, 6) for _ in range(n)])
        exact_drop = float(np.dot(weights, law(x)))
        formula_drop = float(np.dot(weights * coefficients,
                                    (q_formula+offsets)**2))
        worst_drop_error = max(worst_drop_error, abs(exact_drop-formula_drop))
    assert worst_flow_error < 1e-10
    assert worst_drop_error < 1e-8
    # Explicit singular A=B=0 stratum of an even cycle: all offsets coincide,
    # all physical flows vanish, and signs can be assigned two each way.
    offsets = np.array([3., 3., 3., 3.])
    coefficients = np.array([1., 1., -1., -1.])
    assert sum(coefficients) == 0 and np.dot(coefficients, offsets) == 0
    assert np.all(-offsets[0]+offsets == 0)
    assert all(counts.values())
    report = {'sqrt_panels': panel_summary, 'exact_rational_sqrt_checks': panel_checks,
              'cycle_branch_counts': counts, 'maximum_flow_formula_error': worst_flow_error,
              'maximum_weighted_drop_formula_error': worst_drop_error,
              'all_zero_singular_stratum': 'passed'}
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    run()
