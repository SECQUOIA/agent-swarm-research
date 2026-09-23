"""Independent exact audit of F(3 modes, 5 unit cells, 2 switches) = 1.

Uses a flat enumeration of all 14,400 floor histories and integer bit masks.
Does not import the author's recursive enumerator or use a numerical solver.
See notes/review-cia-reopened-small-grid.md for the completeness argument.
"""
from collections import Counter
from itertools import product


def compositions(total):
    if total >= 0:
        for first in range(total + 1):
            for second in range(total - first + 1):
                yield (first, second, total - first - second)


def prefix_vector(word):
    return tuple(tuple(word[:k].count(mode) for mode in range(3))
                 for k in range(1, 6))


def main():
    words = tuple(product(range(3), repeat=5))
    prefixes = tuple(map(prefix_vector, words))
    switches = tuple(sum(word[j] != word[j-1] for j in range(1, 5))
                     for word in words)
    all_words = (1 << len(words)) - 1
    budget_masks = [sum(1 << j for j, switch in enumerate(switches)
                        if switch <= budget) for budget in range(5)]
    floors = [tuple(compositions(k-1)) + tuple(compositions(k-2))
              for k in range(1, 6)]
    assert list(map(len, floors)) == [1, 4, 9, 16, 25]
    allowed = {}
    endpoints = {}
    for time in range(5):
        for floor in floors[time]:
            allowed[time, floor] = sum(
                1 << index for index, counts in enumerate(prefixes)
                if all(floor[i] <= counts[time][i] <= floor[i] + 1
                       for i in range(3)))
            for mode in range(3):
                for side in range(2):
                    endpoints[time, floor, mode, side] = sum(
                        1 << index for index, counts in enumerate(prefixes)
                        if counts[time][mode] == floor[mode] + side)

    statistics = Counter()
    minimum_switches = Counter()
    for history in product(*floors):
        statistics['floor_histories'] += 1
        mask = all_words
        for time, floor in enumerate(history):
            mask &= allowed[time, floor]
        if mask == 0:
            statistics['no_integral_vertex'] += 1
            continue
        if any(not (mask & endpoints[time, floor, mode, side])
               for time, floor in enumerate(history)
               for mode in range(3) for side in range(2)):
            statistics['no_strict_interior'] += 1
            continue
        statistics['strict_chambers'] += 1
        assert mask & budget_masks[2], history
        minimum_switches[next(budget for budget in range(5)
                              if mask & budget_masks[budget])] += 1
        # Pick a certified schedule and independently test the *whole* closed
        # floor box. Its integer counts must lie within 1 of both endpoints.
        chosen = (mask & budget_masks[2] & -(mask & budget_masks[2])).bit_length()-1
        for time, floor in enumerate(history):
            for mode in range(3):
                assert max(abs(prefixes[chosen][time][mode] - floor[mode]),
                           abs(prefixes[chosen][time][mode] - floor[mode] - 1)) <= 1

    assert statistics['floor_histories'] == 14400
    assert statistics['strict_chambers'] == 396
    assert minimum_switches == {0: 3, 1: 138, 2: 255}
    target = prefix_vector((0, 1, 0, 1, 0))
    errors = [max(abs(counts[time][mode]-target[time][mode])
                  for time in range(5) for mode in range(3))
              for counts, switch in zip(prefixes, switches) if switch <= 2]
    assert len(errors) == 99
    assert min(errors) == 1
    print(dict(statistics))
    print('Minimum switches per strict chamber:', dict(sorted(minimum_switches.items())))
    print('Direct witness check:', len(errors), 'feasible schedules, minimum error 1')
    print('Independent integer-only verification passed.')


if __name__ == '__main__':
    main()
