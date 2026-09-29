"""Independent exact checks of value-free search on integer affine lines.

This tests ties, every-optimum retention, deficient-dimensional domains,
and large coordinate encodings. It does not implement or verify the cited
high-dimensional FPT feasibility algorithm.
"""

from fractions import Fraction as F
from itertools import product


def ceil(x):
    return -((-x.numerator) // x.denominator)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def search(lo, hi, base, direction, gradient, mu):
    """No objective value or optimizer is supplied to the search."""
    archive, transcript = [], []
    while lo <= hi:
        t = (lo + hi) // 2
        z = tuple(b + t * v for b, v in zip(base, direction))
        archive.append(t)
        q = gradient(z)
        if not any(q):
            return archive, transcript, t
        slope = dot(q, direction)
        # Substitute x = base + direction * u into the original strict cut.
        rhs = slope * t - mu / 4
        assert slope * t > rhs
        transcript.append((t, slope, rhs))
        if slope > 0:
            hi = min(hi, (rhs / slope).__floor__())
        elif slope < 0:
            lo = max(lo, ceil(rhs / slope))
        else:
            # A zero transformed normal with negative rhs certifies emptiness.
            assert rhs < 0
            break
    return archive, transcript, None


def check_case(lo, hi, base, direction, center, mu, weight, sign, expected=None):
    def value(t):
        errors = [b + t * v - a for b, v, a in zip(base, direction, center)]
        return sum(weight * e**4 + mu * e**2 / 2 for e in errors)

    def gradient(z):
        q = [4 * weight * (x - a)**3 + mu * (x - a)
             for x, a in zip(z, center)]
        # Exact error norm mu/4, including query-dependent sign changes.
        q[0] += sign * (-1 if sum(z) % 2 else 1) * mu / 4
        return tuple(q)

    if expected is None:
        best = min(value(t) for t in range(lo, hi + 1))
        expected = {t for t in range(lo, hi + 1) if value(t) == best}
    archive, transcript, early = search(lo, hi, base, direction, gradient, mu)
    assert expected <= set(archive), (base, direction, center, archive, expected)
    if early is not None:
        assert expected == {early}
    # Every query cut preserves each different global optimum, even after
    # another global optimum has already been queried and rejected.
    for t, slope, rhs in transcript:
        assert all(slope * w <= rhs for w in expected if w != t)
    assert len(archive) <= (hi - lo + 1).bit_length() + 1
    return len(archive), int(len(expected) > 1), int(early is not None)


if __name__ == "__main__":
    cases = queries = ties = early = 0
    for base, direction in [((0,), (1,)), ((0, 0), (1, 2)),
                            ((1, -2), (2, 3)), ((1, -2), (0, 1))]:
        for shift, mu, weight, sign, interval in product(
                [F(-3, 2), F(0), F(1, 2), F(5, 4)],
                [F(1, 7), F(1), F(9)], [F(0), F(1), F(7)],
                [-1, 0, 1], [(-8, 8), (2, 8), (1, 1)]):
            center = tuple(b + shift * v for b, v in zip(base, direction))
            count, tied, stopped = check_case(
                *interval, base, direction, center, mu, weight, sign)
            cases += 1
            queries += count
            ties += tied
            early += stopped
    # Huge box, only O(log R) queries; two exactly tied optima both survive.
    radius = 2**100
    count, tied, stopped = check_case(
        -radius, radius, (0,), (1,), (F(1, 2),), F(1), F(1), 1,
        expected={0, 1})
    assert tied and count <= 103
    print(f"PASS: {cases} affine-line runs, {queries} exact cuts/queries,")
    print(f"      {ties} tied-optimum cases, {early} zero-normal early stops.")
    print(f"PASS: every optimum retained; 101-bit radius uses {count} queries.")
