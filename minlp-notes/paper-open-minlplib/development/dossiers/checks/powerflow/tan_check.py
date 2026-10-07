"""Exact check of the rational tangent bounds used by the angle rows of R (pf_model):
tb >= tan(B0) and ta <= tan(A0), via alternating Taylor series bounds of sin and cos (|x| < 1)."""
import sys
sys.path.insert(0, "/tmp/pfdossier/code")
import pf_model as pm
from fractions import Fraction as Fr
from math import factorial
def sin_cos_bounds(x, N=30):
    s = sum((-1)**k * x**(2*k+1) / factorial(2*k+1) for k in range(N))
    c = sum((-1)**k * x**(2*k) / factorial(2*k) for k in range(N))
    ts = x**(2*N+1) / factorial(2*N+1); tc = x**(2*N) / factorial(2*N)
    return (s - ts, s + ts), (c - tc, c + tc)
for name in sys.argv[1:]:
    M = pm.decode(name)
    worst = None
    for (kp, kq), (A0, B0, ta, tb) in M['angle'].items():
        for a, t, side in ((B0, tb, 'up'), (A0, ta, 'lo')):
            x = abs(a); (slo, shi), (clo, chi) = sin_cos_bounds(x)
            assert 0 < x < 1 and clo > 0
            if side == 'up':
                assert a > 0; m = t - shi / clo
            else:
                assert a < 0; m = -(slo / chi) - t
            assert m > 0
            worst = m if worst is None or m < worst else worst
    print(name, len(M['angle']), 'bus pairs; all tan bounds valid; smallest margin', float(worst))
