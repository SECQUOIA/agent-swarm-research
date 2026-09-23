"""Exact rational checks of the saturated-margin repair and penalty lemma.

Run with Python 3; no third-party dependencies. These checks supplement the proof.
"""
from fractions import Fraction as Q
from random import Random


def outer(r, c, total):
    return [[a*b/total for b in c] for a in r]


def margins(w):
    return [sum(row) for row in w], [sum(col) for col in zip(*w)]


def repair(w):
    r, c = margins(w)
    total = sum(r)
    if total < 1:
        return [[Q(i == 0 and j == 0) for j in range(len(c))]
                for i in range(len(r))]
    for v in (r, c):
        deficit = 1-v[0]
        v[0] = Q(1)
        for i in range(1, len(v)):
            take = min(deficit, v[i])
            v[i] -= take
            deficit -= take
        assert deficit == 0
    return outer(r, c, total)


def dot(a, b):
    return sum(x*y for ar, br in zip(a, b) for x, y in zip(ar, br))


def check(w, rng):
    r, c = margins(w)
    repaired = repair(w)
    rr, cc = margins(repaired)
    assert rr[0] == cc[0] == 1
    assert all(0 <= v <= 1 for v in rr + cc)
    assert all(repaired[i][j]*repaired[0][0] ==
               repaired[i][0]*repaired[0][j]
               for i in range(len(r)) for j in range(len(c)))
    delta = 2-r[0]-c[0]
    distance = sum(abs(a-b) for row, row2 in zip(w, repaired)
                   for a, b in zip(row, row2))
    assert distance <= 2*delta, (w, repaired, distance, delta)
    cost = [[rng.randint(-12, 12) for _ in c] for _ in r]
    big = max(abs(v) for row in cost for v in row)
    penalty = 2*big+1
    change = dot(cost, repaired)-dot(cost, w)-penalty*delta
    assert change <= -delta
    return int(sum(r) < 1), int(sum(r) == 1), int(sum(r) > 1)


def main():
    rng = Random(20260904)
    counts = [0, 0, 0]
    for trial in range(2000):
        p, q = rng.randint(1, 7), rng.randint(1, 7)
        x = [rng.randint(0, 20) for _ in range(p)]
        y = [rng.randint(0, 20) for _ in range(q)]
        denominator = max(max(x)*sum(y), max(y)*sum(x))
        if denominator == 0:
            w = [[Q(0) for _ in y] for _ in x]
        else:
            # Include the capacity boundary and small-total regimes.
            scale = Q(1) if trial % 3 == 0 else Q(1, rng.randint(1, 12))
            w = [[scale*Q(a*b, denominator) for b in y] for a in x]
        for i, value in enumerate(check(w, rng)):
            counts[i] += value
    print('PASS: 2000 exact rational repairs and objective-penalty checks')
    print(f'Total-flow regimes S<1, S=1, S>1: {counts}')


if __name__ == '__main__':
    main()
