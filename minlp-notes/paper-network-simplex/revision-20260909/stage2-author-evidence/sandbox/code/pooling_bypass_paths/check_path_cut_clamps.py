"""Exact binary path energies versus prefix-clamp recovery."""
from fractions import Fraction as F
from itertools import product
from random import Random


def solve(unary, forward, backward):
    p = unary[0][1]-unary[0][0]
    z, e0 = F(0), unary[0][0]
    candidates = {F(0)}
    for i in range(1, len(unary)):
        lo, hi = -backward[i-1]-p, forward[i-1]-p
        assert lo <= hi
        e0 += unary[i][0]+min(F(0), z+p+backward[i-1])
        candidates.update((lo, hi))
        z = max(lo, min(z, hi))
        assert z in candidates
        p += unary[i][1]-unary[i][0]
    return e0+min(F(0), z+p)


def brute(unary, forward, backward):
    values = []
    for bits in product((0, 1), repeat=len(unary)):
        cost = sum(unary[i][x] for i, x in enumerate(bits))
        for i in range(1, len(bits)):
            if bits[i-1:i+1] == (0, 1):
                cost += forward[i-1]
            elif bits[i-1:i+1] == (1, 0):
                cost += backward[i-1]
        values.append(cost)
    return min(values)


def main():
    rng = Random(261904)
    count = 0
    for n in range(1, 10):
        for case in range(40):
            # Rational samples of quadratic parameter data, with nonnegative
            # edge penalties and unrestricted signed unary costs.
            q = F(rng.randrange(-8, 9), 5)
            unary = [(F(rng.randrange(-5, 6))+q*rng.randrange(-3, 4)+q*q*rng.randrange(-2, 3),
                      F(rng.randrange(-5, 6))+q*rng.randrange(-3, 4)+q*q*rng.randrange(-2, 3))
                     for _ in range(n)]
            forward = [F(rng.randrange(4))+(q-rng.randrange(-2, 3))**2 for _ in range(n-1)]
            backward = [F(rng.randrange(4))+(q-rng.randrange(-2, 3))**2 for _ in range(n-1)]
            assert solve(unary, forward, backward) == brute(unary, forward, backward)
            count += 1
    print(f'PASS: {count} exact path energy/clamp comparisons, each versus all binary labelings.')


if __name__ == '__main__':
    main()
