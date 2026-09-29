"""Targeted finite checks for the adaptive integer sign compiler proof."""

from fractions import Fraction


def main():
    samples = 0
    for bound in (4, 16, 256):
        for index in range(1001):
            value = 1 + Fraction((bound - 1) * index, 1000)
            result = 2 * bound * value / (bound + value * value)
            assert 1 <= result and result * result <= bound
            assert -2 * bound * value / (bound + value * value) == -result
            samples += 1
    for size in range(1, 101):
        assert 2 ** (2 * size + 4) > 2 + size * (2**size + 2)
    for value in (Fraction(1), Fraction(5, 4), Fraction(3, 2), Fraction(7, 4), Fraction(2)):
        result = 2 * value / (1 + value * value)
        assert Fraction(4, 5) <= result <= 1
        for _ in range(5):
            successor = 2 * result / (1 + result * result)
            assert 1 - successor <= (1 - result) ** 2
            result = successor
    print(f"PASS: {samples} rational range samples; 100 error-budget inequalities; 25 refinement steps.")


if __name__ == "__main__":
    main()
