"""Critic: construct an explicit eps-tolerance-feasible point (every row/bound violated by <= eps)
by running the convexity rows at G_j = eps, then cap 2+eps and slope alpha+2eps; report its deficit
below v_n (mpmath, 80 digits; numerical evidence of how tight the upper bound D_n(eps) is)."""
import sys, json
from fractions import Fraction as Fr
import mpmath as mp
sys.path.insert(0, '.')
from mine import structure, envelope_exact
mp.mp.dps = 80

def run(n, eps, vn):
    K = structure(f'camshape{n}.osil', n)
    q = lambda x: mp.mpf(x.numerator) / x.denominator
    c, ub1, al, c0, c2 = q(K['c']), q(K['ub1']), q(K['alpha']), q(K['c0']), q(K['c2'])
    e = mp.mpf(eps)
    R = [mp.mpf(1), ub1 + e]
    # G_1: -r1 + c r2 - r1 r2 = eps ; G_j: -r_{j-1} r_j + c r_{j-1} r_{j+1} - r_j r_{j+1} = eps
    R.append((e + R[1]) / (c - R[1]))
    for j in range(2, n):
        R.append((e + R[j - 1] * R[j]) / (c * R[j - 1] - R[j]))
        if R[-1] <= 0 or R[-1] > 10: R[-1] = mp.mpf(10)
    B = [None, R[1]] + [min(R[j], 2 + e) for j in range(2, n + 1)]
    a = al + 2 * e
    F = B[:]
    for j in range(3, n + 1): F[j] = min(F[j], F[j - 1] + a)
    for j in range(n - 1, 1, -1): F[j] = min(F[j], F[j + 1] + a)
    r = F
    # d_i = r_{i+1} - r_i - eps*sign so that |d_i| <= alpha + eps and D-row residual is eps
    viol = mp.mpf(0)
    def G(j):
        if j == 1: return -r[1] + c * r[2] - r[1] * r[2]
        if j < n: return -r[j-1]*r[j] + c*r[j-1]*r[j+1] - r[j]*r[j+1]
        return c2 * r[n-1] - 2 * r[n] - r[n-1] * r[n]
    for j in range(1, n + 1): viol = max(viol, G(j))
    viol = max(viol, c * r[n] ** 2 - 4 * r[n])
    viol = max(viol, r[1] - ub1, max(r[j] - 2 for j in range(2, n + 1)), max(1 - r[j] for j in range(1, n)))
    slope = max(abs(r[j + 1] - r[j]) for j in range(2, n))
    # D rows: choose d_i = clamp(r_{i+1}-r_i, alpha+eps); residual = |r_{i+1}-r_i - d_i| <= eps iff slope <= alpha+2eps
    obj = -c0 * mp.fsum(r[1:])
    return dict(n=n, eps=eps, max_row_or_bound_viol=mp.nstr(viol, 6), slope_excess_over_alpha=mp.nstr(slope - al, 6),
                deficit=mp.nstr(mp.mpf(vn) - obj, 8))

VN = {100: '-4.2841471217467438034410071', 200: '-4.2785002329927222918988259', 400: '-4.2756884789255432151508246', 800: '-4.2742741419541941011244678'}
DN = {(100, '1e-10'): 6.0447e-7, (100, '1e-8'): 6.0449e-5, (200, '1e-10'): 2.3551e-6, (400, '1e-10'): 9.3475e-6, (400, '3e-10'): 2.8043e-5, (800, '3e-10'): 1.1255e-4}
for (n, eps), D in DN.items():
    rec = run(n, eps, VN[n]); rec['D_upper'] = D; rec['ratio'] = float(mp.mpf(rec['deficit']) / D)
    print(json.dumps(rec), flush=True)
