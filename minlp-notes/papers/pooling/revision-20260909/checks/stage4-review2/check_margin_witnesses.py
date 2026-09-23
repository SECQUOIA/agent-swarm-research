"""Independent finite audit of Appendix B; exact Fraction arithmetic only.

Compare the endpoint/square-root minimum test with rational minimization
of the threshold quadratic for all paired box-slice patterns. This tests
the rational certificate construction, including equality and zero cases;
it is not a proof of the asymptotic algorithms.
"""
from fractions import Fraction as F
from itertools import product
from random import Random


def patterns(lo, hi):
    for free in range(len(lo)):
        other = [i for i in range(len(lo)) if i != free]
        for bits in product((0, 1), repeat=len(other)):
            b = [F(0)] * len(lo)
            for i, bit in zip(other, bits):
                b[i] = (lo, hi)[bit][i]
            total = sum(b)
            b[free] = -total
            yield free, b, total + lo[free], total + hi[free]


def check(C, lo, hi, lp, up, threshold):
    count = 0
    for a, b, left, right in patterns(lo, hi):
        for h, d, left2, right2 in patterns(lp, up):
            L, U = max(left, left2), min(right, right2)
            if L > U or U == 0:
                continue
            alpha = C[a][h]
            beta = sum(C[a][j] * d[j] for j in range(len(d)))
            beta += sum(b[i] * C[i][h] for i in range(len(b)))
            gamma = sum(b[i] * C[i][j] * d[j]
                        for i in range(len(b)) for j in range(len(d)))
            f_yes = any(alpha * S + beta + gamma / S <= threshold
                        for S in (L, U) if S > 0)
            if L == 0:
                assert gamma == beta == 0
                f_yes |= threshold >= 0  # zero matrix, handled separately
            if alpha > 0 and gamma > 0:
                ratio = gamma / alpha
                gap = threshold - beta
                if L * L <= ratio <= U * U:
                    f_yes |= gap >= 0 and gap * gap >= 4 * alpha * gamma

            candidates = [L, U]
            if alpha > 0:
                stationary = (threshold - beta) / (2 * alpha)
                if L <= stationary <= U:
                    candidates.append(stationary)
            if alpha == gamma == 0 and beta == threshold:
                candidates.append((L + U) / 2)
            q_good = [S for S in candidates if S > 0 and
                      alpha*S*S + (beta-threshold)*S + gamma <= 0]
            q_yes = bool(q_good) or (L == 0 and threshold >= 0)
            assert f_yes == q_yes, (alpha, beta, gamma, L, U, threshold)
            for S in q_good:
                r, c = b.copy(), d.copy()
                r[a] += S
                c[h] += S
                assert sum(r) == sum(c) == S
                assert all(l <= v <= u for l, v, u in zip(lo, r, hi))
                assert all(l <= v <= u for l, v, u in zip(lp, c, up))
                W = [[ri*cj/S for cj in c] for ri in r]
                assert [sum(row) for row in W] == r
                assert [sum(W[i][j] for i in range(len(r)))
                        for j in range(len(c))] == c
                assert sum(C[i][j]*W[i][j] for i in range(len(r))
                           for j in range(len(c))) <= threshold
            count += 1
    return count


rng = Random(20260909)
counts = 0
for case in range(150):
    m, n = rng.randint(1, 3), rng.randint(1, 4)
    lo = [F(rng.randrange(3), 2) for _ in range(m)]
    hi = [l + F(rng.randrange(4), 2) for l in lo]
    lp = [F(rng.randrange(3), 2) for _ in range(n)]
    up = [l + F(rng.randrange(4), 2) for l in lp]
    if case % 5 == 0:
        lo, lp = [F(0)]*m, [F(0)]*n
    C = [[F(rng.randrange(-5, 6), rng.randrange(1, 4))
          for _ in range(n)] for _ in range(m)]
    threshold = F(rng.randrange(-12, 13), rng.randrange(1, 4))
    counts += check(C, lo, hi, lp, up, threshold)

# Equality thresholds, zero total, constant costs, singleton intervals,
# and the displayed irrational examples.
for C in ([[F(1), F(0)], [F(0), F(1)]],
          [[F(6), F(3)], [F(2), F(1)]],
          [[F(0), F(0)], [F(0), F(0)]]):
    for threshold in map(F, (-1, 0, 1, 2, 3, 4, 5, 6, 7)):
        counts += check(C, [F(1), F(0)], [F(1), F(1)],
                        [F(1), F(0)], [F(1), F(1)], threshold)
        counts += check(C, [F(0), F(0)], [F(1), F(1)],
                        [F(0), F(0)], [F(1), F(1)], threshold)
print(f'PASS: 150 randomized boxes and 54 boundary/example thresholds; '
      f'{counts} feasible positive-total pattern pairs checked exactly.')
