"""Exact uniform coarsening and additive continuous-optimum certificates.

Input rows are exact cell masses, interpreted as constant rates within each
input cell. The routine integrates those rates across possibly nonaligned
coarse cells. No third-party dependency; the archived exact grid solver is
bundled next to this directory. No dwell or transition constraints are assumed.
"""
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reference"))
from rounding import _rational, _validated, optimal_few_switches, optimal_one_switch


@dataclass(frozen=True)
class CoarseCertificate:
    """Bounds concern the original A if ||A - supplied A||_infinity <= tolerance.

    exact_error is the returned schedule's error for the supplied rational
    input. upper bounds its error for the original input; lower bounds the
    original continuous optimum. lower_strict distinguishes (lower, upper]
    from [lower, upper]. schedule contains one zero-based label per coarse cell.
    """
    exact_error: Fraction
    mesh_width: Fraction
    cumulative_tolerance: Fraction
    lower: Fraction
    lower_strict: bool
    upper: Fraction
    schedule: tuple[int, ...]
    coarse_masses: tuple[tuple[Fraction, ...], ...]


def uniform_masses(allocations, durations, cells):
    """Integrate a piecewise-constant input exactly onto `cells` equal cells."""
    rows, dt, n = _validated(allocations, durations)
    if type(cells) is not int or cells < 1:
        raise ValueError("cells must be a positive integer")
    width = sum(dt) / cells
    coarse = []
    fine = 0
    fine_remaining = dt[0]
    rates = tuple(x / dt[0] for x in rows[0])
    for _ in range(cells):
        remaining = width
        masses = [Fraction(0)] * n
        while remaining:
            length = min(remaining, fine_remaining)
            for i in range(n):
                masses[i] += length * rates[i]
            remaining -= length
            fine_remaining -= length
            if not fine_remaining:
                fine += 1
                if fine < len(dt):
                    fine_remaining = dt[fine]
                    rates = tuple(x / dt[fine] for x in rows[fine])
        coarse.append(tuple(masses))
    return tuple(coarse), width


def certified_coarsen(allocations, durations, switch_budget, *, cells=None,
                     epsilon=None, cumulative_tolerance=0):
    """Return an exact coarse optimum with a certified additive error interval.

    Supply exactly one of positive integer cells or rational 0 < epsilon <= 1.
    The epsilon option uses ceil(1/epsilon) cells and gives suboptimality less
    than epsilon*T + 2*cumulative_tolerance for the original input. The caller
    is responsible for the stated original-to-supplied cumulative tolerance.
    A certificate for a given fine switching grid additionally requires every
    coarse boundary to be allowed there. This routine makes no such assumption.
    """
    if type(switch_budget) is not int or switch_budget < 0:
        raise ValueError("switch_budget must be a nonnegative integer")
    if (cells is None) == (epsilon is None):
        raise ValueError("supply exactly one of cells and epsilon")
    if epsilon is not None:
        epsilon = _rational(epsilon)
        if not 0 < epsilon <= 1:
            raise ValueError("epsilon must lie in (0, 1]")
        cells = (epsilon.denominator + epsilon.numerator - 1) // epsilon.numerator
    tolerance = _rational(cumulative_tolerance)
    if tolerance < 0:
        raise ValueError("cumulative_tolerance must be nonnegative")
    masses, width = uniform_masses(allocations, durations, cells)
    dt = (width,) * cells
    if switch_budget == 1:
        answer = optimal_one_switch(masses, dt)
    else:
        answer = optimal_few_switches(masses, dt, switch_budget)
    raw_lower = answer.error - width - tolerance
    return CoarseCertificate(answer.error, width, tolerance,
                             max(Fraction(0), raw_lower), raw_lower >= 0,
                             answer.error + tolerance, answer.schedule(), masses)
