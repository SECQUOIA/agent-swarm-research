"""Numerical checks of clipping, marginal completion, and hard-term bounds.

The analytic proof remains the certificate. These quadrature checks exercise
clipped/unclipped probabilities and widely separated probability scales.
"""

import math
import random

from scipy.integrate import quad


def parameters(delta):
    scale = max(2.0, math.log(1.0 / delta))
    tau = delta / scale**2
    normalizer = math.log1p(tau) - math.log(tau)
    integral = quad(
        lambda z: -math.expm1(-1.0 / (normalizer * (z + scale**-2))),
        0, 1, epsabs=1e-12, epsrel=1e-11)[0]
    return scale, tau, normalizer, integral


def completion(p, tau, normalizer):
    cutoff = p / normalizer - tau
    mass = p if cutoff <= 0 else (
        cutoff + p / normalizer * math.log((1 + tau) / (cutoff + tau)))
    assert -1e-14 <= mass <= p + 1e-14
    extra = (p - mass) / (1 - mass)
    assert -1e-14 <= extra <= 1 + 1e-14
    return cutoff, extra


def main():
    rng = random.Random(26090491)
    marginal_checks = 0
    term_checks = 0
    for delta in (0.5, 0.1, 1e-3, 1e-8, 1e-20, 1e-80):
        scale, tau, normalizer, integral = parameters(delta)
        lower = math.log(normalizer) / (normalizer * (1 + normalizer / scale**2))
        lower -= (normalizer - 1) / (2 * normalizer**2)
        upper = (1 + math.log(normalizer)) / normalizer
        assert lower - 1e-12 <= integral <= upper + 1e-12

        for p in (0.0, delta / 100, delta, min(0.49, 100 * delta), 0.49):
            cutoff, extra = completion(p, tau, normalizer)

            def integrand(s):
                shifted_time = math.exp(math.log(tau) + normalizer * s)
                density = 1.0 / (normalizer * shifted_time)
                clipped = min(1.0, p * density)
                completed = clipped + extra * (1 - clipped)
                return completed * normalizer * shifted_time

            breakpoint = (math.log(p / normalizer / tau) / normalizer
                          if cutoff > 0 else None)
            points = [breakpoint] if breakpoint is not None and 0 < breakpoint < 1 else None
            mass = quad(integrand, 0, 1, points=points,
                        epsabs=max(1e-100, p * 1e-11), epsrel=1e-10)[0]
            assert abs(mass - p) <= max(1e-95, p * 1e-8), (delta, p, mass)
            marginal_checks += 1

        for _ in range(20):
            u = math.exp(rng.uniform(math.log(delta), math.log(0.5)))
            ps = [min(0.49, u * 10**rng.uniform(-2, 2))
                  for _ in range(rng.randrange(1, 16))]
            completions = [completion(p, tau, normalizer) for p in ps]
            points = sorted({cutoff / u for cutoff, _ in completions if 0 < cutoff < u})

            def union(z):
                probability_none = 1.0
                for p, (_, extra) in zip(ps, completions):
                    clipped = min(1.0, p / (normalizer * (u * z + tau)))
                    completed = clipped + extra * (1 - clipped)
                    probability_none *= 1 - completed
                return 1 - probability_none

            normalized_deficiency = quad(union, 0, 1, points=points,
                                         epsabs=1e-11, epsrel=1e-10)[0]
            normalized_gap = min(1.0, sum(ps) / u)
            assert normalized_deficiency + 1e-9 >= integral * normalized_gap, (
                delta, u, ps, normalized_deficiency, integral * normalized_gap)
            term_checks += 1

    print(f"Passed {marginal_checks} marginal-completion quadratures and "
          f"{term_checks} hard-term deficiency checks.")
    print("Probability floors ranged from 1/2 to 1e-80; integral bounds were also checked.")


if __name__ == "__main__":
    main()
