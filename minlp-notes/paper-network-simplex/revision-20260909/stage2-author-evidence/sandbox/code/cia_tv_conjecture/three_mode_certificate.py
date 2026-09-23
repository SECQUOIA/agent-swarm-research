"""Rational checks of the exact three-mode, one-switch finite-grid theorem."""
from fractions import Fraction as F
from random import Random
from one_switch_certificate import integrals, direct_error


def worst_case(N):
    if N == 1:
        return F(2, 3)
    k, residue = divmod(N, 3)
    return F(k) + (F(0), F(1, 2), F(3, 4))[residue]


def construct(a):
    N = len(a[0])
    if N < 2 or len(a) != 3:
        raise ValueError('Requires three modes and N >= 2')
    totals = integrals(a, N)
    q, r, _ = sorted(range(3), key=lambda i: totals[i], reverse=True)
    E = worst_case(N)
    k, residue = divmod(N, 3)
    if not residue:
        return r, q, F(k)
    L = k + 1
    A = integrals(a, L)
    heavy = [i for i in range(3) if totals[i] > E]
    if len(heavy) == 2:
        p = max(heavy, key=lambda i: A[i])
        return p, next(i for i in heavy if i != p), F(L)
    if totals[q] >= N - E - k:
        return r, q, F(k)
    p = max((i for i in range(3) if i != q), key=lambda i: A[i])
    if A[p] >= L - E:
        return p, q, F(L)
    return q, r, F(L)


def extremizer(N):
    k, residue = divmod(N, 3)
    pure = [[F(int(i == mode)) for i in range(3)] for mode in range(3)]
    cols = [pure[2]] * k
    if residue == 1:
        cols += [[F(1, 2), F(1, 2), F(0)]]
    elif residue == 2:
        cols += [[F(1, 4), F(1, 4), F(1, 2)]]
    cols += [pure[0]] * k + [pure[1]] * k
    if residue == 2:
        cols += [[F(1, 2), F(1, 2), F(0)]]
    return [list(row) for row in zip(*cols)]


def verify():
    rng = Random(9904)
    cases = 0
    for N in range(2, 32):
        a = extremizer(N)
        exact = min(direct_error(a, p, q, F(t))
                    for p in range(3) for q in range(3) if p != q for t in range(N + 1))
        assert exact == worst_case(N), (N, exact)
        for _ in range(40):
            cols = [[rng.randrange(10) for _ in range(3)] for _ in range(N)]
            cols = [c if sum(c) else [1, 0, 0] for c in cols]
            a = [[F(c[i], sum(c)) for c in cols] for i in range(3)]
            p, q, t = construct(a)
            assert direct_error(a, p, q, t) <= worst_case(N)
            cases += 1
    print(f'Three-mode theorem: {cases} rational upper-bound checks; '
          'all one-switch schedules checked on 30 exact extremizers.')


if __name__ == '__main__':
    verify()
