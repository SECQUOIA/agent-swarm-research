"""Exact rational checks of the penalty proof's radial repair estimates.

Checks a mathematical estimate, not the numerical behavior of an enormous
penalty coefficient in a floating-point optimizer.
"""
from fractions import Fraction as F
from random import Random


def functional(x, a):
    total, mass = sum(x), sum(ai * xi for ai, xi in zip(a, x))
    return mass * (total - 1) - total


def radial(x, a):
    if functional(x, a) <= 0:
        return x
    total, mass = sum(x), sum(ai * xi for ai, xi in zip(a, x))
    theta = (1 + total / mass) / total
    assert 0 < theta < 1
    return [theta * value for value in x]


def main():
    rng = Random(762098)
    repaired = 0
    for _ in range(500):
        n = rng.randint(1, 7)
        a = [F(rng.randint(11, 100), 10) for _ in range(n)]
        vectors = []
        for _ in range(2):
            raw = [F(rng.randint(0, 100)) for _ in range(n)]
            if not sum(raw):
                raw[0] = 1
            total = F(rng.randint(0, 200), 100)
            vectors.append([v * total / sum(raw) for v in raw])
        x = radial(vectors[0], a)
        candidate = vectors[1]
        corrected = radial(candidate, a)
        L = 3 * max(a) + 1
        distance = sum(abs(v - w) for v, w in zip(x, candidate))
        assert functional(x, a) <= 0
        assert functional(corrected, a) <= 0
        assert max(F(0), functional(candidate, a)) <= L * distance
        removed = sum(abs(v - w) for v, w in zip(candidate, corrected))
        assert removed <= L * distance
        assert sum(abs(v - w) for v, w in zip(x, corrected)) <= (1 + L) * distance
        if removed:
            total, mass = sum(candidate), sum(ai * xi for ai, xi in zip(a, candidate))
            assert total > 1 and mass > 1
            assert removed == functional(candidate, a) / mass
            assert functional(corrected, a) == 0
            repaired += 1
    # The coarse constant is explicitly constructible with controlled bits,
    # including when the integer row entries themselves have many bits.
    for n in [1, 2, 10, 100]:
        for k in [1, 17, 2**257 + 1]:
            h = n * (n * k) ** (n - 1)
            assert h.bit_length() <= n.bit_length() + (n - 1) * (n.bit_length() + k.bit_length())
    print(f'PASS: 500 exact rational radial/error estimates, including {repaired} nontrivial repairs.')
    print('PASS: 12 explicit Hoffman-constant encoding bounds, including 258-bit coefficients.')


if __name__ == '__main__':
    main()
