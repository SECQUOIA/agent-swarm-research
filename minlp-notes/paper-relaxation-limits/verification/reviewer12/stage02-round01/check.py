"""Independent exact checks of frozen Stage 2 certificates and law definitions."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from math import comb
import sympy as S

paper = Path(__file__).resolve().parents[3]
frozen = paper / 'process/snapshots/stage02-round01/sections'

# Replay the actual printed finite certificate, not a live author checker.
certificate = (frozen / 'appendix-cubic-certificates.tex').read_text()
exec(certificate.split('\\begin{verbatim}')[1].split('\\end{verbatim}')[0])

# Derive the two minimized quartics independently, then check each printed row.
a,b,c,t = S.symbols('a b c t')
h = 6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2-37*a-S.Rational(79,2)*b-38*c+S.Rational(103,3)
p = S.expand(h.subs({a:1,b:S.Rational(13,24)-3*c**2/4}))
critical = S.solve([S.diff(h,a),S.diff(h,b)],(a,b))
r = S.expand(h.subs(critical))
text = (frozen / '03-cubic-equal-means.tex').read_text()
rows = [line for line in text.splitlines() if line.startswith(('$p$&','$r$&'))]
minimum = 1
for row in rows:
    name,interval,den,nums = row.split('&')
    lo,hi = map(S.Rational,interval.strip('$[]').split(','))
    nums = [int(v) for v in nums.split('(')[1].split(')')[0].split(',')]
    bernstein = sum(S.Rational(v,int(den))*S.binomial(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(nums))
    assert S.expand((p if name=='$p$' else r).subs(c,lo+(hi-lo)*t)-bernstein)==0
    minimum = min(minimum,*[S.Rational(v,int(den)) for v in nums])
assert minimum == S.Rational(901,120000)
assert (S.Rational(161,4)/(S.Rational(223,12)-minimum)) == S.Rational(1610000,743033)
for coef,la,lc,offset,center,tail in [
    (S.Rational(5,4),S.Rational(11,6),S.Rational(20,27),S.Rational(95,108),(11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135),
    (S.Rational(24,25),S.Rational(41,25),S.Rational(4,5),S.Rational(68,75),(41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480),
]:
    assert S.expand(a*c*c+coef*a*a-la*a-lc*c+offset-coef*(a-center)**2-tail)==0
print('Exact Bernstein rows, uniform slack, and both two-level identities passed.')

# Integrate actual O and B laws without using the manuscript's deficiency formulas.
def actual_deficiencies(means):
    u=min(means)
    d=len(means)
    expected_o=Q(0)
    for orientation in product([0,1],repeat=d):
        left=max([Q(0)]+[1-x for x,o in zip(means,orientation) if o])
        right=min([Q(1)]+[x for x,o in zip(means,orientation) if not o])
        expected_o += max(Q(0),right-left)/2**d
    breaks=sorted({Q(0),Q(1),*[x if x<=Q(1,2) else 2*(1-x) for x in means]})
    expected_b=Q(0)
    for lo,hi in zip(breaks,breaks[1:]):
        mid=(lo+hi)/2
        conditional=Q(1)
        for x in means:
            conditional *= int(mid<=x) if x<=Q(1,2) else (Q(1,2) if mid<=2*(1-x) else Q(1))
        expected_b += (hi-lo)*conditional
    expected_i=Q(1)
    for x in means: expected_i*=x
    return u-expected_o,u-expected_i,u-expected_b

count=0
for d in (2,3):
    for means in combinations_with_replacement([Q(i,12) for i in range(13)],d):
        do,di,db=actual_deficiencies(means)
        gap=min(means)-max(Q(0),sum(means)-d+1)
        assert 18*do+6*di+7*db >= 12*gap
        count+=1
print(f'Actual O/I/B integrals passed for {count} rational boundary/interior tuples (finite evidence).')

# Exact dyadic profiles, including cutoff ties, and actual bit-reversal hit sets.
for L in range(2,31):
    weights=[Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
    bounds=lambda q:Q(L-q+2,2**q)
    for s in range(1,L):
        if not bounds(s+1)<=1<=bounds(s): continue
        mixing=(1-bounds(s+1))/(bounds(s)-bounds(s+1))
        expectation=Q(0); deficiency=Q(0)
        for q,mass in [(s,mixing),(s+1,1-mixing)]:
            for l,weight in enumerate(weights):
                R=0 if l<q else 2**(l-q+1)
                expectation+=mass*weight*R
                deficiency+=mass*weight*sum(min(2**j,R) for j in range(1,l+1))
        assert expectation==1
        assert deficiency==s+Q(L-s,2**s)
    if L<=8:
        order=[int(format(i,f'0{L}b')[::-1],2) for i in range(2**L)]
        for R in range(2**L+1):
            for j in range(1,L+1):
                assert len({v>>(L-j) for v in order[:R]})==min(2**j,R)
print('Dyadic mixture resources and objective passed through L=30; bit-reversal hitting through L=8.')
assert Q(3131,2275)-Q(1,2)==Q(3987,4550)>0
assert 25002-Q(1000**3,23200)<0
print('Finite coefficient-removal logarithmic probability bound and strict margin passed.')
