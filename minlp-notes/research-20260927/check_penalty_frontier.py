"""Exact finite checks for penalty-frontier.md; not a proof of radius bounds."""

from fractions import Fraction as F
from itertools import product


def check_projection():
    # One kernel coordinate v. Rows c_i*v+q_i(u,t)<=0 have rank-one
    # common quadratic dependence. The zero-c rows must survive projection.
    c = (F(-1), F(1), F(-2), F(2), F(0))

    def q(u, t):
        return (u*u-t, u*u-1, 2*u*u+t-2, u*u-3*t-1, u*u+t-1)

    checked = 0
    for u, t in product((F(i, 5) for i in range(-8, 9)), repeat=2):
        values = q(u, t)
        lo = max(-qi/ci for ci, qi in zip(c, values) if ci < 0)
        hi = min(-qi/ci for ci, qi in zip(c, values) if ci > 0)
        fiber = lo <= hi and all(qi <= 0 for ci, qi in zip(c, values) if ci == 0)
        projected = all(qi <= 0 for ci, qi in zip(c, values) if ci == 0)
        for i, ci in enumerate(c):
            for j, cj in enumerate(c):
                if ci < 0 < cj:
                    # Positive ray weights cj and -ci annihilate the v row.
                    assert cj*ci + (-ci)*cj == 0
                    projected &= cj*values[i] - ci*values[j] <= 0
        assert fiber == projected
        checked += 1
    return checked


def check_repair():
    # X={(a,b) in [-1,1]^2: a^2-b-1/4<=0}, equality b=0.
    # The Slater point is (0,0), with sigma=1/4.
    sigma, gradient_bound, diameter_bound = F(1, 4), F(3), F(3)
    checked = 0
    for a, b in product((F(i, 10) for i in range(-10, 11)), repeat=2):
        if a*a-b-sigma > 0:
            continue
        e = abs(b)
        eta = gradient_bound*e
        alpha = eta/(sigma+eta)
        # Affine repair gives y=(a,0); blend y with the Slater point.
        w = (1-alpha)*a
        assert w*w <= sigma
        assert (1-alpha)*eta-alpha*sigma == 0
        assert e+alpha*diameter_bound <= (1+gradient_bound*diameter_bound/sigma)*e
        checked += 1
    return checked


def check_chain():
    for n in range(1, 10):
        rank = n-1
        numerator = 1 << ((1 << n)-1)
        assert numerator.bit_length() == 1 << (rank+1)


def check_facial_identity():
    for n in range(2, 9):
        s = [F(0)] + [F(1, 1 << (1 << i)) for i in range(1, n+1)]
        lam = [F(0)]*n
        lam[n-1] = F(1)
        for i in range(n-1, 1, -1):
            lam[i-1] = 2*s[i]*lam[i]
        lam[0] = 2*s[1]*lam[1]
        assert lam[0] == F(1, 1 << ((1 << n)-n-1))
        coeff = [F(0)]*(n+1)
        coeff[1] = lam[0]
        constant = -lam[0]*s[1]
        for i in range(1, n):
            coeff[i+1] += lam[i]
            coeff[i] -= 2*lam[i]*s[i]
            constant += lam[i]*s[i]*s[i]
        assert coeff[1:n] == [F(0)]*(n-1)
        assert coeff[n] == 1 and constant == -s[n]


if __name__ == "__main__":
    projections = check_projection()
    repairs = check_repair()
    check_chain()
    check_facial_identity()
    print(f"PASS: {projections} exact projection fibers; {repairs} exact repairs; 9 chain rank/bit identities; 7 exposing identities")
