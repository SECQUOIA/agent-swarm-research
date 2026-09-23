"""Exact rational checks of the two-switch equal-mode-totals theorem."""
from fractions import Fraction as F
from random import Random


def bound(n):
    r = F(n, n - 1)
    return max(F(1, n), 1 / (n * (r ** 3 - 1)))


def integral(row, t):
    N = len(row)
    u = N * t
    k = min(int(u), N)
    return sum(row[:k], F(0)) / N + (row[k] * (u - k) / N if k < N else 0)


def reach(row, E, L):
    if L - integral(row, L) <= E:
        return L
    N = len(row)
    previous_t = F(0)
    previous_F = F(0)
    for k in range(N):
        t = min(F(k + 1, N), L)
        Ft = t - integral(row, t)
        if Ft > E:
            return previous_t + (E - previous_F) / (1 - row[k])
        previous_t, previous_F = t, Ft
    raise AssertionError('A crossing must exist')


def construct(a):
    n = len(a)
    E = bound(n)
    L = 1 - F(1, n) - E
    A = [integral(row, L) for row in a]
    R = [reach(row, E, L) for row in a]
    if L in R:
        p = R.index(L)
        q = next(i for i in range(n) if i != p)
        return (p, q, q), (L, L)
    p, q = max(((p, q) for p in range(n) for q in range(n) if p != q),
               key=lambda pair: R[pair[0]] + A[pair[1]])
    r = next(i for i in range(n) if i not in (p, q))
    t1 = max(F(0), L - A[q] - E)
    assert t1 <= R[p]
    return (p, q, r), (t1, L)


def direct_error(a, modes, switches):
    n, N = len(a), len(a[0])
    p, q, r = modes
    t1, t2 = switches
    error = F(0)
    for t in sorted(set([F(k, N) for k in range(N + 1)] + [t1, t2])):
        occupation = [F(0)] * n
        occupation[p] += min(t, t1)
        occupation[q] += max(F(0), min(t, t2) - t1)
        occupation[r] += max(F(0), t - t2)
        for i, row in enumerate(a):
            error = max(error, abs(integral(row, t) - occupation[i]))
    return error


def verify():
    rng = Random(720904)
    count = 0
    for n in range(4, 16):
        for N in range(2, 13):
            for trial in range(6):
                weights = [[20] * N for _ in range(n)]
                for _ in range(100):
                    i, ip = rng.sample(range(n), 2)
                    j, jp = rng.sample(range(N), 2)
                    delta = rng.randint(-min(weights[i][j], weights[ip][jp]),
                                        min(weights[ip][j], weights[i][jp]))
                    weights[i][j] += delta
                    weights[ip][jp] += delta
                    weights[ip][j] -= delta
                    weights[i][jp] -= delta
                a = [[F(x, 20 * n) for x in row] for row in weights]
                assert all(sum(row, F(0)) == F(N, n) for row in a)
                assert all(sum(a[i][j] for i in range(n)) == 1 for j in range(N))
                modes, times = construct(a)
                assert direct_error(a, modes, times) <= bound(n), (n, N, trial)
                count += 1
        uniform = [[F(1, n)]] * n
        modes, times = construct(uniform)
        assert direct_error(uniform, modes, times) == bound(n)
    print(f'Equal-total two-switch theorem: {count} exact rational profiles and 12 sharp uniform profiles passed.')


if __name__ == '__main__':
    verify()
