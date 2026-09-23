"""Exact CIA optimization with at most one switch on an arbitrary rational grid.

Input allocations are interval *masses*, not rates: each row sums to that
interval's positive duration. No third-party packages or floating arithmetic.
See notes/cia-reopened-practical-algorithm.md for proof and scope.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from numbers import Rational
from typing import Iterable, Sequence


@dataclass(frozen=True)
class OneSwitchSolution:
    error: Fraction
    initial_mode: int
    final_mode: int
    switch_index: int  # first interval using final_mode; N for a constant
    intervals: int

    def schedule(self) -> tuple[int, ...]:
        return (self.initial_mode,) * self.switch_index + (self.final_mode,) * (
            self.intervals - self.switch_index
        )


def _rational(x: Rational) -> Fraction:
    if not isinstance(x, Rational) or isinstance(x, bool):
        raise TypeError("Use exact rational numbers, such as int or Fraction")
    return Fraction(x)


def _validated(allocations: Sequence[Sequence[Rational]], durations: Sequence[Rational]):
    dt = tuple(_rational(x) for x in durations)
    if not dt or any(x <= 0 for x in dt):
        raise ValueError("durations must be nonempty and positive")
    rows = tuple(tuple(_rational(x) for x in row) for row in allocations)
    if len(rows) != len(dt) or not rows[0]:
        raise ValueError("one nonempty allocation row is required per interval")
    n = len(rows[0])
    if any(len(row) != n or any(x < 0 for x in row) or sum(row) != d
           for row, d in zip(rows, dt)):
        raise ValueError("allocation rows must be nonnegative, equal length, and sum to durations")
    return rows, dt, n


def optimal_one_switch(
    allocations: Sequence[Sequence[Rational]],
    durations: Sequence[Rational],
    *,
    switch_indices: Iterable[int] | None = None,
    initial_mode: int | None = None,
) -> OneSwitchSolution:
    """Minimize maximum cumulative component error with at most one switch.

    Switch indices are internal grid boundaries 1,...,N-1. Restrict them to
    encode a common minimum dwell time or permitted switching windows. Constant
    schedules are always eligible. initial_mode fixes the first active mode.
    These constraints do not change the O(n*N) arithmetic-operation bound.
    """
    rows, dt, n = _validated(allocations, durations)
    N = len(dt)
    if initial_mode is not None and (type(initial_mode) is not int or not 0 <= initial_mode < n):
        raise ValueError("initial_mode must be a valid mode index")
    boundaries = list(range(1, N)) if switch_indices is None else list(switch_indices)
    if any(type(k) is not int or not 1 <= k < N for k in boundaries):
        raise ValueError("switch indices must be internal integer grid boundaries")
    allowed = set(boundaries)
    totals = tuple(sum(row[i] for row in rows) for i in range(n))
    T = sum(dt)
    # Only three maxima are needed; selecting each avoids an n log n sort.
    leaders: list[int] = []
    for _ in range(min(3, n)):
        leaders.append(max((i for i in range(n) if i not in leaders), key=lambda i: (totals[i], -i)))
    first = leaders[0]
    p0 = first if initial_mode is None else initial_mode
    best = OneSwitchSolution(T - totals[p0], p0, p0, N, N)
    if n == 1 or not allowed:
        return best
    second = leaders[1]
    A = [Fraction(0) for _ in range(n)]
    t = Fraction(0)
    for k, (row, d) in enumerate(zip(rows, dt), 1):
        t += d
        for i in range(n):
            A[i] += row[i]
        if k not in allowed:
            continue
        if initial_mode is None:
            candidates = [first, second]
            if n > 2:
                candidates.append(max((i for i in range(n) if i not in (first, second)),
                                      key=lambda i: (A[i], -i)))
        else:
            candidates = [initial_mode]
        for p in candidates:
            q = second if p == first else first
            omitted = next((totals[i] for i in leaders if i not in (p, q)), Fraction(0))
            error = max(omitted, t - A[p], T - t - totals[q])
            if error < best.error:
                best = OneSwitchSolution(error, p, q, k, N)
    return best


def schedule_error(allocations: Sequence[Sequence[Rational]], durations: Sequence[Rational],
                   schedule: Sequence[int]) -> Fraction:
    """Direct exact prefix evaluation, independent of the optimizer's formula."""
    rows, dt, n = _validated(allocations, durations)
    if len(schedule) != len(rows) or any(type(i) is not int or not 0 <= i < n for i in schedule):
        raise ValueError("schedule must contain one valid mode per interval")
    discrepancy = [Fraction(0) for _ in range(n)]
    error = Fraction(0)
    for row, d, active in zip(rows, dt, schedule):
        for i, a in enumerate(row):
            discrepancy[i] += a - (d if i == active else 0)
            error = max(error, abs(discrepancy[i]))
    return error


@dataclass(frozen=True)
class BlockSolution:
    error: Fraction
    boundaries: tuple[int, ...]  # includes 0 and N
    modes: tuple[int, ...]  # one per block; neighboring modes may coincide

    def schedule(self) -> tuple[int, ...]:
        return tuple(mode for mode, left, right in zip(self.modes, self.boundaries, self.boundaries[1:])
                     for _ in range(right - left))


def complete_with_one_block(allocations, durations, prefix, *, require_switch=False):
    """Optimally append a constant suffix to an arbitrary fixed prefix.

    Returns (error, final_mode). If require_switch, the suffix mode must differ
    from the prefix's last mode. With an empty prefix every mode is eligible.
    """
    rows, dt, n = _validated(allocations, durations)
    prefix = tuple(prefix)
    if len(prefix) >= len(rows) or any(type(i) is not int or not 0 <= i < n for i in prefix):
        raise ValueError("prefix must use valid modes and leave a nonempty suffix")
    discrepancy = [Fraction(0)] * n
    past_error = Fraction(0)
    service = [Fraction(0)] * n
    for row, d, active in zip(rows, dt, prefix):
        service[active] += d
        for i in range(n):
            discrepancy[i] += row[i] - (d if i == active else 0)
            past_error = max(past_error, abs(discrepancy[i]))
    residual = [sum(row[i] for row in rows) - service[i] for i in range(n)]
    eligible = [i for i in range(n) if not (require_switch and prefix and i == prefix[-1])]
    if not eligible:
        raise ValueError("no eligible final mode")
    final = max(eligible, key=lambda i: (residual[i], -i))
    remaining = sum(dt[len(prefix):])
    error = max(past_error, remaining - residual[final],
                max((residual[i] for i in range(n) if i != final), default=Fraction(0)))
    return error, final


def _prefix_data(rows, dt, n):
    times = [Fraction(0)]
    A = [[Fraction(0)] for _ in range(n)]
    for row, d in zip(rows, dt):
        times.append(times[-1] + d)
        for i in range(n):
            A[i].append(A[i][-1] + row[i])
    return A, times


def _dwell_values(minimum_dwell, n):
    values = (Fraction(0),) * n if minimum_dwell is None else tuple(_rational(x) for x in minimum_dwell)
    if len(values) != n or any(x < 0 for x in values):
        raise ValueError("minimum_dwell must have one nonnegative duration per mode")
    return values


def _assign_blocks(A, times, boundaries, minimum_dwell):
    """Exact bottleneck subset-partition DP, with disconnected subsets allowed."""
    n, k = len(A), len(boundaries) - 1
    states = 1 << k
    lengths = [times[r] - times[l] for l, r in zip(boundaries, boundaries[1:])]
    dp = [None] * states
    dp[0] = Fraction(0)
    parents = []
    for i in range(n):
        costs = []
        for mask in range(states):
            service, error, run = Fraction(0), Fraction(0), Fraction(0)
            valid = True
            for b, right in enumerate(boundaries[1:]):
                if mask & (1 << b):
                    service += lengths[b]
                    run += lengths[b]
                elif run:
                    valid = valid and run >= minimum_dwell[i]
                    run = Fraction(0)
                error = max(error, abs(A[i][right] - service))
            valid = valid and (not run or run >= minimum_dwell[i])
            costs.append(error if valid else None)
        nxt, choice = [None] * states, [None] * states
        for covered in range(states):
            assigned = covered
            while True:
                earlier = dp[covered ^ assigned]
                if earlier is not None and costs[assigned] is not None:
                    value = max(earlier, costs[assigned])
                    if nxt[covered] is None or value < nxt[covered]:
                        nxt[covered], choice[covered] = value, assigned
                if assigned == 0:
                    break
                assigned = (assigned - 1) & covered
        dp = nxt
        parents.append(choice)
    if dp[-1] is None:
        return None
    covered = states - 1
    modes = [-1] * k
    for i in reversed(range(n)):
        assigned = parents[i][covered]
        assert assigned is not None
        for b in range(k):
            if assigned & (1 << b):
                modes[b] = i
        covered ^= assigned
    assert covered == 0 and all(i >= 0 for i in modes)
    return BlockSolution(dp[-1], tuple(boundaries), tuple(modes))


def optimal_block_assignment(allocations, durations, boundaries, *, minimum_dwell=None):
    """Optimize mode labels for prescribed blocks, including repeated modes.

    boundaries must include 0 and N. minimum_dwell supplies one nonnegative
    duration per mode. Every maximal active run, including both horizon-end
    runs, must meet it; unused modes are allowed. Returns None if infeasible.
    Complexity O(n*(k*2**k + 3**k)) after
    cumulative allocation preprocessing, and O(n*2**k) traceback storage.
    """
    rows, dt, n = _validated(allocations, durations)
    boundaries = tuple(boundaries)
    if (len(boundaries) < 2 or boundaries[0] != 0 or boundaries[-1] != len(rows)
            or any(type(b) is not int for b in boundaries)
            or any(a >= b for a, b in zip(boundaries, boundaries[1:]))):
        raise ValueError("boundaries must strictly increase from 0 to N")
    A, times = _prefix_data(rows, dt, n)
    return _assign_blocks(A, times, boundaries, _dwell_values(minimum_dwell, n))


def optimal_few_switches(allocations, durations, switch_budget, *, minimum_dwell=None):
    """Exact solver for a small total switch budget on any rational grid.

    Enumerates grid partitions, using subset DP instead of enumerating n**k
    mode words. Exponential in block count and polynomial in grid length for
    fixed budget. Optional per-mode minimum dwell applies to maximal active
    runs including horizon ends. Returns None if infeasible. For budget one
    without dwell constraints use optimal_one_switch for linear time.
    """
    from itertools import combinations

    rows, dt, n = _validated(allocations, durations)
    if type(switch_budget) is not int or switch_budget < 0:
        raise ValueError("switch_budget must be a nonnegative integer")
    k, N = min(switch_budget + 1, len(rows)), len(rows)
    A, times = _prefix_data(rows, dt, n)
    minimum_dwell = _dwell_values(minimum_dwell, n)
    best = None
    for interior in combinations(range(1, N), k - 1):
        answer = _assign_blocks(A, times, (0,) + interior + (N,), minimum_dwell)
        if answer is not None and (best is None or answer.error < best.error):
            best = answer
    return best
