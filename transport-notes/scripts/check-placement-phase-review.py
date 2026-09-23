"""Independent unconstrained-mass discretization of the mobility phase diagram.

The optimization starts from zero mobility and uses no analytic profile as an
initial guess. The exact profiles are evaluated only for the final comparison.
"""
import numpy as np
from scipy.linalg import solve_banded
from scipy.optimize import brentq, minimize

L = 6.0
N = 1200
dx = 2 * L / N
x = -L + (np.arange(N) + 0.5) * dx
edge = -L + (np.arange(N - 1) + 1) * dx
potential = 1 + x**2
eta_first = 8 / (3 * np.sqrt(3))
eta_second = 3 / np.sqrt(2)

for eta in [1.4, 1.8, 3.0]:
    def objective(d):
        diagonal = potential.copy()
        diagonal[:-1] += d / dx**2
        diagonal[1:] += d / dx**2
        band = np.zeros((3, N))
        band[1] = diagonal
        band[0, 1:] = -d / dx**2
        band[2, :-1] = -d / dx**2
        h = solve_banded((1, 1), band, np.ones(N), check_finite=False)
        cost = dx * np.sum(d) + eta**2 * (
            dx * np.sum(h) + np.pi - 2 * np.arctan(L)
        )
        gradient = dx * (1 - eta**2 * (np.diff(h) / dx) ** 2)
        return cost, gradient

    result = minimize(
        objective,
        np.zeros(N - 1),
        method="L-BFGS-B",
        jac=True,
        bounds=[(0, None)] * (N - 1),
        options={"ftol": 1e-14, "gtol": 1e-9, "maxiter": 2000, "maxcor": 20},
    )
    distance = np.abs(edge)
    exact = np.zeros_like(distance)
    if eta <= eta_first:
        mass = 0.0
        cost = eta**2 * np.pi
    elif eta < eta_second:
        S = brentq(
            lambda value: value + value**3 / 4 - eta,
            2 / np.sqrt(3), np.sqrt(2),
        )
        width = np.sqrt(3 * S**2 - 4)
        left = (S - width) / 2
        right = (S + width) / 2
        active = (distance > left) & (distance < right)
        exact[active] = (distance[active] - left)**2 * (distance[active] - right)**2 / 4
        mass = width**5 / 60
        inverse_integral = (
            np.pi - 2 * (np.arctan(right) - np.arctan(left))
            + 2 * width * S / eta
        )
        cost = mass + eta**2 * inverse_integral
    else:
        R = brentq(
            lambda value: (1 + value**2) * (6 + value**2) / (8 * value) - eta,
            np.sqrt(2), 20,
        )
        active = distance < R
        z = distance[active]
        exact[active] = z * (R - z)**2 * (2 * R * z + R**2 - 2) / (8 * R)
        mass = R**3 * (9 * R**2 - 10) / 240
        inverse_integral = (
            np.pi - 2 * np.arctan(R) + 2 * R / (1 + R**2) + R**2 / eta
        )
        cost = mass + eta**2 * inverse_integral

    print({
        "eta": eta,
        "success": bool(result.success),
        "iterations": result.nit,
        "relative_cost_error": (result.fun - cost) / cost,
        "numerical_mass": dx * np.sum(result.x),
        "exact_mass": mass,
        "max_profile_error": np.max(np.abs(result.x - exact)),
    })
