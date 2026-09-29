"""Targeted exact checks for the binary-leaf star hull argument.

These verify identities, representative clipping branches, and the sparse-RLT
counterexample. They do not prove the general theorem or establish novelty.
"""

from dataclasses import dataclass
from fractions import Fraction as F

import sympy as sp


@dataclass(frozen=True)
class Star:
    a: F
    b: F
    c: F
    e: tuple[F, ...]
    k: tuple[F, ...]

    def value(self, t):
        return self.a * t * t + self.b * t + self.c - sum(
            max(F(0), k * t - e) for e, k in zip(self.e, self.k)
        )

    def minimum(self):
        knots = sorted(
            {F(0), F(1)}
            | {e / k for e, k in zip(self.e, self.k) if k and 0 < e < k}
        )
        candidates = list(knots)
        if self.a > 0:
            for left, right in zip(knots, knots[1:]):
                midpoint = (left + right) / 2
                active_k = sum(k for e, k in zip(self.e, self.k) if e < k * midpoint)
                stationary = (active_k - self.b) / (2 * self.a)
                if left <= stationary <= right:
                    candidates.append(stationary)
        return min(self.value(t) for t in candidates)

    def complement(self):
        total_k, total_e = sum(self.k), sum(self.e)
        return Star(
            self.a,
            total_k - 2 * self.a - self.b,
            self.a + self.b + self.c + total_e - total_k,
            tuple(k - e for e, k in zip(self.e, self.k)),
            self.k,
        )


def lower_correction(q):
    assert q.a > 0
    assert all(0 < e < k for e, k in zip(q.e, q.k))
    if q.b <= 0:
        return q, "skip"
    if q.b >= sum(q.k) - sum(q.e):
        assert q.minimum() == q.c
        return None, "endpoint"
    order = sorted(range(len(q.e)), key=lambda i: q.e[i] / q.k[i])
    active_e = active_k = F(0)
    tau = None
    for i in order:
        active_e += q.e[i]
        active_k += q.k[i]
        if active_k <= q.b:
            continue
        candidate = active_e / (active_k - q.b)
        if 0 < candidate < 1 and sum(
            max(F(0), k - e / candidate) for e, k in zip(q.e, q.k)
        ) == q.b:
            tau = candidate
            break
    assert tau is not None
    multipliers = tuple(max(F(0), k - e / tau) for e, k in zip(q.e, q.k))
    assert sum(multipliers) == q.b
    result = Star(q.a, F(0), q.c, q.e, tuple(k - lam for k, lam in zip(q.k, multipliers)))
    assert all(0 < e < k for e, k in zip(result.e, result.k))
    assert result.minimum() == q.minimum()
    # Check the piecewise identity at every old/new breakpoint and a midpoint
    # of every resulting interval. The written proof establishes all t.
    knots = sorted(
        {F(0), tau, F(1)}
        | {e / k for e, k in zip(q.e, q.k) if 0 < e < k}
        | {e / k for e, k in zip(result.e, result.k) if 0 < e < k}
    )
    probes = knots + [(left + right) / 2 for left, right in zip(knots, knots[1:])]
    for t in probes:
        expected = q.a * t * t + q.c if t <= tau else q.value(t)
        assert result.value(t) == expected
    return result, "correct"


def check_clipping_cases():
    cases = {
        "neither": (F(3), F(-1, 4), "skip", "skip"),
        "lower_only": (F(2), F(1, 2), "correct", "skip"),
        "upper_only": (F(11, 10), F(-1, 4), "skip", "correct"),
        "both": (F(3, 4), F(1, 2), "correct", "correct"),
        "lower_endpoint": (F(1), F(2), "endpoint", None),
        "lower_endpoint_equality": (F(1), F(7, 4), "endpoint", None),
        "upper_endpoint": (F(1, 4), F(-2), "skip", "endpoint"),
    }
    for label, (a, b, lower_branch, upper_branch) in cases.items():
        q = Star(a, b, F(2, 7), (F(1, 4), F(1)), (F(1), F(2)))
        assert q.complement().complement() == q
        assert q.complement().minimum() == q.minimum()
        result, branch = lower_correction(q)
        assert branch == lower_branch, label
        if result is None:
            continue
        comp = result.complement()
        transformed, branch = lower_correction(comp)
        assert branch == upper_branch, label
        if transformed is None:
            continue
        final = transformed.complement()
        assert final.b <= 0
        assert sum(final.k) - final.b <= 2 * final.a
        assert final.minimum() == q.minimum()
    for b in (F(-3), F(-1), F(0), F(1)):
        q = Star(F(1), b, F(0), (), ())
        result, _ = lower_correction(q)
        if result is not None:
            transformed, _ = lower_correction(result.complement())
            if transformed is not None:
                final = transformed.complement()
                assert final.b <= 0 and -final.b <= 2 * final.a
                assert final.minimum() == q.minimum()
    print("PASS: seven exact clipping branches, complemented minima, empty-leaf cases")


def check_symbolic_identities():
    a, b, c, t = sp.symbols("a b c t", nonzero=True)
    y = sp.symbols("y0:3")
    e = sp.symbols("e0:3")
    k = sp.symbols("k0:3")
    q = a * t**2 + b * t + c + sum((e[i] - k[i] * t) * y[i] for i in range(3))
    endpoint = a * t**2 + (b - sum(k) + sum(e)) * t
    endpoint += sum((k[i] - e[i]) * t * (1 - y[i]) + e[i] * (1 - t) * y[i] for i in range(3))
    assert sp.expand(q - c - endpoint) == 0
    r = c - b**2 / (4 * a)
    r += sum((e[i] + b * k[i] / (2 * a) - k[i] ** 2 / (4 * a)) * y[i] for i in range(3))
    r -= sum(k[i] * k[j] * y[i] * y[j] / (2 * a) for i in range(3) for j in range(i + 1, 3))
    square = a * (t + (b - sum(k[i] * y[i] for i in range(3))) / (2 * a)) ** 2
    diagonal = sum(k[i] ** 2 * y[i] * (1 - y[i]) / (4 * a) for i in range(3))
    assert sp.expand(q - square - r - diagonal) == 0
    print("PASS: general three-leaf endpoint and square polynomial identities")


def check_sparse_counterexample():
    vectors = ((F(1), F(0)), (F(3, 8), F(1, 10)), (F(4, 5), F(2, 5)), (F(1, 5), F(2, 5)))
    gram = [[sum(a * b for a, b in zip(left, right)) for right in vectors] for left in vectors]
    for i, j in ((1, 1), (2, 2), (3, 3), (1, 2), (1, 3)):
        assert max(F(0), gram[0][i] + gram[0][j] - 1) <= gram[i][j]
        assert gram[i][j] <= min(gram[0][i], gram[0][j])
    assert gram[2][2] == gram[0][2] and gram[3][3] == gram[0][3]
    objective = gram[1][1] - gram[0][1] / 2 + F(1, 16)
    objective += F(5, 64) * gram[0][2] + F(7, 64) * gram[0][3]
    objective -= (gram[1][2] + gram[1][3]) / 4
    assert objective == -F(3, 800)
    assert gram[2][3] == F(8, 25) > gram[0][3]
    t, y, z = sp.symbols("t y z")
    q = t**2 - t / 2 + sp.Rational(1, 16) + 5 * y / 64 + 7 * z / 64 - t * (y + z) / 4
    cert = (t - sp.Rational(1, 4) - (y + z) / 8) ** 2
    cert += (y * (1 - y) + z * (1 - z)) / 64 + z * (1 - y) / 32
    assert sp.expand(q - cert) == 0
    assert q.subs({t: sp.Rational(1, 4), y: 0, z: 0}) == 0
    print("PASS: sparse-RLT Gram feasibility, binary leaf diagonals, exact gap -3/800")


def check_upper_only_scope():
    mu_i, mu_j, product = sp.symbols("mu_i mu_j product")
    complemented_product = 1 - mu_i - mu_j + product
    assert sp.expand((1 - mu_i) - complemented_product - (mu_j - product)) == 0
    assert sp.expand((1 - mu_j) - complemented_product - (mu_i - product)) == 0
    means = (F(1, 4), F(1, 4))
    second = ((F(1, 4), -F(1, 16)), (-F(1, 16), F(1, 4)))
    for i in range(2):
        for j in range(2):
            assert second[i][j] <= min(means[i], means[j])
    covariance = sp.Matrix(
        [[sp.Rational(second[i][j] - means[i] * means[j]) for j in range(2)] for i in range(2)]
    )
    assert set(covariance.eigenvals()) == {sp.Rational(1, 16), sp.Rational(5, 16)}
    assert second[0][1] == -F(1, 16)
    print("PASS: simultaneous complementation preserves upper RLT; arbitrary-sign gap -1/16")


if __name__ == "__main__":
    check_symbolic_identities()
    check_clipping_cases()
    check_sparse_counterexample()
    check_upper_only_scope()
    print("Unchecked: the full analytic theorem, moment-hull separation, and novelty")
