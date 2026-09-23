"""Exact small-polytope check of monotone LP-oracle vertex recovery.

The LP oracle enumerates vertices for these diagnostics only. The theorem
uses polynomial-time rational LP and does not enumerate them.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial
from random import Random


def vertices(weights, total, lower, upper):
    found = set()
    n = len(weights)
    for free in range(n):
        others = [i for i in range(n) if i != free]
        for bits in product((0, 1), repeat=n-1):
            beta = [F(0)] * n
            for i, bit in zip(others, bits):
                beta[i] = upper[i] if bit else lower[i]
            beta[free] = (total-sum(weights[i]*beta[i] for i in others))/weights[free]
            if lower[free] <= beta[free] <= upper[free]:
                found.add(tuple(beta))
    return sorted(found)


def h(q, beta, offsets):
    return sum(be*(q+d)*abs(q+d) for be, d in zip(beta, offsets))


def root_bracket(beta, offsets, width):
    left, right = F(-max(offsets)-1), F(-min(offsets)+1)
    while right-left >= width:
        mid = (left+right)/2
        v = h(mid, beta, offsets)
        if v == 0:
            return mid, mid
        if v < 0:
            left = mid
        else:
            right = mid
    return left, right


def run():
    rng = Random(514762)
    total_vertices = iterations = 0
    for case in range(32):
        n = 3+case % 2
        weights = [F(rng.randrange(1, 4)) for _ in range(n)]
        lower = [F(1)] * n
        upper = [F(rng.randrange(3, 7)) for _ in range(n)]
        midpoint = [(a+b)/2 for a, b in zip(lower, upper)]
        total = sum(a*b for a, b in zip(weights, midpoint))
        verts = vertices(weights, total, lower, upper)
        assert verts
        offsets = [F(0)] + [F(rng.randrange(-3, 4)) for _ in range(n-1)]
        # Clear the single equality's denominator globally. Box rows and
        # both signs of the equality fit this integer entry bound.
        den = total.denominator
        c = max([abs(total.numerator)] + [int(den*v) for v in weights+upper])
        delta = factorial(n)*c**n
        height = max(1, 2*n*delta*(1+max(map(abs, offsets)))**2)
        separation = F(1, 64*int(height)**7)
        left, right = F(-max(offsets)-1), F(-min(offsets)+1)
        while right-left >= separation/2:
            mid = (left+right)/2
            minimum = min(h(mid, beta, offsets) for beta in verts)
            if minimum <= 0:
                left = mid
            else:
                right = mid
            iterations += 1
        winner = min(verts, key=lambda beta: h(left, beta, offsets))
        assert h(left, winner, offsets) <= 0
        win_lo, win_hi = root_bracket(winner, offsets, separation/8)
        for beta in verts:
            lo, hi = root_bracket(beta, offsets, separation/8)
            # A provably greater isolated root would violate exact optimum.
            # Overlapping isolations imply identical roots by separation.
            assert lo <= win_hi
            # Verify the common Cramer denominator and coefficient bounds.
            from math import lcm
            common = lcm(*(x.denominator for x in beta))
            nums = [int(x*common) for x in beta]
            assert common <= delta and max(map(abs, nums)) <= delta
            for signs in product((-1, 1), repeat=n):
                coeff = [sum(s*v for s, v in zip(signs, nums)),
                         sum(2*s*v*d for s, v, d in zip(signs, nums, offsets)),
                         sum(s*v*d*d for s, v, d in zip(signs, nums, offsets))]
                assert max(map(abs, coeff)) <= height
        total_vertices += len(verts)
    print(f'PASS: 32 correlated polytopes, {total_vertices} vertices, '
          f'{iterations} exact threshold bisections; all recovered vertices optimal')


if __name__ == '__main__':
    run()
