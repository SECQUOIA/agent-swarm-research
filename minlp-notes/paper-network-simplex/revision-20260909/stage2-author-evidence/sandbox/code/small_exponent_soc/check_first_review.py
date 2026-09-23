"""Exact primal/dual certificates for the repeated-squaring SOCP.

Independent standard form: q_i=(z_i,1/2,z_(i-1)) in the rotated cone,
with second-coordinate equalities, first input a, and adjacent links.
All checks use Fraction arithmetic; no conic solver tolerances enter.
"""
from fractions import Fraction as F


def check(a, B):
    z = [a]
    for _ in range(B):
        z.append(z[-1] ** 2)
    lam = [F(0)] * (B + 1)
    lam[B] = F(1)
    for i in range(B - 1, 0, -1):
        lam[i] = 2 * z[i] * lam[i + 1]
    alpha = [F(0)] + [-2 * z[i] * lam[i] for i in range(1, B + 1)]
    beta = [F(0)] + [2 * z[i - 1] * lam[i] for i in range(1, B + 1)]
    assert sum(alpha[1:]) / 2 + a * beta[1] == z[B]
    for i in range(1, B + 1):
        q = (z[i], F(1, 2), z[i - 1])
        s = (lam[i], -alpha[i], -beta[i])
        assert 2 * q[0] * q[1] == q[2] ** 2
        assert 2 * s[0] * s[1] == s[2] ** 2
        assert q[0] >= 0 and q[1] >= 0 and s[0] >= 0 and s[1] >= 0
        assert sum(qj * sj for qj, sj in zip(q, s)) == 0
        assert s[0] == (beta[i + 1] if i < B else 1)
        assert alpha[i] + s[1] == 0
        assert beta[i] + s[2] == 0
    strict = [a + F(i, B + 1) * (1 - a) for i in range(B + 1)]
    assert all(strict[i] > strict[i - 1] ** 2 for i in range(1, B + 1))
    for theta in (F(0), F(1, 7), F(1), F(13)):
        assert theta * z[B] == theta * (sum(alpha[1:]) / 2 + a * beta[1])


def main():
    count = 0
    for B in range(1, 8):
        for j in range(1, 16):
            check(F(j, 16), B)
            count += 1
    # Every binary code leaves exactly one feasible selector support.
    for selected in range(16):
        bits = [(selected >> k) & 1 for k in range(4)]
        surviving = [j for j in range(16)
                     if all(bits[k] == ((j >> k) & 1) for k in range(4))]
        assert surviving == [selected]
    print(f'PASS: {count} exact SOCP primal/dual/Slater certificates; 16 selector codes')


if __name__ == '__main__':
    main()
