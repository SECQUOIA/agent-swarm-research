"""Exact arithmetic checks for the constant-data circuit reduction.

These checks cover gate arithmetic and normalization, not physical network
composition; the latter requires the separate original-network checker.
"""

from fractions import Fraction
from random import Random


def multiply(c, length, x):
    value = Fraction(0)
    for k in range(length):
        value = (value + ((c >> k) & 1) * x) / 2
        assert 0 <= value <= 2
    assert value == Fraction(c, 1 << length) * x
    return value


def main():
    rng = Random(67)
    count = 0
    for length in range(1, 25):
        for _ in range(40):
            multiply(rng.randrange(1 << length), length,
                     Fraction(rng.randrange(201), 100))
            count += 1
    for _ in range(500):
        coeffs = [rng.randrange(-1000, 1001) for _ in range(6)]
        rhs = rng.randrange(-1000, 1001)
        values = [Fraction(rng.randrange(201), 100) for _ in coeffs]
        size = sum(map(abs, coeffs)) + abs(rhs)
        length = size.bit_length()
        scale = 1 << length
        assert scale > size
        left = Fraction(0)
        right = Fraction(0)
        for c, x in zip(coeffs, values):
            term = multiply(abs(c), length, x)
            if c >= 0:
                left += term
            else:
                right += term
            assert 0 <= left < 2 and 0 <= right < 2
        constant = multiply(abs(rhs), length, Fraction(1))
        if rhs >= 0:
            right += constant
        else:
            left += constant
        assert 0 <= left < 2 and 0 <= right < 2
        assert (left <= right) == (sum(c*x for c, x in zip(coeffs, values)) <= rhs)
        count += 1
    for n in (5, 6):
        size = n+n*n
        p = n ** (n**4)
        p4 = p ** (4*n)
        u0 = 2*p4-p
        denominator = 1 << ((u0//2).bit_length()-1)
        assert 2*denominator <= u0 < 4*denominator
        assert size < p**n
        assert 4*denominator > p4 and denominator < p4
        upper_u = u0+size*p**(2*n)+2*size*p**(3*n)
        upper_v = u0+size*p**(2*n)
        assert upper_u < 20*denominator
        assert denominator*upper_v < 4*p**(8*n)
        print(f"normalization n={n} passed; D bits={denominator.bit_length()}")
    print(f"PASS {count} exact multiplier and signed-row cases; two source normalizations")


if __name__ == "__main__":
    main()
