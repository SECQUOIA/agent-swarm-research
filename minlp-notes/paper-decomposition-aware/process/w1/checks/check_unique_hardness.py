#!/usr/bin/env python3
"""Exact checks for the unique-optimum width-three reduction from Subset Sum.

F(x,s) = sum_{i=1}^n (s_i - s_{i-1} - a_i x_i)^2 + M sum x_i(1-x_i) + eps sum 2^{i-1} x_i,
s_0 = 0, s_n = T, x in [0,1]^n, s_1..s_{n-1} in [-U, 2U], M = ||a||^2, eps = 1/(n 2^{n+1}).
Checks: decomposition identity F = Phi(x) + sum (d_i-d_{i-1})^2 (symbolic, n<=4),
vertex uniqueness and gap >= eps, decision equivalence, growth inequality with
g = eps / (n (1 + 2(n-1)||a||^2)) at random rational points, coordinate curvature 4.
"""
from fractions import Fraction as Fr
from itertools import product
import random
import sympy as sp

rng = random.Random(7)


def params(a):
    n = len(a)
    M = sum(x * x for x in a)
    eps = Fr(1, n * 2 ** (n + 1))
    g = eps / (n * (1 + 2 * (n - 1) * M))
    return n, M, eps, g


def F(a, T, x, s):
    n, M, eps, _ = params(a)
    S = [Fr(0)] + list(s) + [Fr(T)]
    val = sum((S[i] - S[i - 1] - a[i - 1] * x[i - 1]) ** 2 for i in range(1, n + 1))
    val += M * sum(xi * (1 - xi) for xi in x) + eps * sum(2 ** i * x[i] for i in range(n))
    return val


def sigma(a, T, x):
    n = len(a)
    e = sum(ai * xi for ai, xi in zip(a, x)) - T
    return [sum(a[j] * x[j] for j in range(k)) - Fr(k, n) * e for k in range(1, n)]


def symbolic_identity(nmax=4):
    for n in range(2, nmax + 1):
        a = sp.symbols(f'a1:{n + 1}')
        x = sp.symbols(f'x1:{n + 1}')
        T, M, eps = sp.symbols('T M eps')
        d = sp.symbols(f'd1:{n}')
        e = sum(ai * xi for ai, xi in zip(a, x)) - T
        sig = [sum(a[j] * x[j] for j in range(k)) - sp.Rational(k, n) * e for k in range(1, n)]
        S = [0] + [sig[k] + d[k] for k in range(n - 1)] + [T]
        Fs = sum((S[i] - S[i - 1] - a[i - 1] * x[i - 1]) ** 2 for i in range(1, n + 1))
        dd = [0] + list(d) + [0]
        rhs = e ** 2 / n + sum((dd[i] - dd[i - 1]) ** 2 for i in range(1, n + 1))
        assert sp.expand(Fs - rhs) == 0, n
        # coordinate curvature: s_k diag 4, x_i diag 2a_i^2 - 2M
        svars = sp.symbols(f's1:{n}')
        S2 = [0] + list(svars) + [T]
        Fq = sum((S2[i] - S2[i - 1] - a[i - 1] * x[i - 1]) ** 2 for i in range(1, n + 1)) \
            + M * sum(xi * (1 - xi) for xi in x)
        for sv in svars:
            assert sp.diff(Fq, sv, 2) == 4
        for i, xi in enumerate(x):
            assert sp.expand(sp.diff(Fq, xi, 2) - (2 * a[i] ** 2 - 2 * M)) == 0
    return nmax - 1


def instances():
    out = []
    for n in range(2, 5):
        for a in product(range(1, 6), repeat=n):
            U = sum(a)
            for T in range(0, U + 1):
                out.append((list(a), T))
    return out


def main():
    nid = symbolic_identity()
    count = 0
    growth_pts = 0
    for idx, (a, T) in enumerate(instances()):
        n, M, eps, g = params(a)
        U = sum(a)
        Phi = lambda x: Fr((sum(ai * xi for ai, xi in zip(a, x)) - T) ** 2, 1) / n \
            + M * sum(xi * (1 - xi) for xi in x) + eps * sum(2 ** i * x[i] for i in range(n))
        verts = list(product([0, 1], repeat=n))
        vals = {v: Phi([Fr(t) for t in v]) for v in verts}
        best = min(vals.values())
        argb = [v for v in verts if vals[v] == best]
        assert len(argb) == 1
        xs = argb[0]
        gapmin = min(vals[v] - best for v in verts if v != xs)
        assert gapmin >= eps
        yes = any(sum(ai * vi for ai, vi in zip(a, v)) == T for v in verts)
        Fstar = best
        assert (Fstar < Fr(1, 2 * n)) == yes and (yes or Fstar >= Fr(1, n))
        assert (sum(ai * vi for ai, vi in zip(a, xs)) == T) == yes
        # concavity of Phi: M >= ||a||^2 / n
        assert M * n >= sum(ai * ai for ai in a)
        zx = [Fr(t) for t in xs]
        zs = sigma(a, T, zx)
        assert F(a, T, zx, zs) == Fstar
        if idx % 7 == 0:
            for _ in range(20):
                x = [Fr(rng.randrange(0, 17), 16) for _ in range(n)]
                if rng.random() < 0.3:
                    x = [Fr(t) for t in xs]
                    j = rng.randrange(n)
                    x[j] = Fr(rng.randrange(0, 17), 16)
                sx = sigma(a, T, x)
                assert all(-U <= v <= 2 * U for v in sx)
                s = [v + Fr(rng.randrange(-8, 9), 8) for v in sx]
                s = [min(max(v, Fr(-U)), Fr(2 * U)) for v in s]
                lhs = F(a, T, x, s) - Fstar
                dist2 = sum((p - q) ** 2 for p, q in zip(x, zx)) + sum((p - q) ** 2 for p, q in zip(s, zs))
                assert lhs >= g * dist2
                # intermediate inequality Phi(x)-Phi* >= (eps/n)||x-x*||^2
                assert Phi(x) - Fstar >= eps / n * sum((p - q) ** 2 for p, q in zip(x, zx))
                growth_pts += 1
        count += 1
    print(f'PASS: symbolic identity n=2..{nid + 1}; {count} Subset Sum instances; {growth_pts} growth points')


if __name__ == '__main__':
    main()
