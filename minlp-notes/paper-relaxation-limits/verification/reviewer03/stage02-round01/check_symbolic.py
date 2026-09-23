import sympy as s
from pathlib import Path
import re
Q=s.Rational
a,b,c,t=s.symbols('a b c t')
h=6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a*a-37*a-Q(79,2)*b-38*c+Q(103,3)
p=s.expand(h.subs({a:1,b:Q(13,24)-3*c*c/4}))
sol=s.solve([s.diff(h,a),s.diff(h,b)],[a,b])
r=s.factor(h.subs(sol))
source=(Path(__file__).resolve().parents[3]/'process/snapshots/stage02-round01/sections/03-cubic-equal-means.tex').read_text()
rows=re.findall(r'\$(p|r)\$&\$\[([^,]+),([^]]+)\]\$&(\d+)&\$\(([^)]+)\)\$',source)
assert len(rows)==5
coeff=[]
for name,l,u,d,v in rows:
    l,u=Q(l),Q(u)
    v=[Q(x,int(d)) for x in v.split(',')]
    q=sum(v[i]*s.binomial(4,i)*t**i*(1-t)**(4-i) for i in range(5))
    assert s.expand(q-(p if name=='p' else r).subs(c,l+(u-l)*t))==0
    coeff.extend(v)
assert min(coeff)==Q(901,120000)
assert Q(161,4)/(Q(223,12)-min(coeff))==Q(1610000,743033)
assert s.expand(a*c*c+Q(5,4)*a*a-Q(11,6)*a-Q(20,27)*c+Q(95,108)-Q(5,4)*(a-(11-6*c*c)/15)**2-(1-c)*(3*c-2)**2*(3*c+7)/135)==0
assert s.expand(a*c*c+Q(24,25)*a*a-Q(41,25)*a-Q(4,5)*c+Q(68,75)-Q(24,25)*(a-(41-25*c*c)/48)**2-(1-c)*(5*c-3)**2*(5*c+11)/480)==0
print('Independent symbolic elimination; all five actual frozen Bernstein rows; minimum slack; limiting ratio; both two-level identities: passed')
