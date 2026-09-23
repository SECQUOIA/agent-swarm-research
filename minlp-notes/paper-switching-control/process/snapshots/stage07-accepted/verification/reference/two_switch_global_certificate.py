"""Exact rational checks of the global two-switch CIA upper bound."""
from fractions import Fraction as F
from random import Random
from collections import Counter
from two_switch_equal_mass_certificate import integral, reach, direct_error


def bound(n):
    return max(F(1, 4), F((n - 1) ** 3,
                         3 * n ** 3 - 3 * n ** 2 - 5 * n + 4))


def construct(a):
    n = len(a)
    masses = [integral(row, F(1)) for row in a]
    order = sorted(range(n), key=lambda i: masses[i], reverse=True)
    quarter = F(1, 4)
    heavy = [i for i in order if masses[i] > quarter]
    if heavy:
        q = order[0]
        if masses[q] >= F(1, 2):
            p = next((i for i in heavy if i != q), next(i for i in range(n) if i != q))
            return (p, q, q), (quarter, quarter), 'large_total'
        Ahalf = [integral(row, F(1, 2)) for row in a]
        if len(heavy) >= 2:
            q = next(i for i in heavy if Ahalf[i] <= quarter)
            initial = [i for i in heavy if i != q]
            initial += [i for i in range(n) if i != q and i not in initial][:2 - len(initial)]
            return (*initial, q), (quarter, F(1, 2)), 'multiple_heavy'
        h = heavy[0]
        others = [i for i in range(n) if i != h][:2]
        if Ahalf[h] <= quarter:
            return (*others, h), (quarter, F(1, 2)), 'single_heavy_late'
        return (h, *others), (F(1, 2), F(3, 4)), 'single_heavy_early'
    E = bound(n)
    if masses[order[0]] >= 1 - 3 * E:
        final = order[0]
        initial = [i for i in range(n) if i != final][:2]
        return (*initial, final), (E, 2 * E), 'fixed_blocks'
    third = masses[order[2]]
    L = 1 - third - E
    A = [integral(row, L) for row in a]
    R = [reach(row, E, L) for row in a]
    if L in R:
        p = R.index(L)
        r = next(i for i in order[:3] if i != p)
        return (p, r, r), (L, L), 'reach_endpoint'
    p, q = max(((p, q) for p in range(n) for q in range(n) if p != q),
               key=lambda pair: R[pair[0]] + A[pair[1]])
    r = next(i for i in order[:3] if i not in (p, q))
    t1 = max(F(0), L - A[q] - E)
    assert t1 <= R[p]
    return (p, q, r), (t1, L), 'reach_pair'


def verify():
    rng = Random(230904)
    branches = Counter()
    for n in range(4, 16):
        for N in range(1, 16):
            for _ in range(8):
                columns = []
                for j in range(N):
                    if rng.random() < .6:
                        col = [0] * n
                        col[rng.randrange(n)] = 1
                    else:
                        col = [rng.randrange(10) for i in range(n)]
                        if not sum(col):
                            col[0] = 1
                    columns.append(col)
                a = [[F(c[i], sum(c)) for c in columns] for i in range(n)]
                modes, times, branch = construct(a)
                actual = direct_error(a, modes, times)
                assert actual <= bound(n), (n, N, branch, actual, bound(n))
                if any(integral(row, F(1)) > F(1, 4) for row in a):
                    assert actual <= F(1, 4)
                branches[branch] += 1
    for n in (4, 5, 6):
        a = [[F(int(i == j)) for j in range(4)] for i in range(n)]
        modes, times, _ = construct(a)
        assert direct_error(a, modes, times) == bound(n) == F(1, 4)
    assert all(branches[b] > 0 for b in ('large_total', 'multiple_heavy',
                                        'single_heavy_late', 'single_heavy_early',
                                        'reach_pair'))
    print(f'Global two-switch bound: {sum(branches.values())} rational profiles passed; branches {dict(branches)}.')


if __name__ == '__main__':
    verify()
