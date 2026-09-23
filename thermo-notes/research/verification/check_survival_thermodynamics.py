"""Finite-network checks for survival-conditioned force integration.

Conductances, including killing conductances, remain fixed as well energies
vary. Cycle integrals are endpoint-force constructions, not trajectory work.
"""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad
from scipy.linalg import eigh


def measures(energies, matrix, beta=1.0):
    w = np.exp(-beta * energies)
    values, vectors = eigh(matrix, np.diag(w))
    h = vectors[:, 0]
    if h.sum() < 0:
        vectors[:, 0] *= -1
        h = vectors[:, 0]
    assert h.min() > 0
    pi = w / w.sum()
    nu = w * h / np.dot(w, h)
    eta = w * h * h
    return values, vectors, pi, nu, eta


def response(energies, matrix, direction, beta=1.0):
    vals, vecs, pi, nu, eta = measures(energies, matrix, beta)
    w = np.exp(-beta * energies)
    h = vecs[:, 0]
    amplitudes = vecs.T @ (w * direction * h)
    dh = beta * amplitudes[0] * h / 2.0
    dh -= beta * vals[0] * (vecs[:, 1:] @ (amplitudes[1:] / (vals[1:] - vals[0])))
    log_nu = -beta * direction + dh / h
    log_eta = -beta * direction + 2.0 * dh / h
    dnu = nu * (log_nu - np.dot(nu, log_nu))
    deta = eta * (log_eta - np.dot(eta, log_eta))
    variance = np.dot(eta, direction ** 2) - np.dot(eta, direction) ** 2
    integrated_covariance = np.sum(amplitudes[1:] ** 2 / (vals[1:] - vals[0]))
    curvature = -beta * (variance + 2.0 * vals[0] * integrated_covariance)
    return dnu, deta, curvature


def line_integral(matrix, side, which):
    corners = [np.array([0., 0., 0.]), np.array([side, 0., 0.]),
               np.array([side, side, 0.]), np.array([0., side, 0.]),
               np.array([0., 0., 0.])]
    total = 0.0
    for start, end in zip(corners[:-1], corners[1:]):
        change = end - start
        def integrand(t):
            _, _, pi, nu, eta = measures(start + t * change, matrix)
            if which == "bound":
                b = np.sqrt(pi * eta).sum()
                return (1.0 - b) * np.ptp(change)
            law = {"pi": pi, "nu": nu, "eta": eta}[which]
            return np.dot(law, change)
        total += quad(integrand, 0.0, 1.0, epsabs=2e-13, epsrel=1e-11)[0]
    return total


def main():
    reflect = np.array([[1., -1., 0.], [-1., 2., -1.], [0., -1., 1.]])
    kill = np.diag([56.0 / 55.0, 0., 0.])
    matrix = reflect + kill
    energies = np.zeros(3)
    vals, _, pi, nu, eta = measures(energies, matrix)
    jac = np.column_stack([response(energies, matrix, d)[0] for d in np.eye(3)])
    curl = jac[0, 1] - jac[1, 0]
    assert np.isclose(vals[0], 0.2, atol=1e-14)
    assert np.allclose(nu, np.array([11., 20., 25.]) / 56.)
    assert np.allclose(eta, np.array([121., 400., 625.]) / 1146.)
    assert np.isclose(curl, -275.0 / 64176.0, atol=1e-14)

    rng = np.random.default_rng(20260907)
    worst_response_error = 0.0
    for _ in range(150):
        n = int(rng.integers(3, 10))
        conductance = rng.uniform(0.2, 2.0, size=(n, n))
        conductance = (conductance + conductance.T) / 2.0
        np.fill_diagonal(conductance, 0.)
        a0 = np.diag(conductance.sum(axis=1)) - conductance
        killing = rng.uniform(0.0, 0.7, n)
        a = a0 + np.diag(killing)
        e = rng.normal(scale=0.5, size=n)
        f = rng.normal(size=n)
        lam, vec, p, q, interior = measures(e, a)
        dq, di, formula = response(e, a, f)
        assert np.isclose(np.dot(di, f), formula, rtol=1e-10, atol=1e-11)
        step = 1e-5
        plus = measures(e + step * f, a)
        minus = measures(e - step * f, a)
        numerical = (plus[3] - minus[3]) / (2.0 * step)
        worst_response_error = max(worst_response_error, float(np.max(np.abs(dq - numerical))))
        assert np.allclose(dq, numerical, atol=1e-8, rtol=1e-6)
        grad_potential = (np.log(plus[0][0]) - np.log(minus[0][0])) / (2.0 * step)
        assert np.isclose(grad_potential, np.dot(interior, f), atol=2e-8, rtol=1e-6)
        b = np.sqrt(p * interior).sum()
        midpoint = (p + interior) / 2.0
        assert np.sum(np.abs(q - midpoint)) / 2.0 <= 1.0 - b + 1e-14
        w = np.exp(-e)
        h = vec[:, 0] / np.dot(p, vec[:, 0])
        var_h = np.dot(p, (h - 1.0) ** 2)
        gap = eigh(a0, np.diag(w), eigvals_only=True)[1]
        rates = killing / w
        denominator = gap + rates.min() - lam[0]
        if denominator > 0:
            var_r = np.dot(p, (rates - np.dot(p, rates)) ** 2)
            assert var_h <= var_r / denominator ** 2 + 1e-12

    cycles = []
    for eps in [1., 0.3, 0.1, 0.03, 0.01, 0.003]:
        a = reflect + eps * kill
        cycle = {"killing_scale": eps, "side": 0.5}
        for name in ["pi", "nu", "eta", "bound"]:
            cycle[name] = line_integral(a, 0.5, name)
        assert abs(cycle["pi"]) < 1e-11
        assert abs(cycle["eta"]) < 1e-11
        assert abs(cycle["nu"]) <= cycle["bound"] + 1e-12
        cycle["endpoint_integral_over_epsilon_squared"] = cycle["nu"] / eps ** 2
        cycles.append(cycle)
    result = {"random_cases": 150, "max_endpoint_response_fd_error": worst_response_error,
              "exact_example_curl": curl, "cycles": cycles}
    Path(__file__).with_name("survival-thermodynamics-results.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
