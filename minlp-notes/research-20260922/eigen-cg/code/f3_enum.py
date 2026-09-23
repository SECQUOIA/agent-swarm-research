"""Enumerate 'exact-part' Eigen-CG cuts (family F3 ⊇ F2): v = rho*sigma, v0 = rho*tau with
sigma in Z^n, a = rho^2, b = 2 a tau, such that 2 a s_i s_j in Z and a s_i^2 + b s_i in Z.
Then E-CG(v0, v) is the linearization of  f(h) = a h^2 + b h + floor(b^2/(4a)),  h = sigma.x,
i.e. no rounding happens except in the constant.  Such a cut can only fail to follow from the
BH inequalities in direction sigma if f(h0) < 0 at some integer h0 that is not a subset sum."""
import itertools
import math
from fractions import Fraction as Fr
from math import gcd
from functools import reduce


def subset_sums(s):
    S = {0}
    for t in s:
        S |= {u + t for u in S}
    return S


def bezout(sigma):
    """Integers c with sum c_i s_i = gcd(sigma)."""
    c = []
    g = 0
    for s in sigma:
        r0, r1, x0, x1, y0, y1 = g, s, 1, 0, 0, 1
        while r1:
            q = r0 // r1
            r0, r1 = r1, r0 - q * r1
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        if r0 < 0:
            r0, x0, y0 = -r0, -x0, -y0
        c = [t * x0 for t in c] + [y0]
        g = r0
    assert sum(ci * si for ci, si in zip(c, sigma)) == g
    return c, g


def b_coset(sigma, a):
    """Return b0 in [0,1) with b*s_i ≡ -a s_i^2 (mod 1) for all i, or None.
    With gcd(sigma) = 1, b ≡ -a sum c_i s_i^2 (mod 1) is forced by Bezout (sum c_i s_i = 1)."""
    c, g = bezout(sigma)
    assert g == 1
    b = -a * sum(ci * s * s for ci, s in zip(c, sigma))
    b = b - math.floor(b)
    if all((a * s * s + b * s).denominator == 1 for s in sigma):
        return b
    return None


def candidates(sigma, amax=40, tau_margin=2):
    n = len(sigma)
    g = reduce(gcd, [abs(sigma[i] * sigma[j]) for i in range(n) for j in range(i + 1, n)])
    S = subset_sums(sigma)
    lo, hi = min(S) - tau_margin, max(S) + tau_margin
    out = []
    for m in range(1, amax + 1):
        a = Fr(m, 2 * g)
        b0 = b_coset(sigma, a)
        if b0 is None:
            continue
        # tau = b/(2a) in [-hi, -lo]  =>  b in [-2a hi, -2a lo]
        for k in range(math.floor(-2 * a * hi - b0) - 1, math.ceil(-2 * a * lo - b0) + 2):
            b = b0 + k
            c = math.floor(b * b / (4 * a))
            f = lambda h: a * h * h + b * h + c
            # sanity: validity on subset sums
            assert all(f(h) >= 0 for h in S), (sigma, a, b)
            bad = [h for h in range(lo - 2, hi + 3) if f(h) < 0]
            if bad:
                out.append((a, b, c, bad))
    return out


def ecg_from_abc(sigma, a, b, c):
    n = len(sigma)
    coef_x = [a * s * s + b * s for s in sigma]
    coef_X = [2 * a * sigma[i] * sigma[j] for i in range(n) for j in range(i + 1, n)]
    assert all(t.denominator == 1 for t in coef_x + coef_X)
    return [int(t) for t in coef_x + coef_X], c
