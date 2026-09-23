"""Compare fixed designs and an admissible adaptive design under uncertainty.

The adaptive field is an explicit trial, not a finite-budget optimum. Its
fold-region construction deliberately gives a controlled upper comparison.
"""
import json
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import solve_banded
from scipy.special import beta, gamma


def inverse_integral(offset, face_mobility, n):
    dx = np.pi/n
    x = (np.arange(n)+0.5)*dx
    conductance = face_mobility/dx**2
    matrix = np.zeros((3, n))
    matrix[1] = (offset+np.cos(x))**2
    matrix[1, :-1] += conductance
    matrix[1, 1:] += conductance
    matrix[0, 1:] = matrix[2, :-1] = -conductance
    return float(2*dx*np.sum(solve_banded((1, 1), matrix, np.ones(n))))


def adaptive_trial(offset, budget, faces, dx):
    if offset >= 1:
        return np.full(len(faces), budget/(2*np.pi))
    root = np.arccos(-offset)
    curvature = 1-offset*offset
    radius = (40*budget/(3*curvature))**0.2
    if radius < 0.3*min(root, np.pi-root):
        y = abs(faces-root)/radius
        d = np.where(y < 1, curvature*radius**4/8*y*(1-y)**2*(1+2*y), 0)
    else:
        # For offset >= 0, the merging zeros approach pi.
        extent = min(np.pi, max(4*budget**(1/7), 2*(np.pi-root)))
        d = np.where(faces > np.pi-extent, budget/(2*extent), 0)
    d *= budget/(2*dx*np.sum(d))
    return d


def check(budget, n=16384, nq=40):
    dx = np.pi/n
    faces = np.arange(1, n)*dx
    blind = budget*np.sin(faces)**(-0.4)/(2*beta(0.3, 0.5))
    uniform = np.full(n-1, budget/(2*np.pi))
    widths = [(budget/(4*np.pi))**(1/3), budget**(2/7)]
    breaks = [0, 0.5, 0.9, 1, 1.1, 1.5, 2]
    for w in widths:
        breaks.extend([1-w, 1+w, 1-10*w, 1+10*w])
    breaks = np.unique(np.clip(breaks, 0, 2))
    points, weights = leggauss(nq)
    values = np.zeros(3)
    for lo, hi in zip(breaks[:-1], breaks[1:]):
        for point, weight in zip((lo+hi)/2+(hi-lo)/2*points, weights):
            designs = [uniform, blind, adaptive_trial(point, budget, faces, dx)]
            results = [inverse_integral(point, d, n) for d in designs]
            values += (hi-lo)/4*weight*np.array(results)
    c0 = np.pi/2*gamma(0.25)/gamma(0.75)
    placement = 12*(3/80)**0.2
    blind_coef = c0*(0.25**0.8*2*beta(0.3, 0.5))**1.25
    adaptive_coef = placement*2**1.2/4*beta(0.5, 0.2)
    return {"budget": budget, "half_wall_grid": n, "quadrature_nodes": nq,
            "uniform_mean": values[0], "blind_design_mean": values[1],
            "adaptive_trial_mean": values[2],
            "scaled_uniform_mean": values[0]*budget**0.25,
            "scaled_blind_mean": values[1]*budget**0.25,
            "scaled_adaptive_trial_mean": values[2]*budget**0.2,
            "blind_asymptotic_coefficient": blind_coef,
            "adaptive_optimum_asymptotic_coefficient": adaptive_coef,
            "blind_to_uniform_ratio": values[1]/values[0],
            "adaptive_trial_to_blind_ratio": values[2]/values[1]}


def main():
    rows = [check(m) for m in [1e-3, 1e-6, 1e-9]]
    refined = check(1e-9, n=32768, nq=60)
    result = {"comparisons": rows, "refined_smallest_budget": refined,
              "scope": "Blind design is asymptotically optimal; adaptive values use a conservative trial and do not numerically certify the adaptive optimum at these finite budgets."}
    Path("results").mkdir(exist_ok=True)
    Path("results/robust-design-checks.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
