"""Dossier check (camshape): independent re-derivation of the worst-case tolerance deficit D_n(eps).

eps-relaxed model (every row and bound violated by at most eps, objective row exact):
  G_j <= eps, |r_i - r_{i+1} + d_i| <= eps, r in [lo-eps, hi+eps], |d_i| <= alpha+eps (i>=2), d_1 free.
Then r >= 1-eps > 0, e_j >= -delta with delta = eps/(1-eps)^3, u_1 >= 1/(ub1+eps),
u_j >= S'_j - delta*W_j (W_j = sum_{m=0}^{j-2} U_m), r_j <= min(hi_j+eps, 1/(S'_j - delta W_j)),
|r_{j+1}-r_j| <= alpha + 2 eps (j>=2).  L(eps) = -c0 * sum E(eps); D = v* - L(eps).
Exact Fractions; each radius bound is rounded UP to a 2^-200 grid (keeps validity, bounds sizes).
"""
import sys
import json
from fractions import Fraction as Fr

sys.set_int_max_str_digits(0)
from check_exact import read_osil, structure, certificate

P = 200


def up(q):
    return Fr(-((-q.numerator << P) // q.denominator), 1 << P)


def L(K, n, eps, U):
    c, ub1, al, c0 = K['c'], K['ub1'], K['alpha'], K['c0']
    delta = eps / (1 - eps) ** 3
    S = [Fr(1), 1 / (ub1 + eps)]
    while len(S) < n + 1:
        S.append(c * S[-1] - S[-2])
    W = [Fr(0), Fr(0)]
    acc = Fr(0)
    for j in range(2, n + 1):
        acc += U[j - 2]
        W.append(acc)
    hi = [None, ub1 + eps] + [Fr(2) + eps] * (n - 1)
    B = [None]
    for j in range(1, n + 1):
        low_u = S[j] - delta * W[j]
        B.append(min(hi[j], up(1 / low_u)) if low_u > 0 else hi[j])
    a = al + 2 * eps
    F = [None, B[1], B[2]] + [None] * (n - 2)
    for j in range(3, n + 1):
        F[j] = min(B[j], F[j - 1] + a)
    E = F[:]
    for j in range(n - 1, 1, -1):
        E[j] = min(F[j], E[j + 1] + a)
    return -c0 * sum(E[1:])


if __name__ == '__main__':
    out = []
    for arg in sys.argv[1:]:
        n, eps = arg.split(':')
        n = int(n); eps = Fr(eps)
        M = read_osil(f'camshape{n}.osil')
        K = structure(M, n)
        C = certificate(K, n)
        vstar = -K['c0'] * sum(C['E'][1:])
        Le = L(K, n, eps, C['U'])
        D = vstar - Le
        rec = dict(n=n, eps=str(eps), D=float(D), D_over_eps=float(D / eps), D_over_n2eps=float(D / eps / n ** 2))
        print(json.dumps(rec), flush=True)
        out.append(rec)
    json.dump(out, open('tol_check.json', 'w'), indent=1)
