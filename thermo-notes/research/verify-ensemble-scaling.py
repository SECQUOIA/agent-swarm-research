"""Deterministic quadrature checks for scouting-ensembles.md; no simulation data."""
from math import sqrt
from scipy.integrate import quad
from scipy.special import expit, ndtr
from scipy.stats import norm


def tv(r, k, b):
    scale = 1 / sqrt(1 + k)
    means = [(-r + b) / (1 + k), (r + b) / (1 + k)]
    weight = expit(2 * r * b / (1 + k))

    def delta(x):
        p = (norm.pdf(x + r) + norm.pdf(x - r)) / 2
        q = (1-weight)*norm.pdf(x, means[0], scale) + weight*norm.pdf(x, means[1], scale)
        return abs(p-q) / 2

    # Include all centers and their tails to prevent quadrature from skipping a peak.
    knots = sorted(set(x + dx for x in [-r, r, *means] for dx in [-12, -6, 0, 6, 12]))
    return sum(quad(delta, a, b, epsabs=2e-10, limit=150)[0]
               for a, b in zip(knots[:-1], knots[1:]))


if __name__ == '__main__':
    print('Exact Gaussian mixture; r=m/s, a=k*r, all values deterministic')
    print('a    r      balanced_TV    one_phase_TV   predicted_best_limit')
    for a in [.5, 1., 1.5, 3.]:
        for r in [10., 100., 1000.]:
            k = a/r
            balanced = tv(r,k,0)
            one_phase = tv(r,k,k*r)
            target = min(2*ndtr(a/2)-1,.5)
            print(f'{a:3.1f} {r:6.0f} {balanced:14.9f} {one_phase:14.9f} {target:20.9f}')
        assert abs(tv(1000.,a/1000.,0)-(2*ndtr(a/2)-1)) < .002
        assert abs(tv(1000.,a/1000.,a)-.5) < .002
