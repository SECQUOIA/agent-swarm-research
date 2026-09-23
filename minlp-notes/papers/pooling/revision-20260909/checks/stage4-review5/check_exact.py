"""Independent rational checks; finite regression evidence, not theorem proofs."""
from fractions import Fraction as F
from itertools import product
from random import Random

rng = Random(50409)


def matrix(r, c):
    s = sum(r)
    return [[a*b/s if s else F(0) for b in c] for a in r]


def dist(a, b):
    return sum(abs(x-y) for ar, br in zip(a, b) for x, y in zip(ar, br))


def bounded_margin(n, total, denominator=20):
    a = [0]*n
    for _ in range(total):
        choices = [j for j in range(n) if a[j] < denominator]
        a[rng.choice(choices)] += 1
    return [F(x, denominator) for x in a]


def round_face(r, c):
    m, s = len(r)//2, sum(r)
    w = matrix(r, c)
    deficit = 1-sum(w[i][i] for i in range(2*m))
    cross = sum(w[i][i+m] for i in range(m))
    assert s <= m+2*m*cross+4*m*deficit
    a = [int(x >= F(1, 2)) for x in r]
    for i in range(m):
        if a[i] == a[i+m]:
            a[i], a[i+m] = 1, 0
    v = matrix(a, a)
    assert dist(w, v) <= 8*m*cross+116*m*deficit+5*abs(s-m)
    assert dist(w, v) <= 28*m*cross+156*m*deficit+5*(m-s)
    return w, v


face_count = 0
for m in [1, 2]:
    by_sum = {}
    for a in product(range(5), repeat=2*m):
        by_sum.setdefault(sum(a), []).append([F(x, 4) for x in a])
    for group in by_sum.values():
        for r in group:
            for c in group:
                round_face(r, c)
                face_count += 1
for m in [3, 5, 10]:
    for _ in range(200):
        total = rng.randrange(40*m+1)
        round_face(bounded_margin(2*m, total), bounded_margin(2*m, total))
        face_count += 1
print('Face exposure and constructive rounding:', face_count, 'exact cases passed')

repair_count = 0
for p, q in [(1, 1), (1, 4), (3, 4), (8, 6)]:
    for _ in range(500):
        total = rng.randrange(20*min(p, q)+1)
        r, c = bounded_margin(p, total), bounded_margin(q, total)
        w = matrix(r, c)
        s = sum(r)
        if s < 1:
            rr, cc = [F(1)]+[F(0)]*(p-1), [F(1)]+[F(0)]*(q-1)
        else:
            def fix(a):
                return [F(1)]+[x*(s-1)/(s-a[0]) if s != a[0] else F(0) for x in a[1:]]
            rr, cc = fix(r), fix(c)
        wp = matrix(rr, cc)
        assert sum(rr) == sum(cc)
        assert all(0 <= x <= 1 for x in rr+cc)
        assert dist(w, wp) <= 2*(2-r[0]-c[0])
        repair_count += 1
print('Unit-margin repair:', repair_count, 'exact cases passed')

vertex_count = 0
for n in range(2, 8):
    eps = F(1, 4)
    ds = [3*F(4)**(2*(j-n)) for j in range(1, n)]
    vertices = []
    for bits in product([0, 1], repeat=n):
        x = []
        for bit in bits:
            x.append(bit+(1-2*bit)*eps*(x[-1] if x else 0))
        assert x[-1]-x[-1]**2 == sum(d*y for d, y in zip(ds, x))
        vertices.append(x)
        vertex_count += 1
    assert len(set(x[-1] for x in vertices)) == 2**n
    for v in vertices:
        lam = 2*v[-1]-1
        score = lambda x: sum(d*y for d, y in zip(ds, x))+lam*x[-1]
        for w in vertices:
            if w != v:
                assert score(w) < score(v)
                change = w[-1]-v[-1]
                assert -change**2+F(4)**(-n)*change < 0
print('Path exposure, certificate, and local edge derivative:', vertex_count, 'vertices passed')

graph_count = 0
for entries in product([0, 1], repeat=4):
    c = [[-1 if entries[2*i+j] else 4 for j in range(2)] for i in range(2)]
    binary = list(product([0, 1], repeat=2))
    value = lambda x, y: sum(c[i][j]*x[i]*y[j] for i in range(2) for j in range(2))
    minimum = min(value(x, y) for x in binary for y in binary)
    biclique = max([0]+[sum(x)*sum(y) for x in binary for y in binary
                      if all(not x[i]*y[j] or entries[2*i+j] for i in range(2) for j in range(2))])
    assert minimum == -biclique
    grid = list(product([F(i, 4) for i in range(5)], repeat=2))
    assert all(value(x, y) >= minimum for x in grid for y in grid)
    graph_count += 1
print('Biclique numerator encoding:', graph_count, 'graphs and their quarter-grid margins passed')
