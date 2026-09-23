"""Exact, solver-free certificates for uniform-mode CIA switching errors.

See results/cia-uniform-switching-obstruction.md. All numerical assertions use
integer or Fraction arithmetic. Exhaustive comparisons cover all schedules,
including revisited modes, on the indicated small instances.
"""
from fractions import Fraction
from itertools import product


def continuous_error(n, switches, horizon=1):
    if n < 2 or not 0 <= switches <= n - 2 or horizon <= 0:
        raise ValueError("Require n >= 2, 0 <= switches <= n-2, horizon > 0")
    r = Fraction(n, n - 1)
    return Fraction(horizon) * max(Fraction(1, n), 1 / (n * (r ** (switches + 1) - 1)))


def endpoint(n, switches, K):
    b = 0
    for _ in range(switches + 1):
        b = (n * b + K) // (n - 1)
    return b


def discrete_error(n, switches, N):
    continuous_error(n, switches, N)  # validate n, switches, and N
    if not isinstance(N, int):
        raise ValueError("N must be an integer")
    lo, hi = N, N * (n - 1)
    while lo < hi:
        mid = (lo + hi) // 2
        if endpoint(n, switches, mid) >= N:
            hi = mid
        else:
            lo = mid + 1
    return Fraction(lo, n)


def schedule_error(n, schedule):
    counts = [0] * n
    scaled_error = 0
    for t, mode in enumerate(schedule, 1):
        counts[mode] += 1
        scaled_error = max(scaled_error, *(abs(t - n * count) for count in counts))
    return Fraction(scaled_error, n)


def exhaustive_error(n, switches, N):
    return min(schedule_error(n, seq) for seq in product(range(n), repeat=N)
               if sum(x != y for x, y in zip(seq, seq[1:])) <= switches)


def verify():
    assert discrete_error(7, 1, 3) == Fraction(11, 7) > Fraction(3, 2)
    assert discrete_error(5, 1, 45) == 16
    assert continuous_error(5, 1, 45) == 16
    assert schedule_error(5, [0] * 20 + [1] * 25) == 16
    assert Fraction(45, 3) + Fraction(1, 2) == Fraction(31, 2) < 16
    small_count = 0
    for n in range(2, 6):
        for switches in range(n - 1):
            for N in range(1, 7):
                exact = discrete_error(n, switches, N)
                assert exact == exhaustive_error(n, switches, N), (n, switches, N, exact)
                small_count += 1
    bound_count = 0
    for n in range(2, 41):
        for switches in range(n - 1):
            for N in range(1, 41):
                disc = discrete_error(n, switches, N)
                cont = continuous_error(n, switches, N)
                assert cont <= disc < cont + Fraction(n - 1, n), (n, switches, N)
                bound_count += 1
    print(f"Exact counterexample: 16 > 31/2; exhaustive schedule checks: {small_count}; "
          f"continuous/discrete bound checks: {bound_count}.")


if __name__ == "__main__":
    verify()
