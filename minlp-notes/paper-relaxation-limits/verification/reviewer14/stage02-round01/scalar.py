"""Exact symbolic identities plus explicitly numerical scalar root checks."""
from pathlib import Path
import re, json
import sympy as s
import mpmath as mp

paper=Path(__file__).resolve().parents[3]
text=(paper/'process/snapshots/stage02-round01/sections/03-cubic-equal-means.tex').read_text()
a,b,c,t=s.symbols('a b c t'); Q=s.Rational
h=6*c**3+27*b*c*c+18*b*b+30*a*c+20*a*b+9*a*a-37*a-Q(79,2)*b-38*c+Q(103,3)
stationary=s.solve([s.diff(h,a),s.diff(h,b)],(a,b))
r=s.factor(h.subs(stationary,simultaneous=True))
bstar=s.solve(s.diff(h,b).subs(a,1),b)[0]
p=s.factor(h.subs({a:1,b:bstar},simultaneous=True))
rows=re.findall(r'\$(p|r)\$&\$\[([^,]+),([^\]]+)\]\$&(\d+)&\$\(([^)]+)\)',text)
coeffs=[]
for kind,lo,hi,den,nums in rows:
    values=[Q(v,den) for v in nums.split(',')]
    coeffs+=values
    actual={'p':p,'r':r}[kind].subs(c,Q(lo)+(Q(hi)-Q(lo))*t)
    reconstruction=sum(values[i]*s.binomial(4,i)*t**i*(1-t)**(4-i) for i in range(5))
    assert s.Poly(actual-reconstruction,t).is_zero
assert len(rows)==5 and min(coeffs)==Q(901,120000)
for k,linear,root,tail in [
    (Q(5,4),Q(11,6)*a+Q(20,27)*c-Q(95,108),(11-6*c*c)/15,(1-c)*(3*c-2)**2*(3*c+7)/135),
    (Q(24,25),Q(41,25)*a+Q(4,5)*c-Q(68,75),(41-25*c*c)/48,(1-c)*(5*c-3)**2*(5*c+11)/480)]:
    assert s.Poly(a*c*c+k*a*a-linear-k*(a-root)**2-tail,a,c).is_zero

# Root search uses log(v) integration and bisection, not the supplied scipy check.
mp.mp.dps=60
numerics=[]
for degree,multiplier in [(2,1),(2,Q(3,2)),(3,1),(7,Q(11,10)),(31,3),(1000,1),(1000,10),(10**12,1),(10**12,100)]:
    M=mp.mpf(str(degree-1))*mp.mpf(str(float(multiplier)))
    L=1+mp.log(M); eta=(degree-1)/M
    def F(v): return -mp.expm1(-(1/v-eta)/L)
    def J(z):
        if z==1:return mp.mpf(0)
        return mp.quad(lambda q: F(mp.exp(q))*mp.exp(q),[mp.log(z),0])
    lo,hi=mp.mpf('1e-12'),mp.mpf(1)
    for _ in range(170):
        mid=(lo+hi)/2
        if J(mid)>mid:lo=mid
        else:hi=mid
    z=(lo+hi)/2; w=mp.lambertw(L*mp.exp(-eta))
    lower=(w-1/(2*w))/L if w>=1 else None
    if lower is not None: assert lower<z
    slope=F(z)
    assert all((J(mp.mpf(i)/20)+slope*i/20)/(1+slope)>=z-mp.mpf('1e-48') for i in range(1,21))
    numerics.append({'degree':degree,'M':str(M),'root':str(z),'lambert_lower':str(lower)})
result={'exact':'five Bernstein rows from frozen text; independently solved minimizers; both two-level identities passed','slack':str(min(coeffs)),'numerical_only':numerics}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: exact symbolic certificates and nine numerical cutoff cases')
