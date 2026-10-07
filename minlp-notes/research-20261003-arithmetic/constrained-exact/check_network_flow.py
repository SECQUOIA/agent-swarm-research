"""Exact boundary checks for the polynomial-flow Newton transfer.

This checks two parallel arcs with x1 + x2 = 1. It is not an implementation
of the strongly polynomial quadratic-flow subroutine used in the theorem.
"""

from fractions import Fraction as Q


def derivative(value, center, tilt):
    delta = value - center
    return 4 * delta**3 + 2 * delta + tilt


def hessian(value, center):
    return 12 * (value - center) ** 2 + 2


def check_case(name, optimum, lower, upper, tilts, starts):
    # Both arc costs have the form (z-center)^4 + (z-center)^2 + tilt*z.
    # Centers are (p, 1-p); a signed tilt difference supports endpoint optima.
    centers = (optimum, 1 - optimum)
    assert lower <= optimum <= upper
    assert (optimum == lower and tilts[0] >= tilts[1]) or (
        optimum == upper and tilts[0] <= tilts[1]
    ) or (lower < optimum < upper and tilts[0] == tilts[1])
    count = 0
    for initial in starts:
        current = initial
        assert lower <= current <= upper
        for _ in range(3):
            x = (current, 1 - current)
            h = tuple(hessian(v, s) for v, s in zip(x, centers))
            gradient = tuple(
                derivative(v, s, c) for v, s, c in zip(x, centers, tilts)
            )
            linear = tuple(g - hh * v for g, hh, v in zip(gradient, h, x))
            unconstrained = (h[1] + linear[1] - linear[0]) / (h[0] + h[1])
            assert unconstrained == current - (gradient[0] - gradient[1]) / sum(h)
            new = max(lower, min(upper, unconstrained))
            model_derivative = sum(h) * new + linear[0] - h[1] - linear[1]
            assert new == lower or model_derivative <= 0
            assert new == upper or model_derivative >= 0
            assert lower <= new <= upper
            assert new + (1 - new) == 1

            # On [0,1], |C'''| <= 24 and C'' >= 2, hence K=6.
            old_error_squared = 2 * (current - optimum) ** 2
            new_error_squared = 2 * (new - optimum) ** 2
            assert new_error_squared <= 36 * old_error_squared**2
            count += 1
            current = new
    print(f"PASS {name}: {count} exact Newton steps")
    return count


def main():
    zero, one = Q(0), Q(1)
    cases = [
        ("interior", Q(1, 3), zero, one, (zero, zero), (zero, Q(1, 2), one)),
        ("strict lower endpoint", zero, zero, one, (one, zero), (zero, Q(1, 4), one)),
        ("zero multiplier at lower endpoint", zero, zero, one, (zero, zero), (Q(1, 8), one)),
        ("zero multiplier at upper capacity", Q(2, 3), zero, Q(2, 3), (zero, zero), (zero, Q(1, 2))),
        ("strict upper capacity", Q(2, 3), zero, Q(2, 3), (-one, zero), (zero, Q(1, 2))),
        ("tiny inactive slack", Q(1, 2**80), zero, one, (zero, zero), (zero, Q(1, 4))),
    ]
    total = sum(check_case(*case) for case in cases)
    print(f"PASS: {len(cases)} boundary cases, {total} exact checks")


if __name__ == "__main__":
    main()
