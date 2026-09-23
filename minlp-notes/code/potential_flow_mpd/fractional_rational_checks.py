"""Positive rational surrogate evidence for the fractional additive candidate."""
import math

import numpy as np
from scipy.special import roots_legendre


def surrogate(bits):
    L = 4*(bits+8)
    n = math.ceil((L+bits+math.ceil(math.log2(64*L)))/2)
    u, w = roots_legendre(n)
    u, w = 1.5+u/2, w/2
    k = np.arange(-L, L)
    s = (np.exp2(k[:, None])*u).ravel()
    a = (np.exp2(k[:, None]/4)*w*u**(-3/4)).ravel()
    # Every floating-point a,s is itself a positive rational number. These
    # small precision experiments assess the approximation and derivative;
    # a certified construction must use the stated interval-rounding budget.
    normalizer = np.sum(a/(1+s))
    a /= normalizer
    return a, s, L, n


def run():
    worst_ratio = 0.
    for bits in (4, 8, 12, 16):
        a, s, L, n = surrogate(bits)
        assert np.all(a > 0) and np.all(s > 0)
        ts = np.concatenate(([0.], np.geomspace(2.**(-L), 1., 450)))
        values = np.array([np.sum(a*t/(t+s)) for t in ts])
        error = np.max(np.abs(values-ts**.25))
        zeta = 4*2.**(-L/4)+(4/3)*2.**(-3*L/4)+16*L*2.**(L-2*n)
        assert error < 24*zeta, (bits, error, zeta)
        assert np.all(np.diff(values) >= 0)
        # f(x)=x R(x²) has a nonnegative explicit derivative and a strictly
        # increasing sampled profile across the fractional singularity.
        xs = np.linspace(-1, 1, 503)
        law = np.array([np.sum(a*x**3/(x*x+s)) for x in xs])
        derivative = np.array([np.sum(a*x*x*(x*x+3*s)/(x*x+s)**2) for x in xs])
        exact = xs*np.sqrt(np.abs(xs))
        assert np.min(derivative) >= 0
        assert np.all(np.diff(law) > 0)
        assert np.max(np.abs(law-exact)) <= error+2e-14
        ratio = error/(24*zeta)
        worst_ratio = max(worst_ratio, ratio)
        print(f'precision={bits}: {len(a)} terms, quadrature bound={zeta:.3g}, observed normalized error={error:.3g}')
    rng = np.random.default_rng(590528)
    # Independent stress of the global power-law monotonicity constant,
    # including opposite signs and nearly coincident coordinates.
    for _ in range(10000):
        x, y = rng.uniform(-100, 100, 2)
        lhs = (x*math.sqrt(abs(x))-y*math.sqrt(abs(y)))*(x-y)
        assert lhs+1e-10 >= .5*abs(x-y)**2.5
    print(f'4 positive rational surrogates and 10000 monotonicity pairs passed; max error/bound ratio {worst_ratio:.3g}.')


if __name__ == '__main__':
    run()
