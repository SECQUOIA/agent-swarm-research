"""Exact diagnostics for row normalization and anisotropic closure meshes.

This is not a general separable-MINLP solver. Small-matrix PSD checks use
principal minors only as a diagnostic, not as the polynomial algorithm.
"""

from fractions import Fraction as Q
from itertools import combinations
from math import lcm

import sympy as sp

from check_spectral_normalization import psd


def ceil_log2(x):
    x = Q(x)
    exponent = x.numerator.bit_length() - x.denominator.bit_length()
    power = Q(2) ** exponent
    return exponent + (power < x)


def rational_rotation(gram):
    n = gram.rows
    height = max(sum(abs(gram[i, j]) for j in range(n)) for i in range(n))
    denominator = lcm(*(int(x.q) for x in gram))
    mu = 1 / (sp.Integer(denominator) ** n * height ** (n - 1))
    tolerance = mu / (64 * n)
    rotation, matrix, count = sp.eye(n), gram.copy(), 0
    while n > 1:
        p, q = max(combinations(range(n), 2), key=lambda ij: abs(matrix[ij]))
        cross = matrix[p, q]
        if abs(cross) <= tolerance:
            break
        difference = matrix[q, q] - matrix[p, p]
        endpoint = -sp.sign(cross * difference) / 2 if difference else sp.Rational(1, 2)
        lo, hi = sorted((sp.S.Zero, endpoint))

        def numerator(t):
            return cross * (1 - 6*t*t + t**4) + 2*difference*t*(1-t*t)

        sign_lo = sp.sign(numerator(lo))
        while hi - lo > tolerance / (8 * height):
            middle = (lo + hi) / 2
            sign_mid = sp.sign(numerator(middle))
            if sign_mid == 0:
                lo = hi = middle
                break
            if sign_mid == sign_lo:
                lo = middle
            else:
                hi = middle
        t = (lo + hi) / 2
        cosine, sine = (1-t*t)/(1+t*t), 2*t/(1+t*t)
        g = sp.eye(n)
        g[p, p] = g[q, q] = cosine
        g[p, q], g[q, p] = -sine, sine
        matrix = g.T * matrix * g
        rotation = rotation * g
        assert abs(matrix[p, q]) <= tolerance / 2
        count += 1
        assert count < 1000
    row_rotation = rotation.T
    assert row_rotation * row_rotation.T == sp.eye(n)
    assert row_rotation * gram * row_rotation.T == matrix
    residual = matrix - sp.diag(*matrix.diagonal())
    psd(mu / 64 * sp.eye(n) - residual)
    psd(mu / 64 * sp.eye(n) + residual)
    return row_rotation, matrix, count


def normalize(factor, alpha):
    rotation, gram, count = rational_rotation(factor * factor.T)
    scales = []
    for diagonal in gram.diagonal():
        exponent = (ceil_log2(2 * diagonal) + 1) // 2
        scale = sp.Rational(2) ** exponent
        assert 2 * diagonal <= scale**2 < 8 * diagonal
        scales.append(scale)
    diagonal = sp.diag(*scales)
    frame = diagonal.inv() * rotation * factor
    curvature = alpha * diagonal**2
    psd(frame * frame.T - sp.eye(frame.rows) / 16)
    psd(sp.eye(frame.rows) - frame * frame.T)
    assert frame.T * curvature * frame == alpha * factor.T * factor
    assert max(curvature.diagonal()) < 8 * alpha * max(gram.diagonal())
    bits = max(max(int(x.p).bit_length(), int(x.q).bit_length())
               for x in frame)
    return list(map(Q, curvature.diagonal())), count, bits


def check_mesh(curvatures):
    n = len(curvatures)
    scales = [Q(2) ** ((ceil_log2(1 / value) + 1) // 2) for value in curvatures]
    assert all(1 <= value * scale**2 < 4 for value, scale in zip(curvatures, scales))
    checked = interior = inactive = 0
    for widths in ([Q(1)] * n, [Q(2) ** (20 * (i - 1)) for i in range(n)]):
        largest = max(width / scale for width, scale in zip(widths, scales))
        for level in (0, 1, 2, 5, 10, 20, 40, 80, 120, 180):
            h = largest / (1 << level)
            subdivisions = [1 << max(0, ceil_log2(width / (scale * h)))
                            for width, scale in zip(widths, scales)]
            steps = [width / parts for width, parts in zip(widths, subdivisions)]
            b = sum(value * step**2 for value, step in zip(curvatures, steps)) / 8
            assert b <= n * h*h / 2
            assert sum(step*step for step in steps) <= h*h * sum(scales)**2
            for value, step, scale, parts in zip(curvatures, steps, scales, subdivisions):
                assert parts <= 1 << level
                assert step <= scale * h
                if parts > 1:
                    assert scale*h/2 < step
                    assert value*step + 4*b/step <= (1+8*n)*value*step
                    interior += 1
                else:
                    inactive += 1
            checked += 1
    return checked, interior, inactive


def main():
    fixtures = [
        (sp.Matrix([[1, 2]]), sp.Rational(1)),
        (sp.Matrix([[1, 1, 0], [0, sp.Rational(1, 2**20), sp.Rational(1, 2**30)]]), sp.Rational(1)),
        (sp.Matrix([[1, 2, 3], [2, 1, -1]]), sp.Rational(1, 2**40)),
        (sp.Matrix([[1, 2, 0], [0, 1, 2], [2, 0, 1]]), sp.Rational(2**30)),
    ]
    mesh_count = active = inactive = rotations = max_bits = 0
    for factor, alpha in fixtures:
        curvatures, count, bits = normalize(factor, alpha)
        rotations += count
        max_bits = max(max_bits, bits)
        a, b, c = check_mesh(curvatures)
        mesh_count, active, inactive = mesh_count+a, active+b, inactive+c
    for curvatures in ([Q(2)**-100, Q(1), Q(2)**100], [Q(2)**-101, Q(2)**99]):
        a, b, c = check_mesh(curvatures)
        mesh_count, active, inactive = mesh_count+a, active+b, inactive+c
    print(f"{len(fixtures)} exact normalizations; {rotations} rational rotations; max frame-entry bits {max_bits}")
    print(f"{mesh_count} anisotropic levels; {active} interior-coordinate bounds; {inactive} inactive-coordinate cases")


if __name__ == '__main__':
    main()
