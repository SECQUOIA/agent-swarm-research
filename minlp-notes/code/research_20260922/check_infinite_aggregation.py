"""Exact Gram witnesses for the aggregation obstruction, not a proof of HHC."""

from fractions import Fraction as F


def gram(tau, shift=F(0)):
    return F(1) - F(1, 10) / tau, F(2, 5) - shift, F(1) - tau / 10


def value(tau, ray, shift=F(0)):
    a, c, b = gram(tau, shift)
    return ray * (a - 1) + (b - 1) / ray + 2 * (F(1, 2) - c)


def main():
    count = 0
    rays = [F(1) + F(j, 50) for j in range(51)]
    for tau in rays:
        a, c, b = gram(tau)
        assert a > 0 and b > 0 and a * b - c * c > 0
        for ray in rays:
            v = value(tau, ray)
            assert v == -(ray - tau) ** 2 / (10 * tau * ray)
            assert (v == 0) == (ray == tau)
            count += 1
    for n in (1, 2, 4, 8, 16, 32):
        chosen = [F(1) + F(j, n) for j in range(n + 1)]
        tau = F(1) + F(1, 2 * n)
        slack = min(-value(tau, ray) for ray in chosen)
        shift = min(F(1, 10), slack / 4)
        a, c, b = gram(tau, shift)
        assert a * b - c * c > 0
        assert all(value(tau, ray, shift) < 0 for ray in chosen)
        assert value(tau, tau, shift) > 0
    print(f"PASS: {count} exact ray identities and 6 finite-family "
          "outside witnesses; no numerical square roots")


if __name__ == "__main__":
    main()
