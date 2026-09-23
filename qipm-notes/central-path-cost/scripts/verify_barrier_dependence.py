#!/usr/bin/env python3
"""Numerical checks of the new coupled estimates; these are not proofs.

Centers are independently solved by nested scalar bisection, rather than
integrating the claimed velocity formulas. Finite differences of those
centers are compared with the implicit Hessian equation.
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


def center(z, lam, c):
    def coordinates(a):
        lo, hi = np.zeros_like(z), np.ones_like(z)
        for _ in range(70):
            mid = (lo+hi)/2
            value = 2*mid/(1-mid*mid)+a*mid
            lo = np.where(value < z, mid, lo)
            hi = np.where(value >= z, mid, hi)
        return (lo+hi)/2

    a = brentq(lambda a: a-2*lam/(c-np.dot(coordinates(a), coordinates(a))),
               0, .5, xtol=1e-14)
    return coordinates(a)


def quantities(x, lam, c):
    a = 2*lam/(c-x@x)
    b = 2/(1-x*x)
    d = 2*(1+x*x)/(1-x*x)**2
    hessian = np.diag(d+a)+(a*a/lam)*np.outer(x, x)
    grad = x*(b+a)
    tangent = np.linalg.solve(hessian, grad)
    aprime = (a*a/lam)*(x@tangent)
    positive = x > 1e-14
    theta = d[positive]*tangent[positive]/(b[positive]*x[positive])
    relative = hessian/np.sqrt(d[:, None]*d[None, :])
    return a, d, hessian, grad, tangent, aprime, theta, relative


def rho(x):
    v = np.sqrt(2)*x/np.sqrt(1+x*x)
    return 2*np.arctanh(v)-np.sqrt(2)*np.arctanh(v/np.sqrt(2))


def main():
    rng = np.random.default_rng(813790)
    derivative_error = 0.
    ranges = [np.inf, -np.inf, np.inf, -np.inf]
    for r in [2, 5, 16, 64]:
        for lam in [1., 3., 100.]:
            for _ in range(8):
                c = r+4*lam+rng.uniform(0, 10)
                z = np.exp(rng.uniform(-7, 7, r))
                # Include inactive channels in half of the cases.
                if _ % 2:
                    z[r//2:] = 0.
                x = center(z, lam, c)
                a, d, h, g, tangent, ap, theta, rel = quantities(x, lam, c)
                assert np.linalg.norm(g-z)/max(1, np.linalg.norm(z)) < 1e-11
                eigenvalues = np.linalg.eigvalsh(rel)
                assert eigenvalues[0] >= 1-1e-12
                assert eigenvalues[-1] <= 11/8+1e-12
                assert -1e-12 <= ap <= 1/4+1e-12
                assert theta.min() >= 7/10-1e-12 and theta.max() <= 5/4+1e-12
                assert g@tangent <= r+1e-10
                step = 2e-5
                fd = (center(z*np.exp(step), lam, c)-center(z*np.exp(-step), lam, c))/(2*step)
                err = np.linalg.norm(fd-tangent)/max(1e-10, np.linalg.norm(tangent))
                derivative_error = max(derivative_error, err)
                assert err < 2e-7
                ranges = [min(ranges[0], eigenvalues[0]), max(ranges[1], eigenvalues[-1]),
                          min(ranges[2], theta.min()), max(ranges[3], theta.max())]
    print('96 independently solved radial centers, metric/parameter/speed checks passed.')
    print('Maximum relative finite-difference tangent error:', derivative_error)
    print('Observed metric and logarithmic-speed ranges:', ranges)

    br = np.sqrt(11/8)*25/14
    for r, lam in [(2, 1.), (5, 3.), (10, 100.)]:
        c, weights = r+4*lam, np.exp(np.linspace(4, -4, r))
        def speed(s):
            q = quantities(center(np.exp(s)*weights, lam, c), lam, c)
            return np.sqrt(q[3]@q[4])
        arc = quad(speed, -4, 4, epsabs=1e-8)[0]
        delta = rho(center(np.exp(4)*weights, lam, c))-rho(center(np.exp(-4)*weights, lam, c))
        gamma = np.linalg.norm(np.diff(np.sqrt(np.arange(r+1))))
        assert arc <= br*gamma*np.linalg.norm(delta)
        print(f'Radial arc check r={r}: arc/rho-chord={arc/np.linalg.norm(delta):.9f}, bound={br*gamma:.9f}')

    k = np.log(2.)
    boundary = brentq(lambda a: 2*a-k*(2-np.exp(-a)), .1, 1.)
    def b(a):
        return np.log(4*a/(k*(2-np.exp(-a))**2))
    def stationarity(a):
        return a*(1/a-2*np.exp(-a)/(2-np.exp(-a)))-b(a)
    maximum = brentq(stationarity, boundary, 3., xtol=1e-14)
    assert .65011 < maximum < .65012
    constant = 1+b(maximum)/maximum
    assert 1.83185 < constant < 1.83186
    print('Relaxed-envelope maximizer and value (numerical only):', maximum, constant)


if __name__ == '__main__':
    main()
