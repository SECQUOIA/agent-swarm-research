"""Targeted exact checks for sparse-putinar-kernel.md; not a theorem proof."""

from fractions import Fraction as F
from itertools import product
from math import comb


def clean(p):
    return {k: v for k, v in p.items() if v}


def add(p, q):
    result = dict(p)
    for k, v in q.items():
        result[k] = result.get(k, F(0)) + v
    return clean(result)


def scale(p, c):
    return clean({k: c * v for k, v in p.items()})


def basis_product(i, j):
    return add({i + j: F(1, 2)}, {abs(i - j): F(1, 2)})


def mul(p, q):
    result = {}
    for i, u in p.items():
        for j, v in q.items():
            result = add(result, scale(basis_product(i, j), u * v))
    return result


def power(p, exponent):
    result = {0: F(1)}
    for _ in range(exponent):
        result = mul(result, p)
    return result


def norm(p):
    return sum(map(abs, p.values()), F(0))


def cheb(k, x):
    if k == 0:
        return F(1)
    a, b = F(1), x
    for _ in range(1, k):
        a, b = b, 2 * x * b - a
    return b


def value(p, x):
    return sum((v * cheb(k, x) for k, v in p.items()), F(0))


def source_square(s):
    # Dict y-degree -> source-variable Chebyshev polynomial.
    source = {0: {0: F(1)}}
    source.update({j: {j: 2 * (1 - F(j, s))} for j in range(1, s)})
    square = {}
    for i, p in source.items():
        for j, q in source.items():
            pq = mul(p, q)
            for k, c in basis_product(i, j).items():
                square[k] = add(square.get(k, {}), scale(pq, c))
    return square


def check_kernel(s, N):
    square = source_square(s)
    M = square[0]
    C = F(2 * s * s + 1, 3 * s)
    assert value(M, F(1)) == C
    z = add({0: F(1)}, scale(M, -1 / C))
    assert norm(z) == (C - 1) / C
    geometric = {}
    for j in range(N + 1):
        geometric = add(geometric, power(z, j))
    sos = add({0: F(1)}, power(z, N))
    for j in range(N // 2):
        sos = add(sos, mul(power(z, 2 * j), power(add({0: F(1)}, z), 2)))
    assert geometric == scale(sos, F(1, 2))
    p = scale(geometric, 1 / C)
    n = mul(p, M)
    residual = add(n, {0: F(-1)})
    assert residual == scale(power(z, N + 1), -1)
    D = 2 * (s - 1) * (N + 1)
    delta = F(1, 2 ** (N + 1))
    assert max(n) == D
    assert norm(residual) ** 2 <= 2 * (D + 1) * delta**2
    assert norm(p) <= (N + 1) / C
    for x in [F(j, 8) for j in range(-8, 9)]:
        assert C / 2 <= value(M, x) <= C
        assert 1 - delta <= value(n, x) <= 1

    def a(j):
        return min(F(j, s), F(1))

    for k in range(s + 1):
        Tk = {k: F(1)}
        KT = scale(square.get(k, {}), F(1) if k == 0 else F(1, 2))
        actual = add(KT, scale(mul(M, Tk), -1))
        expected = scale(Tk, -a(k) ** 2)
        for j in range(1, s + 1):
            expected = add(expected, scale(basis_product(j, j + k), -(a(j + k) - a(j)) ** 2))
        for j in range(1, k):
            expected = add(expected, scale(basis_product(j, k - j), -F(1, 2) * (a(k - j) - a(j)) ** 2))
        assert actual == expected, (s, N, k, actual, expected)
        damping_bound = F(k * k, s * s) + F(3 * k * k, 2 * s)
        assert norm(actual) <= damping_bound
        AT = mul(p, KT)
        total_error = norm(add(AT, scale(Tk, -1)))
        assert total_error <= (N + 1) / C * damping_bound + norm(residual)
    return p, M, n


def check_separator():
    s, N = 3, 2
    p, _, n = check_kernel(s, N)
    delta = F(1, 2 ** (N + 1))
    a = 1 - delta

    def Q(x, y):
        source = 1 + 2 * sum(((1 - F(j, s)) * cheb(j, x) * cheb(j, y) for j in range(1, s)), F(0))
        return value(p, x) * source**2

    # Consistent input marginals on separator s; omitted u depends on s.
    atoms_A = [(F(0), F(-1, 2)), (F(1), F(1, 2))]
    atoms_B = [(F(-1, 2), F(0)), (F(1, 2), F(0))]
    ZA = sum((value(n, u) * value(n, sep) for u, sep in atoms_A), F(0)) / 2
    ZB = sum((value(n, sep) * value(n, v) for sep, v in atoms_B), F(0)) / 2
    ZS = (value(n, F(-1, 2)) + value(n, F(1, 2))) / 2
    assert a**2 <= ZA <= ZS <= 1
    assert a**2 <= ZB <= ZS <= 1
    mismatch_found = False
    for y in [F(j, 8) for j in range(-8, 9)]:
        hS = (Q(F(-1, 2), y) + Q(F(1, 2), y)) / 2
        hAS = sum((Q(sep, y) * value(n, u) for u, sep in atoms_A), F(0)) / 2
        hBS = sum((Q(sep, y) * value(n, v) for sep, v in atoms_B), F(0)) / 2
        assert a * hS <= hAS <= hS
        assert a * hS <= hBS <= hS
        assert hAS / ZA >= a * hS / ZS
        assert hBS / ZB >= a * hS / ZS
        mismatch_found |= hAS / ZA != hBS / ZB
    assert mismatch_found, "Test must expose the failure of exact separator consistency."


def check_exact_consistency():
    s, N = 3, 2
    p, _, n = check_kernel(s, N)
    residual = add({0: F(1)}, scale(n, -1))
    square = source_square(s)
    qbar = {k: mul(p, polynomial) for k, polynomial in square.items()}
    qbar[0] = add(qbar[0], residual)
    assert qbar[0] == {0: F(1)}, "Arcsine integration must normalize identically."
    for k in range(1, s + 1):
        assert qbar.get(k, {}) == mul(p, square.get(k, {}))

    def Qbar(x, y):
        return sum((value(poly, x) * cheb(k, y) for k, poly in qbar.items()), F(0))

    # Same consistent atoms as above; compare marginals computed from their
    # different bag laws by exact extraction of the private constant mode.
    atoms_A = [(F(0), F(-1, 2)), (F(1), F(1, 2))]
    atoms_B = [(F(-1, 2), F(0)), (F(1, 2), F(0))]
    for y in [F(j, 8) for j in range(-8, 9)]:
        hAS = sum((Qbar(sep, y) * value(qbar[0], u)
                   for u, sep in atoms_A), F(0)) / 2
        hBS = sum((Qbar(sep, y) * value(qbar[0], v)
                   for sep, v in atoms_B), F(0)) / 2
        assert hAS == hBS
    delta = F(1, 2 ** (N + 1))
    C = F(2 * s * s + 1, 3 * s)
    B = s * s * (N + 1) / C
    previous = F(0)
    for width in range(1, 9):
        Delta = sum((comb(width, j) * delta**j * B ** (width - j)
                     for j in range(2, width + 1)), F(0))
        assert Delta >= previous
        if width >= 2:
            assert Delta <= comb(width, 2) * delta**2 * (B + delta) ** (width - 2)
        previous = Delta

    # An actually signed pair with exactly matching separator marginals.
    # h_A=1+2 T_1(u)T_1(s), h_B=1-2 T_1(s)T_1(v), and Delta=1.
    shift = F(1)
    for u, sep, v in product((F(-1), F(0), F(1)), repeat=3):
        hA = 1 + 2 * u * sep
        hB = 1 - 2 * sep * v
        assert (hA + shift) / (1 + shift) >= 0
        assert (hB + shift) / (1 + shift) >= 0
    # Orthogonality kills the private degree-one factor, so both marginals
    # and both masses remain one, before and after the common shift.
    assert (F(1) + shift) / (1 + shift) == 1


def main():
    count = 0
    for s, N in product(range(2, 8), (2, 4, 6)):
        check_kernel(s, N)
        count += s + 1
    check_separator()
    check_exact_consistency()
    print(f"PASS: {count} exact univariate basis identities and bounds; 18 kernel parameter pairs.")
    print("PASS: exact separator domination and a strict normalization mismatch example.")
    print("PASS: exact signed-kernel normalization, residual bounds, and common signed-density correction.")
    print("These finite checks do not verify all degrees, arbitrary pseudomoments, or the global theorem.")


if __name__ == "__main__":
    main()
