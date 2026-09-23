"""Exact directed-edge checks of the small-price local-optimum refinement."""
from fractions import Fraction as F
from itertools import product

from exact_shadow_check import vertex
from exact_rank_one_slab_check import identity


def main():
    vertices = edges = 0
    for n in range(2, 11):
        eps, delta = F(1, 4), F(1, 4**n)
        points = {bits: vertex(bits, eps) for bits in product((0, 1), repeat=n)}
        values = set()
        for bits, x in points.items():
            t = x[-1]
            assert 4**(n-1) % t.denominator == 0
            values.add(delta*t)
            for j in range(n):
                neighbor = list(bits)
                neighbor[j] ^= 1
                y = points[tuple(neighbor)]
                difference = y[-1]-t
                assert difference != 0 and abs(difference) >= F(1, 4**(n-1))
                assert -difference*difference+delta*difference < 0
                fraction = F(1, 3)
                middle = [(1-fraction)*a+fraction*b for a, b in zip(x, y)]
                assert identity(middle, eps) == fraction*(1-fraction)*difference*difference
                edges += 1
            vertices += 1
        assert len(values) == 2**n and max(values) == delta
        assert sum(x[-1] == 1 for x in points.values()) == 1
    print(f'PASS: {vertices} distinct local-optimum values and {edges} exact negative directed-edge derivatives.')


if __name__ == '__main__':
    main()
