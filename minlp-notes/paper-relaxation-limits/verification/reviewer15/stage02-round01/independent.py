from fractions import Fraction as Q
from math import comb
from pathlib import Path
import re
import sympy as s

a,b,c,t=s.symbols('a b c t')
F=6*c**3+27*b*c**2+18*b*b+30*a*c+20*a*b+9*a*a
h=F-37*a-s.Rational(79,2)*b-38*c+s.Rational(103,3)
p=s.expand(h.subs({a:1,b:s.Rational(13,24)-3*c*c/4}))
stationary=s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r=s.expand(h.subs(stationary))
tex=Path('process/snapshots/stage02-round01/sections/03-cubic-equal-means.tex').read_text()
rows=re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)',tex)
assert len(rows)==5
slacks=[]
for name,lo,hi,D,nums in rows:
    lo,hi=s.Rational(lo),s.Rational(hi)
    vals=[s.Rational(n,int(D)) for n in nums.split(',')]
    target={'p':p,'r':r}[name].subs(c,lo+(hi-lo)*t)
    bern=sum(v*comb(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(vals))
    assert s.expand(target-bern)==0
    slacks.extend(vals)
assert min(slacks)==s.Rational(901,120000)
assert (s.Rational(161,4)/(s.Rational(223,12)-min(slacks)))==s.Rational(1610000,743033)
assert s.expand(a*c*c+s.Rational(5,4)*a*a-s.Rational(11,6)*a-s.Rational(20,27)*c+s.Rational(95,108)-s.Rational(5,4)*(a-(11-6*c*c)/15)**2-(1-c)*(3*c-2)**2*(3*c+7)/135)==0
assert s.expand(a*c*c+s.Rational(24,25)*a*a-s.Rational(41,25)*a-s.Rational(4,5)*c+s.Rational(68,75)-s.Rational(24,25)*(a-(41-25*c*c)/48)**2-(1-c)*(5*c-3)**2*(5*c+11)/480)==0
for L in range(2,17):
    w=[Q(1,2**(j+1)) if j<L else Q(1,2**L) for j in range(L+1)]
    B=lambda q:Q(L-q+2,2**q)
    for cutoff in range(1,L):
        if not B(cutoff+1)<=1<=B(cutoff):continue
        theta=(1-B(cutoff+1))/(B(cutoff)-B(cutoff+1))
        obj=Q(0); ER=Q(0)
        for q,pr in [(cutoff,theta),(cutoff+1,1-theta)]:
            for l in range(L+1):
                R=0 if l<q else 2**(l-q+1)
                Sl=sum(min(2**j,R) for j in range(1,l+1))
                Fl=0 if l<=cutoff else 2**(l-cutoff+1)-2
                assert Sl==cutoff*R+Fl
                ER+=pr*w[l]*R;obj+=pr*w[l]*Sl
        assert ER==1
        assert obj==cutoff+Q(L-cutoff,2**cutoff)
assert Q(3131,2275)-Q(1,2)==Q(3987,4550)>0
assert 25002-Q(1000**3,23200)<0
assert Q(2160)/(1072+Q(12,5))==Q(2700,1343)
print('Exact independent checks passed: five Bernstein identities; slack; two scalar identities; dyadic profiles L=2,...,16 including all cutoff ties; finite sampling and padding margins.')
