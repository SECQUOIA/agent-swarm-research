"""Exact verification of Delsarte-Yudin lower-bound certificates for the elec (Thomson) instances.

Certificate (JSON): N, h = [h_0, ..., h_K] as exact decimal strings (Legendre basis, P_k(1) = 1).
Claim: for every feasible point of elecN (N points on the unit sphere S^2, pairwise distinct so that
the objective is defined),  E = sum_{i<j} 1/|x_i - x_j|  >=  (N^2 h_0 - N sum_k h_k) / 2.

Proof. Let t_ij = <x_i, x_j>, so |x_i - x_j| = sqrt(2 - 2 t_ij) and t_ij in [-1, 1) for i != j.
(a) Schoenberg / addition theorem: P_k(<x, y>) = (4 pi / (2k+1)) sum_m Y_km(x) conj(Y_km(y)) on S^2,
    so sum_{i,j} P_k(t_ij) = (4 pi/(2k+1)) sum_m |sum_i Y_km(x_i)|^2 >= 0, and it equals N^2 for k = 0.
(b) With h = sum h_k P_k and h_k >= 0 for k >= 1:  sum_{i,j} h(t_ij) >= h_0 N^2.
(c) If h(t) <= f(t) := (2 - 2t)^(-1/2) on [-1, 1), then
    sum_{i,j} h(t_ij) = N h(1) + sum_{i != j} h(t_ij) <= N h(1) + 2E,  with h(1) = sum_k h_k.
    Hence E >= (N^2 h_0 - N h(1)) / 2.
Checking (c): substitute s = sqrt(2 - 2t) in (0, 2], t = 1 - s^2/2. Then h(t) <= 1/s iff
    g(s) := 1 - s * h(1 - s^2/2) >= 0.  g is a polynomial with rational coefficients; we prove g > 0
on the closed interval [0, 2] exactly, twice, by independent methods:
    (i)  Bernstein-basis coefficients on dyadic subintervals of [0, 2] all > 0 (de Casteljau subdivision);
    (ii) exact Taylor expansion at the midpoint c of dyadic cells [c-r, c+r]: a_0 - sum_j |a_j| r^j > 0.
All arithmetic is exact (Python Fractions); no floating point is used in this file.
Usage: python elec_verify.py certs/elec25.json [...]
"""
import json
import sys
from fractions import Fraction
from math import comb


def legendre_monomial(K):
    """P_0..P_K as lists of Fraction coefficients in t (index = power), exact three-term recurrence."""
    P = [[Fraction(1)], [Fraction(0), Fraction(1)]]
    for k in range(1, K):
        a = [Fraction(0)] + [Fraction(2 * k + 1, k + 1) * c for c in P[k]]
        b = P[k - 1] + [Fraction(0)] * (len(a) - len(P[k - 1]))
        P.append([x - Fraction(k, k + 1) * y for x, y in zip(a, b)])
    return P[: K + 1]


def poly_add(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)]


def poly_mul(p, q):
    r = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                r[i + j] += a * b
    return r


def g_poly(h):
    """Coefficients (in s) of g(s) = 1 - s * h(1 - s^2/2), h given in the Legendre basis."""
    K = len(h) - 1
    P = legendre_monomial(K)
    c = [Fraction(0)] * (K + 1)  # monomial coefficients of h(t)
    for k, hk in enumerate(h):
        for j, pj in enumerate(P[k]):
            c[j] += hk * pj
    sub = [Fraction(1), Fraction(0), Fraction(-1, 2)]  # 1 - s^2/2
    q = [c[K]]
    for j in range(K - 1, -1, -1):  # Horner
        q = poly_add(poly_mul(q, sub), [c[j]])
    g = poly_add([Fraction(1)], [Fraction(0)] + [-x for x in q])
    return g


def taylor_positive(g, max_depth=60):
    """Prove g > 0 on [0, 2] by exact Taylor bounds on dyadic cells [c - r, c + r]:
    g(c + e) = sum_j a_j e^j (exact Taylor shift), and g >= a_0 - sum_{j>=1} |a_j| r^j on the cell."""
    d = len(g) - 1
    cells, leaves, deepest = [(Fraction(1), Fraction(1), 0)], 0, 0
    while cells:
        c, r, depth = cells.pop()
        a = list(g)
        for i in range(d):  # Taylor shift x -> x + c (Horner / synthetic division)
            for k in range(d - 1, i - 1, -1):
                a[k] += c * a[k + 1]
        low, rp = a[0], Fraction(1)
        for j in range(1, d + 1):
            rp *= r
            low -= abs(a[j]) * rp
        if low > 0:
            leaves += 1
            deepest = max(deepest, depth)
            continue
        if a[0] <= 0 or depth >= max_depth:
            return False, leaves, depth
        cells.append((c - r / 2, r / 2, depth + 1))
        cells.append((c + r / 2, r / 2, depth + 1))
    return True, leaves, deepest


def bernstein_positive(g, max_depth=60):
    """Prove g > 0 on [0, 2]: Bernstein coefficients on each subinterval are all > 0 (exact)."""
    d = len(g) - 1
    a = [x * 2 ** i for i, x in enumerate(g)]  # g(2x), x in [0, 1]
    b = [sum(Fraction(comb(i, j), comb(d, j)) * a[j] for j in range(i + 1)) for i in range(d + 1)]
    stack, leaves, deepest = [(b, 0)], 0, 0
    while stack:
        b, depth = stack.pop()
        if min(b) > 0:
            leaves += 1
            deepest = max(deepest, depth)
            continue
        if b[0] <= 0 or b[-1] <= 0 or depth >= max_depth:
            return False, leaves, depth  # endpoint value <= 0 or no proof found
        # de Casteljau split at the midpoint
        left, right, cur = [b[0]], [b[-1]], b
        for _ in range(d):
            cur = [(cur[i] + cur[i + 1]) / 2 for i in range(len(cur) - 1)]
            left.append(cur[0])
            right.append(cur[-1])
        stack.append((left, depth + 1))
        stack.append((right[::-1], depth + 1))
    return True, leaves, deepest


def verify(path):
    C = json.load(open(path))
    N = int(C["N"])
    h = [Fraction(x) for x in C["h"]]
    assert all(x >= 0 for x in h[1:]), "h_k >= 0 for k >= 1 violated"
    bound = (N * N * h[0] - N * sum(h)) / 2
    assert bound == Fraction(C["bound"]), "stored bound does not match the formula"
    g = g_poly(h)
    ok1, leaves1, depth1 = bernstein_positive(g)
    ok2, leaves2, depth2 = taylor_positive(g)
    return C["instance"], N, len(h) - 1, bound, (ok1, leaves1, depth1), (ok2, leaves2, depth2)


if __name__ == "__main__":
    allok = True
    for p in sys.argv[1:]:
        name, N, K, bound, bern, tay = verify(p)
        allok &= bern[0] and tay[0]
        print(f"{name}: N={N} K={K} bound={float(bound):.6f} = {bound.numerator}/{bound.denominator}\n"
              f"   g>0 on [0,2]: bernstein ok={bern[0]} (cells {bern[1]}, depth {bern[2]}); "
              f"taylor ok={tay[0]} (cells {tay[1]}, depth {tay[2]})")
    print("ALL CERTIFIED" if allok else "FAILED")
    sys.exit(0 if allok else 1)
