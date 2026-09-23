"""Independent review: direct schedule enumeration and crossing-neighbor queries.

Run python code/cia_reopened/check_rounding_review.py.
Only the optimizer is imported; the reference error evaluator is independent.
"""
from fractions import Fraction as F
from itertools import product, combinations
from random import Random

from rounding import (optimal_one_switch, complete_with_one_block,
                      optimal_block_assignment, optimal_few_switches)


def direct(rows, dt, schedule):
    n = len(rows[0])
    allocation, service, error = [F(0)] * n, [F(0)] * n, F(0)
    for row, duration, mode in zip(rows, dt, schedule):
        service[mode] += duration
        for i in range(n):
            allocation[i] += row[i]
            error = max(error, abs(allocation[i] - service[i]))
    return error


def verify(rows, dt, allowed, initial):
    n, N = len(rows[0]), len(rows)
    starts = list(range(n)) if initial is None else [initial]
    reference = min(direct(rows, dt, [p] * N) for p in starts)
    for p in starts:
        for q in range(n):
            for k in allowed:
                reference = min(reference, direct(rows, dt, [p] * k + [q] * (N-k)))
    answer = optimal_one_switch(rows, dt, switch_indices=allowed, initial_mode=initial)
    assert answer.error == reference == direct(rows, dt, answer.schedule())
    assert answer.initial_mode in starts
    assert answer.switch_index == N or answer.switch_index in allowed

    # Independently implement the stated random-access query consequence.
    # Precomputed cumulative input and sorted eligible boundaries are assumed.
    if n == 1 or not allowed:
        return
    times, cumulative = [F(0)], [[F(0)] * n]
    for d, row in zip(dt, rows):
        times.append(times[-1] + d)
        cumulative.append([a+b for a, b in zip(cumulative[-1], row)])
    query_best = min(direct(rows, dt, [p] * N) for p in starts)
    boundaries = sorted(set(allowed))
    for p in starts:
        q = max((i for i in range(n) if i != p), key=lambda i: cumulative[-1][i])
        lo, hi = 0, len(boundaries)
        while lo < hi:
            mid = (lo + hi) // 2
            k = boundaries[mid]
            difference = 2 * times[k] - cumulative[k][p] - times[-1] + cumulative[-1][q]
            if difference < 0:
                lo = mid + 1
            else:
                hi = mid
        for j in (lo-1, lo):
            if 0 <= j < len(boundaries):
                k = boundaries[j]
                query_best = min(query_best, direct(rows, dt, [p] * k + [q] * (N-k)))
    assert query_best == reference


def main():
    count = 0
    # All half-integral 3-mode/3-interval instances, every boundary subset,
    # every fixed initial mode as well as the free initial-mode problem.
    columns = [tuple(F(v, 2) for v in row) for row in product(range(3), repeat=3) if sum(row) == 2]
    for rows in product(columns, repeat=3):
        for allowed in ([], [1], [2], [1, 2]):
            for initial in (None, 0, 1, 2):
                verify(rows, [1] * 3, allowed, initial)
                count += 1
    # Arbitrary positive rational grids; include n=1, n=2, N=1, zero-total
    # modes, ties, empty eligible sets, and duplicate/unsorted boundaries.
    rng = Random(193487)
    for _ in range(160):
        n, N = rng.randrange(1, 8), rng.randrange(1, 9)
        dt = [F(rng.randrange(1, 9), rng.randrange(1, 8)) for _ in range(N)]
        rows = []
        for d in dt:
            weights = [rng.randrange(5) for _ in range(n)]
            if not any(weights):
                weights[0] = 1
            rows.append([d * F(w, sum(weights)) for w in weights])
        allowed = [k for k in range(1, N) if rng.randrange(2)]
        allowed = list(reversed(allowed)) + allowed[:1]
        for initial in (None, rng.randrange(n)):
            verify(rows, dt, allowed, initial)
            count += 1
    for rows, dt, kwargs, exception in [
        ([], [1], {}, ValueError),
        ([[]], [1], {}, ValueError),
        ([[1]], [], {}, ValueError),
        ([[1], [1, 0]], [1, 1], {}, ValueError),
        ([[-1, 2]], [1], {}, ValueError),
        ([[True]], [1], {}, TypeError),
        ([[1]], [1.0], {}, TypeError),
        ([[1]], [1], {"initial_mode": True}, ValueError),
        ([[1], [1]], [1, 1], {"switch_indices": [True]}, ValueError),
        ([[1], [1]], [1, 1], {"switch_indices": [F(1)]}, ValueError),
        ([[1], [1]], [1, 1], {"switch_indices": [1, True]}, ValueError),
        ([[1], [1]], [1, 1], {"switch_indices": [1, 1.0]}, ValueError),
        ([[1], [1]], [1, 1], {"switch_indices": [1, F(1)]}, ValueError),
    ]:
        try:
            optimal_one_switch(rows, dt, **kwargs)
        except exception:
            pass
        else:
            raise AssertionError((rows, dt, kwargs))
    print(f"PASS: {count} independent enumeration/crossing checks; 13 invalid-input checks")
    extension_checks()


def extension_checks():
    # Explicit negative residual: service to mode 0 exceeds its entire mass.
    assert complete_with_one_block([[0, 1]] * 3, [1] * 3, [0, 0]) == (F(2), 1)
    rng = Random(746389)
    assignments = completions = budgets = 0
    for instance in range(32):
        n, N = rng.randrange(1, 5), rng.randrange(1, 6)
        dt = [F(rng.randrange(1, 5), rng.randrange(1, 5)) for _ in range(N)]
        rows = []
        for d in dt:
            weights = [rng.randrange(4) for _ in range(n)]
            if not any(weights):
                weights[0] = 1
            rows.append([d * F(w, sum(weights)) for w in weights])
        all_schedules = [(word, direct(rows, dt, word)) for word in product(range(n), repeat=N)]
        for budget in range(N+2):
            best = min(value for word, value in all_schedules
                       if sum(a != b for a, b in zip(word, word[1:])) <= budget)
            answer = optimal_few_switches(rows, dt, budget)
            assert answer.error == best == direct(rows, dt, answer.schedule())
            assert sum(a != b for a, b in zip(answer.schedule(), answer.schedule()[1:])) <= budget
            budgets += 1
        for k in range(1, N+1):
            for interior in combinations(range(1, N), k-1):
                boundaries = (0,) + interior + (N,)
                words = [tuple(mode for mode, left, right in zip(modes, boundaries, boundaries[1:])
                               for _ in range(right-left)) for modes in product(range(n), repeat=k)]
                best = min(direct(rows, dt, word) for word in words)
                answer = optimal_block_assignment(rows, dt, boundaries)
                assert answer.error == best == direct(rows, dt, answer.schedule())
                assignments += 1
        for length in range(N):
            for prefix in product(range(n), repeat=length):
                for required in (False, True):
                    eligible = [q for q in range(n) if not (required and prefix and q == prefix[-1])]
                    if not eligible:
                        try:
                            complete_with_one_block(rows, dt, prefix, require_switch=required)
                        except ValueError:
                            pass
                        else:
                            raise AssertionError("ineligible suffix accepted")
                        continue
                    best = min(direct(rows, dt, prefix + (q,) * (N-length)) for q in eligible)
                    value, q = complete_with_one_block(rows, dt, prefix, require_switch=required)
                    assert q in eligible
                    assert value == best == direct(rows, dt, prefix + (q,) * (N-length))
                    completions += 1
    print(f"PASS: {assignments} prescribed partitions, {budgets} switch budgets, "
          f"{completions} arbitrary-prefix completions")


if __name__ == "__main__":
    main()
