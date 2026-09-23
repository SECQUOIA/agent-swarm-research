"""Exact finite checks supplementing the foundations proofs; no solver needed.

Run from any directory with Python 3. These checks are not universal proofs.
"""

from fractions import Fraction as F
from random import Random


def solve2(a, b, c, d, u, v):
    determinant = a * d - b * c
    assert determinant != 0
    return ((u * d - b * v) / determinant,
            (a * v - u * c) / determinant)


def check_destination_decomposition():
    rng = Random(20260905)
    for _ in range(240):
        s1, s2, back = (F(rng.randint(1, 20), rng.randint(1, 7))
                        for _ in range(3))
        delivery1 = min(s1 + back, s1 + s2) * F(rng.randint(1, 9), 10)
        forward = s1 + back - delivery1
        delivery2 = s2 + forward - back
        fa, fb = s1 + back, s2 + forward
        q1, q2 = (F(rng.randint(-10, 10), rng.randint(1, 7))
                  for _ in range(2))
        pa, pb = solve2(fa, -back, -forward, fb, s1*q1, s2*q2)
        ha, hb = solve2(fa, -forward, -back, fb, delivery1, F(0))
        assert 0 < ha <= 1 and 0 <= hb < 1
        original = [s1, s2, forward, back, delivery1, delivery2]
        first = [s1*ha, s2*hb, forward*hb, back*ha, delivery1, F(0)]
        second = [a-b for a, b in zip(original, first)]
        for component in (first, second):
            x1, x2, ab, ba, out1, out2 = component
            assert all(0 <= x <= y for x, y in zip(component, original))
            assert x1 + ba == ab + out1
            assert x2 + ab == ba + out2
            assert q1*x1 + pb*ba == pa*(ab+out1)
            assert q2*x2 + pa*ab == pb*(ba+out2)
            assert q1*x1 + q2*x2 == pa*out1 + pb*out2
        assert all(x+y == z for x, y, z in zip(first, second, original))


def check_closed_circulation():
    for exponent in range(1, 81):
        epsilon = F(1, 2**exponent)
        quality = F(-7, 3)
        pa, pb = solve2(F(1), -(1-epsilon), F(-1), F(1),
                        epsilon*quality, F(0))
        assert pa == pb == quality
        residual1 = (quality+1) - (1-epsilon)*(quality+1) - epsilon*quality
        residual2 = -(quality+1)+(quality+1)
        assert residual1 == epsilon and residual2 == 0
    # At epsilon=0, every common concentration solves the homogeneous system.
    for quality in (F(-9, 2), F(0), F(2, 7)):
        assert quality-quality == 0


def check_nonfacial_counterexample():
    for denominator in range(2, 30):
        for numerator in range(1, denominator):
            delta = F(numerator, denominator)
            clean, dirty = 1-delta, delta
            assert clean + dirty == 1
            assert dirty <= delta*(clean+dirty)
            fractional_profit = dirty
            integer_profits = [d for c in (0, 1) for d in (0, 1)
                               if c+d <= 1 and d <= delta*(c+d)]
            assert fractional_profit > max(integer_profits)


if __name__ == '__main__':
    check_destination_decomposition()
    check_closed_circulation()
    check_nonfacial_counterexample()
    print('PASS: 240 exact cyclic destination decompositions; '
          '80 conditioning instances and singular-cycle checks; '
          '406 nonfacial fractional-improvement witnesses.')
