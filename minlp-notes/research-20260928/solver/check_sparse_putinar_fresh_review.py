"""Independent exact checks of the squared-kernel algebra, not a proof.

Uses only rational arithmetic in the Chebyshev basis. The main kernel is
constructed by integration of its square, independently of identity (16).
"""

from fractions import Fraction as F


def add(a, b):
    result = a.copy()
    for k, value in b.items():
        result[k] = result.get(k, F(0)) + value
    return {k: v for k, v in result.items() if v}


def scale(a, c):
    return {k: c * v for k, v in a.items() if c * v}


def multiply(a, b):
    result = {}
    for i, ai in a.items():
        for j, bj in b.items():
            half = ai * bj / 2
            for k in (i + j, abs(i - j)):
                result[k] = result.get(k, F(0)) + half
    return {k: v for k, v in result.items() if v}


def power(a, n):
    result = {0: F(1)}
    for _ in range(n):
        result = multiply(result, a)
    return result


def norm(a):
    return sum(map(abs, a.values()), F(0))


def evaluate(a, x):
    degree = max(a, default=0)
    cheb = [F(1), x]
    for k in range(2, degree + 1):
        cheb.append(2 * x * cheb[-1] - cheb[-2])
    return sum((v * cheb[k] for k, v in a.items()), F(0))


def squared_kernel_image(s, k):
    # S(x,y) = sum_j b_j T_j(x)T_j(y). Integrate T_k(y)S(x,y)^2.
    b = [F(1)] + [2 * (1 - F(j, s)) for j in range(1, s)]
    result = {}
    for i in range(s):
        for j in range(s):
            product = multiply({i: F(1)}, {j: F(1)})
            integral = product.get(k, F(0)) * (1 if k == 0 else F(1, 2))
            result = add(result, scale(product, b[i] * b[j] * integral))
    return result


def main():
    kernel_identities = 0
    normalization_checks = 0
    approximation_checks = 0
    for s in range(2, 10):
        C = F(2 * s * s + 1, 3 * s)
        M = squared_kernel_image(s, 0)
        z = add({0: F(1)}, scale(M, -1 / C))
        assert norm(z) == (C - 1) / C
        assert evaluate(M, F(1)) == C
        for k in range(s + 1):
            a = lambda j: min(F(j, s), F(1))
            lhs = add(squared_kernel_image(s, k), scale(multiply(M, {k: F(1)}), -1))
            rhs = {k: -a(k) ** 2} if k else {}
            for j in range(1, s + 1):
                rhs = add(rhs, scale(multiply({j: F(1)}, {j + k: F(1)}), -(a(j + k) - a(j)) ** 2))
            for j in range(1, k):
                rhs = add(rhs, scale(multiply({j: F(1)}, {k - j: F(1)}), -F(1, 2) * (a(k - j) - a(j)) ** 2))
            assert lhs == rhs, (s, k)
            assert norm(lhs) <= F(k * k, s * s) + F(3 * k * k, 2 * s)
            kernel_identities += 1

        for N in (2, 4, 6):
            D = 2 * (s - 1) * (N + 1)
            delta = F(1, 2 ** (N + 1))
            p = {}
            for j in range(N + 1):
                p = add(p, scale(power(z, j), 1 / C))
            # Check the polynomial SOS identity, separately from the geometric sum.
            sos = add({0: F(1)}, power(z, N))
            for j in range(N // 2):
                sos = add(sos, multiply(power(z, 2 * j), power(add({0: F(1)}, z), 2)))
            assert p == scale(sos, 1 / (2 * C))
            n = multiply(p, M)
            assert n == add({0: F(1)}, scale(power(z, N + 1), -1))
            assert max(n) == D
            assert norm(p) <= F(N + 1) / C
            residual = add(n, {0: F(-1)})
            assert norm(residual) ** 2 <= 2 * (D + 1) * delta ** 2
            for numerator in range(-16, 17):
                x = F(numerator, 16)
                assert C / 2 <= evaluate(M, x) <= C
                assert 1 - delta <= evaluate(n, x) <= 1
            normalization_checks += 1
            for k in range(s + 1):
                error = add(multiply(p, squared_kernel_image(s, k)), {k: F(-1)})
                assert max(error, default=0) <= D
                first = F(N + 1) / C * (F(k * k, s * s) + F(3 * k * k, 2 * s))
                remainder = max(norm(error) - first, F(0))
                assert remainder ** 2 <= 2 * (D + 1) * delta ** 2
                approximation_checks += 1
    print(f"PASS: {kernel_identities} exact kernel identities; {normalization_checks} exact SOS/normalization cases; {approximation_checks} exact coefficient-error bounds")


if __name__ == "__main__":
    main()
