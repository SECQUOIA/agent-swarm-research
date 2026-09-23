"""Exact-rational constructive checks for the three-switch heavy-mode lemma."""
from collections import Counter
from fractions import Fraction as F
from random import Random
from two_switch_equal_mass_certificate import integral


def deadline(row, E):
    """Latest t in [0,1] such that the cumulative allocation is at most E."""
    N = len(row)
    previous_t = F(0)
    previous_A = F(0)
    for k in range(N):
        t = F(k + 1, N)
        A = integral(row, t)
        if A > E:
            return previous_t + (E - previous_A) / row[k]
        previous_t, previous_A = t, A
    return F(1)


def construct(a):
    n, E = len(a), F(1, 5)
    masses = [integral(row, F(1)) for row in a]
    heavy = [i for i in range(n) if masses[i] > E]
    assert heavy and n >= 4
    q = max(range(n), key=masses.__getitem__)
    if masses[q] >= 3 * E:
        p = next((i for i in heavy if i != q), (q + 1) % n)
        return [(p, F(0), E), (q, E, F(1))], 'large'
    over_two = [i for i in range(n) if masses[i] > 2 * E]
    if len(over_two) <= 1:
        q = over_two[0] if over_two else heavy[0]
        selected = [i for i in heavy if i != q]
        selected += [i for i in range(n) if i != q and i not in selected][:3-len(selected)]
        selected.sort(key=lambda i: deadline(a[i], E))
        dq = deadline(a[q], E)
        ceil_d = -(-dq.numerator * 5 // dq.denominator)
        j = min(3, max(0, ceil_d - 2))
        starts = list(range(j)) + list(range(j + 2, 5))
        blocks = [(i, k * E, (k + 1) * E) for i, k in zip(selected, starts)]
        blocks.append((q, j * E, (j + 2) * E))
        return sorted(blocks, key=lambda b: b[1]), 'edf'
    q, r = sorted(over_two, key=lambda i: deadline(a[i], E))
    tau = max(2 * E, deadline(a[q], E))
    p = next(i for i in range(n) if i not in (q, r))
    return [(p, F(0), tau-2*E), (q, tau-2*E, tau),
            (r, tau, tau+2*E), (p, tau+2*E, F(1))], 'two_large'


def direct_error(a, blocks):
    N = len(a[0])
    endpoints = set(F(k, N) for k in range(N + 1))
    for _, b, e in blocks:
        assert F(0) <= b <= e <= 1
        endpoints.update((b, e))
    assert len(blocks) <= 4
    assert sum(e-b for _, b, e in blocks) == 1
    assert all(blocks[j][2] == blocks[j+1][1] for j in range(len(blocks)-1))
    error = F(0)
    for t in endpoints:
        occupation = [F(0)] * len(a)
        for i, b, e in blocks:
            occupation[i] += max(F(0), min(t, e)-b)
        error = max(error, *(abs(integral(row,t)-occupation[i]) for i,row in enumerate(a)))
    return error


def verify():
    rng = Random(4320904)
    counts = Counter()
    for n in range(4, 13):
        for N in (1, 3, 7, 11):
            for scenario in range(4):
                for _ in range(12):
                    columns = []
                    for j in range(N):
                        weights = [rng.randrange(1, 13) for _ in range(n)]
                        if scenario == 1:
                            weights[0] += 80*n
                        elif scenario == 2:
                            weights[0] += 12*n
                        elif scenario == 3:
                            weights[0] += 100*n
                            weights[1] += 100*n
                        total = sum(weights)
                        columns.append([F(w,total) for w in weights])
                    a = [list(row) for row in zip(*columns)]
                    if max(integral(row, F(1)) for row in a) <= F(1,5):
                        continue
                    blocks, branch = construct(a)
                    assert direct_error(a, blocks) <= F(1,5), (n,N,scenario,a,blocks)
                    counts[branch] += 1
    # Piecewise-pure profiles include exact integer deadlines and flat cumulative portions.
    for N in (5, 10):
        for _ in range(200):
            labels = [rng.randrange(4) for _ in range(N)]
            a = [[F(int(i == label)) for label in labels] for i in range(4)]
            blocks, branch = construct(a)
            assert direct_error(a, blocks) <= F(1,5)
            counts[branch] += 1
    print(f'Three-switch heavy-mode lemma: {sum(counts.values())} rational cases passed; branches {dict(counts)}.')


if __name__ == '__main__':
    verify()
