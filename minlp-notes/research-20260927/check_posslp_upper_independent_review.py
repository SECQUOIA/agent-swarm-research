"""Targeted exact checks for the independent cubic-root upper-bound review.

The symbolic identities hold for arbitrary variables. The finite integer
checks stress the endpoint constants; they do not prove the universal
separation or induction arguments and do not expand Newton iterates.
"""

import sympy as sp


def check_newton_identities():
    e = sp.symbols("e", nonnegative=True)
    relative_update = (2 * (1 + e) + (1 + e) ** -2) / 3 - 1
    claimed = e**2 * (3 + 2 * e) / (3 * (1 + e) ** 2)
    assert sp.cancel(relative_update - claimed) == 0
    assert sp.cancel(
        e**2 - claimed - e**3 * (3 * e + 4) / (3 * (e + 1) ** 2)
    ) == 0
    assert sp.cancel(
        2 * e / 3 - claimed - e * (e + 2) / (3 * (e + 1) ** 2)
    ) == 0


def check_fraction_conversion():
    na, nb = sp.symbols("na nb", nonzero=True)
    da, db = sp.symbols("da db", positive=True)
    converted = na * db * nb / (da * nb**2)
    assert sp.cancel(converted - (na / da) / (nb / db)) == 0
    # The numerator can also be zero; no cancellation assumption is used.
    assert sp.cancel(converted.subs(na, 0)) == 0


def check_constant_margins():
    for length in range(2, 129):
        assert (2 * length + 1) <= 2 ** (2 * length)
        assert (4 * length + 2) <= 2 ** (2 * length)
        separation_exponent = length + (4 * length + 1) * (
            3**length - 1
        )
        assert separation_exponent <= 2 ** (6 * length)
        assert length * (2**length + 3 * 2 ** (2 * length)) <= 2 ** (
            4 * length
        )
        total_error_exponent = (
            6 * length**2 + 4 * length + 1 - 2 ** (10 * length)
        )
        assert total_error_exponent <= -7 * length - 1
        assert total_error_exponent <= -(2 ** (6 * length)) - 3
        assert 2 ** (6 * length) >= 20 * length**2
        assert 6 * length**2 + 11 * length + 5 <= 20 * length**2


if __name__ == "__main__":
    check_newton_identities()
    check_fraction_conversion()
    check_constant_margins()
    print("PASS: exact Newton error identities")
    print("PASS: denominator-positive fraction identity")
    print("PASS: integer constant margins for input lengths 2 through 128")
