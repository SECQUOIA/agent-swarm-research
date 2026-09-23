#!/usr/bin/env python3
"""Numerical cross-checks, not proof certificates, for the standard-path theorems."""
from itertools import permutations
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

KAPPA = np.log(4)-np.sqrt(2)*np.arctanh(1/np.sqrt(2))


def velocity(s):
    if s > 350:
        return 1.0
    z = np.exp(s)
    t = np.hypot(1, z)
    return np.sqrt((z/t)*(z/(1+t)))


def H(s):
    if s > 35:
        return s+KAPPA
    if s < -30:
        return np.exp(s)/np.sqrt(2)
    return quad(velocity, -40, s, epsabs=1e-11)[0]


def gamma(alpha):
    masses = np.r_[0, np.cumsum(alpha)]
    d = np.diff(np.sqrt(masses))
    return np.sqrt(np.sum(d*d/alpha))


def main():
    rng = np.random.default_rng(13457)
    largest_violation = 0.0
    for _ in range(80):
        alpha = np.exp(rng.uniform(-3, 3, 5))
        h = np.sort(rng.random(5))[::-1]
        masses = np.r_[0, np.cumsum(alpha)]
        d = np.diff(np.sqrt(masses))
        largest_violation = max(largest_violation,
            np.linalg.norm(np.sqrt(alpha)*h)-d@h)
        values = [gamma(np.array(p)) for p in permutations(alpha)]
        assert gamma(np.sort(alpha)) >= max(values)-1e-12
        assert gamma(np.sort(alpha)[::-1]) <= min(values)+1e-12
    assert largest_violation <= 1e-12
    print('80 random weighted-prefix and exhaustive 5-channel order checks passed.')
    alpha = np.array([1., 3., 2., 7.])
    masses = np.r_[0, np.cumsum(alpha)]
    c = 1/(np.sqrt(masses[1:])+np.sqrt(masses[:-1]))
    target = gamma(alpha)
    ratios = []
    for M in [30., 100., 300., 1000.]:
        u = np.array([brentq(lambda s: H(s)-M*t, -30, M*t+3) for t in c])
        breaks = sorted(set([-float(u[0])-35, *(-u), 0.]))
        def speed(s):
            return np.linalg.norm(np.sqrt(alpha)*np.array([velocity(s+t) for t in u]))
        arc = sum(quad(speed, a, b, epsabs=1e-8)[0] for a,b in zip(breaks,breaks[1:]))
        ratio = arc/(M*target)
        assert 1 <= ratio <= target+1e-9
        ratios.append(ratio)
    assert abs(ratios[-1]-target) < abs(ratios[0]-target)
    print('Weighted sharpness ratios:', ratios, 'target:', target)
    for z in np.exp(np.linspace(-20,20,401)):
        q = z/(1+np.hypot(1,z))
        # Stable objective error identity avoids subtracting q from one.
        ze = 2*z/(1+z+np.hypot(1,z))
        v2 = (z/np.hypot(1,z))*(z/(1+np.hypot(1,z)))
        assert (2-np.sqrt(2))*min(z,1) <= ze*(1+1e-13)
        assert ze <= min(z,1)*(1+1e-13)
        assert (1-1/np.sqrt(2))*min(z*z,1) <= v2*(1+1e-13)
        assert v2 <= min(z*z,1)*(1+1e-13)
    print('401 scalar error/speed checks passed.')


if __name__ == '__main__':
    main()
