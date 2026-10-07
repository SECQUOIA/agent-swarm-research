"""M5: exact check of the tensor Bernstein conversion and enclosure.

Report B foundations.tex, eq. (bernstein-conversion) and Lemma bernstein:
    b_alpha = sum_{beta <= alpha} a_beta prod_i C(alpha_i,beta_i)/C(d_i,beta_i).
For random rational polynomials on random rational boxes (including fixed
coordinates and degree bounds larger than the actual degree) this script
checks symbolically that sum_alpha b_alpha B_alpha^d(t) equals p(x(t)), and
that min b <= p <= max b at random rational points of the box.
"""
import random
from fractions import Fraction
from itertools import product
from math import comb

import sympy as sp

random.seed(20261003)


def rand_q(lo=-5, hi=5, den=4):
    return Fraction(random.randint(lo * den, hi * den), random.randint(1, den))


def bernstein_coefficients(a, d):
    """a: dict beta-tuple -> Fraction (power basis in t); d: degree bound."""
    out = {}
    for alpha in product(*(range(di + 1) for di in d)):
        total = Fraction(0)
        for beta, coeff in a.items():
            if all(b <= al for b, al in zip(beta, alpha)):
                w = Fraction(1)
                for al, b, di in zip(alpha, beta, d):
                    w *= Fraction(comb(al, b), comb(di, b))
                total += coeff * w
        out[alpha] = total
    return out


def check_once(n, max_deg, extra):
    xs = sp.symbols(f"x0:{n}")
    ts = sp.symbols(f"t0:{n}")
    # random polynomial in x with rational coefficients
    p = 0
    for _ in range(random.randint(1, 6)):
        mono = 1
        for x in xs:
            mono *= x ** random.randint(0, max_deg)
        c = rand_q()
        p += sp.Rational(c.numerator, c.denominator) * mono
    p = sp.expand(p)
    box = []
    for i in range(n):
        lo = rand_q(-3, 3)
        hi = lo if random.random() < 0.2 else lo + abs(rand_q(0, 3)) + Fraction(1, 7)
        box.append((lo, hi))
    sub = {}
    free = []
    for i, (lo, hi) in enumerate(box):
        L, U = sp.Rational(lo.numerator, lo.denominator), sp.Rational(hi.numerator, hi.denominator)
        if lo == hi:
            sub[xs[i]] = L          # fixed coordinate is eliminated
        else:
            sub[xs[i]] = L + (U - L) * ts[i]
            free.append(i)
    pt = sp.expand(p.subs(sub))
    if not free:
        return "constant"
    tfree = [ts[i] for i in free]
    poly = sp.Poly(pt, *tfree)
    degs = [poly.degree(t) for t in tfree]
    d = [max(0, dg) + random.randint(0, extra) for dg in degs]
    a = {tuple(m): Fraction(int(c.p), int(c.q)) for m, c in zip(poly.monoms(), poly.coeffs())}
    b = bernstein_coefficients(a, d)
    # symbolic identity
    recon = 0
    for alpha, coeff in b.items():
        term = sp.Rational(coeff.numerator, coeff.denominator)
        for t, al, di in zip(tfree, alpha, d):
            term *= sp.binomial(di, al) * t ** al * (1 - t) ** (di - al)
        recon += term
    assert sp.expand(recon - pt) == 0, "conversion identity failed"
    lo_b, hi_b = min(b.values()), max(b.values())
    for _ in range(30):
        point = {t: sp.Rational(random.randint(0, 50), 50) for t in tfree}
        val = pt.subs(point)
        assert lo_b <= val <= hi_b, "enclosure failed"
    return "ok"


def main():
    counts = {}
    for trial in range(120):
        n = random.choice([1, 1, 2, 2, 3])
        res = check_once(n, max_deg=3 if n < 3 else 2, extra=random.choice([0, 0, 1, 2]))
        counts[res] = counts.get(res, 0) + 1
    print("Bernstein conversion and enclosure:", counts)
    # textbook example: p(t)=t^2 on [0,1], d=2 -> b = (0,0,1)
    b = bernstein_coefficients({(2,): Fraction(1)}, [2])
    assert [b[(i,)] for i in range(3)] == [0, 0, 1]
    # p(t)=t with degree bound 3 -> b_i = i/3
    b = bernstein_coefficients({(1,): Fraction(1)}, [3])
    assert [b[(i,)] for i in range(4)] == [Fraction(i, 3) for i in range(4)]
    print("textbook examples ok")


if __name__ == "__main__":
    main()
