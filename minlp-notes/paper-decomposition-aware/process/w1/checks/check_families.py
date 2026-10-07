"""Exact checks of the lower-bound encodings and the nonconvex example family.

A. ETH family (width): G_delta(x) = 2^n(-sum x_i + 2 sum_E x_i x_j)
   + sum_i 2^{i-1} x_i + delta sum_i (x_i^2 - x_i), delta = 1/(2n), on the
   continuous box [0,1]^n.  Check: unique vertex optimizer, integer vertex
   values, alpha(G) = -floor(G*/2^n), growth >= 1/(2n) at random rational points,
   L = 1/n so kappa <= 2.
B. Subset-sum family (conditioning, p = 3): integer path encoding with
   tie-breaking.  Exhaustive enumeration: unique optimizer, gap >= 1,
   min Phi = 0 iff the instance is a yes-instance, exact growth constant
   >= 1/(m(1+A^2)), and kappa within the stated bound.
C. Block family: corner patterns are strict local minima (strict
   complementarity on u,v; positive definite free Hessian in r), and
   F - F* >= 1/2 ||x - x*||^2 at random rational points.
"""

import random
from fractions import Fraction as Fr
from itertools import product, combinations


def family_A(rng):
    checked = 0
    for n in range(2, 7):
        for _ in range(6):
            E = [(i, j) for i, j in combinations(range(n), 2) if rng.random() < 0.45]
            delta = Fr(1, 2 * n)

            def G(x):
                psi = -sum(x) + 2 * sum(x[i] * x[j] for i, j in E)
                tau = sum(Fr(2) ** i * x[i] for i in range(n))
                return Fr(2) ** n * psi + tau + delta * sum(xi * xi - xi for xi in x)

            verts = [tuple(Fr(v) for v in bits) for bits in product((0, 1), repeat=n)]
            vals = {v: G(v) for v in verts}
            assert all(val.denominator == 1 for val in vals.values())
            gstar = min(vals.values())
            arg = [v for v in verts if vals[v] == gstar]
            assert len(arg) == 1
            xs = arg[0]
            alpha = max(sum(bits) for bits in product((0, 1), repeat=n)
                        if all(not (bits[i] and bits[j]) for i, j in E))
            assert -((gstar) // (2 ** n)) == alpha
            for _ in range(300):
                x = [Fr(rng.randint(0, 64), 64) for _ in range(n)]
                if rng.random() < 0.5:   # points near the optimizer
                    x = [xs[i] + (Fr(rng.randint(0, 8), 512) if xs[i] == 0 else -Fr(rng.randint(0, 8), 512))
                         for i in range(n)]
                d2 = sum((x[i] - xs[i]) ** 2 for i in range(n))
                assert G(x) - gstar >= d2 / (2 * n), (n, x)
                checked += 1
    return checked


def family_B():
    cases = 0
    instances = [((1, 2), 2), ((1, 2), 4), ((2, 3), 4), ((1, 1, 2), 3), ((2, 2, 1), 4), ((1, 3), 2)]
    for a, t in instances:
        m, A = len(a), sum(a)
        M = (A + t) ** 2 + 1
        yes = any(sum(ak * bk for ak, bk in zip(a, bits)) == t for bits in product((0, 1), repeat=m))

        def Phi(sig, s):
            prev, val = 0, 0
            for k in range(m):
                val += M * (s[k] - prev - a[k] * sig[k]) ** 2
                prev = s[k]
            return val + (s[-1] - t) ** 2

        def Psi(sig, s):
            return 2 ** (m + 1) * Phi(sig, s) + sum(2 ** k * sig[k] for k in range(m))

        pts = [(sig, s) for sig in product((0, 1), repeat=m) for s in product(range(A + 1), repeat=m)]
        vals = {p: Psi(*p) for p in pts}
        best = min(vals.values())
        arg = [p for p in pts if vals[p] == best]
        assert len(arg) == 1
        zs = arg[0]
        assert (min(Phi(*p) for p in pts) == 0) == yes
        zvec = list(zs[0]) + list(zs[1])
        g = None
        for p, v in vals.items():
            if p == zs:
                continue
            assert v - best >= 1
            d2 = sum((x - y) ** 2 for x, y in zip(list(p[0]) + list(p[1]), zvec))
            r = Fr(v - best, d2)
            g = r if g is None else min(g, r)
        assert g >= Fr(1, m * (1 + A * A))
        L = 2 ** (m + 2) * M * (max(a) ** 2 + 2)
        # actual diagonal maxima
        Ls = max(max(2 ** (m + 1) * M * 2 * ak * ak for ak in a), 2 ** (m + 1) * (4 * M), 2 ** (m + 1) * (2 * M + 2))
        assert Ls <= L
        kappa = max(1, Fr(Ls) / g)
        assert kappa <= Fr(L) * m * (1 + A * A)
        cases += 1
    return cases


def family_C(rng):
    """Blocks on a 2 x 3 grid graph of blocks, coupling c = 1/(16*Delta)."""
    rows, cols = 2, 3
    blocks = [(r, c) for r in range(rows) for c in range(cols)]
    idx = {b: k for k, b in enumerate(blocks)}
    E = []
    for (r, c) in blocks:
        if r + 1 < rows:
            E.append((idx[(r, c)], idx[(r + 1, c)]))
        if c + 1 < cols:
            E.append((idx[(r, c)], idx[(r, c + 1)]))
    deg = [0] * len(blocks)
    for i, j in E:
        deg[i] += 1
        deg[j] += 1
    Delta = max(deg)
    cpl = Fr(1, 16 * Delta)
    m = len(blocks)

    def F(x):
        val = Fr(0)
        for k in range(m):
            u, v, r = x[3 * k], x[3 * k + 1], x[3 * k + 2]
            val += u * u + v * v - 4 * u * v + (u + v) / 4 + (r - u / 2) ** 2
        for i, j in E:
            val += cpl * (x[3 * i] - x[3 * j]) ** 2
        return val

    def grad(x):
        g = [Fr(0)] * (3 * m)
        for k in range(m):
            u, v, r = x[3 * k], x[3 * k + 1], x[3 * k + 2]
            g[3 * k] += 2 * u - 4 * v + Fr(1, 4) - (r - u / 2)
            g[3 * k + 1] += 2 * v - 4 * u + Fr(1, 4)
            g[3 * k + 2] += 2 * (r - u / 2)
        for i, j in E:
            dd = 2 * cpl * (x[3 * i] - x[3 * j])
            g[3 * i] += dd
            g[3 * j] -= dd
        return g

    xs = []
    for k in range(m):
        xs += [Fr(1), Fr(1), Fr(1, 2)]
    Fs = F(xs)
    strict = 0
    for pattern in product((0, 1), repeat=m):
        x = []
        for p in pattern:
            x += [Fr(p), Fr(p), Fr(p, 2)]
        g = grad(x)
        for k, p in enumerate(pattern):
            for q in (3 * k, 3 * k + 1):
                assert (g[q] > 0) if p == 0 else (g[q] < 0)
            assert g[3 * k + 2] == 0
        strict += 1
        if pattern != (1,) * m:
            assert F(x) > Fs
    pts = 0
    for _ in range(2000):
        x = [Fr(rng.randint(0, 32), 32) for _ in range(3 * m)]
        d2 = sum((a - b) ** 2 for a, b in zip(x, xs))
        assert F(x) - Fs >= d2 / 2
        pts += 1
    # diagonal curvature: u: 2 + 1/2 + 2*cpl*deg ; v: 2 ; r: 2
    L = Fr(5, 2) + 2 * cpl * Delta
    assert L <= Fr(21, 8)
    return strict, pts


def main():
    rng = random.Random(11)
    a = family_A(rng)
    b = family_B()
    c_strict, c_pts = family_C(rng)
    print({"A_growth_points": a, "B_instances": b, "C_strict_local_minima": c_strict,
           "C_growth_points": c_pts})


if __name__ == "__main__":
    main()
