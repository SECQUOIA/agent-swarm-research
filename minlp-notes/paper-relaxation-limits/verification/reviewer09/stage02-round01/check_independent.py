"""Exact supplementary checks; universal arguments are reviewed in the report."""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import re
import sympy as s

root = Path(__file__).resolve().parents[3]
frozen = root / 'process/snapshots/stage02-round01/sections'
text = (frozen / '03-cubic-equal-means.tex').read_text()
a,b,c,t = s.symbols('a b c t')
F = 6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
h = F-(37*a+s.Rational(79,2)*b+38*c-s.Rational(103,3))
p = s.expand(h.subs({a:1,b:s.Rational(13,24)-3*c**2/4}))
critical = s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r = s.expand(h.subs(critical))
rows = re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)', text)
assert len(rows) == 5
coefficients = []
for kind,lo,hi,D,vals in rows:
    lo,hi,D = s.Rational(lo),s.Rational(hi),int(D)
    vals = list(map(int, vals.split(',')))
    poly = sum(s.Rational(v,D)*comb(4,i)*t**i*(1-t)**(4-i) for i,v in enumerate(vals))
    assert s.expand(poly-{'p':p,'r':r}[kind].subs(c,lo+(hi-lo)*t)) == 0
    coefficients.extend(s.Rational(v,D) for v in vals)
delta=min(coefficients)
assert delta == s.Rational(901,120000)
assert (s.Rational(161,4)/(s.Rational(223,12)-delta)) == s.Rational(1610000,743033)
assert s.expand(a*c**2+s.Rational(5,4)*a**2-(s.Rational(11,6)*a+s.Rational(20,27)*c-s.Rational(95,108))-s.Rational(5,4)*(a-(11-6*c**2)/15)**2-(1-c)*(3*c-2)**2*(3*c+7)/135) == 0
assert s.expand(a*c**2+s.Rational(24,25)*a**2-(s.Rational(41,25)*a+s.Rational(4,5)*c-s.Rational(68,75))-s.Rational(24,25)*(a-(41-25*c**2)/48)**2-(1-c)*(5*c-3)**2*(5*c+11)/480) == 0
print('Five frozen Bernstein rows and both two-level identities: exact pass.')

for L in range(2,21):
    B=lambda q:Q(L-q+2,2**q)
    candidates=[q for q in range(1,L) if B(q+1)<=1<=B(q)]
    assert candidates
    values=[]
    weights=[Q(1,2**(l+1)) if l<L else Q(1,2**L) for l in range(L+1)]
    for k in candidates:
        theta=(1-B(k+1))/(B(k)-B(k+1))
        er=Q(0); value=Q(0)
        for q,pq in [(k,theta),(k+1,1-theta)]:
            for l,wl in enumerate(weights):
                R=0 if l<q else 2**(l-q+1)
                Sl=sum(min(2**j,R) for j in range(1,l+1))
                bound=k*R+(0 if l<=k else 2**(l-k+1)-2)
                assert Sl==bound
                er+=pq*wl*R; value+=pq*wl*Sl
        assert er==1
        assert value==k+Q(L-k,2**k)
        values.append(value)
    assert len(set(values))==1
print('Dyadic mixtures, expectations and cutoff ties L=2,...,20: exact pass.')

count=0
for n in range(2,21):
    for denominator in range(2,16):
        for numerator in range(1,denominator):
            u=Q(numerator,denominator); b=int(n*u); theta=n*u-b
            for d in range(2,n+1):
                raw=(1-theta)*comb(b,d)+theta*comb(b+1,d)
                sherali=max([Q(0)]+[comb(k,d-1)*n*u-(d-1)*comb(k+1,d) for k in range(d-1,n)])
                assert raw==sherali
                q=raw/comb(n,d)
                assert q<=u**d<u
                assert min(u,(d-1)*(1-u))/(u-q)<=2
                count+=1
print(f'Sherali/adjacent-count equality and finite ratios: {count} exact cases pass.')
assert Q(943)-2*Q(80947,175)==Q(3131,175)
assert Q(3131,2275)-Q(1,2)>0
assert (25000+2)-Q(1000**3,23200)<0
assert Q(2160)/Q(5372,5)==Q(2700,1343)
print('Finite homogeneous/interior and 25,000-variable arithmetic: exact pass.')
