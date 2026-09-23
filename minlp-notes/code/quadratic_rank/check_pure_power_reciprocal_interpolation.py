"""Exact reciprocal gadget identities and uniform pure-power chord checks."""
from fractions import Fraction as Q
import random

rng = random.Random(6092026)
chords = 0
for degree in range(2, 33):
    for _ in range(12):
        aa, bb = sorted(rng.sample(range(21), 2))
        # Square endpoints make the half-degree powers rational for odd D.
        a, b = Q(aa,20)**2, Q(bb,20)**2
        delta_t = Q(bb,20)**degree-Q(aa,20)**degree
        for numerator in range(9):
            lam = Q(numerator,8)
            x = (1-lam)*a+lam*b
            chord = (1-lam)*a**degree+lam*b**degree
            assert 0 <= chord-x**degree <= 4*delta_t**2
            chords += 1

reciprocals = 0
for L in range(1, 7):
    h = Q(1, 2**L)
    for _ in range(10):
        index = rng.randrange(2**L)
        a = index*h
        bits = [(index >> (L-i-1)) & 1 for i in range(L)]
        assert a == sum(Q(1,2**(i+1))*bits[i] for i in range(L))
        lam = Q(rng.randrange(17),16)
        beta = [Q(1,2**rng.randrange(1,10)), Q(rng.randrange(1,8),3), Q(16)]
        raw = [Q(rng.randrange(1,9),7) for _ in beta]
        normalization = sum(c/(1+b) for c,b in zip(raw,beta))
        alpha = [c/normalization for c in raw]
        R = lambda t: sum(c*t/(t+b) for c,b in zip(alpha,beta))
        assert R(0) == 0 and R(1) == 1
        vm = [(1-lam)/(a+b) for b in beta]
        vp = [lam/(a+h+b) for b in beta]
        for k,b in enumerate(beta):
            assert 0 <= vm[k] <= 1/b and 0 <= vp[k] <= 1/b
            assert b*vm[k]+sum(Q(1,2**(i+1))*bits[i]*vm[k] for i in range(L)) == 1-lam
            assert (b+h)*vp[k]+sum(Q(1,2**(i+1))*bits[i]*vp[k] for i in range(L)) == lam
        x = sum(c*(1-b*(minus+plus)) for c,b,minus,plus in zip(alpha,beta,vm,vp))
        assert x == (1-lam)*R(a)+lam*R(a+h)
        assert 0 <= x <= 1
        a_square = sum(Q(1,2**(i+1))*bits[i]*a for i in range(L))
        a_lambda = sum(Q(1,2**(i+1))*bits[i]*lam for i in range(L))
        y = a_square+2*h*a_lambda+h*h*lam
        assert y == (1-lam)*a*a+lam*(a+h)**2
        reciprocals += 1
print(f'PASS: {chords} exact degree-uniform chord checks; {reciprocals} exact reciprocal, endpoint and shared-bit identities')
