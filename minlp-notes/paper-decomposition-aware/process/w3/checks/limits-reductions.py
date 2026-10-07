"""W3 limits: exact checks of the renamed reductions in Section 10.

1. lim:prop:unique (items m, target a_0, weight lambda = 1/(m 2^{m+1}),
   penalty ||a||^2): split identity, uniqueness, decision gap, and growth
   g = lambda/(m(1+2(m-1)||a||^2)) at random rational points.
2. lim:prop:constraints (items m, target a_0, dummy item x_0 with a_0):
   brute force uniqueness, x_0^* = 0 iff yes-instance, OPT values.
3. prop:lbwidth: decoding floor(A/2^n) = -alpha for every A within 1/2 of
   OPT, and the L = 0 variant (multilinear part) has growth 1/n.
"""
from fractions import Fraction as Fr
from itertools import product, combinations
import random

rng = random.Random(7)


def unique_check(a, a0, pts=300):
    m = len(a)
    nrm = sum(t * t for t in a)
    lam = Fr(1, m * 2 ** (m + 1))
    A = sum(a)

    def F(x, y):
        yy = [Fr(0)] + list(y) + [Fr(a0)]
        return (sum((yy[i] - yy[i - 1] - a[i - 1] * x[i - 1]) ** 2 for i in range(1, m + 1))
                + nrm * sum(t * (1 - t) for t in x)
                + lam * sum(2 ** i * x[i] for i in range(m)))

    def sigma(x):
        e = sum(a[j] * x[j] for j in range(m)) - a0
        return [sum(a[j] * x[j] for j in range(k)) - Fr(k, m) * e for k in range(1, m)]

    def Phi(x):
        e = sum(a[j] * x[j] for j in range(m)) - a0
        return Fr(e * e, m) + nrm * sum(t * (1 - t) for t in x) + lam * sum(2 ** i * x[i] for i in range(m))

    verts = list(product([0, 1], repeat=m))
    vals = sorted((Phi(v), v) for v in verts)
    assert vals[0][0] < vals[1][0]
    xs = vals[0][1]
    opt = vals[0][0]
    yes = any(sum(a[j] * v[j] for j in range(m)) == a0 for v in verts)
    if yes:
        assert opt < Fr(1, 2 * m) and sum(a[j] * xs[j] for j in range(m)) == a0
    else:
        assert opt >= Fr(1, m)
    zs = list(map(Fr, xs)) + sigma(list(map(Fr, xs)))
    g = lam / (m * (1 + 2 * (m - 1) * nrm))
    for s in sigma(list(map(Fr, xs))):
        assert -A <= s <= 2 * A
    for _ in range(pts):
        x = [Fr(rng.randint(0, 12), 12) for _ in range(m)]
        y = [Fr(rng.randint(-12 * A, 24 * A), 12) for _ in range(m - 1)]
        # split identity
        sg = sigma(x)
        d = [Fr(0)] + [y[k] - sg[k] for k in range(m - 1)] + [Fr(0)]
        assert F(x, y) == Phi(x) + sum((d[i] - d[i - 1]) ** 2 for i in range(1, m + 1))
        z = x + y
        dist2 = sum((z[i] - zs[i]) ** 2 for i in range(len(z)))
        assert F(x, y) - opt >= g * dist2
    kappa = 4 / g
    assert kappa <= 2 ** (m + 3) * m * m * (1 + 2 * m * nrm)
    return yes


def constraints_check(a, a0):
    m = len(a)
    aa = [a0] + a
    feas = []
    for x in product([0, 1], repeat=m + 1):
        y = [Fr(0)]
        ok = True
        for i in range(m + 1):
            y.append(y[-1] + Fr(aa[i], a0) * x[i])
            if not (0 <= y[-1] <= 1):
                ok = False
        if ok and y[-1] == 1:
            val = 2 ** (m + 1) * x[0] + sum(2 ** (i - 1) * x[i] for i in range(1, m + 1))
            feas.append((val, x))
    feas.sort()
    assert len(feas) >= 1 and (len(feas) == 1 or feas[0][0] < feas[1][0])
    yes = any(sum(a[j] * v[j] for j in range(m)) == a0 for v in product([0, 1], repeat=m))
    assert (feas[0][1][0] == 0) == yes
    assert (feas[0][0] <= 2 ** m - 1) if yes else (feas[0][0] == 2 ** (m + 1))
    return yes


def lbwidth_check(n, E):
    def Phi(x):
        return -sum(x) + 2 * sum(x[i] * x[j] for i, j in E)

    def chi(x):
        return sum(2 ** i * x[i] for i in range(n))

    alpha = max(sum(v) for v in product([0, 1], repeat=n)
                if all(not (v[i] and v[j]) for i, j in E))
    vals = sorted((2 ** n * Phi(v) + chi(v), v) for v in product([0, 1], repeat=n))
    opt, xs = vals[0]
    assert vals[1][0] >= opt + 1
    assert chi(xs) >= 1
    for A in [opt - Fr(1, 2), opt, opt + Fr(1, 2)]:
        assert Fr(A) // 2 ** n == -alpha
    # L = 0 variant: multilinear part, growth 1/n on the cube
    for _ in range(200):
        x = [Fr(rng.randint(0, 8), 8) for _ in range(n)]
        M = 2 ** n * Phi(x) + chi(x)
        d2 = sum((x[i] - xs[i]) ** 2 for i in range(n))
        assert M - opt >= Fr(1, n) * d2
        Psi = M + Fr(1, 2 * n) * sum(t * t - t for t in x)
        assert Psi - opt >= Fr(1, 2 * n) * d2
    return alpha


if __name__ == "__main__":
    ys = 0
    for _ in range(25):
        m = rng.randint(2, 4)
        a = [rng.randint(1, 7) for _ in range(m)]
        a0 = rng.randint(0, sum(a))
        ys += unique_check(a, a0)
    print(f"unique: 25 random instances ({ys} yes): split identity, uniqueness, gap, growth OK")
    ys = 0
    for _ in range(60):
        m = rng.randint(1, 6)
        a0 = rng.randint(2, 15)
        a = [rng.randint(1, a0) for _ in range(m)]
        ys += constraints_check(a, a0)
    print(f"constraints: 60 random instances ({ys} yes): unique minimizer, x0*=0 iff yes")
    for n in range(1, 6):
        for _ in range(6):
            E = [e for e in combinations(range(n), 2) if rng.random() < 0.5]
            lbwidth_check(n, E)
    print("lbwidth: decoding floor(A/2^n) = -alpha within 1/2; growth 1/(2n) and 1/n (L=0) OK")
