"""Independent exact checks of frozen Stage 2, plus printed-code replay."""
from pathlib import Path
from fractions import Fraction as Q
from math import comb
import re
import sympy as s

base = Path(__file__).resolve().parents[3]
frozen = base / 'process/snapshots/stage02-round02'
text = (frozen / 'sections/appendix-cubic-certificates.tex').read_text()
blocks = re.findall(r'\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}', text, re.S)
assert len(blocks) == 2
printed = ''.join(blocks)
assert printed == (frozen / 'verification/check_stage02_finite.py').read_text()
exec(compile(printed, 'frozen-printed-certificate', 'exec'), {})

# Derive the five Bernstein identities from the original three-variable form.
a,b,c,t=s.symbols('a b c t')
F=6*c**3+27*b*c**2+18*b*b+30*a*c+20*a*b+9*a*a
ell=37*a+s.Rational(79,2)*b+38*c-s.Rational(103,3)
h=F-ell
p=s.expand(h.subs({a:1,b:s.Rational(13,24)-3*c*c/4}))
sol=s.solve([s.diff(h,a),s.diff(h,b)], [a,b])
r=s.expand(h.subs(sol))
source=(frozen / 'sections/03-cubic-equal-means.tex').read_text()
rows=re.findall(r'\$(p|r)\$&\$\[([^,]+),([^]]+)\]\$&(\d+)&\$\(([^)]+)\)\$', source)
assert len(rows)==5
minimum=1
for kind,lo,hi,den,nums in rows:
    lo,hi=s.Rational(lo),s.Rational(hi)
    vals=[s.Rational(v,int(den)) for v in nums.split(',')]
    polynomial=sum(vals[i]*comb(4,i)*t**i*(1-t)**(4-i) for i in range(5))
    assert s.expand(polynomial-{'p':p,'r':r}[kind].subs(c,lo+(hi-lo)*t))==0
    minimum=min(minimum,*vals)
assert minimum==s.Rational(901,120000)
assert s.Rational(161,4)/(s.Rational(223,12)-minimum)==s.Rational(1610000,743033)
for q,L,center,den,factors in [
    (s.Rational(5,4),s.Rational(11,6)*a+s.Rational(20,27)*c-s.Rational(95,108),(11-6*c*c)/15,135,(3*c-2)**2*(3*c+7)),
    (s.Rational(24,25),s.Rational(41,25)*a+s.Rational(4,5)*c-s.Rational(68,75),(41-25*c*c)/48,480,(5*c-3)**2*(5*c+11))]:
    assert s.expand(a*c*c+q*a*a-L-q*(a-center)**2-(1-c)*factors/den)==0
print('Derived Bernstein and both two-level identities exactly.')

# Rational dyadic resource equality; explicit prefix realization through L=9.
for L in range(2,26):
    weights=[Q(1,2**(j+1)) for j in range(L)]+[Q(1,2**L)]
    B=lambda q: Q(L-q+2,2**q)
    choices=[j for j in range(1,L) if B(j+1)<=1<=B(j)]
    hulls=[]
    for cutoff in choices:
        mix=(1-B(cutoff+1))/(B(cutoff)-B(cutoff+1))
        mean=gap=Q(0)
        for q,pq in [(cutoff,mix),(cutoff+1,1-mix)]:
            for l,pl in enumerate(weights):
                R=0 if l<q else 2**(l-q+1)
                mean+=pq*pl*R
                gap+=pq*pl*sum(min(2**j,R) for j in range(1,l+1))
        assert mean==1 and gap==cutoff+Q(L-cutoff,2**cutoff)
        hulls.append(gap)
    assert len(set(hulls))==1
    if L<=9:
        m=2**L
        order=[int(format(j,f'0{L}b')[::-1],2) for j in range(m)]
        for R in range(m+1):
            for j in range(1,L+1):
                assert len({v>>(L-j) for v in order[:R]})==min(R,2**j)
print('Exact dyadic resource/cutoff checks L=2..25 and all prefix counts L=2..9.')

# Equal-mean candidates and optimizer, including adjacent-integer degeneracies.
total=0
for den in range(2,16):
  for num in range(1,den):
    u=Q(num,den)
    ru=u/(1-u)
    candidates={max(1,ru.numerator//ru.denominator),max(1,-(-ru.numerator//ru.denominator))}
    val=lambda k:min(Q(1),k*(1-u)/u)/(1-u**k)
    optimum=max(val(k) for k in candidates)
    assert optimum<=2 and all(val(k)<=optimum for k in range(1,61))
    for n in range(2,20):
      b=int(n*u); theta=n*u-b
      for d in range(2,n+1):
        q=((1-theta)*comb(b,d)+theta*comb(b+1,d))/comb(n,d)
        assert 0<=q<u**d<u
        assert min(u,(d-1)*(1-u))/(u-q)<2
        total+=1
print(f'Exact equal-mean checks: {total} finite candidates; degree optimizer checked through 60.')
assert Q(3131,2275)-Q(1,2)==Q(3987,4550)>0
assert 25002-Q(1000**3,23200)<0
assert Q(2160)/(Q(1072)+Q(12,5))==Q(2700,1343)
assert (Q(161,4)-Q(135,144)+Q(6,1296))/(Q(223,12)+Q(135,144)+Q(9,1296))==Q(16985,8436)
print('Finite padding, sampling margin, and analytic m=36 arithmetic passed.')
