#!/usr/bin/env python3
"""Exact-rational checks of geometric grids and contraction constants.

Run directly with Python 3.10+; only the adjacent exact_checks module is used.
The sweep tests geometry beyond the theorem's theta <= 1/2 restriction.
"""

from fractions import Fraction as Q
from itertools import product

from exact_checks import coordinate_grid, penalties


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def check_grids():
    continuous_boxes = (
        (Q(-13, 4), Q(19, 6), Q(-13, 4)),
        (Q(-13, 4), Q(19, 6), Q(-11, 6)),
        (Q(-13, 4), Q(19, 6), Q(2, 7)),
        (Q(-13, 4), Q(19, 6), Q(19, 6)),
        (Q(2, 7), Q(2, 7), Q(2, 7)),
    )
    integer_boxes = tuple((Q(-7), Q(8), Q(c)) for c in (-7, -3, 2, 8)) + (
        (Q(3), Q(3), Q(3)),
    )
    scales = (Q(1, 16), Q(1, 2), Q(1), Q(3, 2), Q(3))
    slopes = (Q(1, 16), Q(1, 8), Q(1, 2), Q(1), Q(3, 2))
    L = Q(7, 3)
    cases = vertices = clipped = unit_gaps = 0
    for integer, h, theta in product((False, True), scales, slopes):
        boxes = integer_boxes if integer else continuous_boxes
        for lo, hi, center in boxes:
            label = f"integer={integer}, box=({lo},{hi}), c={center}, h={h}, theta={theta}"
            grid, clips = coordinate_grid(lo, hi, center, h, theta, integer)
            correction = penalties(grid, integer, L)
            require(grid[0] == lo and grid[-1] == hi and center in grid, label + ": endpoints and center")
            require(all(a < b for a, b in zip(grid, grid[1:])), label + ": strictly increasing")
            require(len(correction) == len(grid), label + ": one penalty per vertex")
            if integer:
                require(all(v.denominator == 1 for v in grid), label + ": integral vertices")
            if lo == hi:
                require(grid == (center,) and correction == (Q(0),) and clips == 0,
                        label + ": singleton coordinate")

            gaps = tuple(b-a for a, b in zip(grid, grid[1:]))
            for j, (v, dv) in enumerate(zip(grid, correction)):
                adjacent = gaps[max(0, j-1):j+1]
                retained = tuple(gap for gap in adjacent if not integer or gap != 1)
                max_gap = max(retained, default=Q(0))
                require(dv == L*max_gap**2/8, label + ": adjacent-gap penalty")
                require(max_gap <= h+theta*abs(v-center), label + ": retained adjacent-gap bound")
                require(dv <= L*(h*h+theta**2*(v-center)**2)/4,
                        label + ": squared-distance penalty bound")
            cases += 1
            vertices += len(grid)
            clipped += clips
            unit_gaps += sum(gap == 1 for gap in gaps) if integer else 0

    # Final clipping can create a unit gap beside a gap that still needs a penalty.
    grid, clips = coordinate_grid(Q(0), Q(4), Q(0), Q(3), Q(1, 2), True)
    require(grid == (Q(0), Q(3), Q(4)) and clips == 1, "integer final clipping")
    require(penalties(grid, True, L) == (9*L/8, 9*L/8, Q(0)),
            "omit the clipped unit gap without omitting its neighbor")
    grid, clips = coordinate_grid(Q(0), Q(1), Q(0), Q(3, 4), Q(1, 2), False)
    require(grid == (Q(0), Q(3, 4), Q(1)) and clips == 1, "continuous final clipping")
    require(penalties((Q(0), Q(1), Q(2)), True, L) == (Q(0), Q(0), Q(0)),
            "all unit integer gaps have zero penalty")
    require(penalties((Q(0), Q(1)), False, L) == (L/8, L/8),
            "continuous unit gaps retain their penalty")
    require(clipped > 0 and unit_gaps > 0, "sweep exercises clipping and unit gaps")
    print(f"Grid sweep passed: {cases} cases, {vertices} vertices, {clipped} clipped sides, "
          f"{unit_gaps} integer unit gaps; four boundary fixtures passed.")


def check_constants():
    # r = L/c_g and q = theta^2. Include both switching points r=1/2 and r=11/4.
    ratios = (Q(1, 100), Q(1, 10), Q(49, 100), Q(1, 2), Q(51, 100), Q(1),
              Q(109, 40), Q(11, 4), Q(111, 40), Q(3), Q(10), Q(100))
    cases = 0
    for r, fraction in product(ratios, (Q(1), Q(1, 4), Q(1, 9))):
        q = fraction*min(Q(1, 4), 1/(8*r))
        B = max(Q(1), 4*r/11)
        denominator = 4-2*r*q
        require(denominator > 0, "positive recurrence denominator")
        require(r/denominator <= 4*r/15, "recurrence mesh coefficient")
        require(2*r*q/denominator <= Q(1, 15), "recurrence previous-error coefficient")
        require(4*r/15+4*B/15 <= B, "halving invariant")
        require(q*B <= Q(1, 4), "theta-squared times B")
        require(Q(1, 4)+Q(5, 2)*q*B <= Q(7, 8), "final correction coefficient")
        cases += 1
    print(f"Contraction constants passed: {cases} exact rational cases.")


def check_rejected_inputs():
    # These are the input conditions explicitly enforced by coordinate_grid.
    rejected = (
        (Q(0), Q(1), Q(2), Q(1), Q(1, 8), False),
        (Q(0), Q(1), Q(0), Q(0), Q(1, 8), False),
        (Q(0), Q(1), Q(0), Q(1), Q(0), False),
    )
    for arguments in rejected:
        try:
            coordinate_grid(*arguments)
        except AssertionError as error:
            require(str(error) == "grid inputs", "input rejection reason")
        else:
            raise AssertionError(f"expected grid input rejection: {arguments}")
    print(f"Input validation passed: {len(rejected)} rejected cases.")


if __name__ == "__main__":
    check_grids()
    check_constants()
    check_rejected_inputs()
