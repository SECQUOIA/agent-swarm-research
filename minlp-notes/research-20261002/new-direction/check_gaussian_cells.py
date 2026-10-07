"""Targeted diagnostics for the Gaussian cell-count proof, not a QP solver."""

from fractions import Fraction as F
from itertools import product
from math import ceil, erf, exp, floor, log2, pi, sqrt

import mpmath as mp
import sympy as sp


def check_weighted_lattices():
    count = 0
    for c, width, step, offset in product(
        (3, 7, 21), (0, 0.3, 7), (0.01, 0.3, 2, 50), (0, 0.17, 0.99)
    ):
        # Include coarse meshes, zero-width cores and shifted lattices.
        left, right = -c * step / 2, width + c * step / 2
        lo = floor((left - 12) / step - offset)
        hi = ceil((right + 12) / step - offset)
        total = 0.0
        for j in range(lo, hi + 1):
            z = (j + offset) * step
            distance = max(left - z, z - right, 0)
            total += min(1, c * step * exp(-distance**2 / 2) / sqrt(2 * pi))
        bound = c * width / sqrt(2 * pi) + 2 * c + 4
        assert total <= bound + 1e-9, (c, width, step, offset, total, bound)
        # The omitted Gaussian tails are less than 1e-27, far below slack.
        assert bound - total > 1e-6
        count += 1
    return count


def check_covariance():
    count = 0
    frames = [
        sp.Matrix([[sp.Rational(3, 5), sp.Rational(4, 5), 0]]),
        sp.Matrix([[sp.Rational(3, 5), sp.Rational(4, 5), 0], [0, 0, 1]]),
        sp.Matrix([[sp.Rational(4, 5), 0, 0], [0, sp.Rational(9, 10), 0]]),
        sp.Matrix([[sp.Rational(3, 5), sp.Rational(3, 5), 0], [0, 0, 1]]),
    ]
    for t in frames:
        g = t * t.T
        d = g.inv() * t
        residual = sp.eye(t.cols) - t.T * d
        assert d * residual.T == sp.zeros(t.rows, t.cols)
        assert d * d.T == g.inv()
        assert (g - sp.eye(t.rows) / 2).is_positive_semidefinite
        assert (sp.eye(t.rows) - g).is_positive_semidefinite
        count += 1
    return count


def exp_weight(z, bits):
    """One exact-rational Taylor/rounding implementation of the sampler weight."""
    t = z * z / 2
    s = 0
    while t > F(1, 2):
        t /= 2
        s += 1
    precision = bits + s + 8
    term = value = F(1)
    for j in range(1, precision + 5):
        term *= -t / j
        value += term
    denominator = 1 << precision

    def round_clamp(x):
        return F(max(0, min(denominator, x.numerator * denominator // x.denominator)), denominator)

    value = round_clamp(value)
    for _ in range(s):
        value = round_clamp(value * value)
    return value


def check_weights():
    mp.mp.dps = 120
    count = 0
    for bits, z in product((8, 32, 80), (F(0), F(1, 10), F(1), F(7, 3), F(20), F(1000))):
        w = exp_weight(z, bits)
        actual = mp.exp(-(mp.mpf(z.numerator) / z.denominator) ** 2 / 2)
        error = abs(mp.mpf(w.numerator) / w.denominator - actual)
        assert 0 <= w <= 1
        assert error < mp.mpf(2) ** -bits
        count += 1
    return count


def check_finite_laws():
    # Small fully enumerable analogues check normalization and KS bookkeeping.
    # The theorem's much finer grid is not enumerated by its sampler.
    count = 0
    for radius, nodes, bits in product((3, 5, 8), (128, 1024), (8, 16)):
        xs = [-radius + 2 * radius * j / (nodes - 1) for j in range(nodes)]
        true_weights = [exp(-x * x / 2) for x in xs]
        weights = [floor(w * 2**bits) / 2**bits for w in true_weights]
        norm, acc = sum(weights), sum(weights) / nodes
        assert acc >= 1 / (16 * radius)
        cdf = error = 0.0
        for x, w in zip(xs, weights):
            target = (1 + erf(x / sqrt(2))) / 2
            error = max(error, abs(cdf - target), abs(cdf + w / norm - target))
            cdf += w / norm
        mesh = 2 * radius / (nodes - 1)
        tail = 1 - erf(radius / sqrt(2))
        bound = 10 * radius * mesh + 10 * radius * 2**-bits + tail
        assert error <= bound + 1e-12
        count += 1
    return count


def ceil_log2_fraction(x):
    value = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    if F(1 << value) < x:
        value += 1
    return value


def check_budget_loop():
    counts = []
    for n, k, m, height in ((3, 1, 4, 2), (20, 4, 60, 100), (100, 20, 300, 1000)):
        rb, fallback = 1 << m, max(2, 1 << m)
        kb = rb * (m + n + 1)
        csec = (2 * (2 * k + 1) * rb + 1) * (8 * k + 2)
        hessian = 1 << height
        for t in range(1000):
            rs = 1 << t
            width = 1 + 4 * n * rs
            j = ceil_log2_fraction(F(width * 4 * k * kb * fallback * (1 + hessian)))
            qall = (j + 1) * ((1 << j) + 1) ** k
            requirement = max(8 * n * kb * fallback, 2 * n * csec * qall)
            p = max(1, (requirement - 1).bit_length())
            if rs >= p + 20:
                assert F(2 * n * csec * qall, 1 << p) <= 1
                assert F(2 * n * kb, 1 << p) <= F(1, 4 * fallback)
                counts.append((t, j, p))
                break
        else:
            raise AssertionError("base-only budget failed to terminate")
    return counts


if __name__ == "__main__":
    print("weighted lattices:", check_weighted_lattices())
    print("exact covariance/frame identities:", check_covariance())
    print("rational exponential weights:", check_weights())
    print("enumerated finite-law KS checks:", check_finite_laws())
    print("budget (support exponent, cutoff level, precision):", check_budget_loop())
