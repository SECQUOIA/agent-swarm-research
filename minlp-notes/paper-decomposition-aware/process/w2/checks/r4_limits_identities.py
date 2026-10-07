"""R4: independent symbolic/exact checks of identities in limits.tex,
appendix-moments.tex and appendix-boundary.tex."""
import sympy as sp
from fractions import Fraction as Fr
from math import comb
import random


def check_unique_split(n=4):
    # Prop lim:prop:unique: F = Phi + sum (delta_i - delta_{i-1})^2
    a = sp.symbols(f"a1:{n+1}", positive=True)
    x = sp.symbols(f"x1:{n+1}")
    s = sp.symbols(f"s1:{n}")
    T, M, eps = sp.symbols("T M eps")
    ss = [0] + list(s) + [T]
    F = sum((ss[i + 1] - ss[i] - a[i] * x[i]) ** 2 for i in range(n)) \
        + M * sum(xi * (1 - xi) for xi in x) + eps * sum(2 ** i * x[i] for i in range(n))
    e = sum(a[i] * x[i] for i in range(n)) - T
    sig = [0] + [sum(a[j] * x[j] for j in range(k)) - sp.Rational(k, n) * e for k in range(1, n)] + [T]
    dl = [ss[k] - sig[k] for k in range(n + 1)]
    Phi = e ** 2 / n + M * sum(xi * (1 - xi) for xi in x) + eps * sum(2 ** i * x[i] for i in range(n))
    rhs = Phi + sum((dl[i + 1] - dl[i]) ** 2 for i in range(n))
    assert sp.expand(F - rhs) == 0
    print("unique: split identity OK for n =", n)


def check_unique_growth(trials=3000, seed=1):
    # random small Subset Sum instances: check F(z)-OPT >= g ||z-z*||^2 at random rational points
    rng = random.Random(seed)
    for _ in range(40):
        n = rng.randint(2, 4)
        a = [rng.randint(1, 6) for _ in range(n)]
        U = sum(a)
        T = rng.randint(0, U)
        M = sum(t * t for t in a)
        eps = Fr(1, n * 2 ** (n + 1))

        def Phi(x):
            e = sum(ai * xi for ai, xi in zip(a, x)) - T
            return Fr(e * e, n) + M * sum(xi * (1 - xi) for xi in x) + eps * sum(2 ** i * x[i] for i in range(n))

        verts = [tuple(Fr((b >> i) & 1) for i in range(n)) for b in range(2 ** n)]
        vals = sorted((Phi(v), v) for v in verts)
        assert vals[0][0] != vals[1][0]
        xs = vals[0][1]
        OPT = vals[0][0]

        def sig(x):
            e = sum(ai * xi for ai, xi in zip(a, x)) - T
            return [sum(a[j] * x[j] for j in range(k)) - Fr(k, n) * e for k in range(1, n)]

        zs = list(xs) + sig(xs)
        g = eps / (n * (1 + 2 * (n - 1) * M))

        def Fz(x, s):
            ss = [0] + list(s) + [T]
            return sum((ss[i + 1] - ss[i] - a[i] * x[i]) ** 2 for i in range(n)) \
                + M * sum(xi * (1 - xi) for xi in x) + eps * sum(2 ** i * x[i] for i in range(n))

        for _ in range(trials // 40):
            x = [Fr(rng.randint(0, 20), 20) for _ in range(n)]
            s = [Fr(rng.randint(-20 * U, 40 * U), 20) for _ in range(n - 1)]
            z = x + s
            d2 = sum((zi - zsi) ** 2 for zi, zsi in zip(z, zs))
            assert Fz(x, s) - OPT >= g * d2
        # decision gap
        yes = any(sum(ai * vi for ai, vi in zip(a, v)) == T for v in verts)
        if yes:
            assert OPT < Fr(1, 2 * n)
        else:
            assert OPT >= Fr(1, n)
    print("unique: growth and decision gap OK on 40 random instances")


def check_moments(r=3):
    u = sp.symbols(f"u1:{r+1}")
    v = sp.symbols(f"v1:{r}")
    U, V = sum(u), sum(v)
    tau = sp.Rational(1, 8 * r)
    E = U - V - sp.Rational(1, 2)
    Psi = E ** 2 + sum(t * (1 - t) for t in u) + sum(t * (1 - t) for t in v) + tau * (U + V)
    e2 = lambda w: sum(w[i] * w[j] for i in range(len(w)) for j in range(i + 1, len(w)))
    Pi = e2(u) + e2(v) - U * V + V
    assert sp.expand(Psi - sp.Rational(1, 4) - 2 * Pi - tau * (U + V)) == 0
    # parity moments
    for j in range(2 * r + 2):
        ev = sum(Fr(comb(2 * r, 2 * i), 2 ** (2 * r - 1)) * (2 * i) ** j for i in range(r + 1))
        od = sum(Fr(comb(2 * r, 2 * i + 1), 2 ** (2 * r - 1)) * (2 * i + 1) ** j for i in range(r))
        if j < 2 * r:
            assert ev == od, (j, ev, od)
        else:
            assert ev != od
    EU = sum(Fr(comb(2 * r, 2 * i), 2 ** (2 * r - 1)) * i for i in range(r + 1))
    EV = sum(Fr(comb(2 * r, 2 * i + 1), 2 ** (2 * r - 1)) * i for i in range(r))
    val = Fr(1, 8 * r) * (EU + EV)
    assert val == Fr(1, 4) - Fr(2 * r + 1, 16 * r)
    print(f"moments r={r}: reduction identity, parity moments < {2*r}, witness value {val} OK")


def check_boundary():
    # Prop margin identity and a_i
    n = 3
    x = sp.symbols(f"x0:{n+1}")
    y = sp.symbols("y")
    r = [x[0] - sp.Rational(1, 4)] + [x[i] - x[i - 1] ** 2 / 4 for i in range(1, n + 1)]
    h = x[n] - x[n - 1] ** 2 / 8
    Fn = sum(t ** 2 for t in r)
    G = Fn + y ** 2 + 3 * y * h
    rhs = sp.Rational(1, 4) * (Fn + y ** 2) + sp.Rational(3, 4) * (Fn - r[n] ** 2) \
        + sp.Rational(3, 4) * (r[n] + y) ** 2 + sp.Rational(3, 2) * y * x[n]
    assert sp.expand(G - rhs) == 0
    a = [sp.Rational(1, 4)]
    for i in range(1, n + 1):
        a.append(a[-1] ** 2 / 4)
    assert all(a[i] == sp.Rational(1, 2 ** (4 * 2 ** i - 2)) for i in range(n + 1))
    dyG = sp.diff(G, y).subs({**{x[i]: a[i] for i in range(n + 1)}, y: 0})
    assert dyG == sp.Rational(3, 2) * a[n]
    # diagonal second derivatives
    d = [sp.simplify(sp.diff(G, x[i], 2)) for i in range(n + 1)]
    print("margin diag Hessian:", d)
    # Prop weakcompl identity
    X, w1, w2 = sp.symbols("X w1 w2")
    uu = X ** 2 - sp.Rational(1, 2)
    W = uu ** 2 + w1 ** 2 + w2 ** 2 + 3 * w1 * w2 + uu * (w1 - w2)
    rhs = sp.Rational(1, 2) * (uu ** 2 + w1 ** 2 + w2 ** 2) + sp.Rational(1, 2) * (uu + w1 - w2) ** 2 + 4 * w1 * w2
    assert sp.expand(W - rhs) == 0
    Hs = sp.hessian(W, (X, w1, w2)).subs({X: 1 / sp.sqrt(2), w1: 0, w2: 0})
    vv = sp.Matrix([0, 1, -1])
    assert sp.simplify((vv.T * Hs * vv)[0]) == -2
    print("boundary: margin identity, a_i, gamma, weakcompl identity OK")


def check_common_mesh_constants():
    # radius: (1+sqrt(17/15)) + 1 + (2+sqrt(17/15))/sqrt(8)
    rad = (1 + sp.sqrt(sp.Rational(17, 15))) + 1 + (2 + sp.sqrt(sp.Rational(17, 15))) / sp.sqrt(8)
    print("common-mesh radius constant =", sp.N(rad, 8), "(< 4.2:", bool(rad < sp.Rational(21, 5)), ")")
    # cap: 3/4 + 8 ln(5/4 + 2*4.2/sqrt(8) sqrt(n)) <= 8 ceil(log2(n+2))
    import math
    c = 2 * 4.2 / math.sqrt(8)
    worst = 0
    for n in range(1, 200000):
        phi = 0.75 + 8 * math.log(1.25 + c * math.sqrt(n))
        cap = 8 * math.ceil(math.log2(n + 2))
        worst = max(worst, phi / cap)
    print("common-mesh cap: max phi/cap over n<2e5 =", round(worst, 4))
    # radius 5 instead of 4.2 also fits the cap?
    c5 = 2 * 5 / math.sqrt(8)
    worst5 = max((0.75 + 8 * math.log(1.25 + c5 * math.sqrt(n))) / (8 * math.ceil(math.log2(n + 2))) for n in range(1, 200000))
    print("with radius 5: max phi/cap =", round(worst5, 4))


if __name__ == "__main__":
    check_unique_split(4)
    check_unique_growth()
    for r in (1, 2, 3, 4):
        check_moments(r)
    check_boundary()
    check_common_mesh_constants()
