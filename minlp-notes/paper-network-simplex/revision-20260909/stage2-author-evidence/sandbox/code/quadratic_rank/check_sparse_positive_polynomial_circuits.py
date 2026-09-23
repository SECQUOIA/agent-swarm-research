"""Rounded sparse powers and endpoint interpolation checks.

Small exponent enclosures are exact. Very large exponents use 120-digit
reference values as numerical evidence; the note supplies the proof.
"""
from fractions import Fraction as Q
import random
import mpmath as mp

mp.mp.dps = 120
rng = random.Random(8092026)
def rounded_power(x,k,P):
    scale = 1 << P
    base = x.numerator*(scale//x.denominator)
    result = scale
    while k:
        if k & 1:
            result = (result*base)//scale
        k >>= 1
        if k:
            base = (base*base)//scale
    return Q(result,scale)

def mpq(x):
    return mp.mpf(x.numerator)/x.denominator

exact = 0
for k in [2,3,7,31,127,511,1024]:
    for _ in range(8):
        x = Q(rng.randrange(257),256)
        P = 32+k.bit_length()
        value = rounded_power(x,k,P)
        assert 0 <= x**k-value <= Q(k,2**P)
        exact += 1

large = 0
for D in [2**40+3,2**80+7,2**120+11]:
    J = (D-1).bit_length()
    for j in [0,J//2,J-1,J]:
        if j == J:
            left,length = 1-Q(1,2**J),Q(1,2**J)
        else:
            left,length = 1-Q(1,2**j),Q(1,2**(j+1))
        L = 5
        h = Q(1,2**L)
        cell = rng.randrange(2**L)
        a,b = left+length*cell*h,left+length*(cell+1)*h
        eta = Q(1,2**20)
        P = max(J+L+1,D.bit_length()+22)
        low,high = rounded_power(a,D,P),rounded_power(b,D,P)
        for point,value in [(a,low),(b,high)]:
            true = mp.power(mpq(point),D)
            assert -mp.mpf('1e-110') <= true-mpq(value) <= mpq(eta)
        lam = Q(5,13)
        x = (1-lam)*a+lam*b
        interp = (1-lam)*low+lam*high
        error = mpq(interp)-mp.power(mpq(x),D)
        assert -mpq(eta)-mp.mpf('1e-100') <= error <= mpq(h*h/4)+mp.mpf('1e-100')
        large += 1
print(f'PASS: {exact} exact rounded-power enclosures; {large} 120-digit sparse endpoint/band cases through exponent 2^120+11')
