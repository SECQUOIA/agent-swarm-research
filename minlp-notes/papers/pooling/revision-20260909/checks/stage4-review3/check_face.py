"""Independent finite exact checks; these do not certify asymptotic lift bounds."""
from fractions import Fraction as F
from itertools import product
from random import Random


def atom(r, c):
    s = sum(r)
    assert s == sum(c)
    return [[F(a) * F(b) / s if s else F(0) for b in c] for a in r]


def stats(w, m):
    return (sum(map(sum, w)), 1 - sum(w[i][i] for i in range(2*m)),
            sum(w[i][m+i] for i in range(m)))


def distance(w, v):
    return sum(abs(a-b) for row, col in zip(w, v) for a, b in zip(row, col))


def rounding(r, c, m):
    a = [int(x >= F(1, 2)) for x in r]
    for i in range(m):
        if a[i] == a[m+i]:
            a[i], a[m+i] = 1, 0
    return atom(a, a)


count = 0
saved = []
for m in (1, 2):
    groups = {}
    for r in product((F(0), F(1, 3), F(2, 3), F(1)), repeat=2*m):
        groups.setdefault(sum(r), []).append(r)
    for vectors in groups.values():
        for r, c in product(vectors, repeat=2):
            w, v = atom(r, c), rounding(r, c, m)
            t, d, b = stats(w, m)
            assert t <= m + 2*m*b + 4*m*d
            assert distance(w, v) <= 8*m*b + 116*m*d + 5*abs(t-m)
            assert distance(w, v) <= 28*m*b + 156*m*d + 5*(m-t)
            assert stats(v, m) == (m, 0, 0)
            saved.append((m, w, v))
            count += 1

rng = Random(309)
mixed = 0
for _ in range(1000):
    a, b = rng.choice(saved), rng.choice(saved)
    if a[0] != b[0]:
        continue
    m = a[0]
    lam = F(rng.randrange(11), 10)
    w = [[lam*x+(1-lam)*y for x, y in zip(rx, ry)] for rx, ry in zip(a[1], b[1])]
    v = [[lam*x+(1-lam)*y for x, y in zip(rx, ry)] for rx, ry in zip(a[2], b[2])]
    t, d, bmass = stats(w, m)
    assert distance(w, v) <= 28*m*bmass + 156*m*d + 5*(m-t)
    mixed += 1

for k in (3, 5, 7):
    vals = [(F((2*sum(x)-k)**2-1, 4*k*k)) for x in product((0, 1), repeat=k)]
    assert min(vals) == 0
    assert max(vals) + F(1, 8*k*k) < 1
    assert sum(vals)/len(vals) == F(k-1, 4*k*k)

print(f"PASS: {count} exact generator pairs; {mixed} convex mixtures; shifted slack range/means for k=3,5,7.")
