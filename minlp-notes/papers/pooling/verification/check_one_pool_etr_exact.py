"""Independent rational witnesses checked in the original one-pool equations.

This implementation does not import the historical builder or an optimizer.
Tuple identifiers keep normalization variables distinct from original names.
The checks supplement, and do not prove, the reduction theorem.
"""

from fractions import Fraction as F
from random import Random


def verify(values, equations):
    values = {('original', key): F(value) for key, value in values.items()}
    equations = [tuple([row[0]] + [('original', v) for v in row[1:]])
                 for row in equations]
    normalized = []
    for number, row in enumerate(equations):
        if row[0] == 'add' and row[1] == row[2]:
            _, x, _, z = row
            u, copy = ('inverse', number), ('copy', number)
            values[u], values[copy] = 1/values[x], values[x]
            normalized.extend([('inv', x, u), ('inv', u, copy),
                               ('add', x, copy, z)])
        else:
            normalized.append(row)
    assert values  # Empty formulas can first append a uniquely fixed variable.
    assert all(F(1, 2) <= value <= 2 for value in values.values())
    for row in normalized:
        if row[0] == 'inv':
            assert values[row[1]]*values[row[2]] == 1
        else:
            assert values[row[1]]+values[row[2]] == values[row[3]]

    feeds = {('variable', v): value for v, value in values.items()}
    qualities = {('coordinate', s): {s: F(1)} for s in feeds}
    auxiliary = []
    pins = {}
    covered = set()

    def add_auxiliary(value):
        source = ('auxiliary', len(auxiliary))
        feeds[source] = F(value)
        auxiliary.append(source)
        qualities[('coordinate', source)] = {source: F(1)}
        pins[source] = {}
        return source

    def variable_attribute(v):
        return ('coordinate', ('variable', v))

    for number, row in enumerate(normalized):
        if row[0] == 'inv':
            _, x, y = row
            first = add_auxiliary(values[y])
            second = add_auxiliary(1/values[y])
            pins[first][variable_attribute(x)] = F(1)
            pins[second][('coordinate', first)] = F(1)
            pins[second][variable_attribute(y)] = F(1)
            covered.update((x, y))
        else:
            _, x, y, z = row
            assert x != y
            source = add_auxiliary(2/values[z])
            attribute = ('sum', number)
            qualities[attribute] = {('variable', x): F(1),
                                   ('variable', y): F(1)}
            pins[source][variable_attribute(z)] = F(2)
            pins[source][attribute] = F(2)
    for v in values.keys()-covered:
        source = add_auxiliary(1/values[v])
        pins[source][variable_attribute(v)] = F(1)

    capacity = F(4*len(feeds))
    filler = capacity-sum(feeds.values())
    slack = capacity-sum(feeds[s] for s in auxiliary)
    assert 0 <= filler <= capacity and 0 <= slack <= capacity
    assert all(0 <= value <= 2 for value in feeds.values())
    pool_quality = {a: sum(q.get(s, 0)*v for s, v in feeds.items())/capacity
                    for a, q in qualities.items()}
    assert sum(feeds.values())+filler == capacity
    assert sum(feeds[s] for s in auxiliary)+slack == capacity

    # Source, pool, terminal, quality and objective checks use physical flows.
    profit_from_arcs = F(0)
    for source in auxiliary:
        feed = feeds[source]
        bypass, outlet = 2-feed, feed
        assert feed+bypass == 2 and outlet+bypass == 2
        assert min(feed, bypass, outlet) >= 0
        # Forced auxiliary source (feed), source+terminal (bypass),
        # and pool+terminal (outlet) are the three arc coefficients.
        profit_from_arcs += feed + 2*bypass + 2*outlet
        for attribute, q in qualities.items():
            mass = pool_quality[attribute]*outlet + q.get(source, 0)*bypass
            if attribute in pins[source]:
                assert q.get(source, 0) == 0
                bound = pins[source][attribute]/(2*capacity)
                assert mass == bound*(outlet+bypass)
            else:
                assert 0 <= mass <= outlet+bypass
    profit_from_arcs += slack  # Forced pool, unforced slack terminal.
    assert profit_from_arcs == capacity+4*len(auxiliary)
    assert all(0 <= q*slack <= slack for q in pool_quality.values())
    return len(normalized), len(auxiliary), len(qualities)


def main():
    cases = [
        ({'x': 1}, [('inv', 'x', 'x')]),
        ({'x': F(1, 2), 'y': 1, 'z': 2},
         [('add', 'x', 'x', 'y'), ('add', 'y', 'y', 'z')]),
        ({'u0': F(1, 2), 'u0copy0': 1, 'unused': F(3, 4)},
         [('add', 'u0', 'u0', 'u0copy0')]),
        ({'a': F(1, 2), 'b': 2}, []),
    ]
    rng = Random(20260905)
    grid = [F(1, 2), F(2, 3), F(3, 4), F(1), F(5, 4),
            F(4, 3), F(3, 2), F(2)]
    for _ in range(100):
        values = {f'v{i}': rng.choice(grid) for i in range(rng.randint(2, 8))}
        candidates = []
        for x in values:
            for y in values:
                if values[x]*values[y] == 1:
                    candidates.append(('inv', x, y))
                for z in values:
                    if values[x]+values[y] == values[z]:
                        candidates.append(('add', x, y, z))
        equations = rng.sample(candidates, min(len(candidates), 18))
        cases.append((values, equations))
    totals = [verify(values, equations) for values, equations in cases]
    print(f'PASS: {len(cases)} independent exact physical one-pool witnesses; '
          f'{sum(t[0] for t in totals)} normalized equations, '
          f'{sum(t[1] for t in totals)} pinned terminals, '
          'including repeated summands, boundary values, unused variables, '
          'and collision-prone original names.')


if __name__ == '__main__':
    main()
