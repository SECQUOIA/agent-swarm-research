"""Exact finite checks for the continuous sawtooth epigraph lift.

These checks cover finite dyadic cases, not the general proof or MILP complexity.
Run directly from the repository root; no solver or floating-point arithmetic.
"""

from fractions import Fraction as F


def tent(x):
    return min(2 * x, 2 * (1 - x))


def tail(depth, x):
    total = F(0)
    for j in range(1, depth + 1):
        x = tent(x)
        total += x / 4**j
    return total


def interpolation(depth, x):
    return x - tail(depth, x)


def check_dyadic_identities():
    intervals = 0
    for depth in range(9):
        cells = 2**depth
        eta = F(1, 4 ** (depth + 1))
        lip_bound = 1 - F(1, 2**depth)
        for j in range(cells + 1):
            x = F(j, cells)
            assert interpolation(depth, x) == x * x
        for j in range(cells):
            left, right = F(j, cells), F(j + 1, cells)
            mid = (left + right) / 2
            assert interpolation(depth, mid) - mid * mid == eta
            slope = (tail(depth, right) - tail(depth, left)) / (right - left)
            assert abs(slope) <= lip_bound
            assert 1 + slope >= F(1, 2**depth)
            # The shifted interpolant is a tangent at the cell midpoint.
            shifted_slope = (
                interpolation(depth, right) - interpolation(depth, left)
            ) / (right - left)
            assert shifted_slope == 2 * mid
            assert interpolation(depth, mid) - eta == mid * mid
            intervals += 1
    print(f"PASS: dyadic interpolation, sharp error, and tail slopes ({intervals} cells)")


def check_rescaling():
    cases = 0
    for low, high in [(F(-7, 3), F(5, 2)), (F(2, 7), F(4, 3)), (F(-4), F(-1))]:
        width = high - low
        for depth in range(6):
            eta = F(1, 4 ** (depth + 1))
            for j in range(2 ** (depth + 2) + 1):
                s = F(j, 2 ** (depth + 2))
                x = low + width * s
                lower = (
                    width * width * (interpolation(depth, s) - eta)
                    + 2 * low * width * s
                    + low * low
                )
                assert 0 <= x * x - lower <= width * width * eta
                cases += 1
    print(f"PASS: signed-interval square normalization ({cases} exact samples)")


def check_resultants():
    from sympy import expand, resultant, symbols

    u, t = symbols("u t")
    p = u * u - 2
    same = resultant(p, p.subs(u, u - t), u)
    different = resultant(p, ((u - t) ** 2 - 3), u)
    repeated = resultant(p, p.subs(u, u - t) ** 2, u)
    assert expand(same - t * t * (t * t - 8)) == 0
    assert expand(different - (t**4 - 10 * t * t + 1)) == 0
    assert expand(repeated - same**2) == 0
    print("PASS: difference resultants with distinct, shared, and repeated roots")


if __name__ == "__main__":
    check_dyadic_identities()
    check_rescaling()
    check_resultants()
