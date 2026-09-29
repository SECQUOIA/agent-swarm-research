"""Evaluate explicit signed-kernel bounds; this is not a solver benchmark.

The admissibility checks and the choice of the even parameter N are exact.
Displayed error bounds are Decimal approximations to the theorem's formula,
not directed-rounding certificates. No SDP is solved.
"""

from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb


def prescribed_n(s, width):
    """Equation (15), computed without floating-point logarithms."""
    exponent = max(6, width + 1)
    n = 2
    while (1 << (2 * n)) < s**exponent:
        n += 2
    return n


def largest_prescribed_s(order, width):
    lower, upper = 2, order
    result = None
    while lower <= upper:
        s = (lower + upper) // 2
        n = prescribed_n(s, width)
        if 2 * width * (s - 1) * (n + 1) <= order:
            result = s
            lower = s + 1
        else:
            upper = s - 1
    return result


def as_decimal(value):
    return Decimal(value.numerator) / Decimal(value.denominator)


def relative_bound(order, width, degree, s, n):
    assert s >= max(2, degree) and n >= 2 and n % 2 == 0
    source_degree = 2 * (s - 1) * (n + 1)
    assert width * source_degree <= order
    c_s = Fraction(2 * s * s + 1, 3 * s)
    delta = Fraction(1, 2 ** (n + 1))
    b = Fraction(s * s * (n + 1)) / c_s
    correction = sum(
        (comb(width, j) * delta**j * b ** (width - j)
         for j in range(2, width + 1)), Fraction(0)
    )
    first = Fraction(n + 1) / c_s * (
        Fraction(degree * degree, s * s)
        + Fraction(3 * degree * degree, 2 * s)
    )
    eta = as_decimal(first) + (
        Decimal(2 * (source_degree + 1)).sqrt() * as_decimal(delta)
    )
    return (1 + eta)**width - 1 + 2 * as_decimal(correction)


def main():
    getcontext().prec = 40
    print("d_infty=2; approximate E/C_f from the explicit theorem")
    print("width,order,s,N,E_over_C_f,parameter_choice")
    for width in (2, 5, 10):
        for order in (1000, 10000, 100000):
            s = largest_prescribed_s(order, width)
            assert s is not None
            n = prescribed_n(s, width)
            error = relative_bound(order, width, 2, s, n)
            print(f"{width},{order},{s},{n},{error:.9g},equation_15")
    # The asymptotic prescription is not necessarily a good finite-order
    # choice. This single alternative illustrates that distinction.
    error = relative_bound(100000, 10, 2, 82, 60)
    print(f"10,100000,82,60,{error:.9g},admissible_alternative")
    print("No runtime, sharpness, or universal proof conclusion follows.")


if __name__ == "__main__":
    main()
