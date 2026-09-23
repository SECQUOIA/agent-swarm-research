"""Exact coefficient checks for completed-mode bounds seeded at four blocks.

This file does not prove the general distinct-mode reach conjecture.  All checks
use fractions; no numerical solver or floating-point tolerances are involved.
"""
from fractions import Fraction as Q


def uniform_lower(n: int, k: int) -> Q:
    return 1 / (n * ((Q(n, n - 1)) ** k - 1))


def old_upper(n: int, k: int) -> Q:
    return Q(n * (n - 1) + (n - k) * (n - k - 1), n * k * (2 * n - k - 1))


def transfer(n: int, c: Q) -> Q:
    assert n >= 3 and c > 0
    return ((n - 1) ** 2 * c + 1) / (n * (n - 1) * (1 + c))


def seeded_upper(n: int, k: int, seed: int = 4, *, clipped: bool = True) -> Q:
    assert 1 <= seed <= k < n
    m = n - k + seed
    seed_eta = 2 * Q(m - 1, m) ** seed - 1
    eta = Q(m * (m - 1), n * (n - 1)) * (max(Q(0), seed_eta) if clipped else seed_eta)
    return (1 + eta) / (n * (1 - eta))


def verify(limit: int = 120) -> dict:
    cases = 0
    for n in range(5, limit + 1):
        for k in range(4, n):
            m = n - k + 4
            c = max(Q(1, m), uniform_lower(m, 4))
            for size in range(m + 1, n + 1):
                c = transfer(size, c)
            assert c == seeded_upper(n, k)
            assert Q(1, n) <= c <= old_upper(n, k)
            assert c >= uniform_lower(n, k)
            raw = uniform_lower(m, 4)
            for size in range(m + 1, n + 1):
                raw = transfer(size, raw)
            assert raw == seeded_upper(n, k, clipped=False)
            assert uniform_lower(n, k) <= raw <= c
            if n >= k + 2:
                assert c < old_upper(n, k)
            cases += 1
    assert seeded_upper(16, 5) <= Q(1, 6)
    assert old_upper(16, 5) > Q(1, 6)
    assert seeded_upper(17, 5) > Q(1, 6)
    return {'coefficient_cases': cases,
            'new_16_mode_4_switch_upper': str(seeded_upper(16, 5)),
            'old_16_mode_4_switch_upper': str(old_upper(16, 5)),
            'target': '1/6'}


def weighted_triple_relaxation():
    """Necessary event-inclusion constraints; not a characterization of controls.

    Fixed case n=6, distinguished S={0,1,2,3}, minimum first-reach index 0,
    global maximizing pair {0,1}, global maximizing triple {0,1,2}.
    Returns integer rows (dictionary, RHS) and an integer objective dictionary.
    """
    from itertools import combinations
    n = 6
    modes = frozenset(range(n))
    distinguished = frozenset(range(4))
    pair, triple = frozenset((0, 1)), frozenset((0, 1, 2))
    events = [(h, frozenset(u)) for h in (2, 3) for d in range(6 - h)
              for u in combinations(range(n), n - d) if n - d >= h]
    indices = {ev: i for i, ev in enumerate(events)}
    size = n + len(events) * (n + 1)

    def time(ev):
        return n + indices[ev] * (n + 1)

    def allocation(ev, i):
        return time(ev) + 1 + i

    inequalities = [({0: 1, i: -1}, 0) for i in range(1, n)]
    inequalities += [({i: -1 for i in range(1, n)}, -n)]
    inequalities += [({i: -1}, -1) for i in modes]
    equalities = []
    for ev in events:
        h, available = ev
        equalities.append(({time(ev): -1,
                            **{allocation(ev, i): 1 for i in modes}}, 0))
        for i in available:
            inequalities.append(({i: 1, allocation(ev, i): -1}, 1))
            if h == 2:
                for j in available - {i}:
                    inequalities.append(({j: 1, time(ev): -1,
                                          allocation(ev, i): 1}, -1))
            else:
                previous = (2, available - {i})
                inequalities.append(({time(previous): 1, time(ev): -1,
                                      allocation(ev, i): 1}, -1))
        for later in events:
            hh, larger = later
            if h <= hh and available <= larger and ev != later:
                for i in modes:
                    inequalities.append(({allocation(ev, i): 1,
                                          allocation(later, i): -1}, 0))
        maximizer = pair if h == 2 else triple
        if maximizer <= available and available != modes:
            for i in modes:
                inequalities.append(({allocation((h, modes), i): 1,
                                      allocation(ev, i): -1}, 0))
    objective = {}
    for i in distinguished:
        index = time((3, modes - {i}))
        objective[index] = objective.get(index, 0) + 1
        for j in modes - {i}:
            index = time((3, modes - {i, j}))
            objective[index] = objective.get(index, 0) + 1
    return size, inequalities, equalities, objective


def verify_relaxation_witness():
    """Verify a counterexample to sufficiency of these necessary constraints."""
    import json
    from pathlib import Path
    certificate = Path(__file__).with_name('general_reach_relaxation_witness.json')
    raw = json.loads(certificate.read_text())
    x = [Q(v) for v in raw['variables']]
    size, inequalities, equalities, objective = weighted_triple_relaxation()
    assert len(x) == size and all(v >= 0 for v in x)
    for row, rhs in inequalities:
        assert sum(value * x[index] for index, value in row.items()) <= rhs
    for row, rhs in equalities:
        assert sum(value * x[index] for index, value in row.items()) == rhs
    actual = sum(value * x[index] for index, value in objective.items())
    target = 4 * 6 * 6 * (Q(6, 5) ** 3 - 1)
    assert actual == Q(40328, 387) < target == Q(13104, 125)
    return {'variables': size, 'inequalities': len(inequalities),
            'equalities': len(equalities), 'witness_objective': str(actual),
            'conjectured_target': str(target)}


if __name__ == '__main__':
    print(verify())
    print(verify_relaxation_witness())
