"""Critic: explicit eps-tolerance-feasible points for QPLIB_3177 (G_j = eps chain, cap 2+eps, slope alpha+2eps);
smallest eps (on a grid) whose point reaches objective <= -4.27735 (upper end of MINOTAUR's printed -4.2774)."""
import sys
from fractions import Fraction as Fr
import mpmath as mp
sys.path.insert(0, '/tmp/camcrit')
from qplib import to_model
mp.mp.dps = 60
K = to_model('/tmp/camcrit/q/QPLIB_3177.gms', 800)[0]; n = 800
q = lambda x: mp.mpf(x.numerator) / x.denominator
c, ub1, al, c0, c2 = q(K['c']), q(K['ub1']), q(K['alpha']), q(K['c0']), q(K['c2'])
def point(e):
    R = [mp.mpf(1), ub1 + e]
    R.append((e + R[1]) / (c - R[1]))
    for j in range(2, n):
        den = c * R[j - 1] - R[j]
        R.append((e + R[j - 1] * R[j]) / den if den > 0 else mp.mpf(10))
        if R[-1] <= 0 or R[-1] > 10: R[-1] = mp.mpf(10)
    B = [None, R[1]] + [min(R[j], 2 + e) for j in range(2, n + 1)]
    a = al + 2 * e; F = B[:]
    for j in range(3, n + 1): F[j] = min(F[j], F[j - 1] + a)
    for j in range(n - 1, 1, -1): F[j] = min(F[j], F[j + 1] + a)
    r = F
    v = max([-r[1] + c*r[2] - r[1]*r[2]] + [-r[j-1]*r[j] + c*r[j-1]*r[j+1] - r[j]*r[j+1] for j in range(2, n)]
            + [c2*r[n-1] - 2*r[n] - r[n-1]*r[n], c*r[n]**2 - 4*r[n], r[1] - ub1] + [r[j] - 2 for j in range(2, n + 1)])
    return -c0 * mp.fsum(r[1:]), v
for e in ['5e-9', '8e-9', '9e-9', '9.5e-9', '1e-8', '2.98e-8', '1e-7', '1e-6']:
    obj, v = point(mp.mpf(e))
    print(e, 'obj', mp.nstr(obj, 10), 'maxviol', mp.nstr(v, 4))
