"""Independent original-discrepancy checks for coarsening and exact LP examples."""
from bisect import bisect_right
from fractions import Fraction as Q
from itertools import product
from math import comb
from random import Random
import json

from coarsening import certified_coarsen, uniform_masses
from continuous_exact import minimum_vertex, optimal_continuous
from rounding import optimal_few_switches


def breaks(lengths):
    result = [Q(0)]
    for length in lengths:
        result.append(result[-1] + length)
    return tuple(result)


def direct_error(rows, durations, word, times, one_sided=False):
    """Integrate both controls at all original and schedule breakpoints."""
    fine = breaks(durations)
    knots = sorted(set(fine + tuple(times)))
    discrepancy = [Q(0)] * len(rows[0])
    result = Q(0)
    for left, right in zip(knots, knots[1:]):
        # The midpoint also handles any zero-length schedule blocks.
        midpoint = (left+right)/2
        cell = bisect_right(fine, midpoint)-1
        active = word[bisect_right(times, midpoint)-1]
        for i in range(len(discrepancy)):
            discrepancy[i] += (right-left)*(rows[cell][i]/durations[cell] - int(i == active))
            result = max(result, -discrepancy[i] if one_sided else abs(discrepancy[i]))
    return result


def count_switches(word):
    return sum(a != b for a, b in zip(word, word[1:]))


def check_coarse():
    rng = Random(5102026)
    cases = 0
    for n, N, M in ((2, 3, 4), (3, 4, 3), (3, 3, 5), (2, 5, 3)):
        for _ in range(4):
            dt = tuple(Q(rng.randrange(1, 6), rng.randrange(1, 6)) for _ in range(N))
            weights = [tuple(rng.randrange(1, 6) for _ in range(n)) for _ in range(N)]
            rows = tuple(tuple(d*x/sum(row) for x in row) for d, row in zip(dt, weights))
            T = sum(dt)
            grid = tuple(T*j/M for j in range(M+1))
            objective = {word: direct_error(rows, dt, word, grid)
                         for word in product(range(n), repeat=M)}
            for s in range(3):
                certificate = certified_coarsen(rows, dt, s, cells=M)
                optimum = min(error for word, error in objective.items() if count_switches(word) <= s)
                assert certificate.exact_error == optimum == objective[certificate.schedule]
                assert certificate.upper == optimum
                assert count_switches(certificate.schedule) <= s
                assert certificate.mesh_width == T/M
                # An independently enumerated 2M-cell optimum on a nested grid
                # must lie inside the same certificate interval.
                refined_grid = tuple(T*j/(2*M) for j in range(2*M+1))
                # Enumerate words via at most s switch boundaries, avoiding n^(2M).
                from itertools import combinations
                finer = T
                for r in range(min(s+1, 2*M)):
                    for interior in combinations(range(1, 2*M), r):
                        times = (Q(0),) + tuple(refined_grid[j] for j in interior) + (T,)
                        for word in product(range(n), repeat=r+1):
                            finer = min(finer, direct_error(rows, dt, word, times))
                assert certificate.lower < finer if certificate.lower_strict else certificate.lower <= finer
                assert finer <= certificate.upper
                cases += 1
    # Fine mass data are interpreted as constant rates within each fine cell.
    rows, width = uniform_masses(((Q(1, 3), 0), (0, Q(2, 3))), (Q(1, 3), Q(2, 3)), 2)
    assert width == Q(1, 2)
    assert rows == ((Q(1, 3), Q(1, 6)), (0, Q(1, 2)))
    # Both sides of the clipping contract, including equality before clipping.
    a = certified_coarsen(((Q(1, 2), Q(1, 2)),), (1,), 0, cells=2)
    assert a.lower == 0 and a.lower_strict and a.exact_error == Q(1, 2)
    b = certified_coarsen(((1, 0),), (1,), 0, cells=2)
    assert b.lower == b.upper == 0 and not b.lower_strict
    c = certified_coarsen(((Q(1, 2), Q(1, 2)),), (1,), 1, epsilon=Q(2, 7))
    assert len(c.schedule) == 4 and c.mesh_width == Q(1, 4)
    assert c.lower < Q(1, 6) if c.lower_strict else c.lower <= Q(1, 6)
    assert Q(1, 6) <= c.upper
    return cases


def check_perturbation():
    # Actual constant rates (1/3,2/3), approximated by (1/2,1/2).
    original = ((Q(1, 3), Q(2, 3)),)
    supplied = ((Q(1, 2), Q(1, 2)),)
    actual_optimum = Q(2, 15)  # both one-switch orders, by the three-term formula
    for M in (1, 2, 3, 5):
        cert = certified_coarsen(supplied, (1,), 1, cells=M, cumulative_tolerance=Q(1, 6))
        value = direct_error(original, (1,), cert.schedule, tuple(Q(j, M) for j in range(M+1)))
        assert cert.lower < actual_optimum if cert.lower_strict else cert.lower <= actual_optimum
        assert actual_optimum <= value <= cert.upper
        assert value-actual_optimum < cert.mesh_width + 2*cert.cumulative_tolerance
    return 4


def check_dwell():
    source = ((Q(1, 2), 0), (0, Q(1, 2)))
    for M in (3, 5, 9):
        masses, h = uniform_masses(source, (Q(1, 2),)*2, M)
        answer = optimal_few_switches(masses, (h,)*M, 1, minimum_dwell=(Q(1, 2),)*2)
        assert answer.error == Q(1, 2) and count_switches(answer.schedule()) == 0
        assert direct_error(source, (Q(1, 2),)*2, (0, 1), (0, Q(1, 2), 1)) == 0
    masses, h = uniform_masses(source, (Q(1, 2),)*2, 4)
    answer = optimal_few_switches(masses, (h,)*4, 1, minimum_dwell=(Q(1, 2),)*2)
    assert answer.error == 0
    return 4


def check_continuous():
    cases = [(((Q(1, 2), Q(1, 2)),), (1,), 1, False, Q(1, 6)),
             (((Q(1, 3), Q(2, 3)),), (1,), 1, False, Q(2, 15)),
             (((Q(1, 3),)*3,), (1,), 1, False, Q(1, 3)),
             (((Q(1, 3),)*3,), (1,), 2, False, Q(1, 6)),
             (((Q(1, 3),)*3,), (1,), 2, True, Q(8, 57)),
             (((Q(1, 3), 0), (0, Q(2, 3))), (Q(1, 3), Q(2, 3)), 1, False, Q(0)),
             (((Q(1, 3), 0), (0, Q(1, 3)), (Q(1, 3), 0)), (Q(1, 3),)*3, 2, False, Q(0)),
             (((1, 0),), (1,), 1, False, Q(0)),
             (((Q(1, 3), Q(2, 3)),), (1,), 0, False, Q(1, 3))]
    output = []
    for rows, dt, s, one_sided, expected in cases:
        answer = optimal_continuous(rows, dt, s, one_sided=one_sided)
        assert answer.error == expected == direct_error(rows, dt, answer.modes, answer.times, one_sided)
        k, n, N = s+1, len(rows[0]), len(rows)
        assert answer.word_cell_programs == n**k * comb(N+k-2, k-1)
        output.append({'n':n,'input_cells':N,'switch_budget':s,'one_sided':one_sided,
                       'error':str(answer.error),'word':answer.modes,
                       'times':list(map(str,answer.times)),'programs':answer.word_cell_programs})
    # Lower-dimensional polytope: x=0, 1/3 <= E <= 1.
    point = minimum_vertex([((1, 0), 0), ((-1, 0), 0), ((0, -1), -Q(1, 3)), ((0, 1), 1)], 2)
    assert point == (0, Q(1, 3))
    return output


def check_validation():
    base = (((1, 0),), (1,), 1)
    for kwargs in ({}, {'cells':0}, {'cells':True}, {'cells':1.5},
                   {'epsilon':0}, {'epsilon':Q(3, 2)}, {'epsilon':0.5},
                   {'cells':2,'epsilon':Q(1, 2)}, {'cells':2,'cumulative_tolerance':-1}):
        try:
            certified_coarsen(*base, **kwargs)
        except (TypeError, ValueError):
            pass
        else:
            raise AssertionError(kwargs)


def main():
    if not __debug__:
        raise RuntimeError('Run without -O')
    check_validation()
    summary = {'coarse_original_objective_cases':check_coarse(),
               'perturbation_cases':check_perturbation(), 'dwell_refinement_cases':check_dwell(),
               'continuous_exact_cases':check_continuous()}
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
