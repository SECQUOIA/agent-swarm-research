#!/usr/bin/env python3
"""Exact checks for the remaining limits propositions.

1. Star example: bag-local grid corrections are invalid (any fixed local correction fails for large m).
2. Set growth: any corrected grid on the chain sum (x_i-x_{i+1})^2 has b <= -L W_j^2/8.
3. Exponential complete messages: chain G(S,z) with expanding boxes, g=1/8, L=10, nu<=1/4.
4. Constrained reduction: local affine equalities, unique optimum, growth 1/(2n+3), kappa=1.
5. Value-oracle hidden-well family: growth, packing count.
"""
from fractions import Fraction as Fr
from itertools import product
import random
import sympy as sp

rng = random.Random(11)


def star(m, eps=Fr(1, 16)):
    G = [Fr(0), Fr(1, 2), Fr(1)]
    c = Fr(m, 16) - 1 - eps

    def V(x):
        return x * x - m * x * x / 16 + c * x

    def Vh(x):  # grid min over leaves with x fixed
        return x * x + c * x + m * min(y * y - x * y / 2 for y in G)

    # true optimum
    assert V(Fr(1)) == -eps and V(Fr(0)) == 0 and m > 16
    for x in G:
        assert Vh(x) - V(x) == m * min((x / 4 - y) ** 2 for y in G)
    U = min(Vh(x) for x in G)
    assert U == 0
    # corner min-marginals of bag {x, y_1} cell [1/2,1] x [0,1/2]

    def mm(x, y1):
        others = (m - 1) * min(y * y - x * y / 2 for y in G)
        return x * x + c * x + y1 * y1 - x * y1 / 2 + others
    corners = [mm(x, y) for x in (Fr(1, 2), Fr(1)) for y in (Fr(0), Fr(1, 2))]
    best = min(corners)
    assert best == Fr(m, 32) - Fr(1, 4) - eps / 2
    # optimizer bag projection (1, 1/4) lies in the cell; the cell is rejected iff best - e > U
    return best, Vh(Fr(1, 2)), Vh(Fr(1))


def set_growth(trials=300):
    cnt = 0
    for _ in range(trials):
        p = rng.choice([2, 3, 4])
        L = 2 if p == 2 else 4
        grids = []
        for _ in range(p):
            k = rng.randrange(1, 5)
            pts = sorted(set([Fr(0), Fr(1)] + [Fr(rng.randrange(1, 32), 32) for _ in range(k)]))
            grids.append(pts)

        def w(gr, v):
            i = gr.index(v)
            adj = []
            if i > 0:
                adj.append(gr[i] - gr[i - 1])
            if i < len(gr) - 1:
                adj.append(gr[i + 1] - gr[i])
            return max(adj)
        b = min(sum((y[i] - y[i + 1]) ** 2 for i in range(p - 1)) - sum(L * w(grids[i], y[i]) ** 2 / 8 for i in range(p))
                for y in product(*grids))
        for j in range(p):
            W = max(grids[j][i + 1] - grids[j][i] for i in range(len(grids[j]) - 1))
            assert b <= -L * W * W / 8
        cnt += 1
    return cnt


def messages(mmax=7):
    for m in range(2, mmax + 1):
        S = sp.symbols(f'S1:{m + 1}')
        z = sp.symbols(f'z1:{m + 1}')
        SS = [0] + list(S)
        r = [SS[t] - 2 * SS[t - 1] - z[t - 1] for t in range(1, m + 1)]
        G = S[-1] ** 2 + sum(x ** 2 for x in r) + sp.Rational(1, 8) * sum(x * (1 - x) for x in z)
        X = list(S) + list(z)
        H = sp.hessian(G, X)
        assert max(H[i, i] for i in range(2 * m)) == 10
        assert [H[i, i] for i in range(m)] == [10] * (m - 1) + [4]
        assert all(H[m + i, m + i] == sp.Rational(7, 4) for i in range(m))
        Pz = sp.diag(*([0] * m + [1] * m))
        assert (H + sp.Rational(1, 4) * Pz).is_positive_semidefinite
        # growth at random feasible points
        for _ in range(60):
            pt = {S[t]: sp.Rational(rng.randrange(0, 4 * (2 ** (t + 1) - 1) + 1), 4) for t in range(m)}
            pt.update({z[t]: sp.Rational(rng.randrange(0, 9), 8) for t in range(m)})
            if rng.random() < 0.5:  # near the optimum
                pt = {k: (sp.Rational(rng.randrange(0, 5), 64)) for k in X}
            val = G.subs(pt)
            assert 8 * val >= sum(v ** 2 for v in pt.values())
        # binary controls give integer terminal states with zero residuals
        zeros = set()
        for bits in product([0, 1], repeat=m):
            st = [0]
            for t in range(m):
                st.append(2 * st[-1] + bits[t])
            assert all(0 <= st[t] <= 2 ** t - 1 for t in range(1, m + 1))
            zeros.add(st[-1])
        assert zeros == set(range(2 ** m))
        # negative direction inside {r=0, S_m=0}: z with sum 2^{m-t} z_t = 0
        zd = [0] * m
        zd[-2], zd[-1] = 1, -2
        Sd = [0]
        for t in range(m):
            Sd.append(2 * Sd[-1] + zd[t])
        assert Sd[-1] == 0
        vec = sp.Matrix(Sd[1:] + zd)
        assert (vec.T * H * vec)[0] == -sp.Rational(1, 4) * sum(x * x for x in zd)
    return mmax - 1


def constrained(nmax=4, amax=5):
    cnt = 0
    for n in range(1, nmax + 1):
        for a in product(range(1, amax + 1), repeat=n):
            for B in range(1, amax + 1):
                if max(a) > B:
                    continue
                aa = [B] + list(a)
                feas = []
                for x in product([0, 1], repeat=n + 1):
                    if sum(ai * xi for ai, xi in zip(aa, x)) != B:
                        continue
                    y = [Fr(0)]
                    for i in range(n + 1):
                        y.append(y[-1] + Fr(aa[i], B) * x[i])
                    assert y[-1] == 1 and all(0 <= t <= 1 for t in y)
                    obj = 2 ** (n + 1) * x[0] + sum(2 ** (i - 1) * x[i] for i in range(1, n + 1))
                    feas.append((obj, list(x) + y))
                objs = [o for o, _ in feas]
                assert len(set(objs)) == len(objs)
                ostar, zstar = min(feas)
                yes = any(sum(ai * xi for ai, xi in zip(a, x)) == B for x in product([0, 1], repeat=n))
                assert (zstar[0] == 0) == yes
                g = Fr(1, 2 * n + 3)
                for o, z in feas:
                    assert o - ostar >= g * sum((p - q) ** 2 for p, q in zip(z, zstar))
                cnt += 1
    return cnt


def oracle():
    cnt = 0
    for p in (1, 2, 3, 4):
        for k in (1, 2, 3, 5, 8):
            r = Fr(1, 2 * k)  # well radius; kappa = 2p / r^2
            kappa = 2 * p / (r * r)
            L = Fr(1)
            g = L / kappa
            per = int(1 / (2 * r)) + 1
            # exact: per^(2p) >= (kappa/(8p))^p
            assert Fr(per) ** (2 * p) >= (kappa / (8 * p)) ** p
            centers = [tuple(Fr(2 * j) * r for j in idx) for idx in product(range(per), repeat=p)]
            assert all(0 <= cc <= 1 for c in centers for cc in c)
            # growth and plateau
            c = centers[rng.randrange(len(centers))]
            for _ in range(50):
                x = [Fr(rng.randrange(0, 65), 64) for _ in range(p)]
                d2 = sum((xi - ci) ** 2 for xi, ci in zip(x, c))
                Fc = min(g * p, L / 2 * d2)
                assert Fc >= g * d2
                if d2 >= r * r:
                    assert Fc == g * p
            cnt += 1
    return cnt


if __name__ == '__main__':
    best, v12, v1 = star(32)
    assert (best, v12, v1) == (Fr(23, 32), Fr(23, 32), Fr(31, 16))
    for m in (17, 20, 40, 100, 1000):
        star(m)
    print('star: m=32 values 23/32 (x=1/2), 31/16 (x=1); best corner 23/32; local correction 1/8 rejects; general m ok')
    print('set growth: grids checked', set_growth())
    print('messages: m=2..', messages() + 1, 'growth g=1/8, L=10, nu<=1/4, 2^m integer zeros, negative directions')
    print('constrained reduction: instances', constrained())
    print('oracle family: cases', oracle())
    print('ALL PASSED')
