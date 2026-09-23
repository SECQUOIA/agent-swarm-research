"""Check the manuscript's scalar certificates as exact polynomial identities."""
from pathlib import Path
import json
import re
import sympy as s

paper = Path(__file__).resolve().parents[1]
a,b,c,t = s.symbols('a b c t')
Q = s.Rational
F = 6*c**3+27*b*c**2+18*b**2+30*a*c+20*a*b+9*a**2
ell = 37*a+Q(79,2)*b+38*c-Q(103,3)
h = F-ell
H = s.hessian(h,(a,b))
assert H.det() == 248
bstar = Q(13,24)-3*c**2/4
p = (-972*c**4+576*c**3+1404*c**2-768*c+101)/96
assert s.expand(h.subs({a:1,b:bstar})-p) == 0
v,w,q = 30*c-37,27*c**2-Q(79,2),6*c**3-38*c+Q(103,3)
r = (-78732*c**4+212256*c**3-203796*c**2+82032*c-11275)/2976
assert s.expand(q-(18*v**2-20*v*w+9*w**2)/248-r) == 0
# Read all certificate rows from the actual manuscript, not duplicate data.
tex = (paper/'sections/03-cubic-equal-means.tex').read_text()
rows = re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)',tex)
assert len(rows) == 5
coefficients=[]
for kind,lo,hi,den,nums in rows:
    lo,hi,den=Q(lo),Q(hi),int(den)
    vals=[Q(int(n),den) for n in nums.split(',')]
    coefficients.extend(vals)
    bern=sum(vals[i]*s.binomial(4,i)*t**i*(1-t)**(4-i) for i in range(5))
    actual={'p':p,'r':r}[kind].subs(c,lo+(hi-lo)*t)
    assert s.expand(actual-bern) == 0
slack=min(coefficients)
assert slack == Q(901,120000)
assert Q(161,4)/(Q(223,12)-slack) == Q(1610000,743033)
f2=a*c*c+Q(5,4)*a*a
l2=Q(11,6)*a+Q(20,27)*c-Q(95,108)
cert2=Q(5,4)*(a-(11-6*c*c)/15)**2+(1-c)*(3*c-2)**2*(3*c+7)/135
assert s.expand(f2-l2-cert2) == 0
f3=a*c*c+Q(24,25)*a*a
l3=Q(41,25)*a+Q(4,5)*c-Q(68,75)
cert3=Q(24,25)*(a-(41-25*c*c)/48)**2+(1-c)*(5*c-3)**2*(5*c+11)/480
assert s.expand(f3-l3-cert3) == 0
result={'bernstein_rows':len(rows),'uniform_slack':str(slack),
        'cubic_supremum_lower':str(Q(1610000,743033)),
        'scalar_identities':'passed'}
(paper/'verification/stage02-symbolic.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
