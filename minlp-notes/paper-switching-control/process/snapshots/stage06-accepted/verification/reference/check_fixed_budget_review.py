"""Independent checks of fixed-budget CIA subset assignment.

The oracle explicitly enumerates grid schedules and integrates discrepancy at
all microinterval endpoints, including changes of relaxed control inside cells.
It does not use the tested implementation's role-cost or recurrence formula.
Run: python3 code/cia_reopened/check_fixed_budget_review.py
"""
from fractions import Fraction as Q
from itertools import combinations, groupby, permutations, product
from random import Random

from rounding import optimal_block_assignment, optimal_few_switches


def changes(word):
    return sum(a != b for a, b in zip(word, word[1:]))


def micro_error(microcells, schedule, n):
    discrepancy = [Q(0)]*n
    error = Q(0)
    for microcell, active in zip(microcells, schedule):
        for dt, rates in microcell:
            for i in range(n):
                discrepancy[i] += dt*(rates[i]-int(i == active))
                error = max(error, abs(discrepancy[i]))
    return error


def aggregate(microcells, n):
    durations = [sum(dt for dt, _ in cell) for cell in microcells]
    rows = [[sum(dt*rates[i] for dt, rates in cell) for i in range(n)]
            for cell in microcells]
    return rows, durations


def verify(microcells, n):
    N = len(microcells)
    rows, dt = aggregate(microcells, n)
    schedules = [(word, micro_error(microcells, word, n))
                 for word in product(range(n), repeat=N)]
    budgets = partitions = 0
    for s in range(N+2):
        optimum = min(value for word, value in schedules if changes(word) <= s)
        result = optimal_few_switches(rows, dt, s)
        assert result.error == optimum == micro_error(microcells, result.schedule(), n)
        assert changes(result.schedule()) <= s
        assert len(result.modes) == min(s+1, N)
        budgets += 1
    for k in range(1, N+1):
        for interior in combinations(range(1, N), k-1):
            permitted = set(interior)
            optimum = min(value for word, value in schedules
                          if all(word[j-1] == word[j] or j in permitted for j in range(1, N)))
            boundaries = (0,)+interior+(N,)
            result = optimal_block_assignment(rows, dt, boundaries)
            assert result.boundaries == boundaries
            assert result.error == optimum == micro_error(microcells, result.schedule(), n)
            partitions += 1
    return budgets, partitions


def all_binary_microcontrols():
    count = budgets = partitions = 0
    # All original three-mode words on six half-length microintervals.
    # The optimizer only receives aggregate masses on the three unit cells.
    for original in product(range(3), repeat=6):
        microcells = [[(Q(1, 2), tuple(Q(int(i == original[2*j+r])) for i in range(3)))
                       for r in range(2)] for j in range(3)]
        b, p = verify(microcells, 3)
        budgets += b
        partitions += p
        count += 1
    return count, budgets, partitions


def random_nonuniform_controls():
    rng = Random(890531)
    budgets = partitions = 0
    for _ in range(40):
        n, N = rng.randint(1, 4), rng.randint(1, 5)
        microcells = []
        for _ in range(N):
            cell = []
            for _ in range(rng.randint(1, 3)):
                dt = Q(rng.randint(1, 7), rng.randint(1, 7))
                weights = [rng.randint(0, 5) for _ in range(n)]
                if not any(weights):
                    weights[0] = 1
                cell.append((dt, tuple(Q(x, sum(weights)) for x in weights)))
            microcells.append(cell)
        b, p = verify(microcells, n)
        budgets += b
        partitions += p
    return 40, budgets, partitions


def regressions():
    rows = [[1, 0, 0], [0, 1, 0], [1, 0, 0]]
    result = optimal_few_switches(rows, [1]*3, 2)
    assert result.error == 0 and result.schedule() == (0, 1, 0)
    # Adjacent equal block labels are needed when representing fewer than s switches.
    result = optimal_few_switches([[1, 0]]*4, [1]*4, 2)
    assert result.error == 0 and result.schedule() == (0,)*4 and len(result.modes) == 3
    # An unused positive-total mode still contributes to the bottleneck cost.
    result = optimal_block_assignment([[Q(1, 3)]*3]*2, [1, 1], [0, 1, 2])
    assert result.error == Q(2, 3)
    return 3


def candidate_set_lemma():
    """Check the exchange lemma on general role costs, independent of CIA."""
    rng = Random(58467)
    for _ in range(100):
        n = rng.randint(1, 10)
        d = rng.randint(1, min(n, 3))
        totals = [Q(rng.randint(0, 20), rng.randint(1, 7)) for _ in range(n)]
        costs = [[Q(rng.randint(0, 20), rng.randint(1, 7)) for _ in range(n)]
                 for _ in range(d)]
        candidate = set(sorted(range(n), key=lambda i: (-totals[i], i))[:d])
        for row in costs:
            candidate.update(sorted(range(n), key=lambda i: (row[i], i))[:d])
        def objective(labels):
            used = set(labels)
            return max([costs[r][i] for r, i in enumerate(labels)]
                       + [totals[i] for i in range(n) if i not in used])
        full = min(map(objective, permutations(range(n), d)))
        restricted = min(map(objective, permutations(sorted(candidate), d)))
        assert full == restricted
    return 100


def dwell_checks():
    rng = Random(44820)
    comparisons = infeasible = 0
    for _ in range(50):
        n, N = rng.randint(1, 4), rng.randint(1, 5)
        dt = [Q(rng.randint(1, 4), rng.randint(1, 3)) for _ in range(N)]
        rows = []
        for duration in dt:
            weights = [rng.randint(0, 4) for _ in range(n)]
            if not any(weights):
                weights[0] = 1
            rows.append([duration*Q(x, sum(weights)) for x in weights])
        dwell = [Q(rng.randint(0, 15), rng.randint(1, 3)) for _ in range(n)]
        def eligible(word):
            return all(sum(dt[j] for j, _ in run) >= dwell[mode]
                       for mode, run in groupby(enumerate(word), key=lambda pair: pair[1]))
        cells = [[(duration, tuple(x/duration for x in row))]
                 for row, duration in zip(rows, dt)]
        reference = [(word, micro_error(cells, word, n))
                     for word in product(range(n), repeat=N) if eligible(word)]
        requests = [(s, None) for s in range(N+2)]
        for k in range(1, N+1):
            requests.extend((None, (0,)+p+(N,)) for p in combinations(range(1, N), k-1))
        for s, boundaries in requests:
            if boundaries is None:
                candidates = [(w, e) for w, e in reference if changes(w) <= s]
                result = optimal_few_switches(rows, dt, s, minimum_dwell=dwell)
            else:
                allowed = set(boundaries[1:-1])
                candidates = [(w, e) for w, e in reference
                              if all(w[j-1] == w[j] or j in allowed for j in range(1, N))]
                result = optimal_block_assignment(rows, dt, boundaries, minimum_dwell=dwell)
            comparisons += 1
            if not candidates:
                assert result is None
                infeasible += 1
            else:
                assert result is not None and eligible(result.schedule())
                assert result.error == min(e for _, e in candidates)
                assert result.error == micro_error(cells, result.schedule(), n)
    # Adjacent assigned blocks form one physical dwell run.
    result = optimal_block_assignment([[1, 0]]*2, [1, 1], [0, 1, 2], minimum_dwell=[2, 10])
    assert result.error == 0 and result.schedule() == (0, 0)
    # A mode's separated activations cannot pool their lengths to satisfy dwell.
    result = optimal_few_switches([[1, 0], [0, 1], [1, 0]], [1]*3, 2, minimum_dwell=[2, 1])
    assert result.error == 1
    assert optimal_few_switches([[1]], [1], 0, minimum_dwell=[2]) is None
    for value, error_type in (([-1], ValueError), ([], ValueError), ([1.0], TypeError), ([True], TypeError)):
        try:
            optimal_few_switches([[1]], [1], 0, minimum_dwell=value)
        except error_type:
            pass
        else:
            raise AssertionError(('invalid dwell accepted', value))
    return comparisons, infeasible


if __name__ == '__main__':
    c, b, p = all_binary_microcontrols()
    cr, br, pr = random_nonuniform_controls()
    r = regressions()
    k = candidate_set_lemma()
    dwell, infeasible = dwell_checks()
    print(f'PASS: {c} exhaustive microcontrols and {cr} nonuniform rational controls; '
          f'{b+br} switch-budget comparisons; {p+pr} prescribed partitions; '
          f'{r} structural regressions; {k} general candidate-set checks; '
          f'{dwell} dwell comparisons ({infeasible} infeasible).')
