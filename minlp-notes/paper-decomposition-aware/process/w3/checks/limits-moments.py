"""W3 limits: exact checks for Proposition lim:prop:moments (appendix-moments.tex)
in the renamed notation (nodes zeta, residual sum cbar, Upsilon, lambda=1/(8r)).

For r = 1..4: the split identity F = Psi + 2r sum (delta_k - delta_{k-1})^2 at
random rational points, Psi - 1/4 = 2 Upsilon + lambda (ubar + vbar), growth with
g_r at random points, the witness value 1/4 - (2r+1)/(16r), and agreement of
the moments of s through order 2r-1 but not 2r. Also the r = 2 remark numbers.
"""
from fractions import Fraction as Fr
from math import comb
from itertools import combinations
import random

rng = random.Random(3)


def e2(xs):
    return sum(a * b for a, b in combinations(xs, 2))


def F(r, h, s, y, z, u, v):
    yy = [Fr(0)] + y + [s]
    zz = [Fr(0)] + z
    lam = Fr(1, 8 * r)
    res = [(yy[i] - yy[i - 1]) / h - u[i - 1] for i in range(1, r + 1)]
    res += [(zz[j] - zz[j - 1]) / h - v[j - 1] for j in range(1, r)]
    res += [(s - zz[r - 1]) / h - Fr(1, 2)]
    return (2 * r * sum(t * t for t in res) + sum(t * (1 - t) for t in u)
            + sum(t * (1 - t) for t in v) + lam * (sum(u) + sum(v)))


def check(r):
    h = Fr(1, 4 * r)
    lam = Fr(1, 8 * r)
    gr = lam / (1 + 8 * (2 * r - 1) ** 2)
    # minimizer: u=v=0, nodes zeta^0(0,0) with residual -cbar/(2r), cbar=-1/2
    def zeta0(u, v):
        c = list(u) + [Fr(-1, 2)] + [-t for t in reversed(v)]
        cbar = sum(c)
        return [sum(c[:k]) - Fr(k, 2 * r) * cbar for k in range(2 * r + 1)], cbar

    def unpack(zeta):
        y = [h * zeta[k] for k in range(1, r)]
        s = h * zeta[r]
        z = [h * zeta[2 * r - k] for k in range(1, r)]  # z_k = h zeta_{2r-k}
        return s, y, z

    z0, _ = zeta0([Fr(0)] * r, [Fr(0)] * (r - 1))
    s0, y0, zz0 = unpack(z0)
    xstar = [s0] + y0 + zz0 + [Fr(0)] * (2 * r - 1)
    assert F(r, h, s0, y0, zz0, [Fr(0)] * r, [Fr(0)] * (r - 1)) == Fr(1, 4)
    for _ in range(200):
        u = [Fr(rng.randint(0, 6), 6) for _ in range(r)]
        v = [Fr(rng.randint(0, 6), 6) for _ in range(r - 1)]
        s = Fr(rng.randint(-12, 12), 12)
        y = [Fr(rng.randint(-12, 12), 12) for _ in range(r - 1)]
        z = [Fr(rng.randint(-12, 12), 12) for _ in range(r - 1)]
        zeta = [Fr(0)] + [t / h for t in y] + [s / h] + [z[r - 1 - l] / h for l in range(1, r)] + [Fr(0)]
        zz, cbar = zeta0(u, v)
        d = [zeta[k] - zz[k] for k in range(2 * r + 1)]
        ub, vb = sum(u), sum(v)
        Psi = cbar ** 2 + sum(t * (1 - t) for t in u) + sum(t * (1 - t) for t in v) + lam * (ub + vb)
        Fv = F(r, h, s, y, z, u, v)
        assert Fv == Psi + 2 * r * sum((d[k] - d[k - 1]) ** 2 for k in range(1, 2 * r + 1))
        Ups = e2(u) + e2(v) - ub * vb + vb
        assert Psi - Fr(1, 4) == 2 * Ups + lam * (ub + vb)
        x = [s] + y + z + u + v
        dist2 = sum((x[i] - xstar[i]) ** 2 for i in range(len(x)))
        assert Fv - Fr(1, 4) >= gr * dist2
    # witness
    pi = [Fr(comb(2 * r, 2 * i), 2 ** (2 * r - 1)) for i in range(r + 1)]
    pj = [Fr(comb(2 * r, 2 * j + 1), 2 ** (2 * r - 1)) for j in range(r)]
    assert sum(pi) == 1 and sum(pj) == 1
    val = lam * (sum(p * i for i, p in enumerate(pi)) + sum(p * j for j, p in enumerate(pj)))
    assert val == Fr(1, 4) - Fr(2 * r + 1, 16 * r)
    for a in range(2 * r + 1):
        ml = sum(p * (h * i) ** a for i, p in enumerate(pi))
        mr = sum(p * (h * (j + Fr(1, 2))) ** a for j, p in enumerate(pj))
        assert (ml == mr) == (a < 2 * r), (r, a)
    return val


def remark():
    left = [(Fr(1, 8), Fr(0)), (Fr(3, 8), Fr(1, 2)), (Fr(3, 8), Fr(1, 2)), (Fr(1, 8), Fr(1))]
    right = [(Fr(1, 2), Fr(1, 4)), (Fr(1, 2), Fr(3, 4))]
    ml = [sum(p * t ** a for p, t in left) for a in range(1, 5)]
    mr = [sum(p * t ** a for p, t in right) for a in range(1, 5)]
    assert ml[:3] == mr[:3] == [Fr(1, 2), Fr(5, 16), Fr(7, 32)]
    assert ml[3] == Fr(11, 64) and mr[3] == Fr(41, 256)


if __name__ == "__main__":
    for r in range(1, 5):
        print(f"r={r}: identities, growth g_r, witness value {check(r)}, moments OK")
    remark()
    print("remark r=2 moments OK")
