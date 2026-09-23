"""Exact mass-inversion and graph-band checks for constant curvature.

The cumulative integral is piecewise rational here; all checks are exact.
Large indexed grids are sampled without enumerating their cells.
"""
from fractions import Fraction as Q
import random

rng = random.Random(10092026)
zeta = Q(1,512)
def ceil_log2(q):
    k = q.numerator.bit_length()-q.denominator.bit_length()
    if k >= 0:
        return k if Q(2**k)>=q else k+1
    return k if Q(1,2**(-k))>=q else k+1

cells = bands = 0
for A in [Q(1),Q(2),Q(8),Q(2**10),Q(2**20)]:
    eps = Q(1,7)
    cut = 1-1/A
    def F(x):
        if x <= cut:
            return A*x
        return A*cut+A*A*((x-cut)-(x*x-cut*cut)/2)
    M = F(Q(1))
    assert M == A-Q(1,2)
    def approximate_F(x):
        value = F(x)
        return Q((value.numerator*512)//value.denominator,512)
    U = max(zeta,approximate_F(Q(1))+zeta)
    L = max(0,ceil_log2(Q(5,2)*U))
    N = 2**L
    B = 1+A*A
    steps = ceil_log2(B/zeta)+1
    def knot(index):
        if index == 0:
            return Q(0)
        if index == N:
            return Q(1)
        target = index*U/N
        lo,hi = Q(0),Q(1)
        for _ in range(steps):
            mid = (lo+hi)/2
            value = approximate_F(mid)
            if value+zeta < target:
                lo = mid
            elif value-zeta > target:
                hi = mid
            else:
                return mid
        return (lo+hi)/2
    indices = set([0,N-1])
    indices.update(rng.randrange(N) for _ in range(40))
    C = eps*A*A/2
    endpoint_P = max(steps+2,ceil_log2(4*A*A)+2)
    scale = 2**endpoint_P
    def low_f(x):
        square = x*x
        low_square = Q((square.numerator*scale)//square.denominator,scale)
        value = C*low_square
        assert 0 <= C*x*x-value <= eps/8
        return value
    for index in indices:
        a,b = knot(index),knot(index+1)
        assert abs(F(a)-index*U/N) <= 4*zeta
        assert abs(F(b)-(index+1)*U/N) <= 4*zeta
        assert abs(F(b)-F(a)) <= Q(133,320)
        va,vb = low_f(a),low_f(b)
        for lam in [Q(0),Q(1,5),Q(1,2),Q(4,5),Q(1)]:
            x = (1-lam)*a+lam*b
            y = (1-lam)*va+lam*vb
            true = C*x*x
            lower,upper = y-Q(13,16)*eps,y+eps/8
            assert lower <= true <= upper
            assert abs(lower-true) <= Q(15,16)*eps
            assert abs(upper-true) <= Q(15,16)*eps
            bands += 1
        cells += 1
print(f'PASS: {cells} exact indexed mass-cell certificates and {bands} exact graph bands; grids through {2**L} cells without enumeration')
