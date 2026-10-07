"""Exact checks for the bounded-coefficient hardness conditioning note."""

from fractions import Fraction as Q


def construct(B, choices):
    ell = (2 * B - 1).bit_length()
    D = 2**ell
    weights = [B, B - 1]
    bits = [[(a >> k) & 1 for k in range(ell)] for a in weights]
    target = [(B >> k) & 1 for k in range(ell)]
    x = [[Q(u)] * ell for u in choices]
    z = []
    for i, u in enumerate(choices):
        row = []
        prev = Q(0)
        for digit in bits[i]:
            prev = (prev + digit * u) / 2
            row.append(prev)
        z.append(row)
    s = [z[0][-1], z[0][-1] + z[1][-1]]
    w = []
    prev = Q(0)
    for digit in target:
        prev = (prev + digit) / 2
        w.append(prev)
    residuals = []
    for i in range(2):
        residuals.extend(x[i][k] - x[i][k - 1] for k in range(1, ell))
        for k in range(ell):
            residuals.append(2 * z[i][k] - (z[i][k - 1] if k else 0) - bits[i][k] * x[i][k])
    residuals.extend([s[0] - z[0][-1], s[1] - s[0] - z[1][-1]])
    residuals.extend(2 * w[k] - (w[k - 1] if k else 0) - target[k] for k in range(ell))
    residuals.append(s[-1] - w[-1])
    vector = x[0] + x[1] + z[0] + z[1] + s + w
    assert len(vector) == 5 * ell + 2
    assert D > sum(weights)
    return vector, residuals, ell


def main():
    Bs = sorted(set(range(3, 103)) | {2**m for m in (2, 3, 4, 8, 16, 32, 64, 100, 200)})
    count = 0
    residual_count = 0
    for B in Bs:
        optimal, r_star, ell = construct(B, [Q(1), Q(0)])
        witness, r_y, _ = construct(B, [Q(1, B), Q(1)])
        assert not any(r_star) and not any(r_y)
        residual_count += len(r_star) + len(r_y)
        assert all(Q(0) <= value <= Q(1) for value in optimal + witness)
        assert [(u, v) for u in (0, 1) for v in (0, 1) if B * u + (B - 1) * v == B] == [(1, 0)]
        direction = [b - a for a, b in zip(optimal, witness)]
        R = sum(d * d for d in direction)
        q = Q(B - 1, B)
        assert R >= ell * (q * q + 1)
        assert direction[0] == -q and direction[ell] == 1
        for c in (Q(1, 13), Q(1), Q(100)):
            for penalty_scale in (Q(1, 1000), Q(1), Q(10**6)):
                objective = penalty_scale * sum(r * r for r in r_y) + c * (witness[0] * (1 - witness[0]) + witness[ell] * (1 - witness[ell]))
                assert objective == c * q / B
                hessian_direction = 2 * penalty_scale * sum((b - a)**2 for a, b in zip(r_star, r_y)) - 2 * c * (direction[0]**2 + direction[ell]**2)
                assert hessian_direction == -2 * c * (q * q + 1)
                growth_upper = objective / R
                curvature_lower = -hessian_direction / R
                assert curvature_lower / growth_upper == 2 * B * (q * q + 1) / q
                assert curvature_lower / growth_upper >= 4 * B
                count += 1
        if B & (B - 1) == 0:
            m = B.bit_length() - 1
            assert ell == m + 1
            assert len(optimal) == 5 * m + 7
    print(f"PASS: {len(Bs)} constructions, {count} weight cases, {residual_count} zero-residual checks; maximum B bit length {max(Bs).bit_length()}.")


if __name__ == "__main__":
    main()
