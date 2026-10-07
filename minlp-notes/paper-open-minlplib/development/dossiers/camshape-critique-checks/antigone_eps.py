"""Critic: same explicit eps-feasible construction for QPLIB_2738 (ANTIGONE's -4.284302) for comparison."""
import sys
import mpmath as mp
sys.path.insert(0, '/tmp/camcrit')
from qplib import to_model
mp.mp.dps = 60
for name, n, target in (('QPLIB_2738', 100, '-4.2843015'), ('QPLIB_3177', 800, '-4.27735')):
    K = to_model(f'/tmp/camcrit/q/{name}.gms', n)[0]
    q = lambda x: mp.mpf(x.numerator) / x.denominator
    c, ub1, al, c0, c2 = q(K['c']), q(K['ub1']), q(K['alpha']), q(K['c0']), q(K['c2'])
    def obj(e):
        R = [mp.mpf(1), ub1 + e]; R.append((e + R[1]) / (c - R[1]))
        for j in range(2, n):
            den = c * R[j - 1] - R[j]
            R.append((e + R[j - 1] * R[j]) / den if den > 0 else mp.mpf(10))
            if R[-1] <= 0 or R[-1] > 10: R[-1] = mp.mpf(10)
        B = [None, R[1]] + [min(R[j], 2 + e) for j in range(2, n + 1)]
        a = al + 2 * e; F = B[:]
        for j in range(3, n + 1): F[j] = min(F[j], F[j - 1] + a)
        for j in range(n - 1, 1, -1): F[j] = min(F[j], F[j + 1] + a)
        return -c0 * mp.fsum(F[1:])
    lo, hi = mp.mpf('1e-12'), mp.mpf('1e-6')
    for _ in range(60):
        mid = mp.sqrt(lo * hi)
        if obj(mid) <= mp.mpf(target): hi = mid
        else: lo = mid
    print(name, 'smallest eps (explicit construction) reaching', target, ':', mp.nstr(hi, 4))
