"""Independent exact checks; finite ranges do not establish universal theorems."""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import re
import sympy as S

root = Path(__file__).resolve().parents[3]
tex = (root/'process/snapshots/stage02-round01/sections/03-cubic-equal-means.tex').read_text()
a,b,c,t=S.symbols('a b c t')
h=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2-(37*a+S.Rational(79,2)*b+38*c-S.Rational(103,3))
p=S.expand(h.subs({a:1,b:S.Rational(13,24)-3*c*c/4}))
sol=S.solve([S.diff(h,a),S.diff(h,b)],(a,b))
r=S.expand(h.subs(sol))
rows=re.findall(r'\$(p|r)\$&\$\[([^,]+),([^]]+)\]\$&(\d+)&\$\(([^)]+)\)\$',tex)
assert len(rows)==5
coeffs=[]
for name,lo,hi,D,nums in rows:
    lo,hi,D=S.Rational(lo),S.Rational(hi),int(D)
    vals=[S.Rational(v,D) for v in nums.split(',')]
    coeffs.extend(vals)
    bern=sum(vals[i]*comb(4,i)*t**i*(1-t)**(4-i) for i in range(5))
    assert S.expand({'p':p,'r':r}[name].subs(c,lo+(hi-lo)*t)-bern)==0
assert min(coeffs)==S.Rational(901,120000)
assert S.Rational(161,4)/(S.Rational(223,12)-min(coeffs))==S.Rational(1610000,743033)
for coef,la,lc,const,center,residual in [
 (S.Rational(5,4),S.Rational(11,6),S.Rational(20,27),S.Rational(95,108),(11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135),
 (S.Rational(24,25),S.Rational(41,25),S.Rational(4,5),S.Rational(68,75),(41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480)]:
    assert S.expand(a*c*c+coef*a*a-la*a-lc*c+const-coef*(a-center)**2-residual)==0
print('Exact scalar eliminations, five manuscript Bernstein rows, and both two-level identities passed.')

ties=[]
for L in range(2,81):
    weights=[Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
    B=lambda q: Q(L-q+2,2**q)
    cutoffs=[s for s in range(1,L) if B(s+1)<=1<=B(s)]
    assert cutoffs
    values=[]
    for s in cutoffs:
        mixture=(1-B(s+1))/(B(s)-B(s+1))
        expected_resource=Q(0); expected_gain=Q(0)
        for q,mix in [(s,mixture),(s+1,1-mixture)]:
            for l,weight in enumerate(weights):
                R=0 if l<q else 2**(l-q+1)
                gain=sum(min(2**j,R) for j in range(1,l+1))
                offset=0 if l<=s else 2**(l-s+1)-2
                assert gain==s*R+offset
                expected_resource+=mix*weight*R
                expected_gain+=mix*weight*gain
        assert expected_resource==1
        assert expected_gain==s+Q(L-s,2**s)
        values.append(expected_gain)
    assert len(set(values))==1
    if len(cutoffs)>1: ties.append(L)
print('Exact dyadic resource profiles L=2,...,80 passed; tie cases:',ties)

for n in range(2,25):
    for den in range(2,16):
        for num in range(1,den):
            u=Q(num,den); b=int(n*u); theta=n*u-b
            for d in range(2,n+1):
                q=((1-theta)*comb(b,d)+theta*comb(b+1,d))/comb(n,d)
                sherali=max([Q(0)]+[comb(k,d-1)*n*u-(d-1)*comb(k+1,d) for k in range(d-1,n)])
                assert q*comb(n,d)==sherali
                assert 0<=q<=u**d<u
                assert min(u,(d-1)*(1-u))/(u-q)<2
assert Q(3131,2275)-Q(1,2)==Q(3987,4550)>0
print('Exact finite equal-mean/Sherali comparisons and sampling margin passed.')
