"""Explore coalescing kinetic zeros and a bounded random-offset ensemble.

Candidate asymptotics only: this numerical exploration does not prove exchange
of the disorder average and the small-diffusion limit.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.linalg import solve_banded
from scipy.special import gamma, beta
from numpy.polynomial.legendre import leggauss


def pair_integral(mu, dx=0.003):
    extent = max(12.0, np.sqrt(max(mu, 0))+10)
    n = int(np.ceil(extent/dx))
    dx = extent/n
    x = (np.arange(n)+0.5)*dx
    potential = (x*x-mu)**2
    matrix = np.zeros((3, n))
    matrix[1] = potential+2/dx**2
    matrix[1, 0] -= 1/dx**2
    matrix[1, -1] += 1/dx**2
    matrix[0, 1:] = matrix[2, :-1] = -1/dx**2
    rhs = np.ones(n)
    rhs[-1] += 2/(dx*dx*(extent*extent-mu)**2)
    h = solve_banded((1, 1), matrix, rhs)
    tail = 2*quad(lambda y: 1/(y*y-mu)**2, extent, np.inf, epsabs=1e-12)[0]
    return float(2*dx*np.sum(h)+tail)


def periodic_integral(diffusivity, offset, n=16384):
    dx = np.pi/n
    s = (np.arange(n)+0.5)*dx
    matrix = np.zeros((3, n))
    matrix[1] = (offset+np.cos(s))**2+2*diffusivity/dx**2
    matrix[1, 0] -= diffusivity/dx**2
    matrix[1, -1] -= diffusivity/dx**2
    matrix[0, 1:] = matrix[2, :-1] = -diffusivity/dx**2
    return float(2*dx*np.sum(solve_banded((1, 1), matrix, np.ones(n))))


def ensemble(diffusivity, nodes=50, n=16384):
    width = (diffusivity/2)**(1/3)
    breaks = np.unique(np.clip([0, 0.5, 0.9, 1-10*width, 1-width, 1,
                               1+width, 1+10*width, 1.1, 1.5, 2], 0, 2))
    points, weights = leggauss(nodes)
    first, second = 0.0, 0.0
    powers = [0.5, 1.0, 4/3, 2.0, 3.0]
    moments = np.zeros(len(powers))
    for left, right in zip(breaks[:-1], breaks[1:]):
        offsets = (left+right)/2+(right-left)/2*points
        values = np.array([periodic_integral(diffusivity, c, n=n) for c in offsets])
        # Symmetry and uniform offset on [-2,2] give density 1/2 on [0,2].
        first += (right-left)/4*np.dot(weights, values)
        second += (right-left)/4*np.dot(weights, values*values)
        for index, power in enumerate(powers):
            moments[index] += (right-left)/4*np.dot(weights, values**power)
    c0 = np.pi/2*gamma(0.25)/gamma(0.75)
    spectrum = []
    for power, moment in zip(powers, moments):
        if power < 4/3:
            scaled = moment*diffusivity**(power/4)
            prediction = 2**power*c0**power/4*beta(0.5, 1-3*power/4)
        elif power == 4/3:
            scaled = moment*diffusivity**(1/3)/np.log(1/diffusivity)
            prediction = 2**(1/3)*c0**(4/3)/6
        else:
            scaled = moment*diffusivity**(power/2-1/3)
            prediction = None
        spectrum.append({"power": power, "moment": float(moment),
                         "scaled_moment": float(scaled),
                         "analytic_coefficient_if_available": prediction})
    return {"diffusivity": diffusivity, "quadrature_nodes_per_interval": nodes,
            "half_wall_grid": n, "mean": first, "variance": second-first*first,
            "scaled_mean": first*diffusivity**0.25,
            "candidate_scaled_mean": c0*c0/np.sqrt(np.pi),
            "scaled_second_moment": second*diffusivity**(2/3),
            "scaled_variance": (second-first*first)*diffusivity**(2/3),
            "coefficient_of_variation_squared": second/(first*first)-1,
            "moment_spectrum": spectrum}


def pair_moment_integral(power, dx=0.0015, cutoff=200):
    """Numerical integral plus leading tails, with truncation error unbounded."""
    assert power > 4/3
    c0 = np.pi/2*gamma(0.25)/gamma(0.75)
    negative, err_n = quad(lambda u: pair_integral(u, dx)**power,
                           -30, 0, epsabs=1e-5)
    positive, err_p = quad(lambda u: pair_integral(u, dx)**power,
                           0, cutoff, epsabs=1e-5, points=[0.5, 1, 2, 4, 10, 30])
    positive_tail = (c0/np.sqrt(2))**power*cutoff**(1-3*power/4)/(3*power/4-1)
    negative_tail = (np.pi/2)**power*30**(1-3*power/2)/(3*power/2-1)
    value = negative+positive+negative_tail+positive_tail
    return {"power": power, "dx": dx, "positive_cutoff": cutoff,
            "integral_with_leading_tails": value,
            "candidate_ensemble_moment_coefficient": 2**(power-4/3)*value,
            "quadrature_error_estimate_only": err_n+err_p,
            "error_caveat": "Quadrature error excludes mesh and omitted tail corrections."}


def main():
    c0 = np.pi/2*gamma(0.25)/gamma(0.75)
    quartic = np.pi/18*(gamma(1/6)/gamma(2/3))**2
    mus = [-30, -10, -3, -1, 0, 0.25, 0.5, 1, 2, 4, 10, 30, 100]
    pairs = [{"mu": mu, "integral": pair_integral(mu)} for mu in mus]
    assert abs(pair_integral(0, dx=0.0015)/quartic-1) < 1e-5
    profiles = []
    for d in [1e-3, 1e-5, 1e-7, 1e-9]:
        for mu in [-3.0, 0.0, 1.0, 4.0]:
            offset = 1-mu*(d/2)**(1/3)
            value = periodic_integral(d, offset)*np.sqrt(d)/2
            profiles.append({"diffusivity": d, "mu": mu,
                             "scaled_periodic_integral": value,
                             "pair_prediction": pair_integral(mu)})
    moments = [ensemble(d) for d in [1e-3, 1e-5, 1e-7, 1e-9]]
    refined = ensemble(1e-9, nodes=80, n=32768)
    result = {"quartic_coalescence_constant": quartic,
              "separated_pair_tail_constant": c0/np.sqrt(2),
              "local_pair_curve": pairs, "periodic_pair_matching": profiles,
              "random_offset_moments": moments, "refined_smallest_diffusivity": refined,
              "pair_moment_integrals": [pair_moment_integral(2, dx=0.003, cutoff=100),
                                        pair_moment_integral(2), pair_moment_integral(3)],
              "status": "Candidate disorder asymptotics; uniform estimates and second-moment coefficient remain under independent investigation."}
    Path("results").mkdir(exist_ok=True)
    Path("results/coalescing-zero-checks.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
