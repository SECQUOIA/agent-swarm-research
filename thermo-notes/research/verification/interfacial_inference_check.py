"""Deterministic checks for the positive radial-kernel interface scout.

The radius measures below are limiting shell measures, not smooth potentials.
The note proves a common smooth convolution construction separately. Numerical
quadrature error is estimated by scipy; the additional spectral tail bound is
analytic. This is not an interval-arithmetic certificate.
"""
import json
from pathlib import Path

import numpy as np
from scipy.integrate import quad

MODELS = {
    "lower_first_moment": (np.array([0.0, np.sqrt(0.75)]), np.array([1 / 3, 2 / 3])),
    "upper_first_moment": (np.array([0.5, 1.0]), np.array([2 / 3, 1 / 3])),
}


def tension(radii, weights, a, cutoff=2000.0):
    moments = {n: np.dot(weights, radii**n) for n in (2, 4, 6)}

    def integrand(k):
        if k == 0:
            return moments[2] / 6
        if abs(k) < 1e-3:
            d = moments[2] * k**2 / 6 - moments[4] * k**4 / 120 + moments[6] * k**6 / 5040
        else:
            d = np.dot(weights, 1 - np.sinc(k * radii / np.pi))
        return a * d / (a + d) / k**2

    value, quadrature_error = quad(integrand, 0, cutoff, epsabs=1e-9, limit=2000)
    d_infinity = 1 - weights[radii == 0].sum()
    value = 2 / np.pi * (value + a * d_infinity / (a + d_infinity) / cutoff)
    positive = radii > 0
    # |sin(kr)/(kr)| <= 1/(kr), and derivative of a D/(a+D) <= 1.
    tail_error_bound = np.sum(weights[positive] / radii[positive]) / (np.pi * cutoff**2)
    return {
        "tension": float(value),
        "quadrature_error_estimate": float(2 / np.pi * quadrature_error),
        "tail_error_bound": float(tail_error_bound),
    }


def main():
    results = {"mass": 1.0, "range": 1.0, "models": {}, "finite_a": {}}
    for name, (radii, weights) in MODELS.items():
        moments = {str(n): float(np.dot(weights, radii**n)) for n in (0, 1, 2, 4)}
        assert abs(moments["0"] - 1) < 1e-14
        assert abs(moments["2"] - 0.5) < 1e-14
        assert abs(moments["4"] - 0.375) < 1e-14
        results["models"][name] = {"moments": moments, "strong_well_tension": moments["1"] / 2}
    for a in (1.0, 5.0, 20.0, 100.0):
        results["finite_a"][str(a)] = {name: tension(r, w, a) for name, (r, w) in MODELS.items()}
    destination = Path(__file__).with_name("interfacial-inference-check.json")
    destination.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
