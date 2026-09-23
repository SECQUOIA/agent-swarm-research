"""Exact finite proof that five unit cells and three modes need <=2 switches
for cumulative error <=1.

Enumerate generic chambers determined by the integer parts of every cumulative
allocation. Integral prefix-flow rounding implies the pruning rule in this file;
see notes/cia-reopened-small-grid-boundary.md. No solver or saved certificate is
used. Integer arithmetic proves every retained chamber has a valid schedule.
"""
from collections import Counter
from itertools import product

MODES = 3
CELLS = 5
BUDGET = 2


def prefix_counts(word):
    counts = [0] * MODES
    result = []
    for mode in word:
        counts[mode] += 1
        result.append(tuple(counts))
    return tuple(result)


def switch_count(word):
    return sum(a != b for a, b in zip(word, word[1:]))


def prove():
    words = tuple(product(range(MODES), repeat=CELLS))
    prefixes = tuple(prefix_counts(word) for word in words)
    switches = tuple(switch_count(word) for word in words)
    # Generic prefix values have three fractional parts strictly in (0,1).
    # Their integer parts consequently sum to k-1 or k-2 at prefix k.
    possible_floors = tuple(
        tuple(v for v in product(range(k + 1), repeat=MODES)
              if sum(v) in (k - 1, k - 2))
        for k in range(1, CELLS + 1)
    )
    statistics = Counter()
    leaves_by_minimum_switches = Counter()

    def visit(depth, available, history):
        statistics[f'accepted_depth_{depth}'] += 1
        if depth == CELLS:
            best = min(switches[index] for index in available)
            assert best <= BUDGET, (history, available)
            leaves_by_minimum_switches[best] += 1
            statistics['verified_chambers'] += 1
            return
        for floor in possible_floors[depth]:
            retained = tuple(index for index in available
                             if all(floor[i] <= prefixes[index][depth][i]
                                    <= floor[i] + 1 for i in range(MODES)))
            if not retained:
                statistics['empty_word_prunes'] += 1
                continue
            extended = history + (floor,)
            # A strict interior profile is a convex combination of these words.
            # Each cumulative coordinate strictly between b and b+1 therefore
            # requires at least one vertex at EACH of its two integer endpoints.
            if any({prefixes[index][time][mode] for index in retained}
                   != {earlier_floor[mode], earlier_floor[mode] + 1}
                   for time, earlier_floor in enumerate(extended)
                   for mode in range(MODES)):
                statistics['missing_endpoint_prunes'] += 1
                continue
            visit(depth + 1, retained, extended)

    visit(0, tuple(range(len(words))), ())
    assert statistics['verified_chambers'] == 396
    # An alternating pure profile needs four switches for zero discrepancy.
    # Its discrepancy against every integer word is an integer at each prefix.
    witness = (0, 1, 0, 1, 0)
    target = prefix_counts(witness)
    feasible = [index for index in range(len(words)) if switches[index] <= BUDGET]
    errors = [max(abs(target[t][i] - prefixes[index][t][i])
                  for t in range(CELLS) for i in range(MODES))
              for index in feasible]
    assert min(errors) == 1
    assert switch_count(witness) == 4
    return {
        'modes': MODES, 'cells': CELLS, 'switch_budget': BUDGET,
        'integer_words': len(words),
        'chambers_by_minimum_switches': dict(sorted(leaves_by_minimum_switches.items())),
        'statistics': dict(sorted(statistics.items())),
        'exact_worst_case_error': 1,
    }


if __name__ == '__main__':
    print(prove())
