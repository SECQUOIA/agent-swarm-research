"""Finite stress checks of the manuscript's rational Jacobi invariants.

Rotation parameters use high precision; all asserted identities, contractions,
and denominator divisibilities are checked in exact rational arithmetic.
This is a supplementary check, not a proof or a certified full eigensolver.
"""

import mpmath as mp
import sympy as sp

mp.mp.dps = 220


def real(q):
    return mp.mpf(int(sp.numer(q))) / int(sp.denom(q))


tiny = sp.Rational(1, 2**120)
large = sp.Integer(2**100)
cases = [
    ("repeated diagonal", sp.eye(2), sp.Rational(1, 2**180)),
    ("tiny off-diagonal, equal diagonal", sp.Matrix([[1, tiny], [tiny, 1]]), sp.Rational(1, 2**180)),
    ("large indefinite spread", sp.Matrix([[large, tiny], [tiny, -large]]), sp.Rational(1, 2**180)),
    ("nearly equal diagonals", sp.Matrix([[1, 1], [1, 1 + tiny]]), sp.Rational(1, 2**180)),
    ("multiple updates", sp.Matrix([[4, 1, 0], [1, 4, 1], [0, 1, 4]]), sp.Rational(1, 2**10)),
]

total = 0
for name, original, sigma in cases:
    n = original.rows
    pair_count = n * (n - 1)
    magnitude = max(sp.Integer(1), sum(abs(v) for v in original))
    bits = int(mp.ceil(mp.log(real(128 * pair_count * magnitude / sigma), 2)))
    scale = 2**bits
    current, vectors = original.copy(), sp.eye(n)
    initial_denominator = int(sp.prod(sp.denom(v) for v in original))
    matrix_denominator = initial_denominator
    vector_denominator = 1
    limit = int(mp.ceil(2 * pair_count * mp.log(real(magnitude / sigma)))) + 1

    def off_squared(matrix):
        return sum(matrix[i, j] ** 2 for i in range(n) for j in range(n) if i != j)

    steps = 0
    while off_squared(current) > sigma**2:
        assert steps < limit
        old_off = off_squared(current)
        i, j = max(((i, j) for i in range(n) for j in range(i + 1, n)), key=lambda pair: abs(current[pair[0], pair[1]]))
        angle = mp.atan2(2 * real(current[i, j]), real(current[j, j] - current[i, i])) / 2
        if angle > mp.pi / 4:
            angle -= mp.pi / 2
        elif angle < -mp.pi / 4:
            angle += mp.pi / 2
        numerator = int(mp.nint(mp.tan(angle / 2) * scale))
        rotation_denominator = scale**2 + numerator**2
        cosine = sp.Rational(scale**2 - numerator**2, rotation_denominator)
        sine = sp.Rational(2 * scale * numerator, rotation_denominator)
        rotation = sp.eye(n)
        rotation[i, i] = rotation[j, j] = cosine
        rotation[i, j], rotation[j, i] = sine, -sine
        current = rotation.T * current * rotation
        vectors = vectors * rotation
        steps += 1
        assert rotation_denominator.bit_length() <= 2 * bits + 2
        matrix_denominator *= rotation_denominator**2
        vector_denominator *= rotation_denominator
        assert all(matrix_denominator % int(sp.denom(v)) == 0 for v in current)
        assert all(vector_denominator % int(sp.denom(v)) == 0 for v in vectors)
        assert matrix_denominator.bit_length() <= initial_denominator.bit_length() + 2 * steps * (2 * bits + 2)
        assert off_squared(current) <= (1 - sp.Rational(3, 4 * pair_count)) ** 2 * old_off
    assert vectors.T * vectors == sp.eye(n)
    assert vectors * current * vectors.T == original
    assert sum(v**2 for v in current) == sum(v**2 for v in original)
    total += steps
    print(f"PASS: {name}; {steps} updates; rotation precision {bits} bits")

print(f"PASS: {len(cases)} stress cases; {total} exact contractions and denominator checks")
