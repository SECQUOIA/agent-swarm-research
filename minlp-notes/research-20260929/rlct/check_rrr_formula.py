"""Check the Aoyagi-Watanabe (2005) learning coefficient of reduced-rank
regression, as recalled in the note, against Table 1 of Drton and Plummer
(2017, arXiv:1309.0911): N = 5 responses, M = 3 covariates, model rank H = i,
true rank r = j.  Also print the node-complexity exponent n/2 - lambda with
n = H (M + N) parameters.
"""
from fractions import Fraction as Fr


def rrr_lambda(M, N, H, r):
    if N + r <= M + H and M + r <= N + H and H + r <= M + N:
        s = 2 * (H + r) * (M + N) - (M - N) ** 2 - (H + r) ** 2
        if (M + H + N + r) % 2 == 1:
            s += 1
        return Fr(s, 8)
    if M + H < N + r:
        return Fr(H * M - H * r + N * r, 2)
    if N + H < M + r:
        return Fr(H * N - H * r + M * r, 2)
    return Fr(M * N, 2)            # M + N < H + r


# Drton-Plummer Table 1 (N = 5, M = 3), lambda_{ij}, model rank i, true rank j
TABLE = {(1, 0): Fr(3, 2), (1, 1): Fr(7, 2),
         (2, 0): Fr(3), (2, 1): Fr(9, 2), (2, 2): Fr(6),
         (3, 0): Fr(9, 2), (3, 1): Fr(11, 2), (3, 2): Fr(13, 2), (3, 3): Fr(15, 2)}

ok = True
for (i, j), lam in sorted(TABLE.items()):
    got = rrr_lambda(3, 5, i, j)
    n = i * (3 + 5)
    ok &= got == lam
    print(f"H={i} r={j}: formula {got}, table {lam}, n = {n}, exponent n/2 - lambda = {Fr(n, 2) - got}")
print("all match" if ok else "MISMATCH")
print("1x1 case M=N=H=1, r=0 (m ~ a^2 b^2):", rrr_lambda(1, 1, 1, 0))
