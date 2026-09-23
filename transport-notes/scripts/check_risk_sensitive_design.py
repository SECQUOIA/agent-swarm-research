"""Check admissible graded mobility trials for positive disorder moments.

This does not optimize the discretized design. The order theorem applies to
the continuum infimum; these trials check its constructive upper bounds.
"""
import json
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss

from check_robust_design import inverse_integral


def graded_design(budget, order, faces):
    alpha = (6*order-4)/(order+4)
    if order < 1.6:
        radius = budget**(1/(6+alpha))
    elif order == 1.6:
        radius = (budget/np.log(1/budget))**(1/7)
    else:
        radius = budget**(1/7)
    half_interval = np.pi/2
    if abs(alpha-1) < 1e-12:
        normalization = 4*np.log1p(half_interval/radius)
    else:
        normalization = 4*((half_interval+radius)**(1-alpha)
                           - radius**(1-alpha))/(1-alpha)
    amplitude = budget/normalization
    distance = np.minimum(faces, np.pi-faces)
    return amplitude*(distance+radius)**(-alpha), radius, alpha


def check(budget, order, n=32768, nq=40):
    dx = np.pi/n
    faces = np.arange(1, n)*dx
    graded, radius, alpha = graded_design(budget, order, faces)
    uniform = np.full(n-1, budget/(2*np.pi))
    breaks = [0, 0.5, 0.9, 1, 1.1, 1.5, 2]
    for width in [radius**2, (budget/(4*np.pi))**(1/3)]:
        for multiplier in [0.1, 1, 10, 100]:
            breaks.extend([1-width*multiplier, 1+width*multiplier])
    breaks = np.unique(np.clip(breaks, 0, 2))
    points, weights = leggauss(nq)
    moments = np.zeros(2)
    for lo, hi in zip(breaks[:-1], breaks[1:]):
        for offset, weight in zip((lo+hi)/2+(hi-lo)/2*points, weights):
            values = np.array([inverse_integral(offset, d, n)
                               for d in [graded, uniform]])
            # Reflection symmetry reduces the expectation (1/4) int[-2,2].
            moments += (hi-lo)/4*weight*values**order
    if order < 1.6:
        scale = budget**(order/4)
    elif order == 1.6:
        scale = budget**0.4/np.log(1/budget)**1.4
    else:
        scale = budget**((3*order-2)/7)
    return {"budget": budget, "order": order, "half_wall_grid": n,
            "quadrature_nodes": nq, "radius": radius, "tail_exponent": alpha,
            "graded_trial_moment": moments[0], "uniform_moment": moments[1],
            "trial_to_uniform_ratio": moments[0]/moments[1],
            "scaled_trial_moment": moments[0]*scale}


def main():
    rows = []
    for q in [1.2, 1.6, 2, 3]:
        for budget in [1e-3, 1e-6, 1e-9, 1e-12]:
            row = check(budget, q)
            rows.append(row)
            print(json.dumps(row), flush=True)
    refined = [check(1e-12, q, n=65536, nq=60) for q in [1.6, 3]]
    result = {"trials": rows, "refinement": refined,
              "scope": "Explicit graded admissible trials, not finite-budget optima or evidence for sharp optimal constants."}
    Path("results/risk-sensitive-design-checks.json").write_text(
        json.dumps(result, indent=2)+"\n")
    print(json.dumps({"refinement": refined}), flush=True)


if __name__ == "__main__":
    main()
