"""R2 exact checks for Proposition prop:star (families A, B) and Example ex:cr-star32.

Leaves are independent given the centre x, so grid minima and min-marginals are
computed exactly by separable minimization (F is a sum of leaf terms given x).
"""
from fractions import Fraction as Fr
from itertools import product
import sympy as sp


def grid(j):
    h = Fr(1, 2 ** j)
    return h, [h * t for t in range(2 ** j + 1)]


# ---------------- family (A) ----------------
def famA(j, m, eps):
    h, G = grid(j)
    beta = m * h * h / 4 - 1 - eps
    assert beta > 0
    leaf = lambda x, y: y * y - h * x * y
    centre = lambda x: x * x + beta * x
    leafmin = {x: min(leaf(x, y) for y in G) for x in G}
    Vh = {x: centre(x) + m * leafmin[x] for x in G}
    UG = min(Vh.values())
    assert UG == 0, UG
    # exact recourse value V(x) = (1 - m h^2/4) x^2 + beta x, vertex at hx/2 in [0,1]
    V = lambda x: (1 - m * h * h / 4) * x * x + beta * x
    assert V(Fr(1)) == -eps and V(Fr(0)) == 0
    # corner min-marginals of C = [1-h,1] x [0,h]
    mF = lambda x, y1: centre(x) + leaf(x, y1) + (m - 1) * leafmin[x]
    corners = [mF(x, y) for x in (1 - h, Fr(1)) for y in (Fr(0), h)]
    claimed = (1 - h) * (m * h * h / 4 - h - eps)
    assert min(corners) == claimed, (min(corners), claimed)
    assert min(corners) == min(Vh[1 - h], Vh[Fr(1)])
    # threshold rewriting with L = 2
    L = 2
    assert claimed == (1 - h) * (m - 4 / h - 4 * eps / (h * h)) * L * h * h / 8
    # bag-local budget |B| L h^2/8 = L h^2/4
    return claimed, claimed - L * h * h / 4 > UG, claimed - (1 + m) * L * h * h / 8 <= UG


# ---------------- family (B) ----------------
def famB(j, d):
    h, G = grid(j)
    assert d * h >= 2
    m = d * d
    iota = lambda t: h / 2 + t / d
    leafmin = lambda t: min((y - iota(t)) ** 2 for y in G)
    Vh = {}
    for x in G:
        t = x - Fr(1, 2)
        Vh[t] = t * t + m * leafmin(t)
        assert Vh[t] == 2 * t * t - d * h * abs(t) + Fr(d * d) * h * h / 4
    UG = min(Vh.values())
    assert UG == Fr(1, 2) - d * h / 2 + Fr(d * d) * h * h / 4
    mF = lambda t, y1: t * t + (y1 - iota(t)) ** 2 + (m - 1) * leafmin(t)
    out = []
    for sgn in (-1, 1):
        cs = [mF(t, y) for t in (Fr(0), sgn * h) for y in (Fr(0), h)]
        diff = min(cs) - UG
        assert diff == d * h * (Fr(1, 2) - h) + 2 * h * h - Fr(1, 2), diff
        assert min(cs) == min(Vh[Fr(0)], Vh[sgn * h])
        out.append(diff)
    return out[0]


def famB_spectrum(d):
    m = d * d
    n = m + 1
    H = sp.zeros(n, n)
    H[0, 0] = 2 + sp.Rational(2 * m, d * d)
    for i in range(1, n):
        H[i, i] = 2
        H[0, i] = H[i, 0] = sp.Rational(-2, d)
    ev = H.eigenvals()
    lmin = min(ev.keys(), key=lambda e: float(e))
    assert sp.simplify(lmin - (3 - sp.sqrt(5))) == 0, ev
    g = lmin / 2
    kappa = sp.nsimplify(4 / g)
    assert sp.simplify(4 / g - 2 * (3 + sp.sqrt(5))) == 0
    return ev


if __name__ == "__main__":
    # family A
    for j in (1, 2, 3):
        h = Fr(1, 2 ** j)
        for eps in (Fr(1, 16), Fr(1, 3)):
            mmin = int(4 * (1 + eps) / (h * h)) + 1
            for m in (mmin, mmin + 3, 2 * mmin):
                famA(j, m, eps)
    print("family A: formulas OK")
    # family B
    for j in (2, 3, 4):
        h = Fr(1, 2 ** j)
        dmin = int(2 / h)
        for d in (dmin, dmin + 1, 2 * dmin):
            famB(j, d)
    print("family B: formulas OK")
    for d in (2, 3, 4):
        famB_spectrum(d)
    print("family B: spectrum 3+-sqrt5, 2 ; kappa = 2(3+sqrt5) OK")
    # Example ex:cr-star32
    h, G = grid(1)
    m, eps = 32, Fr(1, 16)
    claimed, bag_rejects, global_keeps = famA(1, m, eps)
    beta = m * h * h / 4 - 1 - eps
    assert beta == Fr(15, 16)
    Vh = [x * x + beta * x for x in G]
    assert Vh == [0, Fr(23, 32), Fr(31, 16)]
    leaf = lambda x, y: y * y - h * x * y
    cm = sorted(x * x + beta * x + leaf(x, y) for x in (Fr(1, 2), Fr(1)) for y in (Fr(0), Fr(1, 2)))
    assert cm == [Fr(23, 32), Fr(27, 32), Fr(31, 16), Fr(31, 16)], cm
    assert bag_rejects and global_keeps
    assert (1 + m) * 2 * h * h / 8 == Fr(33, 16)
    print("ex:cr-star32 numbers OK")
    # Is m=32 the smallest? search smallest m (h=1/2) for which family-A hypothesis holds
    # and the bag-local budget L h^2/4 = 1/8 rejects the optimizer cell.
    found = None
    for m in range(1, 40):
        for eps in (Fr(1, 64), Fr(1, 32), Fr(1, 16)):
            if m * h * h <= 4 * (1 + eps):
                continue
            c, rej, keep = famA(1, m, eps)
            if rej:
                found = (m, eps)
                break
        if found:
            break
    print("smallest m with h=1/2 that already refutes the bag-local budget:", found)
