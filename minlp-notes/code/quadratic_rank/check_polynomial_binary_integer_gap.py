"""Exact sample checks for the Bernstein triangular-wave counterfamily.

The uniform approximation follows from the written variance proof. These checks
use exact rational Bernstein values, without expanding thousands of monomials.
"""
from fractions import Fraction


def triangular(m, x):
    phase = m*x - (m*x).__floor__()
    return 2*min(phase,1-phase)


def bernstein(m, x):
    n = (32*m)**2
    if x in (0,1):
        return Fraction(0)
    a,b = x.numerator,x.denominator
    p = (b-a)**n
    total = 0
    for k in range(n+1):
        phase = (m*k)%n
        height_numerator = 2*min(phase,n-phase)
        total += height_numerator*p
        if k<n:
            numerator = p*(n-k)*a
            denominator = (k+1)*(b-a)
            p,remainder = divmod(numerator,denominator)
            assert remainder == 0
    return Fraction(total,n*b**n)


sample_count = packing_count = gadget_count = 0
for m in (2,3):
    peaks = [Fraction(2*j+1,2*m) for j in range(m)]
    troughs = [Fraction(j,m) for j in range(m+1)]
    values = {}
    for x in sorted(set(peaks+troughs)):
        values[x] = bernstein(m,x)
        assert abs(values[x]-triangular(m,x)) <= Fraction(1,32)
        sample_count += 1
    for j,a in enumerate(peaks):
        for b in peaks[j+1:]:
            t = next(x for x in troughs if a<x<b)
            lam = (t-a)/(b-a)
            chord = (1-lam)*values[a]+lam*values[b]
            assert chord-values[t] >= Fraction(30,32)
            packing_count += 1
    for z in range(m):
        for orient in (0,1):
            for j in range(9):
                t = Fraction(orient,2)+Fraction(j,16)
                y = 2*t if orient==0 else 2-2*t
                x = (z+t)/m
                assert triangular(m,x)==y
                assert Fraction(orient,2)<=t<=Fraction(orient+1,2)
                assert -2*orient<=y-2*t<=2*orient
                assert -2*(1-orient)<=y-(2-2*t)<=2*(1-orient)
                gadget_count += 1
print(f'PASS: {sample_count} exact Bernstein values at degrees 4096/9216; '
      f'{packing_count} peak-chord violations; {gadget_count} periodic MILP branch checks')
