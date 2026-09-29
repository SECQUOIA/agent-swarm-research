"""Exact checks supporting the strict-sublevel attainment counterexample."""


def v2(n):
    assert n > 0
    return (n & -n).bit_length() - 1


def main():
    x, y = 1, 0
    rows = []
    for n in range(1, 1025):
        x, y = 3 * x + 4 * y, 2 * x + 3 * y
        assert x * x - 2 * y * y == 1
        assert v2(y) == v2(n) + 1
        if n & (n - 1) == 0:
            a = n.bit_length()
            coefficient = 1 << (2 * a + 1)
            assert y % (1 << a) == 0
            w = y >> a
            assert x * x - coefficient * w * w == 1
            assert x.bit_length() >= (1 << a)
            rows.append((a, coefficient.bit_length(), n, x.bit_length()))
    print("Pell identities and valuations passed for n=1,...,1024.")
    print("a, coefficient bits, first admissible exponent, optimizer x bits:")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
