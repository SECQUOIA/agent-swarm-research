"""Numerical diagnostics for Section 3; these checks are not mathematical proofs.

Run with python scripts/verify_classical.py.
"""
from __future__ import annotations

import math
import numpy as np
from numpy.polynomial.chebyshev import chebval


def residual(lam: np.ndarray, kappa: float, eta: float) -> np.ndarray:
    if kappa == 1:
        return np.zeros_like(lam)
    a = 1 / kappa
    m = math.ceil(math.log(2 / eta) / math.log((math.sqrt(kappa) + 1) / (math.sqrt(kappa) - 1)))
    coef = np.zeros(m + 1)
    coef[m] = 1
    return chebval((1 + a - 2 * lam) / (1 - a), coef) / chebval((1 + a) / (1 - a), coef)


def main() -> None:
    rng = np.random.default_rng(29137)
    for kappa in (1, 1.01, 2, 10, 100):
        for eta in (0.125, 0.01, 0.0001):
            lam = np.linspace(1 / kappa, 1, 10001)
            r = residual(lam, kappa, eta)
            assert np.max(np.abs(r)) <= eta * (1 + 1e-9)
            pinv = (1 - r) / lam
            assert np.all(pinv >= (1 - eta) / lam - 1e-10)
            assert np.all(pinv <= (1 + eta) / lam + 1e-10)

    for n in (2, 5, 9):
        z = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        unitary, _ = np.linalg.qr(z)
        vals = np.linspace(1, 30, n)
        pmat = (unitary * vals) @ unitary.conj().T
        b = rng.normal(size=n) + 1j * rng.normal(size=n)
        b[0] = 0
        bnorm2 = np.vdot(b, b).real
        pb = pmat @ b
        support = np.abs(b) > 0
        probs = np.abs(b[support]) ** 2 / bnorm2
        outcomes = bnorm2 * pb[support] / b[support]
        mean = np.dot(probs, outcomes)
        second = np.dot(probs, np.abs(outcomes) ** 2)
        q = np.vdot(b, pb).real
        assert np.allclose(mean, q)
        assert second <= bnorm2 * np.vdot(pb, pb).real * (1 + 1e-12)
        assert second / q**2 <= (1 + 30) ** 2 / (4 * 30) * (1 + 1e-12)
        tau = 0.01
        coordinate_error = tau * np.abs(b[support]) * np.exp(1j * rng.uniform(0, 2*np.pi, support.sum()))
        perturbed = bnorm2 * (pb[support] + coordinate_error) / b[support]
        assert np.max(np.abs(perturbed - outcomes)) <= tau * bnorm2 * (1 + 1e-11)

    for beta in (1, 2, 100):
        b = np.sqrt(np.array([beta, 1]) / (1 + beta))
        pb = np.array([1, beta]) * b
        ratio = np.vdot(pb, pb).real / np.vdot(b, pb).real**2
        assert np.allclose(ratio, (1 + beta)**2 / (4 * beta))

    # Enumerate a whole raw rejection trial, including a zero vector coordinate.
    pmat = np.array([[1, 0.3j, 0], [-0.3j, 2, 0.2], [0, 0.2, 1.5]], complex)
    v = np.array([1, 0, -1j])
    y = pmat @ v
    radius = 3
    beta = np.linalg.norm(pmat, 2)
    s = np.sum(np.abs(pmat * v)**2, axis=1)
    raw = np.zeros(3)
    for j in range(3):
        c2 = np.linalg.norm(pmat[:, j])**2
        for i in range(3):
            if s[i] > 0:
                raw[i] += (abs(v[j])**2 / np.linalg.norm(v)**2 * c2 / beta**2
                           * abs(pmat[i, j])**2 / c2 * abs(y[i])**2 / (radius * s[i]))
    expected = np.abs(y)**2 / (radius * beta**2 * np.linalg.norm(v)**2)
    assert np.allclose(raw, expected)
    assert np.allclose(raw / raw.sum(), np.abs(y)**2 / np.linalg.norm(y)**2)

    # Median of group means is Lipschitz in deterministic sample perturbations.
    samples = rng.normal(size=(9, 31))
    noise = rng.uniform(-0.03, 0.03, size=samples.shape)
    shift = abs(np.median((samples + noise).mean(axis=1)) - np.median(samples.mean(axis=1)))
    assert shift <= 0.03
    print("PASS: residual, complex/support moments, sharp variance witness, rejection law, and arithmetic transfer")


if __name__ == "__main__":
    main()
