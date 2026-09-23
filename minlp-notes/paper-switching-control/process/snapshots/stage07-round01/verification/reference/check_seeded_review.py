"""Independent exact checks of the four-block-seeded CIA upper coefficient.

Uses no author implementation. Finite checks supplement the analytic review;
they do not prove a measurable-control theorem or establish novelty.
"""

from fractions import Fraction as Q


def multiply(a, b, size):
    return [sum((a[j] * b[i - j] for j in range(i + 1)
                 if j < len(a) and i - j < len(b)), Q(0))
            for i in range(size)]


def divide(a, b, size):
    assert b[0]
    out = []
    for i in range(size):
        previous = sum((b[j] * out[i - j]
                        for j in range(1, min(i + 1, len(b)))), Q(0))
        out.append(((a[i] if i < len(a) else Q(0)) - previous) / b[0])
    return out


def lower(n, k):
    return Q((n - 1) ** k, n * (n ** k - (n - 1) ** k))


def old(n, k):
    return Q(n * (n - 1) + (n - k) * (n - k - 1),
             n * k * (2 * n - k - 1))


def seeded(n, k, *, clipped=True):
    m = n - k + 4
    # Clearing all powers in the displayed eta expression gives integers.
    a = n * (n - 1) * m ** 3
    b = (m - 1) * (2 * (m - 1) ** 4 - m ** 4)
    if clipped:
        b = max(0, b)
    return Q(a + b, n * (a - b))


def check():
    if not __debug__:
        raise RuntimeError("Run without -O: this checker uses assertions.")
    coefficient_cases = 0
    for m in range(5, 65):
        c = max(Q(1, m), lower(m, 4))
        raw = lower(m, 4)
        assert old(m, 4) - lower(m, 4) == Q(
            10 * m * m - 5 * m + 1,
            2 * (2 * m - 5) * (2 * m - 1) * (2 * m * m - 2 * m + 1))
        for steps in range(65):
            n, k = m + steps, 4 + steps
            assert c == seeded(n, k)
            assert Q(1, n) <= c
            assert lower(n, k) <= c <= old(n, k)
            assert (c < old(n, k)) == (m >= 6)
            assert raw == seeded(n, k, clipped=False)
            assert lower(n, k) <= raw <= c
            assert raw < old(n, k)
            assert (raw < c) == (m <= 6)
            assert max(c, Q(1, k + 1)) <= max(old(n, k), Q(1, k + 1))
            coefficient_cases += 1
            # Use D=n*c and the original fractional-linear D recurrence.
            d = n * c
            next_d = (n * d + 1) / (n + d)
            assert ((next_d - 1) / (next_d + 1)
                    == Q(n - 1, n + 1) * (d - 1) / (d + 1))
            c = next_d / (n + 1)
            raw_d = n * raw
            raw = (n * raw_d + 1) / ((n + raw_d) * (n + 1))

    minimum_branch_cases = 0
    for n in range(3, 51):
        for q in (Q(1, 1000), Q(1, 10), Q(1, 2), Q(999, 1000)):
            child = q / (n - 1)
            e = ((n - 1) ** 2 * child + 1) / (n * (n - 1) * (1 + child))
            assert Q(1, n * (n - 1)) < e < Q(1, n)
            for a in (Q(0), Q(1, 100 * n), Q(1, 2 * n), Q(1, n)):
                length = 1 - a - e
                budget = e - a / (n - 1)
                assert length > 1 - Q(2, n)
                assert budget > 0 and child * length <= budget
                minimum_branch_cases += 1

    series_cases = 0
    for k in range(4, 101):
        # Formal x=1/n series, independently expanding the original formula.
        d = k - 4
        m_scaled = [Q(1), Q(-d)]
        mm1_scaled = [Q(1), Q(-d - 1)]
        ratio = divide(mm1_scaled, m_scaled, 4)
        power = [Q(1)]
        for _ in range(4):
            power = multiply(power, ratio, 4)
        power = [2 * p for p in power]
        power[0] -= 1
        prefactor = divide(multiply(m_scaled, mm1_scaled, 4), [Q(1), Q(-1)], 4)
        eta = multiply(prefactor, power, 4)
        assert eta == [Q(1), Q(-2 * k), Q(k * (k - 1)), Q(k * k - k - 20)]
        # x cancels the zero constant term in 1-eta.
        numerator = list(eta)
        numerator[0] += 1
        coefficient = divide(numerator, [-p for p in eta[1:]], 3)
        expected = [Q(1, k), Q(-k - 1, 2 * k),
                    Q(k * k - 1, 4 * k) - Q(10, k * k)]
        assert coefficient == expected
        uniform_second = Q(k * k - 1, 12 * k)
        assert coefficient[2] - uniform_second == Q(k ** 3 - k - 60, 6 * k * k)
        series_cases += 1

    assert seeded(16, 5) == Q(588449, 3544816) < Q(1, 6)
    assert old(16, 5) == Q(35, 208) > Q(1, 6)
    assert seeded(17, 5) > Q(1, 6)
    assert lower(5, 4) < Q(1, 5) and lower(6, 4) < Q(1, 6)
    assert lower(7, 4) > Q(1, 7)
    return {"coefficient_cases": coefficient_cases, "formal_series_cases": series_cases,
            "minimum_branch_cases": minimum_branch_cases,
            "plateau_16_modes_4_switches": "passed"}


def check_event_witness():
    """Read saved values and verify stated constraints without building LP rows."""
    import json
    from itertools import combinations
    from pathlib import Path
    x = [Q(v) for v in json.loads(Path(__file__).with_name(
        "general_reach_relaxation_witness.json").read_text())["variables"]]
    assert len(x) == 454 and min(x) >= 0
    roots = x[:6]
    all_modes = frozenset(range(6))
    events = {}
    cursor = 6
    for order, smallest in ((2, 3), (3, 4)):
        for size in range(6, smallest - 1, -1):
            for subset in combinations(range(6), size):
                events[order, frozenset(subset)] = (x[cursor], x[cursor + 1:cursor + 7])
                cursor += 7
    assert cursor == len(x)
    assert min(roots) >= 1 and roots[0] == min(roots)
    assert sum(roots[1:]) >= 6
    inequality_count = 12
    for (order, available), (time, allocations) in events.items():
        assert sum(allocations) == time
        for i in available:
            assert allocations[i] >= roots[i] - 1
            inequality_count += 1
            if order == 2:
                for j in available - {i}:
                    assert time - allocations[i] >= roots[j] + 1
                    inequality_count += 1
            else:
                assert time - allocations[i] >= events[2, available - {i}][0] + 1
                inequality_count += 1
        for (other_order, other_set), (_, other_allocations) in events.items():
            if ((order, available) != (other_order, other_set)
                    and order <= other_order and available <= other_set):
                assert all(a <= b for a, b in zip(allocations, other_allocations))
                inequality_count += 6
        maximizer = frozenset(range(order))
        if maximizer <= available and available != all_modes:
            assert allocations == events[order, all_modes][1]
            inequality_count += 6
    assert inequality_count == 3660 and len(events) == 64
    objective = sum(events[3, all_modes - {i}][0]
                    + sum(events[3, all_modes - {i, j}][0]
                          for j in all_modes - {i}) for i in range(4))
    assert objective == Q(40328, 387) < Q(13104, 125)
    earlier = events[2, frozenset((0, 2, 3))]
    later = events[2, frozenset((2, 3, 4, 5))]
    assert earlier[0] == Q(1658, 645) < Q(614, 215) == later[0]
    assert earlier[1][2] == Q(239, 645) > Q(47, 129) == later[1][2]
    return {"independent_witness_inequalities": inequality_count,
            "independent_witness_equalities": len(events),
            "nonphysical_allocation_decrease": "passed"}


if __name__ == "__main__":
    print(check())
    print(check_event_witness())
