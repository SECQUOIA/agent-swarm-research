"""Exact rational checks of the complete continuous two-switch theorem.

The proof is analytic; this script independently evaluates its constructive
reach schedules at every original grid endpoint and every switch.
"""
from fractions import Fraction as F
from random import Random
from collections import Counter
from two_switch_equal_mass_certificate import integral, reach, direct_error
from two_switch_global_certificate import construct as previous_construction


def exact_bound(n):
    return max(F(1, 4), F((n - 1) ** 3, n * (3 * n * n - 3 * n + 1)))


def prefix_construct(a, E):
    n = len(a)
    R = [reach(row, E, F(1)) for row in a]
    if F(1) in R:
        p = R.index(F(1))
        return (p, p, p), (F(1), F(1))
    pairs = {(p, q): reach(a[q], R[p] + E, F(1))
             for p in range(n) for q in range(n) if p != q}
    p, q = max(pairs, key=pairs.get)
    if pairs[p, q] == 1:
        return (p, q, q), (R[p], F(1))
    global_pair = p, q
    for r in range(n):
        if r not in global_pair:
            p, q = global_pair
        else:
            p, q = max((pair for pair in pairs if r not in pair), key=pairs.get)
        end = reach(a[r], pairs[p, q] + E, F(1))
        if end == 1:
            return (p, q, r), (R[p], pairs[p, q])
    raise AssertionError('Distinct-mode reach theorem did not reach the horizon')


def construct(a):
    if max(integral(row, F(1)) for row in a) > F(1, 4):
        modes, times, branch = previous_construction(a)
        return modes, times, branch
    modes, times = prefix_construct(a, exact_bound(len(a)))
    return modes, times, 'prefix_three'


def negative_error(a, modes, times):
    n, N = len(a), len(a[0])
    p, q, r = modes
    t1, t2 = times
    err = F(0)
    for t in sorted(set([F(k, N) for k in range(N + 1)] + [t1, t2])):
        C = [F(0)] * n
        C[p] += min(t, t1)
        C[q] += max(F(0), min(t, t2) - t1)
        C[r] += max(F(0), t - t2)
        err = max(err, *(C[i] - integral(row, t) for i, row in enumerate(a)))
    return err


def verify():
    rng = Random(309204)
    branches = Counter()
    prefix_count = 0
    for n in range(4, 16):
        Eprefix = F((n - 1) ** 3, n * (3 * n * n - 3 * n + 1))
        for N in range(1, 11):
            for trial in range(4):
                cols = []
                for _ in range(N):
                    if rng.random() < .5:
                        c = [0] * n
                        c[rng.randrange(n)] = 1
                    else:
                        c = [rng.randrange(10) for _ in range(n)]
                        if not sum(c):
                            c[0] = 1
                    cols.append(c)
                a = [[F(c[i], sum(c)) for c in cols] for i in range(n)]
                modes, times = prefix_construct(a, Eprefix)
                assert negative_error(a, modes, times) <= Eprefix
                prefix_count += 1
                modes, times, branch = construct(a)
                assert direct_error(a, modes, times) <= exact_bound(n)
                branches[branch] += 1
        if n <= 7:
            a = [[F(int(i == j)) for j in range(4)] for i in range(n)]
        else:
            a = [[F(1, n)] for i in range(n)]
        modes, times, _ = construct(a)
        assert direct_error(a, modes, times) == exact_bound(n)
    print(f'Exact two-switch theorem: {prefix_count} arbitrary-total negative-reach checks; '
          f'{sum(branches.values())} full-error checks; 12 sharp constructions. Branches {dict(branches)}.')


if __name__ == '__main__':
    verify()
