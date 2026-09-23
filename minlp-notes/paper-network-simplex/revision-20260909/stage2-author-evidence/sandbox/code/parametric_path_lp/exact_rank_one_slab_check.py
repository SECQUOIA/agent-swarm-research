"""Independent rational checks of the Klee--Minty rank-one identity."""
from fractions import Fraction as F
from itertools import product
from random import Random

from exact_shadow_check import vertex, eliminate


def coefficients(n, eps):
    return [(1-eps) * eps ** (2*(n-1-i)-1) for i in range(n-1)] + [F(0)]


def identity(x, eps):
    n = len(x)
    c = coefficients(n, eps)
    linear = x[-1] - sum(a*v for a, v in zip(c, x))
    previous = F(0)
    total = F(0)
    for j, value in enumerate(x):
        total += eps ** (2*(n-1-j)) * (value-eps*previous) * (1-eps*previous-value)
        previous = value
    assert linear - x[-1]**2 == total
    assert total >= 0
    return total


def main():
    rng = Random(961275)
    points = 0
    for n in range(1, 11):
        eps = F(1, 4)
        c = coefficients(n, eps)
        seen = set()
        for bits in product((0, 1), repeat=n):
            x = vertex(bits, eps)
            assert identity(x, eps) == 0
            t = x[-1]
            assert t not in seen
            seen.add(t)
            support, effective = eliminate(c, 2*t-1, eps)
            assert all(a != 0 and (a > 0) == bool(bit) for a, bit in zip(effective, bits))
            assert support == t*t
            points += 1
        for _ in range(20):
            x = []
            previous = F(0)
            for _ in range(n):
                alpha = F(rng.randint(1, 9), 10)
                previous = eps*previous + alpha*(1-2*eps*previous)
                x.append(previous)
            assert identity(x, eps) > 0
            points += 1
    instances = targets = padded_targets = padded_vertices = 0
    for n in range(1, 8):
        for _ in range(4):
            weights = [rng.randint(1, 10) for _ in range(n)]
            W = sum(weights)
            eps = F(1, 8*W)
            vertex_sums, subset_sums = [], set()
            for bits in product((0, 1), repeat=n):
                x = vertex(bits, eps)
                assert identity(x, eps) == 0
                exact = sum(w*b for w, b in zip(weights, bits))
                perturbed = sum(w*v for w, v in zip(weights, x))
                assert abs(perturbed-exact) <= F(1, 8)
                vertex_sums.append(perturbed)
                subset_sums.add(exact)
            for B in range(W+2):
                yes = any(abs(value-B) <= F(1, 4) for value in vertex_sums)
                assert yes == (B in subset_sums)
                targets += 1
            padding = 0
            while 4 ** (padding + 1) < 8 * W:
                padding += 1
            dimension = n + (n-1)*padding
            positions = [i*(padding+1) for i in range(n)]
            padded_sums = []
            for bits in product((0, 1), repeat=n):
                extended = [0]*dimension
                for position, bit in zip(positions, bits):
                    extended[position] = bit
                x = vertex(extended, F(1, 4))
                assert identity(x, F(1, 4)) == 0
                assert all(x[j] <= F(1, 2) for j in range(dimension) if j not in positions)
                sampled = [x[j] for j in positions]
                integer_sum = sum(w*b for w, b in zip(weights, bits))
                perturbed = sum(w*v for w, v in zip(weights, sampled))
                assert abs(perturbed-integer_sum) <= F(1, 8)
                padded_sums.append(perturbed)
                padded_vertices += 1
            for B in range(W+2):
                assert any(abs(value-B) <= F(1, 4) for value in padded_sums) == (B in subset_sums)
                padded_targets += 1
            # Flipping any padding coordinate to its upper branch violates
            # its singleton bound, independently of the remaining choices.
            for j in range(dimension):
                if j not in positions:
                    extended = [0]*dimension
                    extended[j] = 1
                    assert vertex(extended, F(1, 4))[j] >= F(3, 4)
            instances += 1
    print(f'PASS: {points} exact identity/positivity/tangent checks through dimension10.')
    print(f'PASS: {targets} subset-sum targets from {instances} weighted instances through dimension7.')
    print(f'PASS: {padded_vertices} padded vertex identities and {padded_targets} fixed-coefficient slab targets.')


if __name__ == '__main__':
    main()
