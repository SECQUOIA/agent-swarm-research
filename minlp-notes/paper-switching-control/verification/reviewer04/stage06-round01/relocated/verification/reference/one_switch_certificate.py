"""Exact rational validation of the full one-switch worst-case theorem.

The construction works for piecewise-constant relaxed controls on unit intervals.
It returns a continuous switching time. Validation computes all discrepancies at
all grid endpoints and at the switch, independently of the proof's reduction.
"""
from fractions import Fraction as F
from random import Random


def bound(n, T):
    if n < 3:
        raise ValueError('The theorem requires n >= 3')
    return T * max(F(1, 3), F((n - 1) ** 2, n * (2 * n - 1)))


def integrals(a, t):
    whole = int(t)
    frac = t - whole
    return [sum(row[:whole], F(0)) + (frac * row[whole] if whole < len(row) else 0)
            for row in a]


def construct(a):
    n, T = len(a), len(a[0])
    E = bound(n, T)
    totals = integrals(a, T)
    order = sorted(range(n), key=lambda i: totals[i], reverse=True)
    q, r = order[:2]
    if totals[q] >= E:
        return r, q, max(F(0), T - totals[q] - E)
    tq = T - totals[q] - E
    A = integrals(a, tq)
    p = max((i for i in range(n) if i != q), key=lambda i: A[i])
    if tq - A[p] <= E:
        return p, q, tq
    return q, r, T - totals[r] - E


def direct_error(a, p, q, switch):
    T = len(a[0])
    error = F(0)
    for t in sorted(set([F(k) for k in range(T + 1)] + [switch])):
        A = integrals(a, t)
        for i in range(len(a)):
            occupation = min(t, switch) * (i == p) + max(F(0), t - switch) * (i == q)
            error = max(error, abs(A[i] - occupation))
    return error


def verify():
    rng = Random(20260904)
    count = 0
    for n in range(3, 16):
        for T in range(1, 21):
            for trial in range(8):
                a = [[] for _ in range(n)]
                for _ in range(T):
                    col = [rng.randrange(20) for _ in range(n)]
                    if not sum(col):
                        col[0] = 1
                    total = sum(col)
                    for i in range(n):
                        a[i].append(F(col[i], total))
                p, q, switch = construct(a)
                assert direct_error(a, p, q, switch) <= bound(n, T), (n, T, trial)
                # Round the sole switch to the nearest unit-grid endpoint.
                rounded = F((2 * switch.numerator + switch.denominator) // (2 * switch.denominator))
                assert direct_error(a, p, q, rounded) <= bound(n, T) + F(1, 2)
                count += 1
    # Both sharpness mechanisms, including their transition at n=5.
    for n in range(3, 16):
        if n <= 4:
            a = [[F(int(i == k)) for k in range(3)] for i in range(n)]
        else:
            a = [[F(1, n)] for _ in range(n)]
        p, q, switch = construct(a)
        assert direct_error(a, p, q, switch) == bound(n, len(a[0]))
    print(f'One-switch construction and half-grid bound: {count} rational instances; '
          '13 extremal constructions attain the theorem.')


if __name__ == '__main__':
    verify()
